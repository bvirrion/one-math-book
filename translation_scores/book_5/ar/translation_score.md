# Translation score — Math Book 5 · Arabic (`ar`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 5 (University Year 3, `bachelor-3`) |
| **Language** | Modern Standard Arabic (`ar`), university lecture register as fixed by `arabic_style_card.md` |
| **Quality bar** | **native academic** — an Arabic-medium third-year lecture course. English (`parts/bachelor-3/*.tex`) is the sole source of truth for content; `parts/bachelor-3/fr/` was consulted only as an intra-series reference for how far a Book 5 translation may depart from English clause order, never as a ceiling |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **met** |
| **Date** | 2026-08-08 (edition written); **2026-08-08 — cross-book consistency pass**, see below |
| **Scope of this pass** | The whole edition, written from the English canon: **46 files** (23 chapters + 23 solution files), all bodies produced through a masking pipeline that refuses to write a file unless every `$…$`, `\[…\]`, `tikzpicture`, `\label`, `\cref`, `\begin{solution}{key}` and `\omterm` first argument reappears exactly once, followed by a deliberate native pass over titles, `\emph`, `\index`, `\omterm` displays and drawing text. `tools/term_config/book5_ar.py` was curated from the seed (empty `STOP`/`DROP`/`EXTRA`/`EXTRA_PROTECT`) to a 32-entry stop list plus two Arabic-only protect patterns |

## Verdict in one line

