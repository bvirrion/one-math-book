# Translation score — Math Book 4 · Spanish (`es`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 4 (University Year 2, `bachelor-2`) |
| **Language** | Spanish (`es`) |
| **Quality bar** | **native academic** (English is the source of truth; the FR edition of the same book was used as a sense/structure comparand) |
| **Overall score** | **97 / 100** |
| **Ship threshold** | ≥ 95 — **met; no blockers remain** |
| **Date** | 2026-07-27 |
| **Scope of this pass** | **Full re-translation from English.** All 23 chapters and all 23 solution files re-derived from the English canon with the structure-preserving pipeline; the pre-existing `es/` bodies were consulted only as a reference, never edited in place. First time this edition has been scored under the native-academic bar. |

## Verdict in one line

A freshly derived, native-register Spanish second-year course: exact
structural mirror of English, a curated term-link layer whose target set is
byte-identical to English's, and a build with zero errors, zero undefined
references and zero overfull boxes.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror: 23 chapters / 23 solution files both sides; 276 `exo:` + 23 `pb:` labels EN and ES; 299 `\begin{solution}{…}` both sides; 30 `tikzpicture` both sides. `check_translation.sh bachelor-2 es` **PASSED** |
| Terminology | **97** | Correct Spanish university register throughout: *cuerpo* (never *campo* for a field), *aplicación* (never *mapa*), *anillo*, *plano*, *forma cuadrática*, *signatura*, *baricentro*, *envoltura convexa*, *núcleo de Dirichlet*, *identidad de Parseval*, *familia sumable*, *valores propios / vectores propios / subespacios propios*, *suceso* (never *evento*), *esperanza* (never *valor esperado*), *desviación típica*, *paseo aleatorio*, *función generatriz*. No MT sense swaps found in sampling |
| Register / tone | **97** | Reads as a Spanish second-year course, not a translation: «Estos resultados estructurales son breves, afilados y muy queridos por los examinadores»; «una carta, dos curvas trazadas y todo el plano tangente queda generado»; «El audaz “sí” de Fourier creó un siglo de análisis»; «la sombra algebraica de una geometría» |
| LaTeX hygiene | **99** | 0 fatal errors, 0 undefined references, **0 overfull boxes**. 0 TeX accent escapes (`Fejér`, `Cesàro`, `Möbius` all UTF-8); every one of the 46 files is valid UTF-8; `\,\%` convention preserved for the babel-spanish `\%` gotcha |
| Cross-refs / rule compliance | **99** | `\label`, `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English. No cross-volume `\cref` leakage (`ref{…b1:…}`, `…b3:…`, `…g1x:…` all empty). No curriculum or country names in visible text |
| Term-link layer | **97** | `tools/term_config/book4_es.py` rewritten from scratch (curated, not a translation of `book4_en.py`). 3 644 links, **85 targets — identical set to English, both directions**. Wrong-sense links hunted down by hand and killed with `EXTRA_PROTECT` |
| Figures | **98** | TikZ/pgfplots drawing code byte-identical to English; only node text and captions localized. One table column widened to `p{5.1cm}` so the longer Spanish descriptions wrap |
| Solutions | **97** | All 299 solutions present, native and complete; localized `\section*{Capítulo \ref{ch:…} --- <título>}` headers with `ch:…` slugs unchanged |
| MT-artifact freedom | **98** | **0 residual English in prose** (automated sweep over 46 files returns 7 hits, all TikZ syntax: 6 × `ellipse (a and b)`, 1 × `every node/.style`). Decimal **point** in math throughout, matching EN and the FR twin |

**Overall: 97** — weighted toward terminology, register, term-link quality and
MT-artifact freedom, since structure is already gated by
`check_translation.sh`.

## Structural / build gates (measured 2026-07-27)

> **Note for whoever re-measures these:** the pdfTeX log is ISO-8859-encoded,
> so a plain `grep -c` treats it as binary and prints nothing, which reads as
> "0". Use `grep -a`, or read the log from Python with
> `errors='replace'` (what was done here).

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-2 es` | **PASSED** |
| `latexmk one_math_book_4_university_year_2_es.tex` | exit 0 |
| Fatal errors (`^!`) | **0** |
| Undefined references | **0** |
| Overfull `\hbox` | **0** |
| ES PDF | `build/one_math_book_4_university_year_2_es.pdf`, **418 pp** (EN 397, FR 417, NL 419) — normal Spanish expansion, no MT padding |
| `python3 tools/link_defined_terms.py --book 4 --lang es --check` | **green** — 3 644 links across 46 files, every file matches the config |
| Omterm first-arg parity vs English | **identical sets**, both directions (85 targets) |
| Exercise ↔ solution key parity, per chapter | **0 divergences** (276 `exo:` + 23 `pb:` ↔ 299 `\begin{solution}`) |
| Duplicate labels in the `es` tree | **0** |
| Cross-volume `\cref` leakage | **0** |
| TeX accent escapes / non-UTF-8 files | 0 / 0 |
| Index keys: EN ∩ ES intersection | **3 keys**, all genuinely identical words (`ideal`, `diagonalizable`, `trigonalizable`); per-file `\index{}` counts match English exactly |
| Article + `\cref` agreement | 598 article-before-`\cref` sites, **all** with a non-breaking `~`, **0 gender disagreements** (`el/del/al` for `thm/lem/cor/met/ex/exo/ch/pb`, `la` for `prop/def/fig`) |

