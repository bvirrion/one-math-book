# Translation score — Math Book 1 · Spanish (`es`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 1 (Primary & Middle School, grades 1–9) |
| **Language** | Spanish (`es`) |
| **Quality bar** | **native academic** (English is the source of truth; FR Book 1 used only as a structural/sense reference) |
| **Overall score** | **97 / 100** |
| **Ship threshold** | ≥ 95 — **MET** |
| **Date** | 2026-07-27 |
| **Previous grading** | 95 / 100 on 2026-07-24 |
| **Scope of this pass** | **Full re-translation from English.** The previous `es/` bodies were *not* used as a draft: all 71 chapters and all 71 solution files were re-derived from `parts/grade-{1..9}/*.tex` with the structure-preserving pipeline (protect math/TikZ/labels → translate prose → unprotect → second pass on titles, `\omterm` displays and `\text{…}` inside math), then re-linked from a rewritten `tools/term_config/book1_es.py`. |

## Verdict in one line

The edition is a **byte-exact structural mirror of the English** whose prose
reads as Spanish written for Spanish schoolchildren, not as English seen
through glass: 0 residual English words, 0 build defects, and a defined-term
vocabulary curated for Spanish traps (`media`, `resto`, `cara`, `par`,
`divide`) rather than transliterated from the English config.

## Dimension scores

