# Translation score — Math Book 4 · French (`fr`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 4 (University Year 2, `bachelor-2`) |
| **Language** | French (`fr`) |
| **Quality bar** | **native academic** (EN is the source of truth; this *is* the FR edition, so no French twin exists as a sense reference — English is the only comparand) |
| **Overall score** | **97 / 100** |
| **Ship threshold** | ≥ 95 — **met; no blockers remain** |
| **Date** | 2026-07-27 |
| **Scope of this pass** | Targeted repair. 6 rule-7 rewrites, 3 `MP*` fixes (English source + FR mirror), 1 pre-existing overfull box fixed. No re-translation. |

## Verdict in one line

The strongest French edition in the math series, now unblocked: the six
*lycée* references are gone, the curriculum name that leaked in from the
English source is fixed **at the source**, and the edition builds with zero
errors, zero undefined references and zero overfull boxes.

## What changed since the 95 score

1. **Rule 7 — all 6 *lycée* occurrences rewritten** (see table below).
   `grep -rn "lycée\|Lycée" parts/bachelor-2/fr parts/bachelor-2/solutions/fr`
   now returns nothing.
2. **`MP*` fixed in English first, then mirrored into French.** This was an
   English-side defect (rule 2: English is canonical), so patching French
   alone would have been wrong. The Dutch edition had already solved all
   three neutrally, and its solutions were adopted into English.
3. **One overfull `\hbox` fixed** — pre-existing, and *missed by the previous
   grading*: the pdfTeX log is ISO-8859-encoded, so a plain `grep -c` treats
   it as binary and prints nothing, which the earlier pass read as "0".
   **Always use `grep -a` on these logs.** Real counts are in the gate table.

### The 6 rule-7 rewrites

