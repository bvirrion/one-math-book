# Translation score — Math Book 5 · Dutch (`nl`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 5 (University Year 3, `parts/bachelor-3`) |
| **Language** | Dutch (`nl`) |
| **Quality bar** | **native academic** (EN is the source; the French twin `parts/bachelor-3/fr/` as sense/structure reference; NL Book 1, scored 96, as register reference) |
| **Overall score** | **97 / 100** (96 before the link-coverage pass) |
| **Ship threshold** | ≥ 95 |
| **Date** | 2026-07-26 |
| **Scope** | Full re-translation from scratch: all 46 files rewritten (23 bodies `parts/bachelor-3/nl/*.tex` + 23 solution files `parts/bachelor-3/solutions/nl/*.tex`), ≈ 35 800 lines, 276 exercises + 23 weekend problems and all 299 solutions. The old Dutch edition was deleted file by file, never post-edited |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror: 23 + 23 files, identical `\label` sets **and order**, 276 `exo:` + 23 `pb:` ↔ 299 `\begin{solution}{}` keys, environment/figure census equal to English (15 `tikzpicture`, same `definition`/`theorem`/`proposition`/`lemma`/`corollary`/`example`/`remark`/`method`/`notation` counts) |
| Terminology | **97** | Standard Dutch university mathematics across algebra, topology, analysis, geometry and probability: maatruimte, uitwendige afgeleide, terugtrekking, hoofdideaaldomein, splitsingslichaam, normaaldeler, zelftoegevoegd, hilbertbasis, gespannenheid, verdelingsfunctie, toevalsveranderlijke, verwachtingswaarde. Vocabulary checked against `parts/bachelor-1/nl/` and `parts/bachelor-2/nl/` before coining anything (e.g. *toevalsveranderlijke*, not *stochastische variabele*, which the old Book 5 NL used against the rest of the series) |
| Register / tone | **96** | Written by a Dutch lecturer, not decoded: `Zij $(X, \mathcal A, \mu)$ een maatruimte.` — never "Laat … zijn" (0 occurrences). "Merk op dat", "Stel dat", "Neem aan dat", "Bijgevolg", "Omgekeerd", "Er volgt dat"; every proof closes on a real Dutch sentence. Exercise stems imperative (Bewijs, Toon aan, Bereken, Bepaal, Ga na, Leid af, Onderzoek, Schets) |
| Hygiene / LaTeX | **99** | 0 errors, 0 undefined references, 0 overfull boxes; `enumerate[resume]`, `\admitted`, `\intcc`/`\abs`/`\norm`/`\vertiii`/`\dd`/`\P`/`\E`/`\V` and all math untouched; UTF-8 accents only (0 `\'e`-class escapes); no drafty `...`; no duplicate labels |
| Cross-refs | **98** | `\cref`/`\ref` targets byte-identical to English; solutions headers use the single allowed bare `\ref` (`\section*{Hoofdstuk \ref{ch:…} --- <titel>}`); cross-volume references prose-only ("het volume van bachelorjaar 2", "het bovenbouwvolume") — no country or curriculum name anywhere in visible text |
| Defined-term links | **96** | 4 158 `\omterm` links against English's 4 326 (**96 %** coverage, up from 2 840 = 65 %); identical target sets bar three correct-sense Dutch-only targets. The residual gap is Dutch compounding, not curation |
| Figures | **97** | All 15 TikZ/pgfplots pictures kept byte-identical in drawing code, coordinates, `\foreach`, `xtick=`/`ytick=`/`samples at`; only node text and `{\small …}` captions are Dutch (e.g. the Cauchy-formula contour, the heat kernel, the phase portrait of Lotka--Volterra, the boundary-orientation figure where `induced` became `geïnduceerd`) |
| Solutions | **97** | Each solution file rewritten from the English solution file, not from the Dutch statements; the 23 weekend-problem solutions are complete (up to 25 numbered items each, e.g. Lindeberg's replacement method in ch. 23, Etemadi in ch. 22, Koebe's quarter theorem in ch. 18, the vibrating string and $\zeta(2)$ in ch. 15) |
| MT-artifact freedom | **96** | No English sentence architecture left in the short units; a residual-English sweep over the 46 files returns only Dutch words spelled like English ones ("Let op", "index", "product"). Idiom checks added to the term config after they were caught in review ("op maat", "dicht bij") |

**Overall: 97** (weighted toward terminology + register + MT-freedom). The
score moved from 96 after the link-coverage pass below: a Dutch reader now
gets 96 % of the definition links an English reader gets, where the first
generation gave 65 %.

