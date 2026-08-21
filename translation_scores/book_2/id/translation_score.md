# Book 2 — Indonesian (`id`) — translation self-score

| Field | Value |
|---|---|
| **Book** | One Math Book 2 (High School, Kelas 10–12) |
| **Entry** | `one_math_book_2_high_school_id.tex` |
| **Language** | Indonesian (`id`), EYD orthography per `indonesian_style_card.md` |
| **Register row** | *Math 2, Kelas 10–12: school textbook prose* — the voice of an Indonesian SMA textbook: full sentences, `-lah` imperatives in exercises, no lecture calque |
| **Quality bar** | `native` — an Indonesian-medium SMA teacher should hand it to the class without apologising for it |
| **Scope** | 35 chapters + 35 solutions = **70 files** under `parts/grade-{10,11,12}/id/` and `parts/grade-{10,11,12}/solutions/id/` |
| **Kind of pass** | **translation from the English canon**, chapter by chapter, as a line-range patch on top of the English source (§3). No machine translation was used or post-edited at any point. |
| **Delivered** | **70 of 70 files — the edition is complete.** |
| **Term config** | `tools/term_config/book2_id.py` (curated, not a translation of `book2_en.py`) |
| **Overall score** | **97 / 100** |
| **Date** | 2026-08-20 (revision 2 — the ℕ ruling applied) |

> **Revision note (2026-08-20).** Revision 1 scored 96 and left one open
> question: the style card said `bilangan asli` for `\N`, but the canon's `\N`
> contains `0`. The orchestrator ruled for **`bilangan cacah`** (§4). The three
> places in grades 10–12 that render the canon's ℕ were changed, the index key
> follows the visible term, the link layer was regenerated (same 3 678 links,
> same targets), all three translation gates pass and the book still builds
> 0 / 0 / 0 at 346 pages.

---

## 1. Dimension scores (whole book, 70 files)

Weighting follows the brief: register, terminology and MT-artefact freedom
carry more than structure, because structure is machine-checked and prose is
not.

| Dimension | Weight | Score | Comment |
|---|---:|---:|---|
| Register (Kelas 10–12 school textbook prose) | 25 | 24 | One voice across three years. Course text is declarative and unhurried (`Misalkan $f$ kontinu dan positif pada …`, `Karena itu setiap bilangan kompleks tak nol punya balikan`); exercises use the `-lah` imperative that Indonesian textbooks use for instructions (`Hitunglah`, `Tunjukkan bahwa`, `Simpulkan`, `Periksalah`, `Selesaikan`); weekend problems keep the English narrative voice without turning into lecture calque (`Bandar selalu menang`, `Archimedes melawan mesin`, `Hardy membanggakan diri pada tahun 1940 bahwa teori bilangan “tak ternoda” oleh penerapan`). Discourse connectives are Indonesian, not glossed English: `karena itu`, `sehingga`, `sebaliknya`, `khususnya`, `secara lebih umum`, `jika dan hanya jika`. Loss: a handful of the longest weekend-problem sentences still carry the English clause order (§8). |
| Terminology (standard Indonesian school mathematics) | 20 | 20 | §4 records the whole three-year vocabulary. It follows the Indonesian school standard, not a purist re-invention: `distribusi binomial`, `nilai harapan`, `ragam`, `simpangan baku`, `peubah acak`, `turunan`, `primitif`, `antiturunan`, `pengintegralan parsial`, `bilangan kompleks`, `konjugat`, `modulus`, `argumen`, `akar satuan`, `matriks ketetanggaan`, `permutasi kacau`, `bidang empat`, `garis bersilangan`. The one open question — what to call the canon's `\N` — was ruled on and applied: **`bilangan cacah`** (§4). |
| Freedom from MT artefacts | 20 | 20 | `check_indonesian_prose.py` is **0 in all six classes on all 70 files**: no residual English word in visible text, no untranslated chunk, no space inside inline math, no space in reduplication, no detached enclitic, no split number. Indonesian is written in the same alphabet as the source, so this gate is the only thing standing between a half-translated file and a green build — it was run after every single patch. Every TikZ `node {…}`, every `xlabel=`/`ylabel=`/`title=`, every `\text{…}` inside math, every environment optional title and every `\index{}` key is Indonesian. |
| Structural fidelity | 15 | 15 | `check_translation.sh` **PASSED for all three years**: identical label sets and order, `exo:`/`pb:` ↔ `\begin{solution}{}` parity, environment and figure census, `\end{…>` typo class, drafty `...`, duplicate labels, UTF-8 with no TeX accent escapes. On top of that the applier enforced eight per-file invariants (§3), including an ordered math-span census that no repository gate performs. |
| Mathematical correctness | 10 | 10 | The mathematics is byte-identical to English by construction (§3): every display, every `\addplot` coordinate list, every `xtick=`, every numeral is the English bytes unless a line range was deliberately replaced, and the applier refuses a replacement whose ordered math-span sequence differs by one span. Digits stay ASCII and the decimal separator stays a **point**, in prose and in math, everywhere. |
| Link layer (`\omterm`) | 10 | 9 | Config curated from scratch; `--check` green and idempotent; **3 678 links across 70 files**; whole-book target parity **123 / 123 English targets reached, one extra** (§5). Per-year parity differences are all right-sense and explained. |
| Build | — | pass | 0 errors, 0 undefined references, **0 overfull boxes**, **346 pages**. |

