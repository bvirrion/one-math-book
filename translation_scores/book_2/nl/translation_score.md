# Translation score — Math Book 2 · Dutch (`nl`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 2 (High School, grades 10–12) |
| **Language** | Dutch (`nl`) |
| **Quality bar** | **native academic** (EN is the source; the freshly rewritten NL Book 1 is the register/terminology reference) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 |
| **Date** | 2026-07-26 |
| **Scope** | Full re-translation **from scratch**: 35 bodies + 35 solution files (≈ 23 800 lines of English), including the **35 weekend `problem` environments and their 35 `\begin{solution}{pb:…}` blocks, which the previous Dutch edition did not contain at all** |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror (35 + 35); identical label sets and order; 35 `problem` envs ↔ 35 `pb:` solutions; per-environment and figure census equal to English in all three years |
| Terminology | **97** | Netherlands Dutch, consistent with the rest of the NL series: richtingscoëfficiënt, affiene functie, veelterm, verlooptabel, afgeleide, primitieve functie, integraal, rij/reeks, limiet, toevalsvariabele, kansverdeling, verwachtingswaarde, standaardafwijking, met teruglegging, variatiebreedte, relatief priem, volkomen kwadraat, stelling van Pythagoras/Thales, grootste gemene deler. New grade-12 vocabulary chosen against Dutch textbook usage: variatie/permutatie/combinatie, faculteit, binomiaalcoëfficiënt, complex toegevoegde, beeldgetal, eenheidswortels, euclidische deling, verbindingsmatrix, wandeling, coplanair, kruisende rechten, kansdichtheid, geheugenloosheid |
| Register / tone | **96** | Written Dutch, not translated English: `Zij $f$ een continue functie op $[a,b]$.` — **0** occurrences of the calque "Laat … zijn" as a definition opener (the old edition had 189); "Merk op dat", "Ga na dat", "Bijgevolg", "Omgekeerd", "Daaruit volgt"; exercise stems imperative (Bereken, Bewijs, Toon aan, Bepaal, Leid af, Los op) |
| Hygiene / LaTeX | **98** | 0 errors, 0 undefined refs, 0 overfull boxes; 5 log warnings, all cosmetic/environmental (see *Why not 100*); UTF-8 accents only, 0 `\'e`-class escapes; `enumerate[resume]`, `\admitted`, decimal **point** and all math preserved |
| Cross-refs | **98** | `\cref`/`\ref`/`\label`/`solution{key}` byte-identical to English; cross-volume references prose-only ("het onderbouwvolume", "de universitaire volumes"); no country or curriculum name anywhere in visible text |
| Figures | **97** | TikZ/pgfplots drawing code byte-identical (coordinates, `\foreach`, `samples at`, `fill between`, `soft clip`); only node text and `{\small …}` captions translated; the binomial tree's S/F nodes localized to S/M (succes / mislukking) |
| Solutions | **97** | Every solution rewritten from the English solution, headers `\section*{Hoofdstuk \ref{ch:…} --- <Nederlandse titel>}`; all 35 twenty-question weekend-problem solutions fully written |
| MT-artifact freedom | **96** | Nothing survives from the machine-translated edition (files were deleted before rewriting); the old MT terms "veranderingstabel", "ontwikkelen", "toevalsveranderlijke" are gone in favour of verlooptabel, uitwerken/ontbinden, toevalsvariabele |

**Overall: 96** (weighted toward terminology + register + MT-freedom).

