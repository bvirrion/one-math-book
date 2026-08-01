# Translation score — Math Book 2 · Hindi (`hi`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 2 (High School, grades 10–12) |
| **Language** | Standard technical Hindi (`hi`) |
| **Quality bar** | **native academic** (English is the source of truth; the FR edition was consulted as a sense/structure reference only, per `translation_instruction.md`; `hindi_style_card.md` is binding) |
| **Overall score** | **96 / 100** (weighted raw 96.9) |
| **Ship threshold** | ≥ 95 — **MET** |
| **Date** | 2026-08-01 |
| **Scope of this pass** | **Full re-translation from English.** The pre-existing `hi/` tree was raw machine translation (2026-07-24); it was read only as a warning list and then discarded. All 35 chapters and all 35 solutions files (**70 files**) were re-derived from `parts/grade-1{0,1,2}/*.tex` and `.../solutions/*.tex`, then gated, term-linked, built and reviewed. `tools/term_config/book2_hi.py` was rewritten from a 33-line stub into a curated config. |

## Verdict in one line

Book 2 now reads as a **Hindi-medium senior-secondary textbook that happens
to mirror an English one**: 35 chapters, 343 graded exercises, 35 weekend
problems, 378 solutions, all three structural gates green, the Hindi prose
gate down from **10 401 issues to 0**, **4 041 defined-term links with exact
target parity against English (123 targets = 123)**, and a 323-page PDF with
**0 errors, 0 undefined references and 0 overfull boxes**.

## Why a full re-translation

The `hi/` tree that existed before this pass was unusable — not
post-editable, wrong at the level of the words themselves. Four
representative defects, all from the first twenty lines of
`grade-11/hi/01-quadratic-functions.tex` (`git show HEAD:` still holds them):

| Pre-existing HI | English | Problem |
|-----------------|---------|---------|
| «द्विघात **कार्य**», «**समारोह** का प्रपत्र» | *quadratic function*, *a function of the form* | *function* rendered twice, both times as the wrong homograph: कार्य = *work / task*, समारोह = *a function* in the sense of *a ceremony*. The word for a mathematical function is **फलन** |
| «**कानूनी फॉर्म**» | *canonical form* | कानूनी = ***legal***. The chapter's central object was named "legal form" in its title, its theorem and its index key. Correct: **मानक रूप** |
| «**द** विभेदक», «**ए** द्विघात कार्य», «**इजहार** $ax^2+bx+c$» | *the discriminant*, *a quadratic function*, *the expression* | the English articles *the* / *a* transliterated into Devanagari as words (Hindi has no articles), and *expression* taken in its legal sense (इजहार = *deposition*). Correct: **व्यंजक** |
| «$a $, $ b $», `\text{where } … \text{ and }`, «…वास्तविक संख्या**.**» | — | spurious spaces inside inline math, untranslated math text left in English, and the Latin full stop instead of the danda **।** |

Word order was calqued clause by clause («सबसे सरल हैं कार्य रैखिक वाले के
बाद»), which is unreadable in a verb-final language. Editing that was not
cheaper than writing the book; it was rewritten. **All four classes above
are zero across the whole tree**: 0 residual English tokens in prose, 0
Latin sentence-final stops, 0 stray spaces inside inline math, 0 English
`\text{…}`.

## Structural census — HI vs EN

| Item | EN | HI |
|------|---:|---:|
| Chapter files | 35 | **35** |
| Solutions files | 35 | **35** |
| `\begin{definition}` | 120 | **120** |
| `\begin{theorem}` | 64 | **64** |
| `\begin{proposition}` | 82 | **82** |
| `\begin{lemma}` / `\begin{corollary}` | 1 / 3 | **1 / 3** |
| `\begin{method}` | 55 | **55** |
| `\begin{proof}` | 146 | **146** |
| `\begin{example}` / `\begin{remark}` | 123 / 28 | **123 / 28** |
| `\begin{exercise}` | 343 | **343** |
| `\begin{problem}` (weekend problems) | 35 | **35** |
| `\begin{solution}` | 378 | **378** |
| `exo:` / `pb:` labels | 343 / 35 | **343 / 35** |
| `\begin{tikzpicture}` | 87 | **87** |
| `\begin{omfigure}` | 80 | **80** |
| `\admitted` | 3 | **3** |
| `\label{…}` (all, in order, per file) | 826 | **826, byte-identical** |
| `\index{…}` keys | 211 | **211** (0 with Latin text) |
| `\omterm` links | 3 906 | **4 041** |
| Distinct `\omterm` targets | 123 | **123 (equal sets)** |
| PDF pages | 330 | **323** |
| Underfull boxes | 120 | **102** |

