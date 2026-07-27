# Translation score — Math Book 2 · Spanish (`es`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 2 (High School, grades 10–12) |
| **Language** | Spanish (`es`) |
| **Quality bar** | **native academic** (English is the source of truth; the FR Book 2 edition was used as the sense/structure reference per `translation_instruction.md`) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **MET** |
| **Date** | 2026-07-27 |
| **Scope of this pass** | **Full re-translation from English.** The pre-existing `es/` tree was raw machine translation and was *not* used as a draft. All 35 chapters and all 35 solutions files were re-derived from `parts/grade-1{0,1,2}/*.tex` and `.../solutions/*.tex` with the structure-preserving pipeline, then post-fixed, gated, term-linked and reviewed. |

## Verdict in one line

Book 2 now exists in Spanish as a **written** book rather than a translated
one: 35 chapters, 343 graded exercises, 35 weekend problems, 378 solutions,
all three structural gates green, and a PDF with **0 errors, 0 undefined
references and 0 overfull boxes** at 343 pages — exactly the FR page count.

## Why a full re-translation

The `es/` tree that existed before this pass was unsalvageable MT. Three
representative defects, all from `grade-10/es/01-numbers-and-sets.tex`:

| Pre-existing ES | English | Problem |
|-----------------|---------|---------|
| «Si $p$ eran extraños» | *if $p$ were odd* | `odd` read as *strange*, plus number disagreement |
| «Ni siquiera ambos» | *not both even* | `even` read as *even (adverb)* — the sentence says the opposite |
| «numeros naturales» | *natural numbers* | missing accents throughout (would fail the UTF-8 gate) |

Tabular cells and TikZ node text were also left in English in several
chapters. Editing that was not cheaper than writing the book; it was
rewritten.

## Structural census — ES vs EN

