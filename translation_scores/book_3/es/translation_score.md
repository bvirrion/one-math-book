# Translation score — Math Book 3 · Spanish (`es`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 3 (University Year 1, `bachelor-1`) |
| **Language** | Spanish (`es`) |
| **Quality bar** | **native academic** (EN is the source of truth; the FR edition was consulted only as a sense reference, never as a source) |
| **Overall score** | **97 / 100** |
| **Ship threshold** | ≥ 95 — **MET** |
| **Date** | 2026-07-27 |
| **Scope of this pass** | **Full re-translation from English** of all 50 files (25 chapters + 25 solution files), plus a rebuilt `tools/term_config/book3_es.py`, regenerated `\omterm` links, and a hygiene/register audit. The previous `es/` bodies were not used as a draft. |

## Verdict in one line

Structurally byte-exact against English, written in native Spanish university
register, with the defined-term link map now target-for-target identical to
the English edition and every gate green.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror: 25 chapters, 25 solution files, **300** `exo:` labels EN / 300 ES, **25** `pb:` / 25, **325** `\begin{solution}{…}` on both sides, and the `\label{}` multiset is byte-identical to English (`diff` empty). `check_translation.sh bachelor-1 es` **PASSED** |
| Terminology | **97** | Consistent university register: *aplicación* (not *mapa*), *cuerpo* (not *campo*), *clausura*/*interior*, *familia libre*, *teorema de la base incompleta*, *teorema del rango*, *fórmula de Grassmann*, *desarrollo limitado*→*desarrollo asintótico*, *sumas de Riemann*, *fracciones simples*, *punto de retroceso* (cusp), *punto de silla*, *mínimos cuadrados*, *ecuaciones normales*. No sense swaps found in sampling |
| Register / tone | **96** | Reads as a Spanish first-year lecture course. Exercise stems use the Spanish impersonal imperative (*Calcúlense*, *Demuéstrese*, *Hállense*, *Dedúzcase*), questions carry `¿`, and quotations use `«…»`. Two mild calques found and repaired (*soporta* → *sostiene*, ×2) |
| LaTeX hygiene | **99** | 0 fatal errors, 0 undefined references, **0 Overfull `\hbox`**; **0** TeX accent escapes (UTF-8 throughout); the `$t\,\%$` convention restored in the 3 places where it had been lost |
| Cross-refs / rule compliance | **98** | `\label`, `\cref`/`\ref` targets (multiset identical, `diff` empty) and `\begin{solution}{key}` byte-identical to English. Rule 7 clean: no country or curriculum name in visible text (one *instituto* rewritten to *la secundaria*); cross-volume references stay prose-only (*el volumen anterior* ×20, *el volumen del segundo año* ×28, *del tercer año* ×13) |
| Figures | **97** | All TikZ/pgfplots drawing code byte-identical; only node text and captions localized (2 English node labels, `axis of $r_{1,2}$`, caught and fixed in this pass) |
| Solutions | **97** | All 325 solutions present, complete and native; headers `\section*{Capítulo \ref{ch:…} --- <título>}` with `ch:…` slugs unchanged |
| MT-artifact freedom | **96** | An English-function-word sweep over all 50 files now returns **only** TikZ syntax (`controls … and …`, `circle (r and r)`) and one `%` comment. 16 genuine English leftovers were found and fixed in this pass (see below) — none remains, but the sweep is heuristic, so a residual fragment in an unscanned form cannot be excluded with certainty |

**Overall: 97** (weighted register 0.20, terminology 0.20, MT-freedom 0.18,
cross-refs/rule compliance 0.12, LaTeX hygiene 0.10, solutions 0.08,
figures 0.06, structure 0.06 → 97.1).

## Structural / build gates

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-1 es` | **PASSED** |
| `python3 tools/link_defined_terms.py --book 3 --lang es --unwrap --apply` then `--apply` | 4 141 removed → **4 211 links across 50 files** (EN: 3 944) |
| `python3 tools/link_defined_terms.py --book 3 --lang es --check` | **green** — "every file matches what the config generates" |
| `latexmk one_math_book_3_university_year_1_es.tex` | exit 0 |
| Fatal errors (`^!`) | **0** |
| Undefined references | **0** |
| Overfull `\hbox` | **0** (Underfull 122, the usual ragged-right noise; EN and FR are in the same band) |
| PDF | `build/one_math_book_3_university_year_1_es.pdf`, **413 pp** (EN 395, FR 416, NL 411) — +4.6 %, normal Spanish expansion, no MT padding |
| Exercise / problem / solution census vs EN | 300/300, 25/25, 325/325 |
| `\label` / `\cref` / solution-key multisets vs EN | identical (`diff` empty) |
| TeX accent escapes | **0** |
| `\omterm` **target set** vs EN | identical (both harvests resolve to the same 106-target set; 2 targets are *used* in ES prose that English happens not to use — `def:b1:structures:law`, `thm:b1:matrices:conjugation` — both verified correct-sense) |

## Term configuration rebuilt (`tools/term_config/book3_es.py`)

The stub that existed (7 stoplist words, no `EXTRA`, no `DROP`, no
`EXTRA_PROTECT`) produced both under- and over-linking. It was replaced by a
curated config, written against the English term list word by word:

* **`NOT_A_TERM`** — result heads (*teorema*, *lema*, *desigualdad*,
  *fórmula*, *regla*, *ley(es) de*, *estimación*, …). `criterio` was
  **removed** from the stub's list: it was silently killing *criterio del
  cociente*, which English links (`ratio test → thm:b1:series:ratio`).
* **`DROP`** — result names that reach the harvest through
  `\emph{}\index{}` and so bypass `NOT_A_TERM` (*teorema de Kummer*,
  *fórmula de Legendre*, *desigualdad de Ptolomeo*, *leyes de De Morgan*,
  *ecuación funcional*, *estimación de las series alternadas*), plus the bare
  adjectives English never links (*directa*, *equivalentes*, *semejantes*,
  *algebraico*, *trascendente*, *crítico*) and *argumento*, which is the
  register word (*«el mismo argumento, hecho dentro de $\mathbb U_n$»*)
  inside the very chapter that defines it — `STOP` would have been too soft.
* **`EXTRA`** — the forms the harvest cannot see: *derivable* /
  *derivabilidad* (the definition emphasises `derivable en $x_0 \in I$`, pure
  inline math), bare *ortogonal* / *ortogonalidad* / *ortogonalmente*,
  *traspuesta* / *trasposición*, *criterio del cociente*, *ley de la torre*,
  *clase de equivalencia*, *ecuación diferencial lineal de primer orden*
  (six words, past the harvest's word cap), and *constante de Euler* pinned
  to `pb:b1:series:1` so it resolves exactly where English resolves it.
* **`DERIVED`** — the Spanish forms `WORD_TAIL = (?:e?s)?` cannot spell:
  *continuo/continua*, *convexo/convexidad*,
  *inyectivo/inyectividad/inyección* (and the *sobre-*/*bi-* families),
  *dividen*, *abierta*, *cerrada*, *densa*, *conjugada*.