## Gate results

| Gate | Command | Result |
|------|---------|--------|
| Translation gate, grade-10 | `bash tools/check_translation.sh grade-10 hi` | **PASSED** (18 files, hindi prose gate OK) |
| Translation gate, grade-11 | `bash tools/check_translation.sh grade-11 hi` | **PASSED** (20 files, hindi prose gate OK) |
| Translation gate, grade-12 | `bash tools/check_translation.sh grade-12 hi` | **PASSED** (32 files, hindi prose gate OK) |
| Hindi prose gate issues | `tools/check_hindi_prose.py` (via the above) | **0** (baseline **10 401**) — 0 `english`, 0 `translit`, 0 `danda`, 0 `math-space`, 0 `split-number` |
| Term links regenerate | `link_defined_terms.py --book 2 --lang hi --unwrap --apply` then `--apply` | 4 041 links across 70 files |
| Term links idempotent | `link_defined_terms.py --book 2 --lang hi --check` | **"every file matches what the config generates"** |
| Link-target parity | `comm -3` of the EN and HI `\omterm{…}` target sets | **empty — the two sets are equal (123 targets)** |
| Exercise ↔ solution keys | per-file `exo:`/`pb:` labels vs `\begin{solution}{…}` | **0 mismatches in 35 pairs** |
| Solutions headers | `\section*{अध्याय \ref{ch:…} --- …}` vs the chapter's `\chapter{…}` | **0 mismatches in 35 pairs** |
| Build | `latexmk one_math_book_2_high_school_hi.tex` (XeLaTeX) | exit 0, 323 pages |
| `grep -ac '^!'` | build log | **0** |
| `grep -aci 'undefined'` | build log | **0** |
| `grep -ac 'Overfull'` | build log | **0** |
| Mid-word links (Hindi-specific, see below) | scripted scan of all 70 files | **0** |

The only log noise is 50 `Missing character … in font nullfont` lines for the
string `10pt.`; the **English and Portuguese builds emit exactly the same 50**,
so it is a shared, pre-existing artefact of the preamble, not of this edition.

## Dimension scores