## Structural / build gates

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh grade-10 nl` | **PASSED** |
| `bash tools/check_translation.sh grade-11 nl` | **PASSED** |
| `bash tools/check_translation.sh grade-12 nl` | **PASSED** |
| `latexmk one_math_book_2_high_school_nl.tex` | OK |
| Fatal errors (`^!`) | **0** |
| Undefined references | **0** |
| Overfull boxes | **0** |
| LaTeX warnings | 5 (2 environmental, 2 cosmetic `tcolorbox nobreak`, 1 `amsthm \qedhere`) |
| PDF | `build/one_math_book_2_high_school_nl.pdf`, **342 pp** (EN 330 pp) |
| `python3 tools/link_defined_terms.py --book 2 --lang nl --check` | *every file matches what the config generates* — 3 638 links (def 3 390, prop 115, pb 46, thm 36, ex 27, met 24) |
| `sh tools/check_book5_golden.sh` | unchanged (shared termlink rules untouched) |

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| G10 `02-algebra…` "Nulproductregel" + method | **native** — "een product is nul als en slechts als een van de factoren nul is"; "deel nooit door $x$: de oplossing 0 zou verloren gaan" |
| G11 `04-sequences` definitions | **native** — rekenkundige rij / verschil, meetkundige rij / reden; the theatre exercise phrased so *rij* reads unambiguously as a row of seats |
| G12 `08-combinatorics` §"$k$-tallen, permutaties, faculteiten" | **native** — "$k$-tal", "variatie", "$n$ boven $k$", "somprincipe/productprincipe", "met teruglegging, in volgorde" |
| G12 `09-complex-numbers` §"Het complexe vlak, modulus en argument" | **native** — beeldpunt/beeldgetal, complex toegevoegde, goniometrische en exponentiële vorm, "moduli vermenigvuldigen zich, argumenten tellen op" |
| G12 `10-arithmetic` proof of Fermat's little theorem | **native** — "schrap en herhaal", "wegdelen", "op de volgorde van de factoren na" |
| G12 `pb:g12:contdist:1` (bus paradox) solution | **native** — "naar lengte vertekende bemonsteren", "de stroom veroudert niet", "het interval dat je toevallig inspecteert, is geen typisch interval" |
| G12 `solutions/06-integration` | **native** — "primitieve functie", "hoofdstelling van de integraalrekening", "partiële integratie", "de aangroei $F(x+h)-F(x)$" |
| G10 `08-statistics` + `09-probability…` | **native** — statistische reeks, frequentie, mediaan, kwartiel, interkwartielafstand, variatiebreedte, uitkomstenverzameling, gebeurtenis, boomdiagram, steekproef |

No sample in the rewritten tree reads as MT; the weakest spots are *near-native*
long weekend-problem sentences that keep the English appositive-dash rhythm
(see *Why not 100*).

## Defined-term links (`\omterm`) — target parity vs English

Regenerated with `--unwrap --apply` then `--apply`; `--check` green. Per-year
target-set diff against English:

| Year | Divergence | Verdict |
|---|---|---|
| grade-10 | *none* | — |
| grade-11 | EN links `def:g10:stats:median` (on "median"), NL does not | **English over-link, Dutch is right.** The word is the *geometric* median of a triangle (`ch:g11:vect`), which Dutch calls **zwaartelijn** — a different word from the statistical **mediaan**. English's homonym makes it point at the statistics definition; Dutch has no homonym, so there is nothing to link. Deliberate non-link, no config entry needed. |
| grade-12 | *none* (after the config deltas below) | — |

Investigated and resolved during this pass (all now parity-clean):

| Was | Fix |
|---|---|
| NL linked `thm:g12:comb:binomial` on "binomium van Newton"; EN leaves "binomial theorem" plain (its default `NOT_A_TERM` catches "theorem") | added `"binomium van"` to the Dutch `NOT_A_TERM` — it is a *result name*, exactly the class the Dutch phrase-form list exists for |
| EN linked `met:g12:contdist:fluctuation` on "confidence interval"; NL could not, because **betrouwbaarheidsinterval** is a solid compound and the index-only harvest requires a space | added to `EXTRA` |
| EN linked `thm:g12:exp:growth` on "growth comparison"; NL could not, because **groeiorden** is one word | added to `EXTRA`, plus a lookahead `EXTRA_PROTECT` so the surrounding "vergelijking van groeiorden" (= *comparison*, not *equation*) no longer links *vergelijking* to `def:g10:algebra:equation` |
| NL linked `pb:g11:scal:1` on "hoogtepunt" in `solutions/15-sums-lln` (there = *climax*, not *orthocenter*) | wrong-sense link removed by rewording the sentence ("bekroont de kansrekening…"), no config entry |

## Config deltas (`tools/term_config/book2_nl.py`, each commented in the file)

- `NOT_A_TERM += "binomium van"` — Dutch phrase form of a theorem name.
- `EXTRA += "betrouwbaarheidsinterval" → met:g12:contdist:fluctuation` — solid compound the index-only harvest cannot see.
- `EXTRA += "groeiorden" → thm:g12:exp:growth` — same reason.
- `EXTRA_PROTECT += r'[Vv]ergelijking(?:en)?(?=\s+van\s+groeiorden)'` — lookahead so only *vergelijking* is masked and *groeiorden* stays linkable.

Nothing else outside `parts/grade-1{0,1,2}/…/nl/` was touched.

## Reported, not changed (shared files, other agents active in this repo)

- `styles/lang/nl.tex` was reviewed and needs no change: Definitie, Stelling,
  Propositie, Lemma, Gevolg, Methode, Voorbeeld, Notatie, Opmerking,
  Oefening(en), Probleem, Bewijs, Hoofdstuk, Deel, Bijlage and
  "Op dit niveau zonder bewijs aangenomen." are all correct Dutch.
- `book2_nl.py`'s `DROP = {"Ontwikkelen"}` is now **stale**: the rewritten edition
  uses *uitwerken* / *ontbinden* and never *ontwikkelen*, so the entry is inert.
  The neighbouring `NO_CAPITAL` comment ("Ontbind", "Ontwikkel") should lose its
  second example at the same time. Left in place rather than edited, since these
  are one-line cosmetic cleanups and other agents are working in this file's
  directory.

## Why not 100

- **Decimal point everywhere** (`$4.362$`, `$1.5$ h`, `$0.7$ m`): the series keeps
  the point in all languages so the shared `parts/` math is identical, but a Dutch
  reader writes a comma. Series-wide decision, not fixable here.
- **Register in the longest weekend problems.** The 20-question problems are good
  written Dutch, but a few inherit the English sentence architecture (long
  appositive dashes, "In één zin:", "Slotstuk ---"). A Dutch teacher would break
  some of them into shorter sentences.
- **Two cosmetic `tcolorbox nobreak` warnings** (`grade-10/nl/05-coordinate-geometry`
  line 148, `grade-11/nl/03-differentiation` line 240): a coloured box lands too
  close to a page bottom. Longer Dutch prose makes this slightly likelier than in
  EN/FR/ES (which carry one such warning each). Two rewording attempts did not
  move the break; not worth distorting the text further, and it is invisible in
  the PDF.
- **Dutch link coverage is thinner than English by construction.** Dutch writes
  compounds solid (verbindingsmatrix, kansdichtheid, steekproefgemiddelde), and
  the shared rule refuses to link a component inside a compound — safer, but it
  means a Dutch reader gets fewer term links per page than an English one. Only
  the two cases where English *did* link and Dutch could not were repaired
  (`EXTRA`); a systematic sweep would need dozens more entries and is not
  obviously an improvement.
- **`\cref` reads as a bare noun** ("volgens \cref{thm:…}"). Dutch tolerates this
  far better than French (no article map needed), but a handful of spots would
  read better as "de stelling in …".
- **Index keys are Dutch** (faculteit, priemgetal, eenheidswortels,
  kansdichtheid) — correct, but the EN∩NL index intersection is small; noted for
  the HTML/online-reader export, nothing to fix.

## Pipeline actually used

1. Read `translation_instruction.md`, the root `CLAUDE.md` / `book_style.md`, the
   repo's `CLAUDE.md` / `CONTRIBUTING.md`, then three files of the rewritten NL
   Book 1 to fix register and terminology up front.
2. Confirmed the baseline defect: `check_translation.sh` failed on all three years
   with `problem count 1->0` and a missing `pb:` label per chapter.
3. Per year: `rm -f parts/<year>/nl/[0-9]*.tex parts/<year>/solutions/nl/[0-9]*.tex`,
   then chapter by chapter — read the English body → write the Dutch body fresh;
   read the English solutions → write the Dutch solutions fresh. Never
   post-edited the old MT text.
4. `bash tools/check_translation.sh <year> nl` at each year boundary; every
   reported class fixed before moving on (one `\'e` accent escape was the only
   failure in the whole grade-12 pass).
5. `link_defined_terms.py --unwrap --apply` then `--apply`; per-year target-set
   diff against English; the four divergences above investigated one by one and
   fixed (three by config, one by rewording a wrong-sense link); `--check` and
   `check_book5_golden.sh` green.
6. `latexmk` build gate: three overfull boxes found and removed by rewording
   (a modulus display split in two, a long inline `\P(\text{…})` shortened, a
   packed page in `06-integration` relieved by tightening a proof), plus a
   `\texorpdfstring` for the one section title containing math.
7. Final sweeps: "Laat … zijn" calque count, curriculum/country-name grep,
   accent-escape grep, `pdftotext` spot-reads of a solutions page and the
   fundamental-theorem page.
