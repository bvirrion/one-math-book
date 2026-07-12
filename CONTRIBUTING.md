# Contributing to One Math Book

Thank you for contributing! This document describes the structure of the
project and the conventions that keep the book coherent.

## Project structure

The project is a **series of books** sharing one style and one `parts/`
tree. Each book has its own entry file at the repository root:

- `one_math_book_1_primary_middle_school.tex` — Book 1, Grades 1–9 (English);
- `one_math_book_1_primary_middle_school_fr.tex` — Book 1 (French);
- `one_math_book_1_primary_middle_school_nl.tex` — Book 1 (Dutch);
- `one_math_book_2_high_school.tex` — Book 2, Grades 10–12 (English);
- `one_math_book_2_high_school_fr.tex` — Book 2 (French);
- `one_math_book_2_high_school_nl.tex` — Book 2 (Dutch);
- `one_math_book_3_university_year_1.tex` — Book 3, Bachelor Year 1;
- `one_math_book_4_university_year_2.tex` — Book 4, Bachelor Year 2;
- `one_math_book_5_university_year_3.tex` — Book 5, Bachelor Year 3.

Naming: `one_math_book_<N>_<slug>[_<lang>].tex` → PDF
`build/one_math_book_<N>_<slug>[_<lang>].pdf`.

The shared files:

- `styles/onemath.sty` — **the only place** where packages are loaded and
  macros/environments are defined. Chapter files must not use `\usepackage`
  or define commands.
- `styles/lang/<lang>.tex` — UI strings (theorem names, solution headers,
  cover text, part titles) for each language (`en`, `fr`, …).
- `frontmatter/` — title page, colophon, preface; layout is shared, with
  language-specific preface files when needed (`preface.tex`, `preface.fr.tex`).
- `parts/<year>/part.tex` — shared, language-agnostic structure: declares
  the `\part` via `\omstr{...}` and `\ominput`s chapters.
- `parts/<year>/NN-slug.tex` — English chapter (canonical).
- `parts/<year>/<lang>/NN-slug.tex` — translation of that chapter (same
  labels and exercise set).
- `parts/<year>/solutions/NN-slug.tex` — English solutions;
  `parts/<year>/solutions/<lang>/NN-slug.tex` — translated solutions.

Set `\newcommand{\booklang}{fr}` **before** `\usepackage{styles/onemath}`
in a language-specific entry file. Content is resolved by `\ominput` /
`\ominputsol` (language file if present, else English).

To add a new year: create `parts/<year>/part.tex` plus chapter files, add
one `\input` line in the *Parts* section of the relevant book's entry file,
and mirror the solutions directory in its *Solutions* appendix
(`solutions/solutions.tex`). A new book (e.g.\ University Year 3) gets a
new entry file copied from an existing one, plus a line in `latexmkrc`'s
`@default_files` and in both GitHub workflows.

To add a **new language** for an existing book: add `styles/lang/<lang>.tex`,
translate under `parts/<year>/<lang>/` and `parts/<year>/solutions/<lang>/`
(keep labels identical), add an entry file with `\booklang`, and register it
in `latexmkrc` and the workflows.

**Cross-volume references:** `\cref` only works within one book. Never
reference a label that lives in another book; name the volume in prose
instead ("the distance formula, taken up in the High School volume").

## Building

```sh
make          # runs latexmk (pdflatex), builds every book into build/
```

A single book: `latexmk one_math_book_2_high_school.tex`.

A pull request must build with **zero errors** and introduce no undefined
references (`grep -E "undefined" build/*.log` should stay clean).

## Environments

All statements use the environments from `onemath.sty` (numbered
automatically within the chapter):

| Environment | Use for |
|---|---|
| `definition` | new notions; put the defined term in `\emph{...}` and `\index{...}` it |
| `theorem` / `proposition` / `lemma` / `corollary` | results, by decreasing importance |
| `method` | step-by-step recipes for standard tasks |
| `example`, `remark`, `notation` | worked examples, comments |
| `proof` | proofs (amsthm); a partial proof is titled `\begin{proof}[Partial proof]` |
| `exercise` | end-of-chapter exercises, difficulty in the optional argument: `[$\star$]` to `[$\star\star\star$]` |
| `problem` | (university volumes) one long, structured weekend problem per chapter — 15–25 numbered questions in parts, culminating in a named result; label `pb:<year>:<slug>:1` |
| `solution` | in the solutions file: `\begin{solution}{exo:...}` (or `{pb:...}`) referencing the exercise/problem label |

## Style rules

1. **Rigor**: state precisely, prove what is provable at the
   level of the year; a result stated without proof must say so explicitly
   ("admitted at this level"), ideally pointing to where it will be proved.
2. **Concision**: no filler. An example after each substantial definition or
   theorem; a `method` box for each standard technique.
3. **Exercises**: 8–12 per chapter, graded `$\star$` (direct application) to
   `$\star\star\star$` (challenging); **every exercise must have a full
   solution** in the matching solutions file. University chapters add one
   `problem` (weekend problem set) whose full solution likewise lives in
   the solutions file, keyed by the `pb:` label.
4. **English text** (canonical edition), written for readers anywhere in
   the world: avoid references to any particular country's educational
   system or curriculum-specific terminology. Translated editions keep
   the same international year labels (e.g.\ French «~Année~1~» for
   Grade~1) and the same math notation (decimal point in math mode).
5. Use the macros of `onemath.sty`: `\R, \N, \Z, \Q, \C`, `\abs{}`,
   `\intcc{a}{b}` = [a, b] (and `\intoo` = (a, b), `\intco`, `\intoc`) for
   intervals, `\dd` in integrals, `\eu`/`\iu` for upright e and i, `\E`,
   `\V`, `\P`, `\pcond{B}{A}` (probability of A given B), `\vect{AB}`,
   `\conj{z}`.

The `oc*` colors and the `\ocRosette`/`\ocQuadLine` macros are the One Course
brand (title page only, not for chapter content); they are documented in
`THEME.md`.

## Labels

All labels are namespaced: `<type>:<year>:<chapter-slug>:<name>`.

- Chapters: `ch:g12:seq`
- Statements: `def:g12:seq:limit`, `thm:g12:seq:monotone`,
  `prop:...`, `lem:...`, `cor:...`, `met:...`, `ex:...` (examples)
- Exercises and solutions: `exo:g12:seq:3` — the solution references this
  same label via `\begin{solution}{exo:g12:seq:3}`.
- Weekend problems: `pb:b3:galois:1` — solved via
  `\begin{solution}{pb:b3:galois:1}`.

Year prefixes: `g12` for Grade 12; other years will use `k` (kindergarten),
`g1`–`g11`, and `b1`–`b3` (bachelor years).

Cross-reference with `\cref{...}` (cleveref), never with bare `\ref`.

## Workflow

1. Fork / branch.
2. Write or edit chapter + solutions files.
3. `make` and check the log for errors and undefined references.
4. Open a pull request; CI builds the PDF and attaches it as an artifact.
