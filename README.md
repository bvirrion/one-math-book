# One Math Book

*The One Math Book to Rule Them All.*

An open-source mathematics book, written in English for readers anywhere in
the world, with the ambition of covering everything **from kindergarten to
the end of the bachelor's degree** — in a single, coherent volume.

The style is concise and rigorous: courses built from **definitions,
examples, propositions, theorems and methods**, with proofs whenever they
are accessible at the given level (results admitted without proof are
explicitly marked), followed by graded **exercises with full solutions**
collected at the end of the book.

## Current status

| Part | Level | Status |
|------|-------|--------|
| Grade 3 (age 8–9) | Third year of primary school | ✅ 7 chapters, exercises + solutions |
| Grade 4 (age 9–10) | Fourth year of primary school | ✅ 8 chapters, exercises + solutions |
| Grade 5 (age 10–11) | Last year of primary school | ✅ 8 chapters, exercises + solutions |
| Grade 6 (age 11–12) | First year of lower secondary school | ✅ 8 chapters, exercises + solutions |
| Grade 7 (age 12–13) | Second year of lower secondary school | ✅ 9 chapters, exercises + solutions |
| Grade 8 (age 13–14) | Third year of lower secondary school | ✅ 9 chapters, exercises + solutions |
| Grade 9 (age 14–15) | Last year of lower secondary school | ✅ 9 chapters, exercises + solutions |
| Grade 10 (age 15–16) | First year of upper secondary school | ✅ 9 chapters, exercises + solutions |
| Grade 11 (age 16–17) | Penultimate year of secondary school, advanced track | ✅ 10 chapters, exercises + solutions |
| Grade 12 (age 17–18) | Final year of secondary school, advanced track | ✅ 16 chapters, exercises + solutions |
| Other years | Kindergarten → Grade 2, Bachelor Years 1–3 | 🚧 planned |

The lower the grade, the younger the reader it is written for: earlier
parts use more figures, more detailed worked steps, and gentler
exercises.

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

## Contributors

- Benjamin Virrion
- Fable 5 (Anthropic's Claude)

## License

To be decided (a free-culture license such as CC-BY-SA is envisioned).
