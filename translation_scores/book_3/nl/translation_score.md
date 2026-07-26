# Translation score — Math Book 3 · Dutch (`nl`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 3 (University Year 1, `parts/bachelor-1`) |
| **Language** | Dutch (`nl`) |
| **Quality bar** | **native academic** (EN is the source; FR `parts/bachelor-1/fr/` used as sense/structure reference, never as a ceiling; NL Book 1 `parts/grade-9/nl/02-arithmetic-gcd.tex` as register model at school level, lifted to standard Dutch university mathematics here) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 |
| **Date** | 2026-07-26 |
| **Scope** | Full re-translation **from scratch**: the 25 chapter bodies and the 25 solution files were deleted (`rm -f parts/bachelor-1/nl/[0-9]*.tex parts/bachelor-1/solutions/nl/[0-9]*.tex`) and rewritten from the English — 50 files, 32 442 lines, ~215 000 words, including the 25 weekend problems (25 × 20–25 questions) and their full solutions |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror (25 + 25): identical `\label{}` sets **and order**; `exo:`/`pb:` ↔ `\begin{solution}{}` keys equal; per-environment census equal to English in body and solutions (definition/theorem/proposition/lemma/corollary/example/remark/method/notation/exercise/problem/proof/tikzpicture/omfigure); 107 `enumerate[resume]`, 132 `\textbf{Deel …}` part headers and 5 `\admitted` macros, matching English one for one |
| Terminology | **97** | Standard Dutch university usage, checked against `parts/bachelor-2/nl/`, `parts/bachelor-3/nl/` and `parts/grade-*/nl/` before any new term was coined: lichaam, veelterm, opspansel, vrije familie, voortbrengend, deelruimte, complementaire deelruimten, dimensiestelling, rang, kern/beeld, spoor, getransponeerde, grammatrix, inwendig product, orthonormaal, keerpunt, poolkromme, kegelsnede, booglengte, trapfunctie, Riemannsommen, quotiëntcriterium, alternerende reeks, taylorontwikkeling, geheelwaardige veelterm, torenwet, diëdergroep, glijspiegeling, kleinste kwadraten, normaalvergelijkingen |
| Register / tone | **97** | Written by a Dutch lecturer, not decoded: `Zij $f$ continu op $\intcc ab$.` — **zero** `Laat … zijn` calques in 50 files (the old edition carried 45). Standard connective repertoire throughout: "Merk op dat", "Stel dat", "Neem aan dat", "Bijgevolg", "Omgekeerd", "Er volgt dat", "Uit … volgt", proofs closing on a real Dutch sentence. Exercise stems imperative (Bewijs, Toon aan, Bereken, Bepaal, Ga na, Leid af, Onderzoek, Schets) |
| Hygiene / LaTeX | **99** | 0 errors, 0 undefined references, 0 overfull boxes; UTF-8 accents only (0 hits for the `\'e`/`\"o`/`` \`a ``-class regex, and no `\c{c}`, `\v{}`, `\~{}` either): Cesàro, Apéry, Pólya, Hölder, Schröder, limaçon, astroïde, cardioïde, diëdergroep all written as characters |
| Cross-refs | **98** | `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English; cross-volume references are prose only, with the series' Dutch names: 23× **bovenbouwvolume**, 23× **volume van bachelorjaar 2**, 12× **volume van bachelorjaar 3** — the old edition's "Middelbaar-onderwijsvolume"/"middelbareschoolvolume" wording is gone (0 hits) |
| Figures | **98** | TikZ/pgfplots drawing code byte-identical (coordinates, `\foreach`, `xtick=`/`ytick=`/`samples at`, `\addplot` bodies untouched); only node text and `{\small …}` captions translated — e.g. the mean-value figure ("een of andere raaklijn (gestreept) loopt evenwijdig met de koorde (grijs)"), the alternating-harmonic hop figure, the cycloid arch with `C`/`T` guide chords, the Lissajous figure-eight |
| Solutions | **97** | Every solution rewritten from the English solution; headers `\section*{Hoofdstuk \ref{ch:b1:…} --- <Nederlandse hoofdstuktitel>}` for all 25; the 25 weekend-problem solutions rendered in full, questions 1–25 each |
| MT-artifact freedom | **95** | No polished-MT phrasing survives from the old edition ("Naast haar eigen bekoring" and its family are gone). A residual-English sweep over the 50 files (LaTeX commands and math stripped) returns only Dutch words that happen to look English: *Let op*, TikZ `and` in `.. controls … and …`, and the label `met:b1:counting:which` |

**Overall: 96** (weighted toward terminology, register and MT-freedom).

## Structural / build gates

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-1 nl` | **TRANSLATION GATE: PASSED** |
| `\omterm` target-set parity vs English | **identical sets, 0 divergences** (see below) |
| `python3 tools/link_defined_terms.py --book 3 --lang nl --unwrap --apply` → `--apply` | **3 914** links inserted across 50 files (def 3 260, thm 222, prop 216, pb 144, ex 40, met 16, cor 16) — was 3 459 before the coverage audit |
| `python3 tools/link_defined_terms.py --book 3 --lang nl --check` | every file matches what the config generates |
| `sh tools/check_book5_golden.sh` | unchanged — shared termlink rules untouched |
| `latexmk one_math_book_3_university_year_1_nl.tex` | OK |
| Fatal errors (`^!`) | **0** |
| Undefined references (case-insensitive) | **0** |
| Overfull `\hbox` | **0** |
| PDF | `build/one_math_book_3_university_year_1_nl.pdf`, **411 pp** |

Two overfull boxes appeared on the first build and were fixed by rewording /
re-breaking, not by `\hyphenation` or `\emergencystretch` (neither was added):

- `parts/bachelor-1/nl/04-standard-functions.tex` — the two-tangent display of
  `ex:b1:functions:arctansum` split into two displays with the connective
  "en vervolgens" as running text (6.49 pt).
- `parts/bachelor-1/solutions/nl/01-logic-sets-maps.tex`, solution `pb`
  question 23 — the long inline set-builder for the integer polynomials moved
  into a display (10.78 pt).

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| ch. 13 `thm:b1:continuity:heine` + proof, and the pitfalls remark | **native** — "Zij $f$ continu op $\intcc ab$", "uniform continu", "de twee extremale punten liggen binnen $\delta$ van elkaar"; no `Laat … zijn`, no English clause order |
| ch. 15 `def:b1:integration:step` + `thm:b1:integration:def` | **native** — trapfunctie, verdeling, maaswijdte, "de onderste trapintegraal is $\leq$ elke bovenste", "het supremum en het infimum worden samengeknepen" |
| ch. 17 `rem:b1:series:pitfalls` (five pitfalls) | **native** — "Equivalentie beheerst de \emph{grootte} van de termen, en voor reeksen met wisselende tekens is grootte geen lot"; "Quotiëntlimiet $1$ is stilzwijgen, geen convergentie" |
| ch. 19 `pb:b1:findim:1` (Dedekind's tower law), Parts I–VI | **native** — torenwet, deellichaam, "de $\Q$-dimensie hangt aan elk deellichaam van $\R$ een geheel getal", "$3$ deelt $4$ niet" |
| ch. 21 solutions, `pb:b1:matrices:1` q. 25 | **native** — "machtsverheffen is iteratie geworden", "de begeleidende matrix sluit de kring" |
| ch. 24 `pb:b1:curves:1` (cycloid), Parts I–V | **native** — rollen zonder glijden, keerpunt, ogenblikkelijke rotatiecentrum, tautochroon, "de cycloïde is het leerplan van dit boek, tot één kromme opgerold" |
| ch. 25 `pb:b1:multivar:1` q. 22 (outlier experiment) | **native** — "de kleinste kwadraten zijn efficiënt maar niet robuust" |
| ch. 23 `ex:b1:euclid:parsevalcheck` | **near-native** — accurate and idiomatic, but the sentence architecture ("Deze controle met de som van de kwadraten van de coördinaten (een eindige identiteit van Parseval) kost seconden en …") still shows the English appositive-dash rhythm |
| ch. 16 `rem:b1:taylor:pitfalls` item (iv) | **near-native** — "De rekenkunde van de $o(\cdot)$ is eenrichtingsverkeer" reads well, but the four-item dash-separated block is an English paragraph shape kept for structural parity |
| anywhere | **no MT verdicts** — no sentence in the 50 files was left in a shape a Dutch mathematician would not write |

## Defined-term links (`\omterm`) — target parity vs English

Regenerated with `--unwrap --apply` then `--apply`. The gate

```
diff <(grep -rho '\omterm{[^}]*}' parts/bachelor-1/[0-9]*.tex parts/bachelor-1/solutions/[0-9]*.tex | sort -u) \
     <(grep -rho '\omterm{[^}]*}' parts/bachelor-1/nl/*.tex parts/bachelor-1/solutions/nl/*.tex | sort -u)
```

returns **empty**: the Dutch edition links exactly the English target set.

| Divergence | Verdict |
|---|---|
| *(none)* | The NL target set and the EN target set are identical, so every term that earns a link in English earns one in Dutch, pointing at the same definition |

**Config deltas at first pass: none.** `tools/term_config/book3_nl.py` was not
modified for parity. The existing curation carried the new text unchanged, in
particular:

- `EXTRA` already declares the Dutch solid compounds the index-only harvest skips
  (Riemannsom(men), quotiëntcriterium, Gauss-eliminatie, torenwet, diëdergroep,
  glijspiegeling, Cauchy-determinant, Hilbert-matrix, rij-operatie(s),
  Lagrange-interpolatie, Vandermonde-determinant, groeivergelijking, constante van
  Euler), and `afleidbaar`/`afleidbaarheid`/`continu`/`deelt`/`deelbaar` for the
  definitions whose `\emph{…}` is an inline-math compound. The new prose was
  written to use exactly those forms.
- `NOT_A_TERM` phrase forms (`stelling van`, `formule van`, `ongelijkheid van`,
  `regel van`, `wet van`, `lemma van`, `identiteit van`, `criterium van`,
  `principe van`, `paradox van`) filter the new result names correctly:
  the index keys *formule van Machin*, *formule van Grassmann*, *formule van
  Leibniz*, *stelling van Rolle*, *stelling van Leonardo*, *stelling van
  Schwarz*, *stelling van Pythagoras*, *stelling van Cayley--Hamilton
  (dimensie 2)*, *regel van Cramer*, *algoritme van Euclides* are all filtered,
  exactly as their English counterparts are.
- One key escapes the substring filter by a plural: `\index{formules van Vieta}`
  (ch. 8) does **not** contain `formule van`, so the harvest keeps it as a term
  for `thm:b1:poly:vieta`, where English's `Vieta's formulas` is filtered by the
  default keyword `formula`. It produces **no link** — and therefore no parity
  divergence — because the Dutch prose always writes "volgens Vieta", never the
  full phrase. Left as is (the brief is to curate only where a link is
  wrong-sense); if a later chapter ever writes "formules van Vieta" in running
  text, add `"formules van"` to `NOT_A_TERM` next to the existing
  `"wet van"`/`"wetten van"` pair.
- One index key was deliberately written as a **subentry** so that it is skipped
  by `index_display` (which returns `None` on `!`) instead of relying on the stale
  `DROP` string: `\index{alternerende reeksen!foutschatting}` in
  `pb:b1:taylor:1`, matching English's `DROP`-ped `alternating series estimate`.
  The obsolete `"alternerende reeks schatting"` entry was left in `DROP`
  untouched (harmless, and editing it is not needed for parity).

## Defined-term links — coverage audit (second pass)

Target-set parity does not imply *coverage* parity. Measured per target, the
Dutch edition carried **3 459** links against English's **3 944** — 87 %. A
dedicated audit closed the gap to **3 914 / 3 944 = 99.2 %** and repaired
**16 pre-existing wrong-sense links**.

**Method.** For every `\omterm` target, EN and NL link counts were compared
(`\omterm{<label>}` occurrences over the 50 + 50 files). For each large deficit
the candidate Dutch word forms were counted on the **wrapped** text through
`tools/termlink/protect.masker()` — since `\omterm{…}{…}` is itself masked, a
mask-visible occurrence is exactly one the linker *missed* — restricted to the
chapters at or after the target's defining chapter (earlier uses are skipped by
the generator in both languages). Every surviving form was then read in context
before being declared.

**Three shared-rule causes**, none of them fixable in `tools/term_config/lang_nl.py`
(that file is shared by all five books and would silently re-link them):

1. `WORD_TAIL = (?:e?[ns])?` spells -n/-s/-en/-es but **not the bare attributive
   -e**. English links "continuous" in every position; Dutch lost every
   "continue functie", "lineaire afbeelding", "dichte deelverzameling".
2. `NO_TAIL_END = ("s", …)` in `tools/termlink/morphology.py` gives a term ending
   in **-s** no tail at all (so `reeks` never matched "reeksen", `basis` never
   matched "bases", `bovengrens` never "bovengrenzen"), and Dutch plurals are
   irregular far more often than English ones — interval → interval**len**,
   lichaam → licha**men**, spoor → sp**oren**, supremum → supre**ma**,
   isometrie → isometrie**ën**, priemgetal → priemgetal**len**.
3. The harvester's `\emph` leaf test in `tools/termlink/harvest.py` compares the
   stripped term against the label leaf, so **`orthogonaal` vs leaf `orthogonal`
   fails** and the term was never harvested at all: EN 55 links, NL 3.

Plus a Dutch-specific one: the index-only harvest requires a space in the term,
so the solid compounds *normaalvergelijkingen*, *regressierechte*, *priemdeler*
— English's spaced "normal equations", "regression line", "prime divisor" — were
invisible to it.

**Biggest movers** (EN count · NL before → after):

| Target | EN | before | after | Δ |
|---|---:|---:|---:|---:|
| `def:b1:euclid:orthogonal` | 55 | 3 | 47 | **+44** |
| `def:b1:continuity:continuous` | 215 | 171 | 214 | +43 |
| `def:b1:vspaces:free` | 325 | 290 | 332 | +42 |
| `def:b1:linmaps:def` | 66 | 41 | 79 | +38 |
| `prop:b1:reals:intervals` | 153 | 120 | 147 | +27 |
| `def:b1:logic:statement` | 90 | 55 | 81 | +26 |
| `def:b1:euclid:isometry` | 19 | 19 | 44 | +25 |
| `def:b1:arith:prime` | 57 | 30 | 50 | +20 |
| `def:b1:series:def` | 59 | 37 | 55 | +18 |
| `pb:b1:multivar:1` | 23 | 5 | 23 | +18 |
| `thm:b1:integration:def` | 77 | 50 | 66 | +16 |
| `pb:b1:logic:1` | 33 | 32 | 47 | +15 |
| `def:b1:poly:def` | 227 | 180 | 195 | +15 |
| `thm:b1:multivar:critical` | 18 | 7 | 22 | +15 |
| `def:b1:vspaces:sum` | 28 | 11 | 25 | +14 |
| `def:b1:euclid:def` | 25 | 13 | 25 | +12 |
| `def:b1:reals:bounds` | 64 | 69 | 80 | +11 |
| `def:b1:logic:inj` | 179 | 172 | 183 | +11 |
| `def:b1:findim:def` | 27 | 17 | 27 | +10 |
| `thm:b1:series:alternating` | 3 | 1 | 9 | +8 |

**Two wrong-sense repairs** (both pre-existing; the audit is a correctness pass
as much as a coverage one):

- **`inwendige product` → the interior.** Nine links wrote
  `\omterm{def:b1:topology:closure}{inwendige} product(en)` — the *inner
  product* of ch. 23/25 pointing at the *interior* of ch. 12. Declaring the
  two-word phrase `"inwendige product": "def:b1:euclid:def"` lets the
  longest-first rule take it to the euclidean definition; the singular
  `inwendig product` was already correct and is unaffected. Net effect on
  `def:b1:euclid:def`: 13 → 25 (EN 25).
- **`dicht bij` → dense.** Seven links wrote
  `\omterm{def:b1:topology:dense}{dicht} bij` — ordinary Dutch "close to", not
  the dense subset (ch. 12, 14, 24 and two solution files). Added to
  `EXTRA_PROTECT` as `r'dicht\s+bij'`, the same protection `book5_nl.py` carries.
  English is spared the trap: it writes "close to", not "dense to".

**Deliberate skips, with reasons** (recorded as comments in `book3_nl.py`):

| Form(s) | Why not declared |
|---|---|
| `euclidische` | Two live senses outside ch. 23: "euclidische ruimte" but also "euclidische deling" (six uses, ch. 6/8), "euclidische norm", "euclidische meetkunde". Same call Book 5 made. |
| `vrijheid`, `volledigheid`, `orthogonaliteit`, `lineariteit`, `convexiteit`, `injectiviteit`, `surjectiviteit`, `transcendentie`, `geslotenheid` | The -heid/-iteit abstract nouns. **English does not link theirs**: `lang_en.py` `DERIVE` spells -ally/-ously/-ability/-ely/-ce/-ly but never -ity, and the English tree contains **0** links on *linearity*, *convexity*, *injectivity*, *surjectivity*, *orthogonality*, *completeness*. Declaring them would put NL ~110 links **ahead** of EN on those targets. (`continuïteit`, `dichtheid`, `afleidbaarheid`, `deelbaarheid` stay linked — English links *continuity*, *density*, *differentiability*, *divisibility*, which are harvested or derived there.) |
| `bijectie`, `injectie`, `surjectie` (+ plurals) | Same reason: English links only the adjectives (*injective / surjective / bijective*), never the nouns *bijection* / *injection*. Only the -e adjectives (`bijectieve`, `injectieve`, `surjectieve`) were declared. |

**Where NL now exceeds EN, English is the one under-linking.** `def:b1:euclid:isometry`
(NL 44, EN 19), `def:b1:linmaps:def` (79 vs 66), `pb:b1:logic:1` (47 vs 33),
`def:b1:reals:bounds` (80 vs 64): the same audit run on the English tree would
find 29 unlinked *isometries* (English `WORD_TAIL = (?:e?s)?` cannot reach the
-y → -ies plural), 20 unlinked *bases*, 6 unlinked *suprema*, 23 unlinked
*transcendental* and 11 unlinked *critical*. The Dutch surplus is correct-sense
in every case (each form was read in context); it is English that has room left.

**Residual deficits are content, not rules.** After the pass, the mask-visible
unlinked counts are symmetric between the editions — *veelterm/veeltermen* 28
(EN *polynomial(s)* 34), *groep(en)* 14 (EN *group(s)* 19), *integraal/integralen*
9 (EN 11), *verzameling(en)* 6 (EN 6): all pre-definition chapters, skipped by
the generator in both languages. The 30-link gap that remains is Dutch prose
naming a notion with a compound or a pronoun where English repeats the noun.

All five gates were re-run on top of the current shared Dutch strings (Dutch
cleveref conjunctions in `\AtBeginDocument`, `\today` = 26 juli 2026, part titles
and `\bookline` reading "Bachelorjaar 1", the de-calqued `frontmatter/preface.nl.tex`):
gate **PASSED**, target parity **identical**, `--check` clean, Book 5 golden
**unchanged**, build **0 / 0 / 0** at **411 pp**.

**Re-score: unchanged at 96.** The audit fixed 16 wrong links and added 455
correct ones, but the reasons the book is not a 100 are unrelated to link
coverage (below).

## Why not 100

- **Decimal point kept in all math** (`$0.05$`, `$2.7182818$`, `$3.14126$`). Dutch
  writes a decimal comma; the series keeps the point in every language so the
  shared `parts/` math stays identical. A Dutch first-year reader therefore reads
  a notation that is internationally standard but not native.
- **English paragraph architecture survives in the long remarks.** Structural
  parity forces the same sentence count and the same `---` appositive rhythm as
  the English source; several "Veelgemaakte fouten" and "Vooruitzichten" remarks
  would be shorter and more clause-driven if a Dutch author had written them free
  of that constraint.
- **`\cref` reads as a bare noun** ("volgens \cref{thm:…}", "(\cref{ch:b1:taylor})").
  Dutch tolerates this far better than French (no article map is needed), but a
  handful of places would read better as "de stelling in …".
- **A few proper-name compounds are hyphenated by fiat** (Riemann-reeks,
  Gauss-eliminatie, Hilbert-matrix, Lagrange-basis, Tsjebysjev-veelterm) to match
  the `EXTRA` keys of `book3_nl.py`. That is defensible Dutch and consistent with
  Books 4–5 NL, but a Dutch copy-editor might close some of them up.
- **Index keys are Dutch**, so the EN∩NL index intersection is small. Correct, but
  worth noting for the HTML/online-reader export, which keys some cross-language
  machinery off index terms.
- **Long weekend-problem solutions were self-reviewed, not peer-reviewed.** The
  25 problem solutions run 20–25 questions each; their mathematics was checked
  against the English line by line, but a second Dutch reader would still catch
  stylistic repetitions ("Bijgevolg" density in a few proofs).

## Pipeline actually used

1. Read `translation_instruction.md`, the umbrella `CLAUDE.md` + `book_style.md`,
   and `one-math-book/CLAUDE.md` + `CONTRIBUTING.md`; fixed a glossary and a
   register sheet up front (terms above, `Zij …`, `Weekendopgave --- …`,
   `Deel I --- …`, `\section*{Hoofdstuk \ref{…} --- …}`), reused across all 50
   files.
2. Deleted the stale NL tree and worked chapter by chapter in file order: read the
   English body → write the Dutch body; read the English solutions → write the
   Dutch solutions. Never a sentence-by-sentence pass; each chapter was written as
   Dutch prose from the English content.
3. Anchored terminology per chapter on the old edition's validated `\index{}` keys
   (recovered with `git show HEAD:parts/bachelor-1/nl/NN-*.tex`) and on the
   already-shipped NL volumes, so that link-target parity would hold by
   construction rather than by later curation.
4. A per-chapter structural checker (labels, solution keys, 14-environment census,
   drafty `...`, accent escapes) run after every chapter; `check_translation.sh`
   run at every few chapters. All defects found were fixed immediately (two
   `\end{problem>` typos, one `Schr\"oder` accent escape, one spelling slip).
5. `link_defined_terms.py --unwrap --apply` → `--apply` → target-set diff → `--check`
   → `check_book5_golden.sh`. Parity was clean on the first run; no config edit
   was required for parity.
5b. Second pass: the link-**coverage** audit above (per-target EN/NL counts,
   mask-visible miss scan, context read of every candidate form, 41 `EXTRA`
   declarations + one `EXTRA_PROTECT` regex in `tools/term_config/book3_nl.py`,
   two wrong-sense repairs), then the same pipeline again — 3 459 → 3 914 links.
6. `latexmk` build gate; the two overfull boxes fixed by rewording; rebuild to
   0/0/0.
7. Final sweeps: `Laat … zijn`, accent/cedilla escapes, curriculum and country
   names, old cross-volume wording, residual English (LaTeX and math stripped),
   `\admitted` / `[resume]` / part-header counts against English.
