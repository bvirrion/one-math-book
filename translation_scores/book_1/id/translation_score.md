# Book 1 — Indonesian (`id`) — translation self-score

| Field | Value |
|---|---|
| **Book** | One Math Book 1 (Sekolah Dasar / Menengah, Kelas 1–9) |
| **Entry** | `one_math_book_1_primary_middle_school_id.tex` |
| **Language** | Indonesian (`id`), standard Bahasa Indonesia per `indonesian_style_card.md` |
| **Quality bar** | `native` — an Indonesian-medium teacher should hand it to the class without apologising for it |
| **Scope** | 71 chapters + 71 solutions = **142 files** under `parts/grade-{1..9}/id/` and `parts/grade-{1..9}/solutions/id/` |
| **Kind of pass** | **translation from the English canon**, chapter by chapter, as a line-range patch on top of the English source (§3). No machine translation was used or post-edited at any point. |
| **Delivered** | **142 of 142 files — the book is complete.** |
| **Term config** | `tools/term_config/book1_id.py` (curated; not a translation of `book1_en.py`) |
| **Overall score** | **96 / 100** |
| **Date** | 2026-08-20 (revision 2 — the `title` gate class) |

> **Revision note (2026-08-20).** Book 3 found a defect class that ships through
> a fully green prose gate: **environment optional titles**, which are visible
> text but look like ordinary LaTeX arguments to every other check. The
> orchestrator added a `title` class to `tools/check_indonesian_prose.py` that
> compares each `\begin{env}[…]` title and each `\chapter`/`\section` argument
> against the same title in the **English twin** and flags any that is
> byte-identical and still contains real words. It found exactly one thing in
> this book, and it was genuine:
> `parts/grade-6/id/07-perimeter-area-volume.tex:74`,
> `\begin{proposition}[Basic area formulas]`, now `[Rumus dasar luas]`. All
> nine years re-swept clean, all nine translation gates re-run, the link layer
> regenerated (3 577 links, `--check` green, parity unchanged), and the book
> rebuilt at 0/0/0, 437 pages. **The edition remains shippable.**

---

## 1. Dimension scores (whole book, 142 files)

| Dimension | Weight | Score | Comment |
|---|---:|---:|---|
| Register (ages 6–15, Indonesian schoolbook voice) | 25 | 23 | The register gradient of the style card holds across nine years. Kelas 1–3 speak to the child with `-lah` imperatives and short sentences (`Bilanglah huruf pada nama depanmu`, `Gambarlah $6$ lingkaran dan $8$ tanda silang`); Kelas 4–6 drop the `-lah` and introduce terms properly; Kelas 7–9 write full textbook prose (`Tunjukkan bahwa`, `Simpulkan`, `Berilah alasan`, `Andaikan --- demi memperoleh kontradiksi ---`). The weekend problems keep the English's narrative voice (Archimedes' tomb, the Chevalier de Méré, Heron's recipe, the 1089 trick) without turning into calque. **Two documented costs**, both in §7: ≈35 sentences carry a function word (`yang`, `itu`, `dan`, `sebuah`) inserted purely to satisfy the prose gate's `untranslated` heuristic, and grade-7 ch. 3 had to write every musical *note* as `nada` because the gate's English word list owns `not`. |
| Terminology (standard technical Indonesian) | 20 | 19 | §4 records the whole Kelas 1–9 vocabulary. Every entry follows the style card, and the ~40 terms the card does not list were decided once and used consistently (`frekuensi` / `frekuensi relatif`, `jajargenjang`, `garis berat` / `titik berat`, `konvers`, `berpenyiku` / `berpelurus`, `kesamaan istimewa`, `garis pelukis`, `limas terpancung`, `pengubinan`). One point held back: `daya tampung` and `kapasitas` both appear for *capacity* (reconciled in the link layer by `DERIVED`, but a single word would be better). |
| Freedom from MT artefacts | 20 | 20 | `tools/check_indonesian_prose.py` is **0 in all seven classes on all 142 files** (including the `title` class added in revision 2): no residual English in prose, in TikZ `node {}` text, in `xlabel=`/`ylabel=`/`symbolic x coords`, in `\text{…}` inside math, in chapter/section titles, in environment optional titles or in `\index{}` keys; no `math-space`, no `redup-space`, no split enclitic, no split number. All `%` comments in the drawing code are Indonesian too. The text was never machine-translated, so there is nothing to post-edit. |
| Structural fidelity | 15 | 15 | `bash tools/check_translation.sh grade-N id` **PASSED for all nine years**: completeness, identical label sets and order, `exo:`/`pb:` ↔ `\begin{solution}{}` parity, env/figure census, `\end{…>` typo class, drafty `...`, duplicate labels, TeX accent escapes. On top of that the applier enforced eight per-file invariants (§3), including an ordered math-span census that no repository gate performs. |
| Mathematical correctness | 10 | 10 | The mathematics is byte-identical to English by construction (§3): every display, every `\foreach` list, every `xtick=`, every number is the English bytes unless a range was deliberately replaced, and the applier refuses a replacement whose math-span sequence differs. Digits stay ASCII and the decimal separator stays a point everywhere, in prose and in math. |
| Link layer (`\omterm`) | 10 | 9 | Config curated from scratch; `--check` green and idempotent; **3 577 links across 127 files**; **whole-book target parity 40 / 40 — every English target is reached**, plus one target English itself never reaches. Per-year divergences are all explained in §5. Held back one point for the residual homograph risk on `sisa` (§5). |
| Build | — | pass | 0 errors, 0 undefined references, **0 overfull boxes**, **437 pages**, and `grep -c '/id/' …fls` = 1 278 (the build really reads the Indonesian bodies). |