A complete, structurally exact, natively written Arabic third-year course:
**722 labels and 299 solution keys identical to English in set *and* order**,
a zero-mismatch environment census over 19 environment types, **0 tatweel,
0 Arabic-Indic digits, 0 bidi controls, 0 Latin letters in any index display**,
the nine-class prose gate green on all 46 files, and a build with **0 errors,
0 undefined references and 0 overfull boxes** at 377 pages — with the one
honest weakness being a deliberately thinner link layer (2 228 vs English's
4 326) bought by removing ~630 wrong-sense links that Arabic's proclitics
manufacture and English cannot.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| **Register / tone** | **96** | University lecture Arabic throughout, with the style card's stock phrases used as connectives rather than decoration: `ليكن / لتكن`, `نفترض أن`, `برهن على أن`, `نستنتج أن`, `ومنه`, `لدينا`, `إذا وفقط إذا كان`, `من أجل كل`, `عندئذٍ`, `وأما … فـ`. Statement stems follow `styles/lang/ar.tex` (مبرهنة / قضية / مبرهنة مساعدة / نتيجة / برهان). Exercise stems are imperative (`احسب`, `برهن على`, `استنتج`, `تحقق من`, `أبرز`, `عيّن`), solutions declarative and telegraphic like the English. No school-register `أنت` voice anywhere; no `يمكننا أن نقول إن` padding |
| **Terminology** | **96** | One vocabulary across all nine subject areas, fixed on first use and never drifting: زمرة / زمرة جزئية ناظمية / صف مجاور / تشاكل / تماثل / نواة / مدار / مثبِّت · حلقة / مثالي / حلقة تامة / إقليدية / حلقة تفكيك وحيد / نويثرية · مقاس / حر / التواء / صيغة سميث الناظمية · حقل / امتداد / حقل الانشطار / قابل للفصل / غالوا · طوبولوجيا / مفتوحة / الغلق / الداخل / كثيفة / متراص / مترابط / هاوسدورفي · قياس / جبر من النمط $\sigma$ / في كل مكان تقريبًا / قابلة للمكاملة · فضاء هيلبرت / جداء سلّمي / أساس هيلبرتي / بارسيفال · هولومورفية / مرومورفية / باقٍ / قطب / شذوذ جوهري / مطابق · متنوعة جزئية / فضاء مماسّ / صيغة تفاضلية / سحب عكسي / توجيه · فضاء احتمالي / متغيّر عشوائي / أمل / تباين / دالة مميِّزة / شبه أكيد. Proper names are transliterated once and reused (لوبيغ، فوبيني، تونيلي، باناخ، هيلبرت، فورييه، بلانشرِل، غالوا، ستوكس، براور، لوتكا--فولتيرا، إتِمادي، هوفدنغ). Two places where Arabic simply has no settled term keep a transliteration on purpose — **هولومورفية** and **مرومورفية**, both standard in Arabic mathematical writing. **Since the 2026-08-08 consistency pass this dimension is also aligned *across* the series**, not only inside the book: interval = فترة, vector = متجهة, countable = قابل للعدّ, norm = معيار, criterion = محك, IVT = مبرهنة القيم الوسطى — the five families where Book 5 had drifted from Books 2–4 and from `arabic_style_card.md` §4. The score stays at 96 rather than rising: the pass removed a real defect, but it removed one that should never have been introduced, and the remaining deductions (two transliterated head-terms) are untouched by it |
| **MT-artifact freedom** | **98** | `check_arabic_prose.py` **OK on all 46 files**, all nine classes at zero: `english` 0, `translit` 0, `punct` 0, `digits` 0, `math-space` 0, `bidi-ctrl` 0, `presform` 0, `tatweel` 0, `split-number` 0. The gate reads `\text{…}` arguments out of math and TikZ node text, so the class that usually hides is covered: 923 `\text`-style arguments on the Arabic side (917 on the English), none carrying English words. Independently verified on the concatenated tree: **0 occurrences of U+0640**, **0 Arabic-Indic digits**, **0 bidi control characters**. Digits are ASCII 0–9 in prose and in mathematics, Latin full stop ends sentences, `،` `؛` `؟` do the rest |
| **Structural fidelity** | **99** | Exact mirror. **722 `\label`s identical to English in set *and* order**; **299 `exo:`/`pb:` labels ↔ 299 `\begin{solution}{…}` keys, byte-identical on both sides**; environment census equal to English with **zero mismatches** over 19 gated environments (88 `definition`, 145 `theorem`, 219 `proof`, 276 `exercise`, 23 `problem`, 15 `tikzpicture`, 15 `omfigure`, `enumerate`, `itemize`, `solution`, `center`, `tabular`, …); 1 404 `\emph{` = 1 404, 675 `\item` = 675, 1 039 display openers = 1 039. `check_translation.sh bachelor-3 ar` **PASSED** |
| **LaTeX hygiene** | **98** | 0 fatal errors, 0 undefined references, **0 overfull boxes**, at 377 pages. No `\end{env>` typo class, no duplicate labels, no TeX accent escapes, no drafty `...`. The five overfull boxes the first full build reported were all fixed *in Arabic prose* (rewording, moving a parenthetical, shortening two `\text{}` labels inside a display to match English brevity) — never by touching a formula |
| **Cross-refs / rule compliance** | **99** | Every `\label`, every `\cref`/`\ref` target, every `\begin{solution}{key}` and every `\omterm` **first** argument is byte-identical to English; all 123 Arabic link targets resolve to real `\label`s. Arabic `\crefname` definite forms come from the (orchestrator-owned) `styles/lang/ar.tex`, so a reference reads `حسب المبرهنة 12.4` and not `حسب مبرهنة 12.4`. Zero country, board or curriculum names in visible text; cross-volume references are prose-only (`السنة الجامعية 2`), matching the convention already used in ch. 6 |
| **Solutions** | **96** | All 299 solutions present, complete and natively written — including the long weekend problems (Stirling with a two-sided bracket, Hardy's constant, Lindeberg's swapping with rates, Le Cam, Brouwer, $SO(3)$ and the quaternions). Localized `\section*{الفصل \ref{ch:…} --- <title>}` headers with unchanged `ch:` slugs |
| **Figures** | **98** | All 15 `tikzpicture`s and 15 `omfigure`s present; drawing code (coordinates, `domain`, `samples`, styles, colours) untouched — only `node {…}` text and captions localized (e.g. the heat-kernel figure's `$t = 0.1$ / $t = 0.4$ / $t = 1.6$` labels and the outward-normal figure's `$M$ / $\partial M$ / $\nu$ / المستحثّ`) |
| **Term links** | **90** | **2 228 links across 46 files on 123 targets**, idempotent: `--unwrap --apply` removes exactly what `--apply` reinserts, and `--check` reports every file matching what the config generates. `check_book5_golden.sh` (the English-side regression fixture) still passes byte-for-byte. This is **51.5 %** of English's 4 326, and that gap is the honest weak point of the edition — see below |

**Overall: 96** — weighted toward register, terminology and MT-artifact
freedom, since structure is gated mechanically (`check_translation.sh`, the
label/solution-key diffs, the environment census) and is exact. The link
dimension costs the edition its 97th point.

## The link layer, honestly

