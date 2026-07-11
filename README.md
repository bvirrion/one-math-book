# One Math Book

*The One Math Book to Rule Them All.*

A series of mathematics books, written in English for readers anywhere in
the world (with a full **French** edition of the primary & middle school
volume), with the ambition of covering everything **from kindergarten to
the end of the bachelor's degree** — as one coherent course, published in
several volumes:

1. **Primary & Middle School Mathematics** — Grades 1–9
   (also available in French);
2. **High School Mathematics** — Grades 10–12;
3. **University Mathematics — Year 1**;
4. **University Mathematics — Year 2**;
5. **University Mathematics — Year 3** (planned).

The style is concise and rigorous: courses built from **definitions,
examples, propositions, theorems and methods**, with proofs whenever they
are accessible at the given level (results admitted without proof are
explicitly marked), followed by graded **exercises with full solutions**
collected at the end of each book.

## Current status

| Book | Part | Level | Status |
|------|------|-------|--------|
| Primary & Middle School | Grade 1 (age 6–7) | First year of primary school | ✅ 6 chapters, exercises + solutions |
| Primary & Middle School | Grade 2 (age 7–8) | Second year of primary school | ✅ 7 chapters, exercises + solutions |
| Primary & Middle School | Grade 3 (age 8–9) | Third year of primary school | ✅ 7 chapters, exercises + solutions |
| Primary & Middle School | Grade 4 (age 9–10) | Fourth year of primary school | ✅ 8 chapters, exercises + solutions |
| Primary & Middle School | Grade 5 (age 10–11) | Last year of primary school | ✅ 8 chapters, exercises + solutions |
| Primary & Middle School | Grade 6 (age 11–12) | First year of lower secondary school | ✅ 8 chapters, exercises + solutions |
| Primary & Middle School | Grade 7 (age 12–13) | Second year of lower secondary school | ✅ 9 chapters, exercises + solutions |
| Primary & Middle School | Grade 8 (age 13–14) | Third year of lower secondary school | ✅ 9 chapters, exercises + solutions |
| Primary & Middle School | Grade 9 (age 14–15) | Last year of lower secondary school | ✅ 9 chapters, exercises + solutions |
| High School | Grade 10 (age 15–16) | First year of upper secondary school | ✅ 9 chapters, exercises + solutions |
| High School | Grade 11 (age 16–17) | Penultimate year of secondary school, advanced track | ✅ 10 chapters, exercises + solutions |
| High School | Grade 12 (age 17–18) | Final year of secondary school, advanced track | ✅ 16 chapters, exercises + solutions |
| University — Year 1 | Bachelor Year 1 (age 18–19) | First post-secondary year (old French MPSI program) | ✅ 25 chapters, exercises + solutions |
| University — Year 2 | Bachelor Year 2 (age 19–20) | Second post-secondary year (French MP* program) | ✅ 23 chapters, exercises + solutions |
| Primary & Middle School (FR) | Années 1–9 | Full French translation | ✅ same chapter set as English |
| Other | Kindergarten, University Year 3 | | 🚧 planned |

The lower the grade, the younger the reader it is written for: earlier
parts use more figures, more detailed worked steps, and gentler
exercises.

## Building the books

Requirements: a TeX Live installation with `latexmk` (packages used:
`tcolorbox`, `pgfplots`, `amsthm`, `cleveref`, `imakeidx`, …).

```sh
make            # or just: latexmk — builds all books
```

The PDFs are produced at

```
build/one_math_book_primary_middle_school.pdf
build/one_math_book_primary_middle_school_fr.pdf
build/one_math_book_high_school.pdf
build/one_math_book_university_year_1.pdf
build/one_math_book_university_year_2.pdf
```

`make clean` removes auxiliary files, `make distclean` removes the whole
`build/` directory. To build a single book:
`latexmk one_math_book_high_school.tex` or
`latexmk one_math_book_primary_middle_school_fr.tex`.

French edition: install `texlive-lang-french` when available (better
hyphenation via babel); the book still builds without it.

## Repository layout

```
one_math_book_*.tex          one entry file per book / language
styles/onemath.sty           packages, theorem environments, macros
styles/lang/<lang>.tex       UI strings (en, fr, …)
frontmatter/                 title page, preface (shared layout)
parts/<year>/part.tex        shared structure for a school year
parts/<year>/NN-*.tex        English chapter
parts/<year>/<lang>/NN-*.tex translated chapter (same labels)
parts/<year>/solutions/      English + <lang>/ solutions
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

Not yet decided.
