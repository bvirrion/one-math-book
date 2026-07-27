# Translation score — Math Book 5 · Spanish (`es`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 5 (University Year 3, `bachelor-3`) |
| **Language** | Spanish (`es`) |
| **Quality bar** | **native academic** (English is the source of truth; the FR Book 5 edition was used as the intra-series reference for how far a translation of this book may reasonably depart from the English clause order) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **met** |
| **Date** | 2026-07-27 |
| **Scope of this pass** | **Full re-translation from the English canon.** All 46 files (23 chapters + 23 solution files) re-derived through the structure-preserving pipeline of `translation_instruction.md` §2; the pre-existing `es/` bodies were consulted only as a terminology reference, never edited in place. |

## Verdict in one line

A complete, structurally exact, natively-written Spanish third-year
course: every chapter and every solution re-derived from English through
a mask/translate/unmask pipeline that makes math, labels and figure code
byte-preservation a property of the method rather than of vigilance, with
a freshly curated term-link layer that reaches **exact `\omterm` target
parity** with English.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror: 23 chapters, 23 solution files, 722 `\label`s identical to English (set and order), 299 `exo:`/`pb:` labels ↔ 299 `\begin{solution}{…}` on both sides, weekend problems present in all 23 chapters. `check_translation.sh bachelor-3 es` **PASSED** |
| Terminology | **97** | Correct Spanish L3 register across the nine subject areas: *cuerpo* (never *campo*), *aplicación* (never *mapa*), *anillo*, *DIP/DFU*, *subgrupo normal*, *ecuación de clases*, *grupos resolubles*, *medida exterior*, *numerablemente aditiva*, *en casi todo punto*, *base hilbertiana*, *función holomorfa*, *residuo*, *sumersión/inmersión*, *forma cerrada/exacta*, *variable aleatoria*, *función característica*, *ley cero--uno*. No MT sense swaps found in sampling |
| Register / tone | **96** | Reads as a Spanish third-year lecture course: impersonal-passive imperatives (*demuéstrese*, *tómese*, *obsérvese*, *conclúyase*), *Sea $f$ una función…*, *Se dice que…*, *Supongamos que…*; exercise stems in the infinitive (*Demostrar que*, *Calcular*). Guillemets «…» used for scare quotes throughout |
| LaTeX hygiene | **98** | 0 fatal errors, 0 undefined references, **0 overfull boxes**. **0** TeX accent escapes — all accents UTF-8 (*Hölder*, *Möbius*, *Grönwall*, *Carathéodory*, *Rouché*, *Poincaré*, *Arzelà*, *Cesàro*, *Lévy*, *Apéry*, *Cramér*, *Sierpiński*) |
| Cross-refs / rule compliance | **99** | `\label`, `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English by construction (masked before translation). **Every one of the 1 207 `\cref` calls carries its Spanish article with a non-breaking tie** (`el~`, `la~`, `del~`, `al~`, keyed by label prefix) — 0 bare noun-position `\cref`. Zero curriculum/country names in visible text; cross-volume references are prose-only (*el volumen de segundo año*) |
| Figures | **98** | All TikZ/pgfplots drawing code byte-identical to English (masked as a hard environment); only node text and captions localized. 15 `tikzpicture`s and 11 `tabular`/`array` blocks audited by hand — the two English node strings and the six English table headers that survive byte-preservation were translated |
| Solutions | **97** | All 299 solutions present, complete and natively written; localized `\section*{Capítulo \ref{ch:…} --- <título>}` headers with `ch:…` slugs unchanged |
| MT-artifact freedom | **97** | **0 residual English** after stripping labels, environment names, macros and math from all 46 files. ~200 `\text{…}` strings inside protected math were translated in a dedicated post-pass; index entries are 100 % Spanish (EN∩ES index-key intersection is empty apart from proper names) |

**Overall: 96** (weighted toward terminology + register + MT-freedom;
structure is already gated by `check_translation.sh`).

## Structural / build gates (run 2026-07-27)

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-3 es` | **PASSED** |
| `sh tools/check_book5_golden.sh` | **PASSED** — "every file matches what the config generates"; the English sources were never touched |
| `latexmk one_math_book_5_university_year_3_es.tex` | exit 0 |
| Fatal errors (`^!`) | **0** |
| Undefined references | **0** |
| Overfull `\hbox` | **0** |
| Underfull (`\vbox` from `\output`) | 141 — English twin has 136; page-breaking noise, not a defect |
| `Missing character … nullfont` | 10 — **identical count in the English and French builds**; a preamble artifact, not ES-specific |
| PDF | `build/one_math_book_5_university_year_3_es.pdf`, **418 pp** (EN 395, FR 404, PT 405, NL 417) |
| `\omterm` **target parity** vs English | **exact** — 130 distinct targets on both sides; `set(ES) − set(EN)` and `set(EN) − set(ES)` are both empty |
| Term links | 4 449 across 46 files (EN 4 326, FR 4 251, NL/PT comparable) |
| Exercise ↔ solution parity | 299 / 299 both sides, key by key |
| Duplicate labels | none |
| `\end{proof>` typo class | none |
| Drafty `...` in prose | none |

