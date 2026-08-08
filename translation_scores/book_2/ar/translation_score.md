# Translation score — Math Book 2 · Arabic (`ar`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 2 (High School, grades 10–12) |
| **Language** | Modern Standard Arabic (`ar`), school-textbook register |
| **Quality bar** | **native academic** (English is the source of truth; `arabic_style_card.md` is binding) |
| **Overall score** | **96 / 100** — **the book is complete** |
| **Ship threshold** | ≥ 95 — **met** |
| **Date** | 2026-08-08 |
| **Scope of the writing pass** | **All 35 chapters, 70 files.** The first pass delivered grade-10 (18 files) and grade-11 chapters 01–06 (12 files); the second pass wrote grade-11 chapters 07–10 (8 files) and all sixteen grade-12 chapters with their solutions (32 files), then re-ran every gate over the whole tree, regenerated the term-link layer for the complete book, and built the PDF for the first time. |
| **Latest pass** | **Cross-book consistency passes (2026-08-08): *continuous* and the *intermediate value theorem* aligned on Books 3–5.** Terminology only; no re-translation. See "Continuity terminology pass" and "IVT terminology pass" below. |

## Verdict in one line

The Arabic edition is **complete and green on every gate**: all three years pass
`check_translation.sh`, the Arabic prose gate is at **0 hits in all nine classes
across all 70 files**, the term linker produces **3 418 defined-term links with
*exact* `\omterm` target parity against English** (`diff` of the target sets
empty over the whole book), and `latexmk one_math_book_2_high_school_ar.tex`
builds with **0 errors, 0 undefined references and 0 overfull boxes**
(317 pages). Since 2026-08-08 the book also says **متصل/الاتصال** for
*continuous/continuity* and **مبرهنة القيم الوسطى** for the *intermediate value
theorem*, the same words Books 3–5 use.

## Scope and state

| Year | Chapters | Bodies | Solutions | `check_translation.sh` |
|------|---------:|-------:|----------:|------------------------|
| grade-10 | 9 / 9 | 9 | 9 | **PASSED** |
| grade-11 | 10 / 10 | 10 | 10 | **PASSED** |
| grade-12 | 16 / 16 | 16 | 16 | **PASSED** |
| **total** | **35 / 35** | **35** | **35** | **all PASSED** |

## Gate results

```text
bash tools/check_translation.sh grade-10 ar   -> TRANSLATION GATE: PASSED (18 files)
bash tools/check_translation.sh grade-11 ar   -> TRANSLATION GATE: PASSED (20 files)
bash tools/check_translation.sh grade-12 ar   -> TRANSLATION GATE: PASSED (32 files)
python3 tools/check_arabic_prose.py parts/grade-1{0,1,2}/ar parts/grade-1{0,1,2}/solutions/ar
                                              -> arabic prose gate: OK (70 files)
python3 tools/link_defined_terms.py --book 2 --lang ar --unwrap --apply
python3 tools/link_defined_terms.py --book 2 --lang ar --apply
                                              -> 3418 links across 70 files
                                                 (def 3198, prop 97, pb 52, thm 32, met 25, ex 14)
python3 tools/link_defined_terms.py --book 2 --lang ar --check
                                              -> CHECK: every file matches what the config generates
latexmk one_math_book_2_high_school_ar.tex    -> 0 errors, 0 undefined, 0 overfull
                                                 317 pages (English: 330)
```

The nine Arabic prose classes — `english`, `translit`, `punct`, `digits`,
`math-space`, `bidi-ctrl`, `presform`, `tatweel`, `split-number` — are **all at
0** on all 70 files.

Structural invariants re-verified across the whole tree: exercise/problem labels
match solution keys chapter by chapter (35/35), no duplicate labels, no
`\end{env>` typo, no drafty `...` outside `samples at=`, no `\'e`-style escapes.

## Method

