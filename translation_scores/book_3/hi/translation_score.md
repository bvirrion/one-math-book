# Translation score — Math Book 3 · Hindi (`hi`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 3 (University Year 1, `bachelor-1`) |
| **Language** | Hindi (`hi`) — standard technical Hindi, university lecture register (`hindi_style_card.md` §1) |
| **Quality bar** | **native academic** (English is the source of truth; the FR edition was consulted only as a sense/structure reference, never as a source) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **MET** |
| **Date** | 2026-08-01 |
| **Scope of this pass** | Book-level score for all 50 files. 48 were re-translated from English in the interrupted 2026-07-31 run; this pass re-translated the last 2 (`25-two-variable-functions` chapter + solutions) from English, cleared the book's last 2 overfull boxes, rebuilt `tools/term_config/book3_hi.py` from a 26-line stub into a curated config, regenerated the `\omterm` layer, and audited register / terminology / link senses across the whole book. |

## Verdict in one line

Structurally byte-exact against English, written in native Hindi lecture
register, with an `\omterm` target set now **exactly equal** to English's and
every gate green.

## What this pass did

1. **`parts/bachelor-1/hi/25-two-variable-functions.tex`** and
   **`parts/bachelor-1/solutions/hi/25-two-variable-functions.tex`** —
   re-translated from the English canon. The 2026-07-24 machine translation was
   read only as a warning list and none of it survives. It had, among much else:
   `कार्य` (*work*) for *function*, `गेंदें` (*balls*, the toys) for open balls,
   `समारोह` (*ceremony*) for *function*, `विमान` (*aeroplane*) for the plane
   $\R^2$, `डेरिवेटिव` / `ग्रेडियेंट` / `सबमैनिफोल्ड्स` transliterated, `काठी`
   left bare where the book says `काठी बिंदु`, `महत्वपूर्ण बिंदु` (*important
   point*) for *critical point*, `प्रतिगमन लाइन`, `कम से कम वर्गों`, `सामान्य
   समीकरण` where chapters 20/22/23 had already fixed `प्रतिगमन रेखा`, `न्यूनतम
   वर्ग`, `प्रसामान्य समीकरण`, the transliterated article `द`, Latin full stops
   instead of dandas, spaces injected inside inline math (`$ f $`), and
   untranslated `\textbf{Part III --- The …}` headers.
2. **Both overfull boxes cleared** (details below).
3. **`tools/term_config/book3_hi.py` rebuilt** — the stub was 26 lines with
   `EXTRA = {}`, `DERIVED = {}`, `EXTRA_PROTECT = []` and, worse,
   `DROP = set(STOP)`, which turned every soft stop into a hard one and threw
   away exactly the chapter-local links `STOP` exists to preserve.

## Overfull boxes — resolution

Both were content-level and neither was in the machine-translated chapter; they
were located by walking the log's file stack, not guessed.