| Dimension | Score /100 | 2026-07-24 | Notes |
|-----------|----------:|----------:|--------|
| Structural fidelity | **99** | 97 | Every census identical to English: 71 chapters, 71 solution files, **760 exercises**, **35 problems**, **795 solutions**, 90 definitions, 42 theorems, 107 methods, 278 examples, **144 `omfigure`**, 146 `tikzpicture`, 138 `\index{}`, 70 `[resume]`, 105 `\textbf{Parte …}` vs 105 `\textbf{Part …}`. Per-chapter `exo:`/`pb:` → `\begin{solution}{…}` diff empty for all 71 chapters; no duplicate labels; 27 263 ES lines vs 27 278 EN (line-for-line translation, so figures and displays stay on their original lines) |
| Terminology | **97** | 94 | Genuine Spanish school register, not calques: *máximo común divisor*, *primos entre sí*, *números primos*, *criterios de divisibilidad*, *identidades notables*, *terna pitagórica*, *mediatriz*, *circunferencia circunscrita*, *media armónica / geométrica / ponderada*, *pendiente*, *ordenada en el origen*, *tasa de variación*, *función afín*, *recorrido* (statistical range), *tronco de pirámide / de cono*, *generatriz*, *configuración de mariposa*, *cámara estenopeica*, *contrahuella / huella*, *ley del cuadrado-cubo*, *la prueba del nueve*, *ley de los grandes números* |
| Register / tone | **96** | 93 | Age-graded voice. Grades 1–3 keep the short, concrete child sentence («Tres canicas rojas y dos canicas azules: juntas, ¿cuántas son?»); grades 7–9 move to the terse Spanish textbook imperative (*calcula*, *demuestra*, *deduce*, *concluye*) with lower-case, semicolon-separated `\item` clauses, as Spanish enumerations take them. Idiom, not gloss: «Roosevelt ganó por una goleada», «el truco ha muerto; viva el álgebra», «la aritmética como camuflaje», «compra radio» |
| LaTeX hygiene | **99** | 97 | **0 fatal errors, 0 undefined references, 0 overfull boxes**; 429 pp (EN 422, FR 430, PT 428, NL 431 — right in the family). All accents raw UTF-8: **0** TeX accent escapes anywhere in the ES tree. `«…»` guillemets throughout for the English `` `` … '' ``. The `$t\,\%$` convention untouched (babel-spanish `\%` gotcha, `\spanishplainpercent`). 61 English LaTeX comments localised to ASCII Spanish so the drafty-`...` probe stays clean |
| Cross-refs / rule compliance | **98** | 88 | `\label{…}`, `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English; `\omterm` first arguments byte-identical (parity table below). **60 missing articles before `\cref` repaired** (`de`→`del`/`de la`, `por`→`por el`, `en`→`en el`, `a`→`al`, keyed by label prefix: `thm/met/ex/exo/pb/ch` masculine, `prop/def/rem/not` feminine) — the weakest dimension of the previous grading. Zero curriculum or school-system names in visible text: cross-volume pointers all read «el volumen de secundaria superior», never *bachillerato* or *ESO* |
| Figures | **98** | 92 | TikZ/pgfplots drawing code byte-identical to English; only node text translated (*adyacente / opuesto / hipotenusa*, *cilindro / cono / pirámide / esfera*, *vértice*, *área $2.4$*, *10 casillas de 12*). The probability tree's `R`/`B` leaves became `R`/`N` (rojo/negro) with `RR`, `RN`, `NR`, `NN` and the matching `\P(\text{NN})` in the prose. `\text{…}` inside math translated everywhere (`\text{área}`, `\text{opuesto}`, `\text{casos favorables}`, `\text{suma de cifras de }`) |
| Solutions | **97** | 92 | All 795 present, complete, numerically identical to English. Weekend-problem solutions carry all 15 `\textbf{N.}` answers each; the argumentative ones (Euclid at the fountain, the 1089 trick, the Chevalier's bets, Archimedes' tombstone, the square–cube law) are re-argued in Spanish rather than transposed |
| MT-artifact freedom | **98** | 93 | A residual-English sweep over the whole ES tree (math, labels, environment names and commands stripped, then matched against an English word list) returns **0 hits**. A second sweep with a stateful `$…$` tracker — which catches prose a naive line scanner loses to math wrapping across lines — found and fixed 14 further lines inherited from the old MT bodies (*"found by counting up"*, *"Divisors of $18$"*, *"A square of side $c$ has perimeter $4c$"*, *"Equal: the solution is"*, …). Wrong-sense links the English tree carries by accident were dropped rather than copied (`\omterm{def:g3:numbers:evenodd}{even}` used as the adverb "even assemble", "even your graduation year", "break-even distance", "even money") |

**Overall: 97**, weighting terminology, register and MT-artifact freedom above
structure (structure is already gated mechanically by `check_translation.sh`).

## Structural / build gates

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh grade-1 es` … `grade-9 es` | **PASSED × 9** |
| `python3 tools/link_defined_terms.py --book 1 --lang es --unwrap --apply` | 3 735 links removed |
| `python3 tools/link_defined_terms.py --book 1 --lang es --apply` | **3 728 links inserted** across 125 files (def 3 619, ex 50, prop 33, pb 26) |
| `latexmk one_math_book_1_primary_middle_school_es.tex` | exit 0 |
| `^!` errors in the log | **0** |
| `undefined` (case-insensitive) in the log | **0** |
| `Overfull` boxes | **0** |
| PDF | **429 pages** |
| `exo:`/`pb:` labels ↔ `\begin{solution}{…}` | identical for all 71 chapters |
| duplicate `\label{}` | none |
| TeX accent escapes (`\'e`, `` \`a ``, `\~n`) | **0** |
| drafty `...` outside `\dots`/`\ldots`/`\foreach` | **0** |

### `\omterm` link-target parity (EN vs ES)

Sorted unique first-argument sets: **79 EN / 79 ES**, differing by exactly two
entries, both investigated:

| Divergence | Verdict |
|------------|---------|
| `def:g4:numbers:classes` — 4 links in EN, 0 in ES | **Tooling, not translation.** `tools/termlink/harvest.py` accepts a bare `\emph{…}` in a definition only when it agrees with the *English* label leaf (`key.startswith(leaf)`); `clases` does not agree with `classes`, so the term is never harvested. The Dutch edition has the identical gap (0 links) for the identical reason. Fixing it means touching a shared file, or a global `EXTRA` entry that would then link the *school* classes of grades 3, 7, 8 and 9 as well — reported, not forced |
| `def:g6:wholes:place` — 0 links in EN, 2 in ES | **A gain, not a wrong link.** Both are the caption phrase «la tabla de valor posicional»; the English phrase "place value" simply never occurs in EN prose |

`def:g6:lines:circle` was deliberately taken out of the Spanish vocabulary
(70 links) so that ES mirrors the English decision to stoplist *circle* as
geometry furniture; Spanish splits it into *círculo* (already stoplisted) and
*circunferencia*, and both are on every page of every geometry chapter.
`circunferencia circunscrita` keeps its own link.

## What was rewritten most heavily

| Area | Work |
|------|------|
| Grades 8–9 (18 chapters + 18 solution files) | Written from scratch — the old bodies were unusable MT (`\omterm{…}{incluso}` for *even*, `{extraño}` for *odd*, `{rostro}` for *face*, `{en ángulo recto}` for *right-angled*, spaced maths `$ ABC $`, *factor de escalada*) |
| Grades 1–7 (53 chapters + 53 solution files) | Re-derived line-for-line from English, not edited |
| Mid-chapter exercise stems and long weekend problems | The two weak spots called out on 2026-07-24: every `\item` re-cast as a Spanish enumerated clause (lower-case opening, `;` separators, `¿…?` pairs), every problem narrative re-argued rather than transposed |
| Articles before `\cref` | 60 repairs, keyed by label prefix (previous grading scored this dimension 88) |
| `tools/term_config/book1_es.py` | Rewritten from a 39-line stub to a curated config: `recorrido` added to `STOP`/`SOFT`, `circunferencia` dropped, `NO_CAPITAL` extended to *desarrollar* and *divide*, 19 `EXTRA_PROTECT` spans for the Spanish traps, and a 27-entry `DERIVED` map supplying the plurals of the multi-word terms |

## Samples, verdicted

**1. `parts/grade-1/es/02-addition-first-steps.tex` — native**

> Tres canicas rojas y dos canicas azules: juntas, ¿cuántas son? Juntar
> y contar el conjunto es \emph{sumar} --- la primera operación, con sus
> dos signos famosos $+$ y $=$.

Child-scale nouns (*canicas*), a real question, no calque of "how many
altogether".

**2. `parts/grade-3/es/04-sharing-and-division.tex` — native**

> \section{Las dos caras de la división}

*Las dos caras de* is the ordinary Spanish idiom for "the two faces of"; a
gloss would have produced *los dos rostros*.

**3. `parts/grade-7/es/06-statistics.tex` (weekend problem, Part II) — native**

> En 1936, una revista estadounidense envió por correo diez millones de
> papeletas […] y predijo una victoria aplastante del candidato Landon.
> Un joven estadístico, George Gallup, preguntó solo a unas cincuenta mil
> personas --- elegidas para parecerse al conjunto de la población --- y
> predijo lo contrario. Roosevelt ganó por una goleada.

*victoria aplastante*, *ganó por una goleada*: Spanish politics/sports idiom,
not *landslide* transliterated.

**4. `parts/grade-9/solutions/es/01-fractions-and-powers.tex`, q. 9 — native**

> $0.999\ldots$ \emph{es} el número $1$, escrito con un segundo disfraz.
> Cualquier número estrictamente menor que $1$ deja un hueco, y \cref{…}
> mostró que un hueco siempre contiene más números --- mientras que entre
> $0.999\ldots$ y $1$ no cabe nada.

*escrito con un segundo disfraz*, *no cabe nada*: the register of a Spanish
teacher settling the argument, not of a translated sentence.

**5. `parts/grade-9/es/08-solids-and-volumes.tex` (Archimedes) — near-native**

> Un siglo después, el escritor romano Cicerón, buscando entre las zarzas
> cerca de Siracusa, reconoció la tumba «por la esfera y el cilindro».

Correct and idiomatic; *buscando entre las zarzas* is a shade more literal
than a Spanish essayist's *rebuscando entre la maleza*. This is the register
ceiling of the pass: the historical asides read as very good Spanish prose
rather than as Spanish prose that could not have been written in English
first.

## Why not 100

1. **`def:g4:numbers:classes` has no Spanish links** — `harvest.py` matches a
   bare `\emph{…}` against the English label leaf, so `clases` ≠ `classes`
   (Dutch has the same gap). Fixing it needs a shared file, which this pass
   was not allowed to touch.
2. **`tools/term_config/lang_es.py` pluralises only the last word**
   (`WORD_TAIL` on the tail token), which is not how a Spanish noun phrase
   inflects: *número primo* → *números primos*, not *número primos*. Worked
   around with a 27-entry `DERIVED` in `book1_es.py`, but any multi-word term
   not in that list still misses its plural. The general fix belongs in the
   shared language config.
3. **`punto decimal`, not `coma decimal`.** The printed numerals use a
   decimal *point* (`$2.37$`) throughout the series, so *coma decimal* would
   contradict every figure on the page; *punto decimal* is RAE-accepted but
   is not what a Spanish classroom says first.
4. **`circunferencia` is not linkable.** Mirroring the English stoplist keeps
   the target sets equal and the pages readable, but a Spanish reader may
   expect the word to carry a link to its definition.
5. **`mediana` links to the statistical median even inside the grade-8
   triangle-median problem.** Inherited English behaviour (the term is
   harvested once, from grade 9); parity was preferred over a local fix.
6. **`media` is linked globally behind a protect list.** The half-senses
   (*media hora*, *media vuelta*, *media altura*, *media esfera*, *paralela
   media*) are each protected by name; a future phrase of that shape would
   mis-link until the list is extended.
7. **Register ceiling on the historical/expository asides** (sample 5): very
   good Spanish, occasionally a shade closer to the English clause order than
   an original Spanish author would write.

## Status

**Meets ship threshold (≥ 95): 97 / 100.** Working tree left uncommitted for
human review; no shared file was modified.

---

## Addendum — 2026-07-27, after the per-book runs

Two shared-tooling defects that this book's run reported but correctly did
**not** edit (they are shared across all Spanish books) were fixed afterwards
by the orchestrating session, once every per-book agent had finished:

1. **`tools/term_config/lang_es.py` now sets `TAIL_ON_EVERY_WORD = True`.**
   Spanish inflects every word of a noun phrase, exactly as French does
   (`lang_fr.py` has always set `True`); with `False` the plural tail was tried
   on the last word only, so every regular compound plural went unlinked. Four
   of the five math books had independently worked around this by declaring
   plurals by hand. The now-redundant declarations were removed
   (23 in book1, 5 in book2, 38 in book4); entries for irregular plurals
   (*función* -> *funciones*, *raíz* -> *raíces*, *afín* -> *afines*), gender
   changes and the -idad/-itud nominalisations are genuinely still needed and
   were kept.

2. **`tools/termlink/harvest.py` no longer tests a translated bare `\emph{…}`
   against the English label leaf.** That test can never pass in a translation
   (`clases` vs the leaf `classes`), which silently dropped whole definitions
   from every non-English edition. A translation now defers to the emphases its
   English twin accepted, matched by ordinal position — sound because the
   translation gates already enforce an exact structural mirror. English keeps
   its own leaf rule and is provably unaffected: all five English books
   regenerate byte-identically and `check_book5_golden.sh` passes.

Termlinks were then regenerated for this book: **3742 -> 3742 links**. Re-verified
after the change: `check_translation.sh` green for every year, `latexmk`
0 errors / 0 undefined / 0 overfull, page count unchanged, no nested links, and
`\omterm` target parity now shows **zero English targets missing in Spanish**
(the remaining Spanish-only targets are the curated extras the FR edition also
carries).

The score above is unchanged: these were link-coverage and tooling fixes, not
prose changes.