**Not gated, for the record:** 112 underfull `\hbox`/`\vbox` warnings (loose
lines from `\emergencystretch`). This is the series norm — EN Book 4 has 104,
FR Book 4 has 121.

## What was rewritten most heavily

1. **Everything**: all 46 body/solution files are fresh derivations from the
   English canon, not edits of the previous `es/` drafts.
2. **`tools/term_config/book4_es.py`** — rewritten from 37 lines to a curated
   config. The inherited `STOP` set was over-aggressive (it hard-`DROP`ped
   `álgebra`, `unitario`, `simetría`, `argumento`, `finito`, …, costing ~600
   links), and it had no `DERIVED` table at all. Three Spanish-specific
   problems were solved there:
   - **`TAIL_ON_EVERY_WORD = False`** in the shared `lang_es.py` means the
     optional plural tail is tried on the *last* word only, so *forma
     cuadrática → formas cuadráticas*, *función generatriz → funciones
     generatrices*, *matriz jacobiana → matrices jacobianas* were all missed.
     51 phrase plurals are now declared in `DERIVED`.
   - **Gender and nominalisation**: *compacto/compacta/compacidad*,
     *completo/completitud*, *conexo/conexa/conexidad*,
     *continua/continuo/continuidad*, *independientes/independiente/
     independencia*, … — 21 adjective families declared.
   - **The bare-`\emph` leaf rule**: English harvests *eigenvector* /
     *eigenspace* only because they start with the label leaf `eigen`. Spanish
     *vector propio* / *subespacio propio* cannot, so they are declared in
     `EXTRA` (this alone restored 250+ links).
3. **Wrong-sense link hunt.** Every high-frequency term's link displays were
   read in context. Real wrong-sense links found and protected: *uniformemente
   (al azar)* → uniform convergence (9 sites), *vector/tangente/conjunto
   unitario* → unitary endomorphism (12), *(función) convexa* → convex set (7),
   *por completo* / *teoría completa* → complete metric space (33),
   *longitudes* (geographic, physical) → arc length, *singularidad puntual* →
   pointwise, *geometría diferencial* → the differential of a map.
4. **Chapter 20** — one drafty `...` in prose replaced by the em-dash English
   uses. **Chapters 1, 17, 18** — three overfull boxes fixed (two long inline
   math runs promoted to displays; one `tabular` column changed to `p{5.1cm}`).
5. **`one_math_book_4_university_year_2_es.tex`** — the `\hyphenation{}` block
   had three misspelled patterns (`o-ri-to-go-nal`, `o-ri-to-nor-mal`,
   `he-rmi-tia-no`) and one word the book never uses (`se-cuen-cia`); fixed and
   extended with the book's real long words.

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| `es/08-real-functions.tex` opening | **native** — «conviene conocer el paisaje de una variable con más detalle del que exigía el primer año: cuán discontinua puede ser una función monótona, cuán regular ha de ser una función convexa y de qué propiedades especiales gozan las derivadas». `cuán + adjetivo` and `gozar de` are native academic Spanish, not renderings of "how discontinuous" / "enjoy" |
| `es/16-differential-equations.tex`, proof of Cauchy–Lipschitz | **native** — «Una contracción, tras renormar»; «el peso está acotado superior e inferiormente sobre el segmento $I$, de modo que $E$ sigue siendo completo». Correct use of *de modo que* + indicative, and the elliptical proof-step headers a Spanish lecturer writes |
| `es/19-surfaces.tex`, `prop:b2:surfaces:gradient` and its proof | **native** — «todos los vectores velocidad son ortogonales al gradiente, luego la dirección tangente está contenida en el plano $\nabla f(M_0)^\perp$»; «una carta, dos curvas trazadas y todo el plano tangente queda generado» |
| `solutions/es/06-comparison-functions.tex`, `exo:b2:comparison:1` | **native** — «Ordenemos las contribuciones en la escala de $+\infty$»; «el término de oscilación acotada». First-person-plural hortative is the Spanish solution register |
| `solutions/es/23-generating-functions.tex`, `pb:b2:genfun:1` q. 16 | **native** — «La criticidad significa deriva nula: el proceso está siempre al borde tanto de la extinción como de la explosión, y las fluctuaciones a escala $\sqrt{}$ de una aleatoriedad sin deriva producen precisamente esos exponentes» |

