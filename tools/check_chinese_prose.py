#!/usr/bin/env python3
"""Simplified Chinese hygiene gate for a translated tree (gate 9 of check_translation.sh).

Like Hindi and Arabic, Chinese is written in a script that is not Latin, so
residual English is visibly foreign and a gate can flag any Latin word in the
visible text. The LaTeX reduction is imported from check_hindi_prose.py, not
copied (translation_instruction.md: "import it, do not copy it").

Classes:

  english       a Latin word in visible text: prose, \\text{...} in math, TikZ
                node text, axis labels, environment optional titles. People's
                names are written in Chinese in this edition (欧拉, 柯西), so a
                Latin name is flagged too. Acronyms of up to four capitals and
                unit symbols are allowed, as in the Hindi gate.
  legend        a Latin word in \\legend{...} or \\addlegendentry{...}, which the
                imported reduction does not read (the macro form of a legend:
                see "\\legend{...} is the other blind spot" in
                translation_instruction.md).
  ascii-punct   an ASCII , . ; : ? ! after a Chinese character, or an ASCII
                parenthesis opening or closing on Chinese text: Chinese prose
                takes the full-width forms ，。；：？！（）.

Usage:
    python3 tools/check_chinese_prose.py parts/grade-3/zh parts/grade-3/solutions/zh

Exit status is 1 if anything was flagged.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from check_hindi_prose import (  # noqa: E402
    ALLOWED_UNITS, ALLOWED_WORDS, DOTTED_ABBREV, LATIN_WORD, SHORT_ENGLISH,
    _locate, strip_comments, visible_text)

HAN = r"\u3400-\u4dbf\u4e00-\u9fff"
ASCII_PUNCT = re.compile(rf"[{HAN}][ \t]*[,;:?!]|[{HAN}]\.(?=\s|$|[{HAN}])|\((?=[{HAN}])|(?<=[{HAN}])\)")
LEGEND = re.compile(r"\\(?:legend|addlegendentry)\s*(\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})")
MATHLESS = re.compile(r"\$[^$]*\$|\\[A-Za-z]+")

# Latin that may stay in a Chinese line: the series and product names.
ALLOWED_HERE = {"math", "book", "one", "course", "git", "contributing", "md", "url",
                # function names a display line can leave outside the blanked math (\cos\theta = \frac{\text{邻边}}{…})
                "sin", "cos", "tan", "cot", "log", "exp", "lim", "max", "min", "sup", "inf", "det", "gcd", "lcm",
                "arg", "ker", "dim", "deg", "diag", "sinh", "cosh", "tanh", "arcsin", "arccos", "arctan",
                # math names the blanking leaks from a formula split over lines (Book 5); not theta/zeta, which
                # Haiku also writes in prose ("theta 函数", "zeta 值")
                "delta", "limsup", "liminf",
                # roman numerals of item labels
                "ii", "iii", "iv", "vi", "vii", "viii", "ix", "xi", "xii",
                # Latin kept on purpose in the Chinese text (Book 2): a letter puzzle on the word itself, names of
                # algorithms and codes that Chinese writes in Latin, a fictional company, a function name
                "banana", "isbn", "isbn-", "luhn", "pagerank", "techcorp", "sigmoid",
                # Book 3: a lattice path written as its letters, and a word whose letters are rearranged
                "rurruru", "orange"}


def _flag_latin(text, body, rel, cls, findings, occ):
    for m in LATIN_WORD.finditer(text):
        word = m.group(0)
        low = word.lower()
        if low in ALLOWED_WORDS or low in ALLOWED_UNITS or low in ALLOWED_HERE:
            continue
        if word.islower() and low in SHORT_ENGLISH:
            findings.append((rel, _locate(body, word, occ), cls, f"English in visible text: {word!r}"))
            continue
        if word.isupper() and len(word) <= 4:
            continue
        if len(word) < 3:
            continue
        findings.append((rel, _locate(body, word, occ), cls, f"English in visible text: {word!r}"))


def check_file(path: pathlib.Path, findings: list) -> None:
    raw = path.read_text(encoding="utf-8")
    rel = str(path)
    body = strip_comments(raw)
    seen = visible_text(body, findings, rel)
    occ: dict = {}

    _flag_latin(seen, body, rel, "english", findings, occ)
    for m in DOTTED_ABBREV.finditer(seen):
        findings.append((rel, _locate(body, m.group(0), occ), "english",
                         f"English abbreviation in visible text: {m.group(0)!r}"))

    for m in LEGEND.finditer(body):
        _flag_latin(MATHLESS.sub(" ", m.group(1)), body, rel, "legend", findings, occ)

    for k, line in enumerate(body.split("\n"), 1):
        line = re.sub(r"\$[^$]*\$", "\x00", line)
        # pgfplots lists are code: the comma separates keys (xticklabels={1月,2月}, symbolic x coords={…})
        line = re.sub(r"(?:[xyz]ticklabels|symbolic [xyz] coords)\s*=\s*\{[^{}]*\}", "\x00", line)
        # an index key never prints its `!` (sub-entry); `\text{ (或 } \C)` in display math pairs with a math `)`
        line = re.sub(r"\\index\{[^{}]*(?:\}|$)|\\text\{ \(", "\x00", line)  # a key may run on to the next line
        for m in ASCII_PUNCT.finditer(line):
            findings.append((rel, k, "ascii-punct",
                             f"ASCII punctuation in Chinese text: {line[max(0, m.start() - 6):m.end() + 4]!r}"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dirs", nargs="+", help="directories (or single .tex files)")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--max-detail", type=int, default=8)
    args = ap.parse_args()

    findings: list = []
    files = []
    for d in args.dirs:
        p = pathlib.Path(d)
        files += sorted(p.glob("*.tex")) if p.is_dir() else ([p] if p.suffix == ".tex" and p.exists() else [])
    if not files:
        print("  chinese prose gate: no .tex file found in the arguments")
        return 1
    for f in files:
        check_file(f, findings)

    if not findings:
        print(f"  chinese prose gate: OK ({len(files)} files)")
        return 0
    by_class: dict = {}
    for rel, line, cls, msg in findings:
        by_class.setdefault(cls, []).append((rel, line, msg))
    print(f"  chinese prose gate: {len(findings)} issue(s) in {len(files)} files")
    for cls in sorted(by_class):
        hits = by_class[cls]
        print(f"    {cls:<14} {len(hits):>5} hit(s) in {len({h[0] for h in hits})} file(s)")
        if not args.quiet:
            for rel, line, msg in hits[:args.max_detail]:
                print(f"        {rel}:{line}: {msg}")
            if len(hits) > args.max_detail:
                print(f"        ... {len(hits) - args.max_detail} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
