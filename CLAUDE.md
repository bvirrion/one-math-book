# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A series of five LaTeX math books (Grades 1–9, Grades 10–12, University
Year 1, University Year 2, University Year 3) built from **one shared `parts/` tree**, one
entry file per book at the repo root, and a single style file. Several
volumes also exist in full French and Dutch translations (`*_fr.tex` /
`*_nl.tex` entry files; bodies under `parts/<year>/<lang>/`): the primary,
middle, and high school books (Grades 1–12, `parts/grade-N/{fr,nl}/`) and,
of the university books, **Book 3 (University Year 1)** in both FR and NL
(`parts/bachelor-1/{fr,nl}/`) and **Book 4 (University Year 2)** in both FR
and NL (`parts/bachelor-2/{fr,nl}/`), and **Book 5 (University Year 3)** in
both FR and NL (`parts/bachelor-3/{fr,nl}/`). Everything
is written in English for an international audience; the FR/NL editions
translate that content, keeping identical labels, order, and structure.
`CONTRIBUTING.md` holds the authoritative style/structure conventions;
`THEME.md` documents the One Course cover brand. Read both before writing
chapters.

## Git

**Never create git commits yourself.** Make the changes and leave the
working tree for the user to review and commit.

## Build

```sh
make                                       # latexmk builds all books into build/
latexmk one_math_book_3_university_year_1.tex   # a single book
latexmk one_math_book_1_primary_middle_school_fr.tex  # French primary volume
latexmk one_math_book_2_high_school_nl.tex              # Dutch high school
```