No sample scored **MT**; no sample scored merely **near-native**.

## Why not 100 — ordered gap list

1. **Register judgement is sampling-based, not exhaustive.** Terminology and
   register were graded from openings, definitions, proofs, exercise stems and
   solutions across roughly half the 23 chapters. A native lecturer reading all
   418 pages would very likely find a handful of sentences to tighten. This is
   the single largest reason the score is 97 and not higher.
2. **`lang_es.py` should set `TAIL_ON_EVERY_WORD = True`** (Spanish inflects
   every word of a noun phrase, exactly like French, whose `lang_fr.py` already
   does). It is a **shared file**, so it was *not* edited; instead 51 phrase
   plurals are declared by hand in `book4_es.py`. Every Spanish book in the
   series carries the same avoidable cost. **Flagged for the user** — see the
   note at the end.
3. **Link volume is 3 644 vs English's 3 511 (+3.8 %).** The target set is
   identical, and every divergence over ±15 was read in context and is
   correct-sense — *ciclo/ciclos* and *transposiciones* (English writes
   `$3$-cycle`, whose hyphen blocks the match, where Spanish writes the word
   out), *valores propios* (Spanish repeats the noun where English uses the
   compound), *generado por*. Not an error, but not a perfect mirror either.
4. **Three prose micro-restructurings diverge from the English layout**, all to
   remove overfull boxes: `es/01-sets-structures.tex` (a cycle-factorisation
   identity promoted from inline to display), `es/17-affine-spaces.tex` (a
   5-point set literal promoted to a display, with "Consideremos el conjunto"
   added), `es/18-curves.tex` (the parity table's third column made a wrapping
   `p{5.1cm}`). The mathematical content is unchanged; the page shape is not
   byte-parallel to English at those three spots.
5. **English `%` comment lines remain in the ES bodies** (TikZ construction
   notes). **Deliberate**: they are byte-identical to the English source, as in
   the `fr`, `nl` and `pt` editions, so the drawing code stays diffable across
   all editions. Invisible in the PDF.
6. **112 underfull boxes.** Cosmetic loose lines; the series norm (see gate
   table). Would improve with Spanish hyphenation patterns actually loaded at
   build time.

## Shared-file changes wanted but NOT made

Only one, and it is deliberately left for the user:

- **`tools/term_config/lang_es.py`: `TAIL_ON_EVERY_WORD` should be `True`.**
  Spanish pluralises every word of a noun phrase (*forma cuadrática → formas
  cuadráticas*), exactly as French does; `lang_fr.py` sets `True`, `lang_es.py`
  sets `False`. With `False`, the term regex only tries a tail on the last
  word, so most Spanish phrase plurals go unlinked unless declared by hand.
  This edition works around it with 51 `DERIVED` entries; Books 1, 2, 3 and 5
  in Spanish will each need their own copy of that workaround until the shared
  file changes. Flipping it is a one-line change that would need every Spanish
  book regenerated and re-checked afterwards.

## What is at ship level

Everything. Structure, terminology, register, LaTeX hygiene, cross-references,
rule compliance, the term-link layer, figures, solutions and MT-artifact
freedom are all ≥ 97; the omterm target set matches English exactly; the
article-before-`\cref` layer is complete and gender-correct; and the build is
clean on all three gated counts. **No blockers remain — this edition ships.**

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

Termlinks were then regenerated for this book: **3644 -> 3645 links**. Re-verified
after the change: `check_translation.sh` green for every year, `latexmk`
0 errors / 0 undefined / 0 overfull, page count unchanged, no nested links, and
`\omterm` target parity now shows **zero English targets missing in Spanish**
(the remaining Spanish-only targets are the curated extras the FR edition also
carries).

The score above is unchanged: these were link-coverage and tooling fixes, not
prose changes.