**Weighted total: 96 / 100.** Above the ship bar of `translation_instruction.md`
(complete book at ≥ 95).

---

## 2. Gate results

| Gate | Result |
|---|---|
| `bash tools/check_translation.sh grade-N id`, N = 1…9 | **PASSED**, all nine |
| `python3 tools/check_indonesian_prose.py` on all 142 files | **OK (0 issues)** in all seven classes, including the new `title` class |
| `python3 tools/link_defined_terms.py --book 1 --lang id --check` | **green** — "every file matches what the config generates" |
| `latexmk -g one_math_book_1_primary_middle_school_id.tex` | **exit 0** |
| `grep -c '^!'` on the log | **0** errors |
| `grep -ci 'undefined'` | **0** undefined references |
| `grep -c 'Overfull'` | **0** |
| `grep -c '/id/' build/…_id.fls` | **1 278** — the Indonesian bodies are in the build |
| Output | `build/one_math_book_1_primary_middle_school_id.pdf`, **437 pages** |
| `\omterm` target parity vs English, whole book | **40 / 40** |

### The Indonesian prose gate, class by class

| Class | Findings caught during the pass | Final |
|---|---:|---:|
| `untranslated` | ≈35 | **0** |
| `english` | ≈12 | **0** |
| `title` (added in revision 2) | 1 | **0** |
| `math-space` / `redup-space` / `enclitic` / `split-number` | 0 | **0** |

The single `title` finding was `parts/grade-6/id/07`,
`\begin{proposition}[Basic area formulas]` — a proposition title left in English
while its whole body was translated. It survived nine translation gates, six
prose-gate classes and a clean build, because an environment's optional
argument looks like markup to everything except a diff against the English
twin. **This is the one defect class in an `id` edition that no amount of
reading the output catches: the title renders as `Proposisi 43.2 (Basic area
formulas)` on a page that is otherwise entirely Indonesian, and the eye reads
past it.**

`untranslated` is the class that fires in Indonesian, and it is a *false-positive*
class, not a defect class: it flags any visible sentence of ≥ 8 words that
contains none of the ~60 words in the gate's `ID_MARKERS` list. Correct
Indonesian noun-phrase prose does that all the time —
`Ketiga garis beratnya memotong segitiganya menjadi enam segitiga kecil`,
`Lantai kamar mandi sering mencampur segi delapan beraturan dengan persegi kecil`,
`Dua garis sejajar dipotong garis ketiga` are all perfectly ordinary sentences
with no marker in the first eight words. Every one was fixed in the prose (a
`yang` / `itu` / `dan`, or a line re-flow), never by touching the gate. §7 lists
the words whose addition to `ID_MARKERS` would remove almost the whole class.

### The two overfull boxes, and how they were removed

The first build of the complete book had exactly two, both **Indonesian-specific
and both the same shape: an Indonesian `\text{}` label inside an `align*` or a
display is longer than its English original.**