The masking pipeline built in the first pass was reused unchanged and
re-validated by a full round trip (mask → unmask → verify on the English text
itself) before a single Arabic line was written:

1. `mask.py` replaces every non-translatable span with a numbered marker — whole
   `tikzpicture`s, display and inline math, `\label`/`\cref` targets,
   `\qty`/`\unit`, `\begin{solution}{key}`, `tabular` column specs — and pulls
   the *visible* strings out of `\text{…}` inside math and out of TikZ node text
   / axis labels into a separate per-file string list. `\omterm` wrappers are
   unwrapped (the linker regenerates them).
2. Translation is written against the masked file, marker for marker.
3. `unmask.py` **refuses to write** unless every marker reappears exactly once,
   every string slot is supplied, and the multiset of unmasked inline math is
   unchanged; a pre-lint rejects tatweel, bidi controls, presentation forms and
   Arabic-Indic digits before reassembly; `verify.py` then re-checks the label
   sequence, the environment census, the solution keys, the `\cref` targets and
   the `\emph`/`\index`/`\item`/`\textbf` counts against the English twin.

The refusal caught real errors on almost every file: dropped `\emph{not}`,
numbers spelled out in Arabic words that silently deleted a `$6$`/`$3$`/`$k$`
math span (about 25 such losses this pass, every one restored), an `$=$`
invented where English had a bare `=`, and — repeatedly — the **tatweel** in
`بـ`/`فـ`/`لـ` before a math span. Every occurrence was rewritten by naming the
object (`بمقدار $5$`, `للدالة $f$`, `فإن …`, `حسب \cref{…}`) as
`arabic_style_card.md` §3 now prescribes.

## Dimension scores

| Dimension | Score | Note |
|---|---:|---|
| Structure (labels, env census, exercise↔solution keys) | 100 | machine-verified twice per file, then re-verified book-wide |
| Terminology | 97 | style-card glossary followed; the settled table (فترة، مستقيمي، الجداء السلّمي، نظام إحداثيات، معيار) is honoured, and the new grade-12 vocabulary is recorded below. Since 2026-08-08 *continuous* is **متصل** and the IVT is **مبرهنة القيم الوسطى**, matching §4 and Books 3–5 — see "Continuity terminology pass" and "IVT terminology pass". No cross-book divergence is known to remain |
| **Register** | 95 | school-textbook MSA; `ليكن/لتكن`, `نفترض أن`, `ومنه`, `إذن`; a few weekend-problem preambles still carry the English apposition rhythm |
| LaTeX hygiene | 100 | math byte-identical except for one documented deviation (below); no accents, no stray `...` |
| Cross-references | 100 | `\cref` targets identical file by file; `حسب \cref{…}`, never `ال\cref{…}` |
| Figures | 99 | drawing code untouched; every node string, axis label and `\text{}` inside math localized |
| Solutions | 97 | complete and terse; numbers unchanged |
| **Term links** | 100 | 3 418 links, **exact target-set parity with English** (123 = 123, `diff` empty), `--check` clean; every high-frequency term sampled in context for wrong-sense |
| **Build** | 100 | 0 errors, 0 undefined, 0 overfull |
| **MT-artifact freedom** | 97 | no MT was used at any point — the prose was composed directly, so calques are absent by construction |
| **Overall** | **96** | complete book |

## Sampled passages

**1. `grade-12/ar/01-sequences.tex`, chapter opening — native.**
> المتتالية قائمة من الأعداد الحقيقية مدلَّلة بالأعداد الطبيعية. وتنمذج
> المتتاليات التطورات المتقطعة --- تعدادات السكان محسوبة سنة بعد سنة،
> وأرصدة حساب مصرفي، والتقريبات المتعاقبة لعدد ما --- ونهاياتها هي أول
> لقاء جدي مع اللانهاية.

Verb-initial, `مدلَّلة بـ` for *indexed by*, `أول لقاء جدي مع اللانهاية`
instead of a calqued relative — an Arabic textbook sentence.

