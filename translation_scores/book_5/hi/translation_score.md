# Translation score — Math Book 5 · Hindi (`hi`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 5 (University Year 3, `bachelor-3`) |
| **Language** | Hindi (`hi`), standard technical Hindi as fixed by `hindi_style_card.md` |
| **Quality bar** | **native academic** — a Hindi-medium third-year lecture course. English is the source of truth for content; the FR and PT Book 5 editions were consulted only as intra-series references for how far a translation of *this* book may depart from English clause order |
| **Overall score** | **97 / 100** (was 96 before revision 2) |
| **Ship threshold** | ≥ 95 — **met** |
| **Date** | 2026-08-01 (revision 2, same day) |
| **Scope of this pass** | The book is now **fully re-translated from the English canon**. 43 of the 46 bodies were re-derived by the previous agent before it was interrupted; pass 1 re-translated the last three solution files (ch. 21, 22, 23) from English, cleared the last overfull box, swept what it could see of the residual English out of `\text{…}` inside protected math, and **rewrote `tools/term_config/book5_hi.py` from scratch** (83 lines of stale machine-translation vocabulary → a curated config mirroring `book5_en.py` word for word). **Revision 2** (below) closed the blind spot that pass-1 audit had only sampled: **168 text-macro arguments carrying 235 English word tokens**, across 37 of the 46 files |

## Verdict in one line

A complete, structurally exact, natively written Hindi third-year course:
722 labels and 299 solutions identical to English in set *and* order, index
keys 100 % Devanagari (EN ∩ HI intersection = **0 of 307**), a link layer at
**95.1 %** of English's volume on **129 of English's 130 targets** — and the
single divergence is one English target whose 23 links are, on inspection,
23 wrong-sense links.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| **Register / tone** | **96** | University lecture Hindi throughout: `मान लीजिए`, `सिद्ध कीजिए`, `दर्शाइए`, `निष्कर्ष निकालिए`, `इससे यह निष्कर्ष निकलता है कि`, `तभी और केवल तभी जब`, `अतः / इसलिए / जिससे / जबकि / फलस्वरूप` as connectives. Statement stems agree with `styles/lang/hi.tex` (प्रमेय / प्रतिज्ञप्ति / प्रमेयिका / उपप्रमेय / उपपत्ति). Exercise stems are imperative (`परिकलित कीजिए`, `दर्शाइए`, `जाँचिए`, `निकालिए`), solutions declarative. No `आप`-register school voice anywhere |
| **Terminology** | **97** | Third-year vocabulary is consistent across all nine subject areas and matches the style card: समुच्चय, प्रतिचित्रण, एकैकी / आच्छादक, वलय / क्षेत्र / आदर्श, मॉड्यूल, अखंडनीय, समाकारिता / तुल्याकारिता, संस्थिति / संहत / संबद्ध / सघन / संवृति, माप / मापनीय / लगभग सर्वत्र, समाकल / समाकलनीय, समविश्लेषिक / अवशेष / एकलता, उपबहुविध / अवकल रूप / बाह्य गुणन / प्रत्यानयन / अभिविन्यास / परिसीमा, प्रायिकता / यादृच्छिक चर / प्रत्याशा / प्रसरण / अभिलक्षणिक फलन / गाउसीय. **No MT sense swap survives**: the whole tree is clean of सेट, मानचित्र, अलगाव, समानक, लेम्मा, बानाच, स्पेस, निरंतरता, ऑपरेटर, कर्नेल, इंटीग्रल, लेबेस्गे, लिप्सचिट्ज़ |
| **MT-artifact freedom** | **98** (was 96) | `check_hindi_prose.py` **OK on all 46 files** under the *tightened* gate (0 english / 0 translit / 0 danda / 0 math-space / 0 split-number), which now reads `\text{…}` arguments out of math and also flags short words (`so`, `in`, `of`, `on`, `if`, `and`, `the`, `for`, …) and dotted abbreviations (`i.e.`, `e.g.`). The 20 803 issues of the 2026-07 baseline are gone. Pass 1 hand-audited 19 in-math strings; **revision 2 found and translated 168 text-macro arguments (235 English word tokens) in 37 files** — see the revision section |
| **Structural fidelity** | **99** | Exact mirror: 23 chapters + 23 solution files; **722 `\label`s identical to English in set and order**; 299 `exo:`/`pb:` labels ↔ 299 `\begin{solution}{…}` keys, byte-identical on both sides, checked chapter by chapter; environment census equal to English for all 14 gated environments (88 definitions, 145 theorems, 219 proofs, 276 exercises, 23 problems, 15 `tikzpicture`, 15 `omfigure`, …). `check_translation.sh bachelor-3 hi` **PASSED** |
| **LaTeX hygiene** | **98** | 0 fatal errors, 0 undefined references, **0 overfull boxes**, 0 underfull `\vbox` from `\output`. 0 TeX accent escapes, 0 zero-width characters, no `\end{proof>` typo class, no duplicate labels, no drafty `...` in prose |
| **Cross-refs / rule compliance** | **99** | `\label`, `\cref`/`\ref` targets, `\begin{solution}{key}` and every `\omterm` **first** argument byte-identical to English. Hindi needs no article before a `\cref`, so the FR/NL article-tie problem does not arise. Zero country, board or curriculum names in visible text; cross-volume references are prose-only (`दूसरे वर्ष के खंड में`) |
| **Solutions** | **97** | All 299 solutions present, complete and natively written, with localized `\section*{अध्याय \ref{ch:…} --- <title>}` headers whose `ch:…` slugs are unchanged. Solution-side link volume 1 507 vs English 1 581 (95.3 %) |
| **Figures** | **98** | All 15 `tikzpicture`s and 15 `omfigure`s present; drawing code (coordinates, options, styles) untouched, only `node {…}` text and captions localized — e.g. ch. 21's outward-normal figure reads `प्रेरित`, `परिसीमा`, `बहिर्मुखी-अभिलंब-पहले नियम` |
| **Term links** | **95** | **4 113 links** across 46 files (EN 4 326 → 95.1 %), on **129 of English's 130 targets**. Idempotent: `--unwrap --apply` → `--apply` inserts 0 → `--check` reports every file matching what the config generates. `check_book5_golden.sh` (the English-side regression fixture) still passes |

