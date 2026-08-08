# Book 1 — Arabic (`ar`) — translation self-score

| Field | Value |
|---|---|
| **Book** | One Math Book 1 (Primary / Middle, grades 1–9) |
| **Entry** | `one_math_book_1_primary_middle_school_ar.tex` |
| **Language** | Arabic (`ar`), Modern Standard Arabic per `arabic_style_card.md` |
| **Quality bar** | `native academic` — an Arabic-medium teacher should hand it to the class without apologising for it |
| **Scope** | 71 chapters + 71 solutions = **142 files** under `parts/grade-{1..9}/ar/` and `parts/grade-{1..9}/solutions/ar/` |
| **Kind of pass** | **translation from the English canon**, chapter by chapter, as a line-range patch on top of the English source (§3). No machine translation was used or post-edited at any point. |
| **Delivered** | **142 of 142 files — the book is complete.** |
| **Term config** | `tools/term_config/book1_ar.py` (curated; extended for grades 6–9 in §5) |
| **Overall score** | **96 / 100** |
| **Date** | 2026-08-08 (revision 2 — completion) |

> **Revision note (2026-08-08, second session).** Revision 1 delivered 76 files
> (grades 1–5 and grade 6 chapters 1–2). This revision translated the remaining
> **66**: grade 6 chapters 3–8, and all of grades 7, 8 and 9, chapters and
> solutions. The link layer was then regenerated over the **whole** book and the
> term config extended for the grade 6–9 vocabulary (§5). All nine translation
> gates pass, the Arabic prose gate is zero in all nine classes on all 142
> files, the book builds with 0 errors, 0 undefined references and 0 overfull
> boxes. **The edition is shippable.**

---

## 1. Dimension scores (whole book, 142 files)

| Dimension | Weight | Score | Comment |
|---|---:|---:|---|
| Register (ages 6–15, Arabic schoolbook voice) | 25 | 24 | The register gradient holds across nine years: grades 1–3 speak to the pupil in short imperative sentences (`عُدّ`, `اُرسم`, `قارن`), grades 6–7 move to full textbook prose (`اِستنتج`, `برّر`, `تحقّق من`), and grades 8–9 write like a middle-school course — `وبما أنّ … فإنّ`, `على سبيل الخُلف`, `ومن ثمّ`, `فلا قائمة منتهية تسع كل الأعداد الأولية`. Weekend problems keep the English's narrative voice (Archimedes' tomb, the Chevalier de Méré, Heron's recipe) without turning into lecture calque. Loss: the primary grades are only lightly vocalised (§8). |
| Terminology (standard technical Arabic) | 20 | 19 | §4 lists the whole grade 1–9 vocabulary. Grades 6–9 added ~60 terms (arithmetic, roots, algebra, functions, Thales, trigonometry, solids, statistics) and every one follows the style card's Maghrebi MSA: `أصمّ` for irrational, `ناطق` for rational, `مبرهنة` for theorem, `متراجحة`, `الجداء`, `الوسيط`, `المدى`. |
| Freedom from MT artefacts | 20 | 20 | `check_arabic_prose.py` is **0 in all nine classes on all 142 files**: no residual English in prose, TikZ node text, `\text{}` inside math, chapter/section titles, environment optional titles or index keys; no transliterated function words; no Latin `,;?` after Arabic; no Arabic-Indic digits; no bidi controls, presentation forms or tatweel. The text was never machine-translated, so there is nothing to post-edit. |
| Structural fidelity | 15 | 15 | `check_translation.sh` **PASSED for all nine years**: identical label sets and order, `exo:`/`pb:` ↔ `\begin{solution}{}` parity, env/figure census, `\end{…>` typo class, drafty `...`, duplicate labels, TeX accent escapes. On top of that the applier enforced six per-file invariants (§3), including an ordered math-span census that no repository gate performs. |
| Mathematical correctness | 10 | 10 | The mathematics is byte-identical to English by construction (§3): every display, every `\foreach` list, every `xtick=`, every number is the English bytes unless a range was deliberately replaced, and the applier refuses a replacement whose math-span sequence differs. |
| Link layer (`\omterm`) | 10 | 9 | Config extended and curated; `--check` green and idempotent; **2 975 links across 124 files**; whole-book target parity **78 / 79**; per-year parity in §5. One English target is deliberately unreachable (`def:g3:division:half`). |
| Build | — | pass | 0 errors, 0 undefined references, **0 overfull boxes**, 420 pages. |