**Weighted total: 97 / 100.** Above the ship bar (complete edition at ≥ 95).

---

## 2. Gate results

```
bash tools/check_translation.sh grade-10 id     TRANSLATION GATE: PASSED
bash tools/check_translation.sh grade-11 id     TRANSLATION GATE: PASSED
bash tools/check_translation.sh grade-12 id     TRANSLATION GATE: PASSED

python3 tools/check_indonesian_prose.py \
        parts/grade-{10,11,12}/id parts/grade-{10,11,12}/solutions/id
        indonesian prose gate: OK (70 files)

latexmk one_math_book_2_high_school_id.tex
L=build/one_math_book_2_high_school_id.log
grep -c '^!'      $L   → 0
grep -ci undefined $L  → 0
grep -c Overfull   $L  → 0
Output written on build/one_math_book_2_high_school_id.pdf (346 pages)

python3 tools/link_defined_terms.py --book 2 --lang id --check
        CHECK: every file matches what the config generates
```

### The one overfull box, and how it was removed

`parts/grade-11/id/02-functions-variations.tex`, exercise 6: three
`\text{ pada }` glosses inside one `\[ … \]` line, where English had three
`\text{ on }`. Indonesian `pada` is three characters longer than `on`, three
times over, and the display went 14.4 pt over. Fixed by using the shorter and
equally correct preposition for an interval, `\text{ di }`. No `\allowbreak`,
no `\emergencystretch`, no shrinking: the sentence simply got the right
Indonesian word.

### The build trap that nearly shipped an English book

`latexmk` records the dependency list of the *previous* run. The first run of
this edition happened when `parts/grade-*/id/` was still empty, so `\ominput`
fell through to English and latexmk memorised only the English bodies. Every
later `latexmk` call then answered "up to date" and rebuilt nothing — a green
log, a 330-page PDF, and English prose inside it. **Run `latexmk -g` once
after the first translated file lands**, then check the `.fls`:

```sh
grep -c 'grade-10/id' build/one_math_book_2_high_school_id.fls   # must be > 0
```

---

## 3. Method, and the tooling the next agent should reuse

Every file was produced as a **line-range patch on top of the English source**,
never as a free-hand rewrite. The scratchpad holds three scripts:

* `idlib.py` — the censuses: `\omterm` unwrapper, comment stripper, environment
  sequence, label sequence, `\begin{solution}{key}` sequence, `\emph` signature
  (per emph: *is it immediately followed by `\index{`?*), index count, ordered
  **math-span** sequence (`$…$`, `\[…\]`, `align`, `equation`, … with
  `\text/\mathrm/\textbf/…` arguments blanked), TikZ/pgfplots draw bodies with
  node text and axis labels blanked, and a brace delta relative to English.
