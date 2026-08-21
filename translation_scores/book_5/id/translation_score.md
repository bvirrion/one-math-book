# Book 5 — Indonesian (`id`) — translation self-score

| Field | Value |
|---|---|
| **Book** | One Math Book 5 (University Year 3) |
| **Entry** | `one_math_book_5_university_year_3_id.tex` |
| **Language** | Indonesian (`id`), per `indonesian_style_card.md` — variety “modern lecture practice”, Sarjana 1–3 lecture register |
| **Quality bar** | `native academic` — an Indonesian-medium lecturer should set it as the course text without apologising for it |
| **Scope** | 23 chapters + 23 solutions = **46 files** under `parts/bachelor-3/id/` and `parts/bachelor-3/solutions/id/` (~217 000 words) |
| **Kind of pass** | **translation from the English canon**, chapter by chapter, as a line-range patch on top of the English source. No machine translation was used or post-edited at any point. |
| **Delivered** | **46 of 46 files — the book is complete.** |
| **Term config** | `tools/term_config/book5_id.py` (curated; not a translation of `book5_en.py`) |
| **Overall score** | **96 / 100** |
| **Date** | 2026-08-20 |

> **Book 5 is the frozen book.** `tools/check_book5_golden.sh` holds the whole
> linker to the *English* Book 5 link layer as a byte-identical fixture.
> Nothing in this pass touched `parts/bachelor-3/*.tex` or `tools/termlink/`;
> the golden check was run before the first patch and after the last edit and
> is green in both.

---

## 1. Dimension scores (whole book, 46 files)

| Dimension | Weight | Score | Comment |
|---|---:|---:|---|
| Register (Sarjana 1–3 lecture voice) | 25 | 24 | The book keeps one voice from `Teori Grup` to `Teorema Limit Pusat`: definitions open impersonally (`Misalkan $U \subseteq \R^n$ terbuka.`, `Yang disebut \emph{turunan eksterior} adalah…`), proofs move on connectives that carry logical weight rather than filling space (`sebab`, `sehingga`, `sedangkan`, `padahal`, `jadi`, `menurut`), exercises use the `-lah` imperative (`Tunjukkanlah`, `Simpulkanlah`, `Periksalah`), and the weekend problems keep the English’s narrative register (`kiat sabuk`, `mesin tik`, `bola berbulu`, `setiap angin di Bumi menyisakan satu titik tenang`). Loss: a handful of long displays are followed by lead-ins that read a shade more written than a lecturer would say them aloud. |
| Terminology (standard technical Indonesian) | 20 | 19 | §4 records the vocabulary. The style card’s core rulings are honoured throughout — `ring` (not *gelanggang*), `lapangan` for the algebraic field against `medan` for a vector field, `distribusi` (not *sebaran*), `nilai harapan` never bare *harapan*, `bilangan cacah` for $\N$, `konvers` for the converse against `kebalikan` for the multiplicative inverse, `kuosien` for the quotient ring/group, `terbilang` for countable, `variabel` everywhere except the fixed `peubah acak`, and `rank`/`trace` kept English. Loss: `sekawan` had to carry both *associate* (ch. 2) and *conjugate* (chs. 12, 14, 16, 18, 19) — a homograph English does not have, handled in the config rather than in the prose (§5). |
| Freedom from MT artefacts | 20 | 20 | `check_indonesian_prose.py` is **0 in all seven classes on all 46 files**: no residual English in prose, TikZ node text, `\text{}` inside math, `\index{}` keys, `\chapter`/`\section` arguments or environment optional titles (the new `title` class, compared against the English twin); no `math-space`, `redup-space`, `enclitic` or `split-number` findings. Nothing was machine-translated, so there is nothing to post-edit. |
| Structural fidelity | 15 | 15 | `check_translation.sh bachelor-3 id` **PASSED**: identical label sets and order, `exo:`/`pb:` ↔ `\begin{solution}{}` parity, environment and figure census, `\end{…>` typo class, drafty `...`, duplicate labels, UTF-8 with no TeX accent escapes. On top of that the applier enforced seven per-file invariants (§3), including an ordered math-span census and a per-range display-delimiter balance that no repository gate performs. |
| Mathematical correctness | 10 | 10 | The mathematics is byte-identical to English by construction (§3): every display, every `\foreach` list, every `xtick=`, every number is the English bytes unless a range was deliberately replaced, and the applier refuses a replacement whose ordered math-span sequence differs from the English twin’s. Digits are ASCII and the decimal separator is a point everywhere, in prose and in math. |
| Link layer (`\omterm`) | 10 | 8 | Config curated from scratch; `--check` green and idempotent; **4 257 links across 46 files**; **target parity 130 / 130** — every English target is reached. Loss: the per-target *counts* still diverge by more than ten on 17 of 130 targets (§5), all of them explained, four of them deliberate Indonesian-only homograph defences. |
| Build | — | pass | 0 errors, 0 undefined references, **0 overfull boxes**, 435 pages. |

