"""Numbering, label resolution and cross-language parity checks.

Mirrors the amsthm setup in styles/onemath.sty: all statement environments
(definition, theorem, proposition, lemma, corollary, method, example,
notation, remark) share ONE counter numbered within the chapter; exercise
and problem each have their own per-chapter counter; sections use the
standard chapter.section numbering.
"""

from .lexer import STATEMENT_KINDS, ParseError


def anchor_for(label):
    """LaTeX label -> HTML id (colons are invalid in CSS selectors)."""
    return label.replace(":", "-")


def number_chapter(blocks, chapter_number):
    """Walk the tree, assign numbers in place, return the label map.

    Adds to each numbered node:  node["number"] = "1.4"
    Returns  {label: {"kind": ..., "number": ..., "anchor": ...}}
    """
    labels = {}
    shared = 0     # definition-family counter
    exercise = 0
    problem = 0
    section = 0
    subsection = 0
    figure = 0
    equation = 0

    def record(label, kind, number):
        if label is None:
            return
        if label in labels:
            raise ParseError(f"duplicate label {label}")
        labels[label] = {"kind": kind, "number": number,
                         "anchor": anchor_for(label)}

    def walk(nodes):
        nonlocal shared, exercise, problem, section, subsection, figure, \
            equation
        for node in nodes:
            t = node["t"]
            if t == "section":
                if not node["star"]:
                    section += 1
                    subsection = 0
                    node["number"] = f"{chapter_number}.{section}"
                    if node.get("label"):
                        # anchor = the h2's own sec-N-M id
                        labels[node["label"]] = {
                            "kind": "section",
                            "number": node["number"],
                            "anchor": "sec-"
                            + node["number"].replace(".", "-"),
                        }
                continue
            if t == "subsection":
                if not node["star"]:
                    subsection += 1
                    node["number"] = f"{chapter_number}.{section}.{subsection}"
                continue
            if t == "dmath" and node.get("label"):
                equation += 1
                node["number"] = f"{chapter_number}.{equation}"
                record(node["label"], "equation", node["number"])
                continue
            if t == "figure" and node.get("label"):
                figure += 1
                node["number"] = f"{chapter_number}.{figure}"
                record(node["label"], "figure", node["number"])
                continue
            if t == "env":
                kind = node["kind"]
                if kind in STATEMENT_KINDS:
                    shared += 1
                    node["number"] = f"{chapter_number}.{shared}"
                elif kind == "exercise":
                    exercise += 1
                    node["number"] = f"{chapter_number}.{exercise}"
                elif kind == "problem":
                    problem += 1
                    node["number"] = f"{chapter_number}.{problem}"
                record(node.get("label"), kind, node.get("number"))
                walk(node["body"])
            elif t == "list":
                for item in node["items"]:
                    walk(item)
    walk(blocks)
    return labels


def resume_list_starts(blocks):
    """enumitem's [resume] continues the last same-level enumerate: compute
    the HTML <ol start=...> value for every enumerate, in place."""
    def walk(nodes, state):
        for node in nodes:
            t = node["t"]
            if t == "list" and node["kind"] == "enumerate":
                start = state["last"] + 1 if node["resume"] else 1
                node["start"] = start
                state["last"] = start + len(node["items"]) - 1
                for item in node["items"]:
                    # nested enumerates resume among themselves only
                    walk(item, {"last": 0})
            elif t == "list":
                for item in node["items"]:
                    walk(item, state)
            elif t == "env":
                walk(node["body"], state)
    walk(blocks, {"last": 0})


def structure_signature(blocks):
    """Sequence of (env kind, label) — must be identical across languages."""
    sig = []

    def walk(nodes):
        for node in nodes:
            if node["t"] == "env":
                sig.append((node["kind"], node.get("label")))
                walk(node["body"])
            elif node["t"] == "list":
                for item in node["items"]:
                    walk(item)
    walk(blocks)
    return sig


def check_parity(signatures):
    """signatures: {lang: sig}, first language = canonical (EN).

    Translations sometimes lag the canonical edition at the tail (e.g. a
    weekend problem added to EN after the FR/NL translation): each printed
    book follows its own source, so the HTML does too. A lagging edition
    must therefore be a strict PREFIX of the canonical structure — warned
    loudly — while any reordering, kind change or mid-sequence gap is an
    error."""
    langs = list(signatures)
    ref_lang = langs[0]
    ref = signatures[ref_lang]
    for lang in langs[1:]:
        sig = signatures[lang]
        if sig == ref:
            continue
        for k, (a, b) in enumerate(zip(ref, sig)):
            if a != b:
                raise ParseError(
                    f"structure mismatch between {ref_lang} and {lang} at "
                    f"environment #{k + 1}: {a} vs {b}")
        if len(sig) > len(ref):
            raise ParseError(
                f"structure mismatch: {lang} has more environments "
                f"({len(sig)}) than canonical {ref_lang} ({len(ref)})")
        missing = ref[len(sig):]
        print(f"WARNING: {lang} edition lags {ref_lang}: missing "
              f"{len(missing)} trailing environment(s): "
              + ", ".join(f"{kind} {label}" for kind, label in missing))
