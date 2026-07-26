# Translation score — Math Book 1 · Dutch (`nl`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 1 (Primary / Middle, grades 1–9) |
| **Language** | Dutch (`nl`) |
| **Quality bar** | **native academic** (EN is the source; FR Book 1 as sense/structure reference) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 |
| **Date** | 2026-07-25 |
| **Scope** | Full re-translation from scratch: 71 bodies + 71 solution files rewritten from the English, including the 35 weekend problems and their solutions (grades 6–9), which the previous edition did not have at all |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror (71 + 71); identical label sets and order; 35 `problem` envs ↔ 35 `\begin{solution}{pb:…}`; env/figure census equal to English in all nine grades |
| Terminology | **97** | School Dutch throughout: som/verschil/product/quotiënt, teller/noemer, grootste gemene deler, priemgetal, macht/exponent, vierkantswortel, schuine zijde/rechthoekszijde, middenparallelstelling, zwaartelijn/zwaartepunt, richtingscoëfficiënt, variatiebreedte, harmonisch/meetkundig/rekenkundig gemiddelde. Cross-volume vocabulary matches Books 2–5 NL (relatief priem, volkomen kwadraat, affiene functie, met teruglegging) |
| Register / tone | **96** | Written, not translated: `Zij $a$ en $b$ gehele getallen.` (never "Laat … zijn"), "Merk op dat", "Ga na dat", imperatives in exercise stems (Bereken, Teken, Vul in). Young grades stay concrete and short without baby-talk |
| Hygiene / LaTeX | **99** | 0 errors, 0 undefined refs, 0 overfull boxes, 0 warnings; `enumerate[resume]` preserved; UTF-8 accents only (0 `\'e`-class escapes) |
| Cross-refs | **98** | `\cref`/`\ref` targets untouched; cross-volume references are prose-only ("het bovenbouwvolume") — no country or curriculum name anywhere |
| Figures | **96** | TikZ/pgfplots drawing code byte-identical; only node text and `{\small …}` captions translated; tick-label lists localized (jan/feb/mrt, ma/di/wo, voetbal/zwemmen) |
| Solutions | **97** | Every solution rewritten from the English solution, with Dutch section headers `Hoofdstuk \ref{ch:…} --- <titel>`; all 15-part weekend-problem solutions fully rendered |
| MT-artifact freedom | **96** | No calques left from the old edition (`toegegeven op dit niveau`, `het High School-volume`, `Laat $a$ … zijn`: all gone); a residual-English sweep over the 142 files returns only Dutch words that happen to be spelled like English ones (volume, meter, product) |

**Overall: 96** (weighted toward terminology + register + MT-freedom).

