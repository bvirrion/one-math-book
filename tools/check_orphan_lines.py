#!/usr/bin/env python3
"""Find English source lines that SURVIVED into a translated tree.

The defect class, found by the Spanish Book 5 agent 2026-09-02: a sentence's
translation absorbs the content of the next source line, and that line is
then never named by any patch range -- so `id_apply.py` copies it through
byte-identically, exactly as it is designed to. `es/01-lagrangian-mechanics`
shipped a bare English line reading `then`.

Why nothing else catches it:

  * `id_apply.py`'s censuses all pass -- the line IS byte-identical to
    English, which is the guarantee, not a violation of it.
  * `check_translation.sh` compares labels, environments and counts, never
    prose.
  * the `prose` census inside id_apply only runs for id/hi/ar.
  * `check_latin_prose.py` (gate 9) DOES see duplicated whole lines, but
    reports a one-word match in its second tier, where it is one of dozens
    of true cognates (*amplitude*, *signal*, *metal*) and invisible in
    practice. Two words of English are a defect; one word is a coin toss --
    unless the word is one no target language shares, which is what this
    script keys on.

So: a translated line, byte-identical to a line of its English twin, whose
prose contains a word that is English and is NOT a word of any of the seven
target languages. That list is deliberately tiny and conservative; every
entry was checked against French, Spanish, Portuguese, Dutch and Indonesian
before being added (*note* and *second* are French and Spanish words and are
NOT gated; *of* and *over* are Dutch; *ada*, *dari* are Indonesian).

Usage:
    python3 tools/check_orphan_lines.py parts/bachelor-3/es \
                                        parts/bachelor-3/solutions/es
    python3 tools/check_orphan_lines.py --quiet <dirs...>
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import sys

# English words that are not words in fr, es, pt, nl, id, hi or ar.
# Conservative on purpose: a false positive here wastes a reviewer's time,
# and this gate is meant to be believed.
ENGLISH_ONLY = {
    "the", "then", "this", "that", "these", "those", "there", "their",
    "they", "them", "with", "which", "where", "when", "what", "while",
    "from", "have", "has", "been", "were", "are", "was", "would", "should",
    "could", "because", "through", "between", "into", "about", "after",
    "before", "since", "such", "each", "both", "also", "only", "more",
    "than", "very", "much", "same", "other", "another", "first", "third",
    "gives", "give", "using", "used", "shows", "show", "thus", "hence",
    "therefore", "however", "whose", "whether", "always", "never",
    "already", "still", "again", "here", "above", "below", "within",
    "without", "against", "along", "around", "across", "toward", "towards",
    "every", "some", "many", "few", "must", "may", "might", "shall",
    "cannot", "does", "doing", "done", "being", "makes", "make", "made",
    "take", "takes", "taken", "find", "finds", "found", "means", "meaning",
    "called", "known", "written", "given", "seen", "let", "let's",
}

DRAW_ENVS = ("tikzpicture", "axis", "scope", "circuitikz", "pgfonlayer",
             "semilogxaxis", "semilogyaxis", "loglogaxis", "groupplot")

MATH_ENVS = ("equation", "align", "gather", "multline", "split", "cases",
             "array", "matrix", "pmatrix", "bmatrix", "vmatrix", "aligned")


def strip_math(s: str) -> str:
    s = re.sub(r"\$\$.*?\$\$", " ", s, flags=re.S)
    s = re.sub(r"\$[^$]*\$", " ", s)
    s = re.sub(r"\\\[.*?\\\]", " ", s, flags=re.S)
    s = re.sub(r"\\\(.*?\\\)", " ", s, flags=re.S)
    return s


def prose_words(line: str):
    """Lowercase word tokens of a line, with mathematics and macros removed."""
    s = strip_math(line)
    # quantity macros are mathematics, not prose
    s = re.sub(r"\\(?:qty|num|unit)\s*(\{[^{}]*\}){1,2}", " ", s)
    # a graphics/input path is a filename, not prose: "photo-first-transistor"
    # made `first` fire on a correct Spanish line
    s = re.sub(r"\\(?:includegraphics|input|includepdf)\s*(\[[^\]]*\])?\s*"
               r"\{[^{}]*\}", " ", s)
    s = re.sub(r"\[[^\]]*=[^\]]*\]", " ", s)          # option groups (width=..)
    # a label argument is not prose
    s = re.sub(r"\\(?:label|ref|cref|Cref|autoref|eqref|omterm)\s*\{[^{}]*\}",
               " ", s)
    # remaining macro names are not prose
    s = re.sub(r"\\[A-Za-z@]+", " ", s)
    return re.findall(r"[a-z][a-z']{1,}", s)


def interesting(line: str) -> bool:
    """Could this line carry translatable prose at all?"""
    t = line.strip()
    if not t or t.startswith("%"):
        return False
    if re.match(r"^\\(begin|end)\{", t):
        return False
    return bool(prose_words(t))


def scan_file(tpath: pathlib.Path, epath: pathlib.Path):
    tlines = tpath.read_text(encoding="utf8").splitlines()
    elines = epath.read_text(encoding="utf8").splitlines()
    eset = set(l.strip() for l in elines if l.strip())

    hits = []
    depth = 0
    for i, raw in enumerate(tlines, 1):
        t = raw.strip()
        # track drawing / math environments: their content is copied on
        # purpose and is not prose
        m = re.match(r"^\\begin\{([a-zA-Z*]+)\}", t)
        if m and m.group(1).rstrip("*") in DRAW_ENVS + MATH_ENVS:
            depth += 1
        m = re.match(r"^\\end\{([a-zA-Z*]+)\}", t)
        if m and m.group(1).rstrip("*") in DRAW_ENVS + MATH_ENVS:
            depth = max(0, depth - 1)
            continue
        if depth or not interesting(raw):
            continue
        if t not in eset:
            continue
        words = set(prose_words(t))
        bad = sorted(words & ENGLISH_ONLY)
        if bad:
            hits.append((i, t, bad))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    total = 0
    for d in args.dirs:
        d = pathlib.Path(d)
        # parts/<year>/<lang> -> parts/<year> ; parts/<year>/solutions/<lang>
        english_dir = d.parent
        for tpath in sorted(d.glob("[0-9]*.tex")):
            epath = english_dir / tpath.name
            if not epath.exists():
                continue
            for line_no, text, bad in scan_file(tpath, epath):
                total += 1
                if not args.quiet:
                    print("%s:%d  english-only %s\n    %s"
                          % (tpath, line_no, bad, text))
    if not args.quiet:
        print("\norphan English lines: %d" % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
