#!/usr/bin/env python3
"""Apply an Indonesian line-range patch on top of an English chapter, and
refuse to write the result unless it is structurally identical to its twin.

(Ported to one-math-book from one-physics-book on 2026-11-16 for the pilot
method's Chinese run: pilot_translation/ imports its censuses.)

Lives in tools/ ON PURPOSE. It was written from scratch twice -- once for the
math `id` editions, once for the physics ones -- because both times it lived
only in a session scratchpad and was lost with it. Every census below is a
defect class that shipped, or nearly shipped, in a real edition; none of them
is theoretical, and re-deriving the list costs more than reading it.

This is the tool that produced the Indonesian editions of One Math Book, and
the reason they scored 96/100 rather than reading like post-edited MT: the
translator writes ONLY the prose, as replacements for named line ranges, and
every line that is not named is copied BYTE-IDENTICALLY from English. Labels,
\\cref targets, \\begin{solution}{key}, \\foreach lists, xtick=, \\qty{}{} and
every math display are then physically the same bytes as the canon and cannot
drift.

PATCH FORMAT (one file per stanza; several stanzas per patch file are fine):

    ### parts/grade-9/id/02-arithmetic.tex <<< parts/grade-9/02-arithmetic.tex
    @@ 1
    \\chapter{Aritmetika: Pembagi dan Bilangan Prima}\\label{ch:g9:arith}
    @@ 3-8
    Aritmetika mempelajari bilangan bulat dan cara sebuah bilangan
    membagi bilangan yang lain.
    @@ 40-40

The line numbers are 1-based and refer to the ENGLISH source AFTER unwrapping
(\\omterm{label}{display} -> display); unwrapping never changes the line count,
so they are also the line numbers you see in the file on disk unless a term
link wraps across a line break. A range with no body deletes nothing -- it
replaces those lines with nothing, which is almost always a mistake, so it is
reported. Ranges must be ascending and must not overlap.

WHAT IT REFUSES TO WRITE (each of these cost a real edition real time):

  labels        the ordered \\label{...} sequence must be identical
  envs          the ordered \\begin{env}/\\end{env} sequence must be identical
  solutions     the ordered \\begin{solution}{key} sequence must be identical
  emph          the ordered \\emph adjacency signature must be identical --
                \\emph{x}nya\\index{x} separates the pair and silently
                generates ZERO links for that term, with no gate complaint
  index         the \\index{} count must be identical
  math          the ordered math-span sequence, after blanking \\text{...},
                must be identical. THE MOST VALUABLE ONE: Indonesian absorbs
                numerals into words (keenamnya, keempat sisinya), which
                silently deletes a math span and changes the mathematics
  draw          tikz/pgfplots/circuitikz bodies, after blanking node text,
                axis labels, titles and \\legend{} entries, must be identical.
                Opt out per range
                with "@@ 12-18 !draw" when the range deliberately translates
                symbolic x coords / a \\foreach label list
  delims        per replaced range, the \\[ \\] \\( \\) count must match the
                English lines it replaces. A range covering \\[ but stopping
                one line short of \\] duplicates the delimiter: every whole-file
                census stays happy, the prose gate sees nothing, and the build
                dies on "Bad math environment delimiter". A whole-file census
                MISSES this -- it must be per range
  braces        { } balance must match English
  omterm        no \\omterm may survive (links are regenerated afterwards)
  prose         the script-specific prose gate for the TARGET language must be
                clean on the result, minus the `title` class, which needs the
                written tree. Dispatched on the target path: parts/*/id/ ->
                check_indonesian_prose, /hi/ -> check_hindi_prose, /ar/ ->
                check_arabic_prose. A language with no prose gate (fr, nl, es,
                pt) skips this class; run tools/check_latin_prose.py over the
                written tree instead -- it needs the English twin BY PATH and
                so cannot run against a scratch probe

Usage:
    python3 id_apply.py PATCHFILE [--repo DIR] [--dry-run] [--force-classes c,c]
"""
from __future__ import annotations

import argparse
import io
import os
import pathlib
import re
import subprocess
import sys
import tempfile

# ---------------------------------------------------------------------------
# Reduction helpers. Everything here runs on BOTH sides and is compared.
# ---------------------------------------------------------------------------

OMTERM = re.compile(r"\\omterm\s*\{")


