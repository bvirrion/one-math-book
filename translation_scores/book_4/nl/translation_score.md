# Translation score — Math Book 4 · Dutch (`nl`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 4 (University Year 2, `parts/bachelor-2`) |
| **Language** | Dutch (`nl`) |
| **Quality bar** | **native academic** (EN is the source; FR Book 4 and NL Book 3 as register/terminology references) |
| **Overall score** | **97 / 100** |
| **Ship threshold** | ≥ 95 |
| **Date** | 2026-07-26 (second link-density pass same day) |
| **Scope** | Full re-translation from scratch: 23 bodies + 23 solution files, i.e. the whole volume — 276 exercises, 23 weekend problems and every solution rewritten from the English |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror (23 + 23); identical label sets and order; 276 `exercise` ↔ 276 `\begin{solution}{exo:…}`, 23 `problem` ↔ 23 `\begin{solution}{pb:…}`; env/figure census equal to English in every chapter; the one untitled `problem` (ch. 12) stays untitled |
| Terminology | **97** | Standard Dutch university mathematics: genormeerde vectorruimte, volledigheid, samenhang, kwadratische vorm, polarisatie-identiteit, congruente matrices, signatuur, spectraalstelling, hermitisch inproduct, Fouriercoëfficiënten, Dirichlet-kern, jacobimatrix, kettingregel, wronskiaan, fundamentaalstelsel, barycentrum, convexe omhulsel, booglengte, kromtestraal, osculerende cirkel, torsie, eerste fundamentaalvorm, lijnintegraal, exacte/gesloten vorm, uitkomstenruimte, kansmaat, toevalsveranderlijke, verwachtingswaarde, kansgenererende functie. Result names follow the Dutch pattern `stelling van Cauchy--Lipschitz`, `ongelijkheid van Bessel`, `identiteit van Parseval` |
| Register / tone | **96** | Written, not translated: 169 statements open `Zij $E$ een genormeerde vectorruimte…` (0 occurrences of the `Laat … zijn` calque), "Merk op dat", "Stel dat", "Bijgevolg", "Omgekeerd"; exercise stems are imperatives (Bewijs, Toon aan, Bereken, Bepaal, Ga na, Leid af, Onderzoek, Schets) |
| Hygiene / LaTeX | **99** | 0 errors, 0 undefined refs, 0 overfull boxes; `enumerate[resume]`, `\admitted`, all math and macro usage as in English; UTF-8 accents only (0 `\'e`-class escapes); index keys Dutch and matching the visible term |
| Cross-refs | **98** | `\label`, `\cref`/`\ref` targets and `\begin{solution}{…}` keys byte-identical to English; cross-volume references prose-only (`het bovenbouwvolume`, `het volume van bachelorjaar 1`, `de universitaire volumes`) — no country or curriculum name anywhere in visible text (the two English mentions of a national programme in ch. 21 were replaced by neutral Dutch) |
| Defined-term links | **97** | 3 433 `\omterm` links = **97.8 % of English** (3 433 vs 3 511), identical target set; every remaining divergence audited term by term (table below) |
| Figures | **96** | TikZ/pgfplots drawing code, coordinates, `\foreach`, `xtick=`/`ytick=`/`samples at` byte-identical; only node text and `{\small …}` captions translated (e.g. the phase-portrait chart: zadelpunten, stabiele/instabiele knopen, stabiele/instabiele spiralen, centra) |
| Solutions | **97** | Every solution rewritten from the English solution; headers `\section*{Hoofdstuk \ref{ch:…} --- <Nederlandse titel>}` ×23; the 23 weekend-problem solutions (≈20 questions each) fully rendered, parts as `\noindent\textbf{Deel I --- …}` |
| MT-artifact freedom | **96** | A residual-English sweep (math and macros stripped, English wordlist) over the 46 files returns only Dutch words spelled like English ones (matrix, product, open, compact, vector) and label names inside `\cref{ch:b2:series}` / `\cref{ch:b2:surfaces}` — no untranslated prose, no leftover English figure captions |

**Overall: 97** (weighted toward terminology + register + MT-freedom; +1 over the
first pass for the link-coverage work described below).