**Weighted total: 96 / 100.** Above the ship bar of `translation_instruction.md`
(complete book at ≥ 95).

---

## 2. Gate results

| Gate | Result |
|---|---|
| `bash tools/check_translation.sh grade-N ar`, N = 1…9 | **PASSED**, all nine |
| `python3 tools/check_arabic_prose.py` on all 142 files | **OK (0 issues)** in all nine classes |
| `python3 tools/link_defined_terms.py --book 1 --lang ar --check` | **green** — "every file matches what the config generates" |
| `latexmk one_math_book_1_primary_middle_school_ar.tex` | **exit 0** |
| `grep -ac '^!'` on the log | **0** errors |
| `grep -aci 'undefined'` | **0** undefined references |
| `grep -ac 'Overfull'` | **0** |
| Output | `build/one_math_book_1_primary_middle_school_ar.pdf`, **420 pages** |
| `\omterm` target parity vs English, whole book | **78 / 79** |

### Arabic prose gate

| Class | first pass (76 files) | this revision, all 142 |
|---|---:|---:|
| `english` | 14 → 0 | **0** |
| `tatweel` | 15 → 0 | **0** |
| `punct` / `digits` / `math-space` | 0 | **0** |
| `translit` / `bidi-ctrl` / `presform` / `split-number` | 0 | **0** |

The two classes that fire in Arabic are unchanged from revision 1 and fired
again in grades 6–9 before being fixed: **tatweel** (a one-letter proclitic
before a math span, a `\cref` or an `\emph` — `بـ$5$`, `بـ\cref{…}`,
`فـ\emph{…}`) and **english** (an environment optional title, or a stray
connective, left on a line that no replacement range covered). Both are cheap
to fix and impossible to see without the gate.

### The two overfull boxes, and how they were removed

The first build of the complete book had exactly two, both in **Arabic** files
written in this revision, and both instances of the *same* Arabic-specific
trap: **a long horizontal run that bidi typesetting cannot break.**

1. `parts/grade-9/solutions/ar/02`, the divisors of $60$ written as one math
   group `$1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60$` — twelve numbers, no
   breakpoints, inside Arabic that is narrower than the English. Fixed the way
   revision 1 fixed the same box in grade 5: one math group per number with an
   Arabic comma between them (`$1$، $2$، $3$، …`). This is the one place in the
   tree where the Arabic deliberately departs from the English math grouping.
2. `parts/grade-6/solutions/ar/04`, the list of clock times when the hands of a
   clock coincide (`1:05 و2:11 و3:16 …` — ten of them). Latin digits inside
   Arabic form one bidi run, and `و` glues to the next token, so the whole list
   is a single unbreakable box. Fixed by cutting the list into three short
   clauses (`… و5:27؛ ثم عند 6:33 و7:38؛ ثم عند …`), which restores the
   breakpoints without changing a single number.

**Generalisation worth carrying to Books 2–5: in Arabic, any run of
comma-separated numerals — inside `$…$` or inside prose — is one unbreakable
box. Break it yourself, before the box does.**

---

## 3. Method, and the tooling the next agent should reuse

The pass is a **line-range patch applied on top of the English canon**. For
every chapter a patch names the English source and gives the Arabic replacement
for each line range:

```text
### parts/grade-9/ar/02-arithmetic-gcd.tex <<< parts/grade-9/02-arithmetic-gcd.tex
@@ 1
\chapter{الحساب: القواسم والأعداد الأولية}\label{ch:g9:arith}
@@ 3-8
يدرس الحساب الأعداد الصحيحة وكيف يقسم بعضها بعضًا. …
```

Every English line **not** named is copied byte-identically, so labels, `\cref`
targets, `\begin{solution}{key}`, `\foreach` lists, `xtick=` and every math
display are physically the same bytes as English and cannot drift.

The applier (`ar_apply.py`, ~250 lines, in the session scratchpad) **refuses to
write a file** unless every structural marker survives. Errors it caught in
this revision's 66 files:

| Invariant | Errors it caught in this revision |
|---|---:|
| ordered `\begin{env}` / `\end{env}` and `\label{…}` sequence | 8 — a range that started or ended inside a display or swallowed an `\end{enumerate}` |
| ordered `\begin{solution}{key}` sequence | 0 |
| **ordered math-span sequence, after blanking `\text{…}`** | **11** — a number or a symbol spelled out in Arabic words where English had a math span |
| ordered tikz/axis bodies, after blanking node text and axis labels | 0 (two chapters used the `!draw` escape hatch deliberately) |
| brace-balance drift relative to the English file | 0 |
| character gates (tatweel, Arabic-Indic digits, presentation forms, bidi controls, Latin `,;?` after Arabic) | 12 tatweel, caught before the file was ever written |

The math-span check remains the single most valuable invariant. Arabic *wants*
to absorb small numbers into words — `رقم $0$ واحد` vs `صفر واحد`,
`ضلع القائمة$^2$` vs `مربع ضلع القائمة` — and every such slip silently changes
the mathematics of the page while passing every prose gate.

Two changes were made to the applier this session, both worth keeping:

* the brace check became **relative to the English file** (`EN opens − EN
  closes == AR opens − AR closes`). The absolute check produced false alarms on
  any chapter containing `\%`, because the comment-stripping regex reads `\%`
  as the start of a comment.
* the character gates listed above were moved **into** the applier, so a
  tatweel or an Arabic-Indic digit is rejected before the file is written
  rather than after.

---

## 4. Terminology decisions worth recording

Revision 1's decisions (§4 of that revision, preserved): **`الجداء`** for
*product*, **`النقطة العشرية`** for the decimal point, **`التصميم`** for the
*net* of a solid, `الكوس` / `الفرجار` / `المسطرة` for the instruments,
`الاحتفاظ` / `الاستلاف` for carry and borrow, `الفئات` for the three-digit
classes, `مستقيم الأعداد` for the number line, localised child names, ASCII
digits everywhere, no curriculum or country named as a source.

The series-wide repairs the orchestrator settled mid-session are applied:
**continuity = `الاتصال` / `متصل`** (does not occur in Book 1) and
**interval = `فترة`, never `مجال`**. Book 1 had exactly one violation,
`parts/grade-6/ar/03` ("cut each unit interval"), now `كل فترة واحدية`;
`parts/grade-7/ar/06` was already `الفترات`. The only remaining `مجال` in
grades 1–9 was a *domain of validity* in grade-9/05, rewritten to `نطاق` so the
word does not appear in the book at all.

New in grades 6–9:

* **Arithmetic.** `قاسم` divisor, `مضاعف` multiple, `قابل للقسمة` divisible,
  `عدد أولي` prime, `التفكيك إلى عوامل أولية` prime factorization,
  `القاسم المشترك الأكبر` GCD, `أوليان فيما بينهما` coprime,
  `خوارزمية إقليدس`, `الباقي` remainder, `خارج القسمة` quotient.
* **Numbers.** `أصمّ` irrational (and `الصمم` for irrationality), `ناطق`
  rational, `الجذر التربيعي` square root, `الأُسّ` exponent / `الأساس` base,
  `الترميز العلمي` scientific notation, `مربّع تامّ` perfect square.
* **Algebra.** `النشر` expanding, `التفكيك` factoring, `المتطابقات الثلاث` the
  three identities, `المعادلة`, `المتباينة`, `قاعدة الجداء المعدوم` the
  zero-product rule, `العامل المشترك`.
* **Functions.** `الدالة الخطية` linear, `الدالة التآلفية` affine, `الميل`
  slope, `الترتيب عند المبدأ` the *y*-intercept, `التمثيل البياني` graph,
  `معامل` coefficient.
* **Geometry.** `مبرهنة طاليس`, `وضعية الفراشة` the butterfly configuration,
  `معامل التحجيم` scale factor, `المقطع` cross-section, `الموشور` prism,
  `الأسطوانة` cylinder, `المخروط` cone, `الهرم` pyramid, `الكرة` sphere,
  `الوتر` hypotenuse, `ضلع القائمة` leg, `المجاور` / `المقابل`,
  `جيب التمام` / `الجيب` / `الظلّ`, `خطّ مقارب` asymptote.
* **Statistics and probability.** `المتوسّط` mean, `الوسيط` median, `المدى`
  range, `الاحتمال`, `المخرج` outcome, `الحدث` event, `الحدث المضادّ` the
  complement, `شجرة الاحتمالات`, `التواتر` frequency.

Two judgement calls worth flagging for Books 2–5:

* **`المتوسّط` (with šadda) for the statistical mean, `المتوسط` for the median
  of a triangle.** Arabic writes both with the same consonantal skeleton. The
  book keeps them apart by šadda *and* by the link layer (§5), but a future
  editor normalising šadda would merge two different notions.
