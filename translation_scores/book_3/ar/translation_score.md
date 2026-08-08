# Translation score — Math Book 3 · Arabic (`ar`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 3 (University Year 1, `bachelor-1`) |
| **Language** | Arabic (`ar`) — Modern Standard Arabic, university lecture register (`arabic_style_card.md` §1) |
| **Quality bar** | **native academic** (English is the source of truth; the FR edition was consulted only as a sense/structure reference, never as a source) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **MET** |
| **Date** | 2026-08-08 |
| **Scope** | **Complete: 50 of 50 files.** Chapters 1–25 and their 25 solution files. Chapters 1–9 (18 files) were written in the first pass; chapters 10–25 (32 files), the term-link layer, the whole-book gates and this score in the second. |

## Verdict in one line

The Arabic edition of Book 3 is complete, structurally byte-exact against
English, mechanically proven to carry identical mathematics, gate-green on all
nine prose classes, term-linked with a curated vocabulary whose link *targets*
agree with English on 104 of 106, and it builds to 373 pages with zero errors,
zero undefined references and zero overfull boxes.

## Status per file

All 50 files exist, all are gate-green.

| Chapter | body | sol. | | Chapter | body | sol. |
|---|---|---|---|---|---|---|
| 01 Logic, Sets and Maps | ✅ | ✅ | | 14 Differentiation | ✅ | ✅ |
| 02 Counting | ✅ | ✅ | | 15 Integration | ✅ | ✅ |
| 03 Complex Numbers | ✅ | ✅ | | 16 Taylor and Asymptotics | ✅ | ✅ |
| 04 Standard Functions | ✅ | ✅ | | 17 Numerical Series | ✅ | ✅ |
| 05 Linear Differential Equations | ✅ | ✅ | | 18 Vector Spaces | ✅ | ✅ |
| 06 Integer Arithmetic | ✅ | ✅ | | 19 Finite Dimension | ✅ | ✅ |
| 07 Algebraic Structures | ✅ | ✅ | | 20 Linear Maps | ✅ | ✅ |
| 08 Polynomials | ✅ | ✅ | | 21 Matrices | ✅ | ✅ |
| 09 Rational Fractions | ✅ | ✅ | | 22 Determinants | ✅ | ✅ |
| 10 Real Numbers | ✅ | ✅ | | 23 Euclidean Spaces | ✅ | ✅ |
| 11 Sequences | ✅ | ✅ | | 24 Plane Curves | ✅ | ✅ |
| 12 Topology of ℝ | ✅ | ✅ | | 25 Two-Variable Functions | ✅ | ✅ |
| 13 Limits and Continuity | ✅ | ✅ | | | | |

