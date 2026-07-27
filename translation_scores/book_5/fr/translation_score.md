# Translation score — Math Book 5 · French (`fr`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 5 (University Year 3, `bachelor-3`) |
| **Language** | French (`fr`) |
| **Quality bar** | **native academic** (EN is the source of truth; this *is* the FR edition, so no French twin exists as a sense reference — English is the only comparand. FR Books 3 and 4 were used as the intra-series reference for cross-volume phrasing) |
| **Overall score** | **97 / 100** |
| **Ship threshold** | ≥ 95 — **met, and no longer blocked**: the 9 rule-7 violations are repaired |
| **Date** | 2026-07-27 |
| **Scope of this pass** | Targeted repair, not a re-translation. 8 files touched, 31 lines changed. |

## Verdict in one line

Structurally exact, clean build, and the most demanding register in the
series handled convincingly; the nine French degree-year shorthands
(«~le volume de L2~») that blocked shipping are gone, the one calqued
opening clause is rewritten, and three genuine defects found by sampling
are fixed.

## Dimension scores

| Dimension | Score /100 | Δ | Notes |
|-----------|----------:|:--:|--------|
| Structural fidelity | **99** | = | Exact mirror: 23 chapters, 23 solution files, 299 `exo:`/`pb:` labels EN / 299 FR, 299 `\begin{solution}{…}` on both sides. Weekend problems present. `check_translation.sh bachelor-3 fr` **PASSED** |
| Terminology | **97** | = | Correct French L3 register across algebra, topology, measure and complex analysis: *sous-groupe normal* / *$N \trianglelefteq G$*, *équation aux classes*, *suites de composition*, *groupes résolubles*, *anneaux euclidiens*, *dénombrablement additive*, *mesure extérieure*, *$\C$-différentiabilité*, *composante connexe*, *règle de la chaîne*. No MT sense swaps (*corps* not *champ*, *application* not *carte*) |
| Register / tone | **98** | +1 | Reads as a French third-year lecture course. The one remaining calqued opening («~Le volume de L2 a rencontré les groupes comme dispositifs de comptabilité~») is rewritten with a French subject–verb architecture; two lexical MT artifacts found by sampling (*indélicates* for "delicate", *creveront* for "will crack") are corrected |
| LaTeX hygiene | **98** | = | 0 fatal errors, 0 undefined references, 0 overfull boxes. **0** TeX accent escapes. The 8 English `%` comment lines are TikZ construction notes **byte-identical to the English (and Dutch) figure code** — deliberately left as-is (see below) |
| Cross-refs / rule compliance | **99** | +7 | `\label`, `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English. **0 rule-7 violations** (was 9). *Zero* occurrences of *lycée*, *Terminale* or *collège*. Cross-volume references now use one consistent, curriculum-neutral formula throughout the book |
| Figures | **97** | = | TikZ/pgfplots drawing code byte-identical; only node text and captions localized. `\texorpdfstring{$L^1$}{L1}` / `{$L^2$}{L2}` in `14-fourier-transform.tex` (the Lebesgue spaces) untouched — that file has a zero-byte diff |
| Solutions | **97** | = | All 299 solutions present, native and complete; localized `\section*{Chapitre \ref{ch:…} --- <titre>}` headers with `ch:…` slugs unchanged |
| MT-artifact freedom | **98** | = | **0 residual English** after stripping labels, environment names and math. No systematic calquing; the residual items are single-clause, listed below |

**Overall: 97** (weighted toward terminology + register + MT-freedom;
structure is already gated by `check_translation.sh`).

## Structural / build gates (run 2026-07-27, after the repair)

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-3 fr` | **PASSED** |
| `latexmk -pdf one_math_book_5_university_year_3_fr.tex` | exit 0 |
| Fatal errors (`^!`) | **0** |
| Undefined references | **0** |
| Overfull `\hbox` | **0** |
| Underfull (`\vbox` from `\output` + 1 `\hbox`) | 137 — English twin has 136; page-breaking noise, not a defect |
| `Missing character … nullfont` | 10 — **identical count in all six language builds** including English; a preamble length artifact, not FR-specific |
| PDF | `build/one_math_book_5_university_year_3_fr.pdf`, **404 pp** (EN 395, NL 417, ES 409, PT 405) — unchanged from baseline, still the tightest expansion ratio of the FR editions |
| `python3 tools/link_defined_terms.py --book 5 --lang fr --check` | **green** — 4 251 links across 46 files, every file matches the config |
| Omterm target parity vs English | **exact** — `diff` of the sorted unique `\omterm{target}` sets is empty in both directions (the 2 FR-only targets reported in the previous score were stale and disappeared on regeneration) |
| Exercise ↔ solution parity | 299 / 299 both sides |

