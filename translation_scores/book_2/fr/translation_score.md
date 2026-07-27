# Translation score — Math Book 2 · French (`fr`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 2 (High School, grades 10–12) |
| **Language** | French (`fr`) |
| **Quality bar** | **native academic** (EN is the source of truth; this *is* the FR edition, so no French twin exists as a sense reference — English is the only comparand) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **MET** |
| **Date** | 2026-07-27 |
| **Scope of this pass** | **Targeted repair.** The 2026-07-27 grading pass found exactly one defect: all 35 weekend problems and their 35 solutions were missing. This pass translated them and nothing else was rewritten — the existing 35 chapters of course text and 343 exercise solutions were already at or above the bar and were left alone. |

## Verdict in one line

The single blocking gap is closed: **35 weekend problems and 35 matching
solutions now exist in French**, the three structural gates are green, the
PDF is clean, and the prose that was already the best in the series is
unchanged.

## What this pass added

| Item | Before | After |
|------|-------:|------:|
| `\begin{problem}` blocks in `parts/grade-1{0,1,2}/fr/` | 0 | **35** (EN: 35) |
| `\begin{solution}{pb:…}` in `parts/grade-1{0,1,2}/solutions/fr/` | 0 | **35** (EN: 35) |
| `pb:` labels, byte-identical to English | 0 | **35** |
| `\textbf{Partie N --- …}` part headers | 0 | **140** (EN `\textbf{Part N}`: 140) |
| `enumerate[resume]` occurrences (whole tree) | 105 | **105** (EN: 105) |
| PDF pages | 242 | **343** (EN 330, NL 342, ES 341, PT 336) |
| `\omterm` links (book 2, fr) | 2 441 | **4 024** |
| `\omterm` targets of kind `pb:` | 0 | **64** |

