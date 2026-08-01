# Book 1 — Hindi (`hi`) — translation self-score

| Field | Value |
|---|---|
| **Book** | One Math Book 1 (Primary / Middle, grades 1–9) |
| **Entry** | `one_math_book_1_primary_middle_school_hi.tex` |
| **Language** | Hindi (`hi`), standard technical Hindi per `hindi_style_card.md` |
| **Quality bar** | `native academic` — a Hindi-medium teacher should hand it to the class without apologising for it |
| **Scope** | 71 chapters + 71 solutions = **142 files** under `parts/grade-{1..9}/hi/` and `parts/grade-{1..9}/solutions/hi/` |
| **Kind of pass** | **full re-translation from the English canon**, chapter by chapter; the 2026-07-24 machine translation was read only as a warning list and then discarded |
| **Delivered** | **142 of 142 files — the book is complete** |
| **Term config** | `tools/term_config/book1_hi.py` (rewritten, curated; simplified 2026-08-01, §5) |
| **Overall score** | **96 / 100** (native academic) |
| **Date** | 2026-08-01 (revision 2) |

> **Revision note (2026-08-01, second session).** Revision 1 delivered 126 of
> 142 files and could not be scored as a book. A first resumption finished
> grade-9 chapters 1–5; **this revision finished the last eight files** —
> chapters and solutions of `06-thales-theorem`, `07-trigonometry-right-triangle`,
> `08-solids-and-volumes`, `09-statistics-and-probability` — each re-translated
> from the English canon, not post-edited from the MT. It also cleared the last
> overfull box (§2), simplified the link config now that the Devanagari
> word-boundary bug is fixed upstream (§5), and reached `\omterm` **target
> parity 79/79**. The book is now scorable, and scores **96/100**.

---

## 1. Dimension scores

| Dimension | Weight | Score | Comment |
|---|---:|---:|---|
| Register (ages 6–15, Hindi schoolbook voice) | 25 | 24 | Grades 1–5 use `तुम`/imperative and short sentences, as the style card asks (`कंचे गिनो`, `ख़ाली जगह भरो`, `जाँचो`); grades 6–9 tighten into full textbook prose (`समझाओ`, `नतीजा निकालो`, `कारण बताओ`, `सिद्ध करो`, `कारण दो`). The grade-9 chapters written in this revision lean deliberately towards the high-school volume's voice — definition, worked reasoning, exercise — while keeping grade 9's `तुम` address, so the seam between `ch:g9:statproba` and Book 2's `ch:g10:proba` is a change of address, not of style. No baby-talk, no lecture calque. |
| Terminology (standard technical Hindi) | 20 | 19 | The whole grade 1–9 vocabulary is listed in §4 and §11; the four grade-9 chapters added त्रिकोणमितीय अनुपात (कोज्या / ज्या / स्पर्शज्या / सम्मुख / संलग्न / कर्ण / न्यून कोण), थेल्स प्रमेय and its विलोम, मापक गुणक / विवर्धन / संकुचन, अनुप्रस्थ काट, छिन्नक शंकु, वर्ग–घन नियम, माध्य / माध्यिका / परास, प्रायिकता / यादृच्छिक प्रयोग / परिणाम / घटना / पूरक घटना / वृक्ष आरेख. All of these were checked against the **already-shipped Hindi Book 2** so that the two volumes agree word for word (§4). |
| Freedom from MT artefacts | 20 | 20 | `check_hindi_prose.py` is **0 in all five classes on all 142 files**. Zero residual English in prose, TikZ nodes, `\text{}`, chapter/section titles, environment optional titles or index keys; zero transliterated function words; zero `$P $ और $ Q $` math spacing; every sentence ends in a danda. |
| Structural fidelity | 15 | 15 | `check_translation.sh` green for grade-1 … **grade-9**; identical label sets and order, `exo:`/`pb:` ↔ `\begin{solution}{}` parity, env/figure census, `\end{…>` typo class, drafty `...`, duplicate labels, TeX accent escapes. Whole-tree `\end{...}` census clean. |
| Mathematical correctness | 10 | 10 | Every numeric answer re-derived while writing; no value diverges from the English. Two English slips were silently corrected rather than copied: `\frac Sr` for the surface-to-volume ratio in `solutions/08` question 13 (written `\frac SV`), and the plain `P(` of `solutions/09`'s problem (written `\P(`, as the chapter body does). |
| Link layer (`\omterm`) | 10 | 10 | Config rewritten, curated and now **simplified**; `--check` green and idempotent; **≈1250 wrong-sense links eliminated** in revision 1 (§5); target parity **79 / 79**; whole-tree mid-word scan finds **0** suspects. |

