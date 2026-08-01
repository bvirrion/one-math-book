#!/usr/bin/env python3
"""Hindi-specific hygiene gate for a translated tree.

check_translation.sh proves *structure*: same files, same labels, same
environment census. Its two prose gates are Latin-oriented and score nothing
on Devanagari -- gate 6 looks for TeX accent escapes (\\'e), which Hindi never
writes, and the drafty-"..." gate is script-agnostic. So a Hindi tree can be
structurally perfect and still be raw machine translation.

These are the failure classes the 2026-07-24 Hindi machine translation left
behind, each of which this script detects:

  1. residual English in visible text  -- \\text{ thousands}, TikZ nodes
     reading {tens} {units}, English chapter titles, English \\index keys.
     137 of 177 math bodies and 29 of 35 physics bodies carried these.
  2. transliterated English function words -- "द" for *the*, "ए" for *a*,
     "ऑफ", "एंड". A Hindi sentence never needs an article.
  3. Latin full stop where Hindi ends a sentence with a danda (।). The MT
     output mixed both, sometimes inside one paragraph.
  4. MT-injected spaces inside inline math -- "$P $ और $ Q $", which changes
     spacing in the output and is never what the English source wrote.
  5. a thin space splitting a number away from its noun -- the MT produced
     \\chapter{10 तक की संख्या\\,000} from "Numbers up to 10\\,000".

Usage:
    python3 tools/check_hindi_prose.py parts/grade-3/hi parts/grade-3/solutions/hi
    python3 tools/check_hindi_prose.py --quiet <dir> ...

Exit status is 1 if anything was flagged. Called by check_translation.sh for
lang == hi; safe to run by hand on a single directory while translating.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

DEVANAGARI = r"\u0900-\u097F"
DEV_CHAR = re.compile(f"[{DEVANAGARI}]")

# ---------------------------------------------------------------------------
# What is allowed to stay in Latin script inside visible Hindi text.
# ---------------------------------------------------------------------------
# Brand, markup names the prose legitimately mentions, and SI/unit symbols
# that Hindi textbooks print in Latin. Proper nouns are deliberately NOT
# whitelisted: a Hindi edition transliterates them (Fourier -> फूरिये).
ALLOWED_WORDS = {
    "one", "course", "com", "www", "http", "https",
    "tex", "latex", "pdf", "html",
    "si", "iso", "atp", "dna", "rna", "led", "usb", "gps", "ph",
}

# Unit and symbol strings that may appear bare in a table cell or node.
ALLOWED_UNITS = {
    "m", "s", "kg", "g", "mg", "km", "cm", "mm", "nm", "um",
    "dm", "dam", "hm",
    "n", "j", "w", "hz", "pa", "mol", "cd", "k", "a", "v", "c", "t",
    "wb", "f", "ev", "min", "h", "l", "ml", "rad", "sr", "bq", "gy", "sv",
    "kwh", "kj", "mj", "gpa", "mpa", "kpa", "khz", "mhz", "ghz",
}

LATIN_WORD = re.compile(r"[A-Za-z][A-Za-z'\-]{1,}")

# Short English that the >=3-letter rule below cannot see. A blanket lower
# threshold is not an option: one- and two-letter Latin tokens are usually
# legitimate symbols (x_{\text{m}}, R_{\text{s}}, the dioptre \text{D}), so
# only a named list is safe. The Physics 2 agent found 19 of these hiding
# under the threshold after the 100 visible ones were fixed.
SHORT_ENGLISH = {
    "so", "in", "of", "to", "is", "at", "by", "an", "or", "if", "no",
    "we", "it", "as", "be", "do", "on", "up", "and", "the", "for",
    "ie", "eg", "cf", "vs", "eq", "nc", "wrt", "resp",
}
# "th" is deliberately absent: it collides with the element symbol Th
# (thorium) and with coin-outcome labels like TH. Matched lowercase-only for
# the same reason -- capitalised short tokens are symbols, not words.

# "i.e." / "e.g." never match LATIN_WORD: the dot splits them into single
# letters, which are skipped as symbols.
DOTTED_ABBREV = re.compile(r"\b(?:i\.e\.|e\.g\.|etc\.|cf\.|viz\.)")

# ---------------------------------------------------------------------------
# Macros whose arguments are technical and must not be read as prose.
# ---------------------------------------------------------------------------
# name -> number of braced arguments to drop wholesale.
TECHNICAL_MACROS = {
    "label": 1, "ref": 1, "cref": 1, "Cref": 1, "crefrange": 2,
    "Crefrange": 2, "eqref": 1, "pageref": 1, "nameref": 1, "autoref": 1,
    "input": 1, "include": 1, "includegraphics": 1, "usepackage": 1,
    "documentclass": 1, "bibliography": 1, "bibliographystyle": 1,
    "ominput": 2, "ominputsol": 2, "omsollink": 1,
    "qty": 2, "unit": 1, "num": 1, "ang": 1, "SI": 2, "si": 1,
    "newcommand": 2, "renewcommand": 2, "providecommand": 2,
    "color": 1, "textcolor": 1, "definecolor": 3, "pgfplotsset": 1,
    "hypersetup": 1, "setlength": 2, "addtolength": 2, "url": 1,
}

# \omterm{def:label}{visible display} -- first arg technical, second is prose.
# \href{url}{text} likewise.
SPLIT_MACROS = {"omterm": (1, 1), "href": (1, 1), "hyperref": (1, 1)}

# Environments whose optional argument is a visible title (so it IS prose).
TITLED_ENVS = {
    "definition", "theorem", "proposition", "lemma", "corollary", "example",
    "remark", "method", "notation", "exercise", "problem", "proof",
    "omfigure", "figure", "table", "solution",
}

# Environments whose body is drawing code, not prose. Node text and axis
# labels are pulled out of them separately.
DRAWING_ENVS = {"tikzpicture", "axis", "semilogxaxis", "semilogyaxis",
                "loglogaxis", "groupplot", "scope", "circuitikz"}

MATH_ENVS = {"equation", "equation*", "align", "align*", "gather", "gather*",
             "multline", "multline*", "eqnarray", "eqnarray*", "array",
             "cases", "split", "aligned", "gathered", "pmatrix", "bmatrix",
             "vmatrix", "matrix", "smallmatrix"}

MATH_PLACEHOLDER = "\x00"

# Environments taking a column specification ({c|ccc}) before their body.
COLSPEC_ENVS = {"tabular", "tabular*", "tabularx", "array", "longtable"}

# Text-bearing keys inside a drawing environment.
TIKZ_TEXT_KEYS = re.compile(
    r"\b(?:xlabel|ylabel|zlabel|title|legend\s+entries|label)\s*=\s*"
    r"(\{[^{}]*\}|[^,\]\n]+)"
)
# A node's braced group is its visible label -- but "node" also occurs inside
# pgfplots STYLE KEYS, as in "every node near coord/.append style={font=\small}",
# where the following group is formatting, not text. Exclude a "node" preceded
# by "every", or with a "/." key path before its group.
TIKZ_NODE = re.compile(
    r"(?<!every\s)\bnode\b(?![^{;]*/\.)[^{;]*?(\{(?:[^{}]|\{[^{}]*\})*\})"
)


def strip_comments(text: str) -> str:
    out = []
    for line in text.split("\n"):
        i, esc = 0, False
        cut = len(line)
        while i < len(line):
            ch = line[i]
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == "%":
                cut = i
                break
            i += 1
        out.append(line[:cut])
    return "\n".join(out)


def match_group(text: str, start: int, open_ch: str, close_ch: str):
    """Return (inner, end_index) for a balanced group starting at text[start]."""
    if start >= len(text) or text[start] != open_ch:
        return None, start
    depth, i, esc = 0, start, False
    while i < len(text):
        ch = text[i]
        if esc:
            esc = False
        elif ch == "\\":
            esc = True
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    return None, start


# Text-mode macros used INSIDE math. Their argument is prose a reader sees, so
# it must be Hindi -- "$x \text{ metres}$" is as much residual English as a bare
# sentence. Blanking math wholesale hid 19 of these across 7 files that every
# other gate called finished. \operatorname and \mathrm are deliberately absent:
# their arguments are operator names (sin, det, d) and stay Latin.
MATH_TEXT_MACRO = re.compile(
    r"\\(?:text|textrm|textbf|textit|textsf|textnormal|mbox|hbox)\s*\{")


def extract_math_text(body: str) -> str:
    """Pull \\text{...} arguments out of a math span so they get scanned."""
    out = []
    for m in MATH_TEXT_MACRO.finditer(body):
        inner, _ = match_group(body, m.end() - 1, "{", "}")
        if inner:
            out.append(inner)
    return " ".join(out)


def blank_math(text: str, findings: list, path: str) -> str:
    """Replace math spans with a placeholder, flagging MT spacing damage.

    The argument of a text-mode macro inside the span is kept: it is prose.
    """
    out, i = [], 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "\\" and i + 1 < n:
            nxt = text[i + 1]
            if nxt in "[(":
                closer = "\\]" if nxt == "[" else "\\)"
                j = text.find(closer, i + 2)
                j = n if j < 0 else j + 2
                out.append(MATH_PLACEHOLDER)
                out.append(" " + extract_math_text(text[i + 2:j]) + " " + MATH_PLACEHOLDER)
                i = j
                continue
            out.append(text[i:i + 2])
            i += 2
            continue
        if ch == "$":
            dollars = 2 if text.startswith("$$", i) else 1
            delim = "$" * dollars
            j = i + dollars
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text.startswith(delim, j):
                    break
                j += 1
            body = text[i + dollars:j]
            # A trailing space that terminates a control word ("$\star $") is
            # ordinary TeX and appears in the English sources too; only a
            # leading space, or a trailing one after an ordinary token, is the
            # MT fingerprint we are after ("$P $ और $ Q $").
            bad_lead = bool(body) and body[0] == " "
            bad_trail = (bool(body) and body[-1] == " "
                         and not re.search(r"\\[A-Za-z]+\s*$", body))
            if dollars == 1 and (bad_lead or bad_trail):
                findings.append(
                    (path, line_of(text, i), "math-space",
                     f"MT space inside inline math: ${body[:40]}$"))
            out.append(MATH_PLACEHOLDER)
            out.append(" " + extract_math_text(body) + " " + MATH_PLACEHOLDER)
            i = min(j + dollars, n)
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


MAX_NESTING = 4


def nested_text(fragment: str, depth: int) -> str:
    """Reduce a fragment that is itself LaTeX.

    A node label, an environment's optional title and an \\omterm display are
    all markup, not plain strings: "{size (\\unit{m})}" must not report *unit*
    as residual English, and a generated \\omterm inside a weekend-problem
    title must not leak its label into the prose stream. Findings are
    discarded here -- the caller's own scan of the reduced text reports them,
    with the line numbers of the enclosing file.
    """
    if depth >= MAX_NESTING or not fragment or "\\" not in fragment:
        return fragment
    return visible_text(fragment, [], "<nested>", depth + 1)


def extract_drawing_text(body: str, depth: int = 0) -> str:
    """Pull the visible strings out of tikz/pgfplots/circuitikz drawing code."""
    pieces = [m.group(1) for m in TIKZ_NODE.finditer(body)]
    pieces += [m.group(1) for m in TIKZ_TEXT_KEYS.finditer(body)]
    return " \n ".join(nested_text(p.strip("{}"), depth) for p in pieces)


def visible_text(text: str, findings: list, path: str, depth: int = 0) -> str:
    """Reduce a LaTeX body to the text a reader actually sees."""
    text = blank_math(text, findings, path)
    out, i, n = [], 0, len(text)

    while i < n:
        ch = text[i]

        if ch != "\\":
            if ch in "{}":
                out.append(" ")
            else:
                out.append(ch)
            i += 1
            continue

        m = re.match(r"\\([A-Za-z@]+)\*?", text[i:])
        if not m:
            i += 2 if i + 1 < n else 1
            continue
        name = m.group(1)
        j = i + m.end()

        if name == "begin":
            env, j = match_group(text, skip_ws(text, j), "{", "}")
            env = (env or "").strip()
            if env in DRAWING_ENVS or env in MATH_ENVS:
                end_tag = "\\end{" + env + "}"
                k = text.find(end_tag, j)
                k = n if k < 0 else k
                if env in DRAWING_ENVS:
                    out.append(" " + extract_drawing_text(text[j:k], depth) + " ")
                else:
                    out.append(MATH_PLACEHOLDER)
                    out.append(" " + extract_math_text(text[j:k]) + " " + MATH_PLACEHOLDER)
                i = min(k + len(end_tag), n)
                continue
            j = skip_ws(text, j)
            if text[j:j + 1] == "[":
                inner, j = match_group(text, j, "[", "]")
                if env in TITLED_ENVS and inner:
                    out.append(" " + nested_text(inner, depth) + " ")
            # solution's {key} and tabular's {c|ccc} arguments are technical
            j2 = skip_ws(text, j)
            if (env == "solution" or env in COLSPEC_ENVS) and text[j2:j2 + 1] == "{":
                _, j = match_group(text, j2, "{", "}")
            i = j
            continue

        if name == "end":
            _, j = match_group(text, skip_ws(text, j), "{", "}")
            i = j
            continue

        if name in SPLIT_MACROS:
            drop, keep = SPLIT_MACROS[name]
            for _ in range(drop):
                _, j = match_group(text, skip_ws(text, j), "{", "}")
            for _ in range(keep):
                inner, j = match_group(text, skip_ws(text, j), "{", "}")
                if inner:
                    out.append(" " + nested_text(inner, depth) + " ")
            i = j
            continue

        if name in TECHNICAL_MACROS:
            j = skip_ws(text, j)
            if text[j:j + 1] == "[":
                _, j = match_group(text, j, "[", "]")
            for _ in range(TECHNICAL_MACROS[name]):
                _, j = match_group(text, skip_ws(text, j), "{", "}")
            i = j
            continue

        if name == "index":
            inner, j = match_group(text, skip_ws(text, j), "{", "}")
            if inner:
                out.append(" " + nested_text(
                    inner.replace("!", " ").replace("@", " "), depth) + " ")
            i = j
            continue

        if name == "item":
            j = skip_ws(text, j)
            if text[j:j + 1] == "[":
                _, j = match_group(text, j, "[", "]")
            out.append(" ")
            i = j
            continue

        # Any other macro: drop the control word and the bracket options it
        # may carry (those are keys, not prose), keep braced groups as text.
        j = skip_ws(text, j)
        if text[j:j + 1] == "[":
            _, j = match_group(text, j, "[", "]")
        out.append(" ")
        i = j

    return "".join(out)


def skip_ws(text: str, i: int) -> int:
    while i < len(text) and text[i] in " \t":
        i += 1
    return i


# Transliterated English function words. Hindi has no articles, so "द"/"ए"
# standing alone are always the MT leaving *the*/*a* behind.
#
# "इन" is deliberately NOT here: it is the ordinary Hindi oblique demonstrative
# ("इन संख्याओं में" = among these numbers), not transliterated English *in*.
# Listing it forced agents to write "उन" instead and shift the meaning.
TRANSLITERATED_ARTICLES = {
    "द": "the", "ए": "a/an", "ऑफ": "of", "एंड": "and", "इज": "is",
    "आर": "are", "फॉर": "for", "विद": "with", "टू": "to",
}


def _locate(body: str, token: str, seen_before: dict) -> int:
    """Line of `token` in the ORIGINAL file.

    Findings are detected in the reduced stream, whose line numbers do not
    survive the reduction: a multi-line math span collapses to one placeholder
    character, so every later line number drifts. Map back by finding the
    n-th occurrence of the token in the source, n being how many times this
    token has already been reported for this file.
    """
    n = seen_before.get(token, 0)
    seen_before[token] = n + 1
    start = 0
    for _ in range(n + 1):
        idx = body.find(token, start)
        if idx < 0:
            break
        start = idx + 1
    else:
        return body.count("\n", 0, idx) + 1
    return body.count("\n", 0, max(idx, 0)) + 1 if idx >= 0 else 1


def check_file(path: pathlib.Path, findings: list) -> None:
    raw = path.read_text(encoding="utf-8")
    rel = str(path)
    body = strip_comments(raw)
    seen = visible_text(body, findings, rel)
    _occ: dict = {}

    # 1. residual English in visible text
    for m in LATIN_WORD.finditer(seen):
        word = m.group(0)
        low = word.lower()
        if low in ALLOWED_WORDS or low in ALLOWED_UNITS:
            continue
        if word.islower() and low in SHORT_ENGLISH:
            findings.append((rel, _locate(body, word, _occ),
                             "english", f"English in visible text: {word!r}"))
            continue
        if word.isupper() and len(word) <= 4:
            continue        # acronyms printed in Latin (SI, ATP)
        if len(word) < 3:
            continue        # stray single symbols
        findings.append((rel, _locate(body, word, _occ),
                         "english", f"English in visible text: {word!r}"))

    for m in DOTTED_ABBREV.finditer(seen):
        findings.append((rel, _locate(body, m.group(0), _occ),
                         "english",
                         f"English abbreviation in visible text: {m.group(0)!r}"))

    # 2. transliterated English function words
    for token, gloss in TRANSLITERATED_ARTICLES.items():
        for m in re.finditer(rf"(?<![{DEVANAGARI}]){token}(?![{DEVANAGARI}])", seen):
            findings.append((rel, _locate(body, token, _occ),
                             "translit",
                             f"transliterated English {gloss!r}: {token!r}"))

    # 3. Latin full stop closing a Devanagari sentence (use danda ।)
    for m in re.finditer(rf"[{DEVANAGARI}][)\"'\s]*\.(?=\s|$)", seen):
        findings.append((rel, seen[:m.start()].count("\n") + 1,
                         "danda",
                         "sentence ends with '.' after Devanagari (use ।)"))

    # 5. thin space splitting a number from its noun
    for m in re.finditer(rf"[{DEVANAGARI}]\s*\\,\s*\d", body):
        findings.append((rel, body[:m.start()].count("\n") + 1,
                         "split-number",
                         "\\, between Devanagari and digits (split number?)"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dirs", nargs="+", help="directories of .tex files")
    ap.add_argument("--quiet", action="store_true",
                    help="print only the per-class summary")
    ap.add_argument("--max-detail", type=int, default=8,
                    help="detail lines to show per class (default 8)")
    args = ap.parse_args()

    findings: list = []
    files = 0
    for d in args.dirs:
        p = pathlib.Path(d)
        if not p.is_dir():
            continue
        for f in sorted(p.glob("*.tex")):
            files += 1
            check_file(f, findings)

    if not findings:
        print(f"  hindi prose gate: OK ({files} files)")
        return 0

    by_class: dict = {}
    for rel, line, cls, msg in findings:
        by_class.setdefault(cls, []).append((rel, line, msg))

    print(f"  hindi prose gate: {len(findings)} issue(s) in {files} files")
    for cls in sorted(by_class):
        hits = by_class[cls]
        bad_files = len({h[0] for h in hits})
        print(f"    {cls:<14} {len(hits):>5} hit(s) in {bad_files} file(s)")
        if not args.quiet:
            for rel, line, msg in hits[:args.max_detail]:
                print(f"        {rel}:{line}: {msg}")
            if len(hits) > args.max_detail:
                print(f"        ... {len(hits) - args.max_detail} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