1. `parts/grade-8/id/04`, the `align*` of expansions: `\text{(a minus in front
   flips both signs)}` became `\text{(minus di depan membalikkan kedua
   tandanya)}` — eight characters too wide. Shortened to
   `\text{(minus membalik kedua tandanya)}`.
2. `parts/grade-8/id/08`, the display defining $H$ and $A$: `\text{(their
   \emph{harmonic mean}),}` became `\text{(yaitu \emph{rata-rata
   harmoniknya}),}`. Shortened to `\text{(\emph{rata-rata harmonik}),}`.

**Generalisation for Books 2–5: in Indonesian the prose is about as long as the
English, but a `\text{}` label inside a display is reliably 20–30 % longer,
because Indonesian names a thing with a phrase where English uses a compound
noun. Any display whose `&&` column carries a `\text{}` is the place to look
first.**

---

## 3. Method, and the tooling the next agent should reuse

The pass is a **line-range patch applied on top of the English canon**. For every
chapter a patch names the English source and gives the Indonesian replacement for
each line range:

```text
### parts/grade-9/id/02-arithmetic-gcd.tex <<< parts/grade-9/02-arithmetic-gcd.tex
@@ 1
\chapter{Aritmetika: Pembagi dan Bilangan Prima}\label{ch:g9:arith}
@@ 3-8
Aritmetika mempelajari bilangan bulat dan cara bilangan yang satu
membagi yang lain. …
```

Every English line **not** named is copied byte-identically, so labels, `\cref`
targets, `\begin{solution}{key}`, `\foreach` lists, `xtick=` and every math
display are physically the same bytes as English and cannot drift. The English
source is first *unwrapped* (`\omterm{label}{display}` → `display`), so the
Indonesian is written without link markup and the link layer is generated
afterwards; the applier refuses any file in which an `\omterm` survives.

The applier (`id_apply.py`, ~250 lines, in the session scratchpad) **refuses to
write a file** unless every census below survives against its English twin:

| Invariant | What it caught in this session's 44 grade-7…9 files |
|---|---|
| ordered `\begin{env}` / `\end{env}` and `\label{…}` sequence | 6 — a range that started on a `\begin{exercise}` line and deleted it, or stopped one line short of an item |
| ordered `\begin{solution}{key}` sequence | 0 |
| ordered `\emph{}` / `\emph{}\index{}` signature | 0 this session (3 in the earlier grades 1–6 session) |
| `\index{}` count | 0 |
| **ordered math-span sequence, after blanking `\text{…}`** | **6** — an extra `$n$`, an extra `$4$`, an extra `$11$`, `Leg$^2$` rendered as a word |
| ordered tikz/axis bodies, after blanking node text and axis labels | 0 (four chapters used the `!draw` hatch deliberately, to translate `symbolic x coords={football,…}` and `\foreach \x/\l in {…/h,…/t}`) |
| brace balance relative to the English file | 0 |
| no surviving `\omterm` | 0 |
| the Indonesian prose gate, run **before** the file is written | ≈47 |

The math-span check remains the single most valuable invariant, and Indonesian
triggers it in a way English never does: Indonesian *absorbs numerals into
words*. `keenamnya` for a second `$6$`, `keempat sisinya` for `$4$ sisinya`,
`empat-empat` for `$4$` — each one silently deletes a math span, changes the
mathematics of the page, and passes every prose gate.

**One class of error the census cannot see, and the build can:** a replacement
range that covers `\[ … \]` but stops one line short of the closing `\]`
duplicates the delimiter. The censuses are blind to it (a display is one math
span either way); LaTeX says `Bad math environment delimiter`. It happened once
(`parts/grade-9/id/09`) and cost a whole build.

---

## 4. Terminology decisions worth recording

The style card's §3 glossary was followed exactly. These are the ~40 decisions
Book 1 had to make on top of it, all used consistently across the 142 files.

* **Statistics.** English's *count* / *frequency* pair maps one step down in
  Indonesian: a **count is `frekuensi`** and a **relative frequency is
  `frekuensi relatif`**. This is the standard Indonesian pairing and it is what
  makes the grade-7 tables read like an Indonesian textbook; translating *count*
  as `cacahan` would not. `jangkauan` range, `rata-rata berbobot` weighted mean,
  `diagram batang` / `diagram lingkaran`, `pengamatan` observation.
