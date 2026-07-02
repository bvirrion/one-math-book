# One Math Book

*One math book to rule them all.*

An open-source mathematics book, written in English, with the ambition of
covering the entire French curriculum **from kindergarten to the end of the
licence** (bachelor's degree) — in a single, coherent volume.

The style is that of the French *classes préparatoires*: concise courses
built from **definitions, examples, propositions, theorems and methods**,
with proofs whenever they are accessible at the given level (results admitted
without proof are explicitly marked), followed by graded **exercises with
full solutions** collected at the end of the book.

## Current status

| Part | Level | Status |
|------|-------|--------|
| Terminale | Grade 12 (union of former Terminale S + Spécialité Maths + Maths Expertes) | ✅ 16 chapters, exercises + solutions |
| Other years | Kindergarten → Licence 3 | 🚧 planned |

## Building the book

Requirements: a TeX Live installation with `latexmk` (packages used:
`tcolorbox`, `pgfplots`, `amsthm`, `cleveref`, `imakeidx`, …).

```sh
make            # or just: latexmk
```

The PDF is produced at `build/main.pdf`. `make clean` removes auxiliary
files, `make distclean` removes the whole `build/` directory.

## Repository layout

```
main.tex                  the single entry point of the book
styles/onemath.sty        all packages, theorem environments, macros
frontmatter/              title page, preface
parts/<year>/part.tex     one \part per school year
parts/<year>/NN-*.tex     one file per chapter
parts/<year>/solutions/   solutions, one file per chapter
```

## Contributing

Contributions are welcome — new chapters and years, corrections, better
proofs, additional exercises, figures. Please read
[CONTRIBUTING.md](CONTRIBUTING.md) for the structure, environments and
style conventions of the project.

## License

To be decided (a free-culture license such as CC-BY-SA is envisioned).