## Structural / build gates

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh grade-1…9 nl` | **PASSED** ×9 |
| `latexmk one_math_book_1_primary_middle_school_nl.tex` | OK |
| Fatal errors (`^!`) | 0 |
| Undefined references | 0 |
| Overfull `\hbox` | 0 |
| LaTeX warnings | 0 |
| PDF | `build/one_math_book_1_primary_middle_school_nl.pdf`, 431 pp (EN 422 pp) |
| `python3 tools/link_defined_terms.py --book 1 --lang nl --check` | every file matches what the config generates (3 915 links) |
| `sh tools/check_book5_golden.sh` | unchanged (shared termlink rules untouched) |

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| G1 `01-counting-to-20` opening + method "Zo tel je" | **native** — knikkers, "sla niets over", "het laatste getal dat je zegt, is het aantal" |
| G1 `04-numbers-to-100` | **native, localized** — explains that Dutch says the units before the tens ("zevenenveertig … precies omgekeerd aan de schrijfwijze"), a remark the English source has no reason to carry |
| G2 `06-time-and-money` | **native, localized** — "half vier" for 3:30, with an explicit note that Dutch names the *next* hour |
| G3 `03-multiplication` opening + definition | **native** — "drie zakjes met zeven knikkers", "de bewerking van het herhaald optellen" |
| G6 `pb:g6:wholes:1` (little Gauss) | **native** — "Koppel eromheen en reken de som uit", "een truc die nooit faalt" |
| G8 `pb:g8:pythagoras:1` (Pythagorean triples) | **native** — "pythagorees drietal", "de machine levert altijd een pythagorees drietal" |
| G9 `pb:g9:sqrt:1` (irrationality of √2) | **native** — "Zit het eerst op de hielen", "het schildlemma", "in eenvoudigste vorm" |
| G9 `09-statistics-and-probability` + solutions | **native** — kansproef, uitkomst, gebeurtenis, boomdiagram, met teruglegging, variatiebreedte |

## Defined-term links (`\omterm`) — target parity vs English

Regenerated with `--unwrap --apply` then `--apply`. Remaining per-grade target-set
divergences, each investigated:

| Divergence | Verdict |
|---|---|
| g2, g3: NL links `ex:g1:subtraction:difference` ("verschil") where EN does not | correct sense; Dutch prose names the difference |
| g3, g4: EN links `def:g2:shapes:solids` ("faces the bigger number", "Butterflies, faces, snowflakes") | English homonym over-link; Dutch has no homonym — NL is right |
| g6, g7: EN links `def:g5:solids:net` on "net change / net loss" | same class of English homonym over-link; NL says "netto" |
| g4, g7: NL links `def:g2:measure:units` ("massa's", "inhouden") | correct sense |
| g4: EN links `def:g4:numbers:classes` ("classes") | the Dutch definition names them "groepen (van drie)"; linking the ordinary noun *groep* would flood the book — deliberate non-link |
| g6–g9: EN `def:g4:numbers:round` vs NL `def:g6:decimals:rounding` | one Dutch verb *afronden* covers English *round* (g4) and *rounding* (g6); `AMBIG_POLICY = nearest-preceding` resolves it to the grade-6 definition from grade 6 on — the correct target for a Dutch reader |
| g7: NL `def:g6:decimals:places` where EN has `def:g6:decimals:rounding` | different sentence wording ("als decimaal getal schrijven"); correct sense |
| g9: EN `def:g7:prop:scale`, `def:g8:fractions:inverse` | *schaal* and *omgekeerde* are `STOP`-listed in `book1_nl.py` (both are ordinary Dutch here, and *de omgekeerde* is the converse of a theorem in most of its uses); `SOFT` keeps them linked inside their own chapters |
| g9: NL links `def:g7:negatives:def` ("tegengestelde") | correct sense |

Config deltas made during this pass (`tools/term_config/book1_nl.py`, comments in
the file explain each):

- `STOP`/`SOFT` += `aantal` — it was linking "het aantal negatieve factoren" to the
  statistics count of grade 7; ordinary Dutch everywhere except that chapter.
- `EXTRA_PROTECT`: the "even + adjective" guard now also matches the inflected
  adjective (`even lange stukken`, `even waarschijnlijke uitkomsten`, `even grote
  strook`), which was linking the adverb *even* to the even/odd definition.
- `DERIVED` documented as deliberately empty (a participle entry could not fire on
  an ambiguous base).

Two prose fixes were made for the same reason: "het meetkundige/harmonische
gemiddelde" → the fixed uninflected term forms, and a rate-of-change "snelheid"
reworded to "tempo" so it stops pointing at the average-speed definition.

## Why not 100

- **Decimal point kept in all math** (`$4.362$`, `$1.5$ h`, `$0.7$ m`). Dutch
  writes a decimal comma; the series keeps the point in every language (EN/FR/ES/
  PT/NL) so that the shared `parts/` math is identical. Grade 4 carries one added
  clarifying sentence ("Dit boek zet als decimaalteken een punt, zoals
  internationaal gebruikelijk is; je spreekt het uit als ``komma''…"), but a Dutch
  pupil still reads unfamiliar notation throughout.
- **Thousands separators and units follow the English source** (`10\,201`,
  `$5 \times 10^{-2}$ g), which is fine but not specifically Dutch practice.
- **Register in the longest weekend problems** is good written Dutch, yet the
  15-part problems inherit English sentence architecture in places (long
  appositive dashes, "In één zin:"). A pass by a Dutch teacher would shorten some
  of them.
- **`\cref` reads as a bare noun** ("volgens \cref{thm:…}"); Dutch tolerates this
  better than French (no article map needed), but a few spots would read better
  with "de stelling in …".
- **Index keys are Dutch** (quotiënt, priemgetal, variatiebreedte) — correct, but
  the EN∩NL index intersection is therefore small; nothing to fix, noted for the
  HTML/online-reader export.

## Pipeline actually used

1. Glossary + register sheet fixed up front (terms, `Zij …`, `Weekendopgave`,
   `Deel I --- …`, solution headers), reused verbatim across all 142 files.
2. Grade by grade: delete the stale NL file, read the English body, write the
   Dutch body; then the English solutions file → Dutch solutions file.
3. `bash tools/check_translation.sh grade-N nl` after each grade; every reported
   class fixed before moving on (drafty `...` in pgfplots ticks expanded to
   explicit lists, Dutch index keys, accent escapes).
4. Shared string fix: `\omadmittedtext` in `styles/lang/nl.tex` →
   "Op dit niveau zonder bewijs aangenomen." (NL Books 2–5 pick it up on their
   next build).
5. `link_defined_terms.py --unwrap --apply` then `--apply`; per-grade target-set
   diff against English; config curation above; `--check` and the Book 5 golden
   check green.
6. `latexmk` build gate, `pdftotext` spot-reads of a young chapter and two weekend
   problems, residual-English / accent / curriculum-name sweeps.