## What changed in this pass

### 1. Rule 7 — nine «~volume de L2~» removed

The books never name a national curriculum. English writes "the Year 2
volume"; Dutch writes "het volume van bachelorjaar 2". The formula was
varied to fit each sentence rather than substituted mechanically, and
aligned on «~(volume de) deuxième année~», which this book already used
in `06-general-topology.tex` and `18-conformal-geometry.tex`.

| File:line | Before | After |
|---|---|---|
| `fr/01-group-theory.tex:3` | Le volume de L2 a rencontré les groupes comme dispositifs de comptabilité | Les groupes n'étaient, dans le volume de deuxième année, que des outils de comptabilité |
| `fr/01-group-theory.tex:21` | On rappelle du volume de L2~: | On rappelle du volume de deuxième année~: |
| `fr/02-rings-arithmetic.tex:20` | les idéaux de $\Z$ et $K[X]$ du volume de L2 | les idéaux de $\Z$ et $K[X]$ étudiés en deuxième année |
| `fr/02-rings-arithmetic.tex:170` | le théorème des restes chinois du volume de L2 | le théorème des restes chinois vu en deuxième année |
| `fr/02-rings-arithmetic.tex:245` | le volume de L2 a démontré les deux divisions | les deux divisions ont été établies en deuxième année |
| `fr/02-rings-arithmetic.tex:396` | le volume de L2 a fait cette construction pour $\Q$ | cette construction a été menée en deuxième année pour $\Q$ |
| `fr/03-modules-pid.tex:10` | que le volume de L2 obtenait | que la deuxième année obtenait |
| `fr/03-modules-pid.tex:524` | du théorème de Jordan du volume de L2 | du théorème de Jordan données en deuxième année |
| `solutions/fr/05-representations.tex:26` | le chapitre des fonctions génératrices du volume de L2 | le chapitre de deuxième année sur les fonctions génératrices |

Not violations, left byte-identical: the `L1`/`L2` inside
`\texorpdfstring{$L^1$}{L1}` / `\texorpdfstring{$L^2$}{L2}` section
titles of `fr/14-fourier-transform.tex` — those are the Lebesgue spaces.

### 2. Cross-volume formula harmonized (internal consistency)

Four further references used two other calqued shapes, both renderings
of the English "Year 2 volume" rather than French usage:

- `fr/21-differential-forms.tex:5, 212, 721` — «~le volume d'Année~2~» → «~le volume de deuxième année~» (3×)
- `solutions/fr/10-lebesgue-integral.tex:73` — «~Bâle du volume de 2e année~» → «~Bâle, vu en deuxième année~»

The book now has exactly one cross-volume formula.

### 3. Register / lexical defects found by sampling

- `fr/03-modules-pid.tex:11` — «~par d'**indélicates** récurrences~» for
  EN "by delicate inductions". *Indélicat* means *tactless / dishonest*;
  the intended sense is *délicat* (fiddly). → «~par de délicates
  récurrences~». A real mistranslation, not a stylistic preference.
- `fr/02-rings-arithmetic.tex:15` — «~qui **creveront** le théorème des
  deux carrés de Fermat~» for "which will crack …". *Crever* is wrong
  register (to puncture / to die). → «~qui feront tomber le théorème~».
- `fr/12-lp-spaces.tex:71–73` — «~$\dots$, **de** la convexité de $t^p$,
  pour voir que le membre de gauche est fini lorsque **le droit** l'est~»:
  two calques in one clause ("from convexity of", "the right"). →
  «~conséquence de la convexité de $t^p$ … lorsque celui de droite l'est~».
- `fr/04-field-extensions-galois.tex:6` — «~reçoivent … **une** réponse
  d'une seule idée~» → «~reçoivent … **leur** réponse d'une seule idée~».

### 4. English `%` comment lines — deliberately kept

