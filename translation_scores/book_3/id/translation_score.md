# Book 3 — Indonesian (`id`) — translation self-score

| Field | Value |
|---|---|
| **Book** | One Math Book 3 (University Year 1, `bachelor-1`) |
| **Entry** | `one_math_book_3_university_year_1_id.tex` |
| **Language** | Indonesian (`id`), standard Bahasa Indonesia per `indonesian_style_card.md` |
| **Quality bar** | `native academic` — an Indonesian lecturer should hand it to a first-year class without apologising for it |
| **Scope** | 25 chapters + 25 solutions = **50 files** under `parts/bachelor-1/id/` and `parts/bachelor-1/solutions/id/` (32 209 lines) |
| **Kind of pass** | **translation from the English canon**, chapter by chapter, as a line-range patch on top of the English source (§3). No machine translation was used or post-edited at any point. |
| **Delivered** | **50 of 50 files — the book is complete.** |
| **Term config** | `tools/term_config/book3_id.py` (written for this edition; curated, not a translation of `book3_en.py`) |
| **Overall score** | **96 / 100** |
| **Date** | 2026-08-20 (revision 2 — the `title` gate class) |

> **Revision note (2026-08-20, same session).** After the book was accepted at
> 96/100, the coordinator added class **`title`** to
> `tools/check_indonesian_prose.py` — the defect class this edition reported as
> invisible (§2, §10.5). It caught **three** sites my own byte-identity sweep
> had missed, all of them titles that were *partly* translated and therefore not
> byte-identical to English: `[Plane isometries]` (ch. 23) and the two
> `Rank--nullity` titles (ch. 20). All three are fixed — `[Isometri bidang]`,
> `[Rank--nulitas]` — and `nullity` → **`nulitas`** was carried through all 29
> prose occurrences, the `\section{}` and the `\index{}` key, for consistency.
> Gates re-run: prose gate **OK (50 files)** including the new class,
> `check_translation.sh` **PASSED**, link layer unchanged at **4 111** links
> with `--check` green, build **0/0/0, 426 pages**. Score unchanged.

---

## 1. Dimension scores (whole book, 50 files)