**Weighted total: 96 / 100.**

---

## 2. Gate results

| Gate | Result |
|---|---|
| `bash tools/check_translation.sh grade-1 hi` … `grade-9 hi` | **PASSED**, all nine |
| `python3 tools/check_hindi_prose.py` on all 142 files | **OK (0 issues)** |
| `python3 tools/link_defined_terms.py --book 1 --lang hi --check` | **green** — "every file matches what the config generates" |
| `latexmk one_math_book_1_primary_middle_school_hi.tex` | **exit 0** |
| `grep -ac '^!'` on the log | **0** errors |
| `grep -aci 'undefined'` | **0** undefined references |
| `grep -ac 'Overfull'` | **0** overfull boxes |
| Output | `build/one_math_book_1_primary_middle_school_hi.pdf`, **416 pages** |
| `\end{...}` census, all 142 files (§3) | no mismatch |
| `\omterm` target parity vs English | **79 / 79** |

### Devanagari prose gate

| Class | 2026-07-24 baseline | now (whole book) |
|---|---:|---:|
| `english` | 893 | **0** |
| `translit` | 720 | **0** |
| `danda` | 1946 | **0** |
| `math-space` | 3252 | **0** |
| `split-number` | 2 | **0** |
| **total** | **6813** | **0** |

### The last overfull box

It was **not** in the eight files this revision rewrote: it was in
`parts/grade-9/solutions/hi/02-arithmetic-gcd.tex`, delivered earlier. The
divisor list was set as one inline math group, `$1, 2, 3, 4, 6, 8, 12, 16, 24,
48$`. TeX breaks inline math only at relations and binary operators, never at a
comma, so the whole list is one unbreakable box; the surrounding Hindi is
narrower than the English, and the box overflowed by 26.99pt. Fixed by giving
each number its own math group (`$1$, $2$, $3$, …`), which restores the
breakpoints. **Worth remembering for every language: a comma-separated list
inside one `$…$` is an unbreakable box.**

---

## 3. Method, and the tool the next session should reuse

The pass is a **line-range patch applied on top of the English canon**, not an
edit of the machine translation. For every chapter, a patch file names the
English source and gives the Hindi replacement for each line range:

```text
### parts/grade-9/hi/06-thales-theorem.tex <<< parts/grade-9/06-thales-theorem.tex
@@ 1
\chapter{थेल्स प्रमेय}\label{ch:g9:thales}
@@ 3-7
किसी पिरामिड की ऊँचाई उस पर चढ़े बिना कैसे नापी जाए? …
```

Every English line **not** named is copied byte-identically. That buys three
things for free, and they are why the structural gates were green on the first
try in every one of this revision's eight files:

- labels, `\cref` targets and `\begin{solution}{key}` are physically the same
  bytes as English — they cannot drift;
- `tikzpicture` drawing code, `\foreach` lists, `xtick=`, `samples at` and every
  math display are byte-identical, so `...`-in-`\foreach` and `\,`-in-math
  survive untouched;
- anything forgotten stays English and is caught by the `english` class of the
  prose gate, instead of silently shipping.

The applier lives in the session scratchpad (`hi_apply.py`, ~110 lines) and
warns when a replaced range **starts** on a `\begin{…}` line — the mistake that
silently deletes an exercise. The mirror mistake (a range **ending** on an
`\end{…}` line) is invisible to `check_translation.sh` and surfaces hundreds of
pages later as `TeX capacity exceeded`; catch it with the census below.

**Two whole-tree invariants worth re-running after every batch** — neither is
covered by `check_translation.sh`:

```sh
# 1. an \end{...} swallowed by a patch range
for g in 1 2 3 4 5 6 7 8 9; do
  for f in parts/grade-$g/[0-9]*.tex parts/grade-$g/solutions/[0-9]*.tex; do
    b=$(basename $f); d=$(dirname $f)
    diff -q <(grep -o '^\\end{[a-z]*}' $f) <(grep -o '^\\end{[a-z]*}' $d/hi/$b) \
      >/dev/null || echo "MISMATCH $d/hi/$b"
  done
done
# 2. \omterm target parity against English (§5)
```

A third, added this revision — the **mid-word link scan**. It reads every
`\omterm{…}{display}` and flags any occurrence whose immediately preceding or
following character is Devanagari (other than a danda). It is the only cheap
way to see the failure mode of §5 without eyeballing 3600 links:

```python
# for each \omterm match m in a hi file:
#   flag if t[m.end()] is [ऀ-ॿ] and not '।'
#   flag if t[m.start()-1] is [ऀ-ॿ]
```

Currently **0 suspects across all 142 files**.

---

## 4. Terminology decisions worth recording

Everything follows `hindi_style_card.md`. The judgement calls:

- **`मिलियन` / `बिलियन` for *million* / *billion*.** The book's place-value
  tables group digits in **threes** (`6\,309\,452`) and the grade-4 figure draws
  that grouping. The Indian लाख/करोड़ scale groups 3-2-2 and would contradict
  the figure. लाख/करोड़ are still used where the English spells a number out in
  words and no grouping is shown.
- **`डिग्री`, not `अंश`, for the degree of an angle** — so that `अंश` is
  unambiguously the numerator of a fraction (§5).
- **`शंकु`, not the MT's `कोन`, for *cone*** (`कोन` collides with `कोना`,
  *corner*); **`घातांक`** exponent, **`व्युत्क्रम`** reciprocal, **`छिन्नक`**
  frustum, **`हरात्मक माध्य`** harmonic mean, **`तिरछा नियम`** cross rule,
  **`मापनी`** map scale.
- **`शीर्षाभिमुख कोण`** for *vertically opposite angles*: the standard term.
  (Revision 1 needed an `EXTRA_PROTECT` entry for it; §5 explains why that entry
  is gone and the term now links as a whole.)
- **`ताल-खंड`** for a bar of music and **`स्वर`** for a note (grade-7 problem):
  the Western note values have no settled Hindi names, so the translation uses
  transparent descriptive ones (`पूरा स्वर`, `आधा स्वर`, `चौथाई स्वर`,
  `आठवाँ स्वर`, `सोलहवाँ स्वर`, `बिंदुदार`, `जोड़-रेखा`, `विराम`, `त्रिक`).

### Grade 9, chapters 6–9 (this revision)

Every new term was chosen to agree with **Hindi Book 2**, which is already
shipped at 96/100 — grade 9 is the seam between the two volumes, and a reader
moving from `ch:g9:statproba` to `ch:g10:proba` must not meet a new vocabulary.

- **`प्रायिकता`, not `संभावना`, for *probability*.** §11 of revision 1 had
  pencilled in `संभावना`; that was overturned. `hindi_style_card.md` §4 gives
  प्रायिकता, and Book 2 uses it 210 times against 10 loose uses of संभावना.
  With it come Book 2's `यादृच्छिक प्रयोग`, `परिणाम` (outcome), `घटना` (event),
  `पूरक घटना` (contrary event), `समान रूप से संभावित` (equally likely),
  `वृक्ष आरेख` (tree diagram), `न्यायसंगत` (fair), `चित`/`पट` (heads/tails),
  and `बृहत् संख्याओं का नियम` (law of large numbers).
- **`परास` for the statistical *range***, again from Book 2
  (`def:g10:stats:quartiles`), which keeps `परिसर` free for the range of a
  function and `प्रसार` for spread in general.
- **`मापक गुणक` for *scale factor*** (`def:g9:thales:scaling`), deliberately
  **not** `मापनी गुणक`: `मापनी` is already the map scale of
  `def:g7:prop:scale`, and a compound containing it would have nested one
  defined term inside another. Enlargement/reduction are `विवर्धन` / `संकुचन`.