* `id_show.py` — prints the English canon with line numbers; this is the only
  source of truth for the line numbers a patch may cite.
* `id_apply.py` — the applier. Patch format:

```
### parts/grade-12/id/06-integration.tex <<< parts/grade-12/06-integration.tex
!mathsub $0 = $ ==> $0 = \text{}$
@@ 1
\chapter{Pengintegralan}\label{ch:g12:integ}
@@ 36-38
Untuk fungsi yang tandanya sembarang, luas di bawah sumbu-$x$ dihitung
negatif; dan orang menetapkan
$\int_b^a f(x)\,\dd x = -\int_a^b f(x)\,\dd x$.
```

Every English line not named by a range is copied **byte-identically**. The
applier **refuses to write the file** unless all of these survive:

1. `\begin{env}` / `\end{env}` sequence, in order;
2. `\label{…}` sequence, in order;
3. `\begin{solution}{key}` sequence, in order;
4. `\emph` signature, in order (this is what keeps `harvest.bare_emph_map`
   happy: a bare `\emph` is only accepted when the English twin accepted the
   emphasis in the *same ordinal position*);
5. `\index{}` count;
6. **ordered math-span sequence** — the highest-value invariant, and the one
   that caught the most errors;
7. TikZ/axis draw bodies with node text blanked;
8. brace balance relative to English, and zero surviving `\omterm`.

A round-trip test confirms the pipeline is lossless: an **empty** patch
reproduces the unwrapped English byte-identically.

The loop was: `id_show.py` → hand-write the Indonesian → `id_apply.py` →
`check_indonesian_prose.py` → per-year `check_translation.sh`. Roughly
**forty** applier refusals were caught this way before a single build was run;
about ten of them were dropped or reordered math spans that no repository gate
would ever have found.

---

## 4. Terminology decisions worth recording

These are the rulings this edition made. They are stable across all three
years and should be promoted into `indonesian_style_card.md` so the other four
books do not re-litigate them.

**Numbers, algebra, sets**

| English | Indonesian | Note |
|---|---|---|
| natural numbers (`\N`, containing `0`) | **bilangan cacah** | see the ruling below |
| set / subset / union / intersection | himpunan / himpunan bagian / gabungan / irisan | |
| interval | interval | `selang` is used for the generic "range of x" prose |
| absolute value | nilai mutlak | |
| irrational | irasional | **not** `tak rasional` — the linked term is `irasional` |
| polynomial | suku banyak | `polinomial` kept where the English uses the Latin form in running prose |
| expand / factor | menjabarkan / memfaktorkan | |
| discriminant | diskriminan | |
| gcd | pembagi persekutuan terbesar, `FPB` in prose | notation stays `\gcd` |
| coprime | saling prima | |
| Euclidean division / quotient / remainder | pembagian Euklides / hasil bagi / sisa | |
| congruent modulo *n* | kongruen modulo *n* | the notion: **kekongruenan** |
| prime | prima; bilangan prima | |

**Functions and analysis**

| English | Indonesian | Note |
|---|---|---|
| function / domain / range | fungsi / daerah asal / daerah hasil | |
| increasing / decreasing | naik / turun | both stoplisted (§5) |
| slope | gradien | |
| limit / continuous / continuity | limit / kontinu / kekontinuan | |
| derivative / to differentiate | turunan / menurunkan | chain rule = **aturan rantai** |
| convexity / concavity | kecembungan / kecekungan | convex = cembung, concave = cekung — do not swap these |
| inflection point | titik belok | |
| primitive / antiderivative | primitif / antiturunan | |
| integration by parts | pengintegralan parsial | |
| mean value (of a function) | nilai rata-rata | |
| natural logarithm / half-life | logaritma asli / waktu paruh | |
| differential equation / equilibrium solution | persamaan diferensial / penyelesaian setimbang | |
| terminal velocity | kecepatan terminal | |