* **`السلّم` is both *scale* and *ladder*.** Grade 9's trigonometry chapter
  leans a ladder against a wall two pages after grade 7 defines the map scale.
  Handled with `EXTRA_PROTECT` (§5); a Book 2 agent meeting an inclined plane
  should expect the same collision.

---

## 5. The link layer

Regenerated over the whole book after the last file landed:

```sh
python3 tools/link_defined_terms.py --book 1 --lang ar --unwrap --apply
python3 tools/link_defined_terms.py --book 1 --lang ar --apply
python3 tools/link_defined_terms.py --book 1 --lang ar --check   # green
```

**2 975 links across 124 files** (g1 7, g2 23, g3 62, g4 136, g5 187, g6 510,
g7 588, g8 719, g9 743). Target parity against English:

| Year | English targets | matched | missing | extra |
|---|---:|---:|---:|---:|
| grade-1 | 3 | 3 | 0 | 0 |
| grade-2 | 5 | 4 | 1 | 0 |
| grade-3 | 10 | 8 | 2 | 0 |
| grade-4 | 18 | 16 | 2 | 0 |
| grade-5 | 20 | 17 | 3 | 2 |
| grade-6 | 38 | 33 | 5 | 1 |
| grade-7 | 35 | 32 | 3 | 2 |
| grade-8 | 46 | 42 | 4 | 0 |
| grade-9 | 50 | 48 | 2 | 0 |
| **whole book (union)** | **79** | **78** | **1** | **0** |

The one target the Arabic never reaches is `def:g3:division:half` (`نصف` /
`ربع`), hard-dropped in revision 1 because `نصف ساعة`, `نصف الطريق`,
`نصف المستطيل` would turn every second page blue. The per-year "missing" and
"extra" rows are the spiral curriculum re-pointing a term at a *different but
correct* definition: `def:g4:numbers:round` vs `def:g6:decimals:rounding` for
rounding, `def:g4:geometry:def` vs `def:g6:lines:perp` for perpendicular and
parallel, `def:g5:solids:volume` vs `def:g6:measure:volume` for volume. That is
what `AMBIG_POLICY = "nearest-preceding"` is for, and English's own config makes
the same choice one year earlier.

### What the config needed for grades 6–9

Three classes of edit, all in `tools/term_config/book1_ar.py`:

1. **`DERIVED`, 12 new entries.** Arabic pluralises by internal vowel change and
   `lang_ar.py` sets `DERIVE = False` on purpose, so every plural a chapter
   actually uses must be declared: `الأُسّ → الأُسُس / أُسًّا / أُسّيه`,
   `المخروط → المخاريط`, `الموشور → المواشير`, `القطعة → القطع`,
   `المستقيم → المستقيمات / مستقيمان`, `الدالة الخطية → الدوال الخطية`,
   `العدد الأولي → الأعداد الأولية`, `احتمال → اِحتمال / الاِحتمالات`,
   `قابل للقسمة → قابلية القسمة`, and so on. This alone recovered four English
   targets grade 8 was missing.
2. **`EXTRA`, to re-point three harvests at the definition English uses.** The
   harvest registers a term where its `\emph` display *first* appears, which in
   Arabic was sometimes an example or a theorem rather than the definition:
   `الباقي` was registering on grade 6's Euclidean-division theorem (English
   links remainder to grade 3), `فرق` and `خارج قسمة` on a grade-6 vocabulary
   example (English links them to grade 1 and grade 3), and `السلّم` on a
   grade-6 weekend problem (English defines scale in grade 7). Pointing them at
   the English target removed four whole-book target divergences; the grade-6
   uses of `السلّم` then fall away by themselves, because a link never precedes
   its own definition.
3. **`STOP` + `SOFT` + `EXTRA_PROTECT`, for the two homographs of §4.**
   `متوسط` is stoplisted *and* soft, so it links only inside grade-8's
   midpoints chapter, where every occurrence really is the triangle's median —
   the 27 "average" occurrences of grades 8–9 are no longer linked to it.
   `سلّم` as a ladder is protected by four regexes (`سلّم\s+طوله`,
   `بين\s+السلّم\s+والأرض`, `مسألة\s+السلّم`, `سلّم،\s+لا\s+درج`).
   **`EXTRA_PROTECT` patterns must use `\s+`, never a literal space** — the
   wrapper normalises whitespace before matching.