**2. `grade-12/ar/02-limits-continuity.tex`, the IVT — native.**
> لا بد لمنحنى متصل يصل $(a, f(a))$ بالنقطة $(b, f(b))$ من أن يقطع كل
> مستقيم أفقي $y = k$ يقع بين $f(a)$ و $f(b)$.

`لا بد … من أن` is the register's own way of saying *must*; the math sits
outside the Arabic run, never mixed into it.

**3. `grade-12/ar/09-complex-numbers.tex`, definition — native.**
> والعددان الحقيقيان $a$ و $b$ هما \emph{الجزء الحقيقي} $\Rea(z)$
> و\emph{الجزء التخيلي} $\Ima(z)$ للعدد $z = a + \iu b$؛ وهذه العبارة هي
> \emph{الصورة الجبرية} للعدد $z$، وهي وحيدة.

Definite-state apposition, `وهي وحيدة` for *and it is unique* — no copula
calque.

**4. `grade-12/solutions/ar/10-arithmetic.tex`, answer 17 — near-native.**
> ضرب عددين أوليين طول كل منهما $300$ رقمًا يستغرق ميكروثانية؛ أما
> استعادتهما من جداءهما فتهزم كل خوارزمية معروفة وكل حواسيب العالم ---
> فالقفل طريق باتجاه واحد.

Correct `أما … فـ` contrast; slightly denser than a school answer key would be.

**5. `grade-12/ar/16-continuous-distributions.tex`, problem preamble —
near-native.**
> لماذا تبدو حافلتك دائمًا أطول انتظارًا مما يعد به جدول المواعيد؟

Accurate and grammatical, but the English rhetorical rhythm survives; an Arabic
writer would more likely split the three rhetorical questions differently.

## Terminology decisions taken for this book

Beyond `arabic_style_card.md` §4, and consistent across all 70 files.

Carried over from the first pass: interval = **فترة**, coordinate system =
**نظام إحداثيات**, collinear = **مستقيمي**, scalar product = **الجداء السلّمي**,
frequency = **تواتر** / count = **تكرار**, irrational = **أصمّ**,
preimage = **سابقة**, discriminant = **المميز**, "the Middle School volume" =
**الكتاب السابق**, "Weekend problem" = **مسألة نهاية الأسبوع**.

New in this pass:

| English | Arabic | Reason |
|---|---|---|
| norm | **معيار**; criterion → **محك** | the style card reserves `معيار` for *norm*; the six earlier uses of `معيار` for *criterion* (grade-10/11) were renamed to `محك`, and `محك` replaced `معيار` in `book2_ar.py`'s `NOT_A_TERM` |
| induction (recurrence) | **التراجع** | already used in grade-11; `الاستقراء` avoided so that `\emph{بالتراجع}` reads the same in Book 2 and Book 3 |
| squeeze theorem / bijection theorem | **مبرهنة الحصر** / **مبرهنة التقابل** | standard school forms |
| chain rule | **قاعدة السلسلة** | composes with `قاعدة الجداء`, `قاعدة خارج القسمة` |
| convex / concave / inflection point | **محدب** / **مقعر** / **نقطة انعطاف** | |
| primitive (antiderivative) | **دالة أصلية** | style card |
| binomial coefficient / distribution / theorem | **معامل ثنائي** / **توزيع ثنائي** / **مبرهنة ثنائي الحد** | one family, so grade-11 ch. 10 and grade-12 ch. 8/14 agree |
| modulus / argument (complex) | **المقياس** / **العمدة** | style-card settled table |
| affix | **لاحقة** | |
| congruence / "modulo $n$" | **موافقة** / **بترديد $n$** | |
| gcd / coprime / Bézout | **القاسم المشترك الأكبر** / **أوليان فيما بينهما** / **مساواة بيزو** | |
| graph (network) / edge / walk | **بيان** / **حافة** / **مسلك** | keeps `منحنى` free for the graph *of a function* |
| diagonalization / eigenvector | **القطرنة** / **متجهة ذاتية** | style card for the second |
| skew lines / coplanar | **متخالفان** / **متوافقة في مستوٍ** | |
| conditional probability / Bayes | **الاحتمال الشرطي** / **صيغة بايز** | |
| density / uniform / exponential / normal | **كثافة** / **منتظم** / **أسي** / **طبيعي** | |
| memorylessness / inspection paradox | **انعدام الذاكرة** / **مفارقة المعاينة** | |
| z-score | **الدرجة المعيارية** | |