The 8 English comment lines (`% p = 1 diamond`, `% separatrix E = 1`,
`% hyperbolas x^2 - y^2 = c`, …) in `fr/08-banach-spaces.tex`,
`fr/18-conformal-geometry.tex` and `fr/19-differential-equations.tex`
are **byte-identical to the English chapters** — verified by `diff` —
and the Dutch edition keeps them identical too. The repo convention is
"figures: only text nodes and captions localized; drawing code
preserved", and these comments are drawing code. Translating them would
create a gratuitous divergence in three figures for zero reader-visible
gain. Decision: **left as-is, consistently across all three files**.

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| `fr/01-group-theory.tex` opening (rewritten) — «~Les groupes n'étaient, dans le volume de deuxième année, que des outils de comptabilité~: théorème de Lagrange, groupes cycliques, groupe symétrique et sa signature.~» | **native** — the `ne … que` construction carries the English "met groups *as* bookkeeping devices" dismissiveness without the English subject–verb architecture; clause list intact |
| `fr/01-group-theory.tex` §quotients + proof of the quotient theorem | **native** — «~L'ensemble $G/N$ des classes, muni de la multiplication $(gN)(hN)=ghN$, est un groupe bien défini~»; «~La bonne définition est tout l'enjeu.~» — idiomatic, not a rendering of "Well-definedness is the whole point" |
| `fr/09-measure-theory.tex` opening | **native** — «~La réponse naïve … est \emph{impossible}~: la construction de Vitali … produit un ensemble sans longueur cohérente. La théorie de la mesure est la retraite disciplinée~» |
| `fr/12-lp-spaces.tex` proof of Minkowski (after repair) | **native** — «~inégalité triangulaire ponctuelle/p.p.~», «~conséquence de la convexité de $t^p$~», «~diviser par $\norm{f+g}_p^{p/q}$ (si non nul~; sinon trivial)~» — the terse imperative-infinitive style of French lecture proofs |
| `fr/23-clt-gaussian.tex` opening | **native** — «~le théorème central limite dit \emph{comment elles fluctuent}~: l'erreur, amplifiée par $\sqrt n$, est asymptotiquement gaussienne~» |
| `fr/06-general-topology.tex` opening | **native** — «~les constructions quotients … ne sont tout simplement pas des objets «~métrique d'abord~»~» |
| `solutions/fr/05-representations.tex` | **native** — «~l'orthogonalité des caractères~» used exactly as in French representation-theory courses |

No sample in this pass graded **MT**.

## Why not 100 — ordered gap list

1. **Sampling is not exhaustive.** Seven openings, two proofs and two
   solution files were read line-by-line against their English twins in
   this pass, on top of the previous grading pass. Four genuine lexical
   defects surfaced from that sample across ~46 files; the honest
   inference is that a handful of comparable single-word artifacts
   remain in chapters not sampled (`15-spectral-theory`,
   `17-residues`, `20-submanifolds`, `22-probability-foundations` were
   not read in full).
2. **Terminology is correct but occasionally minimal.** A few
   English-idiom sentences are rendered accurately and tersely rather
   than being recast the way a French lecturer would build the sentence
   — correct and readable, but the French is following the English
   clause order where a native author would have reordered. This is a
   ceiling effect of a *targeted repair* on an already-good text, not a
   defect worth churning a 97-scoring edition for.
3. **One shared-with-English termlink artifact.**
   `fr/19-differential-equations.tex:813` links the ordinary adjective
   *idéal* ("garde le temps idéal") to `def:b3:rings:ideal`. The English
   source has exactly the same wrong-sense link at
   `19-differential-equations.tex:775`, so this is a `book5_*.py`
   curation issue shared by both editions, **not** a translation defect;
   fixing it in FR alone would break omterm target parity, and fixing it
   in EN is out of this agent's scope (`check_book5_golden.sh`).
4. **8 English TikZ comment lines** remain, by the deliberate decision
   documented above. Costs nothing in the PDF; costs a point of purity.

## What is already at ship level

Everything. Structure, terminology, register, hygiene, figures,
solutions and MT-artifact freedom are all ≥ 97; rule compliance is
clean; the term-link layer is freshly regenerated and green with exact
omterm target parity against English; and the book remains the most
concise of the FR editions relative to its English source (404 pp
vs 395). **Ship.**