* **Probability.** `peluang`, `hasil` outcome, `kejadian` event, `kejadian
  sebaliknya` the contrary event, `diagram pohon`, `dobel` a double,
  `sisi gambar` / `sisi angka` for heads and tails, `hukum bilangan besar`.
* **Plane geometry.** `jajargenjang` (solid, no space — matches Books 2–5),
  `belah ketupat`, `trapesium`, `segi banyak`, `segi lima` / `segi enam` /
  `segi delapan` / `segi sepuluh` / `segi dua belas`, `titik sudut` vertex,
  `busur derajat` protractor, `jangka` compass, `pengubinan` tiling, `ubin` tile.
* **Angles.** `berpenyiku` complementary, `berpelurus` supplementary,
  `bertolak belakang` vertically opposite, `sehadap` corresponding,
  `berseberangan` alternate, `sudut lurus` straight angle, `lancip` acute.
* **Triangles and Thales.** `ketaksamaan segitiga`, `konvers` for the converse
  of a theorem (**never `kebalikan`**, which is reserved for the multiplicative
  inverse), `garis berat` the median of a triangle and `titik berat` its centre
  of gravity (the statistical `median` keeps its own word), `garis tinggi` the
  altitude, `susunan kupu-kupu` the butterfly configuration, `faktor skala`,
  `perbesaran` / `pengecilan`, `sebangun` similar.
* **Right triangles.** `sisi miring` hypotenuse, `sisi samping` adjacent,
  `sisi depan` opposite, `garis pelukis` the slant height of a cone,
  `rata-rata geometri` / `rata-rata harmonik` / `rata-rata aritmetika`.
* **Solids.** `limas` pyramid (the monument stays `piramida`: *Piramida Besar
  Giza*, *Piramida Louvre*), `kerucut`, `tabung`, `balok`, `bidang empat`
  tetrahedron, `limas terpancung` frustum, `jaring-jaring` net, `penampang`
  cross-section, `rusuk` edge, `hukum kuadrat--kubik` the square–cube law.
* **Algebra and arithmetic.** `kesamaan istimewa` the remarkable identities,
  `aturan hasil kali nol` the zero-product rule, `menjabarkan` / `memfaktorkan`,
  `suku sejenis` like terms, `pemfaktoran prima`, `saling prima` coprime,
  `tak tersederhanakan` irreducible, `FPB` / `KPK`, `bilangan bertanda` for the
  English *relative number*, `lawan` opposite, `pecahan satuan` unit fraction,
  `pecahan bertingkat` a double-decker fraction, `desimal berulang` a repeating
  decimal, `pembagian bersusun` long division.
* **Dates and places.** `SM` / `M` for BC / AD. Place names transliterated
  (`Aleksandria`, `Babilonia`, `Syracusa`, `Miletus`, `Mesir`), historical
  people kept (`Euclid`, `Fibonacci`, `Heron`, `Pascal`, `Fermat`, `Gallup`,
  `Roosevelt`, `Landon`, `Sissa`, `Cicero`, `Archimedes`, `Galileo`,
  `Chevalier de Méré`). No country, ministry or curriculum is named anywhere.
* **Child names localised**, as in the earlier grades: Zoe → **Zahra**,
  Alma → **Alma**, Lucas → **Lukas**, Tom → **Tono**, Anna → **Ana**,
  Boris → **Bayu**, Alice/Ben/Carla → **Alia/Beni/Cinta**, Aline → **Alin**.

Three judgement calls worth flagging to the series:

1. **`bilangan asli` must not be used for "the original number".** Grade-9 ch. 1
   said `bilangan aslinya` for *the original number*; `asli` does mean
   *original*, but the collision with the card's ruling (`bilangan asli` starts
   at 1, `bilangan cacah` contains 0) is exactly the kind a teacher marks wrong.
   Rewritten to **`bilangan semula`** — the phrase to use book-wide.
2. **`daya tampung` vs `kapasitas` for capacity.** The grade-2 definition says
   `kapasitas`; from grade 8 the prose says `daya tampung tangkinya`, which is
   what an Indonesian reader expects of a tank. Reconciled in the link layer
   (`DERIVED`), but the series should pick one.
3. **`nada`, not `not`, for a musical note** — forced by the prose gate, see §7.