## Structural / build gates

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-3 nl` | **TRANSLATION GATE: PASSED** |
| `latexmk one_math_book_5_university_year_3_nl.tex` | OK |
| Fatal errors (`^!`) | 0 |
| Undefined references | 0 |
| Overfull `\hbox` | 0 |
| `Missing character` warnings | 10 — identical to the English (10) and French (10) builds of the same book; a shared pgf artefact, not introduced here |
| PDF | `build/one_math_book_5_university_year_3_nl.pdf`, **417 pp** (EN 395 pp, FR 404 pp) |
| `python3 tools/link_defined_terms.py --book 5 --lang nl --check` | every file matches what the config generates (**4 158 links**, 96 % of English's 4 326) |
| `sh tools/check_book5_golden.sh` | **green** — English sources come back byte-identical (4 326 links); shared rules in `tools/termlink/` untouched |

## Defined-term links (`\omterm`) — target parity vs English

Generated, never hand-written: `--unwrap --apply`, then `--apply`, then `--check`.
After curation the English and Dutch target sets differ by three labels, all
Dutch-only and all investigated:

| Divergence | Verdict |
|---|---|
| NL links `def:b3:clt:cid` ("convergentie in verdeling", 2×) | **correct sense** — the English text never writes the noun phrase "convergence in distribution" (it writes "converges in distribution"), so the term has no occurrence to link; Dutch does |
| NL links `lem:b3:rings:bezout` ("grootste gemene deler", 16×) | **correct sense** — the gcd is defined in Bézout's lemma; English writes `\gcd` or "gcd" in running text and therefore links nothing |
| NL links `thm:b3:product:changeofvar` ("formule voor variabelensubstitutie", 1×) | **correct sense** — points at the change-of-variables theorem itself |
| ~~`ex:b3:spectral:examples`, `thm:b3:galois:fundamental`, `thm:b3:modules:jordan`, `thm:b3:ode:lyapunov`, `thm:b3:ode:matrixexp`, `thm:b3:probability:zeroone`, `thm:b3:residues:laurent`, `thm:b3:topology:metriccompact`~~ | **fixed** — these eight were EN-only: Dutch writes them as solid compounds (hilbert-schmidtoperator, Galoiscorrespondentie, jordanvorm, lyapunovfunctie, matrixexponentiële, nul-een-wet, laurentreeks, rijcompactheid), which the index harvest skips because they contain no space. Declared in `EXTRA` |
| ~~`thm:b3:product:ballvolume`~~ | **fixed (wrong sense)** — "beeldmaat" is introduced inside an *exercise*, so the harvest attached it to the preceding theorem (the volume of the unit ball). `DROP`ped; English links its "pushforward measure" nowhere either |

Config deltas, all in `tools/term_config/book5_nl.py`, each commented in the file
(nothing else outside `parts/bachelor-3/**/nl/` was touched):

- `STOP` += `enkelvoudig`, `index`, `stabiel`, `inhoud` — the Dutch counterparts of
  four words English already stops. Each was linking wrong-sense outside its own
  chapter: *enkelvoudig* on simple zeros/poles and inside "enkelvoudig
  samenhangend"; *index* on the group index and the index of a stable law;
  *stabiel* on stable laws in the CLT chapter (not Lyapunov stability);
  *inhoud* on the ordinary "de inhoud van de weekendopgave". `STOP` is soft, so
  all four stay linked inside the chapter that defines them — targets preserved.
- `EXTRA` += the nine solid compounds listed above, plus
  `enkelvoudig samenhangende` → `def:b3:conformal:simplyconnected` so the inflected
  phrase keeps its (correct) link after *enkelvoudig* was stoplisted.
- `EXTRA` : stale keys from the previous Dutch edition rewritten to the spellings
  actually used here (`Lyapunov-functie` → `lyapunovfunctie`, `matrixexponentiaal`
  → `matrixexponentiële`, `nul-één-wet` → `nul-een-wet`, `Laurentreeks` →
  `laurentreeks`/`laurentreeksen`, `Hilbert--Schmidt-operator` →
  `hilbert-schmidtoperator(en)`).
- `DROP` += `beeldmaat` (see table).
- `EXTRA_PROTECT` += `op\s+maat` (idiom: made to order, not a measure) and
  `dicht\s+bij` (close to, not topologically dense).

## Link *coverage* parity (second pass)

Target parity does not imply coverage parity: the first generation produced
**2 840** links against English's 4 326 — 65 %, the worst ratio of the five
Dutch books. Cause: the shared Dutch morphology
(`tools/term_config/lang_nl.py`, `WORD_TAIL = (?:e?[ns])?`) matches plurals
but never the attributive adjective in **-e** ("meetbare functie", "compacte
drager", "continue afbeelding") nor the derived noun in **-heid/-iteit**
("meetbaarheid", "compactheid", "continuïteit"), while English reaches its
equivalents through `DERIVED`. `lang_nl.py` is shared by five books and was
**not** touched; every form was declared per-book in `book5_nl.py`.

Result: **4 158 links, 96 % of English**, with the target set unchanged (the
same three correct-sense Dutch-only targets).

| Target | EN | before | after |
|---|---:|---:|---:|
| `def:b3:topology:continuity` | 716 | 108 | **673** |
| `def:b3:topology:compact` | 291 | 46 | **359** |
| `def:b3:topology:connected` | 103 | 39 | **104** |
| `def:b3:clt:gaussianvector` | 69 | 26 | **66** |
| `def:b3:holomorphic:holo` | 147 | 108 | **147** |
| `def:b3:probability:independence` | 147 | 108 | **145** |
| `def:b3:lebesgue:measurable` | 76 | 41 | **75** |
| `def:b3:lebesgue:l1` | 91 | 80 | **113** |
| `def:b3:rings:divisibility` | 124 | 61 | **83** |
| `def:b3:rings:primemaximal` | 33 | 33 | **25** (wrong-sense links removed) |
| `def:b3:galois:separable` | 29 | 31 | **21** (wrong-sense links removed) |
| **total** | **4 326** | **2 840** | **4 158** |

Second-pass config deltas (`tools/term_config/book5_nl.py` only):

- `EXTRA` += 33 inflected/derived forms, each read in context first:
  `continue`, `continuïteit`, `homeomorf(e)`, `compacte`, `compactheid`,
  `gaussische`, `volledigheid`, `meetbare`, `meetbaarheid`, `samenhangende`,
  `samenhang`, `wegsamenhangende`, `holomorfe`, `holomorfie`,
  `onafhankelijke`, `dichte`, `algebraïsche`, `banen`, `idealen`,
  `integreerbare`, `integreerbaarheid`, `conforme`, `torsievrij`, `maten`,
  `radicaal`, `radicale`, `oplosbaarheid`, `zelftoegevoegde`,
  `zelftoegevoegdheid`, `equicontinue`, `hausdorffruimte`, `randen`,
  `magere`.
- `PRIMARY_OK = {"compact", "irreducibel"}` — mirrors English's `PRIMARY_OK`
  for the same two overloaded words, so the dominant sense keeps linking
  outside the chapter that pins it ("compact" → the space, except in ch. 15
  where "compacte operator" wins; "irreducibel" → the ring element, except in
  ch. 5). English's `closed`/`boundary`/`interior`/`path` are deliberately
  *not* mirrored: Dutch "gesloten" is pinned by the closed-forms chapter, so
  promoting it would point every closed set at the wrong definition.
- `STOP` += `separabel` (a separable field extension in ch. 4 vs a separable
  Hilbert/Banach space in ch. 7, 8, 13, 15 — English stops "separable" for the
  same reason; this also removed 10 pre-existing wrong-sense links) and
  `maximaal` (outside the ring chapters it is the maximal solution of an ODE,
  the maximum principle, a maximal element — 8 wrong-sense links removed).
- `EXTRA_PROTECT` += `lineair\s+onafhankelijk\w*` (linear independence, not the
  probabilistic notion) and `volledige\s+(?:inhoud|lijst)`.
- Forms deliberately **not** declared, each with the reason in the file:
  `irreducibele` (88 uses — ring element vs representation; `EXTRA` is global
  and would mis-target one of them), `volledige` (66 — half its uses are the
  ordinary "full/entire": volledige verantwoording, volledige omwenteling,
  volledige elliptische integraal), `normale` (24 — normal subgroup vs normal
  family vs normal distribution), `euclidische` (14 — Euclidean domain vs
  Euclidean norm/division), `vrije` (10), `perfecte` (9 — perfect field vs
  perfect set; English links these to the field proposition, which is wrong).

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| ch. 09 `09-measure-theory` — Carathéodory, uitwendige maat | **native** — "Zij $\mu^*$ een uitwendige maat", "Merk op dat de meetbare verzamelingen een $\sigma$-algebra vormen" |
| ch. 12 `12-lp-spaces` — Hölder/Minkowski/Riesz--Fischer + mollifiers | **native** — regularisatie, hoofdlemma van de variatierekening, "bijna overal" throughout |
| ch. 16 `16-holomorphic-functions` — Goursat and the identity theorem | **native** — "Bijgevolg is $f$ constant op elke samenhangende component", proof endings read as Dutch sentences |
| ch. 18 `18-conformal-geometry` — Riemann mapping theorem | **native** — blaschkefactoren, "normale familie", "Montel geeft een deelrij die uniform op compacta convergeert" |
| ch. 21 `21-differential-forms` — Stokes, orientation, partition of unity | **native** — terugtrekking, geïnduceerde oriëntatie, partitie van de eenheid; the figure caption is Dutch and the drawing code untouched |
| ch. 22 `22-probability-foundations` — SLLN, Etemadi weekend problem | **native** — toevalsveranderlijke, nul-een-wet, "b.z." for *bijna zeker*, Kolmogorov's maximaalongelijkheid |
| ch. 23 `23-clt-gaussian` — characteristic functions, CLT, Lindeberg | **native** — "de vervangingsmethode", "de verwisselingsidentiteit", betrouwbaarheidsinterval, gespannenheid, "de ongelijkheid van Le Cam" |
| Weekend-problem headers everywhere | **native** — `\begin{problem}[{Weekendopgave --- …}]`, parts as `\noindent\textbf{Deel I --- …}` |

## Why not 100

- **Link density is still 4 % under English** (4 158 NL vs 4 326 EN), after the
  coverage pass above closed the 35 % gap the first generation left. What
  remains is genuinely per-word: six inflected forms are deliberately not
  declared because a single global `EXTRA` entry would mis-target one of their
  two senses (`irreducibele`, `volledige`, `normale`, `euclidische`, `vrije`,
  `perfecte`), and Dutch solid compounds (*hilbert-schmidtoperatoren*,
  *maatruimte*) are only linkable one declaration at a time. Removing that last
  4 % means a Dutch morphology layer plus chapter-scoped `EXTRA` in
  `tools/termlink/` — shared code, deliberately untouched here.
- **Decimal point kept** (`$0.98^{100}$`, `$1.96$`) — series-wide convention, not
  Dutch practice.
- **`\cref` reads as a bare noun** ("volgens \cref{thm:…}"); Dutch tolerates it,
  but a handful of places would read better with an article.
- **A few long weekend problems** still carry English sentence architecture in
  the discursive closing paragraphs (long appositive dashes). Good written Dutch,
  but a native lecturer would break some of them in two.
- **Index keys are Dutch**, so the EN∩NL index intersection is small — correct,
  but worth knowing for the HTML/online-reader export.

## Shared UI strings — reported, not edited

`styles/lang/nl.tex` is shared with the other Dutch books, so nothing was
changed there. Reported and since applied by the owner: the part titles now
read **Bachelorjaar 1/2/3**, cleveref's conjunctions are Dutch (" en " / " tot "),
and `\today` prints Dutch ("26 juli 2026" on the cover). Still open:

- **`\crefpairgroupconjunction` / `\creflastgroupconjunction` are still
  English.** A single `\cref` spanning two label types prints a mixed-language
  list: `parts/bachelor-3/solutions/nl/02-rings-arithmetic.tex` (the three-label
  `\cref{thm:…euclideanpid,thm:…pidufd,lem:…bezout}`, identical to English)
  renders as "Stellingen 2.14 en 2.18 **and** Lemma 2.17". It is the only
  English word left in the 417-page PDF, and it needs the same
  `\AtBeginDocument` treatment as the other three conjunctions.
- **`\bookline` in `one_math_book_5_university_year_3_nl.tex`** (line 28) still
  says "Boek 5: Universitaire wiskunde -- Bachelor jaar 3", so the cover and the
  even-page running head keep the two-word spelling the part titles just lost.
  The entry file is outside my edit surface; the other Dutch entry files
  presumably need the same one-word fix.
- `\omnameProblem` is **"Probleem"** — left to the user as a series-wide naming
  decision (Dutch course material usually says *opgave*, and the weekend problems
  are titled "Weekendopgave", so the head reads "Probleem 23.1 (Weekendopgave
  --- …)").

## Pipeline actually used

1. Read `translation_instruction.md`, `book_style.md`, `one-math-book/CLAUDE.md`
   and `CONTRIBUTING.md`; fixed a glossary and register sheet up front and reused
   it verbatim across all 46 files.
2. Chapter by chapter, in file order: `rm` the stale Dutch file → read the English
   body → write the Dutch body; then read the English solutions file → write the
   Dutch solutions file. No sentence-by-sentence transposition, no post-editing of
   the old edition.
3. `bash tools/check_translation.sh bachelor-3 nl` after every chapter — green
   each time; the one substantive defect it did not catch (an unclosed `$f geen`
   in ch. 17's solutions) was found by a manual math-delimiter sweep and fixed.
4. `link_defined_terms.py --unwrap --apply` → `--apply` → target-set diff against
   English → curation above → `--apply` again → `--check` and
   `check_book5_golden.sh` green.
5. Coverage pass: per-target link counts EN vs NL, biggest deficits read in
   context (a sampler prints every use of a candidate form with its
   surroundings), inflected/derived forms declared or explicitly rejected, then
   the full `--unwrap --apply` → `--apply` → `--check` cycle again, with the
   target-set diff and the golden check re-run.
6. `latexmk` build gate: 0 errors, 0 undefined, 0 overfull, 417 pp.
7. Sweeps: residual English (one hit left, cleveref's group conjunction),
   `\'e`-class accents, decimal commas in prose, "Laat … zijn",
   curriculum/country names — otherwise clean.