| Dimension | Weight | Score | Comment |
|---|---:|---:|---|
| Register (first-year lecture Indonesian) | 25 | 24 | The style card's Sarjana register holds across all 25 chapters: `Misalkan $f$ …`, `Andaikan …`, `Tunjukkan bahwa`, `Simpulkanlah`, `Akibatnya`, `Dengan demikian`, and the connective spine an Indonesian lecturer actually uses — `adapun`, `sedangkan`, `sehingga`, `jadi`, `karena`, `yaitu`/`yakni`. Weekend problems keep the English's narrative voice (Wren weighing the cycloid, Leonardo's rosettes, Legendre and Gauss on least squares) without becoming a calque. Loss: a handful of long English appositive sentences survive as long Indonesian ones (§8). |
| Terminology (standard technical Indonesian) | 20 | 19 | §4 records the whole book's vocabulary against the style card's tables. Every §3 entry that occurs here is followed: `polinomial`, `dapat diturunkan`, `cembung`/`cekung`, `bilangan cacah` for $\N$, `hasil kali dalam`, `bebas linear`, `merentang`/`rentang`, `kernel`/`peta`, `rank`/`trace` (kept English by the §7.3 ruling), `lapangan` for the algebraic field, `variabel` for the algebraic variable (§7.2 ruling — and one request, §10). |
| Freedom from MT artefacts | 20 | 20 | `check_indonesian_prose.py` is **OK on all 50 files** in all six classes: no residual English in prose, TikZ node text, `\text{}` inside math, chapter/section titles, environment optional titles, index keys or solution headers; no split enclitics, no spaced reduplication, no MT spaces inside `$…$`, no split numbers. The text was never machine-translated, so there is nothing to post-edit. |
| Structural fidelity | 15 | 15 | `bash tools/check_translation.sh bachelor-1 id` **PASSED**: completeness, identical label sets and order, `exo:`/`pb:` ↔ `\begin{solution}{}` parity, env/figure census, hygiene checks, gate 8. On top of that the applier enforced eight per-file invariants (§3), including an ordered math-span census and a **per-replaced-range delimiter comparison** that no repository gate performs. |
| Mathematical correctness | 10 | 10 | The mathematics is byte-identical to English by construction (§3): every display, every `pmatrix`, every `\foreach`/`domain=`/`samples=`, every number is the English bytes unless a range was deliberately replaced, and the applier refuses a replacement whose ordered math-span sequence differs. Three deliberate math substitutions only, all of them MT-space removals demanded by the prose gate (§3). |
| Link layer (`\omterm`) | 10 | 10 | **4 111 links across all 50 files**; `--check` green and idempotent; **`\omterm` target set byte-identical to English — 106 / 106** (§5). |
| Build | — | pass | 0 errors, 0 undefined references, **0 overfull boxes**, 426 pages. |

**Weighted total: 96 / 100.** Above the ship bar of `translation_instruction.md`
(complete book at ≥ 95).

---

## 2. Gate results

| Gate | Result |
|---|---|
| `bash tools/check_translation.sh bachelor-1 id` | **PASSED** |
| `python3 tools/check_indonesian_prose.py` on all 50 files | **OK (0 issues)** in all seven classes, including the new `title` class |
| `python3 tools/link_defined_terms.py --book 3 --lang id --check` | **green** — "every file matches what the config generates" |
| `latexmk -g one_math_book_3_university_year_1_id.tex` | **exit 0** |
| `grep -c '^!'` on the log | **0** errors |
| `grep -ci 'undefined'` | **0** undefined references |
| `grep -c 'Overfull'` | **0** |
| Output | `build/one_math_book_3_university_year_1_id.pdf`, **426 pages** |
| `grep -c '/id/' …_id.fls` | **450** — no English body reaches the build (`grep -o 'parts/bachelor-1/[0-9]…'` on the `.fls` returns nothing) |
| `\omterm` target parity vs English | **106 / 106 — identical sets** |
| `sh tools/check_book5_golden.sh` | **green** (no shared rule was touched) |

### Indonesian prose gate

| Class | fired during the pass | final |
|---|---:|---:|
| `english` | ~30 | **0** |
| `untranslated` | ~12 | **0** |
| `math-space` | 2 | **0** |
| `title` (added in revision 2) | 3 | **0** |
| `enclitic` / `redup-space` / `split-number` | 0 | **0** |

The two classes that fire in Indonesian are **`english`** — an environment
optional title (`[Characterization]`, `[Cofactor expansion]`, `[Square Cramer
systems]`), a `\text{ and }` inside a display, a TikZ node, or a stray
connective on a line no replacement range covered — and **`untranslated`**, a
line of ≥ 8 visible words that happens to contain no Indonesian function word.
Both are invisible to every other gate, because this edition is written in the
same alphabet as the source.

**Environment optional titles were the sharpest of these, and are now a gate
class.** The gate's English word list is curated, so `[Characterization]` and
`[Properties]` sailed past it. After the gate was first green I ran a separate
structural sweep — *every* `\begin{env}[title]` and `\section{…}` in the `id`
tree compared against its English twin, flagging any that were byte-identical —
and it found five more untranslated titles (chapters 3, 6, 22) that no gate
would have shown.

**That sweep was not enough, and the difference is worth recording.** Byte
identity misses a title that is *partly* translated: `[Rank--nullity dalam
kerja: operator selisihnya]` is not byte-identical to its English twin, so my
sweep passed it, and `[Plane isometries]` survived because the sweep ran before
that chapter's last edit. The coordinator's `title` class compares against the
English twin *and* flags any surviving English-looking word, which is the
correct test; it caught all three. Legitimately identical titles
(`[Gram--Schmidt]`, `[Bolzano--Weierstrass]`, `[Rolle]`, `[Ring]`) survive it
because, once math and macros are stripped, they contain no English-looking
word.

---

## 3. Method, and the tooling the next agent should reuse

The pass is a **line-range patch applied on top of the English canon**. For
every chapter a patch names the English source and gives the Indonesian
replacement for each line range:

```text
### parts/bachelor-1/id/21-matrices.tex <<< parts/bachelor-1/21-matrices.tex
@@ 1
\chapter{Matriks}\label{ch:b1:matrices}
@@ 3-9
Sebuah matriks adalah pemetaan linear yang ditulis dalam koordinat. …
```

Every English line **not** named is copied byte-identically, so labels, `\cref`
targets, `\begin{solution}{key}`, `\foreach` lists, `domain=`, `samples=` and
every math display are physically the same bytes as English and cannot drift.

The applier (`id_apply.py`, in the session scratchpad) **refuses to write a
file** unless every structural marker survives. Errors it caught across the 50
files:

| Invariant | Errors it caught |
|---|---:|
| ordered `\begin{env}` / `\end{env}` and `\label{…}` sequence | ~25 — a range that swallowed an `\end{example}` or a `\begin{exercise}…\label{}` line |
| ordered `\begin{solution}{key}` sequence | 0 |
| **ordered math-span sequence, after blanking `\text{…}`** | ~10 — Indonesian's head-modifier order wants to move a symbol past its noun (`untaian $\{0,2\}$ berpanjang $n$` for *strings of length $n$ over $\{0,2\}$`) |
| ordered `\emph{}`/`\emph{}\index{}` signature | 4 — a dropped emphasis, or an enclitic accidentally placed between `\emph` and `\index` |
| ordered tikz/axis bodies, after blanking node text and axis labels | 0 |
| `\index{}` count, brace-balance drift relative to English | 0 |
| `\omterm` survivors (the link layer is generated later) | 0 |
| **per-replaced-range `\[` / `\]` / `align*` delimiter comparison** | **3** — ranges that covered `\[` but stopped before `\]` (chapters 21, 22, 23) |

The **delimiter comparison is the invariant the coordinator asked for, and it
paid three times.** A whole-file census cannot see it: the counts still
balance, the env/label/math censuses are happy, the prose gate sees nothing,
and the build dies on `Bad math environment delimiter`. Comparing the count of
each delimiter inside *each replaced range* (EN vs ID) catches it before the
file is ever written. My first version of the check — "reject any range whose
start or end falls inside a display" — was too strict and rejected legitimate
replacements of lines strictly *inside* a display; the count comparison is the
correct form.

The **math-span check remains the single most valuable invariant**, exactly as
the Arabic agent reported. Indonesian wants to reorder `$n$ ganjil $>
\frac1\varepsilon$` into `$n > \frac1\varepsilon$ yang ganjil`, which is better
Indonesian and silently different mathematics unless the census refuses it.

Two further scratchpad tools, both worth reusing:

* `census.py` — runs the same eight censuses over **every** `id` file against
  its English twin, so a *direct* edit (a global terminology sweep, a
  hand-fixed line) is validated too, not only a patch. It ends the pass at
  exactly three declared math divergences plus two MT-space removals (below).
* `diag.py` — a per-range diff of env / emph / label / index / `\[` / `\]`
  counts between the English slice and the replacement. It turns "census
  failed, first divergence #284" into "range `@@ 660-666` is one line short" in
  one command.

**Declared math divergences (five, all intentional):** three `!mathsub`
declarations that translate an `\emph{}` inside a display (ch. 15) or restore a
missing operand (ch. 11, solutions ch. 9), and two removals of an MT space
inside inline math that English carries and the Indonesian prose gate refuses —
`$\det = 0 = $` (ch. 22) and `$p = uC_1 + vC_2 = $` (ch. 25).

---

## 4. Terminology decisions worth recording

Everything here follows `indonesian_style_card.md` §3. The entries below are
the ones that were **decided during this pass** or that a later agent may be
tempted to write differently:

| English | Indonesian used | Note |
|---|---|---|
| variable (algebraic) | **variabel** | Style card §7.2 ruling. This book is analysis-heavy and `peubah` is what an Indonesian analysis lecture says (`fungsi dua peubah`); 49 occurrences were converted to `variabel` for series consistency. **Raised as request 1 (§10), not diverged.** |
| natural numbers ($\N$, from 0) | **bilangan cacah** | Coordinator ruling, applied throughout. |
| polynomial | **polinomial** | never `polinom`, never `suku banyak`. |
| differentiable / differentiability | **dapat diturunkan** / **sifat dapat diturunkan** | never `terdiferensialkan`. |
| convex / concave | **cembung** / **cekung** | never `konveks`/`konkaf`. |
| rank, trace | **rank**, **trace** | style card §7.3 — kept English deliberately. |
| nullity (rank–nullity theorem) | **nulitas** | `rank` stays English by the §7.3 ruling, `nullity` does not: `teorema rank--nulitas`, in all 29 prose occurrences, the `\section{}` and the `\index{}` key. |
| field (algebraic) | **lapangan** | never `medan`, never `bidang`; `bidang` is the geometric plane of ch. 24–25. |
| map (n.) / image | **pemetaan** / **peta** | `peta` is reserved for the image; the map is always `pemetaan`. |
| alternating (form, polynomial) | **berselang-seling** | the same word the series uses for alternating series. |
| conic section | **irisan kerucut** | with `elips`, `parabola`, `hiperbola`, `fokus`, `direktriks`, `eksentrisitas`. |
| cusp | **titik runcing** | new to the series (ch. 24, and the cycloid problem). `kuspa` was rejected as not lecture Indonesian. |
| chord | **tali busur** | style card §3 geometry; `talibusur` (12×) was corrected to the spaced form. |
| parallelogram | **jajargenjang** | solid, not `jajaran genjang`. |
| ray | **sinar garis** | style card §3; the bare `sinar` (21×) was expanded. |
| pivot / echelon | **poros** / **eselon** | Gaussian elimination is `penghapusan Gauss`. |
| variance / covariance | **varians** / **kovarians** | `ragam` is reserved for the probabilistic variance of the school books and is used here only for *variations* of a curve. |
| residual, outlier, weighted | **sisaan**, **pencilan**, **terbobot** | least-squares vocabulary, ch. 25. |
| tautochrone, brachistochrone, trochoid | **tautokron**, **brakistokron**, **trokoid** | ch. 24 weekend problem. |
| glide reflection, dihedral group | **pencerminan geser**, **grup dihedral** | ch. 23 weekend problem. |
| barycentre | **barisentrum** | kept distinct from `titik berat`, which the style card reserves for a triangle's centroid. |
| countable | **terbilang** | already the book's word (113 occurrences) before the coordinator's ruling arrived. |
| nondecreasing | **tidak turun** | `tak turun` (11×) was corrected. |
| sign of a permutation | **tanda permutasi** | ch. 22. |
| quotient | **hasil bagi** | correct here: Book 3 has no quotient set/ring/group — every quotient in it is arithmetic or a quotient of polynomials. `kuosien` is therefore unused in this book. |

---

## 5. The link layer

`tools/term_config/book3_id.py` was written for this edition. It is a curation,
not a translation of `book3_en.py`.

| Quantity | Value |
|---|---:|
| terms harvested | 128 |
| dropped (defined twice) | 2 |
| dropped (stoplist) | 8 |
| linkable terms after morphology | 184 |
| **links inserted** | **4 111 across 50 files** (English: 3 944) |
| by target | `def` 3 438, `prop` 233, `thm` 223, `pb` 139, `ex` 46, `met` 17, `cor` 15 |
| **target-set parity vs English** | **106 / 106 — identical** |

**What the parity diff cost, and what it bought.** The first generation was 4
319 links with **eight extra targets and one missing** — and the diff is the
only thing that shows it:

* `def:b1:complex:expi` (+69) — `argumen` is *the reasoning* far more often
  than the argument of a complex number, exactly as English's `argument`.
  `DROP`ped, as `book3_en.py` does.
* `pb:b1:arith:1`, `pb:b1:complex:1`, `pb:b1:continuity:1`,
  `prop:b1:logic:rules` — result-names (`teorema Kummer`, `rumus Legendre`,
  `ketaksamaan Ptolemeus`, `persamaan fungsional Cauchy`, `hukum De Morgan`)
  that reach the harvester through `\emph{…}\index{…}` and therefore **bypass
  `NOT_A_TERM`**. Hand-`DROP`ped, exactly as English hand-drops the same five.
* `pb:b1:counting:1` (+23) — **a language-shape divergence, not an error.**
  English's *derangement* is one word, so the index-only harvest (which
  requires a space) skips it; Indonesian's `permutasi kacau` is two words and
  is picked up. Dropped for parity.