Two English letter-puzzles were replaced by Arabic words of the **same
combinatorial shape**, because a 6-letter Latin word is unreadable in an Arabic
page and trips the `english` gate:

* MATH (4 distinct letters, $4! = 24$ anagrams) → **حساب** (4 distinct letters);
* BANANA (6 letters, A×3, N×2, B×1) → **اللاما** (6 letters, ا×3, ل×2, م×1).

All the displayed mathematics ($\binom63$, $\binom32$, $\frac{6!}{3!2!}$) is
untouched, and the hint ("first place the three A's") became "ضع حروف الألف
الثلاثة أولًا".

Provenance neutralization, per `book_style.md`: `\emph{grade 12}` /
`\emph{grade 10}` / `\emph{grade 9}` self-references became `في السنة المقبلة`,
`من قبل` or `في الكتاب السابق`; "a map of France … on French soil" became
`خريطة لبلدٍ ما … من أرض ذلك البلد`. Historical proper nouns are kept
(أرخميدس، إقليدس، غاوس، لاسكو، أوتزي، سالي كلارك، أكاديمية العلوم الفرنسية سنة
1791، مونتي هول، غوغل) — they are history, not curriculum provenance.

## Term-link curation

`tools/term_config/book2_ar.py` was curated this pass (it had been the seed
file). Harvest, as of 2026-08-08: 237 terms, 44 dropped as defined twice,
2 dropped by the stoplist, 225 linkable, 46 chapter-local, **3 418 links**
inserted, `--check`
clean. Additions, each closing one target-parity divergence against English or
one wrong-sense family found by sampling the links in context:

* `NOT_A_TERM += "مساواة"` — Arabic result-name head (`مساواة بيزو`), the twin
  of English's `identity`; without it `thm:g12:arith:bezout` was linked in
  Arabic and not in English. `"معيار"` was replaced by `"محك"` in the same list
  (see the terminology note above).
* `STOP = {"مجموع", "صورة", "صور"}` (with the definite forms added by
  `STOP |= {"ال" + w for w in STOP}`, as the style card requires).
  `مجموع` closes the documented **`def:g10:vectors:sum` spurious** divergence:
  it is ordinary Arabic outside its own chapter, exactly as English never links
  *sum*. `صورة` is the larger catch: it is the mathematical *image* of a
  function **and** the ordinary word for **form** (`على الصورة الجبرية /
  الأسية / المختزلة / النموذجية`), for the **heads** of a coin, for a **face**
  card, and — with the ب proclitic — for the adverbial `بصورة ساحقة`. Sampling
  all 86 occurrences in context showed that essentially none meant the image,
  so the word is stopped outside grade-10 ch. 3 where it is defined. This is
  the style card's "trade link volume for precision" in action: 91 links
  removed, all of them wrong.
* `EXTRA["متوسط"] = "def:g10:stats:mean"` — closes the documented
  **`def:g10:stats:mean` missing** divergence: the Arabic definition emphasises
  `المتوسط الحسابي` while later chapters write `المتوسط`.
* `EXTRA["تبديلات"] = "def:g12:comb:permutation"` and
  `EXTRA["عاملية"] = "prop:g12:comb:tuples"` — broken plurals / derived forms
  that `WORD_TAIL = ''` and `DERIVE = False` cannot reach.