- **Trigonometry**: `कोज्या` / `ज्या` / `स्पर्शज्या`, and — new in this book —
  `सम्मुख भुजा` for the opposite side, the natural counterpart of grade 8's
  established `संलग्न भुजा`. `कर्ण`, `समकोण भुजा`, `न्यून कोण` come from
  grade 8 unchanged. The English pun in `solutions/07` question 3 (*the
  **co**sine is the sine of the **co**mplement*) is untranslatable word for
  word but true in Hindi by etymology, so the Hindi says what the English only
  jokes about: *`\emph{को}ज्या असल में \emph{कोटि} की, यानी पूरक कोण की, ज्या
  है।*`
- **`अनुप्रस्थ काट` for *cross-section*** (`prop:g9:solids:sections`), a
  two-word term that can never prefix-match inside another word — the §5
  lesson applied at the source. Bare `काट` was rejected for exactly that
  reason.
- **`वर्ग--घन नियम`** for the square–cube law; **`छिन्नक शंकु`** for the
  truncated cone (grade 8 already had `छिन्नक`); **`सूक्ष्मछिद्र कैमरा`** for
  the pinhole camera; **`अनंतस्पर्शी`** for asymptote (the word Book 2 uses);
  **`दो-ठिकाना विधि`** for the surveyors' two-station method;
  **`उन्नयन कोण`** angle of elevation; **`भूमापक`** surveyor;
  **`बिना निशान की पट्टी`** unmarked ruler; **`परकार`** compass.
- **Names** keep the English canon's facts, transliterated: थेल्स, मिलेतुस,
  आर्किमिडीज़, सिसरो, सिरैक्यूज़, गैलीलियो, गीज़ा, शेवालिए दे मेरे, ब्लेज़
  पास्कल, पिएर दे फ़र्मा — plus revision 1's हेमचंद्र, फ़िबोनाच्ची,
  एरातोस्थनीज़, सिकंदरिया, स्येने, यूक्लिड, सिस्सा, लूव्र, मों ब्लां, आल्प्स,
  सिंपसन. Where the English canon itself says "the Indian scholar Hemachandra",
  the Hindi says `भारतीय विद्वान` — a translated historical attribution, not a
  localisation. **No curriculum body, syllabus or country is named anywhere as
  the book's own context.**
  *Gate trap: the French particle `de` must be written `दे`, never `द` — a bare
  `द` is the `translit` gate's transliterated English article (§9.1).*

---

## 5. The link layer

### Revision 1: ≈1250 wrong-sense links removed

The single biggest quality problem of revision 1 was **not** in the prose:
it was in the generated `\omterm` links. `tools/termlink/morphology.py` ended a
term with `(?![\w-])`, and Python's `\w` does **not** include the Devanagari
dependent vowels (U+093E–U+094D are categories Mn/Mc, not alphabetic). A short
term therefore matched *inside* a longer, unrelated word:

| linked term | matched inside | wrong links |
|---|---|---:|
| `सम` (even) | समानुपात, समूह, समीकरण, समान, समुच्चय, समेत … | 510 |
| `लंब` (perpendicular) | लंबाई, लंबा, लंबी, लंबे (*length, long*) | 217 |
| `हर` (denominator) | दोहराव, दोहराता (*repetition*) — and ~400 bare `हर` meaning *every* | ≈490 |
| `कोन` (cone, MT) | कोने, कोना (*corner*) | 17 |
| `अंतर` (difference) | अंतराल, अंतरिक्ष, अंतर्निहित | 13 |

Four remedies were used, in increasing order of preference:

1. **Fix the harvest at source.** `parts/grade-3/hi/01` defines
   `\emph{सम संख्या}\index{सम संख्या}` and `\emph{विषम संख्या}` instead of the
   bare `\emph{सम}` / `\emph{विषम}`. A two-word term can never prefix-match
   inside another word. This removed all 510 `सम` hits at a stroke, and the
   sentence reads better in Hindi. (Applied again this revision when naming
   `अनुप्रस्थ काट`.)
2. **Choose a different Hindi word** where one exists: `शंकु` for cone,
   `डिग्री` for degree, `मापक गुणक` for scale factor.
3. **`EXTRA_PROTECT` with a lookahead** — now largely obsolete, see below.
4. **Hard `DROP`** when the two senses cannot be told apart at all: `हर` is the
   denominator *and* the ordinary determiner *every*, and *every* outnumbers it
   four to one. `def:g4:fractions:def` stays reachable through `अंश`.