| Where | Cause | Fix |
|---|---|---|
| `hi/17-numerical-series.tex`, display at line 111 (30.29 pt) | The comparison test's two implications sit side by side with `\qquad`; Hindi's `अभिसरित होती है` / `अपसरित होती है` are far longer than *converges* / *diverges*, so the line could not fit. | The `\[…\]` became an `align*` with one implication per line, aligned on `\implies`. Same content, same reading order, no wording weakened. |
| `solutions/hi/20-linear-maps.tex`, paragraph at lines 124–134 (17.97 pt) | An unbreakable inline `$\bigl(x_1, f(x_1), \dots, x_k, f(x_k)\bigr)$` inside a long sentence, and the sentence itself was machine phrasing: **`कुल को लालच से बनाइए।`** — literally *"build the family out of greed"* for *"build the family greedily"*. | Sentence rewritten to `कुल को एक-एक चरण में बढ़ाते हुए बनाइए।` and the family displayed on its own line, which also makes the induction easier to read. |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror: 25 chapters, 25 solution files, **300** `exo:` labels EN / 300 HI, **25** `pb:` / 25, **325** `\begin{solution}{…}` on both sides. The `\label{}`, `\cref`/`\Cref` and solution-key multisets are byte-identical to English (all three `diff`s empty). `check_translation.sh bachelor-1 hi` **PASSED** |
| Terminology | **96** | One vocabulary across the volume, and the last chapter was written *against* the chapters that precede it rather than in isolation: *प्रसामान्य समीकरण* (ch. 22/23 already used it), *न्यूनतम वर्ग* (ch. 20/22/23), *मोंज कसौटी* / *मोंज राशि* (ch. 21/22), *ग्राम आव्यूह*, *आघूर्ण आव्यूह*, *लांबिक प्रक्षेप*, *अंतर्गुणन*, *क्रांतिक बिंदु* (ch. 4/14/16), *काठी बिंदु* (ch. 16), *आँकड़े* (ch. 8/20/21, never *डेटा*), *स्थानीय अधिकतम/न्यूनतम* and *समग्र* (ch. 13/14/16), *चरम मान प्रमेय* (ch. 13/14), *शृंखला नियम* (ch. 14/15), *कोशी--श्वार्ट्ज़* (ch. 23). No sense swaps found in sampling; the style card's forbidden list returns zero hits book-wide |
| Register / tone | **96** | Reads as a Hindi university lecture course: `मान लीजिए`, `सिद्ध कीजिए`, `निष्कर्ष निकालिए`, `संगणित कीजिए`, `जाँचिए`, `यदि और केवल यदि`, `अतः`, `इससे`, `विलोमतः`, `अर्थात्`. Sentence count tracks English clause for clause and the PDF is **shorter** than English (386 pp vs 395), so there is no MT padding anywhere |
| LaTeX hygiene | **99** | 0 fatal errors, 0 undefined references, **0 Overfull `\hbox`**; **0** TeX accent escapes, no `\end{proof>` typo class, no drafty `...`, no zero-width spaces. `check_hindi_prose.py` (the Devanagari gate: `english`, `translit`, `danda`, `math-space`, `split-number`) returns **OK on all 50 files** |
| Cross-refs / rule compliance | **98** | `\label`, `\cref`/`\Cref` targets and `\begin{solution}{key}` byte-identical to English; Hindi needs no articles before `\cref`, so the FR/PT gender trap does not exist here. No country, board or curriculum name in visible text (0 hits) |
| Defined-term links | **94** | `--check` **green** and idempotent (a second `--apply` inserts 0). **106 distinct targets in Hindi, 106 in English, and the two sets are equal** (`diff` empty). **3 668** links against English's **3 944** (93.0 %); the whole shortfall is a shared-file morphology limitation, quantified below |
| Figures | **97** | All 33 `tikzpicture` environments present, drawing code byte-identical (coordinates, `\draw`, `\addplot`, styles untouched); only node text, axis labels and captions localized. In ch. 25 the two nodes `saddle` / `min` became `काठी` / `न्यूनतम` |
| Solutions | **96** | All 325 solutions present, complete and native. All 25 headers are `\section*{अध्याय \ref{ch:…} --- <title>}` with the `ch:…` slug unchanged, and a scripted comparison confirms **every** header title equals its chapter's own `\chapter{}` (0 mismatches) |
| MT-artifact freedom | **95** | An English-function-word sweep over all 50 files returns only TikZ syntax (`circle (r and r)`, `.. controls (…) and (…)`) and one inherited source comment. `\text{…}` spans inside math are Hindi (`\text{ तथा }`, `\text{बिंदु पर के मान}`, `\text{कोई शेषफल नहीं}`, `\text{स्पर्शरेखा}`). The sweep is heuristic, so a calque phrased in fully Hindi words cannot be excluded |

**Overall: 96** — weights: register 0.18, terminology 0.18, MT-artifact freedom
0.16, defined-term links 0.12, cross-refs/rule compliance 0.10, LaTeX hygiene
0.08, solutions 0.08, figures 0.05, structure 0.05 → **96.2**.

Register, terminology and MT-artifact freedom carry more than half the weight on
purpose: `check_translation.sh` already gates structure, and a translation can
be structurally perfect and still be unreadable prose — which is exactly what
the 2026-07 machine output was.