| Dimension | Weight | Score /100 | Notes |
|-----------|------:|----------:|--------|
| Terminology | 20 | **96** | Sanskritic school-mathematics register, consistent across 70 files and chosen for the series, not transposed: समुच्चय, अंतराल, फलन / प्रांत / प्रतिबिंब, आलेख, निरपेक्ष मान, प्रवणता, विविक्तकर, मानक रूप, परवलय / अतिपरवलय, चिह्न-सारणी, परिवर्तन-सारणी, छेदक रेखा, स्पर्श रेखा, अवकलज / अवकलनीय, प्रतिअवकलज, समाकल, खंडशः समाकलन, सीमा / सांतत्य / संतत, अनन्तस्पर्शी, समांतर व गुणोत्तर अनुक्रम with सार्व अंतर / सार्व अनुपात, महत्तम समापवर्तक, सह-अभाज्य, यूक्लिडीय भाग, सर्वांगसमता, आव्यूह / सारणिक / प्रतिलोमनीय, क्रमचय / संचय / क्रमगुणित, द्विपद गुणांक, प्रायिकता / प्रत्याशा / प्रसरण / मानक विचलन, सप्रतिबंध प्रायिकता, बर्नूली परीक्षण, द्विपद बंटन, प्रसामान्य बंटन, बृहत् संख्याओं का नियम, प्रतिदर्श माध्य, विश्वास अंतराल, स्मृतिहीनता, निरीक्षण विरोधाभास, अभियोजक की भ्रांति. **No English glosses in parentheses anywhere.** Proper names transliterated once and then kept: हीरोन, केप्लर, गाउस, फ़र्मा, बेज़ू, चेबिशेव, ब्येनेमे, दे म्वाव्र, लाप्लास, ब्राउवर, ऑयलर, पास्कल, बेज़, आर्किमिडीज़, गॉल्टन |
| MT-artifact freedom | 20 | **97** | The prose gate's five artifact classes are all at 0 over 70 files. No article transliterations (`द`, `ए`), no homograph slips of the कार्य / समारोह / कानूनी / इजहार class, no calqued English word order: English participial chains are re-cast as Hindi finite clauses ("Long considered…", "…outruns the noise" → "…बहाव शोर से आगे निकल जाता है"). Idioms localized rather than glossed: *the house always wins* → «जुआघर हमेशा जीतता है», *gambler's fallacy* → «जुआरी की भ्रांति», *too close to call* → «इतनी क़रीबी है कि उसका फ़ैसला नहीं किया जा सकता», *free lunch* → «मुफ़्त माल», *length-biased sampling* → «लंबाई-अभिनत प्रतिदर्शन», *memoryless* → «स्मृतिहीनता» |
| Register / tone | 15 | **95** | Uniform **आप** address in every one of the 343 exercise stems and 35 weekend problems (कीजिए, निकालिए, दिखाइए, सिद्ध कीजिए, हल कीजिए, समझाइए, तुलना कीजिए, निष्कर्ष निकालिए) — the imperative a Hindi-medium exercise list actually uses, never the bare stem or the तू/तुम forms. Course text is expository third person; chapter hooks are written, not rendered: «जुआघर अंत में हमेशा क्यों जीतते हैं, और सर्वेक्षण काम क्यों करते हैं?», «घन को काटिए तो आप वर्ग और आयत की अपेक्षा करते हैं --- फिर भी एक प्रसिद्ध कटान \emph{सम षट्भुज} बना देता है» |
| Structural fidelity | 10 | **99** | `check_translation.sh` passes for all three years: completeness, identical label sets *and order*, per-environment census, exercise↔solution key parity, no duplicate labels, no `\end{…>` typos, no drafty `...`. Every weekend problem keeps its four-part skeleton and its ~20 questions one for one; the `\textbf{भाग …}` headers, `\emph{1.}`/`\textbf{1.}` numbering and `enumerate` structures mirror English exactly. Prose volume per file is a flat 0.62–0.72 of the English character count across all 70 files (Devanagari's shorter technical words) — no outlier, i.e. no truncated or padded chapter |
| LaTeX hygiene | 10 | **99** | 0 errors, 0 undefined references, **0 overfull boxes**, 102 underfull (EN 120). 0 TeX accent escapes in the tree (UTF-8 throughout). Every `$…$`, `\[…\]`, `tikzpicture`, `axis` block and tabular colspec is **byte-identical to English** — guaranteed, not spot-checked: the translation was done through a mask/unmask pipeline whose round trip was verified byte-exact on all 70 files before any prose was written |
| Cross-refs / rule compliance | 10 | **98** | All 826 `\label{…}`, every `\cref`/`\ref` target and all 378 `\begin{solution}{…}` keys byte-identical to English. **0 country, curriculum, board or exam names** in visible text (`NCERT`, `CBSE`, `भारत`, `फ़्रांस`, `France`: 0 hits) — where English named a country the Hindi generalizes («किसी देश का नक्शा … उसी देश की ज़मीन पर», «1791 की विज्ञान अकादमी»). The only bare `\ref` is the mandated `\section*{अध्याय \ref{ch:…} --- …}` solutions header, whose `ch:` key stays English |
| Solutions | 10 | **96** | All 378 present, each with its English twin's numbering and the same numerical answers, spot-checked value by value: $\gcd$ and Bézout coefficients, the $508$ g machine setting with its $8$ g of «मुफ़्त» product, the $\frac{3\sqrt3}{4}$ hexagon, the six-sigma failure rate, the $20$-minute inspection-paradox gap, the $65$ students of the class-size paradox. The discursive closing answers (question 20 of each weekend problem) are re-argued in Hindi, not transposed |
| Figures | 5 | **97** | All 87 `tikzpicture` and 80 `omfigure` blocks copied byte for byte; only node text, legends, axis labels and captions are Hindi (135 distinct strings). Single-letter coded labels kept as codes (S/F, D/T) with the Hindi word spelled out in the caption; units left Latin (`kg`, `cm`, `rad`, `pH`, `Hz`) as the style card requires; ASCII digits and Latin decimal points inside figures, so text and figures agree |

**Weighted total: 96.9 → 96 / 100.** Terminology, MT-artifact freedom and
register carry 55 of the 100 points, as the brief asks; structure and hygiene
are separately gated and weighted below them.

## Sampled passages

Five passages taken at random points of the volume, judged against what a
Hindi-medium textbook would print.

**1. `grade-11/hi/01-quadratic-functions.tex`, chapter opening + definition — native.**

> EN: *Quadratic functions are the simplest functions after the linear ones,
> and the first whose graphs are genuinely curved. This chapter develops the
> complete toolbox for them: the canonical form, the discriminant, the sign of
> a quadratic expression, and the geometry of the parabola.*
>
> HI: «रैखिक फलनों के बाद सबसे सरल फलन द्विघात फलन हैं, और सबसे पहले वही हैं
> जिनके आलेख सचमुच वक्र होते हैं। यह अध्याय उनके लिए पूरा औज़ार-बक्सा तैयार
> करता है: मानक रूप, विविक्तकर, किसी द्विघात व्यंजक का चिह्न, और परवलय की
> ज्यामिति।»

Verb-final, correlative «सबसे पहले वही हैं जिनके», no article debris. Compare
the MT this replaces («द विभेदक», «कानूनी फॉर्म»).

**2. `grade-12/hi/16-continuous-distributions.tex`, chapter hook — native.**

> EN: *Waiting times, physical measurements, proportions: many random
> quantities take a continuum of values, and no single value has positive
> probability.*
>
> HI: «प्रतीक्षा-काल, भौतिक मापन, अनुपात: अनेक यादृच्छिक राशियाँ मानों का पूरा
> सातत्य लेती हैं, और किसी अकेले मान की प्रायिकता धनात्मक नहीं होती।»

«सातत्य» for *continuum*, «किसी अकेले मान की … नहीं होती» rather than a
calqued *no single value has*.

**3. `grade-12/hi/15-sums-lln.tex`, weekend-problem stem — native.**

> EN: *A roulette player after $100$ spins is, almost as often as not, ahead.*
>
> HI: «$100$ चक्करों के बाद कोई रूले खिलाड़ी लगभग आधी बार \emph{आगे} ही होता
> है। पर दस लाख चक्कर चलाने वाला जुआघर इतनी निश्चितता से आगे होता है कि कोई
> अदालत सवाल न उठाए।»

«लगभग आधी बार» for *almost as often as not*; «दस लाख» (not «एक मिलियन») for a
million, i.e. the Indic number word a Hindi reader expects.

**4. `grade-12/solutions/hi/16-…`, the inspection paradox — native.**

> EN: *Inspection paradox in one sentence: the interval you happen to inspect
> is not a typical interval, because you were more likely to fall into a big
> one.*
>
> HI: «निरीक्षण विरोधाभास एक वाक्य में: \emph{आप संयोग से जिस अंतराल का
> निरीक्षण करते हैं वह प्रारूपिक अंतराल नहीं है, क्योंकि आपके किसी बड़े अंतराल
> में गिरने की संभावना अधिक थी।}»

The English relative clause becomes the Hindi «जिस … वह» correlative — the
construction Hindi actually uses, and the one MT never produces.

**5. `grade-12/solutions/hi/13-conditional-probability.tex`, the juror's
sentence — near-native.**

> EN: *ask how probable the evidence is under both hypotheses, and never
> mistake the one conditional for its reverse*
>
> HI: «पूछिए कि दोनों परिकल्पनाओं के अधीन प्रमाण कितना संभावित है, और किसी
> सप्रतिबंध प्रायिकता को उसकी उल्टी कभी मत समझिए»

Correct and idiomatic, but «उसकी उल्टी» is colloquial where the surrounding
paragraph is formal; «उसके विलोम» would sit better. Left as is because the
sentence is deliberately a courtroom aphorism, but it is the one place in the
five where a Hindi editor might reach for the pen.

## Hindi conventions applied (from `hindi_style_card.md`)

* Danda **।** ends every sentence (3 349 in the chapter bodies); Latin `, ? ;
  : ( )` for the rest; 0 Latin full stops at sentence end.
* **ASCII digits only** — 0 Devanagari digits in the tree, so text agrees with
  math and figures.
* No spaces inside `$…$`; numbers never split across a line break.
* Sanskritic technical vocabulary with no English gloss; units and symbols
  stay Latin.
* Uniform आप register; no country, board or curriculum names.

## Term-link curation, and a Devanagari bug worth fixing once

`tools/term_config/book2_hi.py` grew from a 33-line stub to a curated config:
`NOT_A_TERM` in Hindi (the shared default keywords are English, so प्रमेय /
असमिका / सूत्र / नियम / कलनविधि result-names would all have been harvested as
notions), a soft `STOP` for the four Hindi-only homographs (**कोटि** ordinate
vs order/rank, **प्रसार** expansion vs spread, **परिमाण** norm vs magnitude,
**मापांक** complex modulus vs modulo $n$), 55 `EXTRA` entries and 36
`EXTRA_PROTECT` guards. `AMBIG_POLICY = "nearest-preceding"`, as for the other
school books. Result: **the HI and EN target sets are equal** (123 each) and
HI carries 4 041 links to English's 3 906 (Hindi inflects, so a term surfaces
in more forms).