**Overall: 97** — weighted toward register + terminology + MT-artifact
freedom, since structure is already gated mechanically by
`check_translation.sh`, the label/solution-key diffs and the environment
census. The single point comes from MT-artifact freedom: the book no
longer prints English anywhere a reader looks, and that is now *gated*
rather than asserted.

## Revision 2 — `\text{…}` inside math, swept to zero

**The blind spot.** `check_hindi_prose.py` blanked every math span before
scanning, so the argument of `\text{…}` — text the reader sees, set in the
body font, inside `$…$`, `\[…\]`, `align*`, `cases`, `substack` and
sub/superscripts — was invisible to it. `translation_instruction.md`
requires `\text{…}` to be translated and `hindi_style_card.md` says
everything a reader sees must be Hindi, but nothing enforced it. Pass 1
audited the class by hand and found 19; a hand audit of a 390-page book
does not find them all. The orchestrator then taught the gate to extract
`\text`, `\textrm`, `\textbf`, `\textit`, `\textsf`, `\textnormal`, `\mbox`
and `\hbox` arguments out of math and scan them (`\operatorname` and
`\mathrm` stay excluded — their arguments are operator names such as
`sin`, `det`, `d`, which stay Latin), and later to stop skipping words
shorter than three letters and to catch dotted abbreviations.

**What was found and fixed.** Under the tightened gate Book 5 reported
**236 hits in 36 files** — the worst of the six books. In source terms
that is **168 text-macro arguments carrying 235 English word tokens, in 37
of the 46 files**. All 168 were translated. The gate now reads
`hindi prose gate: OK (46 files)`.

Representative before → after:

| Before | After |
|---|---|
| `\text{divides } \abs G` | `\text{जो } \abs G \text{ का भाजक है}` |
| `\text{one point per orbit}` | `\text{प्रति कक्षा एक बिंदु}` |
| `\text{Euclidean} \Rightarrow \text{principal} \Rightarrow \text{factorial (UFD)}` | `\text{यूक्लिडीय} \Rightarrow \text{मुख्य} \Rightarrow \text{गुणनखंडनीय (UFD)}` |
| `\text{for every Borel } A \subseteq U` | `\text{प्रत्येक बोरेल } A \subseteq U \text{ के लिए}` |
| `\text{ellipsoid with semi-axes } a_i` | `\text{अर्ध-अक्षों } a_i \text{ वाला दीर्घवृत्ताभ}` |
| `\sum_{n \text{ odd}}`, `\sum_{k \text{ even}}` | `\sum_{n \text{ विषम}}`, `\sum_{k \text{ सम}}` |
| `\{\text{Borel null}\} \subsetneq \{\text{Lebesgue null}\}` | `\{\text{बोरेल-अकिंचन}\} \subsetneq \{\text{लेबेग-अकिंचन}\}` |
| `\deg(\text{denominator}) \geq \deg(\text{numerator}) + 2` | `\deg(\text{हर}) \geq \deg(\text{अंश}) + 2` |
| `\text{primitive } \tfrac{(z-a)^{n+1}}{n+1}` | `\text{आद्यंतर } \tfrac{(z-a)^{n+1}}{n+1}` |
| `\text{LHS} \sim \lambda^{-d-d/r}` | `\text{बायाँ पक्ष} \sim \lambda^{-d-d/r}` |
| `\text{(a)}\ \lim`, `\text{(b)}`, `\text{(c)}` | `\text{(क)}`, `\text{(ख)}`, `\text{(ग)}` — the surrounding hint already said (क)/(ख)/(ग) |
| `\qquad\text{i.e.}\qquad` (6×) | `\qquad\text{अर्थात्}\qquad` |
| `\text{a.e.}`, `\text{ a.e.\ on }` | `\text{लगभग सर्वत्र}`, `\text{ पर लगभग सर्वत्र}` |