## Structural / build gates

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-1 hi` | **PASSED** |
| `python3 tools/check_hindi_prose.py parts/bachelor-1/hi parts/bachelor-1/solutions/hi` | **OK (50 files)** — 0 in every class |
| `python3 tools/link_defined_terms.py --book 3 --lang hi --unwrap --apply` then `--apply` | 3 668 removed → **3 668 links across 50 files** |
| `python3 tools/link_defined_terms.py --book 3 --lang hi --check` | **green** — "every file matches what the config generates"; a repeat `--apply` inserts **0**, so the pass is idempotent |
| `latexmk one_math_book_3_university_year_1_hi.tex` | exit 0 |
| Fatal errors — `grep -ac '^!'` | **0** |
| Undefined references — `grep -aci 'undefined'` | **0** |
| Overfull `\hbox` — `grep -ac 'Overfull'` | **0** (was 2) |
| Underfull `\hbox` | 121 (ragged-right noise; PT 119, ES 122 — same band) |
| PDF | `build/one_math_book_3_university_year_1_hi.pdf`, **386 pp** (EN 395, FR 416, PT 410) |
| Exercise / problem / solution census vs EN | 300/300, 25/25, 325/325 |
| `\label` / `\cref` / solution-key multisets vs EN | identical (`diff` empty) |
| `tikzpicture` census vs EN | 33/33 |
| Solution-header titles vs chapter titles | 25/25 identical |
| TeX accent escapes | **0** |
| `\index{}` keys | 213 distinct Hindi keys; EN∩HI intersection = **1** (`\index{Z/nZ@$\Z/n\Z$}`, genuinely identical) |
| **`\omterm` first-arg target parity** | **106 targets EN, 106 HI, sets equal** |

## Term configuration rebuilt (`tools/term_config/book3_hi.py`)

Curated against `book3_en.py` entry by entry. Final shape: `NOT_A_TERM` 12 heads,
`STOP` 7, `DROP` 21, `EXTRA` 5, `EXTRA_PROTECT` 9, `NO_CAPITAL` empty,
`AMBIG_POLICY = "drop"`.

* **`DROP` is no longer seeded from `STOP`.** The stub wrote `DROP = set(STOP)`,
  which made every soft stop hard. Separating them restored the chapter-local
  links `STOP` is for, and the effect is visible and correct: *संयुग्मी* now
  links **9** times, all inside chapter 3, against English's **9** *conjugate*
  links, all inside chapter 3. *परिमित* is confined to ch. 2, *सममिति* to
  ch. 20, *प्रवणता* to ch. 25.
* **`STOP` additions.**
  * *संयुग्मी* — the complex conjugate of ch. 3 versus the conjugate expression
    of ch. 11 versus conjugating a matrix in ch. 21/22. English STOPs
    *conjugate* for the same three senses.
  * *प्रवणता* — **a Hindi-only collision.** Chapter 25 defines the *gradient*;
    the same Hindi word is the *slope* of a one-variable graph in ch. 4, 11, 14
    and 24 (English keeps the two apart lexically and has no problem). `STOP`
    reproduces English's behaviour exactly: English links
    `def:b1:multivar:partial` in ch. 25 and nowhere else.
* **`DROP` — ordinary Hindi, or a second technical sense.** *क्रम* (61 links
  before the fix: "उलटे क्रम में", "क्रम से", **and the order of a group** of
  ch. 7 — English links only the order *relation*, 9 times); *प्रत्यक्ष* (bare
  *direct*: a **direct isometry** in ch. 23 is not the direct sum of ch. 18 —
  English DROPs *direct*); *क्रांतिक* and *बीजीय* / *अबीजीय* (bare adjectives;
  the compounds *क्रांतिक बिंदु*, *बीजीय संख्या*, *अबीजीय संख्या* survive);
  *सदृश*.
* **`DROP` — result names** reaching the harvest through `\emph{}\index{}`, so
  `NOT_A_TERM` cannot see them: *कुमर की प्रमेय*, *लजांद्र का सूत्र*, *डी मॉर्गन
  के नियम*, *टॉलेमी असमिका*, *लिउविल असमिका*, *एकांतरित श्रेणी का आकलन*,
  *फलनीय समीकरण*, *कोशी का फलनीय समीकरण* — the same list the English config
  drops by hand.
* **`DROP` — target parity.** Seven correct-sense Hindi links were dropped only
  because English never uses the target (English writes the symbol where Hindi
  spells the name out): *लघुत्तम समापवर्त्य* (EN writes `\lcm`), *कोणांक* (EN
  DROPs *argument* outright), *संयोजन-नियम*, *सम्मिश्र निर्देशांक*, *त्रिभुज
  असमिका*, *समकाल वक्र*, *तुल्य आव्यूह* / *सदृश आव्यूह*. Each is listed in the
  config with its reason; each is a link a Hindi reader loses and an English
  reader never had.
* **`EXTRA` — 5 entries, each closing a specific hole:**
  * *संतत* → `def:b1:continuity:continuous` and *अवकलनीय* →
    `def:b1:derivative:def`: the definitions emphasise a compound
    (`\emph{$x_0 \in I$ पर संतत}`), so the bare adjective the rest of the book
    uses is never harvested. English restores *continuous* / *differentiable*
    for exactly this reason. These two entries alone carry **199** of the book's
    links (*संतत* 161, *अवकलनीय* 38) and bring `def:b1:continuity:continuous` to
    **217** against English's **215** — the closest match of any target in the
    book.
  * *सहगुणनखंड-प्रसार* → `thm:b1:det:cofactor`: the index-only harvest requires
    a space in the term, so a hyphenated Hindi compound is invisible (the gotcha
    `CLAUDE.md` documents for Dutch). Without it English's `thm:b1:det:cofactor`
    had no Hindi twin.
  * *मीनार नियम* → `pb:b1:findim:1`: Hindi says *niyam* for both *rule* and
    *law*, so `NOT_A_TERM`'s bare `नियम` — which must stay, it is what stops
    *क्रामर का नियम* — also eats Dedekind's tower law. English keeps it because
    its `NOT_A_TERM` lists the phrase `"law of"`, not the bare noun.
  * *ऑयलर का अचर* → `pb:b1:series:1`: `\index{ऑयलर का अचर}` sits in exercise 12,
    *before* the weekend problem that defines γ, so the nearest preceding
    statement is an unrelated telescoping example. English resolves it to the
    problem; Hindi must too, or the same words point at two different places.
* **`EXTRA_PROTECT` — 9 spans**, no pattern consuming a `$`:
  *से स्वतंत्र* ("$\theta$ से स्वतंत्र" = independent **of**, not a free
  family — this fired inside the newly written ch. 25), *स्वतंत्र चर*,
  *रैखिक बीजगणित* / *रैखिक संचय* / *रैखिक व्यंजक* (English protects the same
  three), *उच्चतम घात* ("highest degree", not a supremum), *संवृत रूप* ("closed
  form"), *मुक्त पतन* (free fall), and *एकैकी आच्छादन*.
  The last is worth spelling out: **English writes *bijection* as one
  unharvested word and never links it** (95 occurrences, 0 links), while Hindi
  builds the noun out of the adjective, so 82 sites would have linked in Hindi
  and not in English. The *adjective* *एकैकी आच्छादक* is a harvested term of its
  own and still links **42** times, against English's **41** *bijective*.
* **`NO_CAPITAL` is empty and must stay empty.** Devanagari has no letter case,
  so English's *Set / Map / Group* imperative-versus-noun split cannot be
  expressed; it is not needed either, because the Hindi imperatives are
  different words (`रखिए`, `भेजिए`, `समूहबद्ध कीजिए`).
* **`AMBIG_POLICY = "drop"`** — the university convention, and load-bearing
  here: *कोटि* is `def:b1:findim:rank` in ch. 19 and `def:b1:linmaps:rank` in
  ch. 20 with no dominant first sense, exactly as English *rank*.

### Devanagari word-boundary trap — verified closed

`tools/termlink/morphology.py` used to leak word boundaries in Devanagari
(Python's `\w` is false for matras, virama, nukta and anusvara), so terms matched
*inside* longer words. That is fixed upstream, and it was re-verified here rather
than assumed: a script re-read all 3 668 generated links and checked the
character on each side of every one. **Zero** links are adjacent to a Devanagari
letter, matra or virama; the only Devanagari character ever touching a link is
the sentence-final danda `।`, which is correct. No `EXTRA_PROTECT`/`DROP`
work-around was needed for this class.

### Link-count reconciliation against English

| | EN | HI |
|---|---:|---:|
| total `\omterm` | 3 944 | 3 668 (93.0 %) |
| distinct targets used | 106 | 106 — **identical sets** |

The 276-link gap is **one cause**, and it is not curation. `lang_hi.py` sets
`WORD_TAIL = ''` and `DERIVE = False`, so **no inflected form is generated at
all** and every oblique plural is unreachable. Counting only the surfaces of 14
common heads that are not already inside a link:

| Unreachable surface | count |
|---|---:|
| समुच्चयों | 64 |
| बहुपदों | 47 |
| उपसमष्टियाँ / उपसमष्टियों | 34 |
| श्रेणियों | 19 |
| क्रमचयों | 18 |
| समाकलों | 12 |
| … 14 heads × 6 tails, total | **320** |

320 unreachable surfaces on 14 heads alone exceed the whole 276-link gap, and
they land exactly where the gap is: `def:b1:poly:def` −49, `def:b1:logic:sets`
−30, `def:b1:vspaces:subspace` −28, `def:b1:topology:closure` −27,
`def:b1:series:def` −17. The three targets where Hindi links *more* than English
are the mirror image — Hindi spells out what English abbreviates
(`thm:b1:arith:gcd` 14 vs 1, because English writes `$\gcd$`), or reaches a form
English's own `WORD_TAIL` cannot spell (`def:b1:reals:bounds` 82 vs 64).
`def:b1:logic:inj` is 214 vs 179 for a third reason: Hindi's three linked
surfaces are *एकैकी* (121), *आच्छादक* (51) and *एकैकी आच्छादक* (42), and the
first of these also stands where English writes the unlinked noun *injection*.

## What was sampled for this score

I did not write 48 of these 50 files, so they were sampled deliberately, not
skimmed:

* **Chapter openings** — 1 (logic), 2 (counting), 24 (plane curves), 25 (mine).
* **Definitions** — 1 (statement/connectives, quantifiers), 13 (limit,
  continuity, uniform continuity), 24 (parametrized curve), 25 (topology of
  $\R^2$, partial derivatives).
* **Proofs** — 1 (computation rules, negation of quantifiers), 14 (Fermat's
  interior-extremum), 16 (Landau algebra, Taylor with integral remainder), 17
  (comparison test), 25 (tangent plane, chain rule).
* **Exercise stems** — 6 (arithmetic), 18 (vector spaces), 21 (matrices), 25.
* **Solutions** — 19 (common supplementary, in full), 20 (ex. 9–11, the overfull
  paragraph), 23 (normal equations), 25 (all 13, mine).
* **Perspective remarks** (the register's hardest passages, since they are pure
  prose) — 20, 21, 22, 23, 25.
* **Whole-book scripted checks** — solution headers vs chapter titles (25/25),
  the label/cref/solution-key diffs, the English-function-word sweep, the
  Devanagari-adjacency scan of every link, and the five prose-gate classes.

## Sampled prose — verdicts

> प्रत्येक तुल्यता सत्य सारणियों की तुलना से जाँची जाती है: $P$, $Q$, $R$ से
> बने दो संयुक्त कथन ठीक तब तुल्य हैं जब वे (चार या आठ) प्रत्येक स्थिति में एक
> ही सत्य-मान लेते हों। […] प्रतिधनात्मकता के लिए एक शाब्दिक संक्षेप तेज़
> पड़ता है। (ch. 1, proof of the computation rules)

**Native.** `जाँची जाती है`, `तेज़ पड़ता है`, `सत्य-मान` — this is how a Hindi
lecturer talks, not how English word order looks in Devanagari.

> हर एक परिभाषाओं की छोटी-सी हेराफेरी है […] (4) के दो अंश अपनी-अपनी पंक्ति के
> अधिकारी हैं। […] तुल्यता $f \sim g \iff f = g + o(g)$ परिभाषा को दो बार पढ़ना
> ही है। (ch. 16, proof of the Landau rules)

**Native.** *"each one is a small manipulation of the definitions"*,
*"the two halves of (4) deserve a line each"*, *"is just reading the definition
twice"* — the English's dry humour survives as Hindi idiom (`हेराफेरी`,
`अपनी-अपनी पंक्ति के अधिकारी`), not as a calque.

> वर्ष उच्चतर विमा में पहली चहलकदमी के साथ समाप्त होता है: दो वास्तविक चरों के
> फलन $f(x, y)$। सब कुछ सामान्यीकृत हो जाता है --- सीमाएँ, सांतत्य, अवकलज, चरम
> --- पर हर धारणा में एक नया मोड़ आ जाता है। (ch. 25 opening, written in this
> pass)

**Native.** *"a first walk into higher dimension"* → `पहली चहलकदमी`, *"each
notion gains a twist"* → `एक नया मोड़ आ जाता है`. Compare the machine version it
replaced: `वर्ष का अंत उच्च आयाम में पहली बार चलने के साथ होता है: कार्य $f(x,
y)$ दो वास्तविक चरों में से` — *work*, not *function*, and English word order
verbatim.

> एक ही बिंदु ने स्पष्ट रूप से बढ़ती प्रवृत्ति को हलकी घटती प्रवृत्ति में बदल
> दिया। वर्ग-त्रुटि हर अवशेष पर $\varepsilon^2$ वसूलती है, अतः एक ही दूर बैठा
> बिंदु […] दोनों पर हावी हो जाता है: न्यूनतम वर्ग दक्ष तो हैं, सुदृढ़ नहीं।
> (solutions ch. 25, q. 22, written in this pass)

**Native.** `वसूलती है` (*charges*), `दूर बैठा बिंदु`, and the closing
`दक्ष तो हैं, सुदृढ़ नहीं` reproduce the English's clipped verdict *"efficient
but not robust"* as an idiom rather than a gloss.

> \cref{ch:b1:multivar} प्रवणता को कोशी--श्वार्ट्ज़ के द्वारा पढ़ता है (तीव्रतम
> आरोहण) और खंड को न्यूनतम वर्गों के साथ बंद करता है, जो $\R^n$ के किसी
> आँकड़ा-सदिश पर लगाया गया \cref{thm:b1:euclid:projection} ही है। अंतर्गुणन वही
> बिंदु है जहाँ इस पुस्तक का बीजगणित और उसका विश्लेषण अंततः मिलते हैं।
> (ch. 23, perspectives remark)

**Native.** Long, hinged, entirely idiomatic — and it is the sentence that
*forced* ch. 25's vocabulary, since chapters 20–23 had already committed to
`प्रवणता`, `न्यूनतम वर्ग` and `आँकड़ा-सदिश`.

> $\R^3$ में स्वतंत्रता तय कीजिए: $\;\bigl((1,1,0), (1,0,1), (0,1,1)\bigr)$ […]
> (ch. 18, exercise 3)

**Native.** Terse imperative exercise register, the same length as the English.

*No sampled passage scored below near-native. The two files re-translated in
this pass were read end to end against English line by line; the other 48 were
sampled as listed above.*

## Why not 100 — ordered gap list

1. **`lang_hi.py` generates no inflected forms, so ~7 % of English's links are
   unreachable in Hindi.** `WORD_TAIL = ''`, `DERIVE = False`. Hindi's oblique
   plural (`-ों`, `-ओं`, `-एँ`, `-यों`) is the single most common form of every
   technical noun in running prose, and it never links. This is the whole of the
   276-link gap and the reason the link dimension scores 94. **See the request
   below — this file cannot fix it.**
2. **Seven correct-sense links were removed for target parity.** *लघुत्तम
   समापवर्त्य*, *कोणांक*, *संयोजन-नियम*, *सम्मिश्र निर्देशांक*, *त्रिभुज
   असमिका*, *समकाल वक्र*, *सदृश आव्यूह* are each the notion the target defines;
   they were dropped only because English never links that target. Parity was
   chosen over local completeness because a divergent target set is the defect
   `CLAUDE.md` gates on. Each is documented in the config, so the decision is
   reversible if the policy ever changes.
3. **`प्रवणता` carries two senses and is solved by confinement, not by
   distinction.** Gradient (ch. 25) and slope (ch. 4, 11, 14, 24) are one word in
   this vocabulary. `STOP` gives exactly English's link footprint, but a Hindi
   reader in ch. 24 sees an unlinked word that ch. 25 defines. Coining a
   two-word *prāvaṇatā sadish* would have been padding, so confinement won.
4. **The MT-artifact sweep is heuristic.** It greps English function words and
   the five prose-gate classes; a calque phrased in fully Hindi words — an
   unidiomatic postposition, say — would pass it. Roughly 40 passages were read
   end to end; the rest of the ~1.4 MB was sampled.
5. **`\index{}` sort order was not audited.** 213 Hindi keys; Devanagari sorts
   under `makeindex`'s byte order, which is Unicode code-point order and is
   *nearly* but not exactly Devanagari alphabetical order (nukta forms and
   pre-composed characters can misfile). No `@`-sort keys were added beyond the
   ones English already had. The printed index has not been proof-read.
6. **`NOT_A_TERM` cannot be tightened without collateral damage.** Bare `नियम`
   must stay (it stops *क्रामर का नियम*), which costs one hand-written `EXTRA`
   per genuine `…नियम` term. A future chapter introducing another one will
   silently lose its links until someone notices.
7. **No Hindi hyphenation patterns are loaded.** The zero-overfull result rests
   on Devanagari's `\emergencystretch` behaviour with unhyphenated words; 121
   underfull boxes (same band as PT/ES) are the price. A future TeX Live with
   Devanagari patterns would change line breaks and the page total slightly.

## Shared-file change requested — **NOT APPLIED HERE**

`tools/term_config/lang_hi.py` is orchestrator-owned, so this is a request, per
`hindi_style_card.md` §6.

```python
WORD_TAIL = r''            ->   r'(?:ों|ओं|एँ|ें|याँ|यों)?'
```

This is the same request the Math 2 agent raised and the status file lists as
"known, out of scope"; **Book 3 now quantifies it.** With `TAIL_ON_EVERY_WORD`
left `False` (Hindi compounds inflect only the head, unlike Portuguese), it would
recover on the order of 300 links in this book alone and close most of the gap
against English without adding a single hand-written `EXTRA`. It changes every
Hindi book's link layer, so it should land in one deliberate pass across all six
editions, exactly as `lang_pt.py`'s `TAIL_ON_EVERY_WORD` did — not book by book.

Two cautions for whoever applies it:

* `ें` is ambiguous — it is the plural of `-ा`-less feminines (`प्रमेय` →
  `प्रमेयें`) but also a verb ending (`करें`, `लें`). Because the tail is only
  ever appended to a *harvested term*, a verb can only be hit if a term happens
  to be a verb stem; none currently is, but the config's `DROP` list should be
  re-checked after the flip.
* After the flip this book's `EXTRA` should be re-tested: *संतत* / *अवकलनीय* /
  *सहगुणनखंड-प्रसार* / *मीनार नियम* / *ऑयलर का अचर* are **not** plural
  work-arounds and must all stay.

Nothing else on any shared file is outstanding. `styles/`, `latexmkrc`,
`tools/check_translation.sh`, `tools/check_hindi_prose.py`,
`tools/term_config/lang_hi.py`, `tools/termlink/` and `tools/link_defined_terms.py`
were **not** touched by this pass.

## Status

**Meets the ship threshold (≥ 95): 96 / 100.** Book 3 Hindi is complete: 50 of
50 files re-translated from English, 0 errors / 0 undefined / 0 overfull /
386 pp, every gate green, and `\omterm` target parity with English exact. No git
commit was created; the working tree is left for human review.