English inserts 4 326 links; Arabic inserts 2 228. Nearly all of the
difference is **deliberate**, and the reason is morphological rather than
editorial.

`lang_ar.py` sets `HEAD = (?:لل|[وفبك]?ال|[وفبكل])?` with
`HEAD_ON_EVERY_WORD = True`, because the article `ال` and the one-letter
particles `و ف ب ك ل` are written joined and repeat on every word of a noun
phrase; without that, almost nothing links. The price is that a one-word
Arabic term matches far more text than its English twin, and Arabic
technical words are more polysemous than the English ones because the
mathematical sense and the ordinary sense share a root.

The first generation inserted 2 861 links. Reading the top of the frequency
table showed the damage: `الدرجة` → `def:b3:galois:extension` **113 times**,
almost all of them the degree of a *polynomial*; `كاملة / الكاملة` →
`prop:b3:galois:perfect` 31 times, almost all of them the ordinary
"complete/entire"; `تامًّا` → `def:b3:complete:complete` 30 times, mostly the
adverb in `انعدامًا تامًّا`; `بجوار` → `def:b3:topology:topology` 61 times,
almost all of them the preposition "near"; `بسيطة` → `def:b3:groups:simple`
49 times across simple poles, simple functions and simple zeros; `مغلقة`
and `تامة` pointing every *closed set* and every *complete* thing at
`def:b3:forms:closedexact`.

`book5_ar.py` now carries a 32-entry `STOP` list that mirrors
`book5_en.py`'s decisions word for word where the words correspond
(*simple, dense, normal, maximal, radical, content, action, basis, degree,
free, Euclidean, separable, closed, exact, prime, path, boundary, interior,
a.e.*) and adds the Arabic-only traps (`كاملة`, `مركز`, `طابع`, `مدار`,
`الباقي`, `الدليل`, `غاوسية`, `التواء`, `متكاملة`). `STOP` still links a
word inside the chapter that defines it, so nothing is lost where the term
is actually introduced. Two `EXTRA_PROTECT` patterns (`بجوار`, `في\s+جوار`)
mask the preposition that collides with `جوار` = neighbourhood — a collision
English cannot have. Regenerating drops 29 terms and 633 links, and every
one of the 633 that I sampled was a wrong-sense link.

What remains is a **cleaner** layer than English's on a per-link basis and a
**thinner** one: 123 targets against English's 130. Thirteen English targets
carry no Arabic link (`prop:b3:galois:perfect`, `def:b3:holomorphic:index`,
`thm:b3:probability:zeroone`, `def:b3:topology:components`,
`prop:b3:holomorphic:cauchyriemann`, `thm:b3:hilbert:decomposition`, …) —
each one is a target whose Arabic term is precisely a stop-listed word, so
it links only inside its defining chapter, where the definition is on the
same page. Six targets are Arabic-only (`thm:b3:groups:firstiso`,
`lem:b3:rings:bezout`, `thm:b3:product:ballvolume`,
`thm:b3:submanifolds:characterizations`, `thm:b3:lebesgue:paramcont`,
`cor:b3:galois:impossible`): Arabic names those results with a noun phrase
(`مبرهنات التماثل`, `قاسم مشترك أكبر`, `متنوعة جزئية`) where English uses a
bare result name that `NOT_A_TERM` filters out.

**Request implicit in this**: nothing needs changing upstream. The tuning
lives entirely in the book-owned `tools/term_config/book5_ar.py`.

## Sampled passages, judged

Five passages read cold, against the question "would an Arabic-medium
lecturer have written this?".

**1 — ch. 11, chapter opening (native).**

> تصير نظرية لوبيغ ذات البُعد الواحد حسابًا متعدّد الأبعاد بواسطة
> مبرهنتين. فتقول \emph{تونيلي--فوبيني} إن التكاملات على الجداءات
> تكاملاتٌ متتالية --- أي إن التشريح مشروع، بأي ترتيب، تحت فرضيات يمكن
> التحقق منها فعلًا.

Verdict: **native**. The `فـ`-initial explanatory sentence, the appositive
`تكاملاتٌ متتالية` without a copula, and `أي إن` re-glossing the metaphor
are all Arabic expository moves, not English ones. `التشريح` for *slicing*
is the metaphor English uses, carried rather than calqued.

**2 — ch. 16, Liouville / d'Alembert–Gauss proof (native).**