**Word order.** Hindi has no prepositions, so a word-for-word substitution
of `\text{on } I` gives `में`/`पर` in front of its object — English word
order in Devanagari. Where that happened the **text macro moved to the
other side of the operand and the mathematics stayed byte-identical**:
`f(z) = \sum c_n(z-a)^n \quad\text{on } D(a,R)` became
`\quad D(a,R) \text{ पर}`; `\quad\text{in } L^2` became
`\quad L^2 \text{ में}`; `\text{for all } v \in H` became
`\text{प्रत्येक } v \in H \text{ के लिए}`. No formula, `\label`, `\cref`
target, `\begin{solution}{key}` or `\omterm` first argument was touched,
and `\quad`/`\qquad` spacing was preserved throughout.

**Deliberately left Latin.**

- `UFD` in `\text{गुणनखंडनीय (UFD)}` — an acronym the chapter also prints in
  its own definition list, alongside `PID`; the Hindi text around it reads
  `मुख्य आदर्श प्रांत`, and the parenthesis is the standard label, not prose.
- Roman part numerals in the weekend-problem headers
  (`\textbf{भाग IV --- उपसंहार।}`) — numbering, identical in all six
  language editions.
- Single-letter and symbol-shaped arguments generally (`\mathrm{id}`,
  `\operatorname{Fix}`, `\operatorname{Res}`, `\mathrm{LIM}`) — symbols, not
  words, and `\operatorname`/`\mathrm` are outside the gate by design.
- `\text{\emph{…}}` / `\text{\cref{…}}` wrappers keep their macro names, of
  course; the only remaining Latin inside a `\text{}` in the whole tree is
  `UFD`, `\emph`, and two `\cref` targets.

**Score movement: 96 → 97.** MT-artifact freedom moves 96 → 98. The book
previously *claimed* zero visible English on the strength of a sample; it
now *has* zero visible English under a gate that reads the class that was
hiding. Nothing else moved: no prose outside math was rewritten, the link
layer regenerated to the same 4 113 links, and the build is unchanged at
390 pp.

**Gates after revision 2** (all re-run):

| Gate | Result |
|------|--------|
| `python3 tools/check_hindi_prose.py --quiet parts/bachelor-3/{hi,solutions/hi}` | **OK (46 files)** — 0 issues |
| `bash tools/check_translation.sh bachelor-3 hi` | **TRANSLATION GATE: PASSED** |
| `link_defined_terms.py --book 5 --lang hi --unwrap --apply` → `--apply` → `--check` | 4 113 removed, 4 113 inserted, **CHECK: every file matches what the config generates** |
| `sh tools/check_book5_golden.sh` | **PASSED** — English sources byte-identical |
| `latexmk one_math_book_5_university_year_3_hi.tex` | exit 0 |
| Fatal errors / undefined / **Overfull** | **0 / 0 / 0** |
| `Missing character … nullfont` | 10 — the same preamble artifact as every other edition |
| PDF | 390 pp, unchanged |

No new overfull box appeared: the Hindi replacements are on average
slightly narrower than the English they replaced, and the two that grew
(`\text{प्रत्येक परिबद्ध संतत }`, `\text{अर्ध-अक्षों } a_i \text{ वाला
दीर्घवृत्ताभ}`) sit in displays with slack.

## What was sampled, and how

The 43 files this agent did not write were **read, not assumed**. Sampled
before scoring:

* **Chapter openings** — ch. 9 (measure theory), ch. 13 (Hilbert spaces),
  ch. 18 (conformal geometry), ch. 21 (differential forms), ch. 22
  (probability), ch. 23 (characteristic functions).
* **Definitions and statements** — `def:b3:groups:normal` and
  `thm:b3:groups:quotient` (ch. 1), `def:b3:measure:sigmaalgebra` (ch. 9),
  the whole of ch. 21 (both sections of alternating multilinear algebra,
  Poincaré, orientation, Stokes, winding number).