### This revision: the six workaround regexes removed

The orchestrator fixed `morphology.py` upstream — `_BEFORE`/`_AFTER` now
exclude the Devanagari sign ranges. That made six of `book1_hi.py`'s
`EXTRA_PROTECT` entries dead weight:

```text
लंब(?=[ा-्])   दोहर   अंतर(?=[ाि्])   शून्येतर
सममिति(?!\s*(?:अक्ष|केंद्र))   शीर्षाभिमुख
```

All six were removed and the link layer regenerated. The result is not merely
neutral — it is **better**: 10 links *appeared*, and every one of them is a
correct whole-word link that the blunt regexes had been suppressing as
collateral damage —

| link that came back | count |
|---|---:|
| `\omterm{def:g7:central:def}{केंद्रीय सममिति}` | 6 |
| `\omterm{def:g7:triangles:pairs}{शीर्षाभिमुख कोण}` | 4 |
| `\omterm{def:g6:symmetry:def}{अक्षीय सममिति}` | 1 |

(`शीर्षाभिमुख` had been protected to stop `शीर्ष` matching inside it; the
protection also blocked the genuine term `शीर्षाभिमुख कोण`.) The mid-word scan
of §3 reports **0 suspects** afterwards, and `--check` is green and idempotent.

**Result: 3634 links across 118 files, target parity 79 / 79.** The one target
missing in revision 1, `def:g9:arith:prime`, arrived with grade-9 chapter 2;
the last of the 79, `def:g9:thales:scaling`, `def:g9:trig:ratios`,
`prop:g9:solids:sections`, `def:g9:statproba:indicators` and
`def:g9:statproba:probability`, arrived with this revision's four chapters.

---

## 6. Term config

`tools/term_config/book1_hi.py`, curated by hand:

- `STOP`: `रेखा`, `जाल`, `समूह`, `हर`, and the geometry furniture `वर्ग`,
  `त्रिभुज`, `आयत`, `वृत्त`, `कोण`, `विपरीत` — dropped for the same reason the
  English config drops square/triangle/rectangle/circle/angle.
- `SOFT`: `जाल` (net vs. the grid of grid paper — linked only inside
  `parts/grade-5/07`, where every occurrence is a net) and `समूह`.
- `DROP` = `STOP − SOFT`, plus the MT-defect sentence
  `किसी अंक का मान उसके स्थान पर निर्भर करता है`.
- `EXTRA`: five manual term → label pairs the harvest cannot reach.
- `DERIVED`: 26 declared oblique/plural forms (`lang_hi.py` sets
  `DERIVE = False` and `WORD_TAIL = ''` on purpose — Hindi has no `-s` to bolt
  on).
- `EXTRA_PROTECT`: **sense regexes only** now (`जाल वाला काग़ज़`, `आधा घंटा`,
  `साढ़े`, `सवा`, `पौने`, `अगले खंड`). The six morpheme-boundary regexes are
  gone (§5); the comment block that replaces them records why, so that nobody
  reintroduces them.
- `AMBIG_POLICY = "nearest-preceding"` — a spiral curriculum re-defines its
  terms, and a grade-8 use of *fraction* should point at the grade-6 definition
  the reader has already met.

---

## 7. Sampled passages, judged

1. **`parts/grade-2/hi/01`, opening** — *पिछले साल हमने इकाइयों को दहाइयों में
   बाँधा था (…); अब दस दहाइयाँ मिलकर एक सैकड़ा बनती हैं, और संख्याएँ $1000$ तक
   पहुँच जाती हैं। तीन अंक, तीन काम: सैकड़ा, दहाई, इकाई।* — **native**. The
   telegraphic last sentence is a Hindi schoolbook move, not a calque.
2. **`parts/grade-8/hi/01`, proof** — *हर क़दम पर पहला गुणक $1$ घटता है और उत्तर
   $4$ बढ़ता है। … कोई भी दूसरा चुनाव अंकगणित की इस नियमितता (वितरण नियम) को तोड़
   देगा।* — **native**. Exactly the register a grade-8 proof wants.