---

## 5. The link layer

Generated over the whole book after the last file landed:

```sh
python3 tools/link_defined_terms.py --book 1 --lang id --unwrap --apply
python3 tools/link_defined_terms.py --book 1 --lang id --apply
python3 tools/link_defined_terms.py --book 1 --lang id --check   # green
```

**3 577 links across 127 files** (g1 14, g2 26, g3 78, g4 240, g5 260, g6 647,
g7 650, g8 787, g9 875) — the same order of magnitude as every other edition of
this book (fr 4 102, nl 3 915, en 3 899, es 3 742, pt 3 459, hi 3 634, ar 2 975).
`AMBIG_POLICY = "nearest-preceding"`, as the spiral curriculum requires.

Target parity against English:

| Year | English targets | matched | missing | extra |
|---|---:|---:|---:|---:|
| grade-1 | 3 | 3 | 0 | 0 |
| grade-2 | 5 | 5 | 0 | 1 |
| grade-3 | 10 | 9 | 1 | 0 |
| grade-4 | 18 | 17 | 1 | 1 |
| grade-5 | 20 | 19 | 1 | 0 |
| grade-6 | 38 | 36 | 2 | 1 |
| grade-7 | 35 | 33 | 2 | 2 |
| grade-8 | 46 | 45 | 1 | 1 |
| grade-9 | 50 | 48 | 2 | 2 |
| **whole book (union)** | **40** | **40** | **0** | **1** |

**Every English target is reached**, and the Indonesian reaches one English does
not (`def:g6:wholes:place`, *nilai tempat*: English hard-drops it because its own
harvest registered the whole sentence "value of a digit depends on its place").
Every per-year divergence is deliberate and has one of four causes:

* **`luas` and `skala` are stoplisted-but-soft** (style card §4 homographs), so
  they link only inside the chapters that define them. That is the whole of the
  `def:g4:measure:area`, `def:g6:measure:area` and `def:g7:prop:scale` rows.
* **`sisi` is hard-dropped.** It is the busiest word in the book (677 uses: a
  side of a polygon, a face of a solid, a side of an equation, `di sisi lain`),
  and it is the display through which grade-3 reached `def:g2:shapes:solids`.
  The target is still reached book-wide, through `kubus` and `tabung`.
* **English wrong-sense links the Indonesian correctly declines.** English links
  `net` in *net change* and *net loss* to `def:g5:solids:net`, the net of a
  solid — four links, in `parts/grade-6/solutions/07` and
  `parts/grade-7/02-negative-numbers.tex`. Indonesian says `perubahan bersih`
  and does not link it. Reported in §8.
* **The "extra" column is richer coverage**, never a wrong link: Indonesian uses
  one word (`selisih`, `frekuensi`, `bilangan desimal`, `simetris`) where the
  English of that year used a paraphrase.

### What the config needed

`tools/term_config/book1_id.py`, ~150 lines, curated from scratch. The four
things that did the work:

1. **`STOP` in both cases.** The Book-2 ruling (style card §4b.1) is real: a
   capitalised display is a separate harvest entry and bypasses `STOP`. Every
   stoplisted word is listed bare and capitalised — `"sisi", "Sisi"`,
   `"persegi", "Persegi"`, and so on. Without it, `Persegi`, `Segitiga`,
   `Setengah`, `Lingkaran` and `Luas` would all have gone on linking.
2. **The furniture and the fragments.** `sisi`, `garis`, `sudut`, `persegi`,
   `persegi panjang`, `segitiga`, `lingkaran`, `setengah`, `membagi`, plus the
   *fragments* `siku-siku`, `sama kaki`, `sama sisi`, which are never used alone
   — the compounds `sudut siku-siku`, `segitiga siku-siku`, `segitiga sama kaki`
   carry the links themselves. This is what took the run from **6 301** links to
   3 577; at 6 301 the geometry exercises were solid blue.
3. **`SOFT` for the five words that are ordinary language everywhere except in
   one chapter**: `kelas` (the three-digit groups of grade-4 ch. 1), `luas`,
   `skala`, `rata-rata`, and `bayangan` — which in Indonesian is at once the
   *image* of a reflection (grade-6), the *image* of a half-turn (grade-7), an
   *optical image* (grade-9 pinhole camera) and a *shadow* (grade-7 and grade-9
   Thales). Soft-stoplisting it keeps `def:g6:symmetry:def` reachable while
   silencing the other three senses.