## Method

Because the job was a *full* re-translation (~138 000 English prose words
across 46 files), the pass was run through a masking pipeline rather than
by editing files in place:

1. **Protect** — every `tikzpicture`, `axis`, `tabular`, `align`,
   `equation`, `gather`, `multline`, `verbatim` block, every `$…$` and
   `\[…\]`, every `\label`/`\cref`/`\ref`/`\eqref`/`\nameref`, every
   `\begin{solution}{key}`, every `\omterm{label}` first argument and
   every `enumerate`/`itemize` option list is replaced by a numbered
   placeholder. Cross-reference placeholders carry a `|thm`, `|prop`,
   `|def`, `|exo`, `|pb`, `|ch`, `|lem`, `|cor`, `|ex`, `|met`, `|sec`,
   `|eq`, `|rem` type hint, so the correct Spanish article can be chosen
   while writing.
2. **Translate** the remaining prose blocks.
3. **Unprotect** with an integrity check that refuses to write a file
   unless *every* protected span reappears exactly once (nesting-aware).
   This caught six dropped placeholders and one skipped block during the
   pass; none reached the tree.
4. **Second pass** over titles and `\omterm` display text, then the
   post-passes below.

The pipeline is why label/`\cref`/solution-key/figure-code fidelity is
100 %: those tokens never pass through the translation step at all.

### Post-passes run after the 23 chapter passes

- **`\text{…}` inside protected math** — 195 replacements across the
  book (`\text{a.s.}`→`\text{c.s.}`, `\text{LHS}`/`\text{RHS}`→
  `\text{MI}`/`\text{MD}`, `\text{even}`→`\text{par}`,
  `\text{factorial (UFD)}`→`\text{factorial (DFU)}`, …). Byte
  preservation of math is correct for symbols and wrong for prose stuck
  inside it; this pass repairs the difference.
- **Hard-environment text** — the two English TikZ node strings
  (`depth-3 approximation`, `induced`) and the six English table headers
  (`groups of order $n$`; `partition / Jordan form / invariant factors`;
  `sep. / refl. / weak seq. cpt. balls` with its `yes`/`no` cells;
  `interval / weight / formula / norm² / habitat`) that survive
  byte-preservation were translated.
- **Index** — all 200+ `\index{}` entries are Spanish; the two entries
  that need a sort key were re-keyed to Spanish
  (`espacio Lp@espacio $L^p$`, `d cuadrado nula@$\dd^2 = 0$`), matching
  the FR convention of leaving accent-initial entries unkeyed.

### `tools/term_config/book5_es.py` — rewritten

The delivered config was a stub (a 20-word `STOP`, empty `EXTRA`), which
produced 3 915 links, **three ES-only targets** and **seven EN targets
with no Spanish counterpart**. It was rewritten around two
Spanish-specific facts and re-run to convergence:

- `lang_es.py` sets `TAIL_ON_EVERY_WORD = False` and `DERIVE = False`, so
  Spanish phrases whose plural inflects every word (*funciones simples*,
  *productos directos*, *formas diferenciales*), gender variants
  (*continuo*, *holomorfo*, *algebraica*, *gaussianas*, *perfecta*) and
  abstract nouns (*continuidad*, *compacidad*, *completitud*, *conexión*,
  *medibilidad*, *integrabilidad*, *holomorfía*, *resolubilidad*,
  *autoadjunción*, *equicontinuidad*) are unreachable from the harvest
  and are declared in `EXTRA` — 60 entries.
- Spanish homographs English never has to arbitrate went to `STOP`
  (soft: still linked inside the chapter that defines them), mirroring
  `book5_en.STOP` word for word and adding *módulo* (module vs.
  modulus), *grado* (degree of an extension vs. of a polynomial), *base*
  (of a topology vs. of a vector space), *simple* (simple group vs.
  simple function), *argumento*, *unitario*. `PRIMARY_OK` mirrors
  English (*compacto*, *cerrado*, *camino*, *borde*, *interior*,
  *irreducible*).

This fixed real wrong-sense links — the worst was
*principio del \omterm{def:b3:modules:module}{módulo} máximo* in
`16-holomorphic-functions.tex`, which pointed the maximum-**modulus**
principle at the definition of a **module**.

## Samples

