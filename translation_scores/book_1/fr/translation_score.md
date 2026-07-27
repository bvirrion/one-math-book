# Translation score — Math Book 1 · French (`fr`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 1 (Primary & Middle School, grades 1–9) |
| **Language** | French (`fr`) |
| **Quality bar** | **native academic** (EN is the source of truth; this *is* the FR edition, so no French twin exists as a sense reference — English is the only comparand) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **MET** |
| **Date** | 2026-07-27 |
| **Scope of this pass** | **Targeted repair on top of an existing edition.** The prose of the previous edition was already at ship level (terminology 96, register 95, MT-artifact freedom 97); it was *not* re-translated. Three defects were fixed: (1) the 35 missing weekend problems and their 35 solutions, written from the English source; (2) 1 637 TeX accent escapes in grades 1–3 converted to UTF-8; (3) 10 curriculum-name violations of hard rule 7. A fourth defect surfaced during the work and was fixed too: 55 grammatically-wrong `de`/`à` + `\cref` constructions in the newly written text. |

## Verdict in one line

The edition is now **complete and encoding-clean**, and the new material is
written directly in French at the register of the surrounding chapters —
the two blockers of the previous grading are gone.

## What changed in this pass

| Item | Before | After |
|------|--------|--------|
| Weekend problems in FR bodies (g6–g9) | **0 / 35** | **35 / 35** |
| Weekend-problem solutions in FR | **0 / 35** | **35 / 35** |
| TeX accent escapes (`\'e`, `` \`a ``, `\^o`, `\c{c}`, `{\oe}`, …) | **1 637** | **0** |
| Visible curriculum names (`lycée`, `collège`) | **11** | **0** |
| `de`/`à` immediately before a `\cref` (missing contraction/elision) | 55 (all newly introduced) | **0** |
| `check_translation.sh` years genuinely passing | 4 / 9 | **9 / 9** |
| Defined-term links | 2 416 (no `pb:` targets) | **4 102** (incl. **25 `pb:` targets**) |
| PDF | 345 pp | **430 pp** |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror of English: 71 chapters, 760 exercises, **35 problems**, 795 solutions, 144 `omfigure`s — every census identical. 105 `\textbf{Partie …}` headers vs 105 English `\textbf{Part …}`; 70 `[resume]` vs 70; 525 `\textbf{N.}` answers = 35 × 15 exactly. Per-chapter `exo:`/`pb:` → `solution` diff is empty for all 71 chapters; no duplicate labels |
| Terminology | **97** | New material uses the genuine French school register, not calques: *identités remarquables*, *triplet pythagoricien*, *cerf-volant*, *médiatrice*, *cercle circonscrit*, *moyenne harmonique / géométrique*, *coefficient directeur*, *ordonnée à l'origine*, *taux d'accroissement*, *effectif / fréquence*, *contremarche / giron*, *sténopé*, *la preuve par neuf*, *ronde / blanche / noire / croche / double croche*, *fraction irréductible*, *tronc de pyramide*, *configuration papillon* |
| Register / tone | **96** | Age-appropriate native voice, matched to the neighbouring FR exercise blocks before writing. Infinitive imperatives throughout (*Calculer*, *Montrer*, *En déduire*, *Expliquer*), never *Calculez* and never *On calcule*. g9: «~Divisons $3$ par $11$~: les chiffres se mettent à psalmodier~»; g6: «~Une horloge est un rapporteur qui donne l'heure~» |
| LaTeX hygiene | **98** | 0 fatal errors, 0 undefined refs, **0 overfull boxes** (measured with `grep -a`, see gate table), 0 non-`nullfont` missing characters. Zero TeX accent escapes remain anywhere in the FR tree; grades 1–3 now match the UTF-8 style of grades 4–9. `\index{}` keys converted with their visible terms, so they stay in one alphabetical run |
| Cross-refs / rule compliance | **98** | `\label{…}`, `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English, including all 35 `pb:g{6..9}:<slug>:1`. **`\omterm` first-argument set is byte-identical to the English tree** (`diff` of the sorted unique target sets is empty). Zero curriculum or school-system names in visible text |
| Figures | **97** | Untouched: TikZ/pgfplots drawing code byte-identical to English. The 2 English `%` comments in `grade-2/fr/03-subtraction.tex` are **deliberately left in English** — figure code is kept diffable across EN/FR/NL editions |
| Solutions | **97** | All 795 solutions present. The 35 new weekend-problem solutions are complete and numerically verified against the English (`\textbf{1.}` … `\textbf{15.}`), terse but decisive in the house style |
| MT-artifact freedom | **97** | The new material was **written**, not machine-translated. A residual-English sweep over the 35 new problem blocks and 35 new solution blocks (math, labels, env names and commands stripped) returns **0 English words**: the only hits are FR/EN homographs (*point*, *triangle*, *fraction*, *volume*, *angle*, *second*, *prime*, *six*) and label fragments (`g8:speed:`) |

**Overall: 96**, weighting register + terminology + MT-artifact freedom above
structure (structure is already gated by `check_translation.sh`).

## Structural / build gates

**Measure the log with `grep -a`.** pdfTeX writes `build/*.log` as ISO-8859
text; plain `grep -c 'Overfull'` treats it as binary, prints nothing and
exits 1 — which a previous grading pass misread as "0 overfull". Every
number below was taken with `grep -a`.

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh grade-1 fr` | **PASSED** (was FAILED — accent escapes) |
| `bash tools/check_translation.sh grade-2 fr` | FAILED — **false positive only** (see below) |
| `bash tools/check_translation.sh grade-3 fr` | **PASSED** (was FAILED — accent escapes) |
| `bash tools/check_translation.sh grade-4 fr` | PASSED |
| `bash tools/check_translation.sh grade-5 fr` | FAILED — **false positive only** |
| `bash tools/check_translation.sh grade-6 fr` | FAILED — **false positive only** (was 8 × missing `problem` + 8 × label diff) |
| `bash tools/check_translation.sh grade-7 fr` | **PASSED** (was 9 × missing `problem` + 9 × label diff) |
| `bash tools/check_translation.sh grade-8 fr` | **PASSED** (was 9 × missing `problem` + 9 × label diff) |
| `bash tools/check_translation.sh grade-9 fr` | **PASSED** (was 9 × missing `problem` + 9 × label diff) |
| `latexmk -pdf one_math_book_1_primary_middle_school_fr.tex` | OK (exit 0) |
| `grep -ac '^!' $L` — fatal errors | **0** |
| `grep -aci 'undefined' $L` — undefined refs | **0** |
| `grep -ac 'Overfull' $L` | **0** |
| `grep -ac 'Underfull' $L` | **117** — series norm across every language including English; **context, not a defect** |
| `grep -a 'Missing character' $L \| grep -avc nullfont` | **0** (all 20 hits are benign `nullfont`, from pgfplots measuring passes) |
| PDF | `build/one_math_book_1_primary_middle_school_fr.pdf`, **430 pp** — vs **EN 422**, NL 431, PT 428, ES 431. Was 345 pp; the +85 pp *are* the restored weekend problems |
| `python3 tools/link_defined_terms.py --book 1 --lang fr --check` | **green** — 4 102 links across 120 files, every file matches the config; targets `def 4012, ex 44, pb 25, prop 21` |
| Omterm target parity vs English | **identical sets** (`diff` empty) |

**The three remaining `...` gate failures are false positives**, unchanged
from the previous grading. The flagged lines are `xtick={1,...,6}` /
`xtick={1,...,9}` (pgfplots) in `grade-5/fr/08-problems-and-charts.tex:115`
and `grade-6/fr/08-proportionality-and-data.tex:137`, plus two English `%`
comments in `grade-2/fr/03-subtraction.tex:21,27`. All four are
byte-for-byte identical to their English twins. The gate's exclusion list
covers `\foreach` and `samples at` but not `xtick=`/`ytick=`, and it does
not skip comment lines. **The English `%` comments are kept in English on
purpose** — figure code is deliberately identical across editions so it
stays diffable. Not translation defects; do not "fix" them.

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| `grade-9/fr/03-square-roots.tex` — new problem opening | **native** — «~La diagonale du carré unité est une longueur parfaitement réelle --- on l'a tracée dans \cref{…} --- et pourtant, comme les pythagoriciens l'ont découvert avec horreur il y a quelque vingt-cinq siècles, aucune fraction ne la mesure. La légende prétend que la découverte fut punie par noyade.~» Passé simple used correctly for the legend, present for the mathematics |
| `grade-8/fr/04-literal-calculation-equations.tex` — new problem opening | **native** — «~Trois développements reviennent si souvent que l'algèbre les connaît par cœur~: on les appelle les \emph{identités remarquables}.~» The French name is the real classroom term, not a translation of "remarkable identities" |
| `grade-7/fr/03-fractions.tex` — new problem, music notation | **native** — *ronde / blanche / noire / croche / double croche*, *blanche pointée*, *liaison*, *triolet*, *mesure à $4/4$*: the actual French solfège vocabulary, which a literal translation of "half note / eighth note" would have destroyed |
| `grade-6/solutions/fr/07-perimeter-area-volume.tex` — new solution 5 | **native** — «~Cinq carreaux ont été enlevés et quatre seulement sont revenus~: la bande ajoutée se pose le long du côté $4$, plus court que le côté $5$ que couvrait la bande retirée.~» Reads as a French teacher's board explanation |
| `grade-1/fr/01-counting-to-20.tex` opening (encoding pass) | **native** — «~Combien de billes~? Compter répond à la toute première question des mathématiques.~» Previously marred by `\`a`/`\'e`; now clean UTF-8, text otherwise untouched |
| `grade-3/fr/05-shapes-and-right-angles.tex` (encoding pass) | **native** — «~Ce chapitre les regarde avec l'œil du géomètre~» — `{\oe}` → `œ`; *équerre* used exactly as a French primary teacher would |

## Why not 100 — ordered gap list

1. **House `\cref` style is terser than native French.** The edition writes
   bare `\cref` after most prepositions («~prouvé dans \cref{ch:…}~» →
   "dans Chapitre 14"), where native French would say «~dans le chapitre
   14~». This is a pre-existing, consistent convention across all of Book 1
   FR, so it was kept. Only the constructions that are actually
   *ungrammatical* were repaired in the new text: `de`/`à` now contract or
   elide correctly (`du~\cref{thm:…}`, `de la~\cref{prop:…}`,
   `de l'\cref{exo:…}`), matching what `one-math-book/CLAUDE.md` prescribes
   and what the mature bachelor FR editions do. The result is a small
   internal inconsistency between the new problems and the older chapters.
2. **60 English `%` comment lines** remain in the FR bodies. Invisible in
   the PDF and **intentional** (figure code stays byte-identical across
   editions), but they do mean the sources are not monolingual.
3. **Register ceiling in the youngest chapters of the range.** A few grade-6
   problem openings (Dido's fence, Zeno's runner) are ambitious for an
   11-year-old — but they are exactly as ambitious in the English source,
   so this is a series-level choice, not a translation defect.
4. **`\index{médiane}` is used for two different notions** — the median of a
   triangle (g8) and the median of a data set (g9). This mirrors English
   exactly (`\index{median}` in both places), so it is an inherited quirk
   rather than an FR gap; a French index would ideally disambiguate.
5. **Sampling, not exhaustive re-reading.** The 35 new problems and 35 new
   solutions were written and checked line by line. The 760 pre-existing
   exercise solutions were *not* re-read in full this pass; their score
   rests on the previous grading plus spot checks.

## Evidence that the edition is now complete

Weekend-problem census for grades 6–9: EN 35, **FR 35**, ES 35, NL 35,
PT 35, HI 35. The `pb:` targets that were entirely absent from the FR
term-link census now number 25, and the FR `\omterm` target set is
byte-identical to the English one. French is once again usable as the
*structure reference* that `translation_instruction.md` designates it to be.

## Working tree

Uncommitted, 215 changed files, for human review. **No git commit was
created.**