def unwrap_omterm(text: str) -> str:
    """\\omterm{label}{display} -> display, preserving the line count.

    Only the macro name and the braces are removed, so a display that wraps
    across a source line keeps its newline and the numbering stays true.
    """
    out = []
    i = 0
    while True:
        m = OMTERM.search(text, i)
        if not m:
            out.append(text[i:])
            break
        out.append(text[i:m.start()])
        j = m.end() - 1              # at the '{' of the label
        label, j = _group(text, j)
        j = _skip_ws(text, j)
        if j >= len(text) or text[j] != "{":
            # not the shape we expect; copy verbatim and move on
            out.append(text[m.start():j])
            i = j
            continue
        display, j = _group(text, j)
        out.append(display)
        i = j
    return "".join(out)


def _group(text: str, i: int):
    """text[i] is '{'. Return (contents, index just past the matching '}')."""
    assert text[i] == "{"
    depth = 0
    j = i
    while j < len(text):
        c = text[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1:j], j + 1
        j += 1
    return text[i + 1:], len(text)


def _skip_ws(text: str, i: int) -> int:
    while i < len(text) and text[i] in " \t":
        i += 1
    return i


def strip_comments(text: str) -> str:
    """Drop % comments, keeping \\%. Line structure is preserved."""
    out = []
    for line in text.split("\n"):
        j = 0
        keep = line
        while j < len(line):
            if line[j] == "\\":
                j += 2
                continue
            if line[j] == "%":
                keep = line[:j]
                break
            j += 1
        out.append(keep)
    return "\n".join(out)


# \index inside a display is a translated key (math Book 4 zh: \index{谱定理} at the end of a \[...\])
TEXT_IN_MATH = re.compile(r"\\(?:text|mathrm|textrm|mbox|textup|index)\s*\{")


def _blank_text_macros(s: str) -> str:
    """Replace \\text{...} contents with a placeholder: the words inside are
    prose and are SUPPOSED to differ; the surrounding mathematics is not."""
    out = []
    i = 0
    while True:
        m = TEXT_IN_MATH.search(s, i)
        if not m:
            out.append(s[i:])
            break
        out.append(s[i:m.start()])
        j = m.end() - 1
        _, j = _group(s, j)
        out.append("\\text{@}")
        i = j
    return "".join(out)


def math_spans(text: str):
    """Ordered list of math spans, with \\text{...} blanked.

    Covers $...$, $$...$$, \\[...\\], \\(...\\) and the amsmath display
    environments, which is everything these books use.
    """
    t = strip_comments(text)
    spans = []
    i = 0
    n = len(t)
    while i < n:
        c = t[i]
        if c == "\\":
            if t.startswith("\\[", i):
                k = t.find("\\]", i + 2)
                k = n if k < 0 else k + 2
                spans.append(_blank_text_macros(t[i:k]))
                i = k
                continue
            if t.startswith("\\(", i):
                k = t.find("\\)", i + 2)
                k = n if k < 0 else k + 2
                spans.append(_blank_text_macros(t[i:k]))
                i = k
                continue
            i += 2
            continue
        if c == "$":
            dollar = "$$" if t.startswith("$$", i) else "$"
            k = i + len(dollar)
            while k < n:
                if t[k] == "\\":
                    k += 2
                    continue
                if t.startswith(dollar, k):
                    k += len(dollar)
                    break
                k += 1
            spans.append(_blank_text_macros(t[i:k]))
            i = k
            continue
        i += 1
    for env in ("equation", "equation*", "align", "align*", "gather",
                "gather*", "multline", "multline*", "eqnarray"):
        for m in re.finditer(r"\\begin\{%s\}(.*?)\\end\{%s\}"
                             % (re.escape(env), re.escape(env)), t, re.S):
            spans.append(_blank_text_macros(m.group(1)))
    return spans


ENV = re.compile(r"\\(begin|end)\s*\{([^}]*)\}")
LABEL = re.compile(r"\\label\s*\{([^}]*)\}")
SOLUTION = re.compile(r"\\begin\s*\{solution\}\s*\{([^}]*)\}")
INDEX = re.compile(r"\\index\s*\{")
EMPH = re.compile(r"\\emph\s*\{")


def env_seq(text):
    return [(m.group(1), m.group(2)) for m in ENV.finditer(strip_comments(text))]


def label_seq(text):
    return [m.group(1) for m in LABEL.finditer(strip_comments(text))]


