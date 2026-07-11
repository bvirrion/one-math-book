# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A series of five LaTeX math books (Grades 1–9, Grades 10–12, University
Year 1, University Year 2, University Year 3) built from **one shared `parts/` tree**, one
entry file per book at the repo root, and a single style file. The primary
school volumes also exist in full French and Dutch translations
(`*_fr.tex` / `*_nl.tex` entry files; bodies under `parts/grade-N/fr/`
and `parts/grade-N/nl/` for Grades 1–12). Everything is written in
English for an international audience; FR/NL editions translate the
primary, middle, and high school content.
`CONTRIBUTING.md` holds the authoritative style/structure conventions;
`THEME.md` documents the One Course cover brand. Read both before writing
chapters.

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

Reference implementations:

- `one_math_book_1_primary_middle_school_fr.tex` / `_nl.tex`
- `one_math_book_2_high_school_fr.tex` / `_nl.tex`

PDFs: `build/one_math_book_<N>_<slug>[_<lang>].pdf`.

## Invariants to verify after writing/editing chapters

Every exercise has exactly one solution, keyed by label. Per chapter:

```sh
diff <(grep -o 'label{exo:[^}]*}' parts/<year>/NN-slug.tex | sed 's/label{//;s/}//') \
     <(grep -o 'begin{solution}{[^}]*}' parts/<year>/solutions/NN-slug.tex | sed 's/begin{solution}{//;s/}//')
# French edition:
diff <(grep -o 'label{exo:[^}]*}' parts/<year>/fr/NN-slug.tex | sed 's/label{//;s/}//') \
     <(grep -o 'begin{solution}{[^}]*}' parts/<year>/solutions/fr/NN-slug.tex | sed 's/begin{solution}{//;s/}//')
grep -rho 'label{[^}]*}' parts/<year>/ | sort | uniq -d   # duplicate labels
grep -rn 'end{[a-z]*>' parts/<year>/                       # \end{proof> typo class
```

Content rules (from CONTRIBUTING.md, enforced in review):

- 8–12 exercises per chapter, graded `[$\star$]` to `[$\star\star\star$]`,
  each with a full solution.
- Proofs essentially complete at the level of the year. A result stated
  without proof uses `\admitted` — a zero-argument macro that emits the
  whole "Admitted at this level" proof; it replaces the proof entirely
  (no optional argument), and should be followed by a `remark` saying
  where the result is honestly proved (usually "Year 3").
- New terms: `\emph{...}` + `\index{...}` in a `definition`.

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