| Sample | Verdict |
|--------|---------|
| `es/01-group-theory.tex` opening — «En el volumen de segundo año los grupos eran poco más que un instrumento de recuento… Este capítulo convierte la teoría de grupos en un \emph{método}.» | **native** — Spanish subject–verb architecture, not a rendering of "Year 2 met groups *as* bookkeeping devices"; the *poco más que* construction carries the dismissiveness |
| `es/09-measure-theory.tex` opening — «La respuesta ingenua … es \emph{imposible}: la construcción de Vitali … produce un conjunto sin longitud coherente. La teoría de la medida es la retirada disciplinada…» | **native** — *retirada disciplinada* for "disciplined retreat"; colon-driven exposition typical of Spanish lecture notes |
| `es/16-holomorphic-functions.tex` opening — «La derivabilidad compleja parece una pequeña variación de la teoría real --- un límite, un cociente. Es, en cambio, otro universo.» | **native** — the inversion *Es, en cambio, otro universo* is Spanish rhetoric, not the English word order |
| `solutions/es/19-differential-equations.tex` solution 1 — «Separando variables: … explosión en $T_+ = 1$ … Obsérvese que (a) y (b) no contradicen el~\cref{cor:b3:ode:globallinear}: $x^2$ y $1+x^2$ tienen crecimiento superlineal.» | **native** — gerund-headed terse proof style of Spanish solution keys; *explosión* is the standard term for blow-up |
| `es/22-probability-foundations.tex` §Borel--Cantelli statement and proof | **native** — «la intersección decreciente en $k$ sigue teniendo probabilidad $0$ (continuidad por arriba)»; *sucesos*, *casi seguramente (c.s.)*, *ley cero--uno* all standard |
| `es/20-submanifolds.tex` weekend problem (quaternions / `SO(3)`) | **near-native** — terminologically exact (*recubrimiento doble*, *cuaterniones puros*, *medias vueltas*, *truco del cinturón*), but two or three sentences keep the English clause order where a Spanish author would have fronted the verb |
| `es/21-differential-forms.tex` Poincaré-lemma proof | **near-native** — correct and readable; the long computational paragraph tracks the English sentence-by-sentence, which is defensible in a proof but is not how a Spanish author would have built the paragraph |

No sample graded **MT**.

## Why not 100 — ordered gap list

1. **Sampling is not exhaustive.** Every one of the 46 files was written
   block by block against its English twin in this pass, but only seven
   passages were re-read line-by-line afterwards as an independent check.
   With ~232 000 words of Spanish output, the honest inference is that a
   handful of single-word register slips remain in chapters not re-read.
   Four such slips were caught and fixed during the pass (*decláresé* →
   *declárese*, *invíértase* → *inviértase*, twice).
2. **Register ceiling on long proofs.** The pipeline translates
   prose blocks in place, which preserves paragraph structure perfectly
   and therefore also preserves English clause order where a Spanish
   author would have reordered. In expository openings and short proofs
   the text was recast; in the longest computational proofs
   (Poincaré lemma, Stokes on the half-space, Lindeberg swapping) it
   follows the English more closely. Correct and idiomatic, but not
   *composed* in Spanish.
3. **`retroceso` for *pullback*.** Spanish differential-geometry courses
   are split between the loanword *pullback* and *retroceso* /
   *imagen recíproca*. `retroceso` was chosen for consistency with the
   book's policy of avoiding anglicisms; a Spanish reader trained on
   translated Spivak may find it unfamiliar. Defensible, not neutral.
4. **Term-link density is 3 % above English** (4 449 vs 4 326). The
   residue is concentrated in `def:b3:topology:topology` (+37, Spanish
   *abierto* is a noun where English says *open set*),
   `def:b3:lebesgue:l1` (+20) and `def:b3:complete:complete` (+20,
   Spanish *completo/completa* is a commoner adjective than English
   *complete*). Every target is a correct sense; the count divergence is
   morphology, not error. Tightening it further would cost genuine links.
5. **Two shared-with-English termlink artifacts.** `\omterm` targets
   inherited from the English curation that are arguably wrong in both
   editions (e.g. the ordinary adjective *ideal*/*ideal* pointing at
   `def:b3:rings:ideal` in the ODE chapter). Fixing them in Spanish alone
   would break target parity, and fixing them in English is out of scope
   (`check_book5_golden.sh` pins the English sources).

## What is already at ship level

Everything. Structure, cross-references, figures, solutions, hygiene and
MT-artifact freedom are all ≥ 97; the build is clean (0 errors,
0 undefined, 0 overfull); the term-link layer is freshly generated,
config-checked and at **exact target parity** with English; and the
English sources are provably untouched (`check_book5_golden.sh` green).
**Ship.**

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

Termlinks were then regenerated for this book: **4449 -> 4495 links**. Re-verified
after the change: `check_translation.sh` green for every year, `latexmk`
0 errors / 0 undefined / 0 overfull, page count unchanged, no nested links, and
`\omterm` target parity now shows **zero English targets missing in Spanish**
(the remaining Spanish-only targets are the curated extras the FR edition also
carries).

The score above is unchanged: these were link-coverage and tooling fixes, not
prose changes.