**Geometry, trigonometry, complex numbers**

| English | Indonesian | Note |
|---|---|---|
| unit circle / period / periodic | lingkaran satuan / kala / berkala | |
| law of cosines / addition formulas | aturan kosinus / rumus penjumlahan | result names, never linked (§5) |
| scalar product / orthogonal / orthonormal | hasil kali skalar / ortogonal / ortonormal | |
| collinear / coplanar / skew lines | segaris / sebidang / garis bersilangan | |
| normal vector / Cartesian equation | vektor normal / persamaan Kartesius | |
| tetrahedron / regular *n*-gon | bidang empat / segi-*n* beraturan | |
| complex number / conjugate | bilangan kompleks / konjugat | |
| real part / imaginary part | bagian real / bagian imajiner | |
| affix / modulus / argument | afiks / modulus / argumen | |
| algebraic / trigonometric / exponential form | bentuk aljabar / trigonometri / eksponen | |
| roots of unity / field | akar satuan / lapangan | |
| translation / rotation / scaling (homothety) | geseran / putaran / penskalaan (homoteti) | |

**Combinatorics, matrices, probability, statistics**

| English | Indonesian | Note |
|---|---|---|
| arrangement / permutation / combination | susunan / permutasi / kombinasi | |
| *k*-tuple / factorial / binomial coefficient | tupel-*k* / faktorial / koefisien binomial | |
| Pascal's triangle / binomial theorem | segitiga Pascal / teorema binomial | |
| derangement | permutasi kacau | |
| stars and bars | bintang dan batang | |
| matrix / entry / identity matrix / determinant | matriks / isian / matriks satuan / determinan | |
| adjacency matrix / graph / vertex / edge / walk | matriks ketetanggaan / graf / simpul / sisi / jalan | |
| diagonalization / eigenvector / steady state | pendiagonalan / vektor eigen / keadaan mapan | |
| sample space / event / independent / mutually exclusive | ruang sampel / kejadian / saling bebas / saling lepas | |
| conditional probability / law of total probability | peluang bersyarat / hukum peluang total | |
| Bayes' formula / prosecutor's fallacy | rumus Bayes / sesat pikir jaksa | |
| random variable / distribution | peubah acak / **distribusi** | see the ruling below |
| expectation / variance / standard deviation | **nilai harapan** / ragam / simpangan baku | see the ruling below |
| Bernoulli trial / success / failure | percobaan Bernoulli / berhasil / gagal | |
| mode / median / quartile / range (stat.) | modus / median / kuartil / jangkauan | |
| z-score | skor-z | |
| law of large numbers / sample mean | hukum bilangan besar / rata-rata contoh | |
| Markov / Bienaymé–Chebyshev inequality | ketaksamaan Markov / Bienaymé–Chebyshev | |
| density / uniform / exponential / normal distribution | kerapatan / distribusi seragam / eksponen / normal | |
| memorylessness / inspection paradox | ketiadaan ingatan / paradoks pemeriksaan | |
| fluctuation / confidence interval | selang ayunan / selang kepercayaan | |

### Three rulings that had to be made mid-book, and were then applied backwards

* **`distribution` = `distribusi`, not `sebaran`.** Grades 10–11 were written
  first and used `distribusi` (the term Indonesian SMA textbooks use:
  *distribusi binomial*, *distribusi normal*, *distribusi peluang*). Grade 12
  drifted to the purist `sebaran`. The whole of grade 12 was rewritten back to
  `distribusi`; `sebaran` survives only in grade 11 as the ordinary noun
  *spread* (`ragam mengukur sebaran nilainya`), which is exactly what it means
  there. **Promote `distribusi` to the card.**