* `EXTRA["المحدد"] = "def:g11:vect:det"` — sense fix: the grade-12 matrix
  proposition re-emphasises the determinant, and `AMBIG_POLICY =
  nearest-preceding` was sending one occurrence there instead of to the
  grade-11 definition English uses.
* `DROP = {"انعدام الذاكرة"}` — an asymmetry of the index-only harvest: it
  requires a space in the term, so English's `\index{memorylessness}` (one word)
  is skipped while Arabic's two-word key is not.
* `EXTRA["متصلة"] = "def:g12:limcont:continuity"` — added by the 2026-08-08
  continuity pass, mirroring `book3_ar.py`; see that section for the reasoning
  and the resulting counts.

**Result: `diff` of the `\omterm` target sets, English vs Arabic, over all 70
files, is empty.** Both parity divergences documented by the previous pass are
closed.

## Continuity terminology pass (2026-08-08)

A sweep across the finished Arabic books found Book 2 alone on the **مستمر**
family for *continuous*, while Books 3 and 5 use **متصل** — the form
`arabic_style_card.md` §4 prescribes. That divergence matters more here than
anywhere else: grade-12 ch. 2 is where a pupil meets continuity for the first
time, and Book 3 ch. 13 re-uses the concept at university. A pupil must not
have to relearn the word. Book 2 is now converted; the school→university seam
is a single vocabulary.

Book 3's `parts/bachelor-1/ar/13-limits-continuity.tex` and `15-integration.tex`
were read first and their constructions copied verbatim, so the two volumes now
phrase the concept identically:

| | Book 3 (`bachelor-1`) | Book 2 (grade-12), after |
|---|---|---|
| chapter title | `النهايات والاتصال` | `النهايات والاتصال` |
| section | `\section{الاتصال}` | `\section{الاتصال}` |
| index key | `\index{اتصال}` | `\index{اتصال}` (+ `\index{دالة متصلة}`, EN has two keys) |
| at a point | `متصلة عند $x_0$` | `متصلة عند $a$` |
| on an interval | `متصلة على $I$` | `متصلة على $I$` |
| "by continuity" | `وبالاتصال` / `بالاتصال` | `وبالاتصال` / `بالاتصال` |
| integral of a continuous fn | `\section{تكامل دالة متصلة}` | `\section{تكامل دالة متصلة}` |
| dual | `متصلتين` / `متصلتان` | `متصلتين` / `متصلتان` |
| accusative | `متصلًا` | `متصلًا` |
| "depends continuously on" | (Book 5) `يتعلق اتصاليًّا بـ` | `يتعلق اتصاليًّا بـ` |

### Before / after

Measured over `parts/grade-10..12/{ar,solutions/ar}` (grade-10 and grade-11
contain no continuity at all — every occurrence in the book is grade-12):

| token family | before | after |
|---|---:|---:|
| `مستمر*` (adjective) | 68 | **0** |
| `الاستمرار*` / `استمرار*` (noun) | 23 | **0** |
| `متصل*` (adjective) | 1 | **69** |
| `الاتصال` / `اتصال` (noun) | 2 | **41** |