## Gate results

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-1 ar` | **PASSED** — completeness 50/50, `\label` sequence identical to English in all 25 chapters, env + figure census identical, UTF-8 clean, no TeX accent escapes |
| `python3 tools/check_arabic_prose.py parts/bachelor-1/ar parts/bachelor-1/solutions/ar` | **OK (50 files)** — 0 hits in every one of the nine classes (`english`, `translit`, `punct`, `digits`, `math-space`, `bidi-ctrl`, `presform`, `tatweel`, `split-number`) |
| `python3 tools/link_defined_terms.py --book 3 --lang ar --check` | **CHECK: every file matches what the config generates** (3026 links, 223 linkable terms) |
| `latexmk one_math_book_3_university_year_1_ar.tex` | exit 0 · **0 errors · 0 undefined · 0 overfull** · 373 pp |
| exercise ↔ solution key parity | exact for all 25 chapters (`label{exo|pb:…}` vs `begin{solution}{…}`) |
| duplicate labels / `\end{env>` typos / drafty `...` | none |

## Structural verification (by script, not by eye)

* `diff` of the `\label{…}` sequence, English vs Arabic: **empty for all 25
  chapters** — labels, `\cref` targets and solution keys were never translated.
* **Mathematics is byte-identical to English**, enforced mechanically: the
  build step of the translation pipeline refuses to write a file unless the
  *multiset* of every math span (`$…$`, `\[…\]`, `align`-family bodies) equals
  the English original's, modulo `\text{…}` bodies (which must be Arabic) and
  two documented normalisations (below). It caught roughly one real defect per
  file — a dropped `$s$`, an invented `$0$`, `$u_n \in A$` split into two
  spans, `$x, y \to \infty$` truncated — every one of which would otherwise
  have shipped silently.
* Environment census (`definition theorem proposition lemma corollary example
  remark method notation exercise problem proof tikzpicture omfigure`), chapter
  and solutions, English vs Arabic: **no divergence in any of the 50 files**.
* **Index keys**: 247 `\index` calls in Arabic, 247 in English. The EN ∩ AR
  intersection of index *keys* is exactly **one** entry, `Z/nZ@$\Z/n\Z$` (a
  symbol, identical on purpose) — i.e. no English key was left behind while its
  visible `\emph{}` was translated, the failure mode that orphan-splits the
  index. A normalisation sweep (diacritics/hamza/ta-marbuta folded) found one
  near-duplicate pair, `عدد متسام` / `عدد متسامٍ`, now unified to `عدد متسام`.

## The pipeline (throwaway, lived in the scratchpad — described here so it can be rebuilt)

Two commands, `mask` and `build`, over a marker syntax `@@n@@`:

1. **`mask english.tex → masked.txt + map.json`**
   * `\omterm{lab}{disp}` is unwrapped to `disp` first.
   * Masked into numbered markers: comments; `tikzpicture`/`axis` bodies;
     `equation`/`align`/`gather`/… bodies; inline math longer than 22
     characters and all display math; `\label` `\cref` `\Cref` `\ref` `\eqref`;
     `\begin{solution}{key}`; `tabular` column specs; spacing/graphics macros.
   * **Left visible on purpose**, because the translator must see or translate
     them: short inline math (copied verbatim — this halved the number of
     opaque markers and made the prose readable); the body of `\text` /
     `\intertext` / `\mbox` inside masked math; TikZ node text and
     `xlabel=`/`ylabel=`/`title=` values; `\index{…}` keys.
   * Exposure is decided **structurally, never by content**, so masking the
     English file and masking the finished Arabic file produce the *same*
     marker numbering — which is what makes the working file recoverable from
     the committed `.tex` at any time (verified: the maps compare equal).
2. **`build arabic.masked + map.json + english.tex → arabic.tex`** refuses to
   write unless: every marker reappears **exactly once**; the environment
   census matches English; the `\label` sequence matches English; and the
   multiset of mathematics matches English. Two documented normalisations:
   * a tikz node positioned at `({cos(72)},{sin(72)})` is rewritten to polar
     `(72:1)` — the prose gate reads a node's first braced group as its label
     and would report `cos` as residual English (the Hindi edition made exactly
     this rewrite by hand, in the same ch. 3 figure);
   * a stray space before the closing `$` of an inline span (present in the
     English source in three places) may be removed, because the Arabic
     `math-space` gate rejects it. Hindi removed the same spaces.
3. A one-line `autofix` pass rewrites the Arabic proclitics `فـ` / `لـ` / `بـ`
   before math or a marker into `فإن` / `للمقدار` / `بالمقدار`. Arabic binds
   those particles to the front of a word, and a writer reaches for a
   **tatweel** (`ـ`, U+0640) to detach them before a formula; the tatweel gate
   rejects it. This was the single most frequent mechanical defect — about 15
   per chapter before the autofix, zero after. Residual tatweels that the
   autofix cannot repair (`بـ\emph{كل}`, `فـ«العمودي»`, `لـلمجموعة`) are
   reported and were removed by **rewording**, never by deleting the particle.
4. A per-block differ (`wh.py`) splits English and Arabic at
   `\begin{solution}` / `\textbf{N.}` / statement environments and reports the
   first divergent block with context — this turned each math-multiset failure
   from a file-wide hunt into a one-minute fix.

Round-trip was proven before any translation started: masking then rebuilding
all 50 English files reproduced them **byte-identically**.

## Term linking

Run over the finished tree, then curated, then regenerated:

```
python3 tools/link_defined_terms.py --book 3 --lang ar --unwrap --apply
python3 tools/link_defined_terms.py --book 3 --lang ar --apply
python3 tools/link_defined_terms.py --book 3 --lang ar --check
```

| | seed config | curated |
|---|---|---|
| linkable terms | 243 | **223** |
| links inserted | 3211 | **3026** |
| distinct targets | — | **104** (English: 106) |

For scale: English Book 3 carries 3944 `\omterm`, FR 4511, NL 3914; the Arabic
editions of Books 4 and 5 sit at 46 % and 51 % of their English twins. Arabic
Book 3 lands at 77 %, which is deliberate and not laxity: Arabic proclitics
(`ال و ف ب ك ل`, glued to the front of *every* word of a noun phrase) make a
short term fire far more often than its English twin, so the curation went
after **senses**, not volume — every entry below was found by reading the real
occurrences in this tree, and the resulting link set was checked target by
target against English.

`tools/term_config/book3_ar.py` now carries:

* `STOP` (8 words, closed under prefixing `ال`, so bare and definite forms are
  both covered): `منتهية` (EN *finite*), `مرافق` (EN *conjugate*),
  `كثير الحدود المميز` (EN *characteristic polynomial*), plus four
  Arabic-only traps — `صورة` (image of a map vs. «في صورة» = *in the form of*,
  ~70 uses each way), `أثر` (trace vs. «بأثر رجعي» / «الأثر الفلسفي»),
  `الجزء الصحيح` (the floor of ch. 10 vs. the polynomial part of ch. 9), and
  `تجزئة` (see the known divergence below).
* `DROP` (also closed under `ال`): the ordinary-register words English drops
  for the same reason — `طول`, `داخل` (the preposition *inside* is spelled
  exactly like the topological interior), `تماثل`, `مباشرًا`, `حرجة`, `جبريّ`,
  `متسامٍ`, `متكافئتان` — plus seven result-names that reach the harvest
  through `\emph{}\index{}` and one mis-target (`عدد أصمّ`, whose `\index` sits
  inside the ch. 19 tower-law problem).
* `EXTRA`: `متصلة` and `قابلة للاشتقاق` (the definitions emphasise the
  compound «متصلة عند $x_0 \in I$», so the bare adjective — the form the book
  uses ~150 times — is never harvested), `ثابت أويلر` → `pb:b1:series:1`
  (as `book3_en.py` does), `خاصية أرخميدس` and `قانون البرج` (filtered out of
  the index-only harvest by `NOT_A_TERM`'s «خاصية» / «قانون», yet named
  repeatedly afterwards), and three inflected forms of *coprime*
  (dual/plural — Arabic inflects the whole three-word phrase).
* `EXTRA_PROTECT` (all with `\s+`, never a literal space, and never consuming
  a `$`): `بجوار` / `في جوار` (= *near*, the trap `book5_ar.py` documents),
  `(?:ال)?أساس\s+(?=\$(?![(\\]))` — «الأساس $b$ / $2$ / $10$ / $p$» is the
  **base of a numeral system** in ch. 6, 10 and 17, whereas a basis is always
  written with a tuple «الأساس $(e_1, \dots, e_n)$», so the lookahead splits
  the two senses without touching the formula; `صورة مغلقة` (EN protects
  *closed form* for exactly this), `في صورة`, and `عبارةٌ عن` (= *is nothing
  but*, not the logical statement of ch. 1).

**Target parity against English** — `\omterm` first arguments, sorted unique:
104 Arabic vs 106 English, **101 shared**.

| In English only | why |
|---|---|
| `thm:b1:logic:partition` | see below |
| `def:b1:diffeq:linear2` | English says *characteristic polynomial* five times in ch. 5; the Arabic chapter names «كثير الحدود المميز» once, at the definition itself, and refers to it afterwards through the equation, so there is nothing left to link |
| `def:b1:curves:def` | English has a single link (*Parametrized curves*, in a heading-adjacent sentence); the four Arabic occurrences of «منحن معلَّمي» all sit inside protected spans (the `\emph{}\index{}` definition and a `\begin{method}[…]` title) |

| In Arabic only | why |
|---|---|
| `def:b1:complex:expi` | «عمدة» (*argument* of a complex number) is unambiguous in Arabic; English must drop *argument* because of "the same argument shows" |
| `def:b1:structures:law` | «قانون التركيب» is a genuine definition, not a result-name; English's default `NOT_A_TERM` swallows *composition law* |
| `def:b1:arith:lcm` | Arabic writes «المضاعف المشترك الأصغر» in prose where English writes `lcm` |
| `prop:b1:logic:rules`, `pb:b1:linmaps:1`, `pb:b1:curves:1` | «عكس النقيض», «معدوم القوى», «متساوية الزمن» are each used again after the statement that introduces them; the English wording happens not to repeat them |

**Known divergence, recorded deliberately** — `thm:b1:logic:partition` (14
links in English) has **no Arabic counterpart**. In Arabic the same word
«تجزئة» carries three senses in this book: the *partition* of ch. 1, the
*subdivision* of an interval in ch. 15 (English uses a different word there),
and — with the instrumental `ب` — the idiom «المكاملة بالتجزئة», *integration
by parts*, 29 occurrences. `\index{تجزئة}` sits in a `theorem`, and for terms
introduced outside a `definition` environment `STOP` is hard rather than
chapter-local (`harvest.py`, second pass), so the choice is binary: either
partition links or integration-by-parts links, not both. Integration by parts
was kept (it is the higher-traffic notion and already carries 6 links). The
alternative — renaming *integration by parts* to «المكاملة بالأجزاء», which is
equally standard MSA — was rejected as a late, book-wide terminology change
made for the linker's benefit rather than the reader's; it is recorded here in
case a future pass wants it.

## Register and terminology

Technical vocabulary follows `arabic_style_card.md` §4 exactly (مجموعة، تطبيق،
متباينة، شاملة، تقابلية، متتالية، حَدّ، كثير حدود، جذر، درجة، مصفوفة، محدد،
مبرهنة not نظرية, متجهة not شعاع, ASCII digits, Arabic ، ؛ ؟ with the Latin
full stop). The lecture register uses the stock phrases the card prescribes:
**ليكن / لتكن**, **نفترض أن**, **برهن على أن**, **نستنتج أن**, **ومنه**,
**لدينا**, plus **بيّن أن**, **حُلَّ**, **احسب**, **تحقق من**, **إذا وفقط إذا**.

Consistency was audited across the volume, not assumed: a sweep for شعاع
(*ray*) versus متجهة (*vector*) found 13 sites in ch. 13/14/18/20/21/23/24/25
where the first pass had drifted, and all 13 were normalised to متجهة (شعاعية
= *radial* and شعاع ضوء = *light ray* are kept, since they are the physical
sense).

### Settled in chapters 1–9 (first pass)

| English | Arabic |
|---|---|
| statement (logic) | **عبارة** (keeps قضية free for the `proposition` environment) |
| modulus \|z\| / argument | **المقياس / العمدة** |
| affix | **اللاحقة** |
| pigeonhole principle | **مبدأ الأدراج** |
| arrangement / combination / permutation | **ترتيبة / توفيقة / تبديلة** |
| binomial coefficient | **المعامل الثنائي** |
| inclusion–exclusion / derangement | **الاحتواء والاستبعاد / الاضطراب** |
| signature (of a permutation) | **التوقيع** (keeps إشارة for *sign*) |
| carry (in an addition) | **الاحتفاظ** |
| valuation `v_p` / unit (of a ring) | **التقييم / عنصر قابل للقلب** |
| idempotent | **عنصر جامد** |
| partial fractions / pole / order | **العناصر البسيطة / قطب / رتبة** |
| variation of constants | **تغيير الثابت** |

Truth values are written **ص / ك** (صادق / كاذب) in truth tables, and the
ch. 2 anagram exercise uses **برتقال** (6 distinct letters → 720) and
**بانانا** (ا×3, ن×2, ب×1 → 60) so that both the mathematics and the answer
stay byte-identical to English while the words become Arabic.

### Settled in chapters 10–25 (this pass)

| English | Arabic | | English | Arabic |
|---|---|---|---|---|
| supremum / infimum | **الحد الأعلى / الحد الأدنى** | | vector space / subspace | **فضاء متجهي / فضاء جزئي** |
| upper bound | **حاصر أعلى** | | span | **الفضاء المولَّد** |
| bounded above | **محدودة من أعلى** | | direct sum / supplementary | **مجموع مباشر / متتامّان** |
| max / min (attained) | **أكبر عنصر / أصغر عنصر** | | free family / basis | **عائلة حرة / أساس** |
| completeness axiom | **بديهية التمام** | | exchange lemma | **مبرهنة التبادل المساعدة** |
| floor | **الجزء الصحيح** | | incomplete-basis theorem | **مبرهنة الأساس غير التام** |
| squeeze theorem | **مبرهنة الحصر** | | Grassmann's formula | **صيغة غراسمان** |
| monotone-limit theorem | **مبرهنة النهاية الرتيبة** | | hyperplane | **مستوٍ فائق** |
| adjacent sequences | **متتاليتان متجاورتان** | | endomorphism / isomorphism | **تشاكل ذاتي / تشاكل تقابلي** |
| subsequence / Cauchy sequence | **متتالية جزئية / متتالية كوشي** | | rank–nullity theorem | **مبرهنة الرتبة** |
| fixed point / contraction | **نقطة صامدة / تقلّصي** | | projection / projector | **إسقاط / مسقط** |
| neighbourhood | **جوار** | | linear form | **شكل خطي** |
| open / closed | **مفتوحة / مغلقة** | | nilpotent / Fitting's lemma | **معدوم القوى / مبرهنة فيتينغ المساعدة** |
| interior / closure / boundary | **الداخل / الغلق / الحافة** | | trace / transpose | **أثر / المنقولة** |
| compact / dense / perfect | **متراصة / كثيفة / تامّة** | | similar matrices | **مصفوفتان متشابهتان** |
| totally disconnected | **مفكّكة كليًا** | | row operations / Gaussian elimination | **عمليات على السطور / إزاحة غاوس** |
| IVT / EVT / Heine | **مبرهنة القيم الوسطى / القيم الحدّية / هاينه** | | determinant / cofactor expansion | **محدد / النشر بالعوامل المرافقة** |
| uniform continuity | **الاتصال المنتظم** | | Cramer's rule | **قاعدة كرامر** |
| derivative / MVT / chain rule | **مشتقة / مبرهنة التزايدات المنتهية / قاعدة السلسلة** | | inner product / Euclidean space | **جداء سلّمي / فضاء إقليدي** |
| convex | **محدَّبة** | | orthonormal / Gram–Schmidt | **متعامد ممنظم / غرام--شميت** |
| Landau notation / asymptotic expansion | **ترميز لانداو / نشر مقارب** | | isometry / glide reflection | **تقايس / انعكاس منزلق** |
| series / absolute convergence | **متسلسلة / التقارب بإطلاق** | | dihedral group | **زمرة ثنائية السطح** |
| ratio test / Euler's constant | **محك النسبة / ثابت أويلر** | | parametrized curve / cusp | **منحن معلَّمي / نقطة ارتداد** |
| step function / subdivision | **دالة درجية / تجزئة** | | astroid / cardioid / cycloid | **النجمية / القلبية / الدويرية** |
| integration by parts | **المكاملة بالتجزئة** | | tautochrone / conic / eccentricity | **متساوية الزمن / مقطع مخروطي / الانحراف المركزي** |
| Riemann sums | **مجاميع ريمان** | | partial derivative / gradient | **مشتق جزئي / تدرج** |
| tower law (Dedekind) | **قانون البرج** | | saddle point | **نقطة سرج** |
| Archimedean property | **خاصية أرخميدس** | | least squares / regression line | **المربعات الصغرى / مستقيم الانحدار** |

## Build

`latexmk one_math_book_3_university_year_1_ar.tex` (LuaHBTeX):

| | |
|---|---|
| exit status | 0 |
| fatal errors (`grep -ac '^!'`) | **0** |
| undefined references (`grep -aci undefined`) | **0** |
| `Overfull \hbox` | **0** |
| PDF | `build/one_math_book_3_university_year_1_ar.pdf`, **373 pp** |

The five overfull boxes reported at the end of the first pass were an artefact
of the mixed tree (nine Arabic chapters, sixteen English fallbacks); with the
book fully Arabic the count fell to one — 1.68 pt in Example 18.16 — which was
cleared by shortening the sentence («\emph{الأساس القانوني} للمقدار $K^n$:» →
«\emph{الأساس القانوني} في $K^n$:»), never by weakening the wording or
touching the mathematics. The current build is at zero.

## Sampled prose — verdicts

> يبدأ الجبر الخطي هنا: فبديهيات الفضاءات المتجهية تعزل ما يشترك فيه $\R^2$ و
> $\R^3$ وفضاءات كثيرات الحدود وفضاءات الدوال --- إذ يمكن الجمع والضرب في
> سلّم. … واللغة التي يهيّئانها --- الفضاء المولَّد، والعائلة الحرة، والأساس،
> والمجموع المباشر --- هي الخبز اليومي لكل فصل بعدهما. (ch. 18, opening)

**Native.** «تعزل ما يشترك فيه» for *isolates what … have in common* and «الخبز
اليومي» for *bread and butter* are Arabic idiom, not calque; the dual
«يهيّئانها … بعدهما» is handled correctly throughout.

> بُني حساب \cref{…} من أجل الدوال $y = f(x)$؛ وأكثر منحنيات الهندسة
> والميكانيك --- المسارات، والدوائر المتدحرجة على دوائر، والمدارات --- تأبى
> ذلك الشكل. (ch. 24, opening)

**Native.** «تأبى ذلك الشكل» (*refuse that shape*) is exactly the register an
Arabic lecturer uses; the appositive dash list keeps English's rhythm without
English's word order.

> استُعملت مبرهنة القيم الوسطى ومبرهنة القيم الحدّية في مستوى الثانوي على
> الثقة البصرية. ومع المتتاليات وطوبولوجيا $\R$ في اليد، يبرهن هذا الفصل
> عليهما --- ويكمّل النظرية بمبرهنة التقابل الرتيب. (ch. 13, opening)

**Native.** «على الثقة البصرية» and «في اليد» carry *on visual trust* / *in
hand* idiomatically; note the passive استُعملت, the correct register for a
retrospective opening.

> فمبرهنة كومر تضغط الجواب من أجل المعاملات الثنائية في احتفاظات عملية جمع
> واحدة --- فقابلية القسمة، وهي في الظاهر خاصية إجمالية لأعداد ضخمة، تُقرأ
> محليًا رقمًا رقمًا. (solutions ch. 6, q. 25)

**Near-native.** Correct and idiomatic; «تُقرأ محليًا رقمًا رقمًا» is good, but
«تضغط الجواب … في» leans slightly on the English *compresses … into*. A native
pass would prefer «تختصر الجواب … إلى». This is the weakest sampled passage in
the volume and it is still publishable.

No sampled passage scored below near-native. The volume was written sentence by
sentence against the English, never post-edited from machine output; the
register was set in ch. 1 and carried forward deliberately (the same stock
verbs, the same statement vocabulary, the same «والفكرة النافذة» for the book's
recurring *The insight:*), and chapters 10–25 were written against the openings
of 1–9 so the book has one voice.

## Score

| Dimension | Weight | Score | Note |
|---|---|---|---|
| Completeness | 15 | 15 | 50/50 files; gate PASSED |
| Structural fidelity (labels, envs, keys, order) | 15 | 15 | zero divergence, machine-checked |
| Mathematical fidelity | 15 | 15 | math multiset proven identical to English |
| Prose gates (9 classes) | 10 | 10 | 0 hits in 50 files |
| Register / idiom (native academic) | 20 | 19 | native in sampling; one near-native passage found and left |
| Terminology consistency | 10 | 10 | style card §4 honoured; شعاع/متجهة sweep done; index near-duplicate unified |
| Term-link layer | 10 | 8 | 101/106 English targets matched; 3 English targets unreachable in Arabic (one of them structurally — see «تجزئة»), 6 extra Arabic targets, each justified |
| Build quality | 5 | 5 | 0 errors, 0 undefined, 0 overfull |
| **Total** | **100** | **96** | |

Where the four points went: 1 for the near-native seam in the ch. 6 solutions
(and the acceptance that a handful of similar seams likely survive unsampled
across 373 pages), 2 for the three English link targets Arabic cannot reach,
1 for the six extra Arabic targets — defensible, but a divergence is a
divergence and a reader comparing editions would see it.

## Requests to the orchestrator

1. **Promote the two terminology tables above into `arabic_style_card.md` §4.**
   Books 4 and 5 (already translated) and any future Arabic volume must not
   diverge on المقياس / العمدة / التوقيع / التقييم / قطب / العناصر البسيطة, nor
   on the Book-3 analysis and linear-algebra vocabulary settled here (الحد
   الأعلى، حاصر أعلى، متراصة، الغلق، الحافة، مستوٍ فائق، إزاحة غاوس، جداء
   سلّمي، متعامد ممنظم، …). I did not touch the card, as instructed.
2. **`harvest.py`: `STOP` is hard, not chapter-local, for a term introduced
   outside a `definition` environment.** `CLAUDE.md` documents `STOP` as "still
   linked inside the chapter that defines it", and that is true for the
   `definition` path (`local[t][seq]`), but the second pass — notions
   introduced by `\emph{}\index{}` under a `theorem`/`proposition` label —
   simply `continue`s on `t in cfg.STOP`, with no `local` fallback. That is
   what costs Arabic the `thm:b1:logic:partition` target above. Giving that
   pass the same `local` fallback would be a small change in shared code; I did
   not make it, since `tools/termlink/**` is infrastructure and Book 5's golden
   test guards it.
3. **Optional, for the linker's Arabic display text.** Because `HEAD` glues the
   proclitics onto the term, a link's *display* can open with a conjunction —
   «\omterm{…}{والأساس}», «\omterm{…}{فالمجموعة}». It reads fine and is
   certainly better than a broken match, but if a future pass wants the link to
   start at the noun, that belongs in `lang_ar.py` (excluding a leading `و`/`ف`
   from the wrapped span), not in a book config.

Nothing else on any shared file is outstanding. `styles/`, `latexmkrc`,
`.github/`, `tools/check_translation.sh`, `tools/check_arabic_prose.py`,
`tools/termlink/`, `tools/term_config/lang_ar.py`, `arabic_style_card.md` and
`one_math_book_3_university_year_1_ar.tex` were **not touched**. The files this
pass owns and changed are `parts/bachelor-1/ar/`,
`parts/bachelor-1/solutions/ar/`, `tools/term_config/book3_ar.py` and this
score file.

## Status

**Complete: 50 of 50 files, all gates green, overall 96/100 (threshold 95).**
No git commit was created; the working tree is left for human review.