* **`\N` = `bilangan cacah`, not `bilangan asli`.** The style card said
  `bilangan asli`; the canon defines `$\N$ is the set of natural numbers:
  $0, 1, 2, 3, \dots$`. Indonesian splits that set — `bilangan asli` starts at
  1, `bilangan cacah` starts at 0 — so printing `bilangan asli` beside
  `0, 1, 2, 3, …` would state something an Indonesian teacher would mark
  wrong. Raised rather than silently overridden; the orchestrator ruled that
  English is the source of truth for content, so the display follows the
  content. Three places render the canon's ℕ in grades 10–12 — the definition
  and the `⊂` chain in `parts/grade-10/id/01-numbers-and-sets.tex`, and the
  opening line of `parts/grade-12/id/01-sequences.tex` — and all three now say
  `bilangan cacah`, with `\index{bilangan cacah}` matching the visible term.
  `bilangan asli` is kept only where a set genuinely starts at 1; nowhere in
  this book does one. **Now on the card.**
* **`expectation` = `nilai harapan`, not bare `harapan`.** Grade 11 defines
  `nilai harapan`; grade 12 initially defined bare `harapan`, which then
  collided with the very common ordinary noun (`harapan labanya`, `harapan
  bayarannya`). Grade 12 was changed to `nilai harapan`, which both matches
  grade 11 and stops the link layer from wrapping every ordinary use.
  **Promote `nilai harapan` to the card.**

### Mechanics the card already rules, confirmed in use

Decimal separator is a **point** everywhere (`0.368`, `9.81`, `2.006`), digits
are ASCII, `-nya` is attached, reduplication is a bare hyphen
(`lagi-lagi`, `sepasang demi sepasang`, `masing-masing`), `di`/`ke` are
separated as prepositions and attached as prefixes (`di bawah` vs `diterima`),
and no English gloss is ever left in parentheses.

---

## 5. The link layer

`tools/term_config/book2_id.py` was written from scratch, not translated from
`book2_en.py`. `AMBIG_POLICY = "nearest-preceding"` (a spiral curriculum
re-defines its terms each year, exactly as in English).

```
terms harvested        : 187
dropped (defined twice): 35
dropped (stoplist)     : 12
LINKABLE TERMS         : 169
chapter-local terms    : 34
links inserted         : 3 678 across 70 files
by target              : def 3 405, prop 104, pb 52, ex 49, thm 37, met 31
--check                : every file matches what the config generates
```

| Year | EN links | ID links | EN targets | ID targets | target diff |
|---|---:|---:|---:|---:|---|
| grade-10 | 978 | 1 023 | — | — | **identical sets** |
| grade-11 | 1 275 | 1 171 | — | — | 4 EN-only, 0 ID-only |
| grade-12 | 1 653 | 1 484 | — | — | 6 EN-only, 2 ID-only |
| **whole book** | 3 906 | **3 678** | **123** | **124** | **0 EN-only, 1 ID-only** |

**Whole-book parity: every English target is reached by the Indonesian tree.**

### The stoplist, and why each word is on it

`STOP` is soft: a stoplisted word is still linked inside the chapter that
defines it, which is what makes the school-book senses behave.

* The style card's homograph list: `bidang` (plane / face / field of study),
  `kali` (times / occasion), `bagi` (divide / for), `sisi` (side / face /
  "di sisi lain"), `luas` (area / broad), `naik`, `turun` (monotonicity / the
  ordinary verbs), `titik` (point / full stop), `modus` (statistical mode /
  *modus operandi*), `deret` (series / row), `rata-rata` (mean / expectation /
  "the average person"), `skala`.
* Added by this edition: `jumlah` (sum of numbers, of a series, of roots — the
  harvested sense is the sum of two *vectors*), `gabungan` (union of sets /
  linear combination), `genap`, `ganjil` (parity of an *integer* everywhere,
  while the harvested sense is the parity of a *function*; `fungsi genap` /
  `fungsi ganjil` survive as phrases), `terbatas` (the participle "bounded
  interval" far more often than the property), `jangkauan` (statistical range /
  ordinary reach), `peluang` (the measure / everyday "chance"), `aritmetika`,
  `geometri` (the branches, not the sequence adjectives), and the ordinary
  emphasis words `semua`, `tegas`, `serentak`, `tepat`.