def solution_seq(text):
    return [m.group(1) for m in SOLUTION.finditer(strip_comments(text))]


def index_count(text):
    return len(INDEX.findall(strip_comments(text)))


def emph_signature(text):
    """For each \\emph{...}: is it immediately followed by \\index{...}?

    The harvester needs the pair ADJACENT. Indonesian invites
    \\emph{selubung}nya\\index{selubung}, which is not adjacent, is invisible
    to every gate, and generates zero links for that term.
    """
    t = strip_comments(text)
    sig = []
    for m in EMPH.finditer(t):
        _, j = _group(t, m.end() - 1)
        sig.append(bool(re.match(r"\s*\\index\s*\{", t[j:j + 12])))
    return sig


DRAW_ENVS = ("tikzpicture", "axis", "circuitikz")
NODE_TEXT = re.compile(r"node\s*(\[[^\]]*\])?\s*(\([^)]*\))?\s*(at\s*\([^)]*\))?\s*\{")
# pgfplots' \legend{...} and \addlegendentry{...} MACROS. AXIS_STR below only knows the KEY form,
# "legend entries=", so a legend used to be compared BYTE-FOR-BYTE as drawing
# code: translating one -- which you must, it is visible text -- forced
# "@@ N !draw" and opted the whole file out of the drawing census. That is the
# exact inverse of the prose gates, which could not see a \legend at all.
# Blank it here so a translated legend is legal and the byte-identity
# guarantee is kept for every other line of the picture.
LEGEND_MACRO = re.compile(r"\\(?:legend|addlegendentry)\s*\{")
AXIS_STR = re.compile(
    r"(xlabel|ylabel|zlabel|title|legend entries|symbolic x coords|"
    r"symbolic y coords|xticklabels|yticklabels|nodes near coords)\s*=\s*")


def draw_bodies(text):
    """Drawing code with every visible string blanked: coordinates, options
    and styles must be byte-identical, the words inside must not."""
    t = strip_comments(text)
    bodies = []
    for env in DRAW_ENVS:
        for m in re.finditer(r"\\begin\{%s\}(.*?)\\end\{%s\}"
                             % (env, env), t, re.S):
            body = m.group(1)
            body = _blank_braced(body, NODE_TEXT)
            body = _blank_braced(body, LEGEND_MACRO)
            body = _blank_axis_strings(body)
            body = _blank_text_macros(body)
            bodies.append(re.sub(r"\s+", " ", body).strip())
    return bodies


def _blank_braced(s, opener):
    out = []
    i = 0
    while True:
        m = opener.search(s, i)
        if not m:
            out.append(s[i:])
            break
        out.append(s[i:m.end() - 1])
        _, j = _group(s, m.end() - 1)
        out.append("{@}")
        i = j
    return "".join(out)


def _blank_axis_strings(s):
    out = []
    i = 0
    while True:
        m = AXIS_STR.search(s, i)
        if not m:
            out.append(s[i:])
            break
        out.append(s[i:m.end()])
        j = m.end()
        if j < len(s) and s[j] == "{":
            _, j = _group(s, j)
            out.append("{@}")
        else:
            k = j
            while k < len(s) and s[k] not in ",]\n":
                k += 1
            out.append("@")
            j = k
        i = j
    return "".join(out)


DELIMS = (r"\[", r"\]", r"\(", r"\)")


def delim_counts(text):
    t = strip_comments(text)
    return tuple(t.count(d) for d in DELIMS)


def brace_balance(text):
    t = strip_comments(text)
    t = re.sub(r"\\[{}]", "", t)
    return t.count("{") - t.count("}")


# ---------------------------------------------------------------------------
# Patch parsing
# ---------------------------------------------------------------------------

STANZA = re.compile(r"^###\s+(\S+)\s+<<<\s+(\S+)\s*$")
RANGE = re.compile(r"^@@\s+(\d+)(?:-(\d+))?\s*(!\w+(?:,!?\w+)*)?\s*$")