> وإذا لم يقبل $P$ أي جذر، لكانت $1/P$ صحيحة ومحدودة (<<…>> حين
> $\abs z \to \infty$: إذ يهيمن الحدّ الرئيسي، ومنه يكون $\abs{1/P}$
> صغيرًا خارج قرص كبير ومتصلًا على القرص المتراص): فتكون ثابتة --- وهو
> محال من أجل $P$ غير ثابت.

Verdict: **native**. Counterfactual `لو … لكان`, the `إذ` causal, the `ومنه`
chain and the closing `وهو محال` are exactly how an Arabic proof ends a
reductio. English's participial "being bounded" is re-expressed, not
transcribed.

**3 — ch. 19, the method box (near-native).**

> حين تواجه معادلة تفاضلية: (1) الوجود والوحدانية --- تحقق من الليبشيتزية
> المحلية (وهي عادةً $\mathcal C^1$)؛ (2) الشمول --- بالنمو الخطي، أو
> الحدّية، أو متراصة صامدة عبر دالة ليابونوف أو تكامل أول؛ …

Verdict: **near-native**. The content and register are right and the
imperative `تحقق من` is idiomatic, but the dash-plus-fragment layout is
English typographic rhythm kept because the English `method` boxes are
telegraphic by design and the series wants them to look the same in every
language. An Arabic author writing from scratch would more likely use a
colon and a verb. Deliberate, not accidental.

**4 — ch. 22, Borel–Cantelli proof (native).**

> ومنه <<…>> من أجل كل $N$، ويبقى للتقاطع المتناقص على $N$ الاحتمالُ $1$
> (بالاتصال من الأعلى، …).

Verdict: **native**. The fronted predicate `ويبقى للتقاطع … الاحتمالُ $1$`
is a genuinely Arabic word order — a word-for-word rendering would have
produced `التقاطع المتناقص … لا يزال له احتمال $1$`, which reads as
translated.

**5 — ch. 21, Poincaré lemma proof (near-native, and the hardest page).**

> إذ تجمع الزمرة الأولى الحدودَ التي تصيب فيها $\dd$ العاملَ $x_{i_r}$ ---
> ويعيد الإسفين <<…>> تركيبَ $\dd x_I$ بإشارة $(-1)^{r-1}$ تلغي المعامل
> السابق، وتعطي قيم $r$ البالغة $k$ العاملَ $k$ ---

Verdict: **near-native**. Correct, unambiguous and correctly cased
(`الحدودَ`, `العاملَ`, `تركيبَ` all take the accusative), but the sentence
carries three parenthetical clauses in a row because the English does, and
Arabic prefers to break such a chain into two sentences. This is the one
place in the book where I would expect a native copy-editor to reach for a
full stop.

No sampled passage read as machine translation.

## Cross-book consistency pass — 2026-08-08

An orchestrator sweep across the finished Arabic editions found that Book 5
had drifted from the rest of the series on **five term families**. None of
them was a translation error inside Book 5 — every one of them was
*internally* consistent — but each broke the Book 3 → Book 4 → Book 5 seam
for a reader following the course, and two of them collided with a sense
that another subject already owns. This pass fixed all five. It is a
terminology pass only: no mathematics, no `\label`, no `\cref` target, no
solution key and no structural count changed, and the English tree was not
touched (`check_book5_golden.sh` still byte-identical).

Every site was read against the English source before it was touched;
nothing was search-and-replaced blind, and the deliberate keeps are listed
in full below.

### 1. interval = **فترة** (was مجال)

`arabic_style_card.md` §4 fixes *interval* = **فترة** and warns explicitly
against مجال, "which is already *field* / *range*". The warning is
load-bearing: Physics 2 uses مجال **221 times** for the physical field
(المجال المغناطيسي / الكهربائي), so مجال = interval in a maths book is a
cross-subject collision, not just an intra-series one.

| | Math 2 | Math 3 | Math 4 | Math 5 before | **Math 5 after** |
|---|---:|---:|---:|---:|---:|
| فترة | 123 | 137 | 0 | 0 | **225** |
| مجال | 13 | 43 | 110 | 278 | **52** |

