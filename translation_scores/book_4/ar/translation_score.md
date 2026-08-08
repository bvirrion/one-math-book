# Translation score — Math Book 4 · Arabic (`ar`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 4 (University Year 2, `bachelor-2`) |
| **Language** | Arabic (`ar`), Modern Standard Arabic, university lecture register |
| **Quality bar** | **native academic** (English is the source of truth; the French twin was consulted for sense and structure only, never as a source) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **met; no blockers remain** |
| **Date** | 2026-08-08 (pass 1: full translation · pass 2: cross-book terminology sweep, same day) |
| **Scope of pass 1** | **Full first translation from the English canon.** All 23 chapters and all 23 solution files written against a structure-preserving placeholder pipeline. `tools/term_config/book4_ar.py` grown from the orchestrator's 45-line seed into a curated config with a documented Arabic rationale. The `ar` infrastructure (LuaLaTeX + babel `bidi=basic, layout=graphics`, bundled variable font, LTR picture hooks, RTL `tcolorbox` content, Arabic `\crefname` definite forms, `lang_ar.py` proclitic morphology) was delivered ready and was **not** touched. |
| **Scope of pass 2** | **Cross-book terminology consistency sweep** ordered by the orchestrator after a series-wide diff against Books 3 and 5: four word families in which this book had forked from `arabic_style_card.md`. No re-translation, no structural change; the math multiset, the `\label` set and the environment census are provably unchanged. See "Pass 2" below. |

## Pass 2 — cross-book terminology sweep (2026-08-08)

An orchestrator diff across the three finished university books found that
Book 4 had forked from `arabic_style_card.md` on four word families. The book
was consistent *with itself* in each of them, which is why nothing in pass 1
caught it — only a cross-volume comparison could. This pass normalised all
four to the settled series forms, by hand, site by site, with the English
canon open beside each ambiguous occurrence.

The link layer was regenerated from scratch (`--unwrap --apply`, then
`--apply`, then `--check`), because the surface form of several defined-term
displays changed.

### Counts, measured over the whole `ar` tree (chapters + solutions)

| family | Book 3 | Book 4 **before** | Book 4 **after** | Book 5 |
|---|---:|---:|---:|---:|
| متصل\* (continuous, adj.) | 198 | **8** | **355** | 490 |
| مستمر\* (continuous, adj.) | 0 | **347** | **0** | 0 |
| اتصال (continuity, noun) | 78 | **0** | **162** | 228 |
| استمرار\* (continuity, noun) | 10 | **166** | **4** | 2 |
| متجه\* (vector) | 191 | 166 | **261** | 166 |
| شعاع / أشعة | 5 | **120** | **24** | 23 |
| فترة\* (interval) | 170 | **2** | **103** | 223 |
| مجال\* (interval / domain / range) | 43 | **110** | **8** | 52 |
| القيم الوسطى (intermediate values) | 35 | **0** | **15** | 14 |
| القيم المتوسطة (mean values) | 1 | **4** | **1** | 6 |