def parse_patch(path):
    stanzas = []
    cur = None
    rng = None
    for raw in pathlib.Path(path).read_text(encoding="utf-8").split("\n"):
        m = STANZA.match(raw)
        if m:
            if cur:
                stanzas.append(cur)
            cur = {"target": m.group(1), "source": m.group(2), "ranges": []}
            rng = None
            continue
        m = RANGE.match(raw)
        if m and cur is not None:
            lo = int(m.group(1))
            hi = int(m.group(2)) if m.group(2) else lo
            opts = set((m.group(3) or "").replace("!", "").split(",")) - {""}
            rng = {"lo": lo, "hi": hi, "body": [], "opts": opts}
            cur["ranges"].append(rng)
            continue
        if rng is not None:
            rng["body"].append(raw)
        elif cur is not None and raw.strip():
            die("stray text before the first @@ in %s: %r" % (cur["target"], raw[:60]))
    if cur:
        stanzas.append(cur)
    for st in stanzas:
        for r in st["ranges"]:
            while r["body"] and r["body"][-1] == "":
                r["body"].pop()
    return stanzas


def die(msg):
    print("id_apply: %s" % msg, file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# Apply + verify
# ---------------------------------------------------------------------------

def build(en_lines, ranges):
    out = []
    pos = 0
    prev_hi = 0
    for r in ranges:
        lo, hi = r["lo"], r["hi"]
        if lo <= prev_hi:
            return None, "range %d-%d overlaps or precedes %d" % (lo, hi, prev_hi)
        if hi < lo:
            return None, "range %d-%d is inverted" % (lo, hi)
        if hi > len(en_lines):
            return None, "range %d-%d runs past the file (%d lines)" % (
                lo, hi, len(en_lines))
        out.extend(en_lines[pos:lo - 1])
        out.extend(r["body"])
        pos = hi
        prev_hi = hi
    out.extend(en_lines[pos:])
    return out, None


CLASSES = ("labels", "envs", "solutions", "emph", "index", "math", "draw",
           "delims", "braces", "omterm", "prose")


def window(x, y):
    """A readable excerpt of two long strings around their first difference."""
    if not isinstance(x, str) or not isinstance(y, str) or len(x) < 90:
        return repr(x)[:150], repr(y)[:150]
    i = 0
    while i < min(len(x), len(y)) and x[i] == y[i]:
        i += 1
    lo = max(0, i - 30)
    return repr(x[lo:i + 60]), repr(y[lo:i + 60])


def first_diff(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i, x, y
    if len(a) != len(b):
        i = min(len(a), len(b))
        return i, (a[i] if i < len(a) else None), (b[i] if i < len(b) else None)
    return None


def verify(en_text, id_text, ranges, en_lines, id_lines, gate, force,
           target=""):
    problems = []

    def cmp(cls, name, fa, brief=lambda v: repr(v)[:120]):
        if cls in force:
            return
        a, b = fa(en_text), fa(id_text)
        if a == b:
            return
        d = first_diff(a, b) if isinstance(a, list) else None
        if d:
            wx, wy = window(d[1], d[2])
            extra = "\n        first divergence at #%d:\n           EN %s\n           ID %s" % (
                d[0], wx, wy)
        else:
            extra = "\n        EN %s / ID %s" % (brief(a), brief(b))
        problems.append("%-9s %s differs%s" % (cls, name, extra))

    cmp("labels", "ordered \\label{} sequence", label_seq)
    cmp("envs", "ordered \\begin/\\end sequence", env_seq)
    cmp("solutions", "ordered \\begin{solution}{} sequence", solution_seq)
    cmp("emph", "\\emph/\\index adjacency signature", emph_signature)
    cmp("index", "\\index{} count", index_count)
    cmp("math", "ordered math-span sequence", math_spans)
    cmp("draw", "tikz/axis drawing code", draw_bodies)

    if "braces" not in force and brace_balance(en_text) != brace_balance(id_text):
        problems.append("braces   { } balance %d -> %d"
                        % (brace_balance(en_text), brace_balance(id_text)))

    if "omterm" not in force and OMTERM.search(id_text):
        problems.append("omterm   a \\omterm survived; write the display, "
                        "the link layer is regenerated later")

    # Per-range delimiter counts. A whole-file census cannot see this.
    if "delims" not in force:
        for r in ranges:
            en_chunk = "\n".join(en_lines[r["lo"] - 1:r["hi"]])
            id_chunk = "\n".join(r["body"])
            a, b = delim_counts(en_chunk), delim_counts(id_chunk)
            if a != b:
                problems.append(
                    "delims   range %d-%d: \\[ \\] \\( \\) counts %s -> %s "
                    "(a range covering \\[ but not \\] duplicates the delimiter)"
                    % (r["lo"], r["hi"], a, b))
        if not any(r["body"] for r in ranges):
            problems.append("delims   every range has an empty body")

    if gate and "prose" not in force:
        problems.extend(run_prose_gate(id_text, target))
    return problems


# The script-specific prose gate to run, by the language directory the file is
# being written into. Only a target whose script differs from English has one:
# gates 5-8 all ask "is this the wrong script / an English word?", and for fr,
# nl, es and pt the answer needs the English TWIN, which a scratch probe file
# has not got. Those editions are covered after the write by
# tools/check_latin_prose.py (gate 9) over the real tree.
PROSE_GATES = {
    "id": "check_indonesian_prose",
    "hi": "check_hindi_prose",
    "ar": "check_arabic_prose",
    "zh": "check_chinese_prose",
}


def run_prose_gate(id_text, target=""):
    """The target language's prose gate, minus the `title` class.

    `title` compares against the English twin found BY PATH, so against a temp
    file it finds no twin (or reports every title as identical). It is run over
    the written tree by the gate script proper.

    Returns nothing for a language that has no script-specific gate.
    """
    import importlib
    lang = next((l for l in PROSE_GATES
                 if "/%s/" % l in target.replace(os.sep, "/")), None)
    if lang is None:
        return []
    mod = importlib.import_module(PROSE_GATES[lang])
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "probe.tex"
        p.write_text(id_text, encoding="utf-8")
        findings = []
        mod.check_file(p, findings)
    return ["prose    %s: %s" % (cls, msg)
            for _rel, _line, cls, msg in findings if cls != "title"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("patch")
    ap.add_argument("--repo", default=str(pathlib.Path(__file__).resolve().parent.parent),
                    help="repository root (default: the repo this script lives in)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-gate", action="store_true",
                    help="skip the prose gate (do not use to ship)")
    ap.add_argument("--force-classes", default="",
                    help="comma-separated classes to skip, e.g. draw,math. "
                         "Every use must be justified in the score file.")
    args = ap.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    sys.path.insert(0, str(repo / "tools"))
    force = set(x.strip() for x in args.force_classes.split(",") if x.strip())
    bad = force - set(CLASSES)
    if bad:
        die("unknown class(es) %s; known: %s" % (sorted(bad), ", ".join(CLASSES)))

    stanzas = parse_patch(args.patch)
    if not stanzas:
        die("no ### stanza in %s" % args.patch)

    failed = 0
    for st in stanzas:
        src = repo / st["source"]
        dst = repo / st["target"]
        if not src.is_file():
            print("REJECT %s\n         source not found: %s" % (st["target"], src))
            failed += 1
            continue
        raw = src.read_text(encoding="utf-8")
        en_text = unwrap_omterm(raw)
        if en_text.count("\n") != raw.count("\n"):
            print("REJECT %s\n         unwrapping \\omterm changed the line count"
                  % st["target"])
            failed += 1
            continue
        en_lines = en_text.split("\n")

        id_lines, err = build(en_lines, st["ranges"])
        if err:
            print("REJECT %s\n         %s" % (st["target"], err))
            failed += 1
            continue
        id_text = "\n".join(id_lines)

        # A "@@ 12-18 !draw" range opts THIS FILE out of that class. The
        # commonest legitimate use is a range that deliberately translates
        # symbolic x coords or a \foreach label list inside drawing code.
        local = set(force)
        for r in st["ranges"]:
            local |= r["opts"]
        unknown = local - set(CLASSES)
        if unknown:
            print("REJECT %s\n         unknown !class %s" % (st["target"],
                                                             sorted(unknown)))
            failed += 1
            continue
        problems = verify(en_text, id_text, st["ranges"], en_lines, id_lines,
                          not args.no_gate, local, st["target"])
        if problems:
            print("REJECT %s  (%d range(s))" % (st["target"], len(st["ranges"])))
            for p in problems[:12]:
                print("         " + p)
            if len(problems) > 12:
                print("         ... %d more" % (len(problems) - 12))
            failed += 1
            continue

        if args.dry_run:
            print("ok     %s  (%d range(s), %d lines)"
                  % (st["target"], len(st["ranges"]), len(id_lines)))
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(id_text, encoding="utf-8")
            print("wrote  %s  (%d range(s), %d lines)"
                  % (st["target"], len(st["ranges"]), len(id_lines)))

    if failed:
        print("\n%d of %d file(s) REJECTED -- nothing was written for those."
              % (failed, len(stanzas)))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