`NOT_A_TERM` uses bare Indonesian heads — Indonesian writes result names as
`X <nama>` phrases with no solid compounding to substring-match into, unlike
Dutch: `teorema`, `lema`, `akibat`, `ketaksamaan`, `rumus`, `kaidah`,
**`aturan`**, `asas`, `identitas`, `hukum`, `paradoks`, `soal`, `sifat`.
`aturan` had to be added: without it, `aturan kosinus` and `aturan rantai`
became links to `thm:g11:scal:cosines` and `thm:g12:deriv:chain`, two targets
English does not use.

`DROP` holds exactly one entry: `ketiadaan ingatan`. English writes
*memorylessness* as one word and the index-only harvest skips single words;
the Indonesian phrase has a space, so it slipped in as a term and had to be
dropped by hand.

`DERIVED` declares the reduplicated plurals `lang_id.py` deliberately does not
generate for multi-word terms (`bilangan-bilangan prima`, `peubah-peubah
acak`, `himpunan-himpunan bagian`, …).

### Four calibration bugs found by the parity diff, and fixed at source

The parity diff is the only tool that finds these; a green `--check` does not.

1. **A capitalised display becomes a separate term that bypasses `STOP`.**
   `\emph{Jumlah}\index{vektor!jumlah}` (sentence-initial, grade-10 vectors)
   harvested `Jumlah` as its own term, which `STOP = {"jumlah"}` did not
   match — so 21 occurrences of "Jumlah dua kuadrat" across grades 11–12
   linked to the *vector* sum. Fixed by rewording so the emphasis is
   lowercase (`Yang disebut \emph{jumlah}…`), after which `_cap` handles both
   cases and `STOP` applies.
2. **A `-nya` inside the display does the same.** `\emph{gradiennya}` and
   `\emph{Distribusinya}` created the terms `gradiennya` and `Distribusinya`,
   pinned to whatever label preceded them, instead of merging with `gradien`
   and `distribusi` (whose patterns already cover `-nya` via
   `WORD_TAIL`). Fixed by taking the enclitic out of the emphasis.
3. **A capitalised display can also make a term unreachable.**
   `\emph{Skor-z}\index{skor-z}` produced a pattern that only matched the
   capitalised form — which occurs nowhere but in the definition itself, so
   the term generated **zero** links while English generated 14. Fixed the
   same way.
4. **One wording slip.** Grade-12 arithmetic wrote `tak rasional` where the
   book's term is `irasional`; the exercise lost its link to
   `ex:g10:numbers:classify`.

### The remaining divergences, one by one

**Whole book — one extra target, zero missing.**

* `def:g12:contdist:uniform` (`distribusi seragam`, 2 links). English defines
  *uniform distribution* identically but never writes the phrase again outside
  the definition, so English harvests the term and links it zero times. The
  Indonesian prose does say `distribusi seragam` twice more. Density, not
  sense.

**Per-year — which year a target is reached in.** All of these are
`nearest-preceding` doing its job, or a stoplist ruling:

* `def:g10:proba:distribution` (EN grades 11 and 12): Indonesian `distribusi`
  resolves to the *nearer* definition `def:g11:prob:rv` inside grades 11–12 —
  the same notion, one year closer to the reader.
* `def:g10:stats:mean` (EN grade 11): `rata-rata` is stoplisted, so inside
  grade 11 it links to `def:g11:stat:mean`, the grade's own definition.
* `def:g10:numbers:interunion` (EN grade 11): reached in Indonesian through
  `irisan`, not `gabungan` — `gabungan` is stoplisted because it is also
  *linear combination* and *integer combination* throughout grades 11–12.
* `def:g10:functions:variations`, `def:g10:lines:system`,
  `def:g10:proba:sample`, `def:g10:stats:series`, `def:g11:func:monotone`,
  `def:g11:vect:collinear` (EN grade 12): the Indonesian prose of those
  chapters happens not to use the phrase, or uses a word that resolves to a
  nearer definition (`monoton` → `def:g12:seq:monotonic`, `segaris` →
  `def:g12:space:collinear`). Every one of them is reached elsewhere in the
  book, which is why whole-book parity is complete.