| Item | EN | ES |
|------|---:|---:|
| Chapter files | 35 | **35** |
| Solutions files | 35 | **35** |
| `\begin{exercise}` | 343 | **343** |
| `\begin{problem}` (weekend problems) | 35 | **35** |
| `\begin{solution}` | 378 | **378** |
| `pb:` labels | 35 | **35** |
| `\textbf{Part/Parte N ---}` headers | 140 | **140** |
| `enumerate[resume]` | 105 | **105** |
| `\begin{tikzpicture}` | 87 | **87** |
| `\begin{omfigure}` | 80 | **80** |
| `\admitted` | 3 | **3** |
| Source lines (bodies + solutions) | — | 23 663 |
| `\omterm` links | 3 906 | **3 739** |
| PDF pages | 330 | **343** (FR 343, NL 342) |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | `check_translation.sh` PASSES for grade-10, grade-11 and grade-12: file completeness, identical label sets *and order*, per-environment census, no duplicate labels. Per chapter, the ordered `exo:`/`pb:` list in the body equals the ordered `\begin{solution}{…}` key list — verified independently for all 35 chapters. Every weekend problem keeps its four-part skeleton and its ~20 questions one for one |
| Terminology | **97** | Spanish school-mathematics vocabulary, chosen from Spanish practice rather than transposed: *inecuación*, *forma canónica*, *tabla de signos*, *tasa de variación media*, *recta secante*, *primitiva*, *punto de inflexión*, *sucesión*, *razón*/*diferencia*, *criterio de comparación*, *forma binómica*, *afijo*, *módulo*/*argumento*, *raíces de la unidad*, *mediatriz*, *homotecia*, *división euclídea*, *primos entre sí*, *pequeño teorema de Fermat*, *lema de Gauss*, *rectas que se cruzan*, *vector normal*, *ley de la probabilidad total*, *falacia del fiscal*, *distribución binomial*, *desviación típica*, *ley de los grandes números*, *media muestral*, *intervalo de fluctuación*, *falta de memoria*, *paradoja de la inspección*. No MT sense swaps found on review |
| Register / tone | **96** | Spanish school register: **2nd-person-singular imperative** in every exercise and problem stem (*Calcula, Demuestra, Deduce, Resuelve, Halla, Determina, Comprueba, Explica, Concluye*) — what a Spanish exercise sheet actually says, and applied uniformly across all three years. Chapter hooks are written, not rendered: «Una matriz es una máquina que se come un estado y devuelve el siguiente», «La trigonometría empieza en los triángulos rectángulos, pero su verdadera casa es la circunferencia unidad», «Un jugador de ruleta, después de 100 tiradas, va ganando casi tantas veces como no». No *usted*/*vosotros* leakage (0 occurrences) |
| LaTeX hygiene | **99** | 0 fatal errors, 0 undefined references, **0 overfull boxes**, 118 underfull (EN 120, FR 117 — series norm). **0** TeX accent escapes anywhere in the ES tree: English's `Vi\`ete`, `Bienaym\'e`, `\"Otzi`, `Chevalier de M\'er\'e` are *Viète*, *Bienaymé*, *Ötzi*, *caballero de Méré* in UTF-8. The babel-spanish rule is honoured everywhere: **0** occurrences of `[0-9]\%`; every percentage is `$60\,\%$`. Two overfull boxes introduced by longer Spanish prose were fixed at source (the modulus-properties display in `grade-12/es/09`, the `\sqrt{\text{…}}` inline in `grade-12/solutions/es/03`) |
| Cross-refs / rule compliance | **98** | Every `\label{…}`, every `\cref` target and every `\begin{solution}{…}` key is byte-identical to English — the label diff is empty for all three years. **0 curriculum or country names** in visible text: EN's "the Middle School volume", "grade 11", "grade 12", "the university volumes" became «el volumen anterior», «el curso que viene», «el año que viene», «los volúmenes universitarios». The only bare `\ref` is the mandated `\section*{Capítulo \ref{ch:…} --- …}` header, and its title matches the body `\chapter{…}` in all 35 pairs |
| Figures | **97** | TikZ/pgfplots drawing code copied byte for byte (87 `tikzpicture`, 80 `omfigure`, both = EN); only node text and `{\small …}` captions are Spanish. Coded labels were localized without touching node *names*: *S/F* → **E/F** (éxito/fracaso) in the Bernoulli tree, *R/B* → **R/A** (rojo/azul) in the urn trees, *mark/grade* → *nota*, *min/max* → *mín/máx*. Decimal points inside figures left as in EN for consistency with the rest of the book |
| Solutions | **97** | All 378 present, each with the `\textbf{1.}`…`\textbf{20.}` numbering of its English twin and the same numerical answers, spot-checked value by value across the volume: Cassini's $(-1)^n$, $\gcd(1071,462)=21$ with $u=-3, v=7$, $n \equiv 23 \pmod{105}$, the regular hexagon's $\frac{3\sqrt3}{4}$, the $109.5^\circ$ diamond angle, the $\frac16$ Bayes screening verdict, the $27\sigma$ casino, $\frac{13\,000}{200} = 65$ for the inspection paradox |
| MT-artifact freedom | **97** | **0 residual English** in prose (the only English tokens in the ES tree are TikZ/pgfplots keywords and English-identical labels). English participial and nominal chains were re-cast as Spanish finite clauses rather than transposed: *"Long considered the purest of pure mathematics, it now protects…"* → «Durante mucho tiempo se la consideró la más pura de las matemáticas puras y hoy protege…»; *"the drift outruns the noise"* → «la deriva adelanta al ruido». Idioms localized, not calqued: *the house always wins* → «la banca siempre gana», *gambler's fallacy* → «falacia del jugador», *free lunch* → «comida gratis», *too close to call* → «demasiado igualado para pronunciarse», *skew lines* → «rectas que se cruzan» |

**Overall: 96.** Weighting register, terminology and MT-artifact freedom above
structure (structure being separately gated), the edition ships.

## Structural / build gates

> **Measurement note.** pdfTeX writes `build/*.log` as ISO-8859 text, so a
> plain `grep -c` treats it as binary and prints nothing (which reads as
> "0"). **All counts below were taken with `grep -a`.**

| Gate | Command | Result |
|------|---------|--------|
| Structure, grade-10 | `bash tools/check_translation.sh grade-10 es` | **PASSED** |
| Structure, grade-11 | `bash tools/check_translation.sh grade-11 es` | **PASSED** |
| Structure, grade-12 | `bash tools/check_translation.sh grade-12 es` | **PASSED** |
| Build | `latexmk one_math_book_2_high_school_es.tex` | exit 0 |
| Fatal errors | `grep -ac '^!' build/…_es.log` | **0** |
| Undefined references | `grep -aci 'undefined' build/…_es.log` | **0** |
| Overfull `\hbox` | `grep -ac 'Overfull' build/…_es.log` | **0** |
| Underfull `\hbox` | `grep -ac 'Underfull' build/…_es.log` | 118 (EN 120, FR 117 — series norm) |
| `Missing character … nullfont` | `grep -ac 'Missing character'` | 50 — **identical in EN, FR and NL**; a shared-figure artifact, not an ES defect |
| PDF | `build/one_math_book_2_high_school_es.pdf` | **343 pp**, 2.6 MB |
| Term links | `link_defined_terms.py --book 2 --lang es --unwrap --apply` then `--apply` | **3 739** links across 70 files; targets `def 3518, prop 88, pb 51, thm 35, met 31, ex 16` (EN 3 906, FR 4 024, NL 3 638) |
| Omterm target parity vs EN | `diff` of sorted target sets | EN ⊂ ES; two extra ES targets (`def:g12:contdist:uniform`, `thm:g12:contdist:memoryless`), both correct-sense links inside their own defining chapter — the same two extras the FR edition has |
| Exercise ↔ solution parity | per-chapter `diff` of label lists | all 35 chapters match |
| Chapter-title parity body ↔ solutions header | scripted compare | all 35 pairs match |
| Duplicate labels | `grep -rho 'label{…}' \| uniq -d` | none |
| TeX accent escapes | `grep -rnE "\\\\['\`\"^~=.]\{?[aeiouAEIOUNc]"` | **0** |
| Percent convention | `grep -rn '[0-9]\\%'` | **0** (all `\,\%`) |
| Curriculum / country names | targeted grep | **0** |

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| `grade-10/es/01-numbers-and-sets.tex`, chapter hook — «Las matemáticas empiezan con los números, y no todos los números son de la misma clase: los que sirven para contar, los negativos, las fracciones y números como $\sqrt 2$ o $\pi$ que ninguna fracción puede expresar.» | **native** — the relative «los que sirven para contar» is the Spanish way to nominalize; a translator would have produced «los números de contar» |
| `grade-12/es/10-arithmetic.tex`, weekend-problem opening — «G. H. Hardy presumía en 1940 de que la teoría de números estaba “sin mancillar” por las aplicaciones. Ochenta años después, cada pitido de un código de barras, cada pago con tarjeta y cada mensaje cifrado lo contradicen.» | **native** — *presumir de que* with its preposition, and the tricolon in Spanish rhythm; *boasted* is not rendered as the calque «se jactó» |
| `grade-12/solutions/es/16-continuous-distributions.tex`, q14 — «*el intervalo que te toca inspeccionar no es un intervalo típico, porque tenías más probabilidad de caer en uno grande.*» | **native** — «que te toca» carries English's *you happen to* idiomatically; the imperfect «tenías» is the correct Spanish tense for the counterfactual sampling frame |
| `grade-11/es/05-trigonometry.tex`, hook — «La trigonometría empieza en los triángulos rectángulos, pero su verdadera casa es la circunferencia unidad, donde el coseno y el seno pasan a ser funciones de un número real cualquiera.» | **native** — «pasan a ser» for *become*, «un número real cualquiera» for *any real number* (not the calque «cualquier número real» in this position) |
| `grade-12/es/11-matrices-graphs.tex`, problem opening — «Una matriz es una máquina que se come un estado y devuelve el siguiente; y sus *potencias* guardan, por tanto, futuros enteros.» | **near-native** — idiomatic and lively, but «se come» is colloquial register in what is otherwise an academic sentence; a Spanish editor might prefer «que consume un estado». Kept because the English is deliberately colloquial there too |

## Why not 100 — ordered gap list

1. **Peninsular Spanish, not neutral pan-Hispanic.** The edition consistently
   uses *ordenador* (5×), *coche* (29×), *zumo* (5×), *cerilla* (2×),
   *billete* (9×), *autobús* (9×) — Spain's lexicon. A Latin-American reader
   meets *computadora*, *carro/auto*, *jugo*, *fósforo*, *boleto*, *camión*.
   The choice was made once and applied uniformly (so it reads as a Spanish
   book rather than a mixed one), but it *is* a choice, and a pan-Hispanic
   pass would neutralize the ~50 affected tokens.
2. **Decimal point, not decimal comma.** `0.5`, `1.96`, `95.4` keep the
   English point. Spanish school books print `0,5`. This is a deliberate
   series-wide convention (FR and NL do the same, and the point is baked into
   the shared TikZ/pgfplots figures, which are copied byte for byte), so
   changing it in ES alone would break figure/text consistency — but it is
   the single most visible non-native detail on the page.
3. **`\gcd` prints "gcd", not "mcd".** In math mode the shared
   `\gcd` operator is used throughout; the prose says *máximo común divisor*.
   FR (*pgcd*) and NL (*ggd*) have exactly the same gap, because `\gcd` is
   LaTeX's own operator and is not language-aware in `styles/onemath.sty`.
   Fixing it means a **shared-file** change (a `\booklang`-switched
   `\DeclareMathOperator`), which this pass deliberately did not make — see
   "Shared-file notes" below.
4. **Two `\omterm` homograph collisions survive.** Spanish *muestra* is both
   the noun *sample* and the 3sg verb *shows*, and *divide* is both the
   arithmetic term and the ordinary verb. `tools/term_config/book2_es.py`
   now carries `EXTRA_PROTECT` patterns that remove the clear verb readings
   (5 wrong links killed), but the patterns are lexical, not syntactic: a
   sentence shaped `«… muestra <noun>»` that is not in the guarded list would
   still be linked. A syntactic guard is out of scope for a per-book config.
5. **Cross-volume references are uniformly «el volumen anterior».** English
   names "the Middle School volume" and points at individual weekend problems
   in it. Spanish renders the volume neutrally to keep the zero-curriculum
   record; the individual problems are still named by topic, so no reference
   is lost, but a little of English's pointedness is.
6. **343 pp against EN's 330 (+4 %).** Spanish runs longer than English by
   nature and the figure is identical to FR (343) and one page above NL
   (342), so the density is in series norm — but two or three of the longest
   solution files (`grade-12/16`, `grade-12/15`, `grade-12/13`) could each be
   tightened by a line or two.
7. **118 underfull boxes.** Reported for completeness only: English itself has
   120 and every language edition is in the same range.

## Shared-file notes

Nothing outside my scope was edited. `styles/onemath.sty`, `styles/lang/es.tex`,
`latexmkrc`, `.github/workflows/release.yml`, `tools/termlink/`,
`tools/link_defined_terms.py`, `tools/check_translation.sh`,
`tools/term_config/lang_es.py` and the other books' `book<N>_es.py` are
untouched. Two shared-file changes would raise the ceiling and are left for
the owner to decide:

- **`\gcd` → `mcd` / `pgcd` / `ggd`** — a `\booklang`-switched
  `\DeclareMathOperator` in `styles/onemath.sty` would fix gap 3 for ES, FR
  and NL at once.
- **Decimal separator** — a language-aware decimal macro (or a
  `\DeclareMathSymbol`-level comma) would fix gap 2 for ES/FR/NL/PT, but only
  if the shared TikZ figures are migrated to it in the same change.

`frontmatter/preface.es.tex` was reviewed and is **good native Spanish**
(«El estilo es conciso y riguroso: cursos construidos a partir de
definiciones, ejemplos, proposiciones y teoremas…»). No change needed, and
none made — it is shared across all ES editions.

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

Termlinks were then regenerated for this book: **3739 -> 3804 links**. Re-verified
after the change: `check_translation.sh` green for every year, `latexmk`
0 errors / 0 undefined / 0 overfull, page count unchanged, no nested links, and
`\omterm` target parity now shows **zero English targets missing in Spanish**
(the remaining Spanish-only targets are the curated extras the FR edition also
carries).

The score above is unchanged: these were link-coverage and tooling fixes, not
prose changes.