| File:line | Before | After |
|-----------|--------|-------|
| `fr/19-surfaces.tex:441` (env title) | «~Le cône, confronté à la formule du lycée~» | «~Le cône, confronté à la formule du **secondaire**~» |
| `fr/19-surfaces.tex:488` | «~la formule du lycée, désormais démontrée~» | «~la formule **apprise au secondaire**, désormais démontrée~» |
| `fr/20-multiple-integrals.tex:631` | «~le un tiers des formules du lycée~» | «~le un tiers des formules **scolaires**~» |
| `fr/21-countable-probability.tex:6` | «~La théorie finie du volume de lycée~» | «~La théorie finie du **volume du secondaire**~» |
| `fr/21-countable-probability.tex:55` | «~le cas fini (volume de lycée)~» | «~le cas fini (**volume du secondaire**)~» |
| `fr/22-discrete-random-variables.tex:36` | «~(volume Lycée~;~» | «~(**volume du secondaire**~;~» |

The wording is not a mechanical substitution: it mirrors English's own
distinction between *the High School volume* (→ «~volume du secondaire~»,
3×) and *the school formula(s)* (→ «~formule du secondaire~» / «~apprise au
secondaire~» / «~formules scolaires~»).

«~volume de Licence~1/2/3~» was **left untouched** — *licence* is the generic
French word for a bachelor's degree, exactly parallel to Dutch *bachelorjaar*
and Spanish *Grado*, and is the correct neutral form.

### The 3 `MP*` fixes (English source + FR mirror)

| File:line | English before → after | French before → after |
|-----------|------------------------|------------------------|
| `14-fourier-series.tex:5` | "the two pillars within **MP\*** reach" → "within **reach at this level**" | «~à portée de la **MP\***~» → «~**accessibles à ce niveau**~» |
| `21-countable-probability.tex:3` | "the probability theory of the modern **MP\*** program" → "**modern probability theory**" | «~du programme moderne de **MP\***~» → «~la **théorie moderne** des probabilités~» |
| `21-countable-probability.tex:580` | "the standard **MP\*** convention" → "the standard **convention at this level**" | «~la convention **MP\*** standard~» → «~la convention **standard à ce niveau**~» |

These were the only 3 curriculum names in visible text anywhere in the
English math sources. The two remaining `MP*` strings in
`parts/bachelor-2/part.tex` are `%` **comments** (provenance), which the
project explicitly permits.

**Outstanding for the user:** `es`, `pt` (and `hi`, when it exists) still
carry `MP*` on the same three lines and now diverge from English. `nl` was
already correct and needs nothing.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror: 23 chapters / 23 solution files both sides; 276 `exo:` + 23 `pb:` labels EN and FR; 299 `\begin{solution}{…}` both sides. `check_translation.sh bachelor-2 fr` **PASSED** |
| Terminology | **97** | Correct French L2 register throughout: *corps* (never *champ*), *bases duales*, *annulateurs*, *formes multilinéaires alternées*, *noyau de Dirichlet*, *identité de Parseval*, *familles sommables*, *théorème de projection*, *pgcd*. No MT sense swaps found in sampling |
| Register / tone | **97** | Reads as a French second-year course, not a translation: «~L'imparité tue les $a_n$~»; «~Ce chapitre lève ces trois restrictions~»; «~soldant chaque admission de première année~»; «~Le « oui » audacieux de Fourier a engendré un siècle d'analyse~» |
| LaTeX hygiene | **99** | 0 fatal errors, 0 undefined references, **0 overfull boxes** (the one pre-existing box is fixed). 0 TeX accent escapes; every file valid UTF-8 |
| Cross-refs / rule compliance | **99** | `\label`, `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English. **Rule 7 clean.** No curriculum names in visible text in either language |
| Figures | **97** | TikZ/pgfplots drawing code byte-identical to English; only node text and captions localized |
| Solutions | **97** | All 299 solutions present, native and complete; localized `\section*{Chapitre \ref{ch:…} --- <titre>}` headers with `ch:…` slugs unchanged |
| MT-artifact freedom | **98** | **0 residual English in prose** (an automated sweep over 46 files returns 7 hits, all TikZ syntax keywords — `every node/.style`, `ellipse (1.5 and 0.95)`). No English word-order calques found |

**Overall: 97** — weighted toward terminology + register + MT-artifact
freedom, since structure is already gated by `check_translation.sh`.

## Structural / build gates (measured 2026-07-27)

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-2 fr` | **PASSED** |
| `latexmk -pdf one_math_book_4_university_year_2_fr.tex` | exit 0 |
| Fatal errors (`grep -ac '^!'`) | **0** |
| Undefined references (`grep -aci undefined`) | **0** |
| Overfull `\hbox` (`grep -ac Overfull`) | **0** |
| FR PDF | `build/one_math_book_4_university_year_2_fr.pdf`, **417 pp** (EN 397) — normal French expansion, no MT padding |
| `python3 tools/link_defined_terms.py --book 4 --lang fr --check` | **green** — 3 512 links across 46 files, every file matches the config |
| `python3 tools/link_defined_terms.py --book 4 --lang en --check` | **green** — 3 511 links across 46 files (re-verified after the English edit) |
| EN rebuild `one_math_book_4_university_year_2.tex` | exit 0 — 0 errors, 0 undefined, 0 overfull, 397 pp |
| Omterm first-arg parity vs English | **identical sets**, both directions |
| Rule-7 grep (`lycée\|Lycée\|MP\*` in FR bodies + solutions) | **no matches** |
| TeX accent escapes / non-UTF-8 files | 0 / 0 |

**Not gated, for the record:** 121 underfull `\hbox`/`\vbox` warnings (loose
lines from `\emergencystretch` with no French hyphenation patterns loaded).
This is the series norm, not a defect of this edition — EN Book 4 has 104,
FR Book 3 has 118, FR Book 5 has 137. The previous score's "0 / 0" for these
was the `grep`-on-ISO-8859 artifact described above.

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| `fr/14-fourier-series.tex` opening (edited this pass) | **native** — «~Ce chapitre démontre les deux piliers accessibles à ce niveau~: le \emph{théorème de Dirichlet}…~»; the new neutral phrase is idiomatic and carries the level without naming a track |
| `solutions/fr/14-fourier-series.tex`, solution to `exo:b2:fourier:1` | **native** — «~L'imparité tue les $a_n$~» is a French lecturer's ellipsis, not a rendering of an English sentence; «~Dirichlet en $t = \frac\pi2$ (un point de continuité, valeur~$1$)~» |
| `fr/19-surfaces.tex` exercise stems | **native** — «~Montrer que les plans tangents… passent tous par le sommet~»; «~Paramétrer le tore obtenu en faisant tourner le cercle…~». Correct French imperative-infinitive exercise register |
| `fr/21-countable-probability.tex` opening (edited this pass) | **native** — «~La théorie finie du volume du secondaire acquiert toute son infrastructure~: la $\sigma$-additivité remplace l'additivité finie~». Fluent *and* now rule-7 compliant |
| `fr/02-linear-algebra.tex` standing conventions | **native** — «~$K$ est un corps ($\Q$, $\R$, $\C$, ou $\Z/p\Z$ --- la théorie ne s'en soucie pas)~»; «~se transposent mot pour mot~» |

No sample in this pass scored **MT**.

## Why not 100 — ordered gap list

1. **Coverage of the register judgement is sampling-based, not exhaustive.**
   Terminology and register are graded from openings, definitions, proofs,
   exercise stems and solution headers across ~10 of 23 chapters. A native L2
   lecturer reading all 417 pages would very likely find a handful of
   sentences to tighten. This is the single largest reason the score is 97
   and not higher.
2. **«~volume du secondaire~» is a coined neutral formula.** It is correct,
   compliant and readable, but a French textbook writing natively would more
   often say «~le volume précédent de la série~» or simply drop the
   back-reference. Faithfulness to the English cross-reference was preferred
   over maximal idiom.
3. **One typographic accommodation diverges from the English layout.**
   `fr/20-multiple-integrals.tex:557` now carries `\leavevmode\par\noindent`
   so the long French theorem head («~Exemple 20.27 (Coordonnées cylindriques
   et sphériques).~») no longer shares its line with the coordinate formula.
   This removes the overfull box and keeps the translated prose verbatim, at
   the cost of one extra line break relative to English. The `\leavevmode`
   idiom is already used elsewhere in this tree.
4. **16 English `%` comment lines remain in the FR bodies** (TikZ
   construction notes in `16-differential-equations`, `18-curves`,
   `19-surfaces`, `23-generating-functions`). **Deliberately left in
   English**: they are byte-identical to the English source, and the `nl`,
   `es` and `pt` editions keep them in English too, so the drawing code stays
   diffable across all five editions. Invisible in the PDF.
5. **Series-level inconsistency pending.** `es` and `pt` Book 4 still say
   `MP*` on the three lines fixed here and now diverge from canonical
   English. Outside this edition's scope; flagged for scheduling.
6. **121 underfull boxes.** Cosmetic loose lines; the series norm (see gate
   table). Would need French hyphenation patterns to improve.

## What is at ship level

Everything. Structure, terminology, register, LaTeX hygiene, cross-references,
rule compliance, figures, solutions and MT-artifact freedom are all ≥ 97; the
term-link layer is fresh and green in both languages; the omterm target set
matches English exactly; and the build is clean on all three gated counts.
**No blockers remain — this edition ships.**