* `def:g10:numbers:abs`, `def:g10:stats:median`, `def:g10:vectors:sum`
  (ID-only, per-year): the Indonesian prose uses `nilai mutlak`, `median`,
  `jumlah vektor` in a year where the English prose did not. Right sense,
  right target.

---

## 6. Sampled passages, judged

Five passages, read cold and judged as an Indonesian teacher would.

**(1) Chapter opening, grade 10 — `01-numbers-and-sets.tex`** — *native.*

> Matematika bermula dari bilangan, dan tidak semua bilangan sejenis: bilangan
> untuk membilang, bilangan negatif, pecahan, serta bilangan seperti $\sqrt 2$
> atau $\pi$ yang tidak dapat dinyatakan oleh pecahan mana pun.

Correct `serta` for the third member of a list, `mana pun` written apart, no
calque of "of the same kind". Reads like the first page of an SMA book.

**(2) Definition, grade 12 — `06-integration.tex`** — *native.*

> Misalkan $f$ kontinu dan positif pada $\intcc{a}{b}$. Yang disebut
> \emph{integral}\index{integral} … adalah luas, dalam satuan luas, daerah yang
> dibatasi oleh kurva $f$, sumbu-$x$, dan garis tegak $x = a$ dan $x = b$.

`Yang disebut … adalah` is the standard Indonesian definitional frame and lets
the emphasised term stay lowercase (which the link layer needs, §5). `garis
tegak` rather than a calqued *garis vertikal*.

**(3) Proof, grade 12 — `10-arithmetic.tex`, infinitude of primes** — *native.*

> Diberikan sebarang daftar berhingga $p_1, \dots, p_k$ berisi bilangan prima,
> tinjaulah $N = p_1 p_2 \cdots p_k + 1$. Ada prima $p$ yang membagi $N$;
> tetapi tak satu pun $p_i$ membagi $N$ (sebab sisanya $1$), sehingga $p$ prima
> yang tak ada di daftarnya. Jadi tak ada daftar berhingga yang menghabiskan
> bilangan primanya.

`sebarang` (arbitrary) correctly distinguished from `sebaran`; `tak satu pun`
for "no"; the closing `Jadi …` is how an Indonesian proof ends.

**(4) Weekend-problem narration, grade 12 — `15-sums-lln.tex`** — *near-native.*

> Seorang pemain rolet sesudah $100$ putaran, hampir sesering tidak, sedang
> \emph{unggul}. Kasino yang menjalankan sejuta putaran unggul dengan kepastian
> yang takkan dipersoalkan pengadilan mana pun.

Vivid and idiomatic, but `hampir sesering tidak` is a close rendering of
English *almost as often as not*; a native writer would more likely say
`kira-kira separuh waktunya`. Kept because the rhythm of the original sentence
is part of the book's voice. This is the register cost counted in §8.

**(5) Solution prose, grade 12 — `13-conditional-probability.tex`** — *native.*

> Dengan laju dasar $\frac{1}{1000}$, orang sakit itu begitu jarang sehingga
> bahkan bocoran $5\,\%$ dari mayoritas sehat yang sangat besar itu
> menenggelamkan positif benarnya lima puluh berbanding satu.

`begitu … sehingga` is the right correlative, `berbanding` is the right word
for a ratio, and the sentence keeps the English's rhetorical punch without its
syntax.

**Verdict: 5 native / near-native, 0 MT.** Nothing in the sample reads as
post-edited machine output, which is expected — none of it is.

---

## 7. Gate traps for the next Indonesian agent

1. **`bahwa` is not in `ID_MARKERS`.** A line whose only function words are
   `bahwa` and a verb will trip the `untranslated` class. Add `yang`, `itu`,
   `pada`, `dan`, `dengan`, or re-flow the line.