* **Proofs** — ch. 21's Poincaré-lemma homotopy computation and the
  half-space Stokes lemma, ch. 1's quotient-group theorem, ch. 4's
  separability proposition.
* **Exercise stems** — ch. 16 (holomorphic functions) exercises 1–3, ch. 21
  exercises 1–12 and the 25-question weekend problem, ch. 22 exercises 1–12,
  ch. 23 exercises 1–12 and the 25-question weekend problem.
* **Solution headers and solution prose** — ch. 5 (representations), ch. 12
  ($L^p$), ch. 20 (submanifolds), ch. 8 (Banach), plus the three files
  re-translated here.
* **Machine audits over all 46 files** — index-key intersection with English,
  a forbidden-MT-relic sweep, an env/label/solution-key census, a per-target
  and per-file link-count diff against English, and a length ratio.

**Length ratio HI : EN = 1.01** (1 701 917 characters against 1 686 554) —
Devanagari is denser per character than Latin, so a *padded* Hindi rendering
would come out well above 1.0. It does not; the prose matches English
sentence for sentence, and the PDF is **390 pp** against English's 395
(FR 404, PT 411, NL 417, ES 418).

## Structural / build gates (run 2026-08-01)

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-3 hi` | **PASSED** (includes gate 7, the Devanagari prose gate) |
| `python3 tools/check_hindi_prose.py parts/bachelor-3/{hi,solutions/hi}` | **OK (46 files)** — 0 issues in all five classes |
| `python3 tools/link_defined_terms.py --book 5 --lang hi --check` | **PASSED**, and idempotent (`--unwrap --apply` → `--apply` inserts 0) |
| `sh tools/check_book5_golden.sh` | **PASSED** — "every file matches what the config generates"; the English sources were never touched |
| `latexmk one_math_book_5_university_year_3_hi.tex` (XeLaTeX) | exit 0 |
| Fatal errors (`grep -ac '^!'`) | **0** |
| Undefined references (`grep -aci 'undefined'`) | **0** |
| Overfull `\hbox` (`grep -ac 'Overfull'`) | **0** |
| Underfull `\vbox` from `\output` | 0 |
| `Missing character … nullfont` | 10 — the same 10 as the English, French, Spanish and Portuguese builds; a preamble artifact, not Hindi-specific |
| PDF | `build/one_math_book_5_university_year_3_hi.pdf`, **390 pp** (EN 395, FR 404, PT 411, NL 417, ES 418) |
| `\omterm` **target parity** vs English | **129 / 130**; `set(HI) − set(EN)` is **empty**. The one absentee is analysed below |
| Term links | **4 113** across 46 files (EN 4 326 → **95.1 %**); chapters 2 606 / 2 745 (94.9 %), solutions 1 507 / 1 581 (95.3 %) |
| Per-file link ratio | every one of the 46 files between **76 %** and **129 %** of its English twin; no file collapsed |
| Exercise ↔ solution parity | 299 / 299 both sides, key by key, checked chapter by chapter |
| `\label` set and order | identical to English (722) |
| Environment census (14 kinds) | identical to English, file by file |
| Duplicate labels | none |
| `\end{proof>` typo class | none |
| Drafty `...` in prose | none |
| TeX accent escapes / zero-width characters | **0** / **0** |
| `\index` keys | 307 EN, 307 HI, **intersection 0** — every visible term and every index key is Devanagari |
| Country / curriculum names in visible text | none |

## What this pass changed

### 1. The last three solution files, re-translated from English

`parts/bachelor-3/solutions/hi/{21-differential-forms, 22-probability-foundations,
23-clt-gaussian}.tex` were still the 2026-07-24 machine translation
(*"बार-बार कारकों का विस्तार और हत्या"* — "expansion and **murder** of
repeated factors" — for "Expanding and killing repeated factors"; 563
MT-injected spaces inside inline math in ch. 22 alone; 79 Latin full stops;
86 transliterated function words). All three were rewritten against the
English canon, **not** post-edited: the existing Hindi was read once as a
warning list and then discarded.

Each was written after reading its own chapter in Hindi first, so the
terminology is the chapter's own — प्रत्याकर्षण for *retraction*,
गोला / गोलक for *ball* / *sphere*, आद्यंतर for *primitive*, इकाई विभाजन for
*partition of unity*, संकर for *hybrid*, अदला-बदली for *swap*, कुल विचरण for
*total variation*, गुट for *coalition*, कर्तन for *truncation*, अभिलेख for
*records*, लड़ी for *runs*, त्रुटि-दंड for *error bar*.

Solution keys are byte-identical to English by construction, and every
`\begin{solution}{…}` was diffed against its exercise labels after writing.

### 2. The overfull box

The single remaining overfull box was a *display* (1.68655 pt, ch. 14
solutions, line 281), and it was Hindi-specific for a reason worth recording:
the Hindi editions build with **XeLaTeX**, where `\qquad` inside a display
takes its `em` from Noto Sans Devanagari rather than from Latin Modern, so a
`\qquad`-joined two-part display that fits in the English, French and Spanish
builds overflows here by under 2 pt. The formula was split into a `gather*`
at the `\qquad`, changing no mathematics and no environment the census gates
(`gather*` is not one of them). The book now reports **0 overfull boxes** —
the only Book 5 edition that does, alongside English, French and Spanish
(NL and PT ship 5 each).

### 3. `tools/term_config/book5_hi.py`, rewritten

The previous config was 83 lines of the machine translation's own vocabulary
— `"विभेदक रूप"`, `"मॉड्यूल"`, `"स्वयं adjoint"`, `"आत्म adjointness"`,
`"लेबेस्गे माप"`, `"स्पर्शरेखा अंतरिक्ष"`, `"सीमा के साथ सबमैनिफोल्ड"`,
`"बोरेल--कैंटेली लेम्मास"` — none of which occurs anywhere in the
re-translated tree, and it declared `DROP = set(STOP)`, which hard-drops every
stoplisted word everywhere and destroys the soft, chapter-local linking that
`STOP` exists to provide.

The replacement is built on one principle: **mirror `book5_en.py` word for
word**. English's config is almost empty — it stops the ordinary words and the
words whose sense changes by chapter, marks six of them `PRIMARY_OK`, and lets
the harvest do the rest. So:

* **`STOP` (41 entries)** — each one the Hindi rendering of a `book5_en.STOP`
  entry, with the English word in a comment on the line: प्रत्यक्ष *direct*,
  सरल *simple*, स्थायी *stable*, सूचकांक *index*, सघन *dense*, प्रसामान्य
  *normal*, महत्तम *maximal*, मूलक *radical*, अंतर्वस्तु *content*, क्रिया
  *action*, आधार *basis*, घात *degree*, मुक्त *free*, यूक्लिडीय *Euclidean*,
  वियोज्य *separable*, संवृत *closed*, यथार्थ *exact*, संहत *compact*, अभाज्य
  *prime*, अखंडनीय *irreducible*, गुणन / गुणनफल *product*, भागफल *quotient*,
  पथ *path*, परिसीमा *boundary*, अंतःभाग *interior*, … plus **one homograph
  Hindi has where English has two words**: सीमा, which is both *limit* and
  *boundary* (the book writes परिसीमा for the boundary, but plain सीमा is the
  ordinary word for a limit and for केंद्रीय सीमा प्रमेय).
* **`PRIMARY_OK` (6)** — the Hindi of English's *compact, closed, path,
  boundary, interior, irreducible*, item for item.
* **`NOT_A_TERM` (9)** — the Hindi statement-name heads
  (प्रमेय — which also catches प्रमेयिका and उपप्रमेय — प्रतिज्ञप्ति, असमिका,
  सूत्र, कसौटी, सिद्धांत, सर्वसमिका, विरोधाभास, समस्या). Bare **नियम** is
  deliberately *not* listed: English blocks bare *rule* but only the phrase
  *law of*, because *tower law* and *zero--one law* are names it links; Hindi
  spells all three with नियम, so listing it costs two of English's targets.
  It is stoplisted instead — which is soft — and the one Hindi rule-name that
  then slips through is named in `DROP`.
* **`EXTRA` (17)** — two classes only, and nothing else. **Surface forms the
  harvest cannot reach**: the oblique plurals Hindi forms with -ओं
  (अवकल रूपों, प्रारंभिक भाजकों), the short form prose prefers over the index
  key (इकाई विभाजन against `\index{इकाई का विभाजन}`), the hyphenated negation
  मरोड़-मुक्त for *torsion-free* (the hyphen ends the word for the boundary
  rule, so मरोड़ never reaches it), and the one phrase that disambiguates a
  word too generic to declare bare (प्रवाह प्रतिचित्रण, since bare प्रवाह is also
  fluid flow in ch. 18 and heat flow in ch. 14). And **the
  abstract nouns English gets free from `DERIVED`**: सांतत्य, समसांतत्य,
  संबद्धता, पथ-संबद्धता, पूर्णता, मापनीयता, समाकलनीयता, समविश्लेषिकता,
  विलेयता, स्वसंलग्नता, अभिविन्यासनीय. English derives *continuity* from
  *continuous* by suffix; Hindi forms सांतत्य from संतत by a different stem, and
  no rule in `tools/termlink/morphology.py` reaches it. This block alone is
  worth **+292 links** (3 808 → 4 100, before the last two `EXTRA` entries
  took it to 4 113).
* **`DROP` (1)** — महत्तम समापवर्तक, which reached `lem:b3:rings:bezout`; English
  does not link the gcd. It carries the target it would have reached in a
  comment, so the parity argument is auditable line by line. `DROP` is
  emphatically **not** `set(STOP)` any more.
* **`AMBIG_POLICY = "drop"`**, deliberately, as for every university book.
* **`EXTRA_PROTECT` (1)** — `पूर्ण\s+(?:\(?पारस्परिक\)?\s+)?स्वातंत्र्य`, the
  *full (mutual) independence* of ch. 22, where पूर्ण means plain *full* and not
  the *complete* of ch. 7. Audited against the four documented silent-failure
  rules (consumes no `$`; no literal space, so it still matches across a line
  break under `re.S`; checked on unwrapped source; verified live by a moved
  number — 4 125 links with `EXTRA_PROTECT = []`, 4 113 with it) **and against
  a fifth rule this pass had to learn**: the pattern must be idempotent under
  its own output. The narrower lookahead form
  `पूर्ण(?=\s+…स्वातंत्र्य)` — which would have masked only पूर्ण and left
  English's स्वातंत्र्य link standing — stops matching the moment स्वातंत्र्य is
  wrapped, so a second `--apply` inserted 6 links that `--check` then reported
  as stale. The consuming form costs 6 correct links to buy back 6 wrong ones
  and is stable. That failure mode is recorded in the config's own comment.

**Measured effect of the rewrite: 4 225 → 4 113 links, targets 129 → 129, but
the six spurious Hindi-only targets are gone** and one English target was
recovered. Before: Hindi linked `thm:b3:lp:holder`, `thm:b3:lp:minkowski`,
`thm:b3:lp:young`, `met:b3:lp:toolkit`, `pb:b3:lp:1` (five named
*inequalities* — होल्डर की असमिका, मिन्कोव्स्की की असमिका, यंग की असमिका,
येंसन की असमिका, हार्डी की असमिका) and `lem:b3:rings:bezout`, none of which
English links, while missing seven English targets. After: **zero
Hindi-only targets**, and six of the seven missing English targets restored.

### 4. Residual English inside protected math

`check_hindi_prose.py` blanks math before scanning, by design — so
`\text{…}` strings inside `$…$`, `\[…\]` and `align*` are invisible to it and
survive every gate while a reader sees them. An audit of the whole tree found
19 and translated them, in the three files written here and in seven of the
files written earlier (ch. 4, 9, 21, 22, 23 and solutions 10, 17). This is
the class the PT edition found 216 of; Hindi had far fewer because the
previous agent had already been careful, but not zero.

**Superseded by revision 2.** This hand audit sampled the class; it did not
exhaust it. 168 more were still there, and are gone now — see
*Revision 2* above.

## Samples

**1 — chapter opening, ch. 9 (measure theory).** *Not written by this agent.*

> $\R$ का कोई उपसमुच्चय कितना लंबा होता है? भोला उत्तर --- प्रत्येक
> समुच्चय को अंतरालों की लंबाई का विस्तार करने वाली कोई
> स्थानांतरण-अपरिवर्ती लंबाई सौंप देना --- \emph{असंभव} है: इस अध्याय के
> अंत में विटाली की रचना एक ऐसा समुच्चय बना देती है जिसकी कोई संगत लंबाई
> नहीं। माप सिद्धांत अनुशासित पीछे हटना है: हम अपना ध्यान \emph{मापनीय}
> समुच्चयों के एक समृद्ध वर्ग तक सीमित कर लेते हैं, जिस पर गणनीय रूप से
> योज्य लंबाई विद्यमान है और अद्वितीय भी।

*Verdict: **native**.* Rhetorical question, em-dash aside, colon-and-gloss —
the cadence of a Hindi-medium university text. *अनुशासित पीछे हटना* for "the
disciplined retreat" is an idiomatic choice, not a calque; *गणनीय रूप से
योज्य* is the standard term (the MT wrote *गणना* for countability).

**2 — statement, ch. 1 (quotient group).** *Not written by this agent.*

> मान लीजिए $N \trianglelefteq G$। सहसमुच्चयों का समुच्चय $G/N$, गुणन
> $(gN)(hN) = ghN$ के साथ, एक सुपरिभाषित समूह है --- \emph{भागफल समूह}
> --- और \emph{विहित प्रक्षेप} $\pi \colon G \to G/N$ एक आच्छादक
> समाकारिता है जिसकी अष्टि $N$ है। विलोमतः, किसी भी समूह समाकारिता की
> अष्टि प्रसामान्य होती है: प्रसामान्य उपसमूह ठीक अष्टियाँ ही हैं।

*Verdict: **native**.* `मान लीजिए` opening, `सुपरिभाषित`, `विहित प्रक्षेप`,
`आच्छादक समाकारिता`, `अष्टि` (kernel) — and the closing appositive
*ठीक अष्टियाँ ही हैं* reads as written, not rendered.

**3 — solutions, ch. 12 ($L^p$).** *Not written by this agent.*

> \cref{thm:b3:lp:holder} में $p = q = 2$: … --- अर्थात् कोशी--श्वार्ज़,
> जिसमें बराबरी तभी और केवल तभी जब $\abs f, \abs g$ समानुपाती हों और कलाएँ
> संरेखित। … उत्तल $\Phi(t) = \abs t^{q/p}$ के साथ येंसन को फलन $\abs f^p$
> पर लगाइए।

*Verdict: **native**.* *तभी और केवल तभी जब* + subjunctive, the elliptical
*और कलाएँ संरेखित* (no repeated verb) — exactly how a Hindi solutions manual
compresses an equality case.

**4 — solutions, ch. 21 (Brouwer, question 5).** *Written in this pass.*

> हम गोलक पर $r^*\sigma$ का समाकलन करेंगे और उसे दो प्रकार से गिनेंगे।
> चूँकि $r$ $S$ को बिंदुशः स्थिर रखता है, इसलिए वह समाकल
> $\int_S\sigma = n\operatorname{vol}(\bar B) \neq 0$ के बराबर है। … एक ही
> संख्या, दो मान: अतः वह प्रत्याकर्षण हो ही नहीं सकता।

*Verdict: **native**.* `चूँकि … इसलिए` for the causal pair, `बिंदुशः`, and the
verdict sentence *एक ही संख्या, दो मान* — a nominal sentence with no verb,
which is how Hindi closes a contradiction.

**5 — solutions, ch. 23 (Le Cam, closing paragraph).** *Written in this pass.*

> वही संकर, वही दूरबीन, भिन्न स्थानीय आकलन: प्रतिस्थापन कोई प्रमेय नहीं, एक
> रणनीति है, और गाउसीय तथा प्वासों सीमाएँ उसके दो सबसे पुराने लाभांश हैं।

*Verdict: **native**.* Three-part nominal parallelism, the *कोई … नहीं, एक …
है* correction pattern, and *लाभांश* for the book's recurring "dividends" —
the same word the chapter's own Part V heading uses.

## Why not 100

Ordered by cost to the reader.

1. **`prop:b3:galois:perfect` — 23 English links Hindi does not make.** This
   is the one target-parity divergence, and it is deliberate. English defines
   *perfect field* with `\emph{perfect}\index{perfect field}`, so the bare word
   *perfect* becomes linkable and then fires on every ordinary use of the
   adjective: 9 links in ch. 6's *perfect compact sets* (a topological notion
   with nothing to do with fields), 2 in ch. 14's *a perfect bijection*, 1 in
   ch. 15, 1 in ch. 5, 7 more in the solutions, and the single one in ch. 4
   itself is *"the perfect analogue of"*. **All 23 are wrong-sense links.**
   Hindi cannot reproduce them even by accident: the Hindi for *perfect field*
   is पूर्ण क्षेत्र, and पूर्ण is already the display of `def:b3:complete:complete`,
   so the harvest resolves it to *complete* — the honest sense in 22 of the 23
   places. The phrase पूर्ण क्षेत्र occurs nowhere in prose (only in the
   `\index` key of the proposition that defines it, where self-links are
   suppressed), so there is no correct link to make. Recovering the target
   would mean manufacturing a use of the phrase. Not done.
2. **213 fewer links than English (95.1 %).** Beyond the 23 above, the gap is
   spread thin and has one structural cause: Hindi forms abstract nouns by
   changing the stem (संतत → सांतत्य, विलेय → विलेयता, संबद्ध → संबद्धता), so every
   one of them is a hand-declared `EXTRA` entry rather than a rule, and the
   forms nobody thought to declare are simply missing. The 11 declared here
   are worth 292 links; a Hindi-aware nominaliser in
   `tools/termlink/morphology.py` would retire the whole block and probably
   close most of the remaining gap. That directory is shared by five books and
   gated by `check_book5_golden.sh`, so it was not touched — see *Requests*.
3. **`मॉड्यूल` for *module* (80 occurrences).** The one transliteration in an
   otherwise Sanskritic technical vocabulary. It is the form the standard
   technical dictionaries give (there is no settled Sanskritic word for the
   algebraic *module*; मापांक means *modulus*), and it is used consistently,
   but a purist reviewer would notice it.
4. **6 correct `स्वातंत्र्य` links traded away** by the `EXTRA_PROTECT` pattern,
   because the idempotent form has to consume the whole phrase. Six wrong
   links avoided, six right ones lost; a per-occurrence protection mechanism
   in `tools/termlink/protect.py` would cost nothing.
5. **The lowest-density file is now `solutions/hi/03-modules-pid.tex` at 76 %
   of its English twin.** It was 64 % until the audit traced the gap to a
   single word: English links *torsion-free* 13 times, and Hindi writes it
   मरोड़-मुक्त, whose hyphen ends the word for the boundary rule so that plain
   मरोड़ can never reach it. Declaring it recovered 13 links. The residue is
   ordinary prose difference, not a defect — but it is a reminder that in an
   agglutinating-by-hyphen language every compound is a potential silent
   miss, and only a per-file ratio audit finds them.
6. Register is uniformly that of a Hindi-medium lecture course, but a native
   reviewer would still find places where a shorter connective could replace a
   longer one; the translation is faithful before it is terse.

## Requests to orchestrator-owned files

Recorded here rather than edited, per `hindi_style_card.md` §6.

1. **`tools/term_config/lang_hi.py` — a nominaliser, or a `WORD_TAIL` for
   oblique plurals.** Hindi's oblique plural is regular (`ों|ओं|एँ|यों`) and its
   abstract-noun suffixes (`-ता`, `-त्व`, `-पन`) nearly so. Either would let
   most of this book's 17 `EXTRA` entries be deleted — and the same is true of
   the ~50 entries the Math 2 agent reported. It changes every Hindi book's
   link layer, so it should land in one deliberate pass, as `lang_pt.py`'s
   `TAIL_ON_EVERY_WORD` did.
2. **`tools/check_hindi_prose.py` — an option to scan `\text{…}` inside math.**
   The gate blanks math wholesale, so English surviving inside `\text{…}` is
   invisible to it: 18 such strings were found here by hand, and the PT edition
   found 216. A `\text{…}`-only pass over the blanked spans would catch the
   whole class mechanically.
3. **`tools/termlink/protect.py` — note the idempotence requirement.** The file
   documents four silent-failure rules for `EXTRA_PROTECT` patterns; a fifth
   belongs beside them: *a pattern whose context can itself be wrapped must
   consume that context, not look ahead at it*, or `--apply` stops being
   idempotent and `--check` reports stale files on the second run. Measured
   here at 6 links.
4. **`tools/build_html_book.sh`** still defaults to `LANGS=en,fr,nl`; the Hindi
   Book 5 is now complete and could join the online reader.

## Files changed by this pass

| Path | Change |
|------|--------|
| `parts/bachelor-3/solutions/hi/21-differential-forms.tex` | fully re-translated from English |
| `parts/bachelor-3/solutions/hi/22-probability-foundations.tex` | fully re-translated from English |
| `parts/bachelor-3/solutions/hi/23-clt-gaussian.tex` | fully re-translated from English |
| `parts/bachelor-3/solutions/hi/14-fourier-transform.tex` | overfull display split into `gather*`; one abbreviation tie |
| `parts/bachelor-3/solutions/hi/08-banach-spaces.tex` | table abbreviation `अनुक्र.\ ` → `अनुक्र.~` (danda gate) |
| `parts/bachelor-3/hi/{04,09,21,22,23}-*.tex`, `parts/bachelor-3/solutions/hi/{10,17}-*.tex` | residual English inside `\text{…}` (19 strings); `फूर्ये` → `फूरिये` (6); `गुणनफल माप` → `गुणन माप` |
| **revision 2** — `parts/bachelor-3/hi/{01–19,22,23}-*.tex` and `parts/bachelor-3/solutions/hi/{01–05,08–13,15,17–20}-*.tex` (37 files) | **168 text-macro arguments translated** (235 English word tokens) inside protected math: the class the gate could not see. Mathematics, `\label`s, `\cref` targets, solution keys and `\omterm` first arguments untouched |
| all 46 `parts/bachelor-3/{hi,solutions/hi}/*.tex` | link layer regenerated against the new config |
| `tools/term_config/book5_hi.py` | rewritten as a curated config |
| `translation_scores/book_5/hi/translation_score.md` | this file |

`styles/**`, `tools/check_translation.sh`, `tools/check_hindi_prose.py`,
`tools/term_config/lang_hi.py`, `tools/termlink/**`,
`tools/link_defined_terms.py`, `latexmkrc`, `.github/**`, the entry file and
`frontmatter/preface.hi.tex` were **not touched**.

## Status

**Meets the ship threshold (≥ 95): 97 / 100.** Book 5 Hindi is complete: 46 of
46 bodies re-translated from the English canon, **zero English visible to a
reader anywhere, including inside math**, 0 errors / 0 undefined /
0 overfull, 390 pp. Working tree left uncommitted for human review; no git
commit was created.