(Book 5's row moved during this pass — a parallel agent was normalising the
same families there. Book 4's own tree is the column that matters here.)

Additional counts for the intermediate/mean split, Book 4 only:

| form | before | after | sense |
|---|---:|---:|---|
| القيم الوسيطة | 9 | **0** | intermediate values → merged into القيم الوسطى |
| القيمة الوسيطة | 1 | **0** | intermediate value → القيمة الوسطى |
| القيمة المتوسطة | 11 | **11** | *mean value* theorem / inequality — correct, untouched |

### 1. continuity: مستمر\* → متصل\*, الاستمرار\* → الاتصال

Mechanical in form but checked for sense: 347 adjective sites and 162 noun
sites across 41 of the 46 files. The constructions were copied from Books 3
and 5 before starting, and Book 4's pre-existing 8 متصل sites already used the
same ones, so nothing had to be invented:

- uniformly continuous → **متصلة بانتظام**; uniform continuity → **الاتصال المنتظم**
- continuous at a point → **متصلة عند**; continuity of $f$ → **اتصال $f$**
- discontinuity → **عدم الاتصال** (the `\index{دالة رتيبة!نقاط عدم الاتصال}`
  key moved with its visible term)
- modulus of continuity → **مقياس الاتصال**
- monotone continuity (of a probability measure) → **الاتصال الرتيب**
- extends by continuity → **يمتد بالاتصال**

Piecewise continuity was left as Book 4 already wrote it — **متصلة على قطع**.
Books 3 and 5 do not agree with each other here (they use both
«متصلة قطعةً قطعة» and «متصلة بالقطع»), so there is no settled form to copy,
and the phrase is outside the word family the sweep was about.

**Deliberately kept — 4 sites where the word is ordinary Arabic, not the
technical noun.** Each was verified against the English:

| site | Arabic | English |
|---|---|---|
| `ar/01-sets-structures.tex:95` | نستعمله **باستمرار** فيما يلي | "we use this **constantly** below" |
| `ar/09-integration.tex:199` | فيُستعمل **باستمرار** من الآن فصاعداً | "is used **constantly** from now on" |
| `ar/21-countable-probability.tex:185` | ويعمل أهل الاحتمالات **باستمرار** | "Probabilists **constantly** …" |
| `solutions/ar/23-generating-functions.tex:74` | تُستعمل **باستمرار** في نظرية الطوابير | "**constantly** used in queueing theory" |

Also untouched: «قوة **المتصل**» (`ar/01-sets-structures.tex:248`) — the
*cardinality of the continuum*, a noun, not the adjective; and
«أمراض الذيول الثقيلة **متصلة**» (`ar/23-generating-functions.tex:575`), where
the English is "the heavy-tail pathologies **connect**".

### 2. vector: شعاع → متجهة, with agreement

**Not a search-and-replace.** شعاع is masculine, متجهة is feminine, so 96
sites were read individually and every agreeing adjective, demonstrative,
relative pronoun and verb moved with the noun:

- شعاع واحدي → **متجهة واحدية**; شعاعا ثابتا موازيا → **متجهة ثابتة موازية**
- الشعاعان … مستقلان → **المتجهتان … مستقلتان**; شعاعين ذاتيين → **متجهتين ذاتيتين**
- يبلغ الشعاع → **تُبلَغ المتجهة**; يحملها الشعاع → **تحملها المتجهة**
- الشعاع … ناظميا → **المتجهة … ناظمية**; وهو شعاع واحدي → **وهي متجهة واحدية**
- فضاء شعاعي → **فضاء متجهي**; الفضاءات الشعاعية → **الفضاءات المتجهية**
- التطبيق الشعاعي (*the vector map* of an affine map) → **التطبيق المتجهي**
- حقل شعاعي → **حقل متجهي** (matching Book 5's «حقل متجهي»)
- ذات قيم شعاعية → **ذات قيم متجهية**
- `\section{النقط والأشعة}` → `\section{النقط والمتجهات}`
- `\begin{example}[شعاع داربو]` → `[متجهة داربو]`

Two chapter-17 derivations of شعاع that mean *vectorialization* were also
retired, so the chapter no longer mixes roots: «تشعيع تطبيق أفيني عند نقطته
الثابتة» → «**إعادة تمركز** تطبيق أفيني…» and «وبالتشعيع عندها» →
«**وبإعادة التمركز** عندها» — the same operation, and the phrase the chapter
already used at `ar/17-affine-spaces.tex:332`. «نشعّع عند مبدأ $O$ ونكتب
النقط أشعة» became «نتخذ $O$ مبدأ ونكتب النقط **متجهات**» ("Vectorialize at an
origin $O$ and write points as vectors").

**Deliberately kept — 24 sites where شعاع is not a vector.** Every one was
checked against the English:

| sense | sites | why |
|---|---|---|
| **light ray** (`ray`, `rays`) | 18 sites in `ar/18-curves.tex` (830, 929–967) and `solutions/ar/18-curves.tex` (381, 416, 420, 438, 441, 443, 444, 445) — the envelope/caustic problem | English says *ray*; شعاع is the correct Arabic and has nothing to do with the vector decision |
| **cross product** «الجداء الشعاعي» | `ar/19-surfaces.tex:5`, `ar/19-surfaces.tex:313`, `ar/12-quadratic-forms.tex:81`, `solutions/ar/18-curves.tex:224`, `solutions/ar/19-surfaces.tex:153` | Book 5 uses «الجداء الشعاعي» for *cross product* in `20-submanifolds` and `05-representations`; changing it here would have created a **new** cross-book divergence. The *operands* did move: «لشعاعين متعامدين» → «لمتجهتين متعامدتين» |
| **radioactive** «التفككات الإشعاعية» | `ar/23-generating-functions.tex:382` | *radioactive decays*; a different root sense entirely |

One further correction fell out of the review: `solutions/ar/19-surfaces.tex:443`
read «موازٍ **للشعاع** $Oz$» where the English says "axis parallel to $Oz$";
it is now «موازٍ **للمحور** $Oz$».

**No radius senses were found in this book.** *Radius of convergence* is
«نصف القطر» throughout ch. 11 and ch. 23, not «شعاع التقارب», so the
radius-of-convergence trap the brief warned about did not arise here; there is
no spectral radius in Book 4 either.

### 3. interval: مجال → فترة, with agreement

مجال is masculine, فترة is feminine, so the same per-site treatment applied to
the 102 interval occurrences: فترة كيفية، الفترة التامة، الفترة نصف المفتوحة …
مغطّاة، فترةً كاملةً … متقاطعةً، الفترة الأعظمية، فترة مشتركة، فترتين
متتاليتين، الفترة كلها، فترة تحتوي، فترة طولها، ففترة طولها … تلتقي،
تتلقّى كل فترة جزئية، وتُحصر الفترة نصف المفتوحة، فترتين مغلقتين — and
«لتكن $I$ فترةً» where the text had «ليكن $I$ مجالاً».

**Deliberately kept — 8 sites where مجال is not an interval.** All verified
against the English, all of them *domain* or *range*, the two senses
`arabic_style_card.md` §3 reserves the word for:

| site | Arabic | English |
|---|---|---|
| `ar/05-normed-spaces.tex:501` | بتصغير **مجال التعريف** | "shrinking the **domain**" |
| `ar/10-function-sequences.tex:36` | خاصية **لمجال التعريف** | "a property of the **domain**" |
| `ar/08-real-functions.tex:406` | محدب على **مجال تعريفه** | "convex on their **domain**" |
| `solutions/ar/05-normed-spaces.tex:200` | رتابة النهاية العليا في **مجال التعريف** | "monotonicity of the sup over the **domain**" |
| `ar/19-surfaces.tex:61` | في كل نقطة من **مجالها** (المفتوح) | "everywhere on its (open) **domain**" |
| `ar/15-differential-calculus.tex:319` | وعلى **مجال** ذي حافة | "on a **domain** with boundary" |
| `ar/14-fourier-series.tex:140` | ويجعل **مجال الدليل** المتناظر | "the symmetric index **range**" |
| `ar/07-sequences-series.tex:55` | وبجمع **المجال المشترك** $0 \leq n \leq N-1$ | "collecting the common **range**" |

Two pre-existing «فترات» in `solutions/ar/21-countable-probability.tex`
(347, 405) mean *stretches* of a random walk with no tie; they were already
correct and were not touched.

### 4. intermediate values: → القيم الوسطى

The settled series form is **مبرهنة القيم الوسطى**. Book 4 had two forks, and
the sweep covered both:

- **القيم المتوسطة (4 sites).** Three are the IVT and became القيم الوسطى:
  `ar/23-generating-functions.tex:492`, `solutions/ar/23-generating-functions.tex:13`
  ("intermediate value theorem") and `solutions/ar/16-differential-equations.tex:411`
  ("intermediate values"). The fourth, `ar/20-multiple-integrals.tex:344`
  `\begin{example}[القيم المتوسطة]`, is the English *"Average values"* example
  whose body defines the **mean value** of $f$ over a region — genuinely mean,
  so **kept**.
- **القيم الوسيطة (9 sites) and القيمة الوسيطة (1 site)** — a second spelling
  of the same *intermediate* sense that the brief's count did not reach. Book 3
  uses it once, Book 5 not at all, so these were merged into القيم الوسطى /
  القيمة الوسطى too: `ar/04-metric-topology.tex` (447–448, 481, 532, 560, 586),
  `ar/06-comparison-functions.tex` (327, 434–435), `ar/08-real-functions.tex:401`,
  `ar/20-multiple-integrals.tex:109`, `solutions/ar/05-normed-spaces.tex`
  (318, 327–328), `solutions/ar/08-real-functions.tex:22`, and
  `ar/01-sets-structures.tex:669` ("exactly the intermediate value found by
  substitution").

**Deliberately kept — the 11 «القيمة المتوسطة» sites are the *mean value*
theorem and the mean value inequality** (`ar/15-differential-calculus.tex`
44, 107, 122–123, 131, 146, 171, 488, 490; `ar/23-generating-functions.tex`
128, 449, 477; `ar/20-multiple-integrals.tex:345`;
`solutions/ar/15-differential-calculus.tex` 131, 164;
`solutions/ar/23-generating-functions.tex:473`). English says *mean value* at
every one of them, and Book 5 needs the same form for متراجحة القيم المتوسطة.

### `book4_ar.py`

One entry keyed on a retired surface form:
`"الأشعة الذاتية": "def:b2:reduction:eigen"` → `"المتجهات الذاتية"`, with a
comment pointing at the style card. Nothing else in `NOT_A_TERM`, `DROP`,
`EXTRA`, `EXTRA_PROTECT` or `DERIVED` referenced any of the four families.

### What pass 2 did **not** change

The math multiset of all 46 files is byte-identical to what pass 1 shipped
(verified programmatically, ignoring `\omterm` wrappers); `\label`,
`\cref`/`\ref` targets and `\begin{solution}{key}` are untouched;
`check_translation.sh` still reports the environment/figure census identical to
English.

### One divergence recorded, and since RESOLVED by the orchestrator

Book 4 writes the accusative tanween as **اً** (1 458 sites, 0 of ًا) while
Books 3 and 5 write **ًا** (Book 3: 2 738 sites, 0 of اً). This is an
orthographic convention, not a word-family fork — a reader sees the same word —
and normalising it would mean touching 1 458 unrelated sites in a book whose
gates are green. The new متصلاً / فترةً / متجهةً forms were therefore written
in Book 4's own convention so the book stays internally consistent. **Flagged
for the orchestrator** as a series-level decision, since it is the last visible
Arabic difference between the three university volumes.

> **RESOLVED 2026-08-08 (orchestrator).** Measured across all six books, not
> just the three university ones: Book 4 was the sole outlier at 1 443 sites of
> ـاً, against **11 372 sites of ـًا** in Math 1, 2, 3, 5 and Physics 2, none of
> which used ـاً even once. ـًا is also the typographically preferred order.
> Because the change is a pure character-order swap (U+0627 U+064B →
> U+064B U+0627) with no agreement or meaning consequence, it was applied by
> script rather than by a further agent pass — first verifying that no genuine
> occurrence sits inside mathematics and that `book4_ar.py` contained none.
> 1 443 sites in 28 of the 46 files. Re-gated afterwards: `check_translation.sh
> bachelor-2 ar` PASSED, prose gate 0 across all nine classes, link layer
> regenerated to **1 646 links** with `--check` idempotent, `\omterm` target
> parity unchanged at 84 of 85 shared, and the build back at **0 errors,
> 0 undefined, 2 overfull** (the same two known display-math boxes), 380 pp.
> The judgement to flag rather than act was the right one — the decision needed
> the other three books' evidence, which this agent could not see.

## Verdict in one line

A natively written Arabic second-year university course: an exact structural
mirror of English down to every environment count, mathematics byte-identical
to the canon, a curated term-link layer whose target set matches English's
84 targets out of 85, a nine-class Arabic prose gate at **0 issues across all
46 files**, and a build with zero errors, zero undefined references and two
overfull boxes that are inherited display math, not prose.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Terminology | **96** | A complete Arabic technical glossary was built and applied uniformly across 46 files: مجموعة، تطبيق، قابلية العد، تساوي القوة، زمرة/حلقة/جسم، مثالي، مجموعة القسمة، تبديلة/دورة/مبادلة، الزمرة المتناوبة، تشاكل/تشاكل تقابلي، الفضاء الثنوي، المبيد، المنقول، المحدد، الأثر، القيمة/الشعاع الذاتي، الطيف، قابل للتقطير/للتثليث، معدوم القوى، تفكيك دونفور، الفضاء المتري، مفتوح/مغلق، متراص، مترابط، تام، تقلص، المعيار، معيار المؤثر، سلّم المقارنة، عائلة قابلة للجمع، تكامل معتل، التقارب المهيمن، التقارب المنتظم/النقطي/الناظمي، متسلسلة قوى، دالة تحليلية، صورة تربيعية، البصمة، المرافق، متعامد ممنظم، هرميتي، وحدوي، متسلسلة فورييه، التفاضل، مصفوفة جاكوبي، مصفوفة هس، الفضاء الأفيني، مركز الثقل، الغلاف المحدب، طول القوس، الانحناء، الالتواء، معلم فرينيه، دائرة التقبيل، المطوّرة، المغلِّف، الصورة الأساسية الأولى، التكامل المنحني، الصورة التفاضلية، الجاكوبي، الفضاء العيني، الاحتمال الشرطي، الأمل الرياضي، التباين، التغاير، الدالة المولّدة، مسار التفرع، احتمال الانقراض. Proper names transliterated once and reused (كانتور، لاغرانج، بيزو، أويلر، كوشي، بناخ، ريمان، لوبيغ، فورييه، هيلبرت، فايل، شور، هادامار، تشوليسكي، لوجاندر، ليوفيل، غرونوال، دوهاميل، دو موافر، تشيبيشيف، هولدر، مينكوفسكي، جنسن، داربو، شوارتز، بيانو، أرتزيلا--أسكولي، بور--موليروب، بيرون--فروبينيوس، بوليا، كولموغوروف، هوفدينغ، تشيرنوف، ياغلوم) |
| Register / tone | **96** | University lecture register end to end — ليكن / لتكن / نفترض أن / برهن على أن / بيّن أن / استنتج أن / ومنه / لدينا — with the English book's voice carried rather than flattened: «فالرجل السكران يجد طريقه إلى البيت؛ أما الطائر السكران فقد لا يجده»، «فالاحتمالات الصغيرة ميدان يحتاج فيه الحدس إلى الأسّي، لا إلى المسطرة»، «أعد التوسيم أولا، ثم استنتج ثانيا»، «فالكرة المصمتة العالية البعد، إحصائيا، فطيرة رقيقة في كل اتجاه في آن واحد»، «والنرد لا يتذكر، ولا ``تستحق'' أي ستة الظهور أبدا» |
| Script hygiene | **99** | All nine gate classes at 0 over 46 files: `english`, `translit`, `punct`, `digits`, `math-space`, `bidi-ctrl`, `presform`, `tatweel`, `split-number`. ASCII digits 0–9 throughout prose and mathematics; Arabic ، ؛ ؟ with the Latin full stop; no tatweel, no ZWNJ/RLM/LRM, no presentation forms |
| Term-link layer | **95** | `book4_ar.py` grown from a seed to a curated config with 30 documented `DROP` decisions and 15 `EXTRA` broken plurals. 1 646 links after the pass-2 regeneration (1 613 before), **84 targets against English's 85 — unchanged by pass 2** (`AR − EN = ∅`; `EN − AR = {pb:b2:hermitian:1}`). `--check` green and idempotent. Deduction: link *density* is half English's, deliberately (see "why not 100") |
| LaTeX hygiene | **97** | 0 fatal errors, 0 undefined references, **2 overfull boxes**, both `detected at line` inside display math that is byte-identical to English (which builds them at 0) — an RTL width difference in a file this agent must not touch. 46 files valid UTF-8, 0 TeX accent escapes, no nested `\omterm` |
| Cross-refs / rule compliance | **99** | `\label`, `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English (806 labels, 299 solution keys, identical sets). 0 duplicate labels. 0 cross-volume `\cref` leakage (`:b1:`, `:b3:`, `:g1x:`). No country or curriculum name in visible text; cross-volume references read «مجلد السنة الأولى»، «مجلد السنة الثالثة»، «مجلد الثانوية» |
| Structural fidelity | **99** | Exact mirror: 23 chapters / 23 solution files both sides; 125 sections, 89 theorems, 65 definitions, 25 propositions, 6 corollaries, 5 lemmas, 272 examples, 99 remarks, 16 methods, 276 exercises, 23 problems, 299 solutions, 130 proofs, 168 enumerates, 3 figures, 20 omfigures, 30 `tikzpicture`, 11 `axis`, 184 `pmatrix`, 186 `\index` — every census identical to English |
| Mathematics fidelity | **99** | The math multiset of every one of the 46 files is byte-identical to English, once `\text{…}` and `\index{…}` payloads (which are visible text) are set aside. Exactly one divergence in the whole tree, and it is deliberate: `$f' $` → `$f'$` in ch. 14 (see the orchestrator request) |
| Solutions | **97** | All 299 solutions present, complete and native; `\section*{الفصل \ref{ch:…} --- <title>}` headers localized with the English `ch:` slug untouched |
| Figures | **98** | TikZ/pgfplots drawing code byte-identical to English; only node text and captions localized (`center of curvature` → «مركز الانحناء», `saddles / stable nodes / centers` → «سروج / عقد مستقرة / مراكز», `ellipsoid` → «مجسم إهليلجي», `small $n$ / large $n$` → «صغيرة $n$ / كبيرة $n$») |

Weighted (terminology 0.18, register 0.18, script hygiene 0.14, term-link 0.12,
LaTeX 0.10, cross-refs 0.08, structure 0.06, mathematics 0.06, solutions 0.05,
figures 0.03) the arithmetic gives **97.0**; reported as **96**, rounded down
for the link-density gap described below.

## Structural / build gates (re-measured 2026-08-08 after pass 2)

> The Arabic book builds with **LuaLaTeX** (dispatched by `latexmkrc` for
> `*_ar.tex`). Measure on `build/one_math_book_4_university_year_2_ar.log`,
> which is the **last** run; the piped console log concatenates every
> `latexmk` pass and therefore still contains the first pass's undefined
> references. Use `grep -a`, the log is not UTF-8 throughout.

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-2 ar` | **PASSED** — arabic prose gate OK (46 files) |
| Arabic prose gate, nine classes (`english`, `translit`, `punct`, `digits`, `math-space`, `bidi-ctrl`, `presform`, `tatweel`, `split-number`) | **0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0** |
| `python3 tools/link_defined_terms.py --book 4 --lang ar --unwrap --apply` | 1 646 links removed, then 0 |
| `python3 tools/link_defined_terms.py --book 4 --lang ar --apply` | **1 646 links** across 45 files (def 1 458, thm 89, pb 65, ex 29, lem 4, prop 1) — 209 linkable terms; pass 1 gave 1 613 |
| `python3 tools/link_defined_terms.py --book 4 --lang ar --check` | **green** — every file matches the config, idempotent |
| `\omterm` first-arg parity vs English | **84 of 85 targets shared**; `AR − EN = ∅`, `EN − AR = {pb:b2:hermitian:1}` — **identical to pass 1**, re-measured after the sweep |
| `latexmk one_math_book_4_university_year_2_ar.tex` | exit 0 |
| Fatal errors (`grep -ac '^!'`) | **0** |
| Undefined references (`LaTeX Warning: Reference`, `There were undefined references`) | **0 / 0** |
| Overfull `\hbox`/`\vbox` | **2** (3.5362 pt, 1.85275 pt), both `detected at line` in display math identical to English (EN: 0) — the same two boxes as pass 1, unmoved |
| AR PDF | `build/one_math_book_4_university_year_2_ar.pdf`, **380 pp** (unchanged by pass 2) (EN 397, FR 417, HI 388); token count 187 836 vs EN 195 391, so no padding |
| Exercise ↔ solution key parity | **0 divergences** (276 `exo:` + 23 `pb:` ↔ 299 `\begin{solution}`) |
| `\label` sets EN vs AR | **identical**, 806 each; duplicates in the `ar` tree: **0** |
| `\cref`/`\ref` target sets EN vs AR | **identical**; cross-volume leakage: **0** |
| Index keys: EN ∩ AR intersection | **0 keys** (185 AR, 184 EN) |
| Mathematics multiset EN vs AR, per file | **identical in 46/46**, one deliberate exception (`$f' $`) |
| TeX accent escapes / non-UTF-8 files / non-ASCII digits | 0 / 0 / 0 |
| Country / curriculum names in visible text | **0** |

**Not gated, for the record:** 113 underfull `\hbox`/`\vbox` warnings after pass 2
(115 before; EN 104, HI 111) — the series norm.

## How it was done

1. **Everything is a fresh derivation from English.** Each English file was
   mechanically split into a *skeleton* of prose carrying `<<N>>` placeholders
   and a *slot table*, with every `$…$`, `\[…\]`, math environment,
   `tikzpicture`/`axis`/`circuitikz` body, `\label`, `\cref`/`\ref`, `\qty`,
   `\unit`, `\includegraphics`, `\begin{solution}{key}` and the **first
   argument of every `\omterm`** protected byte-for-byte. The Arabic prose was
   authored against the skeleton and rebuilt by a builder that **refuses to
   write a file unless every marker reappears exactly once** — several real
   placeholder errors (a dropped marker in ch. 03 that shifted 340 later
   markers; a re-ordered marker run in `solutions/01`) were caught this way.
   A second census pass then compared, per file, the counts of every
   environment, `\item`, `\emph{`, `\index{`, `\textbf{`, `\dots`,
   `\admitted`, `\\`, `&` and the exact `\label` sequence; that gate caught
   seven silently dropped `\emph{}` emphases which were restored.
   Environment optional titles, `\text{…}` payloads, TikZ node texts and
   captions were lifted into the slot table and translated *there*, so figure
   *drawing* code is provably byte-identical while figure *text* is Arabic.
2. **`tools/term_config/book4_ar.py` curated.** `NOT_A_TERM` was corrected:
   the seed listed «معيار» as a result-name head, but in this book معيار is
   the translation of *norm* (a genuine defined term) and *criterion* is
   محك — the two were swapped. 30 `DROP` decisions were then made, each after
   reading the term's link displays in context, and each documented in the
   file with the sense clash that motivated it. 15 `EXTRA` entries declare the
   broken plurals that `lang_ar.py` deliberately cannot reach
   (`WORD_TAIL = ''`, `DERIVE = False`).
3. **`AMBIG_POLICY` kept `"drop"`,** as briefed and as `book4_en.py` does; the
   gate this edition is measured against is sense parity with English.
4. **Wrong-sense link hunt.** The Arabic proclitic morphology (`HEAD` with
   `HEAD_ON_EVERY_WORD`) links a term through ال، و، ف، ب، ك، ل, which is
   exactly what makes Arabic linkable at all — and exactly what makes a short
   term fire in the wrong sense. Real wrong-sense links found and killed:
   - **«رتبة» → `def:b2:structures:generated` (194 sites).** The order of a
     group element in ch. 1 *and* «من الرتبة الثانية» — the order of a
     derivative, of a Taylor expansion, of an ODE — in eighteen other
     chapters. English stoplists `order`; hard-dropped here.
   - **«دورية» → `def:b2:structures:generated` (60 sites).** *Cyclic* in
     ch. 1, *periodic* in every chapter after ch. 14. «زمرة دورية» keeps the
     target.
   - **«يتقارب» → `def:b2:integration:improper` (40 sites).** A verb
     («converges») harvested from the improper-integral definition; it fired
     on every series in chapters 7, 10, 11, 14, 20, 21, 23. «تكامل معتل»
     carries the target.
   - **«بانتظام» → `def:b2:funcseq:def` (69 sites).** Uniform convergence in
     ch. 10, but also *uniformly continuous* and *uniformly at random*.
     «تقارب منتظم» carries the target.
   - **«مرافق» → `def:b2:quadratic:adjoint` (14 sites).** The adjoint `u^*`
     in ch. 12–13, but also the algebraic *cofactor* and the *subordinate*
     norm in ch. 15 and a *conjugate* pair in ch. 16.
   - **«مغلقة»/«تامة» → `def:b2:multint:exact` (28 sites).** Closed and exact
     differential forms in ch. 20, but also closed sets and curves, and
     «تامة» as *strict* («قيمة صغرى محلية تامة»). «صورة مغلقة»/«صورة تامة»
     keep the target, exactly as English keeps `closed form`.
   - **«جبر» → `def:b2:structures:algebra` (19 sites).** The algebra
     structure of ch. 1, but «الجبر الخطي» and «جبر σ» are what the word
     almost always means here.
   - **«دورة» → `def:b2:structures:sn` (35 sites)** — a permutation cycle in
     ch. 1, a full turn in ch. 16/18/19. **«الإشارة»** — the signature of a
     permutation and the sign of a number. **«مستقلين»** — independent
     *events* in ch. 21 and linearly independent *vectors* everywhere before.
     **«متكافئين»**, **«محدبة»** (any convex *function* vs the convex *set*),
     **«التوافق»**, **«طوله»** — same story, all documented in the config.
   - Named **results** rather than notions, one-for-one with `book4_en.py`'s
     own `DROP`: صيغة غاوس الحدّية، مبرهنة كوروفكين، متراجحة هادامار،
     مبرهنة كوران--فيشر، متراجحات فايل، صيغة جاكوبي، مبرهنتا شتورم،
     حصر تشيرنوف، متراجحات التركيز، ظاهرة غيبس، دالة أويلر، نقطة المركز،
     توقيع، مصفوفة هس. Dropping these is what took the `AR − EN` target
     difference to **∅**.
5. **Broken plurals declared, not derived.** Arabic pluralises by internal
   vowel change, so «حلقات القسمة»، «السطوح الموسّمة»، «الأقواس الموسّمة»،
   «الفضاءات المترية/الأفينية/الذاتية/المعيارية»، «المتغيرات العشوائية»،
   «الصور التربيعية/التفاضلية»، «القيم الذاتية»، «الأشعة الذاتية» each had to
   be listed by hand in `EXTRA`. That alone recovered two of the three targets
   English had and Arabic did not.
6. **Three English `\index{}` keys localized by hand.** `Jensen's inequality`,
   `Stirling's formula` and `spectral theorem` sit *inside display math*,
   where the pipeline correctly refuses to touch anything; localizing them
   took the EN ∩ AR index-key intersection to **0**.
7. **Build driven from 16 overfull boxes to 2.** An intermediate build had 16;
   fourteen were "in paragraph" boxes cleared by tightening Arabic prose, with
   no structural change. The remaining two are display math (below).

## Sampled passages, judged

**1. `ar/01-sets-structures.tex`, chapter opening — native.**

> يشحذ هذا الفصل الافتتاحي الأسس الموضوعة في مجلد السنة الأولى ويحوّلها
> إلى أدوات عمل يومية: حساب المجموعات ومجموعات القسمة، ومقارنة المجموعات
> غير المنتهية (قابلية العد، كانتور--برنشتاين)، والنظرية البنيوية للزمر
> والحلقات […] كل ما هنا يُستعمل بلا انقطاع في بقية الكتاب.

Verbal-sentence word order throughout (يشحذ … ويحوّل …), correct إضافة chains
(«النظرية البنيوية للزمر والحلقات»), and «يشحذ» / «أدوات عمل يومية» rather
than a calque of *sharpens into everyday tools*. No English residue.

**2. `ar/22-discrete-random-variables.tex`, the gambler's fallacy — native.**

> فالنرد لا يتذكر، ولا ``تستحق'' أي ستة الظهور أبدا --- ومغالطة المقامر هي
> الاعتقاد بأن القانون الشرطي كان ينبغي أن ينزاح. […] فكل زمن انتظار لا
> يتحدث تنبؤه أبدا يكون هندسيا.

Carries the English aphorism without importing its syntax; «تستحق» is the
ordinary Arabic verb for *to be due/owed*, which is exactly the rhetorical
move the English makes with *due*, and «لا يتحدث تنبؤه» reads as Arabic, not
as translated English.

**3. `solutions/ar/21-countable-probability.tex`, Pólya's theorem — native.**

> فالسير العشوائي البسيط عوّاد على $\Z$ و$\Z^2$، وعابر على $\Z^d$ من أجل
> $d \geq 3$. فالرجل السكران يجد طريقه إلى البيت؛ أما الطائر السكران فقد لا
> يجده.

The joke survives, which is the hardest thing to get right here; عوّاد /
عابر are the standard Arabic renderings of *recurrent* / *transient*, and the
أما … فـ construction gives the punchline its beat.

**4. `ar/20-multiple-integrals.tex`, "Method: choosing the change of
variables" — native.**

> اقرأ معادلات الحد، ودع \emph{هي} تختار الإحداثيات؛ ويحوّل الجاكوبي عندئذ
> مساحة خلية الشبكة المنحنية الأضلاع […] ثلاث خانات ينبغي التأشير عليها قبل
> المكاملة.

Imperative lecture register (اقرأ، ودع) exactly as the brief asks; «ثلاث خانات
ينبغي التأشير عليها» is the natural Arabic for *three boxes to tick*.

**5. `ar/18-curves.tex`, the local-study method — near-native.**

> المعلم $(u, v)$ \emph{ليس} متعامدا عادة --- فالجدول يصف المواضع بالنسبة
> إلى المماس، لا الزوايا ولا المسافات، فلا تقرأ الانحناء من الصورة.

Correct and fluent, but «المطوّرة» (for *evolute*) and «المغلِّف» (for
*envelope*), used a few lines further down, are principled coinages that an
Arabic-medium reader is likely to meet here for the first time; the register
is a shade more compressed than a lecture would be. Judged *near-native*
rather than native for that reason only.

No passage sampled was judged *MT*.

## Why not 100

1. **Link density is half English's (−1.5).** 1 646 links against English's
   3 511, on an identical target set bar one. The gap is structural, not
   sloppy: fourteen of English's most frequent link displays are single words
   whose Arabic equivalents carry a second, far more common ordinary sense
   (order/rank, cyclic/periodic, closed, converges, uniformly, independent,
   sign, algebra, adjoint/cofactor/conjugate), and the proclitic `HEAD` rule
   makes each of them fire through ال، و، ف، ب، ك، ل as well. Erring toward
   fewer, correct links was the deliberate choice; every one of the 30 `DROP`
   decisions is documented in the config with the clash that motivated it.
2. **One English target has no Arabic site outside its own definition
   (−0.5).** `pb:b2:hermitian:1` (the Rayleigh quotient, «خارج قسمة رايلي»):
   all four Arabic occurrences sit inside the very problem that defines it,
   which the linker correctly refuses to self-link. Forcing it would have
   meant rewriting prose to create a mention, which is worse than a missing
   link.
3. **Arabic has no settled term for a handful of nineteenth-century curve and
   surface notions (−1).** *osculating circle*, *evolute*, *envelope*,
   *caustic*, *cusp*, *nephroid*, *astroid*, *cycloid* were rendered
   دائرة التقبيل، المطوّرة، المغلِّف، المنحنى الحارق، نقطة الرجوع، الكلوية،
   النجمية، الدويري. Each is a principled Arabic coinage rather than a
   transliteration, each is used consistently, and each is introduced next to
   its defining formula — but a different Arabic mathematical tradition might
   choose differently.
4. **Two overfull boxes remain, and they are not prose (−1).** Both are
   `detected at line` inside display math that is byte-identical to English —
   `solutions/06-comparison-functions` (the `u_n = \sqrt{2n}(…)` chain, 3.54 pt)
   and `solutions/19-surfaces` (the torus `\sigma_\theta, \sigma_\psi` pair,
   1.85 pt). The English book sets both at zero overfull, so the ~4 pt comes
   from the RTL layout, in files this agent must not touch (see the request
   below). Fixing them from this side would mean editing mathematics, which
   the brief forbids.

## Requests to the orchestrator

These are all in files this agent must not touch.

1. **English-canon nit, for the canon's owner — a stray space inside inline
   math.** `parts/bachelor-2/14-fourier-series.tex:105` contains `$f' $`. The
   Arabic prose gate's `math-space` class rejects a space at the edge of
   inline math, so this is the **one and only** place in the whole book where
   the Arabic mathematics is not byte-identical to English: the `ar` file
   carries `$f'$`. Removing the space in the canon would restore exact
   identity and costs nothing typographically. (The Hindi pass raised the
   same nit on 2026-08-01; it is still there.)
2. **English-canon nit — `\cref` split across a line break.**
   `parts/bachelor-2/solutions/23-generating-functions.tex:404–405` has
   `\cref` on one line and `{thm:b2:genfun:compound}` on the next. Any tooling
   that protects `\cref{…}` as a single token — including
   `tools/check_arabic_prose.py`, which reported `thm`, `genfun` and
   `compound` as *English in visible text* — sees a bare `\cref` followed by a
   brace group of English words. It was worked around locally by joining the
   two lines in the generated `ar` file; joining them in the canon would help
   every translation. (Also flagged by the Hindi pass.)
3. **Two overfull display boxes appear only in the RTL layout.** The two
   displays named in "why not 100" are byte-identical to English and overflow
   the Arabic measure by 3.54 pt and 1.85 pt while the English build reports
   zero overfull boxes. That points at a small difference in the effective
   line width for display math inside `solution` under
   `babel bidi=basic, layout=graphics` — in `styles/**` or in
   `one_math_book_4_university_year_2_ar.tex`, both orchestrator-owned. Either
   widening that measure by ~4 pt or adding a display-math
   `\allowdisplaybreaks`/`\thinmuskip` tweak in the RTL branch would take the
   book to 0 overfull without anyone touching mathematics.
4. **`tools/term_config/lang_ar.py` — consider an optional definite-plural
   tail.** `WORD_TAIL = ''` is the right default for broken plurals, and the
   docstring's reasoning is sound. But the *sound* feminine plural ات and the
   dual ان/ين are fully regular and cover a large fraction of this book's
   terms (مبرهنات، مصفوفات، دالتان، فضاءان). A tail of the shape
   `(?:ات|تان|تين|ان|ين)?` applied **only when the base term already matched**
   would let roughly a third of the 15 hand-written `EXTRA` plurals in
   `book4_ar.py` be deleted, and would spare the next Arabic book from
   rediscovering the same list. Broken plurals would still need declaring;
   that is unavoidable.
5. **No change requested to `tools/check_arabic_prose.py`.** Every one of its
   findings during this pass was a real defect in my prose — tatweel after a
   proclitic (the dominant error, ~40 sites), one stray ZWNJ, one stray RLM,
   a Latin `iii` in a pitfall list, and the `\cref` line break of request 2.
   It flagged nothing spurious.

## Files written by this pass

- `parts/bachelor-2/ar/01-sets-structures.tex` … `23-generating-functions.tex`
  — 23 files, all new
- `parts/bachelor-2/solutions/ar/01-sets-structures.tex` …
  `23-generating-functions.tex` — 23 files, all new
- `tools/term_config/book4_ar.py` — curated (45-line seed → documented config
  with 30 `DROP` decisions and 15 `EXTRA` plurals)
- `translation_scores/book_4/ar/translation_score.md` — this file

`one_math_book_4_university_year_2_ar.tex`, `styles/**`, `latexmkrc`,
`tools/check_translation.sh`, `tools/check_arabic_prose.py`,
`tools/termlink/**`, `tools/term_config/lang_ar.py` and `arabic_style_card.md`
were read but **not modified**.

**No git commits were created.** The working tree is left for review.