**Weighted total: 96 / 100.** Above the ship bar of `translation_instruction.md`
(complete book at ≥ 95).

---

## 2. Gate results

| Gate | Result |
|---|---|
| `sh tools/check_book5_golden.sh` (before and after) | **green** — “every file matches what the config generates” |
| `bash tools/check_translation.sh bachelor-3 id` | **TRANSLATION GATE: PASSED** |
| `python3 tools/check_indonesian_prose.py parts/bachelor-3/id parts/bachelor-3/solutions/id` | **OK (46 files)**, 0 in all seven classes |
| `python3 tools/link_defined_terms.py --book 5 --lang id --check` | **green**, and idempotent (`links to insert: 0`) |
| `latexmk one_math_book_5_university_year_3_id.tex` | **exit 0** |
| `grep -c '^!'` on the log | **0** errors |
| `grep -ci 'undefined'` | **0** undefined references |
| `grep -c 'Overfull'` | **0** |
| `grep -c '/id/' …_id.fls` after `latexmk -g` | **414** (all 46 Indonesian files really compiled; no English fallback) |
| Output | `build/one_math_book_5_university_year_3_id.pdf`, **435 pages** |

### Indonesian prose gate, by class

| Class | Findings |
|---|---:|
| `english` | 0 |
| `title` | 0 |
| `untranslated` | 0 |
| `math-space` | 0 |
| `redup-space` | 0 |
| `enclitic` | 0 |
| `split-number` | 0 |

---

## 3. Method

The pass followed §3 of `translation_scores/book_1/ar/translation_score.md`:
translate **from the English canon**, chapter by chapter, as a **line-range
patch** applied by a scratch script that copies every English line not
explicitly replaced **byte-identically**. The applier refuses to write a file
unless all of the following survive as *ordered* censuses against the English
twin:

1. `\begin{env}` / `\end{env}` sequence;
2. `\label{…}` sequence;
3. `\begin{solution}{key}` sequence;
4. `\cref`/`\ref` target sequence;
5. **math-span sequence** after blanking `\text{…}` and normalising whitespace —
   the highest-value invariant, and the one that caught most of the errors;
6. `tikzpicture`/`axis` bodies after blanking node text and axis labels;
7. **per-replaced-range display-delimiter balance** (`\[`/`\]`, `equation`,
   `align`, …): a range that covers `\[` but stops before `\]` duplicates the
   delimiter, every other census stays balanced, and the build dies on
   *Bad math environment delimiter*. This book is the display-heaviest of the
   five and the guard fired repeatedly.