2. **The gate splits chunks on `[.!?;:\n]+`, so the unit is the *source
   line*.** A perfectly Indonesian sentence can fail because its second
   physical line happens to hold eight bare content words. Re-flow, do not
   invent words.
3. **`as` (the ace of cards) is English.** The plural rule strips the `s` and
   finds `a` in `ENGLISH_FUNCTION`. Use `kartu raja` / `kartu hati` in card
   exercises — this edition did, consistently, in both the exercises and their
   solutions.
4. **English `$3x + 2y = $ constant` trips `math-space`.** The English canon
   itself contains open-ended inline math like `$0 = $ nonzero`. Either reword
   (`keluarga garis $3x + 2y$ tetap`) or declare a `!mathsub` in the applier so
   the census still matches (`!mathsub $0 = $ ==> $0 = \text{}$`).
5. **TeX accent escapes are a gate-6 failure and the English sources have
   several.** `Ren\'e`, `Vi\`ete`, `M\'er\'e`, `Bienaym\'e`, `\"Otzi`,
   `caf\'e` all had to become UTF-8 (`René`, `Viète`, `Méré`, `Bienaymé`,
   `Ötzi`, `kafe`) as they were translated.
6. **Longer Indonesian words make displays overfull.** Prefer the shorter of
   two correct prepositions inside `\text{…}` in a display (`di` over `pada`).
7. **`latexmk` will lie to you.** See §2: force `-g` once, then check the
   `.fls`.

---

## 8. Why not 100

* **−1 register.** Roughly a dozen of the longest weekend-problem sentences
  keep the English clause order (sample 4 above). They are grammatical and
  clear, and the rhythm is deliberate, but a native author writing from
  scratch would have broken two or three of them differently.
* **−1 link layer.** One ID-only target (`def:g12:contdist:uniform`) and a
  per-year distribution of targets that differs from English wherever the
  Indonesian prose naturally used a different word. Every case is right-sense
  (§5), but it is not byte-parity.
* **−1 elsewhere.** The book carries two Indonesian words for *conjugate*:
  `bentuk sekawan` for the conjugate surd (defined in grade-10 §4, used by the
  limit chapters — `kalikan dengan bentuk sekawannya`) and `konjugat` for the
  complex conjugate (grade-12 §9). The split follows Indonesian usage and each
  word is right where it stands, but a reader meeting both in one volume has
  to be told they are the same idea twice; a purist edition would say so in a
  remark.

---

## 9. State

* **70 / 70 files delivered**, all three years complete.
* `tools/term_config/book2_id.py` created and curated.
* Link layer generated, `--check` green, idempotent.
* Build: 0 / 0 / 0, **346 pages**.
* **No git commit was made**; the working tree is left for review.
* No file outside the assigned scope was modified. In particular the shared
  wiring (`styles/`, entry files, `frontmatter/`, `latexmkrc`, CI,
  `tools/termlink/`, `tools/term_config/lang_id.py`,
  `tools/check_indonesian_prose.py`, `tools/check_translation.sh`) was read but
  **not** touched.

---

## 10. Requests to the orchestrator

1. ~~Rule on `\N`.~~ **Done** — ruled `bilangan cacah`, applied, rebuilt (see
   the revision note and §4). Nothing outstanding.
2. ~~Promote the rulings to `indonesian_style_card.md`.~~ **Done by the
   orchestrator** — the ℕ ruling, `distribusi` not `sebaran`, `nilai harapan`
   not bare `harapan`, `irasional` not `tak rasional`, the four link-layer
   calibration rules as a new §4b, and the `latexmk -g` trap in §5.
3. **Nothing shared needs changing.** The `id` wiring — style file,
   `styles/lang/id.tex`, the five entry files, `frontmatter/preface.id.tex`,
   `latexmkrc`, CI, `tools/termlink/books.py`, `tools/term_config/lang_id.py`,
   `tools/check_indonesian_prose.py`, gate 8 — was correct as delivered and
   carried three years of prose without a single amendment.