* `ex:b1:series:oddtelescope` (+6) / `pb:b1:series:1` (−5) — the same
  mis-target English documents in its own `EXTRA`: `\index{konstanta Euler}`
  sits in exercise 12, *before* the weekend problem that defines $\gamma$.
  Fixed the same way, by `EXTRA`.
* `thm:b1:matrices:conjugation` (+6) — `serupa` is the everyday *similar*;
  English links neither `similar` nor `similar matrices`.
* `thm:b1:reals:archimedes` (**missing**) and `pb:b1:findim:1` (**missing after
  round 2**) — both casualties of `NOT_A_TERM`. `sifat` and `hukum` are heads of
  Indonesian result-names (`sifat distributif`, `hukum De Morgan`) and must be
  filtered, but they also head the book's two genuine `sifat X` / `hukum X`
  **terms**: `sifat Archimedes` and `hukum menara` (the tower law). Declared in
  `EXTRA`. **This is the Indonesian shape of the trap: the result-name filter
  is a substring match, so a term whose head is a result-name word is
  unreachable and must be declared by hand.**

**Wrong-sense links the parity diff does *not* show, found by reading counts.**
Target parity was reached at 4 137 links, 193 more than English. Comparing
*per-target counts* found four families of over-linking, each a homograph the
style card §4 predicts or a near neighbour of one:

| Display | Target | Links | Fix |
|---|---|---:|---|
| `hingga` | `def:b1:counting:card` | 166 | `STOP` — it is `berdimensi hingga`, `jumlah hingga`, `sampai/hingga` far more often than the finite *set*. English `STOP`s `finite` for the same reason. |
| `langsung` | `def:b1:vspaces:sum` | 47 | `DROP` — `perhitungan langsung`, `secara langsung`. `jumlah langsung` keeps the target; `pelengkap` and `saling melengkapi` were added to `EXTRA` to restore English's `supplementary` links. |
| `urutan` | `def:b1:logic:order` | 42 | `STOP` — the everyday *sequence/order of things*. |
| `kutub` | `def:b1:fractions:field` | 13 | `STOP` — the **pole** of ch. 9 collides head-on with the **polar** of ch. 3/24/25 (`kurva kutub`, `koordinat kutub`, `bentuk kutub`). `STOP` is soft, so ch. 9 keeps all 42 of its links and the polar chapters lose 13 wrong ones. |
| `transenden`, `kritis`, `simetri` | 3 targets | 25 | `DROP` — bare adjectives; `titik kritis` and `proyeksi` carry the links. |
| `penutupnya` | `def:b1:topology:closure` | 25 | `EXTRA_PROTECT` — the solutions' recurring `Inti gagasan penutupnya` is English's *The closing insight*, not the topological closure. |
| `rentang` | `def:b1:vspaces:span` | 1 | reworded to `jangkauan` — `di luar rentang itu` (outside that **range**, ch. 24) is not the linear span. |