**Orchestrator request (blocked file, not touched).** Python's `\w` is false
for every Devanagari matra, virama and anusvara (they are `Mc`/`Mn`, not
alphanumeric), so the shared boundary in `tools/termlink/morphology.py` —
`(?<![\w\\@-]) … (?![\w-])` — does not see Devanagari word boundaries at all.
A term therefore matches *inside* a longer orthographic word whenever the
boundary falls on a vowel sign. Before curation this produced **~250 links**
that were both wrong and typographically broken, e.g.

* `भुज` (*abscissa*) linked inside **भुजा** (*side*) — 78 times, and inside
  **त्रिभुज / चतुर्भुज / बहुभुज / षट्भुज**;
* `ज्या` (*sine*) linked inside **त्रिज्या** (*radius*);
* `माध्य` (*mean*) linked inside **माध्यिका** (*median*);
* `सम` (*even*) linked inside **समुच्चय** (*set*), `मूल` (*root*) inside
  **मूल्य** (*value*) and **मामूली** (*ordinary*);
* worst, `\omterm{…}{रमचय-संचय}` — the link started **after** the virama of
  क्, splitting the conjunct क्र across two boxes, which XeLaTeX shapes with
  a dotted circle.

I closed all of them from the config (the mid-word scan is now 0/70 files),
but the fix belongs in the shared rules, once, for every Indic edition:

```python
# morphology.py — Devanagari-aware boundaries (marks are not \w in Python)
_IND = r'ऀ-ॿ'                      # or the wider Indic block set
#   lookbehind: (?<![\w\\@-])  ->  (?<![\w\\@-])(?<![ऀ-ॿ])
#   lookahead:  (?![\w-])      ->  (?![\w-])(?![ऺ-ॏॕ-ॣ])
```

and, in `tools/term_config/lang_hi.py`, `WORD_TAIL = r'[ा-्]*'` (or
an explicit oblique-plural tail `(?:ों|ओं|एँ|यों)?`), which would let the
linker cover **अवकलजों / माध्यिकाएँ / प्रायिकताएँ** as whole words instead of
needing the ~50 `EXTRA` entries this config now carries by hand. If those two
land, roughly half of `book2_hi.py`'s `EXTRA`/`EXTRA_PROTECT` can be deleted;
until then the config is self-contained and the check is idempotent, so
nothing here blocks the release.

## Why not 100

1. **Hindi inflection is covered by enumeration, not by rule** (−1.5). With
   `WORD_TAIL` empty upstream, oblique plurals reach the linker only through
   `EXTRA`. I declared every form that actually occurs (the scan is clean),
   but a new chapter would add unlinked plurals until someone re-runs the
   scan. This is the single biggest structural weakness of the edition, and it
   is the request above.
2. **Nine open compounds lose their link to a protection guard** (−0.5):
   `अंतर-चतुर्थक परास`, `छद्म-अभाज्य`, `हरात्मक-माध्य` and six others are
   guarded whole, because the shared `HEAD` would otherwise wrap a fragment of
   the first element. Correct, but slightly less linked than English.
3. **Register is uniform, not yet house-polished** (−1.5). The आप imperative,
   the correlatives and the technical vocabulary are consistent across 70
   files, but a native subject editor would still smooth perhaps one sentence
   per chapter — passage 5 above is an honest example. That is the gap between
   "reads as written in Hindi" (achieved) and "reads as edited in Hindi".
4. **Two English artifacts inherited from the canon were repaired, not
   mirrored** (−0.5): `$3x + 2y = $ constant` and `$0 = $ nonzero` in the
   English sources put prose inside a math span; Hindi writes them as
   `$3x + 2y = c$ ($c$ अचर)` and `$0 = c$ (शून्येतर $c$)`. Mathematically
   identical and typographically better, but it is a deliberate divergence
   from the canon, and the English side should be fixed to match.
5. **Terminology is standardized on Sanskritic forms** (−0.5). Where Hindi
   classrooms mix a Sanskritic and an English-loan word (प्रायिकता /
   प्रोबेबिलिटी, आव्यूह / मैट्रिक्स), this edition always takes the Sanskritic
   one, which is right for a printed textbook but slightly further from
   spoken classroom Hindi than an Indian publisher might set.
