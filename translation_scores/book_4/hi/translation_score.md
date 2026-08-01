# Translation score — Math Book 4 · Hindi (`hi`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 4 (University Year 2, `bachelor-2`) |
| **Language** | Hindi (`hi`), Devanagari, standard Khari Boli academic register |
| **Quality bar** | **native academic** (English is the source of truth; the French twin was consulted for sense and structure only, never as a source) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **met; no blockers remain** |
| **Date** | 2026-08-01 |
| **Scope of this pass** | **Full re-translation from the English canon.** All 23 chapters and all 23 solution files re-derived with a structure-preserving placeholder pipeline. The 2026-07-24 machine translation was read once, as a list of things not to do, and then discarded — not one of its sentences survives. `tools/term_config/book4_hi.py` was rewritten from a 26-line stub to a curated config. |

## Verdict in one line

A freshly written, native-register Hindi second-year university course: exact
structural mirror of English, a curated term-link layer whose target set is
identical to English's in both directions, a Devanagari prose gate at **0
issues from a 15 734 baseline**, and a build with zero errors, zero undefined
references and zero overfull boxes.

## What the previous edition looked like

The raw MT this replaces had exactly the failure modes the brief named, and
every one of them is now absent from the tree:

| MT failure | Status |
|---|---|
| sense swaps (*map* → मानचित्र, *field* → खेत, *class* → कक्षा) | **0** — *प्रतिचित्रण*, *क्षेत्र*, *वर्ग* throughout |
| transliterated English function words (`द`, `ए`, `ऑफ`, `एंड`, `इज`, `आर`, `फॉर`, `विद`, `टू`) | **0** across all 46 files (gate class `translit`) |
| residual English in visible text, TikZ node text, `\text{…}` | **0** (gate class `english`) |
| Latin `.` where Devanagari wants `।` | **0** (gate class `danda`) |
| MT-injected spaces inside inline math (`$P $ और $ Q$`) | **0** (gate class `math-space`) |
| digits split from their unit / `\,` between Devanagari and digits | **0** (gate class `split-number`) |
| English `\index{}` keys left behind | **0** — EN ∩ HI index-key intersection is now the empty set |