That is **~320 wrong-sense links removed after target parity was already
reached.** Target parity is necessary and not sufficient; the per-target *count*
diff is the second half of the job.

`EXTRA` also carries the two declarations English needs and Indonesian needs for
the same reason: the definitions emphasise a compound (`\emph{kontinu di $x_0
\in I$}`, `\emph{dapat diturunkan di $x_0 \in I$}`), so the bare adjective — the
form the other 24 chapters use — is never harvested. Adding `kontinu` and
`dapat diturunkan` restored 161 and 41 links respectively.

### Rules 5 and 6 of §4b, audited

* **Adjacency (rule 5).** The applier's `\emph` census records, for every
  `\emph{}`, whether an `\index{}` follows it immediately; a translation that
  breaks the pair fails the census before the file is written. So the pass is
  structurally immune to `\emph{selubung}nya\index{selubung}`. Where Indonesian
  wanted the enclitic, it was written **after** the `\index`
  (`\emph{rentang}\index{rentang}nya`), which keeps the pair adjacent and the
  display bare.
* **Capitalised / `-nya` displays (rules 1–3).** A separate audit of all 102
  `\emph{…}\index{…}` pairs found **17** defective displays — 12 capitalised
  (`Grup`, `Ring`, `Polinomial`, `Pecahan rasional`, `Rank`, `Panjang`,
  `Turunan parsial`, …) and 5 with `-nya` (`gradiennya`, `rentangnya`,
  `lantainya`, `polinomial karakteristiknya`, `operasi baris elementernya`).
  Every one was reworded (`Sebuah \emph{grup}…`, `Adapun \emph{rank}…`) so the
  registered display is the bare lower-case noun the book actually uses.
* **Duplicate `\index{}` keys (rule 6).** Audited across all 50 files:
  **none**. The two `rank` definitions are already keyed apart by the English
  (`rank!keluarga` vs `rank!pemetaan linear`).

---

## 6. Sampled passages, judged