The one pre-existing `متصل` was `تأخذ متصلًا من القيم` (ch. 16, EN "take a
*continuum* of values") — already the right family, left as it was. The two
pre-existing `اتصال` tokens are `الاتصالات` in the graph-theory solutions
(*connections* in a network), untouched and correctly still unlinked.

Every one of the 91 converted sites was checked against the English twin line
by line: **all 91 render `continuous`, `continuity` or `continuously`** — there
was no ordinary "ongoing/continual" sense anywhere in the book, so nothing was
kept on lexical grounds. Agreement was verified site by site rather than
assumed; `مستمر` (form X participle) and `متصل` (form VIII participle) inflect
identically (`-ة`, `-تين`, `-تان`, `-ًا`, `ال-`), so every feminine, dual and
accusative form carried over unchanged, and the noun forms — masculine in both
families — needed no surrounding rework beyond the ordinary construct state
(`تصحيح الاستمرار` → `تصحيح الاتصال`, `اتصال الدوال المألوفة`).

### Deliberately kept as-is

* **`يستمر`** — `grade-12/solutions/ar/02-limits-continuity.tex:103`,
  the bisection method: *"keep the half of the interval in which the sign change
  **continues**"*. This is the ordinary verb, not the analytic notion; English
  does not link it either. **Left alone.**
* **`المتغيرات العشوائية المتصلة`** (ch. 16 title) — converted, not kept, but
  worth recording: Book 2 already said `متقطعة` for *discrete*, and Book 3 says
  `المتوسط المتقطّع … والمتوسط المتصل`. The pass therefore restores the standard
  Arabic **متصل / متقطع** pair; keeping `مستمر` would have broken it.
* **`مبرهنة القيم المتوسطة`** (IVT) — Book 3 names the same theorem
  `مبرهنة القيم الوسطى`. This is a *second*, independent cross-book divergence,
  outside this pass's remit (it is a result-name, not the continuity family) and
  outside the measured counts. **Flagged to the orchestrator below, not touched.**

### One restructured site

`grade-12/ar/02-limits-continuity.tex:464` (wobbly-table problem) rendered
English's adverb *"depends **continuously** on the table's rotation angle"*.
The old Arabic `يتعلق باستمرار بـ` was the one place a literal swap would have
gone wrong twice over: `باستمرار` is the everyday adverb *constantly*, and
`باتصال بـ` stacks two ب's. It now reads `يتعلق اتصاليًّا بزاوية دوران الطاولة`,
copied from Book 5's identical construction
(`bachelor-3/ar/15-spectral-theory.tex:213`, *"depends continuously on the
function $f$"*). Like Book 5, `اتصاليًّا` is left unlinked — it is not a declared
form — which costs one `\omterm` occurrence and no target.

### Link layer

`--unwrap --apply` → `--apply` → `--check`, all clean. One entry was added to
`tools/term_config/book2_ar.py`, mirroring `book3_ar.py`'s entry for the same
term and the same reason:

```python
"متصلة": "def:g12:limcont:continuity",
```

The definition emphasises the *compound* (`\emph{متصلة عند $a$}`), so the bare
adjective — the form the rest of grade 12 actually uses — was never harvested.
Book 3 declares exactly this. Effect: links to `def:g12:limcont:continuity` rise
from **19 → 60** against English's 74, and total links from 3 377 → **3 418**.
The residual 14 are masculine and dual forms (`متصل`, `متصلتين`, `متصلتان`,
`متصلًا`, `المتصل`) plus the three-proclitic `وبالاتصال` / `وباتصال`, which
`lang_ar.py`'s `HEAD` matches at most one particle before `ال` — all of them
unlinked in Book 3 too, so the two volumes behave the same way. All 60 displays
were read in context; none is a wrong-sense match, and grade-10/11 contribute
none.

**`\omterm` target-set parity with English is unchanged: 123 distinct targets on
both sides, sets identical.**

## IVT terminology pass (2026-08-08)

The continuity pass flagged a second cross-book divergence in the same chapter;
the orchestrator settled it and it is now applied. **Intermediate value theorem
= مبرهنة القيم الوسطى** (`arabic_style_card.md` §4; Book 3 uses it 27 times).
The split is by *sense*, not by phrase:

* **القيم الوسطى** = *intermediate* values → the IVT.
* **القيم المتوسطة** / **القيمة المتوسطة** = *mean* values → only where English
  really says *mean* or *average*.

Book 3 already draws exactly this line: 27 × `القيم الوسطى` for the theorem,
1 × `القيم المتوسطة` for the mean-value example (`ex:b1:integration:average`).

### What changed

| site class | before | after | count |
|---|---|---|---:|
| IVT, all forms | `مبرهنة القيم المتوسطة` | `مبرهنة القيم الوسطى` | **25** |
| "every intermediate value visited" | `كل قيمة متوسطة` | `كل قيمة وسطى` | **1** |
| "the average-cost curve" | `منحنى الكلفة الوسطى` | `منحنى التكلفة المتوسطة` | **1** |

All 27 edits are in **grade-12 ch. 2** — 14 in `ar/02-limits-continuity.tex`,
12 in `solutions/ar/02-limits-continuity.tex`, plus the one average-cost site.
Nothing else in the book carries the phrase.

Each of the 25 was read against its English twin: they render *intermediate
value theorem* (9×), *the IVT* (14×), *IVT's* (2×). **None was a mean value.**
Two of the 25 span a line break inside the phrase (`ar/02` l. 378–379, the
weekend-problem title; `solutions/ar/02` l. 155–156), which a naive grep misses
— the substitution was whitespace-tolerant and preserves the break, so no line
was rewrapped.

`مبرهنة` is in `NOT_A_TERM`, so the theorem's name is not itself a linkable
term: the rename touches no `\omterm` and no `\label`. `thm:g12:limcont:ivt`
is unchanged, and so are the two `\omterm{thm:g12:limcont:ivt}{بالتنصيف}`
(*dichotomy*) links that point at it. The visible term and its index key moved
together: `\section{مبرهنة القيم الوسطى}`,
`\begin{theorem}[مبرهنة القيم الوسطى]`, `\index{مبرهنة القيم الوسطى}` — the
same index key Book 3 writes at `bachelor-1/ar/13-limits-continuity.tex:183`.

### Kept as mean/average — checked, not assumed

* `\begin{definition}[القيمة المتوسطة]\label{def:g12:integ:mean}` and
  `\emph{القيمة المتوسطة}\index{قيمة متوسطة}` (ch. 6) ← EN `[Mean value]`,
  `\emph{mean value}\index{mean value}`. The two `\omterm{def:g12:integ:mean}`
  displays likewise. **The `\index{قيمة متوسطة}` key is deliberately left
  alone** — it is now the only `متوسطة` index key in the book, and it means
  *mean value*, so it no longer competes with the IVT's key.
* `السرعة المتوسطة` ×5 (ch. 6 body and solutions) ← *average speed*.
* `grade-11/ar/03-differentiation.tex:240`, `مبرهنة القيمة المتوسطة` ← EN
  *"a rigorous proof needs the **mean** value theorem"*. This is Lagrange's
  MVT, a genuinely different theorem; **left as it was.** It is also outside
  grade-12, and the pass touched no file outside grade-12.
* All 60-odd `متوسط` / `المتوسط` statistics sites (`def:g10:stats:mean`,
  `def:g11:stat:mean`) — the arithmetic mean, untouched.

### One pre-existing error the new rule exposed

`grade-12/ar/02-limits-continuity.tex:485` said `منحنى الكلفة الوسطى` for
English's *"the average-cost curve"* — `الوسطى` used for *average*, the exact
reverse of the settled rule, and sitting in the IVT chapter itself. Worse, the
sentence `\cref`s `pb:g10:reffunc:1`, where the grade-10 Arabic already says
`التكلفة \emph{المتوسطة}`. Corrected to `منحنى التكلفة المتوسطة`, which now
matches both the rule and the problem it points at.

### Not touched: `وسطى` in its ordinary "middle" sense

Six sites use `وسطى`/`أوسط` for *middle*, and English says *middle* at each:
`القيمة الوسطى` in the median definition (`grade-10/ar/08-statistics.tex:86`,
`grade-11/ar/08-descriptive-statistics.tex:31` — EN "the middle value"),
`الخانة الوسطى` (*middle cell*), `الحد الأوسط` / `الحدود الوسطى` (*middle
term*), `النصف الأوسط` (*middle half*, the IQR). These are correct Arabic for
*middle* and are not the IVT phrase; they live in statistics and algebra
chapters far from ch. 2. Recorded here only so a future sweep does not read
them as strays.

## Why not 100

1. **Register in the weekend-problem prose.** The English weekend problems are
   deliberately literary (long dashes, apposition, one-line jokes). Roughly one
   paragraph in six in the `\begin{problem}` preambles would read better split
   into two Arabic sentences. The course text, the exercises and the solutions
   do not have this problem.
2. **Tashkīl is used sparingly and not systematically** — `مُدرَج`, `المعرَّفة`,
   `حَدّ`, `مُنزَل` are vocalized where ambiguity would otherwise bite, but the
   policy is ad hoc rather than a rule.
3. **One deliberate math deviation.** `grade-12/12-space-geometry.tex` writes
   `$0 = $ nonzero` in English; the trailing space inside `$…$` is a hard
   `math-space` failure, so the Arabic says
   `ومساواة مستحيلة $0 = c$ مع $c \neq 0$`. Same class as the grade-10 case
   below; both are noted in the requests section.
4. **Broken-plural link coverage.** `lang_ar.py` keeps `DERIVE = False`, so the
   Arabic link count (3 418) is high only because the proclitic `HEAD` fires
   often; individual broken plurals still have to be declared term by term, and
   only the four the parity diff exposed are declared so far.
5. **Wrong-sense sweep is sampled, not exhaustive.** The twenty-five
   highest-frequency Arabic link displays were read in context (which is how
   `صورة` was caught); the long tail was not. A second pass on the terms with
   5–20 occurrences would likely find one or two more `صورة`-class collisions.

## Requests to the orchestrator

1. **`check_arabic_prose.py` `math-space`** flags `$3x + 2y = $` and `$0 = $` —
   both occur verbatim in the **English** source
   (`grade-10/07-lines-and-systems.tex` weekend problem Q18, and
   `grade-12/12-space-geometry.tex` method box). Per instruction the English
   canon was left alone and the Arabic deviates locally. Either the gate should
   ignore a trailing `= ` before the closing `$`, or the English source should
   be fixed and every edition re-synced.
2. **`check_arabic_prose.py` `english`, uppercase words longer than 4 letters.**
   The gate allows `word.isupper() and len(word) <= 4` (acronyms). Real English
   words used as *letter puzzles* (BANANA in the anagram exercise) are therefore
   rejected, which forced the Arabic-word substitution described above. That is
   the right outcome for prose; if a future book needs a genuine Latin token
   longer than four letters (a gene name, a chemical formula), the gate will
   need an allow-list hook.
3. **`arabic_style_card.md` §4 could record the norm/criterion split**
   (`norm = معيار`, `criterion = محك`) as an explicit *pair*: the card states
   the reason in a parenthesis, but the first two `ar` agents on this book both
   used `معيار` for *criterion* before the collision was noticed. Book 3–5 will
   hit the same fork.
4. ~~**A second cross-book divergence is still open: the IVT's name**~~ —
   **RESOLVED 2026-08-08.** Raised by the continuity pass, settled by the
   orchestrator as `مبرهنة القيم الوسطى` (now in `arabic_style_card.md` §4)
   and applied to Book 2 the same day; the mean-value sense keeps
   `القيمة المتوسطة`. See "IVT terminology pass" above.
5. **Consider recording in the style card** the cross-book decisions taken here
   that Physics 2 and the university volumes will need: `induction = التراجع`,
   `graph (network) = بيان` with `حافة`/`مسلك`, `density = كثافة`,
   `normal distribution = التوزيع الطبيعي`, `eigenvector = متجهة ذاتية`
   (already there), `modulus/argument = المقياس/العمدة` (already there).