Baseline for the five gate classes was **15 734**; it is **0**.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Terminology | **96** | A complete Hindi technical glossary was built and applied uniformly: समुच्चय, प्रतिचित्रण, विभाग, गणनीय/अगणनीय, समशक्त, गणनसंख्या, समूह/वलय/क्षेत्र, गुणजावली, सहसमुच्चय, क्रमचय, चक्र/पार्यय, एकांतर समूह, समाकारिता/तुल्याकारिता, केंद्रक, द्वैत समष्टि, विलोपक, परिवर्त, सारणिक, अनुरेख, अभिलक्षणिक मान/सदिश, वर्णक्रम, विकर्णनीय/त्रिभुजनीय, शून्यंभावी, दूरिक समष्टि, विवृत/संवृत, संहत, संबद्ध, पूर्ण, संकुचन, मानदंड, संकारक मानदंड, अनंतस्पर्शी, योग्य कुल, अनुचित समाकल, प्रभावी अभिसरण, एकसमान/बिंदुवार/सामान्य अभिसरण, घात श्रेणी, वैश्लेषिक फलन, द्विघात रूप, चिह्नांक, सहसंलग्न, प्रसामान्य लांबिक, हर्मीशियन, एकात्मक, फूरिये श्रेणी, अवकल, याकोबी आव्यूह, आनत समष्टि, बैरिकेंद्र, उत्तल कवच, चाप-लंबाई, वक्रता, ऐंठन, फ्रेने ढाँचा, प्रथम आधारभूत रूप, अन्वालोप, रेखा समाकल, याकोबी सारणिक, प्रतिदर्श समष्टि, सप्रतिबंध प्रायिकता, प्रत्याशा, प्रसरण, सहप्रसरण, जनक फलन, शाखन प्रक्रम, विलोपन प्रायिकता. Proper names transliterated once and reused (कैंटर, लाग्रांज, बेज़ू, ऑयलर, कोशी, बानाख, रीमान, लेबेग, फूरिये, हिल्बर्ट, वाइल, शूर, आदामार, चोलेस्की, लजांद्र, ल्यूविल, ग्रोनवाल, द्यूआमेल, डी म्वाव्र, चेबिशेव, हॉल्डर, मिंकोव्स्की, जेनसन, डार्बू, श्वार्ज़, पियानो, आर्ज़ेला--आस्कोली, बोर--मोलेरुप, पेरों--फ्रोबेनियस, पोया, कोल्मोगोरोव, हॉफडिंग, चेर्नोफ़, याग्लोम) |
| Register / tone | **96** | University lecture register end to end — मान लीजिए / सिद्ध कीजिए / दिखाइए / निष्कर्ष निकालिए / इससे यह निष्कर्ष निकलता है — with the English book's voice preserved rather than flattened: «कोई पिया हुआ आदमी घर का रास्ता पा लेता है; कोई पिया हुआ पक्षी शायद न पाए», «छोटी प्रायिकताएँ वह क्षेत्र हैं जहाँ अंतर्ज्ञान को पैमाना नहीं, चरघातांकी चाहिए», «पहले पुनःप्राचलन कीजिए, निष्कर्ष बाद में निकालिए», «ऊँची विमा का गोलक, सांख्यिकीय रूप से, एक साथ हर दिशा में एक पतला पूआ है» |
| MT-artifact freedom | **98** | All five gate classes at 0 over 46 files. No transliterated function word, no Latin sentence terminator in Devanagari prose, no English inside `\text{}` or TikZ nodes, no English `\index{}` key |
| Term-link layer | **95** | `book4_hi.py` rewritten from 26 lines to a curated config with a documented Hindi-morphology rationale. 3 298 links, **85 targets — identical set to English, both directions**. `--check` green and idempotent. Deduction: the shared morphology still ends a link one matra short on oblique plurals (see "why not 100") |
| LaTeX hygiene | **99** | 0 fatal errors, 0 undefined references, **0 overfull boxes**. All 46 files valid UTF-8, 0 TeX accent escapes, no nested `\omterm`, no drafty `...` |
| Cross-refs / rule compliance | **99** | `\label`, `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English. 0 duplicate labels. 0 cross-volume `\cref` leakage. No country or curriculum name in visible text (`NCERT`, `CBSE`, `भारत`, `India` all return 0); cross-volume references read «प्रथम वर्ष का खंड», «तृतीय वर्ष का खंड», «हाई स्कूल खंड» |
| Structural fidelity | **99** | Exact mirror: 23 chapters / 23 solution files both sides; 125 sections, 89 theorems, 65 definitions, 25 propositions, 5 lemmas, 272 examples, 99 remarks, 16 methods, 276 exercises, 23 problems, 299 solutions, 3 figures, 30 `tikzpicture` — every census identical to English |
| Solutions | **97** | All 299 solutions present, complete and native; `\section*{अध्याय \ref{ch:…} --- <title>}` headers localized with the English `ch:` slug untouched |
| Figures | **98** | TikZ/pgfplots drawing code byte-identical to English; only node text and captions localized (e.g. `center of curvature` → `वक्रता केंद्र`, `small $n$ / large $n$` → `छोटा $n$ / बड़ा $n$`, `ellipsoid` → `दीर्घवृत्तज`) |

Weighted (terminology 0.18, register 0.18, MT-artifact freedom 0.16, term-link
0.14, LaTeX 0.10, cross-refs 0.08, structure 0.06, solutions 0.06, figures
0.04) the arithmetic gives **97.0**; reported as **96**, rounded down for the
link-display truncation described below, which is visible in the PDF.

## Structural / build gates (measured 2026-08-01)

> **Note for whoever re-measures these:** the Hindi book builds with **XeLaTeX**
> (dispatched by `latexmkrc` for `*_hi.tex`). The log is not UTF-8 throughout,
> so use `grep -a` / `grep -ac`; a plain `grep -c` treats it as binary and
> prints nothing, which reads as "0".

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-2 hi` | **PASSED** — hindi prose gate OK (46 files) |
| Devanagari prose gate, five classes (`english`, `translit`, `danda`, `math-space`, `split-number`) | **0 / 0 / 0 / 0 / 0** (baseline 15 734) |
| `python3 tools/link_defined_terms.py --book 4 --lang hi --unwrap --apply` | 4 139 stale links removed, then 0 |
| `python3 tools/link_defined_terms.py --book 4 --lang hi --apply` | **3 298 links** across 46 files (def 2 996, thm 121, pb 113, ex 63, lem 4, prop 1) |
| `python3 tools/link_defined_terms.py --book 4 --lang hi --check` | **green** — every file matches the config, idempotent |
| `\omterm` first-arg parity vs English | **identical sets, both directions — 85 targets** (`EN−HI = ∅`, `HI−EN = ∅`) |
| `latexmk one_math_book_4_university_year_2_hi.tex` | exit 0 |
| Fatal errors (`grep -ac '^!'`) | **0** |
| Undefined references (`grep -aci 'undefined'`) | **0** |
| Overfull `\hbox`/`\vbox` (`grep -ac 'Overfull'`) | **0** |
| HI PDF | `build/one_math_book_4_university_year_2_hi.pdf`, **388 pp** (EN 397) — Devanagari sets slightly tighter per page; token count is +9.8 % vs English, so no padding |
| Exercise ↔ solution key parity | **0 divergences** (276 `exo:` + 23 `pb:` ↔ 299 `\begin{solution}`) |
| Duplicate labels in the `hi` tree | **0** |
| Cross-volume `\cref` leakage (`:b1:`, `:b3:`, `:g1x:`) | **0** |
| TeX accent escapes / non-UTF-8 files | 0 / 0 |
| Index keys: EN ∩ HI intersection | **0 keys** |
| Country / curriculum names in visible text | **0** |

