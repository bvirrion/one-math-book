# Contributing to One Math Book

Thank you for contributing! This document describes the structure of the
project and the conventions that keep the book coherent.

## Project structure

The book is **one single document** (`main.tex` → `build/one_math_book.pdf`),
split into many files:

- `styles/onemath.sty` — **the only place** where packages are loaded and
  macros/environments are defined. Chapter files must not use `\usepackage`
  or define commands.
- `parts/<year>/part.tex` — declares the `\part` for a school year and
  `\input`s its chapters.
- `parts/<year>/NN-slug.tex` — one chapter per file, numbered in reading
  order (`01-sequences.tex`, …).
- `parts/<year>/solutions/NN-slug.tex` — the solutions of that chapter's
  exercises, same file name.

To add a new year: create `parts/<year>/part.tex` plus chapter files, add
one `\input` line in the *Parts* section of `main.tex`, and mirror the
solutions directory in the *Solutions* appendix (`solutions/solutions.tex`).

## Building

```sh
make          # runs latexmk (pdflatex), output in build/one_math_book.pdf
```

A pull request must build with **zero errors** and introduce no undefined
references (`grep -E "undefined" build/one_math_book.log` should stay clean).

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
| `solution` | in the solutions file: `\begin{solution}{exo:...}` referencing the exercise label |

## Style rules

1. **Rigor**: state precisely, prove what is provable at the
   level of the year; a result stated without proof must say so explicitly
   ("admitted at this level"), ideally pointing to where it will be proved.
2. **Concision**: no filler. An example after each substantial definition or
   theorem; a `method` box for each standard technique.
3. **Exercises**: 8–12 per chapter, graded `$\star$` (direct application) to
   `$\star\star\star$` (challenging); **every exercise must have a full
   solution** in the matching solutions file.
4. **English text**, written for readers anywhere in the world: avoid
   references to any particular country's educational system or
   curriculum-specific terminology.
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

Year prefixes: `g12` for Grade 12; other years will use `k` (kindergarten),
`g1`–`g11`, and `b1`–`b3` (bachelor years).

Cross-reference with `\cref{...}` (cleveref), never with bare `\ref`.

## Workflow

1. Fork / branch.
2. Write or edit chapter + solutions files.
3. `make` and check the log for errors and undefined references.
4. Open a pull request; CI builds the PDF and attaches it as an artifact.