* **`EXTRA_PROTECT`** — the Spanish spans where a good term means something
  else: *álgebra lineal*, *combinación lineal*, *ejercicio de aplicación*,
  *módulo de continuidad*, *cuerpo no numerable*, *forma integral*, *en su
  conjunto*, *en el interior de la…*, *lazo interior*, *base $b$*, *de forma
  continua*.
* **Plural compounds** — 37 hand-declared entries (see the shared-file note
  below).

## English leftovers found and fixed (16)

Range-based translation leaves the untouched English line in place, and a
math/label parity checker cannot see prose. A full English-function-word
sweep over the 50 files caught every survivor:

| File | Leftover |
|------|----------|
| `es/07-algebraic-structures.tex` | a whole exercise clause: *“and that $\R_+^*$ is another; is $H \cup \R_+^*$ a …?”* |
| `es/07-algebraic-structures.tex` | *The operations*; `\index{symmetric group}\index{signature}\index{alternating group}` |
| `es/01-logic-sets-maps.tex` | two connective *and*s, a duplicated *first distributivity law in full:*, a stray *and* |
| `es/05-differential-equations.tex` | duplicated *Then* |
| `es/06-integer-arithmetic.tex` | duplicated *such pair works:* |
| `es/08-polynomials.tex` | *the root $1$ is multiple; dividing twice, …* |
| `es/11-sequences.tex` | duplicated *by the conjugate:* |
| `es/15-integration.tex` | duplicated *with* |
| `es/16-taylor-asymptotics.tex` | *so … with …*; duplicated *First,* |
| `es/17-numerical-series.tex` | two environment titles: *[Periodic decimals are geometric series]*, *[First facts]* |
| `es/23-euclidean-spaces.tex` | two TikZ node labels *axis of $r_1$ / $r_2$* |
| `solutions/es/16-taylor-asymptotics.tex` | *which is Machin's formula.* |

