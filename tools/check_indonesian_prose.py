#!/usr/bin/env python3
"""Indonesian-specific hygiene gate for a translated tree.

check_translation.sh proves *structure*: same files, same labels, same
environment census. Its prose gates prove almost nothing here -- gate 6 looks
for TeX accent escapes, which Indonesian never writes (the orthography is
plain ASCII), and the drafty-"..." gate is script-agnostic. So an Indonesian
tree can pass every existing gate and still be half English.

**Indonesian is the hard case, and it is hard for the opposite reason to
Hindi.** The Devanagari and Arabic gates can flag *any* Latin word in visible
text, because in those editions Latin script is itself the defect. Indonesian
is written in the same alphabet as the English source, so a forgotten
sentence, a forgotten TikZ node or a forgotten \\text{...} is invisible to
that rule. The only safe detector is the inverse: a **curated list of English
words that are not also Indonesian words**, plus a density heuristic for
sentences that were never touched at all.

Every entry in ENGLISH_WORDS below was checked against Indonesian. Words that
are spelled identically in both languages are deliberately absent and listed
in NOT_GATED with the reason -- "data", "total", "real", "ring", "limit",
"integral", "unit", "area", "set", "median", "mode" are ordinary Indonesian
and flagging them would make the gate unusable.

Failure classes this script detects:

  1. `english`      -- a listed English word in visible text: prose, TikZ node
                       text, \\text{...} inside math, chapter/section titles,
                       environment optional titles, \\index keys.
  2. `untranslated` -- a long visible sentence containing not one of the
                       commonest Indonesian function words. An Indonesian
                       sentence of eight words essentially always contains a
                       "yang", "dan", "di", "dari", "untuk", "adalah", ...;
                       one that does not was never translated.
  3. `math-space`   -- MT-injected spaces inside inline math ("$P $ dan $ Q $"),
                       detected by the shared reduction.
  4. `redup-space`  -- plural reduplication written with spaces around the
                       hyphen ("bilangan - bilangan"). Invisible in print,
                       fatal to the term linker's word boundaries.
  5. `enclitic`     -- the enclitic -nya written as a separate word
                       ("turunan nya"), which is not Indonesian and again
                       breaks term matching.
  6. `split-number` -- a thin space splitting a word from a thousands group
                       ("bilangan\\,000"), the class that damaged Hindi when
                       MT moved a number out of "Numbers up to 10\\,000".

The LaTeX reduction is imported from tools/check_hindi_prose.py rather than
copied: it is language-independent (it drops technical macro arguments, keeps
\\text{...} inside math, pulls visible strings out of tikz/pgfplots drawing
code) and one implementation is better than three.

Usage:
    python3 tools/check_indonesian_prose.py parts/grade-3/id parts/grade-3/solutions/id
    python3 tools/check_indonesian_prose.py --quiet <dir> ...

Exit status is 1 if anything was flagged. Called by check_translation.sh for
lang == id; safe to run by hand on a single directory while translating.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

from check_hindi_prose import (  # noqa: E402  -- shared, language-independent
    LATIN_WORD,
    _locate,
    strip_comments,
    visible_text,
)

# ---------------------------------------------------------------------------
# 1. Residual English.
# ---------------------------------------------------------------------------
# Grammar words. None of these is a word in Indonesian in any spelling, so the
# match is case-insensitive: "The" at the head of a forgotten sentence and
# "the" mid-line are the same defect.
ENGLISH_FUNCTION = {
    "the", "a", "an", "and", "or", "but", "if", "then", "else", "so", "thus",
    "hence", "therefore", "because", "since", "while", "when", "where",
    "which", "whose", "that", "this", "these", "those", "there", "here",
    "of", "to", "in", "on", "at", "by", "for", "from", "into", "onto",
    "with", "without", "within", "about", "above", "below", "under", "over",
    "between", "among", "through", "during", "after", "before", "until",
    "we", "us", "our", "you", "your", "they", "them", "their", "it", "its",
    "he", "she", "him", "her", "his", "who", "what", "how", "why",
    "is", "are", "was", "were", "be", "been", "being", "am",
    "has", "have", "had", "do", "does", "did", "can", "cannot", "could",
    "will", "would", "shall", "should", "must", "might", "may",
    "no", "yes", "all", "any", "both", "each", "every", "some",
    "many", "much", "more", "most", "less", "least", "few", "several",
    "same", "other", "another", "such", "only", "also", "even", "still",
    "first", "second", "third", "last", "next", "previous", "then",
    "let", "given", "using", "note", "recall", "suppose", "assume",
    "consider", "observe", "indeed", "conversely", "moreover", "however",
    "again", "always", "never", "often", "sometimes", "now", "once",
    "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
}
# "no" is kept out of the short-token pass below, because "No." for "nomor"
# is ordinary Indonesian in a table head; it is listed here and screened by
# NUMBER_ABBREV instead.

# Content words a maths translation leaves behind. Every one was checked not to
# be Indonesian (see NOT_GATED for the ones that are).
ENGLISH_CONTENT = {
    # book furniture
    "chapter", "section", "page", "pages", "exercise", "exercises",
    "problem", "problems", "solution", "solutions", "proof", "proofs",
    "theorem", "theorems", "definition", "definitions", "proposition",
    "lemma", "corollary", "example", "examples", "remark", "remarks",
    "method", "notation", "figure", "table", "answer", "answers", "hint",
    # arithmetic and number
    "number", "numbers", "integer", "integers",
    "fraction", "fractions", "decimal", "decimals", "sum", "difference",
    "product", "quotient", "remainder", "divisor", "multiple", "prime",
    "even", "odd", "add", "adds", "subtract", "multiply", "divide",
    "addition", "subtraction", "multiplication", "division", "count",
    "half", "quarter", "third", "double", "rounding", "round",
    "percentage", "percent", "average", "power", "powers", "root", "roots",
    "square", "cube", "squared", "negative", "positive",
    # geometry and measure
    "line", "lines", "point", "points", "segment", "angle", "angles",
    "circle", "triangle", "rectangle", "polygon", "shape", "shapes",
    "side", "sides", "vertex", "edge", "face", "faces", "length", "width",
    "height", "depth", "surface", "distance",
    "perpendicular", "symmetry", "rotation", "translation",
    "left", "right", "middle", "centre", "center", "scale",
    # algebra and analysis
    "equation", "equations", "inequality", "unknown", "variable",
    "function", "functions", "graph", "slope", "coefficient", "polynomial",
    "sequence", "series", "convergent", "convergence", "divergent",
    "continuous", "continuity", "derivative", "differentiable", "bounded",
    "increasing", "decreasing", "maximum",
    "neighbourhood", "neighborhood", "subset",
    "mapping", "matrix", "matrices", "vector", "vectors",
    "dimension", "kernel", "image", "eigenvalue", "eigenvector",
    "subspace", "orthogonal", "invertible", "determinant",
    "measure", "measurable", "probability", "random", "outcome", "event",
    "expectation", "variance", "distribution", "sample",
    # environment optional titles -- the class that shipped green (see
    # ENGLISH_SUFFIX_CAP and the `title` class below)
    "property", "properties", "characterization", "linearization",
    "invertibility", "expansion", "cofactor", "system", "systems",
    "isometry", "isometries", "plane", "case", "cases", "converse",
    "uniqueness", "existence", "criterion", "criteria",
    # place-value furniture, the commonest leftover in TikZ node text
    "thousand", "hundred", "tens", "ones", "metres", "meters",
    # verbs an exercise stem uses
    "compute", "calculate", "find", "show", "prove", "deduce", "explain",
    "justify", "draw", "write", "read", "complete", "check", "state",
    "simplify", "expand", "factor", "factorise", "factorize", "solve",
    "compare", "estimate", "measure", "order", "sort", "list", "give",
}

ENGLISH_WORDS = ENGLISH_FUNCTION | ENGLISH_CONTENT

# Deliberately NOT gated -- identical or near-identical in Indonesian, so a
# hit would be a false alarm on correct prose. Kept as a list so the next
# agent does not "helpfully" add them.
NOT_GATED = {
    "data", "total", "real", "ring", "grup", "limit", "integral", "unit",
    "area", "set", "median", "modus", "mode", "faktor", "vektor", "matriks",
    "normal", "positif", "negatif", "final", "modul", "ideal", "kernel",
    "domain", "kompleks", "abstrak", "aljabar", "analisis", "geometri",
    # spelled identically in both languages -- KBBI has all of these. Each one
    # was in ENGLISH_CONTENT until it fired on correct Indonesian prose.
    # "not" is Indonesian for a MUSICAL note (from Dutch "noot"; "not balok" is
    # staff notation). It fired ~35 times on the correct grade-7 fractions
    # chapter, whose weekend problem is about note values. Losing English "not"
    # costs nothing: a forgotten English sentence containing "not" always
    # carries "is"/"the"/"does" as well, and the `untranslated` class sees it.
    "not",
    "minimum", "supremum", "infimum", "volume", "basis", "linear",
    "interval", "parallel", "perimeter", "digit", "digits", "meter",
    "koordinat", "gradien", "polinomial", "determinan", "ortogonal",
    "konvergen", "divergen", "kontinu", "dimensi", "variabel", "skala",
    "desimal", "persen", "segmen", "poligon", "kubus", "sampel",
}

# Brand, markup names and unit symbols that legitimately stay Latin.
ALLOWED = {
    "one", "course", "com", "www", "http", "https", "math", "book",
    "tex", "latex", "pdf", "html", "github", "md",
    "si", "iso", "cm", "mm", "km", "kg", "mg", "ml", "hz", "rad",
}

# A curated list cannot be complete, and the words it misses are exactly the
# ones nobody thought of ("thousands" in a place-value node, "metres" in a
# \text{}). Two generic rules close most of that gap without touching correct
# Indonesian:
#
#   * ENGLISH_SUFFIX -- endings Indonesian orthography does not produce. Applied
#     to LOWERCASE words only, which removes the proper-noun risk entirely: the
#     books are full of Smith-shaped surnames and Indonesian keeps them in
#     Latin. "-ing" is deliberately absent (penting, kucing, masing-masing are
#     ordinary Indonesian) and so is "-ed" (it would fire on names).
#   * the plural rule -- a listed noun with an English -s/-es on it.
ENGLISH_SUFFIX = re.compile(
    r"(?:tion|sion|ly|ness|ous|ful|ght|th|ance|ence|ship|hood|wise)$")
# Title-Case words need a NARROWER set. Environment optional titles are Title
# Case ("[Characterization]", "[Linearization]", "[Invertibility mod $n$]"),
# and the lowercase-only rule above let every one of them through a green gate
# -- the one defect class this edition could ship with. But the books are also
# full of surnames, so -th, -ght, -ly and -ous are dropped here: Smith, Booth,
# Wright, Knight would all fire. None of the series' mathematicians (Gauss,
# Cauchy, Riemann, Lebesgue, Frobenius, Legendre, Sylvester, ...) matches this.
ENGLISH_SUFFIX_CAP = re.compile(
    r"(?:tion|sion|ness|ance|ence|ship|hood|wise|ity)$")

DOTTED_ABBREV = re.compile(r"\b(?:i\.e\.|e\.g\.|etc\.|cf\.|viz\.)")
# "No. 3" / "no. 3" is Indonesian for "nomor"; "no" elsewhere is English.
NUMBER_ABBREV = re.compile(r"\b[Nn]o\.\s*\d")

# ---------------------------------------------------------------------------
# 2. Untranslated sentences.
# ---------------------------------------------------------------------------
# The commonest Indonesian function words. A visible sentence of any length
# worth reading contains at least one; a long one that contains none was never
# translated. Kept small on purpose -- a long list would excuse real defects.
ID_MARKERS = {
    "yang", "dan", "di", "ke", "dari", "untuk", "dengan", "adalah", "ialah",
    "itu", "ini", "pada", "atau", "tidak", "bukan", "jika", "maka", "kita",
    "setiap", "sebuah", "suatu", "akan", "sudah", "telah", "juga", "dapat",
    "bisa", "harus", "karena", "sehingga", "yaitu", "yakni", "oleh", "agar",
    "lalu", "kemudian", "hanya", "masih", "sama", "lebih", "kurang",
    "bilangan", "himpunan", "fungsi", "misalkan", "maka", "jadi", "ada",
    "semua", "banyak", "tiap", "bagi", "kali", "hasil", "nilai", "berapa",
    "hitung", "hitunglah", "tentukan", "buktikan", "gambar", "gambarlah",
    "tunjukkan", "carilah", "cari", "jawab", "solusi", "latihan", "soal",
    "bab", "halaman", "contoh", "definisi", "teorema", "bukti", "sifat",
    # Added after Book 1: a paragraph built out of noun phrases can go a long
    # way without any of the words above, and fired ~35 times on correct prose.
    # Every one of these is unambiguously Indonesian, so widening the list
    # cannot let an English sentence through.
    "tetapi", "namun", "sedangkan", "tanpa", "antara", "menjadi", "sesudah",
    "sebelum", "seperti", "sampai", "bahwa", "masing-masing", "saling",
    "sendiri", "mengapa",
    # Added after Book 4, same reason. "per" was proposed and REJECTED: English
    # writes "per" too ("per cent", "per second"), so it would excuse a real
    # English sentence. Every marker in this set must be unambiguously
    # Indonesian, or the class stops meaning anything.
    "daripada", "sebagaimana", "merupakan", "atas", "demi", "itulah",
}
MIN_SENTENCE_WORDS = 8
SENTENCE_SPLIT = re.compile(r"[.!?;:\n]+")

# ---------------------------------------------------------------------------
# 3-6. Indonesian-specific spelling damage.
# ---------------------------------------------------------------------------
# "bilangan - bilangan" / "bilangan -bilangan": reduplication must be a single
# token joined by a bare hyphen.
REDUP_SPACE = re.compile(r"\b([a-z]{3,})\s+-\s*\1\b|\b([a-z]{3,})\s*-\s+\2\b",
                         re.IGNORECASE)
# The enclitic written as a word. "nya" never stands alone in Indonesian.
ENCLITIC_SPACE = re.compile(r"(?<=[a-zA-Z])\s+-?nya\b")
# A word glued to a thousands group by a thin space: "bilangan\,000".
SPLIT_NUMBER = re.compile(r"[A-Za-z]{2,}\s*\\,\s*\d{3}\b")


# ---------------------------------------------------------------------------
# 7. Titles left byte-identical to the English twin.
# ---------------------------------------------------------------------------
# Book 3 shipped seven untranslated environment titles -- [Characterization],
# [Properties], [Cofactor expansion], [Vandermonde determinant], [Square Cramer
# systems], [Linearization], [Invertibility mod $n$] -- through a FULLY GREEN
# prose gate. A title is short, Title-Cased and often a single word, so the
# word lists and the sentence-density rule all slide off it.
#
# The decisive check is not a word list at all: compare the title with the
# SAME title in the English twin file. If they are byte-identical and the
# title contains real words, it was never translated. Legitimately identical
# titles -- [Gram--Schmidt], [Bolzano--Weierstrass], [Rolle], [Ring],
# [$\arcsin$, $\arccos$] -- survive, because after math and macros are
# stripped they contain no lowercase word and no English-looking one.
TITLE_ENVS = ("definition", "theorem", "proposition", "lemma", "corollary",
              "example", "remark", "method", "notation", "exercise",
              "problem", "proof", "omfigure", "figure", "table")
TITLE_RE = re.compile(
    r"\\begin\{(?:" + "|".join(TITLE_ENVS) + r")\}"
    r"\[((?:[^\[\]]|\[[^\]]*\])*)\]"
    r"|\\(?:chapter|section|subsection)\*?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")


def _titles(text: str):
    return [(m.group(1) if m.group(1) is not None else m.group(2))
            for m in TITLE_RE.finditer(text)]


def _looks_english(word: str) -> bool:
    low = word.lower()
    if low in ALLOWED or low in NOT_GATED:
        return False
    if low in ENGLISH_WORDS:
        return True
    if word.islower() and len(word) > 3 and ENGLISH_SUFFIX.search(low):
        return True
    if word[:1].isupper() and len(word) > 4 and ENGLISH_SUFFIX_CAP.search(low):
        return True
    # a lowercase word of real length that is not an Indonesian function word:
    # "Plane isometries" is caught here and by nothing else.
    return word.islower() and len(word) > 2 and low not in ID_MARKERS


# An ACCENT-AWARE word pattern, unlike LATIN_WORD. The shared LATIN_WORD is
# [A-Za-z]-only, so it splits "Caratheodory"-with-an-acute into "Carath" +
# "odory" -- and the second half is a lowercase non-Indonesian word, i.e. a
# false positive on a mathematician's name. Every accented surname in the
# series (Caratheodory, Poincare, Levy, Godel, Muller, ...) breaks the same way.
TITLE_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def _title_has_words(title: str) -> bool:
    t = re.sub(r"\$[^$]*\$", " ", title)
    t = re.sub(r"\\[A-Za-z@]+", " ", t)
    return any(_looks_english(w) for w in TITLE_WORD.findall(t))


def check_titles(path: pathlib.Path, body: str, findings: list) -> None:
    twin = pathlib.Path(str(path).replace("/id/", "/"))
    if not twin.is_file():
        return
    en = _titles(strip_comments(twin.read_text(encoding="utf-8")))
    idt = _titles(body)
    if len(en) != len(idt):
        return          # a structural divergence; check_translation.sh owns it
    for e, i in zip(en, idt):
        if e.strip() == i.strip() and _title_has_words(i):
            findings.append(
                (str(path), body.count("\n", 0, body.find(i)) + 1, "title",
                 f"title identical to English (untranslated?): {i.strip()[:60]!r}"))


def check_file(path: pathlib.Path, findings: list) -> None:
    raw = path.read_text(encoding="utf-8")
    rel = str(path)
    body = strip_comments(raw)
    # visible_text also reports the shared `math-space` class into findings.
    seen = visible_text(body, findings, rel)
    _occ: dict = {}

    # --- 1. residual English -------------------------------------------
    for m in NUMBER_ABBREV.finditer(seen):
        seen = seen[:m.start()] + " " * (m.end() - m.start()) + seen[m.end():]
    for m in LATIN_WORD.finditer(seen):
        word = m.group(0)
        low = word.lower()
        if low in ALLOWED or low in NOT_GATED:
            continue
        stem = low[:-2] if low.endswith("es") else low[:-1] if low.endswith("s") else None
        if (low in ENGLISH_WORDS
                or (stem and stem in ENGLISH_WORDS and stem not in NOT_GATED)
                or (word.islower() and len(word) > 3
                    and ENGLISH_SUFFIX.search(low))
                or (word[:1].isupper() and len(word) > 4
                    and ENGLISH_SUFFIX_CAP.search(low))):
            findings.append((rel, _locate(body, word, _occ), "english",
                             f"English in visible text: {word!r}"))
    for m in DOTTED_ABBREV.finditer(seen):
        findings.append((rel, _locate(body, m.group(0), _occ), "english",
                         f"English abbreviation: {m.group(0)!r}"))

    # --- 2. sentences that were never translated ------------------------
    for chunk in SENTENCE_SPLIT.split(seen):
        words = [w.lower() for w in LATIN_WORD.findall(chunk)]
        if len(words) < MIN_SENTENCE_WORDS:
            continue
        if any(w in ID_MARKERS for w in words):
            continue
        snippet = " ".join(words[:10])
        findings.append((rel, _locate(body, words[0], _occ), "untranslated",
                         f"no Indonesian function word in {len(words)} words: "
                         f"{snippet}..."))

    # --- 7. titles left identical to the English twin -------------------
    check_titles(path, body, findings)

    # --- 4-6. spelling damage, measured on the raw body -----------------
    for cls, rx, msg in (
            ("redup-space", REDUP_SPACE,
             "reduplication split by spaces (write bilangan-bilangan)"),
            ("enclitic", ENCLITIC_SPACE,
             "enclitic -nya written as a separate word"),
            ("split-number", SPLIT_NUMBER,
             "\\, between a word and a thousands group (split number?)"),
    ):
        for m in rx.finditer(body):
            findings.append((rel, body.count("\n", 0, m.start()) + 1, cls,
                             f"{msg}: {m.group(0)[:40]!r}"))


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
        print(f"  indonesian prose gate: OK ({files} files)")
        return 0

    by_class: dict = {}
    for rel, line, cls, msg in findings:
        by_class.setdefault(cls, []).append((rel, line, msg))

    print(f"  indonesian prose gate: {len(findings)} issue(s) in {files} files")
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