**225 sites converted, 52 kept, 1 reworded.** فترة is feminine and مجال
masculine, so this could not be a substitution: 93 further edits fixed the
agreement that follows the noun — adjectives (`مجال متراص` →
`فترة متراصة`, `مفتوح` → `مفتوحة`, `جزئي` → `جزئية`, `ثنائي` → `ثنائية`,
`منزوع` → `منزوعة`), pronouns (`طوله` → `طولها`, `فيه` → `فيها`),
demonstratives (`ذلك المجال` → `تلك الفترة`, `هذا` → `هذه`), the
`ليكن`/`لتكن` opener, and verb agreement (`يحقق` → `تحقق`, `يوجد` →
`توجد`, `سيقع` → `ستقع`, `ينشطر` → `تنشطر`, `يتراكب` → `تتراكب`). Two
places were *left* masculine on purpose because the head of the phrase is
not the interval: `وجزءٌ … من فترة هو الفترة كلها` (the subject is
`جزء`), and `نصف فترة تكون فيه` (the head is `نصف`).

**The 52 sites where مجال was kept**, with the English that justifies each:

| Where | English | Sense |
|---|---|---|
| `ar/01-group-theory:410`, `sol/01-group-theory:556` | "leaves room for" / "leaves no room" | idiom, not a set at all |
| `ar/03-modules-pid:255` | "the shaded fundamental domain" | fundamental domain |
| `ar/06-general-topology:733`, `sol/06-general-topology:426` | "invariance of domain" | the theorem's name |
| `ar/11-product-measures:594`, `sol/11-product-measures:590` | "the sign on each range", "the range $0 \leq x \leq t$" | range |
| `ar/13-hilbert-spaces:305,306` | "injective with closed range", "the range is dense" | range of an operator |
| `ar/14-fourier-transform:282` | "Working ranges: $L^1$ …" | scope / range of validity |
| `ar/14-fourier-transform:316` | "in frequency, the same picture reads" | frequency **domain** |
| `ar/15-spectral-theory:276`, `sol/15-spectral-theory:59` | "finite-dimensional range", "range in $\operatorname{Vect}(…)$" | range |
| `sol/15-spectral-theory:96` | "at the top of the numerical range" | numerical range |
| `ar/16-holomorphic-functions` — 9 sites | "on a whole domain", "star-shaped domain", "subdomain", "bounded domains", "its (connected) domain", "(Dense range)", "the range of a nonconstant …", "a bounded domain" | complex-analysis domain / range |
| `sol/16-holomorphic-functions` — 5 sites | "the bounded domain", "On a bounded domain", "the range of a nonconstant", "range missing a disc" | domain / range |
| `ar/17-residues:11` | "star-shaped domains" | domain |
| `ar/18-conformal-geometry` — 6 sites, incl. `\index{مجال بسيط الترابط}` | "between two domains", "simply connected proper subdomain", "Two domains are …", "simply connected domain", "fractal-boundary domain", "multiply connected domains" | domain (the chapter's subject) |
| `sol/18-conformal-geometry:278` | "on any star-shaped subdomain" | domain |
| `ar/21-differential-forms` — 8 sites | "its domain", "a plane domain", "a compact domain with smooth boundary", "elementary domains", "compact domain", "is the domain a boundary?", "on its domain", "a compact domain $\Omega$" | domain |
| `sol/21-differential-forms` — 3 sites | "The domain $\R^3$", "domain passes through $0$", "compact domain $\Omega$" | domain |
| `sol/12-lp-spaces:513,581` | "uniformly for $n$ in any range", "on that range" | range |
| `sol/14-fourier-transform:306,350` | "transition zone widens", "its range consists of" | zone / range |
| `sol/19-differential-equations:527` | "on the compact $y$-range of $C_h$" | range |

One further site was **reworded rather than kept**:
`ar/14-fourier-transform:421` read `أساس فورييه للمجال $L^2(\intcc{-\pi}\pi)$`
where the English says "the Fourier basis of $L^2([-\pi,\pi])$" — the object
named is a *space*, not an interval and not a domain, so مجال was wrong in
both directions. It is now `للفضاء`.

### 2. vector = **متجهة**; شعاع kept only where it is not a vector

The settled series decision is *vector* = **متجهة** (Book 5 already uses the
متجه- family **166 times**). Book 5 had **18** occurrences of شعاع. Only
**7** of them meant a vector; all 7 were converted, and **11 were kept**.

| Converted (7) | English | New form |
|---|---|---|
| `ar/05-representations:731` | "the cross product on $\R^3$" | الجداء المتجهي |
| `ar/20-submanifolds:476` | "($A_uv = u\wedge v$, the cross product)" | الجداء المتجهي |
| `sol/20-submanifolds:379` | "with the scalar–vector rule" | السلّمي والمتجهي |
| `sol/20-submanifolds:384` | "the vector part is" | الجزء المتجهي |
| `sol/20-submanifolds:496` | "give the vector $(v_2w_3 - v_3w_2, …)$" | المتجهيَّ |
| `sol/20-submanifolds:500` | "the cross products add" | الجداءان المتجهيان |
| `sol/20-submanifolds:643` | "the vector part $\frac12(i-j+k)$" | الجزء المتجهي |

**Kept (11), because none of them is a vector:**

* **Ray** (4): `ar/09-measure-theory:270,274` ("every ray
  $A = (-\infty,c)$", "an interval minus a ray is an interval"),
  `sol/10-lebesgue-integral:6` ("a ray $(a,+\infty)$"),
  `ar/04-field-extensions-galois:619` ("similar triangles on two rays").
* **Radial** (7): `ar/21-differential-forms:842` ("a radial segment"),
  `ar/21-differential-forms:973` ("a radial homeomorphism"),
  `sol/21-differential-forms:54` ("the radial cousin of the angular form"),
  `sol/21-differential-forms:147` ("(radial) $\nu$"),
  `sol/21-differential-forms:401` ("the radial map from its barycenter"),
  `sol/18-conformal-geometry:614` ("radial integration"),
  `sol/20-submanifolds:12` ("the radial component").

**Radius of convergence and spectral radius were never at risk here**: this
edition already renders "radius of convergence" as **نصف قطر التقارب**
(`ar/16-holomorphic-functions:284`) and never used شعاع التقارب, so there
was nothing to protect. Recorded because the brief asked for it.

### 3. intermediate value vs mean value

A *sense* split, not a style preference. Book 5 was mixed. Note that three
of the sites were **line-wrapped** across `القيم` / `المتوسطة` and are
invisible to a single-line grep; the census below is computed on the
whitespace-normalised tree, which is why it finds 20 sites rather than 17.

| | before | **after** |
|---|---:|---:|
| `القيم الوسطى` (intermediate → the IVT) | 6 | **14** |
| `القيم المتوسطة` (mean value) | 14 | **6** |

**8 sites moved to الوسطى**, each against an English "intermediate value
theorem": `ar/16-holomorphic-functions:647`, `sol/13-hilbert-spaces:550`,
`sol/16-holomorphic-functions:259, 301, 320`,
`sol/19-differential-equations:425`, `sol/21-differential-forms:318`,
`sol/23-clt-gaussian:330`.

**6 sites kept المتوسطة**, each against an English "mean value inequality":
`ar/10-lebesgue-integral:322`, `ar/11-product-measures:274`,
`ar/19-differential-equations:25`, `ar/20-submanifolds:40`,
`sol/07-complete-spaces:133, 392`.

### 4. countable = **قابل / قابلة للعدّ** (was معدود)

Book 3 is where countability is introduced and it indexes the notion as
`\index{مجموعة قابلة للعدّ}`; Books 3 and 4 use the قابل-للعدّ form 91 and
82 times. Book 5 used **معدود 122 times and قابل للعدّ 0 times**, which
renamed a Book-3 definition out from under the reader.

| | Math 3 | Math 4 | Math 5 before | **Math 5 after** |
|---|---:|---:|---:|---:|
| قابل / قابلة للعدّ | 91 | 82 | 0 | **122** |
| معدود | 0 | 1 | 69* | **0** |

\* the orchestrator's 69 counted `معدودة` only; the full معدود- paradigm in
this tree was 122 (`معدود` 33, `معدودة` 36, `المعدودة` 30, `معدودًا` 15,
plus `المعدود`, `ومعدودًا`, `ومعدودة`, `والمعدودة`, `معدودتين`,
`معدودةً`, `المعدودية`).

All 122 are genuinely *countable* — checked, because Arabic معدود can also
mean "few, numbered", and it does not here. Agreement was carried through
the conversion: `معدودة` → `قابلة للعدّ`, `معدودًا` → `قابلًا للعدّ`,
`معدودتين` → `قابلتين للعدّ`, `المعدودية` → `القابلية للعدّ` (in
`sol/06-general-topology:239`, "uncountability"). The near-homograph
**معدوم** (*null*, of measure zero) is a different word and was untouched —
it appears in the same sentences as countability throughout ch. 9, so this
was checked explicitly.

### 5. norm = **معيار**, criterion = **محك** (the pair moved together)

Book 5 used **النظيم** for the norm and left معيار for the *criterion*.
Books 3 and 4 do the opposite — معيار = norm (79 and 151 sites), محك =
criterion — and that is what the style card specifies. Converting only one
half would have made the book worse, so the criterion pass ran **first**,
while the two senses were still distinguishable.

| | Math 3 | Math 5 before | **Math 5 after** |
|---|---:|---:|---:|
| معيار (norm) | 79 | 0 | **160** (+ 15 معايير, + 15 معياري "normed") |
| نظيم (norm) | 0 | 179 | **0** |
| محك (criterion) | 67 | 0 | **35** |
| معيار (criterion) | 0 | 35 | **0** |

Order of operations, and the three traps:

1. **Criterion first.** All 35 معيار-as-noun sites were read against the
   English and every one of them was a *criterion* — Eisenstein, Euler,
   Burnside, Morera, Lyapunov, Leibniz, Lebesgue's criterion, the
   `$\{0,1\}$`-criterion, the basis criterion, the series criterion,
   criteria (b)/(c)/(d) of the Parseval theorem. Not one was a norm, so the
   split was clean. `معايير عدم قابلية الاختزال` → `محكات …`;
   `\index{معيار أيزنشتاين}` → `\index{محك أيزنشتاين}`, with the visible
   `\emph{أيزنشتاين}` beside it unchanged.
2. **`معياري` / `المعيارية` = *standard, canonical* was left alone** — a
   third sense, neither norm nor criterion: `الآلة المعيارية` (the standard
   machine), `التوجيه المعياري` (the standard orientation), `انحراف
   معياري` (standard deviation), `غاوسية معيارية` (standard Gaussian). The
   conversion regex carries a negative lookahead on `ي` so none of them was
   touched. The resulting homonymy with `فضاء معياري` (*normed* space) is
   the same one Book 3 already lives with, deliberately.
3. **`تنظيم` / `التنظيم` = *regularization, normalization* is a different
   word that contains نظيم as a substring** (`\begin{theorem}[التنظيم]`,
   `\section{الالتفاف والتنظيم}`, `التعامد والتنظيم`). All 8 occurrences
   were protected by a negative lookbehind and are unchanged.

`\index{نظيم مؤثر}` → `\index{معيار مؤثر}` moved in step with its visible
`\emph{نظيم المؤثر}` → `\emph{معيار المؤثر}`, and with the three
`\omterm{def:b3:banach:operator}{بنظيم المؤثر}` **displays** — the `\omterm`
first arguments are untouched.

### Config change this pass required

`tools/term_config/book5_ar.py`: `NOT_A_TERM` listed **`"معيار"`** as a
word that heads a statement and is therefore never a defined term. After the
swap that is false — معيار is now the *norm*, and `\index{معيار مؤثر}` is a
genuine defined term — while محك is the word that heads a statement. The
entry is now `"محك"`, with a comment saying why. Without this edit the
operator-norm term would have been silently dropped from the harvest; with
it, the link layer regenerates to the same 293 linkable terms and 2 228
links as before, and `--check` is clean.

### What this pass did *not* change

0 mathematics edits, 0 `\label` edits, 0 `\cref`/`\ref` target edits, 0
`\begin{solution}{key}` edits, 0 `\omterm` first-argument edits, 0 English
files. The structural census is still identical to English (722 labels, 299
solution keys, 19-type environment census at zero mismatches), the build is
still 377 pages at 0/0/0, and `check_book5_golden.sh` still reports the
frozen English path byte-identical.

## Why not 100

1. **The link layer is half of English's** (dimension score 90). Every
   removed link was wrong-sense, so the *precision* went up, but a reader
   of the Arabic edition genuinely gets fewer clickable definitions than a
   reader of the English one. Closing the gap needs per-occurrence
   disambiguation (a `PROTECT` regex per collocation, `الدرجة الأولى`,
   `درجة كثير الحدود`, …), which is a second curation pass measured in
   hours, not minutes, and carries its own risk of protecting a legitimate
   link. I chose precision over volume; that is a defensible call, not a
   free one.
2. **Two transliterated head-terms**: `هولومورفية` and `مرومورفية`. They
   are the standard Arabic forms and every alternative (`تامة التحليل`,
   `تحليلية بالكامل`) collides with `تام` = complete, which the book already
   uses heavily. Standard, but still not a native Arabic root.
3. **English typographic rhythm survives in the `method` boxes and in the
   weekend-problem part headers** (passage 3). This is a series-wide design
   choice — every language edition keeps the same skeleton — but it is a
   place where Arabic could read better if the series allowed it to
   diverge.
4. **Three long proofs keep English's parenthetical density** (passage 5:
   the Poincaré lemma computation, Dixon's proof of the global Cauchy
   theorem in ch. 17, and the Lindeberg telescoping in ch. 23). They are
   correct and unambiguous; they are also the three places a native
   copy-editor would repunctuate.
5. **`\index` sort keys were chosen for readability, not for a defined
   Arabic collation.** They are 100 % Arabic in display (0 Latin letters
   outside math across 308 entries) and use `sort@display` where the
   display carries mathematics, but the sort halves I wrote (`جبر سيغما@…`)
   assume `makeindex`'s byte order rather than an Arabic alphabetical
   convention. The index is usable; it is not linguistically sorted.

## Gate results (final state)

Re-run in full after the 2026-08-08 consistency pass; every number below is
from that re-run, and every one of them is unchanged from before the pass.

```
bash tools/check_translation.sh bachelor-3 ar
    arabic prose gate: OK (46 files)          TRANSLATION GATE: PASSED

python3 tools/check_arabic_prose.py parts/bachelor-3/ar parts/bachelor-3/solutions/ar
    arabic prose gate: OK (46 files)
    english 0 · translit 0 · punct 0 · digits 0 · math-space 0
    bidi-ctrl 0 · presform 0 · tatweel 0 · split-number 0

python3 tools/link_defined_terms.py --book 5 --lang ar --unwrap --apply   → links removed: 2228
python3 tools/link_defined_terms.py --book 5 --lang ar --apply            → links inserted: 2228 across 46 files
python3 tools/link_defined_terms.py --book 5 --lang ar --check            → CHECK: every file matches what the config generates

sh tools/check_book5_golden.sh
    CHECK: every file matches what the config generates      (English path untouched)

latexmk one_math_book_5_university_year_3_ar.tex
    0 errors (^!)   0 undefined references   0 overfull boxes   377 pages
```

Structural diffs against English, computed on the concatenated trees:

| Quantity | English | Arabic |
|---|---:|---:|
| `\label` (set **and** order) | 722 | 722 — identical |
| `\begin{solution}{key}` (set **and** order) | 299 | 299 — identical |
| environment census, 19 types | — | 0 mismatches |
| `\emph{` | 1 404 | 1 404 |
| `\item` | 675 | 675 |
| display openers `\[` | 1 039 | 1 039 |
| `\index` entries | 307 | 308 (0 with Latin outside math) |
| `\text{…}`-family arguments | 917 | 923 (0 carrying English) |
| `\omterm` links / targets | 4 326 / 130 | 2 228 / 123 |
| U+0640 tatweel · Arabic-Indic digits · bidi controls | — | 0 · 0 · 0 |

## Requests to the orchestrator

None blocking. Two observations, for the record:

1. **`tools/check_arabic_prose.py` earns its keep.** Its `tatweel` and
   `math-space` classes caught genuine errors on almost every file — the
   tatweel class in particular, because the natural Arabic way to attach a
   particle to a symbol (`بـ$X$`, `لـ$f$`) is exactly what the gate forbids,
   and the fix (insert a noun: `بالدالة $f$`, `للمقدار $X$`) is also the
   better prose. Worth keeping as-is.
2. **Two English-side artefacts leaked into the Arabic through masked
   spans** and had to be normalised in the span map to satisfy the
   `math-space` class: `$ (x,y)\mapsto x -\ny$` in
   `parts/bachelor-3/11-product-measures.tex` and
   `$f_{n_k} \to f_{n_1} + \sum(\cdots) $` in
   `parts/bachelor-3/solutions/12-lp-spaces.tex` (leading/trailing space
   inside inline math), plus `$B(a, 1-a) = \Gamma(a)\Gamma(1-a)/\Gamma(1) $`
   in `parts/bachelor-3/solutions/17-residues.tex`. The Arabic edition
   carries them without the stray space; the English originals still have
   it. Harmless typographically in English, but if the gate is ever pointed
   at English these are the three it would flag.