The build is pdflatex via `latexmkrc` (which also raises pdfTeX memory
limits for the TikZ-heavy books — don't bypass it). PDFs land in
`build/one_math_book_<N>_<slug>.pdf`. There are no tests; the quality gate is
the log:

```sh
L=build/one_math_book_<N>_<slug>.log
grep -c '^!' $L                 # errors — must be 0
grep -ci 'undefined' $L         # undefined references — must be 0
grep -c 'Overfull' $L           # overfull boxes — keep at 0 (fix by breaking long inline math into displays / align*)
```

CI (`.github/workflows/build.yml`) builds all books on every push;
`release.yml` additionally generates `version.tex` (overriding
`\bookversion`/`\bookdate` in the entry files) and attaches
`one_math_book_<N>_<slug>_vX.Y.Z.pdf` to the release.

## Architecture

- `one_math_book_<N>_<slug>.tex` — entry file per book (series number N):
  optionally sets `\booklang` (default `en`), loads `styles/onemath.sty`,
  defines `\bookline` ("Book N: ..." shown on the shared cover), inputs
  `parts/<year>/part.tex` for its years, then a Solutions appendix
  inputting `parts/<year>/solutions/solutions.tex`.
- `styles/onemath.sty` — **the only place** packages are loaded and
  macros/environments defined. Chapter files never `\usepackage` or
  `\newcommand`. Language UI strings live in `styles/lang/<lang>.tex`.
- `styles/lang/en.tex`, `styles/lang/fr.tex`, `styles/lang/nl.tex` —
  theorem titles, solution headers, cover strings, part titles
  (`\omstr{part.grade1}` … `part.grade12`).
- Language-aware content paths:
  - English (canonical): `parts/<year>/NN-slug.tex`
  - Other languages: `parts/<year>/<lang>/NN-slug.tex` (same labels)
  - `\ominput{grade-1}{01-counting-to-20}` and `\ominputsol{...}` pick
    the language file when it exists, else fall back to English.
- `parts/<year>/part.tex` — shared structure: `\part{\omstr{...}}` and
  `\ominput` lines; `solutions/solutions.tex` likewise with `\ominputsol`.
- Year label prefixes: `g1`–`g12`, `b1`, `b2`, `b3` (future: `k`). All
  labels are namespaced `<type>:<year>:<chapter-slug>:<name>`, e.g.
  `thm:b2:fourier:parseval`, exercises `exo:b2:fourier:3`. Reference with
  `\cref`, never bare `\ref`. Labels are **language-independent** (same
  IDs in English and French).
- **Cross-volume references are prose-only** ("the Year 1 volume", "the
  High School volume") — `\cref` to another book's label will build
  locally by accident and break that book. Check with
  `grep -rn 'ref{[^}]*b1:' parts/bachelor-2/` (adapt prefixes).

### Adding a language edition

1. Add `styles/lang/<lang>.tex` (copy `en.tex` or `fr.tex`).
2. Translate bodies to `parts/<year>/<lang>/` and
   `parts/<year>/solutions/<lang>/` (same file names and labels).
3. Add entry file `one_math_book_<N>_<slug>_<lang>.tex` with
   `\newcommand{\booklang}{<lang>}` before `\usepackage{styles/onemath}`.
4. Register the entry in `latexmkrc` and both GitHub workflows.
5. Write `tools/term_config/book<N>_<lang>.py` (curated, NOT a translation of
   the English config — see the termlink notes below), then generate `\omterm`
   links: `python3 tools/link_defined_terms.py --book N --lang <lang> --apply`.

Reference implementations:

- `one_math_book_1_primary_middle_school_fr.tex` / `_nl.tex`
- `one_math_book_2_high_school_fr.tex` / `_nl.tex`
- `one_math_book_3_university_year_1_fr.tex` / `_nl.tex` (+ `book3_{fr,nl}.py`)
- `one_math_book_4_university_year_2_fr.tex` / `_nl.tex` (+ `book4_{fr,nl}.py`)
- `one_math_book_5_university_year_3_fr.tex` / `_nl.tex` (+ `book5_{fr,nl}.py`)

PDFs: `build/one_math_book_<N>_<slug>[_<lang>].pdf`.

**Verify a translation** — a clean build proves almost nothing (`\ominput`
silently falls back to English, `\omstr` to empty). Gate on:

- `bash tools/check_translation.sh <year> <lang>` — completeness + identical
  labels/order + env/figure census vs English + UTF-8 (no `\'e` escapes).
- **Link-target parity**: the translated `\omterm` *targets* must be the same
  set as English (a term must link to the same definition). Compare
  `grep -rho '\omterm{[^}]*}' <lang>/ | sort -u` against the English tree;
  investigate every divergence (wrong-sense link vs. a curation choice).

**Translation gotchas (cost real time on the bachelor books):**

- Translators leave English `\index{}` keys while translating the visible
  `\emph{}` — orphan-splits the index. Normalise so the EN∩<lang> index-key
  intersection is only genuinely-identical terms (argument, basis, ring, …).
- Each FR/NL config needs its own `NOT_A_TERM` (the default keywords are
  English, so French/Dutch result-names slip through and over-link). French uses
  bare heads (`"théorème"`, `"lemme"`, `"inégalité"`, `"règle"`, …); **Dutch must
  use the "X van Y" PHRASE forms** (`"stelling van"`, `"formule van"`), never
  bare nouns — Dutch substring-matches solid compounds (kettingregel,
  quotiëntcriterium, hoofdstelling), French does not. Keep bare `"loi"` in FR
  (the distribution *definition*). Result-names reaching via `\emph{}\index{}`
  bypass `NOT_A_TERM` — hand-`DROP` those.
- The index-only harvest needs a space in the term (`" " not in d → skip`), so
  Dutch solid/hyphenated compounds (Riemannsommen, Gauss-eliminatie) — and any FR
  compound the harvest drops as ambiguous (bare "courbure") — are never linked;
  declare each in the config's `EXTRA` → target.
- FR `\cref` used as a noun needs its article, keyed by label prefix (`le~` thm,
  `la~` prop/def, `l'` ex/exo, contractions du/au) with a non-breaking `~`. Give
  translators this map up front — retrofitting it is ~200 edits per book.
- Overfull boxes from longer translated prose (no babel FR/NL here): a
  `\hyphenation{...}` block (with UTF-8 accents) + `\setlength{\emergencystretch}
  {3em}` in the entry file. Convert `\"o`→`ö` in prose; keep index keys ASCII.

## Invariants to verify after writing/editing chapters

Every exercise (and every university-volume weekend `problem`, label
`pb:...`) has exactly one solution, keyed by label. Per chapter:

```sh
diff <(grep -o 'label{\(exo\|pb\):[^}]*}' parts/<year>/NN-slug.tex | sed 's/label{//;s/}//') \
     <(grep -o 'begin{solution}{[^}]*}' parts/<year>/solutions/NN-slug.tex | sed 's/begin{solution}{//;s/}//')
# French edition:
diff <(grep -o 'label{exo:[^}]*}' parts/<year>/fr/NN-slug.tex | sed 's/label{//;s/}//') \
     <(grep -o 'begin{solution}{[^}]*}' parts/<year>/solutions/fr/NN-slug.tex | sed 's/begin{solution}{//;s/}//')
grep -rho 'label{[^}]*}' parts/<year>/ | sort | uniq -d   # duplicate labels
grep -rn 'end{[a-z]*>' parts/<year>/                       # \end{proof> typo class
grep -rn '\.\.\.' parts/<year>/ | grep -v '\\dots\|\\ldots\|\\cdots\|\\foreach'  # drafty "..." prose (use \dots)
```

Exercise→solution hyperlinks: every `solution` env emits a `sol:<key>`
link target; a book that calls `\omsolutionlinks` in its entry file
(currently Book 5) prints a hyperlinked "Solution p. N" pointer at the
end of each exercise/problem. The pointer resolves to the first `\label`
inside the environment, so keep the `exo:`/`pb:` label first.

Branded running header: a book that calls `\ombrandheader` (all of them)
gets the rosette + `ONE-COURSE.COM` (linking to the site) above the
chapter mark and `\bookline` on even pages, the section mark on odd
pages, and the page number at the foot. The chapter and section marks
link to their own lines in the table of contents.

Link landing: every book raises each statement's and each solution's
hyperlink destination by three lines (`\omlinkpad`, default
`3\baselineskip`), so a clicked link lands just above its target instead
of flush against the top of the window. `\omlinkpadding{<len>}` overrides
the amount for one book; `\omlinkpadding{0pt}` restores hyperref's own
placement. The raise only works on an anchor sitting in a line of type,
so the statement anchor amsthm writes in vertical mode is caught and
released inside the theorem head — see the comment in `styles/onemath.sty`
before touching it.

Defined-term links: `\omterm{def:...}{term}` links a term used in the
course, an exercise, a problem or a solution back to its definition.
**These are generated, not hand-written** — after adding chapters or
definitions, regenerate the affected book:

```sh
python3 tools/link_defined_terms.py --book 5                    # dry run
python3 tools/link_defined_terms.py --book 5 --unwrap --apply   # drop old links
python3 tools/link_defined_terms.py --book 5 --apply            # regenerate
python3 tools/link_defined_terms.py --book 1 --lang fr --apply  # a translation
```

Always `--unwrap` before regenerating: a plain re-run can only *add*
links, so removing a term from a config looks like it worked (0 new
links) while its stale links stay in the sources.

- The **rules** live in `tools/termlink/` and are shared by every book.
  Do not tune them for one book: `sh tools/check_book5_golden.sh`
  regenerates Book 5 and fails unless the sources come back
  byte-identical.
- The **vocabulary** lives in `tools/term_config/book<N>_<lang>.py` —
  `STOP` (words that are ordinary language here), `NO_CAPITAL` (linked
  mid-sentence but not sentence-initially: "Circle the even numbers" is
  an imperative), `EXTRA` (manual term → label, and it may point at any
  label, not just a `def:` one), `EXTRA_PROTECT` (regexes for a fixed
  phrase in which a defined word carries another sense — "for free",
  "closed form", "il reste 7 cerises"), `AMBIG_POLICY` (`drop` for the
  university books; `nearest-preceding` for the school books, whose
  spiral curriculum re-defines a term each year).
- `STOP` is **soft on purpose**: a stoplisted word is still linked inside
  the chapter that defines it, which is what lets `compact` point at the
  space in one chapter and at the operator in another. `DROP` is the hard
  version — use it when a word must never be a link anywhere.

A term earns a link only if introduced as `\emph{term}\index{...}` in a
`definition` (a bare `\emph` is ordinary emphasis — linking those made
"countable" point at the σ-algebra definition). Under `AMBIG_POLICY =
drop`, terms defined twice (`compact` as a space and as an operator) and
words whose sense changes by chapter (`basis`, `degree`, `Euclidean`, …)
are skipped: an automatic link would point at the wrong definition.

Content rules (from CONTRIBUTING.md, enforced in review):

- 8–12 exercises per chapter, graded `[$\star$]` to `[$\star\star\star$]`,
  each with a full solution.
- Proofs essentially complete at the level of the year. A result stated
  without proof uses `\admitted` — a zero-argument macro that emits the
  whole "Admitted at this level" proof; it replaces the proof entirely
  (no optional argument), and should be followed by a `remark` saying
  where the result is honestly proved (usually "Year 3").
- New terms: `\emph{...}` + `\index{...}` in a `definition`.

## HTML export (the one-course.com online reader)

`tools/build_html_chapter.py` converts a chapter (all language editions)
to HTML fragments + figure SVGs + a manifest for the website's online
reader (the `saas` repo serves them as Blade pages):

```sh
cd tools/htmlbook && npm install   # once (KaTeX, version-pinned)
python3 tools/build_html_chapter.py \
    --chapter parts/grade-10/01-numbers-and-sets.tex \
    --chapter-number 1 --book math-2 --languages en,fr,nl \
    --out ../../saas/resources/onecourse/chapters \
    --svg-out ../../saas/public/images/onecourse/chapters
```

The parser in `tools/htmlbook/` covers exactly the constructs the books
use and **hard-errors on anything unknown** — if a new chapter adds a
LaTeX construct, extend the converter, never let it skip content. Math is
pre-rendered with KaTeX (macro map mirrors `onemath.sty`; keep the katex
version pinned identically here and in the saas `package.json`). Figures
compile standalone via pdflatex + dvisvgm (the preamble includes the
`omaxis` pgfplots style). A translation that lags the English chapter is
accepted only as a strict structural prefix (warning); any other
structural divergence between languages aborts the build.

Cross-chapter `\cref`/`\omterm`: the manifest stores each chapter's label
map, and references to an already-published chapter resolve to links into
its page. **Build chapters in order** — a chapter referencing another
needs that one in the manifest first (rebuild the referenced chapter
before the referencing one after label changes). Generated output is
committed in the saas repo only, never here.

## Style-file specifics worth knowing

- `\P` = ℙ, `\E` = 𝔼, `\V` = 𝕍 (redefined); `\pcond{B}{A}`;
  intervals `\intcc/\intoo/\intco/\intoc{a}{b}`, integer range
  `\intint{a}{b}`; `\abs{}`, `\norm{}`, `\floor{}`; `\dd` in integrals;
  `\vertiii{}` for operator norms.
- `\scal{A}{B}` typesets arrows over its arguments (school-level vector
  dot product). At university level write `\langle x, y \rangle`
  directly.
- Semantic colors for chapter figures/boxes: `omDef` (blue), `omThm`
  (dark red), `omProp` (orange). The `oc*` palette and
  `\ocRosette`/`\ocQuadLine` are the cover brand (see THEME.md).
- A `]` inside a theorem's optional title breaks the parse — brace it:
  `\begin{theorem}[{Ideals of $K[X]$}]`.

## LaTeX gotchas seen in this repo

- `\foreach` wrapped around `\addplot` fails in pgfplots; use explicit
  `\draw plot` in plain TikZ instead (chapter figures are plain TikZ).
- Two side-by-side plots: use two `tikzpicture`s separated by `\qquad`,
  not scopes with `xshift` (the shift is scaled and overflows the line).
- Map overfull boxes to source files by walking the log's file-stack
  (parse `(` filename / `)` tokens around each `Overfull \hbox ... at
  lines N--M` entry).
- Translated editions: install `texlive-lang-french` / Dutch babel
  packages when possible so babel loads the language `.ldf`. Without
  them the books still build; UI strings come from `styles/lang/<lang>.tex`.