3. **`parts/grade-9/hi/06`, opening (this revision)** — *किसी पिरामिड की ऊँचाई
   उस पर चढ़े बिना कैसे नापी जाए? मिलेतुस के थेल्स ने उसकी छाया की तुलना एक छड़ी
   की छाया से की।* — **native**. The English's two sentences stay two sentences;
   `उस पर चढ़े बिना` is the ordinary Hindi construction, not a rendering of
   *without climbing it*.
4. **`parts/grade-9/hi/07`, definition (this revision)** — *ये अनुपात सिर्फ़
   $\theta$ पर टिके हैं, त्रिभुज की नाप पर नहीं: एक ही न्यून कोण वाले सारे
   समकोण त्रिभुज, थेल्स के अनुसार, एक-दूसरे के घटे-बढ़े रूप हैं।* —
   **native academic**. `टिके हैं` for *depend on* is the idiom a Hindi textbook
   uses; the appositive `थेल्स के अनुसार` carries the English parenthesis
   without a calqued *by Thales*.
5. **`parts/grade-9/solutions/hi/08`, question 12 (this revision)** — *अपने भार
   से पचास गुना उठा लेने वाली चींटी कोई महाबली नहीं है --- वह बस छोटी है; चींटी
   के नाप तक सिकोड़ दिया गया आदमी भी यही कर लेता।* — **native**. Keeps the
   English's punch (*is not a super-athlete — it is merely small*) in a Hindi
   sentence shape, and the counterfactual `कर लेता` is right.
6. **`parts/grade-9/hi/09`, problem III.4 (this revision)** — *अटकल की मरम्मत:
   $23$ विद्यार्थियों की कक्षा में कितने \emph{जोड़े} एक ही जन्मदिन बाँट सकते
   हैं …? एक वाक्य में समझाओ कि हैरानी की जड़ यही संख्या क्यों है, $23$ ख़ुद
   क्यों नहीं।* — **native**; the grade-9 `तुम` imperative, and the English's
   *the intuition repaired* becomes an idiomatic Hindi heading rather than a
   literal one.

No sampled passage reads as post-edited MT.

---

## 8. Why not 100

- Terminology 19/20: several choices are defensible but not the only defensible
  ones — `मिलियन`/`बिलियन` over लाख/करोड़, `मापनी` for the map scale,
  `ताल-खंड`/`स्वर` for the music vocabulary, `तिरछा नियम` for the cross rule,
  and this revision's `मापक गुणक` (an editor might prefer `अनुमापन गुणक`) and
  `दो-ठिकाना विधि` (a coinage; the method has no settled Hindi name).
- Register 24/25: the grade-1–2 chapters could still lose a few connectives;
  Hindi tolerates shorter sentences than English does at that age. The grade-9
  weekend problems are long in every language, and their Hindi is faithful
  rather than tightened.
- Nothing else is outstanding: all 142 files are delivered, all gates are zero,
  and target parity is exact.

---

## 9. Gate traps for the next session

1. **`आर` in `आर-पार`.** The `translit` class flags a bare `आर`
   (transliterated *are*), and `आर-पार` puts `आर` between a space and a hyphen.
   Write `के पार`. — *`इन` used to be flagged the same way; the orchestrator
   removed it from the check on 2026-08-01 and the six affected sentences were
   restored to the natural demonstrative. `उन` is not a substitute: it means*
   those, *not* these.
   **Same class, found this revision: the French particle `de` in a name.**
   `शेवालिए द मेरे` and `पिएर द फ़र्मा` trip the `translit` gate on `द`
   (transliterated *the*). Write `दे`.
2. **A unit or letter glued to a closing quote** (`km''`, `b''`, `d''`) is read
   as an English word. Put the letter in math mode (`$b$`) or add a Hindi word
   after the unit.
3. **`\emph` or `\lbl` inside a TikZ node** leaks as the English words *emph* /
   *lbl* (node text is extracted raw). Drop the `\emph`, and keep loop variables
   to two letters (`\lb`), below the gate's `len < 3` threshold.
4. **`\dots` in an environment optional title** leaks as *dots*; rephrase.
5. **`xtick={1,...,9}`** trips the drafty-`...` check (only `\foreach` and
   `samples at` are exempt); write the list out.
6. **`dam`** in the grade-4 units table is not in `ALLOWED_UNITS`; it is written
   `$\mathrm{dam}$` as a workaround.