Revision 1's structural lesson still holds and is the thing to read first:
**the harvest registers the `\emph` display and the `\index` key as two
separate terms**, and in Arabic they differ by the article, so every stoplisted
word is listed bare *and* definite (`STOP |= {"ال" + w for w in STOP}`).

---

## 6. Sampled passages, judged

1. **`parts/grade-7/ar/01`, opening** — *ما قيمة $3 + 4 \times 5$؟ إن حسبت من
   اليسار إلى اليمين وجدت $35$؛ وإن ضربت أولًا وجدت $23$. والرياضيات تحتاج
   جوابًا واحدًا لا غير، فكانت للحسابات قواعد سير --- هي الأولويات.* —
   **native**. `قواعد سير` keeps the English's traffic-rules image in two words,
   and `لا غير` is how an Arabic textbook says *one answer, not two*.
2. **`parts/grade-8/ar/03`, powers of ten** — *ومنه فالسنة الضوئية نحو … أي عشرة
   ملايين مليار متر. فقوى العشرة تجعل الحسابات …* — **native academic**.
   `عشرة ملايين مليار` is the ordinary Arabic reading of $10^{16}$; a translator
   working from the words would have written a calque of *ten million billion*.
3. **`parts/grade-9/ar/02`, opening** — *يدرس الحساب الأعداد الصحيحة وكيف يقسم
   بعضها بعضًا. وأبطاله الرئيسيون هم الأعداد الأولية، اللبنات التي يُبنى منها كل
   عدد صحيح بالضرب.* — **native academic**. `يقسم بعضها بعضًا` is the standard
   reciprocal construction; `اللبنات` carries *building blocks* exactly.
4. **`parts/grade-9/solutions/ar/03`, the irrationality proof** — *كون $a$ و $b$
   زوجيين معناه أنّهما قابلان للقسمة على $2$ --- لكنّ $\frac ab$ كان مختزلًا إلى
   أبسط صورة، فلا يشتركان في أيّ قاسم. وهذا تناقض.* — **native academic**. This
   is how the proof is written in an Arabic school textbook: `كون … معناه`,
   `فلا يشتركان`, `وهذا تناقض`.
5. **`parts/grade-9/ar/05`, chained percentages** — *وتتابع التغيّرات يضرب
   العوامل بعضها في بعض. فزيادة $20\%$ يتبعها نقصان $20\%$ تعطي … أي نقصانًا
   إجماليًّا قدره $4\%$، لا عودةً إلى البداية!* — **native**. `لا عودةً إلى
   البداية` reproduces the English's punchline rhythm without its syntax.
6. **`parts/grade-9/ar/08`, Archimedes' tomb** — *برهن أرخميدس على مبرهنات
   كثيرة، لكنّ واحدة منها أفخرته حتى طلب أن يُنقش شكلها على قبره: كرة محشورة في
   أضيق أسطوانة لها.* — **near-native**. Correct and idiomatic, but `أفخرته`
   is a slightly literary causative; an editor might prefer `اعتزّ بها حتى`.

No sampled passage reads as post-edited MT — there was no MT.

---

## 7. Gate traps for the next Arabic agent

1. **Tatweel is the trap of this language.** Any proclitic before a math span, a
   `\cref` or an `\emph` (`بـ$5$`, `بـ\cref{…}`, `فـ\emph{…}`) is written with
   U+0640 and is gated. Name the object instead: `بمقدار $5$`,
   `حسب \cref{…}`, `فالجداء …`.
2. **A number spelled out in Arabic words is a deleted math span.** `صفران` for
   `$0$, $0$`, `مربع ضلع القائمة` for `Leg$^2$`. Only an ordered math-span
   census sees it.
3. **A replaced range must not start or end inside a display.** Eight rejections
   this revision were exactly that.
4. **Environment optional titles and one-word connective lines** (`so`, `then`)
   are easy to leave English when only the body range is replaced. The `english`
   gate is the only thing that sees them.
5. **`\text{}` inside math is visible text.** `\text{cyl}`, `\text{area}`,
   `\text{if }` all fire the `english` gate; they must be translated even though
   they sit inside `$…$`.
6. **A comma-separated list of numerals is an unbreakable box** — in math or in
   prose (§2). Break it before the typesetter does.