The applier also ran the repository’s own Indonesian prose gate over the
candidate text before writing, and converted TeX accent escapes (`\'e`,
``\`a``, `\"o`) to UTF-8 so gate 6 stays clean.

Everything a reader sees is Indonesian: TikZ `node {…}` text, `xlabel=` /
`ylabel=` / `title=`, `\text{…}` inside math, environment optional titles,
`\chapter` / `\section`, `\index{}` keys. Nothing a machine reads was touched:
`\label{}`, `\cref` targets, `\begin{solution}{key}` and the first argument of
`\omterm{}{}` are the English bytes.

---

## 4. Terminology decisions worth recording

Beyond the style card, this volume needed rulings the earlier books did not.

**Algebra (chs. 1–5).** `grup kuosien` / `ring kuosien` / `modul kuosien` /
`topologi kuosien` (never *hasil bagi*, which is reserved for the quotient of a
division and for the Rayleigh quotient); `lapangan pemecah` (splitting field),
`lapangan tetap` (fixed field), `unsur sekawan` (associate), `unsur tak
tereduksi`, `DIU` / `DFT` (PID / UFD), `kandungan` (content), `tanda
permutasi`, `rank` and `trace` kept English.

**Topology and analysis (chs. 6–15).** `persekitaran`, `kompak`, `terhubung
lintasan`, `kurus` (meagre), `ukuran` / `terukur`, `hampir di mana-mana`,
`berhingga-$\sigma$`, `kue berlapis` (layer cake), `konvolusi`, `pemulus`
(mollifier), `sup esensial`, `mesin tik` (the typewriter sequence),
`swa-adjoin`, `alternatif Fredholm`, `hampiran rank berhingga`.

**Complex analysis and geometry (chs. 16–21).** `holomorfik`, `residu`,
`kutub`, `utuh` (entire), `anulus`, `kesingularan terhapuskan` / `hakiki`,
`konformal`, `univalen`, `teorema seperempat Koebe`, `kesesatan` (distortion),
`submanifold`, `ruang singgung`, `pengali Lagrange`, `kuaternion`, `selimut
ganda`, `kiat sabuk` (the belt trick), `bentuk diferensial`, `hasil kali
eksterior`, `turunan eksterior`, `tarikan balik` (pullback), `partisi
kesatuan`, `normal-keluar-dulu`, `bilangan lilitan`, `bentuk berselang-seling`.

**Probability (chs. 22–23).** `ruang peluang`, `kejadian`, `peubah acak` (the
one place `peubah` survives), `distribusi`, `fungsi distribusi`, `kepadatan`,
`nilai harapan`, `varians`, `hampir pasti` glossed once as `h.p.` and used as
such thereafter (English writes `a.s.`), `i.i.d.` kept, `hukum bilangan besar`,
`$\sigma$-aljabar ekor`, `hukum nol--satu`, `fungsi karakteristik`,
`keketatan` (tightness), `teorema limit pusat`, `vektor Gauss`, `matriks
kovarians`, `selang kepercayaan`, `metode penggantian` (Lindeberg’s
replacement method), `variasi total`, `penggandengan` (coupling), `metode
delta`, `kemencengan` (skew).

**Two consistency sweeps run at the end of the pass**, both worth promoting
into the style card:

* **`kepadatan`, not `kerapatan`, for *density***, in both the measure-theoretic
  and the probabilistic sense. The tree had drifted (27 vs 38) because
  chs. 9–14 were written before chs. 22–23; the Radon–Nikodym density and the
  probability density are the same object and must read the same.
* **`trace` and `rank` are English words in Indonesian mathematical prose.**
  The tree had `jejak` for *trace* in chs. 15, 17 and 20, which collides with
  `jejak` = the trace/track of a path (kept, once, in
  `jejak analitis selimut gandanya`), and `berperingkat berhingga` for
  *finite-rank*, which collides with `peringkat` = an ordinary ranking (kept
  for “at rank $n$” in chs. 6 and 10, and for the rank of $X_n$ among its
  predecessors in ch. 22).

---

## 5. Link layer

| Measure | English | Indonesian |
|---|---:|---:|
| Terms harvested | — | 183 |
| Dropped (defined twice) | — | 5 |
| Dropped (stoplist) | — | 25 |
| **Linkable terms** | 284 | **270** |
| **Links inserted** | 4 326 | **4 257** |
| Files touched | 46 | 46 |
| **Distinct targets** | 130 | **133** |
| **Target parity** | — | **130 / 130 English targets reached** |

`AMBIG_POLICY = "drop"`, the university convention. The config carries its own
`NOT_A_TERM` (`teorema`, `lema`, `akibat`, `ketaksamaan`, `rumus`, `kaidah`,
`aturan`, `asas`, `identitas`, `paradoks`, `kriteria`, `sifat`, `prinsip`,
`soal`, `masalah`, `hukum`), the style card’s homograph stoplist **in both
cases and in their `-nya` forms**, and `EXTRA_PROTECT` for `bagi` as a
preposition, `kali` as an occasion, `titik` as a decimal point and `ukuran` as
plain size.

Three targets English reaches through a head word that Indonesian puts inside
`NOT_A_TERM` are restored by hand (style-card rule 7):

```
"hukum menara"                -> thm:b3:galois:tower
"hukum nol--satu"             -> thm:b3:probability:zeroone
"keteraturan ukuran Lebesgue" -> thm:b3:measure:regularity   # "aturan" is a
                                                             # substring of it
```

One term is force-dropped: `penggaris dan jangka`, because English never links
*ruler and compass* either.

### Per-target count divergences (> 10), and why

Target parity is necessary but not sufficient, so the per-target counts were
diffed against English. Seventeen of 130 targets differ by more than ten:

| Target | EN | ID | Δ | Explanation |
|---|---:|---:|---:|---|
| `def:b3:galois:algebraic` | 72 | 30 | −42 | `aljabar` is the *branch* (aljabar linear, $\sigma$-aljabar, aljabar Borel) far more often than the adjective *algebraic*; stoplisted, so it links only in ch. 4. Deliberate. |
| `ex:b3:groups:actions` | 81 | 39 | −42 | `pusat` is the centre of a group **and** the ordinary “central”; `teorema limit pusat` alone would have taken 30 wrong links. Deliberate. |
| `def:b3:probability:independence` | 147 | 112 | −35 | Indonesian writes `bebas` for both *independent* and *free* (modul bebas); stoplisted, so it links inside ch. 3 and ch. 22 only. Deliberate. |
| `def:b3:measure:measure` | 142 | 110 | −32 | `ukuran` is also plain *size*; protected in `ukuran cuplikan`, `ukuran abjad`, … |
| `def:b3:galois:extension` | 54 | 24 | −30 | English links bare *degree*; Indonesian `derajat` is stoplisted (derajat polinomial, derajat kebebasan, derajat $120^\circ$). |
| `def:b3:topology:topology` | 164 | 191 | +27 | `persekitaran` is a single word where English alternates *neighborhood* / *neighbourhood* / *nbhd*; correct sense throughout. |
| `def:b3:rings:divisibility` | 124 | 144 | +20 | `tak tereduksi` covers both *irreducible* and *irreducibles*; correct sense. |
| `thm:b3:groups:quotient` | 2 | 17 | +15 | Indonesian names the object (`grup kuosien`) where English often writes just “the quotient”; correct sense. |
| `def:b3:topology:pathconnected` | 54 | 69 | +15 | `lintasan` also renders *trajectory* in ch. 19; same definition, so the sense is right. |
| `def:b3:modules:free` | 38 | 52 | +14 | `bebas` inside ch. 3 (see above); one occurrence in 30 is *linearly independent*. |
| `def:b3:rings:ideal` | 61 | 74 | +13 | `ideal` is invariant in Indonesian where English has *ideal* / *ideals*. |
| `def:b3:clt:gaussianvector` | 69 | 56 | −13 | `Gauss` only starts linking in ch. 23; the earlier `bilangan bulat Gauss`, `lema Gauss`, `hukum Gauss` are correctly untouched. |
| `def:b3:topology:interior` | 105 | 93 | −12 | `padat` (*dense*) is stoplisted: it is also the everyday “crowded”, and `kepadatan` is the density of a measure. |
| `def:b3:topology:compact` | 291 | 302 | +11 | `kompak` in `PRIMARY_OK`, like English *compact*. |
| `def:b3:galois:separable` | 29 | 40 | +11 | `separabel` is invariant; correct sense. |
| `def:b3:forms:boundary` | 24 | 13 | −11 | **`batas` is deliberately absent from `PRIMARY_OK`**: unlike English *boundary* it is also the ordinary *bound* (batas atas, batas gabungan, batas ekor), and a primary link sent 25 of its 40 occurrences to the wrong sense in chs. 22–23. |
| `def:b3:probability:space` | 62 | 51 | −11 | `peluang` and `distribusi` are stoplisted: both are ordinary words here (`fungsi distribusi`, `distribusi Gauss`, “ada peluang bahwa …”). |

Three targets are reached in Indonesian and not in English
(`ex:b3:probability:laws`, `thm:b3:lebesgue:paramcont`,
`thm:b3:product:ballvolume`): in each case the Indonesian phrase
(`distribusi Gauss`, `integral berparameter`, `volume bola satuan`) recurs in
the prose where the English one happens not to. All are the right sense.

Four Indonesian-only stoplist entries defend homographs English does not have,
and each was added only after reading the links it produced:

* **`sekawan`** — *associate* (ch. 2) vs *conjugate* (conjugate exponents,
  complex conjugate, harmonic conjugate): 37 of 43 links were the wrong sense.
* **`Euclid`** — Indonesian writes both *Euclidean* and *Euclid’s* as `Euclid`,
  so `geometri Euclid`, `lema Euclid` and `tolok ukur Euclid` were all pointing
  at the Euclidean **ring**.
* **`hampir di mana-mana`** — English writes `a.e.` (stoplisted there) 90 % of
  the time; spelled out, the Indonesian linked 100 times against English’s 2.
* **`batas`** — see the table.

---

## 6. Sampled passages, judged

Five passages were re-read cold, without the English beside them, and judged
`native` / `near-native` / `MT`.

**(a) `parts/bachelor-3/id/13-hilbert-spaces.tex`, chapter opening — *native*.**

> …satu struktur tambahan itu memulihkan, dalam dimensi tak berhingga, hampir
> seluruh geometri Euclid: proyeksi ortogonalnya ada, setiap fungsional kontinu
> berupa hasil kali dalam terhadap sebuah vektor tetap (menurut Riesz), dan
> basis ortonormalnya menguraikan setiap vektor menjadi deret konvergen dengan
> pembukuan Pythagoras (menurut Parseval).

The colon-then-list rhythm, `menurut X` for attribution and the metaphor
`pembakuan/pembukuan Pythagoras` are how an Indonesian lecturer writes; nothing
here is word-order calque.

**(b) `parts/bachelor-3/id/23-clt-gaussian.tex`, the `method` box — *native*.**

> Ritual tiga langkahnya (kebebasan $\to$ hasil kali; Taylor di $0$ $\to$ limit
> eksponensial; Lévy $\to$ konvergensi distribusi) membuktikan teorema limit
> pusatnya, hukum kejadian langka Poisson, dan setiap teorema limit klasik pada
> kuliah ini.

`Ritual tiga langkahnya` keeps the English’s slight wryness without importing
its syntax; `hukum kejadian langka` is the standard Indonesian name.

**(c) `parts/bachelor-3/solutions/id/20-submanifolds.tex`, the belt trick —
*native*.**

> …sehingga sebuah benda yang terikat ke sekitarnya oleh tali (yakni kiat
> sabuknya) kembali ke keadaan tak terpilin setelah $4\pi$ tetapi tidak setelah
> $2\pi$. Jadi grup rotasinya mengingat paritas putaran penuhnya; dan $S^3$,
> yang terhubung sederhana, adalah tempat ingatan itu tinggal.

`tempat ingatan itu tinggal` is an idiomatic rendering of “is where that memory
lives”; a machine would have produced *di mana memori itu hidup*.

**(d) `parts/bachelor-3/id/21-differential-forms.tex`, Poincaré lemma proof —
*native*.**

> Memeriksa \eqref{eq:b3:forms:homotopy} adalah perhitungan yang dikerjakan
> sekali seumur hidup, jadi kita kerjakan selengkapnya. … Sifat berbentuk
> bintangnya masuk tepat di tempat yang seharusnya: $tx \in U$ untuk
> $t \in \intcc01$, sehingga $a(tx)$ bermakna.

`sekali seumur hidup` and `masuk tepat di tempat yang seharusnya` are
Indonesian idiom, not glosses.

**(e) `parts/bachelor-3/solutions/id/22-probability-foundations.tex`, question
24 — *near-native*.**

> …jadi keseragamannya berharga $\ln N$, bukan $N$: yakni pengamatan yang
> menjadikan peminimuman risiko empiris, dan bersamanya pembelajaran mesin,
> mungkin secara statistik.

Correct and readable, but `mungkin secara statistik` (“statistically possible”)
is the one place in the sample where the English word order still shows; a
native writer would more likely close with `…secara statistik menjadi mungkin`.
This is the kind of residue that keeps the register score at 24 rather than 25.

---

## 7. Why not 100

1. **The link layer costs two points.** Target parity is complete, but four
   Indonesian homographs (`sekawan`, `Euclid`, `batas`, `bebas`) had to be
   defended by stoplisting rather than by a distinct word, which costs the
   reader ~120 links English gets. `aljabar` and `pusat` cost another 84 for
   the same reason. Two of these could be repaired in the prose instead — by
   writing `kawan` only for the ring sense, or `sekutu` — but that is a
   vocabulary change that belongs in the style card, not in one book.
2. **Register loses a point** to a handful of clause-final constructions that
   still follow the English order, as in sample (e).
3. **Terminology loses a point** to `sekawan`, which is doing two jobs, and to
   the `variabel` / `peubah acak` split, which is settled but slightly uneven to
   read: `variabel acak` never appears, yet `variabel` alone often denotes a
   random variable in chs. 22–23.

Nothing on this list is a defect a reader would call an error; they are the
three places where the Indonesian edition is a translation rather than an
original.

---

## 8. Notes for the coordinator

* **Shared-gate false positive, reported not fixed.** `TECHNICAL_MACROS` in
  `tools/check_hindi_prose.py` (whose `visible_text` the Indonesian gate reuses)
  does not include `texorpdfstring`, so the *second*, PDF-bookmark argument is
  read as prose. `\texorpdfstring{$SO(3)$}{SO(3)}` therefore fires
  `english: 'SO'`. Worked around in scope, in
  `parts/bachelor-3/id/20-submanifolds.tex`, by writing the bookmark as
  `grup rotasi`.
* **Promote into `indonesian_style_card.md`:** `kepadatan` (never `kerapatan`)
  for *density* in both senses; and the note that `jejak` must be reserved for
  the trace of a path now that `trace` is English, with `peringkat` likewise
  reserved for an ordinary ranking now that `rank` is English.