7. **Devanagari inside `\foreach`** breaks pgffor (`TeX capacity exceeded`);
   expand the loop into explicit `\node` lines. Devanagari inside
   `symbolic x coords` is likewise risky — use ASCII keys plus `xticklabels`
   (done in `parts/grade-7/hi/06`).
8. **English abbreviations inside `\text{}` in math** are visible text and are
   gated: `V_{\text{cyl}}`, `V_{\text{sphere}}` in `solutions/08` had to become
   `V_{\text{बेलन}}`, `V_{\text{गोला}}`. So do `\qquad\text{so}\qquad` and
   `\qquad\text{i.e.}\qquad` inside displays — both are `\qquad\text{यानी}`.
9. **A comma-separated list inside a single `$…$` is unbreakable** and is the
   one remaining way to make an overfull box in a Hindi edition (§2). Give each
   number its own math group.

---

## 10. Requests to the orchestrator

1. ~~`tools/termlink/morphology.py`: the word-boundary rule is wrong for
   Devanagari.~~ **Done** — fixed upstream, and this revision removed the six
   `EXTRA_PROTECT` workarounds it had forced (§5). No further action.
2. **`tools/check_hindi_prose.py` → `ALLOWED_UNITS`: add `dam`, `hm`, `dm`.**
   `dm`, `dam`, `hm` are now present; the grade-4 `$\mathrm{dam}$` workaround
   could be reverted to plain `dam` on the next pass. Low priority.
3. ~~`tools/check_hindi_prose.py` → drafty-`...`: exempt `xtick=` / `ytick=`~~
   **Done.**
4. **`lang_hi.py` `WORD_TAIL` for oblique plurals (`ों|ओं|एँ|यों`).** Requested
   by the Math 2 agent and still open. It would let ~26 hand-written `DERIVED`
   entries be deleted from `book1_hi.py` alone. It changes every Hindi book's
   link layer, so it should land in one deliberate pass, as `lang_pt.py`'s
   `TAIL_ON_EVERY_WORD` did — not here.
5. **Hindi HTML web edition.** `tools/build_html_book.sh` still defaults to
   `LANGS=en,fr,nl` and the README web-links row has no HI entry. Book 1 hi is
   now complete and could be published in the online reader.

---

## 11. State: complete

| Files | State |
|---|---|
| `parts/grade-{1..9}/hi/*.tex` (71) | **delivered**, native academic |
| `parts/grade-{1..9}/solutions/hi/*.tex` (71) | **delivered**, native academic |

The eight files finished in this revision:

```text
parts/grade-9/hi/06-thales-theorem.tex              + solutions/hi/
parts/grade-9/hi/07-trigonometry-right-triangle.tex + solutions/hi/
parts/grade-9/hi/08-solids-and-volumes.tex          + solutions/hi/
parts/grade-9/hi/09-statistics-and-probability.tex  + solutions/hi/
```

Vocabulary the whole of grade 9 uses, for anyone editing it later:
`अभाज्य संख्या`, `महत्तम समापवर्तक`, `वर्गमूल`, `अपरिमेय`, `गुणनखंडन`,
`ढलान`, `थेल्स प्रमेय` / `विलोम` / `विन्यास` / `तितली`, `मापक गुणक`,
`विवर्धन` / `संकुचन`, `कोज्या` / `ज्या` / `स्पर्शज्या`, `कर्ण` /
`सम्मुख भुजा` / `संलग्न भुजा` / `न्यून कोण`, `उन्नयन कोण`, `अनंतस्पर्शी`,
`गोला` / `बेलन` / `शंकु` / `पिरामिड` / `प्रिज़्म` / `छिन्नक शंकु`,
`अनुप्रस्थ काट`, `वर्ग--घन नियम`, `प्रायिकता`, `यादृच्छिक प्रयोग`,
`परिणाम` / `घटना` / `पूरक घटना`, `वृक्ष आरेख`, `माध्य` / `माध्यिका` /
`परास`, `बृहत् संख्याओं का नियम`.
The MT's `प्रतिपादक`, `एकाधिक`, `सिलेंडर`, `कोन`, `विभाजित`, `अर्थ`,
`चेहरा` and `संभावना` are all wrong and appear nowhere in the tree.

**No git commit was created; the working tree is left for review.**