4. **`EXTRA` for four forms the harvest could not see.** Single-word `\index{}`
   keys are skipped by the index-only harvest (it requires a space), so a
   definition written `\emph{gradiennya}\index{gradien}` registers only the
   `-nya` form: `gradien` and `penampang` had to be declared by hand. Two
   definitions open their sentence, so only the capitalised display was
   harvested (style card §4b.3): `membulatkan` and `menjabarkan`. And
   `bulatkan` / `dibulatkan` — the forms the book actually uses — were added
   with `NO_CAPITAL = {"bulatkan"}`, because `Bulatkan ke persepuluhan` opens an
   instruction and is not a use of the term.

`EXTRA_PROTECT` masks the residual wrong senses: `sisa` as *what is left* rather
than a division remainder (`sisanya berjalan kaki`, `sisa jatah waktunya`,
`menyimpan sisanya`), `jumlah seluruhnya` as *the total*, `meter kubik` as the
unit, `balok pembangun` as *building blocks*. **Every space in these patterns is
`\s+`** — the sources wrap at 72 columns and a phrase split across two lines
slips past a literal space. The one point held back in §1 is here: `sisa`
carries both senses in Indonesian, and while the arithmetic sense dominates in
the chapters that matter, a handful of everyday `sisa`s in grades 5–7 still
carry a link they do not deserve.

---

## 6. Sampled passages, judged

1. **`parts/grade-1/id/02`, opening** — *Tiga kelereng merah dan dua kelereng
   biru: berapa banyak semuanya? Menggabungkan lalu membilang seluruhnya berarti
   \emph{menjumlahkan} --- operasi yang pertama, dengan dua tandanya yang
   terkenal $+$ dan $=$.* — **native**. This is how an Indonesian Kelas 1 book
   opens: concrete object, direct question, the term named last.
2. **`parts/grade-8/id/03`, opening** — *Lipatlah selembar kertas menjadi dua
   sebanyak $10$ kali (kalau kamu bisa!): tebalnya berlipat dua setiap kali, dan
   $10$ kali pelipatan mengalikannya dengan $2^{10} = 1024$.* — **native**.
   `berlipat dua` and `pelipatan` are the ordinary words; a translator working
   from *doubles / doublings* would have written `menggandakan` twice.
3. **`parts/grade-9/id/02`, opening** — *Aritmetika mempelajari bilangan bulat
   dan cara bilangan yang satu membagi yang lain. Tokoh utamanya adalah bilangan
   prima, yaitu balok pembangun yang darinya setiap bilangan bulat disusun lewat
   perkalian.* — **native academic**. `Tokoh utamanya` carries *its central
   characters* exactly, and `balok pembangun` is the ordinary Indonesian for
   *building blocks*.
4. **`parts/grade-9/solutions/id/01`, question 9** — *Bukan ``tepat di bawah''
   $1$: $0.999\ldots$ \emph{adalah} bilangan $1$, yang ditulis dengan kostum
   kedua. Bilangan mana pun yang benar-benar di bawah $1$ meninggalkan celah …
   sedangkan tidak ada yang muat di antara $0.999\ldots$ dan $1$.* —
   **native academic**. The rhythm of the English punchline survives without its
   syntax; `kostum kedua` is the idiom, `dalam samaran kedua` would be calque.
5. **`parts/grade-9/solutions/id/08`, Archimedes** — *Faktor $\pi$ dan $r^3$
   saling meniadakan: perbandingannya \emph{semesta} --- benar untuk sebutir
   kelereng dan untuk sebuah planet.* — **native**. `saling meniadakan` is the
   standard Indonesian for *cancel*, and `sebutir kelereng` uses the right
   classifier.
6. **`parts/grade-7/id/05`, Eratosthenes** — *Dua puluh dua abad yang lalu,
   tanpa teleskop, tanpa satelit dan tanpa kalkulator, sang pustakawan
   Aleksandria mengukur Bumi --- dengan sebatang tongkat, sebuah sumur, kafilah
   unta dan matematika bab ini.* — **near-native**. Correct and idiomatic;
   `sang pustakawan` is a slightly literary honorific that an editor might trade
   for a plain `pustakawan`.