One pre-existing overfull box (in `parts/grade-12/fr/15-sums-lln.tex`, the
proof of linearity of expectation) was also fixed by moving the regrouping
formula into a display; it was not introduced by this pass.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **98** | 35 chapters, 343 exercises, 35 weekend problems and 378 solutions now mirror English exactly. `check_translation.sh` PASSES for grade-10, grade-11 and grade-12. Per chapter, the ordered list of `exo:`/`pb:` labels in the body equals the ordered list of `\begin{solution}{…}` keys. Zero duplicate labels. The four-part structure (`Partie I–IV`) and the ~20-question count of every problem are preserved one-for-one |
| Terminology | **97** | The new problem set stays inside the vocabulary the book already established: *taux de variation moyen*, *coefficient directeur*, *sécante*, *primitive*, *valeur moyenne*, *forme canonique*, *tableau de signes*, *point fixe*, *foyer*/*directrice*, *orthocentre*, *loi binomiale*, *espérance*, *inégalité de Bienaymé–Tchebychev*, *loi des grands nombres*, *théorème des valeurs intermédiaires*, *loi de la réfraction*, *moyenne arithmético-géométrique*. No MT sense swaps. `\emph{…}\index{…}` term introductions inside problems were carried over natively (*point fixe*, *foyer*, *directrice*, *orthocentre*, *cote z*) |
| Register / tone | **96** | French infinitive imperative throughout the new stems (*Calculer, Déterminer, Montrer, Démontrer, En déduire, Énoncer, Interpréter, Conclure, Vérifier*), which is what a French exercise sheet says. Story openings are written, not translated: «~Froissez la carte d'un pays et laissez-la tomber n'importe où sur le sol de ce pays~»; «~Une matrice est une machine qui avale un état et renvoie le suivant~»; «~Les rationnels ressemblent à une foule (toutes les fractions~!)~». Full French typographic spacing (`~:`, `~;`, `~?`, `«~…~»`) matches the surrounding chapters |
| LaTeX hygiene | **99** | 0 fatal errors, 0 undefined references, **0 overfull boxes**, 117 underfull (EN itself has 120 — series norm, not a defect). UTF-8 accents only: **0** TeX accent escapes anywhere in the FR tree (English source has `Ren\'e`, `Vi\`ete`, `Bienaym\'e`, `\"Otzi` — all rendered as *René*, *Viète*, *Bienaymé*, *Ötzi*). `\admitted` macro count 3 = EN 3. Decimal point kept in math |
| Cross-refs / rule compliance | **98** | Every `\label{pb:g1{0,1,2}:<slug>:1}` and every `\begin{solution}{pb:…}` is byte-identical to English; `diff` of the sorted `pb:` label sets is empty for all three years. All 35 problems reuse the English `\cref` targets unchanged, including the long cross-problem chain (`pb:g10:algebra:1` → `pb:g10:coordgeom:1` → `pb:g11:quad:1` → `pb:g11:deriv:1` → `pb:g12:seq:1` → …). **0 curriculum or country names** in visible text: EN's "grade 8", "grade 11", "grade 12", "the Middle School volume", "a map of France", "the French Academy" all became neutral French («~le volume précédent~», «~l'an prochain~», «~la carte d'un pays~», «~l'Académie des sciences, en 1791~») |
| Figures | **97** | The weekend problems carry no TikZ of their own (English has none there either); the 100+ figures in the existing chapters are untouched, drawing code byte-identical, only node text and `{\small …}` captions in French |
| Solutions | **96** | All 378 solutions present: 343 exercise solutions (unchanged) plus 35 new weekend-problem solutions, each with the `\textbf{1.}` … `\textbf{20.}` numbering of the English twin and the same numerical answers, checked value by value (Heron's $\frac{577}{408}$, the $56{:}8$ pistole split, $\cos 72^\circ = \frac{\sqrt5-1}{4}$, $M(1,2) \approx 1.456791$, the $27\sigma$ casino, the $1.9\,\%$ Bayes verdict, …) |
| MT-artifact freedom | **98** | **0 residual English** in the new prose (the only English tokens in the FR tree are TikZ/pgfplots keywords such as `ellipse (5.4 and 2.9)` and `fill between[of=line and parab]`). No English word-order calques: EN's participial and nominal constructions were re-cast as French finite clauses («~Trois fois déjà cette série a croisé la recette de Héron~», «~c'est là son vrai talent~», «~les grands intervalles attrapent plus de voyageurs~»). Idioms were localized rather than transposed: *the house always wins* → «~la banque gagne toujours~», *gambler's fallacy* → «~l'illusion du joueur~», *stars and bars* → «~étoiles et barres~», *Collatz/hailstone* → «~la machine à grêlons~», *Snell's law* → «~la loi de la réfraction~» |

**Overall: 96.** Weighting register + terminology + MT-artifact freedom above
structure (structure being already gated by `check_translation.sh`), the
edition ships.

## Structural / build gates

> **Measurement note for the next grading pass.** pdfTeX writes `build/*.log`
> as ISO-8859 text, so plain `grep -c 'Overfull' build/…log` treats the file
> as binary, prints nothing and exits 1 — which a previous pass read as "0".
> **Always use `grep -a`** on these logs. All counts below were taken with
> `grep -a`.

| Gate | Command | Result |
|------|---------|--------|
| Structure, grade-10 | `bash tools/check_translation.sh grade-10 fr` | **PASSED** |
| Structure, grade-11 | `bash tools/check_translation.sh grade-11 fr` | **PASSED** |
| Structure, grade-12 | `bash tools/check_translation.sh grade-12 fr` | **PASSED** |
| Build | `latexmk -pdf one_math_book_2_high_school_fr.tex` | exit 0 |
| Fatal errors | `grep -ac '^!' build/…_fr.log` | **0** |
| Undefined references | `grep -aci 'undefined' build/…_fr.log` | **0** |
| Overfull `\hbox` | `grep -ac 'Overfull' build/…_fr.log` | **0** |
| Underfull `\hbox` | `grep -ac 'Underfull' build/…_fr.log` | 117 (EN: 120 — series norm, context not defect) |
| PDF | `build/one_math_book_2_high_school_fr.pdf` | **343 pp** (was 242; EN 330, NL 342, ES 341, PT 336) |
| Term links | `python3 tools/link_defined_terms.py --book 2 --lang fr --check` | **green** — 4 024 links across 70 files; targets `def 3778, prop 97, pb 64, thm 38, met 31, ex 16` |
| Omterm target parity vs EN | `diff` of sorted target sets | EN ⊂ FR; two extra FR targets (`def:g12:contdist:uniform`, `thm:g12:contdist:memoryless`), both correct-sense links inside their own defining chapter |
| Exercise ↔ solution parity | per-chapter `diff` of label lists | all 35 chapters match |
| Duplicate labels | `grep -rho 'label{…}' \| uniq -d` | none |
| TeX accent escapes | `grep -rnP "\\\\['\`^\"]…"` | **0** |

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| **New**: `grade-10/fr/01-numbers-and-sets.tex`, problem opening + Part IV — «~Les rationnels ressemblent à une foule (toutes les fractions~!) et les irrationnels à des exceptions exotiques~»; «~aucune mesure physique, si précise soit-elle, ne peut décider si une longueur est rationnelle~»; «~la règle de l'ingénieur \emph{est} l'inégalité triangulaire~» | **native** — the `si … soit-il` construction and the concessive word order are French-native, not calqued from *however small* |
| **New**: `grade-12/fr/09-complex-numbers.tex`, problem opening + q10 — «~Euclide savait construire le pentagone régulier, mais la raison \emph{pour laquelle} il cède à la règle et au compas --- alors que l'humble angle de $20^\circ$ y résiste --- est restée cachée deux mille ans~»; «~laisser le nombre d'or signer son œuvre~» | **native** — periodic sentence with a French parenthetical dash clause; *céder à la règle et au compas* is the idiom a French geometry text uses |
| **New**: `grade-12/solutions/fr/07-differential-equations.tex`, q14 (the milk) — «~La vitesse de perte est proportionnelle à l'écart $T - T_a$~: un café brûlant perd sa chaleur le plus vite. […] Pour la tasse la plus chaude~: le lait d'abord. (Les hôtes impatients ont la thermodynamique à l'envers.)~» | **native** — the joke lands in French rather than being transposed word for word |
| **New**: `grade-11/fr/08-descriptive-statistics.tex`, the *cote z* problem — «~Les nombres bruts ne savent pas le dire --- mais divisés par le bon écart type, ils parlent tous une même langue~» | **near-native** — the prose is idiomatic; the coinage *cote z* is defensible French (and is now a properly indexed defined term) but *score z* / *valeur centrée réduite* are equally current, so the choice is a judgement call rather than the single obvious one |
| **Existing, re-checked**: `grade-12/fr/06-integration.tex` proofs and exercise stems | **native** (unchanged by this pass) — «~Chasles et la positivité sont immédiates d'après l'interprétation en aires~»; infinitive imperatives throughout |

## Why not 100 — ordered gap list

1. **`cote z` is a coinage, not the unique standard.** French statistics
   writing also says *score z* or *valeur centrée réduite*. `cote z` was
   chosen because it is short, indexable and links cleanly; a native
   reviewer might prefer another. (It was written without inline math
   precisely so the term-linker can match it — `cote $z$` is invisible to
   the harvest.)
2. **`en moyenne` is auto-linked to the definition of *moyenne*.** The FR
   term config links the bare noun, so the adverbial phrase picks up a link
   a hand-linker would not add. This is **pre-existing** behaviour of
   `tools/term_config/book2_fr.py` (it already occurred in the course
   chapters before this pass) and is harmless, but it is not what a careful
   human would produce. Fixing it means a `EXTRA_PROTECT` entry, i.e. a
   config change, which this pass deliberately did not make.
3. **A few homograph links inherited from the config survive elsewhere in
   the book** — e.g. *milieu* (statistics sense) pointing at
   `prop:g10:coordgeom:midpoint`, *sécantes* (intersecting lines) pointing
   at `def:g11:deriv:rate` in the space-geometry chapter. Three such
   collisions *created by the new text* were removed by rewording
   (`grade-11/fr/07`, `grade-11/solutions/fr/06`,
   `grade-12/solutions/fr/12`, `grade-11/fr/08`); the pre-existing ones in
   the course chapters were left alone, since this was a targeted repair.
4. **Cross-volume references are uniformly «~du volume précédent~».** English
   names "the Middle School volume" and its individual weekend problems
   ("the two-mirrors weekend problem", "the repeating-decimals weekend
   problem"). French renders the volume neutrally to keep the perfect
   rule-7 record, which costs a little of English's pointedness. The
   individual problems are still named by topic, so no reference is lost.
5. **343 pp against EN's 330 (+4 %).** French runs longer than English by
   nature and the figure sits below NL (342 is comparable) and below ES/PT
   density, but two or three of the longest solutions (`grade-12/16`,
   `grade-12/15`) could be tightened by a line or two each.
6. **117 underfull boxes.** Reported for completeness only: English itself
   has 120 and every language edition is in the same range. This is the
   series norm, not a defect of the French edition.

## Note for the other language editions

`translation_instruction.md` designates the French edition as the *sense and
structure reference* for every other language. As of this pass that
reference is **structurally complete for Book 2**: weekend-problem census
for grades 10–12 is now EN 35, **FR 35**, ES 35, NL 35, PT 35, HI 35. An
editor comparing an ES/NL/PT/HI weekend problem against its FR twin will
now find one, with byte-identical labels and the same four-part / ~20-question
skeleton.