## Structural / build gates

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-2 nl` | **TRANSLATION GATE: PASSED** |
| `latexmk one_math_book_4_university_year_2_nl.tex` | exit 0 |
| Fatal errors (`^!`) | 0 |
| Undefined references | 0 |
| Overfull `\hbox` | 0 |
| PDF | `build/one_math_book_4_university_year_2_nl.pdf`, 419 pp (EN 397 pp, FR 417 pp) |
| `python3 tools/link_defined_terms.py --book 4 --lang nl --check` | every file matches what the config generates (3 433 links: def 3 141, thm 116, pb 107, ex 64, lem 4, prop 1) |
| `\omterm` target set vs English | **identical** — 85 targets on both sides, empty diff |
| `\omterm` link count vs English | 3 433 vs 3 511 = **97.8 %** |
| `sh tools/check_book5_golden.sh` | unchanged (shared termlink rules untouched) |

Three overfull boxes appeared on the first build and were fixed at the source
rather than with glue: the ch. 17 example title (`[Overbodige voortbrengers]`),
the ch. 18 local-shape table (`\small` + `p{5.6cm}` last column), and one
sentence in the ch. 12 solutions.

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| ch. 4 `04-metric-topology` (limieten, continuïteit, compactheid) | **native** — "Een afbeelding $f \colon X \to Y$ tussen metrische ruimten heet continu in $a$ wanneer…", "De compactheid leverde precies één ding" |
| ch. 12 `12-quadratic-forms` (Gauss-reductie, traagheidswet) | **native** — "drie positieve kwadraten op onafhankelijke vormen, signatuur $(3,0)$" |
| ch. 14 `14-fourier-series` opening | **native** — "Kan elk periodiek signaal uit zuivere sinussen en cosinussen worden heropgebouwd? Fouriers vermetele ``ja'' bracht een eeuw analyse voort." |
| ch. 16 `16-differential-equations` + phase-portrait figure | **native** — stelling van Cauchy--Lipschitz, fundamentaalstelsel, zadelpunten/knopen/spiralen |
| ch. 18 `18-curves` solutions (cycloïde, Frenet) | **native** — "en $\norm{\gamma'(t)} = 2\sin\frac t2$ (niet-negatief op $[0,2\pi]$). Bijgevolg is…" |
| ch. 21 `21-countable-probability` opening | **native** — "De eindige theorie van het bovenbouwvolume krijgt haar volledige infrastructuur: $\sigma$-additiviteit vervangt de eindige additiviteit" |
| ch. 22 `pb:b2:randomvar:1` (concentratie: Hoeffding, Chernoff) | **native** — concentratieongelijkheden, grens van Chernoff, "Ga na dat…" |
| ch. 23 `23-generating-functions` + closing `\section*{Het volume afsluiten}` | **native** — kansgenererende functie, vertakkingsproces, uitstervingskans |

## Defined-term links (`\omterm`) — target parity vs English

Regenerated with `--unwrap --apply` then `--apply`. The **target set is exactly
English's** (85 labels, empty diff both ways). Two divergences were found on the
way and each was resolved at the source, not papered over:

| Divergence | Verdict |
|---|---|
| NL had an extra target `thm:b2:diffcalc:taylor`, fed by 10 links on "hessiaan" | Dutch names the object with one word where English uses the two-word "Hessian matrix", which never matches; the English book therefore never links it. `hessiaan`/`hessianen`/`Hessematrice` moved to `DROP` — parity restored, and the link was pointing at the Taylor theorem rather than at a definition anyway |
| NL was missing `thm:b2:nvs:finitedim` (equivalence of norms in finite dimension) | the Dutch ch. 5 used the same `\index` key at the definition and at the theorem, so the harvest saw an ambiguous term and dropped it. The definition was re-keyed `\emph{equivalent}\index{equivalente normen}`, leaving `equivalentie van normen` to harvest uniquely to the theorem, as in English |

Link **density** was then audited target by target against English (parity of the
target set does not imply parity of coverage). The raw translation sat at 2 365
links vs. English's 3 511 — a Dutch-specific gap, because `lang_nl.py` sets
`WORD_TAIL = (?:e?[ns])?`, so the attributive `-e` adjective and the abstract
noun never match on their own, while English gets them from `DERIVED`
(continuity/continuously, compactness). Two passes of `EXTRA`/`STOP` curation,
each link read in context before it was accepted, took the book to

    2 365  →  2 936  →  **3 433 links = 97.8 % of English** (NL Book 5: 96 %)

with the same 85 targets throughout. Biggest movers (EN / NL before / NL after):

| Target | EN | before | after | what was missing in Dutch |
|---|--:|--:|--:|---|
| `def:b2:metric:continuity` | 481 | 44 | 455 | `continu` was `STOP`-listed; `continue`/`continuïteit` are unreachable forms |
| `def:b2:proba:independence` | 117 | 39 | 125 | `onafhankelijke`, `onafhankelijkheid` — safe globally because the wrapper never links a term before its defining chapter, so chs. 1–20 (*lineair onafhankelijk*) are untouched |
| `def:b2:metric:compact` | 159 | 59 | 156 | `compacte`, `compactheid` |
| `def:b2:metric:topology` | 82 | 35 | 81 | `open` was `STOP`-listed; every use in the book is the topological one |
| `def:b2:hermitian:adjoint` | 89 | 50 | 91 | `hermitische`, `unitaire`, `antihermitisch(e)` (English reaches "skew-Hermitian" through the shared hyphen-prefix rule, which cannot fire on a Dutch solid compound) |
| `def:b2:randomvar:law` | 87 | 38 | 78 | `verdeling` was `STOP`-listed; the ordinary-language risk is `wet`, which stays stopped |
| `def:b2:series:def` | 53 | 28 | 76 | `absoluut` was `STOP`-listed + `absolute convergentie` |
| `def:b2:funcseq:def` | 112 | 79 | 110 | `uniforme`, `puntsgewijze` |
| `def:b2:affine:subspace` | 65 | 33 | 66 | `affiene` |
| `def:b2:quadratic:adjoint` | 60 | 42 | 74 | `symmetrische`, `zelftoegevoegde` |
| `def:b2:metric:complete` | 83 | 66 | 93 | `volledigheid` |
| `def:b2:curves:length` | 72 | 47 | 66 | `lengte` was `STOP`-listed (ch. 21's path lengths are protected instead, as in English) |
| `def:b2:series:summable` | 66 | 48 | 67 | `sommeerbare`, `sommeerbaarheid` |
| `def:b2:affine:barycenter` | 44 | 27 | 43 | `barycentra` |
| `def:b2:metric:connected` | 40 | 17 | 32 | `samenhang`, `samenhangende` |
| `def:b2:linalg:dual` | 32 | 14 | 27 | `duale` was `STOP`-listed |
| `def:b2:structures:generated` | 92 | 73 | 85 | `voortgebracht`, `voortgebrachte` |

The remaining differences were each inspected and are deliberate:

| Divergence | Verdict |
|---|---|
| `def:b2:reduction:eigen` (EN 361 / NL 335), `def:b2:metric:continuity` (481/455), `def:b2:nvs:norm` (113/98) | prose frequency, not curation: every occurrence of *eigenwaarde(n)*, *continu(e)*, *norm(en)* is linked; Dutch simply repeats the noun less than English, which re-states "the eigenvalues of $A$" where Dutch says "ze" |
| `def:b2:structures:sn` (51/40) | the unlinked Dutch *cykel* uses sit inside the defining definition, the theorem titles and `$k$-cykel` math compounds — English's profile is the same, only its plural "cycles" fires more often |
| `def:b2:surfaces:area` (38/27) | Dutch writes the solid compound *oppervlakte-element*, which English spells as two words; the English phrase is not linked either, so a Dutch `EXTRA` would over-link relative to the source |
| `def:b2:funcseq:series` (41/31) | bare `normale` is genuinely ambiguous here (normale modi, normale component, normaal endomorfisme); the phrase *normale convergentie* keeps the link — the same call English makes with its `STOP` on "normal" |
| `uniforme` in chs. 21–23 (uniforme verdeling/steekproef/maat) | not linked, by an `EXTRA_PROTECT` look-ahead that mirrors English's `uniformly\s+(?:at random\|chosen\|…)` — the uniform *law* is not uniform *convergence*. The look-ahead consumes only the adjective, so the noun after it still links |
| NL ahead on `def:b2:series:def` (53/76), `def:b2:fourier:coefficients` (5/21), `def:b2:curves:arc` (9/24), `def:b2:quadratic:adjoint` (60/74), `ex:b2:powerseries:fibonacci` (42/56) | Dutch splits into two forms what English says with one (*absoluut* / *absolute convergentie*), or writes a solid compound (Fourierreeks, geparametriseerde boog, genererende functies) that English's multi-word form misses. Extra service to the reader, same targets |

Config deltas (`tools/term_config/book4_nl.py`, each commented in the file):

- `DROP` += `Hessematrice`, `hessiaan`, `hessianen` (target parity, see above).
- `STOP` −= `continu`, `open`, `verdeling`, `absoluut`, `lengte`, `duale` — six
  words English links book-wide and whose ordinary-language uses are better
  handled by a protect than by keeping the term chapter-local.
- `STOP` keeps `uniform` (already at English's count as a bare adverb),
  `wet`, `normaal`, `gesloten`, `orde`, `exact`, `affien`, `cyclisch`, … .
- `EXTRA` += 30 Dutch forms `WORD_TAIL` cannot generate: the `-e` attributives
  (`continue`, `compacte`, `aftelbare`, `convexe`, `affiene`, `hermitische`,
  `unitaire`, `symmetrische`, `diagonaliseerbare`, `sommeerbare`,
  `samenhangende`, `puntsgewijze`, `uniforme`, `duale`, `onafhankelijke`,
  `voortgebrachte`, …) and the abstract nouns (`continuïteit`, `compactheid`,
  `aftelbaarheid`, `volledigheid`, `sommeerbaarheid`, `samenhang`,
  `differentieerbaarheid`, `onafhankelijkheid`, `barycentra`, `oppervlakten`).
- `EXTRA_PROTECT` += the convex guard extended to the attributive form
  (`convexe functie(s)`), the uniform-law look-ahead, the three arc-length
  phrases English also protects (`pad(en) van lengte`, `lengte van de reeks`,
  `tekst van elke lengte`) and `symmetrische(?= gebeurtenis)`.

One source fix for the same reason: the ch. 5 index key `equivalentie van
normen` → `equivalente normen` at the definition.

Method, for the next translator: dry-run the generator in memory with candidate
config overrides and print every proposed link **with its context** before
applying anything (`--terms` lists the vocabulary; a 40-line probe script over
`tools/termlink/` prints the diffs). Raw counts alone cannot tell an unreachable
inflected form from a deliberate exclusion.

## Why not 100

- **Decimal point kept in all math** (`$0.5$`, `$1.96$`), series-wide across
  EN/FR/NL so the shared `parts/` math is identical; a Dutch reader expects a
  comma.
- **No Dutch babel on this machine** (`dutch.ldf not found`, warning emitted by
  `onemath.sty`): the book builds with `\emergencystretch` and the entry file's
  `\hyphenation{…}` list instead of real Dutch hyphenation patterns, so a few
  paragraphs are looser than they would be on a full TeX Live. Nothing to fix in
  the sources; it will improve by itself once `texlive-lang-european` is
  installed.
- **`\cref` reads as a bare noun** ("volgens \cref{thm:…}"). Dutch tolerates
  this far better than French (no article map needed), but a handful of spots
  would read better with "de stelling in …".
- **Link coverage is 97.8 % of English**, not 100 %: the last two points come
  from prose frequency (Dutch repeats *eigenwaarde* and *norm* less often than
  English repeats "eigenvalue" and "norm") and from `oppervlakte-element`, a
  solid compound whose English two-word counterpart is not linked either. Both
  would need either a shared-rule change or an over-link; neither is worth it.
- **Register in the longest weekend problems** is good written Dutch, yet the
  ≈20-question problems inherit some English sentence architecture (long
  appositive dashes, "In één zin:"). A pass by a Dutch mathematician would
  shorten a few.
- **Index keys are Dutch** (kwadratische vorm, toevalsveranderlijke,
  uitkomstenruimte) — correct, but the EN∩NL index intersection is therefore
  small; noted for the HTML/online-reader export, nothing to fix.

## Pipeline actually used

1. Glossary + register sheet fixed up front (terms, `Zij …`, `Weekendopgave`,
   `Deel I --- …`, solution headers, cross-volume prose), reused verbatim across
   all 46 files.
2. Chapter by chapter: read the English body, write the Dutch body from scratch;
   then the English solutions file → Dutch solutions file. A per-chapter checker
   (label sets, environment census, `exo:`/`pb:` ↔ solution keys, drafty `...`,
   accent escapes, `\end{x>` typos) ran on each pair before moving on.
3. `bash tools/check_translation.sh bachelor-2 nl` on the whole year.
4. `link_defined_terms.py --unwrap --apply` then `--apply`; target-set diff
   against English; two per-target density audits (counts per label EN vs NL,
   then every candidate form read in context in an in-memory dry run before it
   was declared); config curation above; `--check` and
   `sh tools/check_book5_golden.sh` green.
5. `latexmk` build gate; overfull boxes mapped back to their source files by
   walking the log's file stack, then fixed in the prose/table.
6. `pdftotext` spot-reads (front matter, ch. 18 body, solutions header) plus
   sweeps for residual English, accent escapes, `Laat … zijn` calques and
   curriculum/country names.

## Out of scope: reported, then fixed elsewhere

Both shared-file items raised after the first pass have since been fixed by
their owners, and this book was rebuilt on top of them:

- `frontmatter/preface.nl.tex` now reads "expliciet als **aangenomen**
  gemarkeerd" (was the calque "als toegegeven"), matching `\omadmittedtext`.
- The cover prints "26 juli 2026" (Dutch `\today` in `styles/lang/nl.tex`), the
  part titles and `\bookline` read "Bachelorjaar 2", and cleveref's
  conjunctions are Dutch. Verified in the 419-page PDF.

Still open, and not ours to fix: `dutch.ldf` is missing on this machine, so the
build has no Dutch hyphenation patterns (see "Why not 100").