7. **Arabic homographs collide across chapters**: `سلّم` scale/ladder,
   `المتوسط` mean/median, `الباقي` remainder/the rest, `مجال` interval/field.
   Expect one wrong-sense link family per collision and fix it in the config,
   not in the prose.
8. **`\to`, `\pm`, `0/5` and `$^2$` are math spans**; `م$^2$`, `سم$^3$` and
   `كلم$^2$` must keep the exponent outside the Arabic unit name.
9. **Left/right on the page is a bidi trap.** Prefer `في طرف` … `في الطرف
   الآخر` over "left-hand side"/"right-hand side" when the equation is typeset
   LTR inside RTL prose; keep `اليسار`/`اليمين` only where a figure really has a
   left and a right.

---

## 8. Why not 100

* **Register 24/25.** Grades 1–3 are only *lightly vocalised* (harakat on
  imperatives and where a word would otherwise be ambiguous). A printed Arabic
  textbook for six-year-olds is usually **fully** vocalised. Full tashkīl was
  rejected deliberately: it would have to be consistent across 142 files and it
  breaks the term linker, which matches literal strings — a vocalised
  `المُضاعَف` would not match the term `مضاعف`. Recorded as request 1 in §10.
* **Terminology 19/20.** Several choices are defensible but not the only
  defensible ones: `الجداء` over `حاصل الضرب`, `التصميم` over `الشبكة` for a
  net, `أصمّ` over `غير ناطق` for irrational, `الترتيب عند المبدأ` over
  `الجزء الثابت` for the intercept. All are documented so Books 2–5 can follow
  or overrule as a series.
* **Link layer 9/10.** `def:g3:division:half` is unreachable without
  over-linking `نصف`; several years point rounding, parallelism and volume at
  the grade-6 re-definition instead of the grade-4/5 one (§5) — correct
  behaviour under `nearest-preceding`, but not byte-parity with English.
* Nothing else is outstanding: all gates are zero, the build is clean, and no
  passage reads as machine translation.

---

## 9. State

| Files | State |
|---|---|
| `parts/grade-{1..9}/ar/*.tex` (71) | **delivered**, gates green |
| `parts/grade-{1..9}/solutions/ar/*.tex` (71) | **delivered**, gates green |
| `tools/term_config/book1_ar.py` | extended for grades 6–9 (§5) |
| `build/one_math_book_1_primary_middle_school_ar.pdf` | 420 pages, clean log |

---

## 10. Requests to the orchestrator

1. **Full vocalisation (tashkīl) for grades 1–3 — decide as a series.** Carried
   over from revision 1 and still open. Full vocalisation is what a real Arabic
   primary textbook looks like, but it must be one deliberate pass over the
   whole series, it must come **after** the link layer is generated, and
   `tools/termlink/morphology.py` plus `check_arabic_prose.py` would need to
   normalise harakat away before matching. If the answer is "no", please record
   it in `arabic_style_card.md` §2 so the next agents do not reopen it.
2. **`check_arabic_prose.py`: add a tatweel *hint*.** The class is correct and
   caught 27 real defects across the two revisions, but the message ("kashida
   padding") describes a different failure. A one-line hint — "a proclitic
   before math/`\cref`; name the object instead" — would save the next agent a
   lookup.
3. **`arabic_style_card.md` §4 — please append the two homograph rulings this
   book had to make**, because Books 2–5 will meet them: **statistical mean =
   `المتوسّط` (with šadda), median of a triangle = `المتوسط`**, and **`السلّم`
   means both *scale* and *ladder*, so a ladder in a geometry chapter needs an
   `EXTRA_PROTECT` entry**.
4. **`translation_instruction.md` — one generic line worth adding**: *in
   Arabic, any comma-separated run of numerals (inside `$…$` or in prose) is a
   single unbreakable box; break it yourself.* Two of the three overfull boxes
   this edition ever produced were exactly that, in two different books' worth
   of chapters (§2).
5. **`arabic_style_card.md` §6** — worth recording that the harvest registers
   `\emph{display}` and `\index{key}` as two separate terms, and that in Arabic
   they differ by the article, so every stoplisted word must be listed bare
   *and* definite (§5). It is not obvious and it cost 300 wrong links in
   revision 1.
6. **Arabic web edition.** `tools/build_html_book.sh` still defaults to
   `LANGS=en,fr,nl`. Book 1 ar is now complete, so `ar` can be added whenever
   the reader is ready for an RTL edition.

**No git commit was created; the working tree is left for review.**