Every one of them sat immediately after a `\[…\]` display or inside a figure
— the two places a line-range patch most easily skips.

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| `es/12-topology-of-r.tex` opening | **native** — «Los límites remiten una y otra vez al mismo vocabulario geométrico: puntos «próximos a» un conjunto, conjuntos «sin fugas por la frontera», intervalos de los que las sucesiones no pueden escapar.» |
| `es/19-finite-dimension.tex` opening + `def:b1:findim:def` | **native** — «Las demostraciones de más abajo salen todas de un mismo motor combinatorio, el lema del intercambio: una familia libre nunca puede superar en número a una generadora.»; «$E$ es \emph{de dimensión finita} cuando…» is the standard Spanish definitional stem |
| `es/22-determinants-systems.tex` opening + `thm:b1:det:def` | **native** — «El determinante condensa en un solo escalar la respuesta a «¿son estos $n$ vectores una base?»»; «Hay exactamente una aplicación $\det \colon \mathcal M_n(K) \to K$…» |
| `es/16-taylor-asymptotics.tex` opening | **native** — «Cerca de un punto, una función regular vale tanto como un polinomio --- con un error controlable… se convierten en la herramienta más afilada del análisis elemental» |
| `solutions/es/17-numerical-series.tex` solutions 1–3 | **native** — «telescópica, $S_N = 1 - \frac{1}{N+1} \to 1$. Convergente, con suma $1$.» — the standard Spanish solution shorthand, with correct feminine agreement on *convergente*/*telescópica* (serie) |
| `es/25-two-variable-functions.tex` `rem:b1:multivar:pitfalls` | **near-native** — accurate and idiomatic, but the five-fault list keeps the English sentence rhythm more closely than the chapter openings do |

## Register audit performed in this pass

Every chapter was written sentence-by-sentence from the English (not
post-edited), so the audit targeted the two failure modes a from-scratch pass
still has: mechanical calques and untranslated fragments. Sweeps run over all
50 files: English function words; `\%` without the mandated thin space;
` ``…'' ` English quotes; `?`/`!` without `¿`/`¡`; anglicism list (*asumir*,
*mapa*, *campo*, *cerradura*, *chequear*, *es fácil de ver*, *proveer*,
*adicionalmente*, *de acuerdo a*); country/curriculum names; identical-prose
lines vs the English twin (107 hits, **all** TikZ coordinates and formulas).
Chapter openings and definition/theorem stems were read against their English
twins in **12, 16, 17, 19, 22, 24, 25** plus every file touched by a repair
(01, 03, 05, 06, 07, 08, 11, 12, 15, 16, 17, 23 and solutions 01, 12, 16, 22).

## Shared file that needs a change — NOT made

`tools/term_config/lang_es.py` sets **`TAIL_ON_EVERY_WORD = False`**. Spanish
agrees the adjective in the plural exactly as French does
(*aplicaciones lineales*, *curvas parametrizadas*, *puntos críticos*), and
`lang_fr.py` sets the flag to `True` for that reason; with `False`, a
multi-word term only ever grows its tail on the last word
(*curva parametrizadas*), so **every plural of a compound is missed**. The
file is shared with the other `es` books, so it was left untouched and the
gap was closed locally: 37 plural forms are hand-declared in `EXTRA` in
`book3_es.py` (that is how `def:b1:curves:def` regained its links). If the
flag is flipped for all Spanish books, those 37 entries should be deleted in
the same commit. The same remark applies to `lang_pt.py`.

## Why not 100 — ordered gap list

1. **The English-leftover sweep is heuristic.** It keys on English function
   words; a leftover consisting only of proper nouns, numerals and math
   would slip through. Sixteen leftovers were found and fixed, so the class
   was real; the residual risk is small but not zero.
2. **Register audit is sampled, not exhaustive.** Openings and statement
   stems were compared for 7 chapters plus the 16 repaired files; a residual
   calque in an unsampled paragraph cannot be excluded.
3. **Link counts diverge from English by construction.** ES carries 4 211
   `\omterm` links against 3 944 in English, on an identical target set: the
   Spanish adjective families (*continuo/continua*, *inyectivo/inyectiva*)
   and the hand-declared plurals simply match more often. Correct, but the
   editions are not link-for-link identical.
4. **Two link targets are used in Spanish prose that English leaves
   unlinked** (`def:b1:structures:law` in ch. 8 and 23,
   `thm:b1:matrices:conjugation` in ch. 21). Both were read in context and
   are the right sense; they exist because Spanish word order matches the
   defined term where English word order does not (*composition law* vs
   *ley de composición*).
5. **Spanish expansion.** 413 pp against 395 EN (+4.6 %). In the normal band
   (FR 416, NL 411) and not MT padding — spot-checked paragraphs match the
   English sentence for sentence — but the edition is not as tight as the
   English.

## What is at ship level

Every dimension is ≥ 96. Structure, terminology, register, hygiene,
cross-references, figures, solutions and MT-artifact freedom all pass; every
gate is green. **Ship.**

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

Termlinks were then regenerated for this book: **4211 -> 4209 links**. Re-verified
after the change: `check_translation.sh` green for every year, `latexmk`
0 errors / 0 undefined / 0 overfull, page count unchanged, no nested links, and
`\omterm` target parity now shows **zero English targets missing in Spanish**
(the remaining Spanish-only targets are the curated extras the FR edition also
carries).

The score above is unchanged: these were link-coverage and tooling fixes, not
prose changes.
