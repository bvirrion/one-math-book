# Translation score — Math Book 3 · French (`fr`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 3 (University Year 1, `bachelor-1`) |
| **Language** | French (`fr`) |
| **Quality bar** | **native academic** (EN is the source of truth; this *is* the FR edition, so no French twin exists as a sense reference — English is the only comparand) |
| **Overall score** | **97 / 100** |
| **Ship threshold** | ≥ 95 — **MET** |
| **Date** | 2026-07-27 |
| **Previous score** | 94 (2026-07-27, blocked solely by 30 hard-rule-7 violations) |
| **Scope of this pass** | Targeted repair: 30 rule-7 rewrites across 16 files, plus a sampled register audit. No re-translation. |

## Verdict in one line

Structurally exact, written in genuinely native French university register,
and now free of national school-system names — the single blocker of the
previous grading has been removed and every gate is green.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror: 25 chapters, 25 solution files, 300 `exo:` labels EN / 300 FR, 25 `pb:` EN / 25 FR, 325 `\begin{solution}{…}` on both sides. `check_translation.sh bachelor-1 fr` **PASSED** |
| Terminology | **97** | Correct French university register throughout: *assertion*, *application* (not *carte*), *corps* (not *champ*), *théorème du rang*, *éléments simples*, *sommes de Riemann*, *développement limité*, *primitive*, *adhérence*, *famille libre*, *théorème de la base incomplète*. No MT sense swaps found in sampling |
| Register / tone | **97** | Reads as a French L1 lecture course. Ch. 24 opening renders "The calculus of …" as «~Le calcul différentiel et intégral des \cref{…}~» — an idiomatic expansion, not a calque. Exercise stems use the French infinitive imperative (Calculer, Déterminer, Montrer, En déduire) |
| LaTeX hygiene | **99** | 0 fatal errors, 0 undefined references, **0 Overfull and 0 Underfull `\hbox`**. **0** TeX accent escapes — UTF-8 throughout. The 3 `%` comment lines in the bodies are French, translated from their English twins (the previous grading's "3 English comments" was a false positive — see below) |
| Cross-refs / rule compliance | **98** | `\label`, `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English. **Rule 7 now clean**: `grep -rn "lycée\|Lycée\|Terminale"` over `parts/bachelor-1/{fr,solutions/fr}` returns **0**. «~volume de Licence~1/2/3~» retained deliberately: *licence* is the generic French word for a bachelor's degree, parallel to Dutch *bachelorjaar* and Spanish *Grado* |
| Figures | **97** | TikZ/pgfplots drawing code byte-identical; only node text and captions localized |
| Solutions | **97** | All 325 solutions present, native and complete; headers `\section*{Chapitre \ref{ch:…} --- <titre>}` with `ch:…` slugs unchanged |
| MT-artifact freedom | **98** | **0 residual English** in prose: an English-function-word sweep over all 50 files returns 7 hits, all of them `\label{met:b1:counting:which}` and TikZ `controls … and …` / `circle (0.045 and 0.19)` syntax. No English word-order calques found in sampling |

**Overall: 97** (weighted register 0.20, terminology 0.20, MT-freedom 0.18,
cross-refs/rule compliance 0.12, LaTeX hygiene 0.10, solutions 0.08,
figures 0.06, structure 0.06 → 97.6).

## Structural / build gates

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-1 fr` | **PASSED** |
| `python3 tools/link_defined_terms.py --book 3 --lang fr --check` | **green** — 126 terms harvested, 256 linkable, **4 511 links across 50 files**, "every file matches what the config generates" (identical to the pre-repair baseline: no visible term text changed) |
| `latexmk -pdf one_math_book_3_university_year_1_fr.tex` | exit 0 |
| Fatal errors (`^!`) | **0** |
| Undefined references | **0** |
| Overfull / Underfull `\hbox` | **0 / 0** |
| PDF | `build/one_math_book_3_university_year_1_fr.pdf`, **416 pp** (EN 395) — normal French expansion (+5.3 %), no MT padding |
| Rule 7 (`lycée`/`Terminale`) | **0 occurrences** (was 30) |
| TeX accent escapes | **0** |
| Exercise / problem / solution census vs EN | 300/300, 25/25, 325/325 |

## The rule-7 repair (30 occurrences, 16 files)

English contains **zero** occurrences of *lycée* or *Terminale*; it says
"the High School volume", "at High School level", "inherited from secondary
school". Each French hit was rewritten against its English twin sentence,
varying the formula to fit the sentence rather than substituting one string:

| File | Old | New |
|------|-----|-----|
| `fr/04-standard-functions.tex` | la collection héritée du **lycée** | … du **secondaire** |
| | utilisées librement **au niveau du lycée** | … **dès le secondaire** |
| | Les rappels relèvent du **lycée** | … du **secondaire** |
| | démontré dans le **volume de Terminale** | … le **volume du secondaire** |
| | utilisé **au niveau du lycée** | utilisé **dès le secondaire** |
| | à crédit sur le **lycée** | à crédit sur le **secondaire** |
| | familière depuis le **lycée** | … depuis le **secondaire** |
| `fr/11-sequences.tex` | le **volume de Terminale (lycée)** | le **volume du secondaire** |
| | du **volume de Terminale** | du **volume du secondaire** |
| | Deux faits du **volume de Terminale** | … du **volume du secondaire** |
| `fr/09-rational-fractions.tex` | utilisé ici **au niveau du lycée** | … **au niveau du secondaire** |
| | trigonométrie du **lycée** | trigonométrie du **secondaire** |
| | utilisées **au niveau du lycée** | **admises telles quelles ici** |
| `fr/03-complex-numbers.tex` | le **volume de Terminale (lycée)** | le **volume du secondaire** |
| `fr/08-polynomials.tex` | utilisée ici **au niveau du lycée** | … **au niveau du secondaire** |
| | utilisé **au niveau du lycée**, démontré | **admis ici**, démontré |
| `fr/01-logic-sets-maps.tex` | comme on l'a vu **au lycée** | comme cela est **familier depuis le secondaire** |
| `fr/02-counting.tex` | utilisé ici **au niveau du lycée** | … **au niveau du secondaire** |
| `fr/05-differential-equations.tex` | le **volume de Terminale** | le **volume du secondaire** |
| `fr/06-integer-arithmetic.tex` | le **volume de Terminale (lycée)** | le **volume du secondaire** |
| `fr/07-algebraic-structures.tex` | l'algèbre du **lycée** | l'algèbre du **secondaire** |
| `fr/13-limits-continuity.tex` | utilisés **au lycée** sur la foi du dessin | utilisés **dans le secondaire** … |
| `fr/14-differentiation.tex` | le **volume de Terminale** | le **volume du secondaire** |
| `fr/15-integration.tex` | du **volume de Terminale** | du **volume du secondaire** |
| `fr/21-matrices.tex` | le **volume de Terminale** | le **volume du secondaire** |
| `solutions/fr/04-standard-functions.tex` | utilisé **au niveau du lycée** | **admis à ce stade** |
| `solutions/fr/09-rational-fractions.tex` | familier depuis le **lycée** | … depuis le **secondaire** |

*secondaire* is the generic French word for secondary education, exactly
parallel to the English source's "secondary school" / "High School"; it
names no national curriculum, class or institution.

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| `fr/12-topology-of-r.tex` opening | **native** — «~Les limites renvoient sans cesse au même vocabulaire géométrique~: des points «~proches~» d'un ensemble, des ensembles «~sans fuite par la frontière~»~»; «~relèvent de la deuxième année~» for "are second-year material" |
| `fr/19-finite-dimension.tex` opening + `def:b1:findim:def` | **native** — «~un même moteur combinatoire, le lemme d'échange~: une famille libre ne peut jamais être plus nombreuse qu'une famille génératrice~»; «~$E$ est \emph{de dimension finie} lorsqu'il…~» is the standard French definitional stem |
| `fr/22-determinants-systems.tex` theorem stems (`thm:b1:det:def`, `thm:b1:det:cofactor`) | **native** — «~Il existe exactement une application $\det\colon\dots$, vue comme fonction des $n$ colonnes, qui soit~:~» (subjunctive after the uniqueness existential — a native construction MT does not produce); «~le déterminant de $A$ privée de sa ligne $i$~» |
| `fr/24-plane-curves.tex` opening | **native** — «~la plupart des courbes de la géométrie et de la mécanique … refusent cette forme et se présentent plutôt comme des courbes \emph{paramétrées}~» |
| `solutions/fr/17-numerical-series.tex` header + solution 1 | **native** — «~télescopage, $S_N = 1 - \frac{1}{N+1} \to 1$. Convergente, de somme $1$.~» — standard French solution shorthand, with correct feminine agreement on *convergente* (série) |
| `fr/03-complex-numbers.tex` opening (repaired) | **native** — «~Les nombres complexes ont été rencontrés dans le volume du secondaire comme un outil de calcul pour les équations du second degré.~» |
| `fr/04-standard-functions.tex` opening (repaired) | **native** — «~À la collection héritée du secondaire --- puissances, exponentielle, logarithme, fonctions trigonométriques --- ce chapitre ajoute leurs fonctions réciproques…~» |

## Register audit performed in this pass

Deliberate sampling of chapter openings and definition/theorem stems against
the English twins, in chapters **12, 19, 22, 24** (untouched by the repair)
plus **01, 02, 03, 04, 05, 06, 07, 08, 09, 11, 13, 14, 15, 21** and
solutions **04, 09, 17** (read while repairing). **No genuine calque was
found**, so no prose was rewritten beyond the 30 rule-7 sentences — per
`translation_instruction.md` §6, a change that does not clearly improve the
French is a regression.

## Correction to the previous grading

The previous score listed "3 English LaTeX comment lines" as a cosmetic
defect. Verified false: the three `%` lines in the FR bodies
(`fr/11-sequences.tex:249,524`, `fr/25-two-variable-functions.tex:338`) are
already French translations of their English twins
(`% a_n increasing (omDef)…` → `% a_n croissante (omDef)…`;
`% cobweb: u0=2…` → `% escalier : u0=2…`;
`% level curves of f…` → `% lignes de niveau de f…`). No fix was needed.
LaTeX hygiene is therefore raised 98 → 99.

## Why not 100 — ordered gap list

1. **The neutral reference is slightly more colorless than the English.**
   English "the High School volume" carries a concrete image; «~le volume du
   secondaire~» is correct, neutral and rule-compliant but marginally
   flatter. Unavoidable under hard rule 7 — no French formula names a
   pre-university level as vividly without naming an institution.
2. **Register audit is sampled, not exhaustive.** 18 of 25 chapters (and 3
   of 25 solution files) were read against their English twins in this pass.
   A residual calque in an unsampled chapter cannot be excluded, though none
   was found in a fairly aggressive sample.
3. **Term-link curation diverges from English by design.** `book3_fr.py`
   links 37 targets `book3_en.py` does not (and 2 the other way). All 37 are
   real labels present in the English source; this is a curation choice, not
   a defect, but it means the two editions are not link-for-link identical.
4. **French expansion.** 416 pp vs 395 EN (+5.3 %). Within the normal band
   for FR (NL 411, ES 411, PT 406) and not attributable to MT padding —
   spot-checked paragraphs match the English sentence-for-sentence — but the
   edition is not as tight as the English.

## What is at ship level

Every dimension is ≥ 97. Structure, terminology, register, hygiene,
cross-references, figures, solutions and MT-artifact freedom all pass; every
gate is green; the rule-7 blocker is gone. **Ship.**