**Not gated, for the record:** 111 underfull `\hbox`/`\vbox` warnings, the
series norm (EN 104, PT 108). The `_hi` entry file already carries
`\emergencystretch{3em}`.

## How it was done

1. **Everything is a fresh derivation.** Each English file was mechanically
   split into a *skeleton* of prose with `«N»` placeholders and a *slot
   table*, with every `$…$`, `\[…\]`, math environment, `tikzpicture`, `axis`,
   `\label`, `\cref`/`\ref`, `\index` sort key, `\includegraphics`,
   `\begin{solution}{key}` and the **first argument of every `\omterm`**
   protected byte-for-byte. The Hindi prose was authored against the skeleton
   and rebuilt, with the builder refusing any file whose placeholder multiset
   did not match the English one — six real placeholder errors were caught
   this way and fixed. TikZ node texts, environment optional titles, `\text{…}`
   contents and captions were lifted into the slot table and translated there,
   so figure *drawing* code is provably byte-identical while figure *text* is
   Hindi.
2. **`tools/term_config/book4_hi.py` rewritten.** The stub had
   `DROP = set(STOP)` (which destroys the soft "still linked in its defining
   chapter" behaviour), an English-head `NOT_A_TERM` that cannot fire on Hindi
   (Hindi puts the head noun last: «कोरोवकिन की प्रमेय»), and empty `EXTRA` /
   `EXTRA_PROTECT`. The rewrite mirrors `book4_en.py` decision by decision and
   documents the Hindi-specific reasoning in its docstring.
3. **`AMBIG_POLICY` kept `"drop"`, deliberately.** It is what `book4_en.py`
   uses, and the gate this edition is measured against is *sense parity with
   English*. The two terms the harvester reports as defined twice would be
   exactly the ones mis-sent by `nearest-preceding`.
4. **Wrong-sense link hunt.** Every high-frequency term's link displays were
   read in context. Real wrong-sense links found and killed:
   - **`चिह्न` → `thm:b2:structures:signature` (131 sites).** *चिह्न* is the
     signature of a permutation *and* the everyday Hindi word for "sign"
     (sign of a coefficient, sign table, sign change, integral sign,
     Descartes' rule of signs). English stoplists `signature`; here even the
     defining chapter mixes the senses, so it is hard-`DROP`ped — which also
     restores target parity, since English links neither signature.
   - **`चिह्नांक` → `thm:b2:quadratic:sylvester` (43 sites)** — the signature
     of a quadratic form. English links it nowhere; dropped for parity.
   - **`संवृत` → `def:b2:multint:exact` (15 sites)** — *संवृत* is "closed" in
     every sense (closed set ch. 4, closed curve ch. 18/21, closed interval,
     closed form ch. 20). Hard-dropped exactly as English hard-drops `closed`;
     the phrase *संवृत रूप* still carries the target.
   - **`कोटि` → `def:b2:structures:generated` (164 sites)** — *कोटि* is the
     order of a group element *and* the order of a derivative, of a Taylor
     expansion, of an ODE, and the rank of a matrix. Stoplisted, so it is now
     chapter-local, exactly like English's `order`.
   - **`अभिसरित` → `def:b2:integration:improper` (137 sites)** — every series
     in chapters 7, 10, 11, 14, 20, 21, 23 was pointing at the improper
     *integral* definition. Stoplisted; *अनुचित समाकल* carries the target.
   - `तुल्य` (equivalent), `बीजगणित` (linear algebra, the subject),
     `एकांतर` (alternating series vs alternating form), `यथातथ` (the exact
     *value*) — stoplisted, one-for-one with English.
   - Named **results** rather than notions, matching `book4_en.py`'s `DROP`:
     गाउस का सीमा-सूत्र, कोरोवकिन की प्रमेय, आदामार की असमिका,
     कूराँ--फिशर न्यूनतम-अधिकतम प्रमेय, वाइल की असमिका, याकोबी सूत्र,
     स्टुर्म की पृथक्करण तथा तुलना प्रमेय, समपरिमापी असमिका,
     हॉफडिंग असमिका, चेर्नोफ़ परिबंध, संकेंद्रण असमिकाएँ, गिब्स परिघटना,
     ऑयलर फलन, केंद्रबिंदु.
   - Phrase-level protections mirroring English: *शृंखला नियम* (chain rule),
     *बृहत् संख्याओं का नियम*, *दुर्बल/प्रबल/स्थानीय नियम*, *परावर्तन का
     नियम*, *क्रामर का नियम*, *विभाग नियम*, *अंगूठे का नियम* → the law of a
     random variable; *अवकल समीकरण / अवकल कलन / अवकल ज्यामिति / अवकल
     समाकृतिकता* → the differential of a map; *उत्तल फलन / उत्तल वक्र* → the
     convex set of ch. 17; *पूर्ण प्रायिकता / पूर्ण परिबद्धता / पूर्ण वर्ग* →
     the complete metric space; *सममित रूप से* → the symmetric endomorphism;
     *आबेल-योग्य*, *चेज़ारो-योग्य*, *वृत्त-जनित* (the English config protects
     precisely these three).
5. **A Devanagari-specific link bug found and fenced.** Python's `\w` does not
   include Devanagari combining marks (matras), so a word boundary falls
   *between* a stem and its matra. That is convenient for inflection —
   «चक्रों», «वर्णक्रमीय», «मानों» are matched on the stem for free — but it
   also makes a defined term match as the *prefix* of an unrelated word and as
   the *suffix* of a prefixed one. Real damage found and fenced in
   `EXTRA_PROTECT`: **चक्र** inside **चक्रिका** (disk, 60 sites), **पूर्ण**
   inside **पूर्णांक** (integer, 36), **सममित** inside **सममिति** (symmetry,
   25) and after **प्रति** in **प्रतिसममित** (antisymmetric, 21), **संतत**
   inside **संतति** (progeny, ch. 23, 23 sites), **मानदंड** inside
   **मानदंडित** (normed, 22), **बीजगणित** inside **बीजगणितीय** (algebraic,
   10), **तुल्य** inside **तुल्याकारिता** (isomorphism), **परिवर्त** inside
   **परिवर्तित** (changed), **चिह्न** inside **अंगुलिचिह्न** (fingerprint),
   **घटना** inside **परिघटना** (phenomenon). All 305 remaining
   partial-word matches were re-inspected one by one and are benign
   inflections, dandas, or the correct hyphenated compounds English links too
   (विषम-हर्मीशियन, पूर्व-द्वैत, अर्ध-विवृत, विरल-घटना, वर्ग-योग्य).
6. **Three build failures found and fixed.** One fatal (`Missing $ inserted`)
   and two typographic. The fatal one and two silent siblings were the same
   mistake: an English `\text{…}` slot whose *placeholder* had been moved
   inside the braces while re-ordering for Hindi word order, so math ended up
   in text mode (`\text{ at }v = …` → `\text{ यहाँ: }v = …`, plus
   `\text{integrable, independent of }x`, `\text{terms in }x_{k+1}` and
   `\text{(a matrix polynomial in }t`). Three overfull boxes were then cleared
   by tightening prose and one `\qquad`→`\quad`, with no structural change.
7. **Three English `\index{}` keys localized.** `Jensen's inequality`,
   `Stirling's formula` and `spectral theorem` sit *inside display math*, where
   the pipeline correctly refuses to touch anything; they were localized by
   hand (and the fix folded back into the rebuild script), taking the EN ∩ HI
   index-key intersection to **0**.

## Sampled passages, judged

**1. `hi/01-sets-structures.tex`, chapter opening — native.**

> यह आरंभिक अध्याय प्रथम वर्ष के खंड में रखी गई नींव को रोज़ काम आने वाले
> औज़ारों में ढालता है: समुच्चयों और विभागों का कलन, अनंत समुच्चयों की
> तुलना (गणनीयता, कैंटर--बर्नस्टाइन), तथा समूहों और वलयों का संरचनात्मक
> सिद्धांत […] यहाँ की हर बात पुस्तक के शेष भाग में लगातार काम आती है।

Idiomatic Hindi word order, correct `का/की/के` agreement throughout, the
compound verb «ढालता है» (casts/moulds) rather than a calqued "turns … into".
No English residue, no translationese.

**2. `hi/22-discrete-random-variables.tex`, the gambler's fallacy — native.**

> पासा याद नहीं रखता, और कोई छक्का कभी ``बक़ाया'' नहीं होता --- जुआरी का
> भ्रम यही मान्यता है कि सप्रतिबंध नियम खिसक जाना चाहिए था। […] जिस भी
> प्रतीक्षा-समय का पूर्वानुमान कभी नहीं बदलता वह ज्यामितीय है।

Carries the English aphorism without importing its syntax; «बक़ाया» is the
ordinary Hindi word for "owing / due", which is exactly the rhetorical move
the English makes with *due*.

**3. `solutions/hi/21-countable-probability.tex`, Pólya's theorem — native.**

> सरल यादृच्छिक चहलक़दमी $\Z$ तथा $\Z^2$ पर पुनरावर्ती है, और $d \geq 3$
> के लिए $\Z^d$ पर क्षणिक। कोई पिया हुआ आदमी घर का रास्ता पा लेता है; कोई
> पिया हुआ पक्षी शायद न पाए।

The joke survives the translation, which is the hardest thing to get right
here; *पुनरावर्ती / क्षणिक* are the standard Hindi renderings of
recurrent / transient.

**4. `hi/20-multiple-integrals.tex`, "Method: choosing the change of
variables" — native.**

> सीमा-समीकरण पढ़िए, और \emph{उन्हीं को} निर्देशांक चुनने दीजिए; फिर याकोबी
> वक्ररेखीय जाल की कोशिका का क्षेत्रफल बदल देता है […] हर स्थिति में
> समाकलन से पहले तीन ख़ाने भरने हैं।

Imperative lecture register (`पढ़िए`, `दीजिए`) exactly as the brief asks;
«तीन ख़ाने भरने हैं» is the natural Hindi for "three boxes to tick".

**5. `hi/18-curves.tex`, the local-study method — near-native.**

> ढाँचा $(f^{(p)}(t_0), f^{(q)}(t_0))$ सामान्यतः प्रसामान्य लांबिक
> \emph{नहीं} होता --- सारणी स्पर्श रेखा के सापेक्ष स्थितियाँ बताती है, कोण
> या दूरियाँ नहीं, अतः चित्र से वक्रता मत पढ़िए।

Correct and fluent, but «प्रसामान्य लांबिक» (orthonormal) is a Sanskritic
coinage that a Hindi-medium reader will meet here for the first time; a
Hindi-medium mathematician might prefer the transliteration. Judged
*near-native* rather than native only because the register is a shade more
formal than a lecture would be.

No passage sampled was judged *MT*.

## Why not 100

1. **Link displays end one matra short on oblique plurals (−1.5).** Because
   Python's `\w` excludes Devanagari matras, «चक्रों» is linked as
   «[चक्र]ों» and «वर्णक्रमीय» as «[वर्णक्रम]ीय»: the visible text is
   correct and the link target is correct, but the coloured span stops one
   character early. 305 sites. This is a shared-morphology limitation, not a
   config one — see the orchestrator request below. Every such site was
   inspected; none is a wrong-sense link.
2. **Hindi has no settled term for a handful of nineteenth-century curve and
   surface notions (−1).** *osculating circle*, *evolute*, *envelope*,
   *caustic*, *cusp*, *nephroid*, *astroid* were rendered
   चुंबन वृत्त, विकसिता, अन्वालोप, दाहक वक्र, उभयाग्र, नेफ्रॉयड, ऐस्ट्रॉयड.
   The first four are principled Sanskritic coinages (and *अन्वालोप* is
   attested), the last two are transliterations; a different Hindi
   mathematical tradition might choose differently. They are at least used
   consistently, and each is introduced next to its English-derived form or
   its defining formula.
3. **Fifteen `EXTRA_PROTECT` entries exist only to work around the matra
   boundary (−1).** *चक्रिका*, *पूर्णांक*, *सममिति*, *संतति*, *मानदंडित*,
   *प्रतिसममित*, … are not curation decisions — they are orthographic
   accidents. If the shared boundary rule is made Devanagari-aware they should
   all be deleted, and a future Hindi book will otherwise have to rediscover
   the same list.
4. **Three link-count divergences from English are accepted, not resolved
   (−0.5).** HI has 3 298 links against EN's 3 511. The gap is concentrated in
   `def:b2:randomvar:law` (Hindi *नियम* is both "law" and "rule", so more of
   it is protected than English protects `law`) and in the six stoplisted
   words, whose Hindi spread across senses is wider than the English one. The
   **target set is identical**, which is the gate; the density is not, and
   erring toward fewer links was the deliberate choice.

## Requests to the orchestrator

These are all in files this agent must not touch.

1. **`tools/term_config/lang_hi.py` — make the word boundary
   Devanagari-aware.** The single highest-value change available to this
   edition. Concretely: a match should not be accepted when the character
   immediately *before* it is a Devanagari letter or combining mark, and the
   run of combining marks immediately *after* it should be absorbed into the
   match when it is an inflectional tail. Something like
   `WORD_TAIL = r'(?:ों|ओं|ें|एँ|ियाँ|ीय|ी|ों)?'` plus a Devanagari-aware
   left boundary would (a) make the link display cover the whole word at 305
   sites and (b) let ~15 `EXTRA_PROTECT` entries in `book4_hi.py` be deleted.
   It affects all five Hindi books identically, so it is worth doing once,
   centrally, rather than five times in five configs.
2. **`tools/term_config/lang_hi.py` — consider `HEAD = r''`.** The hyphenated
   prefix rule does buy the correct compound links (विषम-हर्मीशियन,
   पूर्व-द्वैत, अर्ध-विवृत, विरल-घटना, वर्ग-योग्य), so this is a genuine
   trade-off, not a bug report; but the prefix it captures is truncated at the
   first matra («द्वितीय-कोटि» is linked from «य-कोटि»), which looks wrong in
   the PDF. If request 1 is implemented, this one becomes unnecessary.
3. **English-canon nits, for the canon's owner** (both were mirrored verbatim
   into Hindi rather than silently "fixed", to keep the trees in step):
   - `parts/bachelor-2/14-fourier-series.tex:105` — `$f' $` has a stray space
     inside inline math.
   - `parts/bachelor-2/solutions/23-generating-functions.tex:404–405` — `\cref`
     is separated from its argument by a line break, so any tooling that
     protects `\cref{…}` as one token sees a bare `\cref` followed by a
     brace group of English words. Joining the two lines would help every
     translation.
4. **No change requested to `tools/check_hindi_prose.py`.** After the
   2026-08-01 correction (removal of `इन`; recursive reduction of environment
   optional titles, `\omterm` displays, `\index` keys and `\href` text;
   `circuitikz` treated as drawing code; `{size (\unit{m})}` no longer
   reporting *unit*) it flagged nothing spurious in this book. All 15 734
   baseline issues were real.

## Files written by this pass

- `parts/bachelor-2/hi/01-…` through `23-generating-functions.tex` — 23 files,
  all rewritten
- `parts/bachelor-2/solutions/hi/01-…` through `23-generating-functions.tex` —
  23 files, all rewritten
- `tools/term_config/book4_hi.py` — rewritten (26 lines → curated config)
- `translation_scores/book_4/hi/translation_score.md` — this file

`one_math_book_4_university_year_2_hi.tex` was inspected and needed no change:
it already sets `\booklang{hi}`, `\emergencystretch{3em}`, `\ombrandheader`,
`\omsolutionlinks` and a Hindi `\bookline`.

**No git commits were created.** The working tree is left for review.