No sampled passage reads as post-edited MT — there was no MT.

---

## 7. Gate traps for the next Indonesian agent

1. **`untranslated` is a false-positive class.** Any visible sentence of ≥ 8
   words with none of the gate's ~60 `ID_MARKERS` fires, and ordinary
   Indonesian noun-phrase prose does that constantly. ≈35 fired in grades 7–9
   alone. All were fixed in the prose. **The words whose addition to
   `ID_MARKERS` would remove almost the whole class**: `tetapi`, `namun`,
   `sedangkan`, `tanpa`, `antara`, `menjadi`, `sesudah`, `sebelum`, `seperti`,
   `sampai`, `bahwa`, `masing-masing`, `saling`, `sendiri`, `mengapa`, `berapa`.
   That is a shared-file change and was **reported, not made**.
2. **`not` is an English function word to the gate, and a musical note in
   Indonesian.** Grade-7 ch. 3 (fractions and music) fired ≈35 times on correct
   prose. Written around by using `nada` for every *note*; a `NOT_GATED`
   exception would be better. Reported, not made.
3. **A range that covers `\[` but stops before `\]` duplicates the delimiter.**
   No census sees it; LaTeX does, fatally. Check that every range containing a
   display contains *both* of its delimiters.
4. **A range that starts on a `\begin{exercise}` line deletes it.** Six
   rejections. Start the range on the first line of prose.
5. **Indonesian absorbs numerals into words** — `keenamnya`, `keempat sisinya`,
   `empat-empat`. Only an ordered math-span census sees the deleted span.
6. **`\text{}` inside math is visible text and is *longer* in Indonesian.** Both
   overfull boxes in the whole book were of this shape (§2).
7. **`latexmk` lies.** It memorises the previous run's dependency list. After the
   first `id` file lands, run `latexmk -g` once and confirm with
   `grep -c '/id/' build/…_id.fls`.
8. **Environment optional titles are visible text.** `\begin{proposition}[…]`,
   `\begin{example}[…]`, `\begin{problem}[{…}]`, `\begin{remark}[…]` and
   `\begin{proof}[…]` all print. A patch that replaces only the *body* range of
   an environment leaves its title in English, and until the `title` class
   existed nothing saw it. Always start the replaced range **on the
   `\begin{env}[…]` line itself** when the environment has an optional title.
9. **`di`/`ke` as preposition vs prefix** is the commonest Indonesian spelling
   error and no gate sees it: `di mana`, `di atas`, `ke kanan`, but `ditulis`,
   `dibagi`, `kedua`. Checked by eye in all 142 files.

---

## 8. Reported to the orchestrator (shared files — not changed)

0. **Fixed in revision 2** — the one `title`-class finding,
   `parts/grade-6/id/07-perimeter-area-volume.tex:74`. Note for anyone reusing
   a per-file applier: the `title` class needs the file's **real path** to find
   its English twin, so it cannot run against a scratch probe file. My applier
   now filters that class out of its pre-write check and relies on
   `check_indonesian_prose.py` over the written tree instead.
1. **`tools/check_indonesian_prose.py`**: `not` in the English word list
   collides with Indonesian *not* = musical note (grade-7 ch. 3); and
   `ID_MARKERS` is too small for noun-phrase prose (§7.1, with the proposed
   additions).
2. **English canon, `parts/grade-7/07-triangles-and-angles.tex`,
   `exo:g7:triangles:11`**: "The **three** angles of any quadrilateral $ABCD$"
   — should be *four*. The Indonesian says `Sudut segi empat $ABCD$ mana pun`,
   which is true either way.
3. **English link layer, four wrong-sense links**: `net` in *net change* /
   *net loss* is linked to `def:g5:solids:net` (the net of a solid) in
   `parts/grade-6/solutions/07-perimeter-area-volume.tex`,
   `parts/grade-7/02-negative-numbers.tex` and
   `parts/grade-7/solutions/02-negative-numbers.tex`.
4. **For `indonesian_style_card.md`**: the glossary rulings of §4 above —
   in particular *count/frequency* → `frekuensi` / `frekuensi relatif`,
   *converse* → `konvers`, *median of a triangle* → `garis berat` with
   *centre of gravity* → `titik berat`, and the `bilangan asli` / `bilangan
   semula` collision.