1. **`parts/bachelor-1/id/23`, opening** — *Menambahkan hasil kali dalam pada
   ruang vektor real membeli gagasan geometrinya --- panjang, sudut,
   keortogonalan, jarak --- dan satu teorema yang menjulang di atas bab ini:
   bahwa setiap subruang mempunyai proyeksi ortogonal …* — **native academic**.
   `membeli` keeps the English's commercial metaphor, `menjulang di atas bab
   ini` is the ordinary Indonesian for *towers over the chapter*, and the
   `bahwa`-clause is how a lecturer announces a theorem.
2. **`parts/bachelor-1/id/25`, opening** — *Tahun ini berakhir dengan langkah
   pertama ke dimensi yang lebih tinggi … Segalanya terampat --- limit,
   kekontinuan, turunan, ekstremum --- tetapi setiap gagasannya memperoleh
   puntiran: karena limitnya dapat didekati sepanjang setiap arah sekaligus …*
   — **native academic**. `terampat` (generalises) and `memperoleh puntiran`
   (gains a twist) are idiomatic; the `karena …` clause carries the English's
   colon-plus-explanation rhythm without its syntax.
3. **`parts/bachelor-1/id/24`, the cycloid problem** — *Abad ketujuh belas
   bertengkar atas kurva ini --- Galileo menimbang guntingan kertasnya, Wren
   mengukurnya, Roberval menghitung luasnya, Huygens membangun jam di atasnya
   --- dan setiap hasil mereka terjangkau bab ini.* — **native**. The
   four-verb parallel survives intact, and `terjangkau bab ini` says *within
   reach of this chapter* in three words.
4. **`parts/bachelor-1/id/21`, the trace** — *sehingga semua matriks yang
   serupa dengan $A$ berbagi tracenya --- yaitu invarian numerik yang pertama
   bagi sebuah endomorfisma, yang akan disusul oleh determinan pada …* —
   **native academic**. `berbagi` for *share*, `disusul oleh` for *joined by*.
5. **`parts/bachelor-1/solutions/id/22`, alternating polynomials** — *Jika $x_i
   = x_j$, maka penukaran kedua variabelnya menetapkan titiknya tetapi mesti
   mengubah tanda $F$: jadi $F = -F$, sehingga $F = 0$ di situ.* —
   **native academic**. This is how the argument is written at an Indonesian
   board: `menetapkan` for *fixes*, `mesti` for the forced consequence.
6. **`parts/bachelor-1/id/22`, the pitfalls remark** — *Determinan nol itu
   awalnya, bukan akhirnya: karena ia mengatakan ``rank $< n$'' tetapi bukan
   rank yang mana …* — **near-native**. Correct and idiomatic, but `awalnya,
   bukan akhirnya` is a compressed rendering of *the beginning, not the end*; an
   editor might expand it to `itu permulaan, bukan kesimpulan`.

No sampled passage reads as post-edited MT — there was no MT.

---

## 7. Gate traps for the next Indonesian agent

1. **Environment optional titles — now covered by gate class `title`, so
   trust the gate, not a byte-identity sweep.** `[Characterization]`,
   `[Properties]`, `[Cofactor expansion]`, `[Vandermonde determinant]`,
   `[Square Cramer systems]`, `[Linearization]`, `[Invertibility mod $n$]` all
   passed gate 8 before the class existed. A hand-rolled byte-identity sweep is
   *not* equivalent: it misses the half-translated title
   (`[Rank--nullity dalam kerja: …]`), which is exactly the shape that survives
   longest, because it looks translated at a glance.
2. **`\text{…}` inside displays.** `\text{ and }`, `\text{otherwise}`,
   `\text{axis }`, `\text{trigonometric polynomial in }`, `\text{ellipse: }`
   are visible text and must be translated — and the math-span census blanks
   `\text{…}`, so **no `!mathsub` is needed**; declaring one is an error the
   applier will (correctly) reject.
3. **English carries MT spaces the Indonesian gate refuses.** `$\det = 0 = $`
   and `$p = uC_1 + vC_2 = $` exist in the English canon. They must be
   declared as `!mathsub` and reported, not silently kept.
4. **Every replaced line of ≥ 8 visible words needs an `ID_MARKER`.** The gate
   splits on `[.!?;:\n]+`, so chunks are line-bounded: a perfectly Indonesian
   sentence can still trip `untranslated` because the *line* it wraps onto
   contains only content words. The cheapest fix is to move a `jadi`, `yang`,
   `karena`, `adapun` or `yaitu` onto that line.
5. **The delimiter trap fires on the last line of a range.** All three of mine
   were a range that ended one line *before* the `\[` (or `\]`) that belonged
   to it. Compare delimiter counts per range, EN vs ID.

---

## 8. Why not 100

* **Register 24/25.** English's long appositive sentences — a clause, an em-dash
  aside, a colon and a second clause — survive as long Indonesian sentences in
  the "perspectives" and "where this goes" remarks. They are correct and they
  read as lecture prose, but an Indonesian editor would break perhaps one in
  five into two sentences.
* **Terminology 19/20.** Three choices are defensible but not the only
  defensible ones, and all three are recorded so the series can overrule them:
  `titik runcing` for *cusp* (new to the series), `barisentrum` for
  *barycentre* (against the style card's `titik berat`, which it reserves for a
  triangle's centroid), and `variabel` over `peubah` in an analysis book
  (§7.2 — the style card's own open question, raised as request 1).
* **Nothing else is outstanding.** All gates are zero, the build is clean, the
  `\omterm` target set is byte-identical to English, and no passage reads as
  machine translation.

---

## 9. State

| Files | State |
|---|---|
| `parts/bachelor-1/id/*.tex` (25) | **delivered**, gates green, links generated |
| `parts/bachelor-1/solutions/id/*.tex` (25) | **delivered**, gates green, links generated |
| `tools/term_config/book3_id.py` | **new**, curated, `--check` green |
| `build/one_math_book_3_university_year_1_id.pdf` | 426 pages, clean log |
| Shared infrastructure | **untouched** — `check_book5_golden.sh` still green |

---

## 10. Requests to the orchestrator

1. **`peubah` vs `variabel` in the university analysis books — decide as a
   series (style card §7.2).** This book was written with `peubah` and
   converted to `variabel` to obey the ruling; the conversion is complete and
   consistent. But `fungsi dua peubah`, `perubahan peubah` and `peubah bebas`
   are what an Indonesian analysis lecture says, and the style card itself
   flags the question as open for Books 3–5. If the ruling stands, please
   strike the "Books 3–5 may find `peubah` more natural" sentence from §7.2 so
   it is not reopened; if it is revised, the change here is one `sed`.
2. **Promote these into `indonesian_style_card.md` §3 so Books 4 and 5 do not
   re-decide them:** *cusp* = **titik runcing**; *conic section* = **irisan
   kerucut**; *chord* = **tali busur** (spaced); *parallelogram* =
   **jajargenjang** (solid); *pivot* = **poros**, *echelon* = **eselon**,
   *Gaussian elimination* = **penghapusan Gauss**; *alternating* (form,
   polynomial, series) = **berselang-seling**; *variance/covariance* =
   **varians**/**kovarians** in the analysis books, with `ragam` left to the
   probability chapters; *residual* = **sisaan**, *outlier* = **pencilan**,
   *weighted* = **terbobot**; *glide reflection* = **pencerminan geser**;
   *tautochrone/brachistochrone* = **tautokron**/**brakistokron**.
   And one collision to record next to `medan`/`lapangan`: **`kutub` is the
   pole of a rational fraction *and* the polar of a curve** — it must be
   stoplisted in any book that contains both.
3. **Add rule 7 to §4b: a term whose head word is in `NOT_A_TERM` is
   unreachable and must be declared in `EXTRA`.** `sifat Archimedes` and
   `hukum menara` are the Book 3 instances; every Indonesian book will have
   some, because Indonesian names its results `sifat X` / `hukum X` / `kaidah
   X` with the same nouns that head genuine terms.
4. **Add rule 8 to §4b: reach target parity, then diff per-target *counts*.**
   Target-set parity was reached with ~320 wrong-sense links still in the tree
   (`hingga` 166, `langsung` 47, `urutan` 42, `kutub` 13, `penutupnya` 25, …).
   The count diff against English is what exposes them, and it costs one
   command.
5. ~~**Consider a `title` class in `check_indonesian_prose.py`**~~ —
   **done, revision 2.** Implemented by the coordinator as class `title` plus an
   `ENGLISH_SUFFIX_CAP` rule for Title-Case single words. It immediately caught
   three sites in this book that a byte-identity sweep had missed. Nothing
   further is requested.
