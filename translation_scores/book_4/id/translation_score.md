# Book 4 — Indonesian (`id`) — translation self-score

| Field | Value |
|---|---|
| **Book** | One Math Book 4 (University Year 2) |
| **Entry** | `one_math_book_4_university_year_2_id.tex` |
| **Language** | Indonesian (`id`), per `indonesian_style_card.md` |
| **Quality bar** | `native academic` — an Indonesian-medium lecturer should set it as the course text without apologising for it |
| **Scope** | 23 chapters + 23 solutions = **46 files** under `parts/bachelor-2/id/` and `parts/bachelor-2/solutions/id/` |
| **Kind of pass** | **translation from the English canon**, chapter by chapter, as a line-range patch on top of the English source. No machine translation was used or post-edited at any point. |
| **Delivered** | **46 of 46 files — the book is complete.** |
| **Term config** | `tools/term_config/book4_id.py` (curated, not a translation of `book4_en.py`) |
| **Overall score** | **96 / 100** |
| **Date** | 2026-08-20 |

---

## 1. Dimension scores (whole book, 46 files)

| Dimension | Weight | Score | Comment |
|---|---:|---:|---|
| Register (second-year university, Indonesian academic voice) | 25 | 24 | The book speaks the register an Indonesian mathematics faculty actually writes: `Misalkan`, `Andaikan`, `Tunjukkan bahwa`, `Buktikan`, `Simpulkan`, `Adapun … `, `Sebaliknya, …`, `bila dan hanya bila`, `Menurut \cref{…}`. Discourse particles carry the argument the way the English `so/hence/whereas` do — `jadi`, `sehingga`, `sedangkan`, `padahal`, `justru`, `yakni`, `alih-alih`. The narrative asides of the weekend problems keep their voice (de Méré's wager, the Galton–Watson epidemic, the polling problem) without turning into lecture calque. Loss: a handful of long displays keep an English-shaped clause order because the ordered math-span census forbade re-ordering them (§7). |
| Terminology (standard Indonesian mathematics) | 20 | 19 | §4 lists the whole ruling set. Everything follows the style card and the coordinator's rulings: `cembung`/`cekung`, `konvers` (the converse of a theorem) vs `kebalikan` (the multiplicative inverse), `distribusi`, `nilai harapan` (never bare `harapan`), `irasional`, `bilangan cacah` for the canon's `$\N$`. University-specific rulings in §4 (`lapangan` vs `medan`, `kuosien`, `terbilang`, `ragam`, `peubah acak`, `tanda permutasi`). Deduction: `rank` and `trace` stay untranslated per the card — defensible, but they are the only two visibly English nouns left in a 195 000-word book (§4, §7). |
| Freedom from MT artefacts | 20 | 20 | `check_indonesian_prose.py` is **OK on all 46 files** in all six classes (`english`, `untranslated`, `math-space`, `redup-space`, `enclitic`, `split-number`). No residual English in prose, TikZ node text, `\text{}` inside math, `xlabel/ylabel/title`, chapter/section titles, environment optional titles or index keys. The two `\mathrm{}` subscripts a reader sees were localised (`\mathrm{odd}` → `\mathrm{ganjil}`, `\mathrm{slow}` → `\mathrm{lambat}`); `\mathrm{id}`, `\mathrm{cl}`, `\mathrm{ext}`, `\mathrm{diag}`, `\mathrm{tan}` are notation and stay. Decimal separator is a **point** and every digit is ASCII, as the card requires. |
| Structural fidelity | 15 | 15 | `check_translation.sh bachelor-2 id` **PASSED**: identical label sets and order, env/figure census, UTF-8 (no `\'e`-class escapes), completeness. On top of it: `exo:`/`pb:` ↔ `\begin{solution}{}` parity verified chapter by chapter (23/23 clean), no duplicate labels, no `\end{…>` typos, no drafty `...`. The applier additionally enforced six per-file invariants the repository has no gate for (§3). |
| Mathematical correctness | 10 | 10 | The mathematics is byte-identical to English by construction: every display, every TikZ body, every `\foreach` list, every number is the English bytes unless a line range was deliberately replaced, and the applier refuses a replacement whose **ordered math-span sequence** (after blanking `\text{…}`) or whose `\[`/`\]` sequence differs from the English lines it replaces. |
| Link layer (`\omterm`) | 10 | 9 | `--check` green and idempotent; **3 388 links across 46 files**; **whole-book target parity is exact — 85 / 85, no missing target and no extra target.** Deduction: per-target link *density* still diverges from English on eight targets (§5), in both directions, for reasons that are linguistic rather than curatorial. |
| Build | — | pass | 0 errors, 0 undefined references, **0 overfull boxes**, 428 pages. |

**Weighted total: 96 / 100.** Above the ship bar of `translation_instruction.md`
(complete book at ≥ 95).

---

## 2. Gate results

| Gate | Result |
|---|---|
| `bash tools/check_translation.sh bachelor-2 id` | **TRANSLATION GATE: PASSED** |
| `python3 tools/check_indonesian_prose.py parts/bachelor-2/id parts/bachelor-2/solutions/id` | **OK (46 files)** — zero in all six classes |
| `python3 tools/link_defined_terms.py --book 4 --lang id --check` | **green** — "every file matches what the config generates" |
| `latexmk -g one_math_book_4_university_year_2_id.tex` | **exit 0** |
| `grep -c '^!'` on the log | **0** errors |
| `grep -ci 'undefined'` | **0** undefined references |
| `grep -c 'Overfull'` | **0** |
| Output | `build/one_math_book_4_university_year_2_id.pdf`, **428 pages** |
| `grep -c '/id/' …_id.fls` (after `latexmk -g`) | **414** — the translated bodies really are in the build, not an English fallback |
| `\omterm` target parity vs English | **85 / 85 — exact** |
| Exercise ↔ solution parity, per chapter | **23 / 23 clean** |
| Index-key intersection EN ∩ id | **4 / 164** (`Lipschitz`, `astroid`, `ideal`, `wronskian`) — only genuinely identical terms, so the index does not orphan-split |

---

## 3. Method

Every file was produced as a **line-range patch on top of the English source**,
applied by a small script written for this job (in scratchpad, not in the repo).
The applier copies every English line that is not explicitly replaced
**byte-identically**, and refuses to write a file unless all of these survive,
in order, against the English twin:

1. the sequence of `\begin{env}` / `\end{env}` tokens;
2. the set and order of `\label{…}`;
3. the sequence of `\begin{solution}{key}` keys;
4. the **ordered sequence of math spans** after blanking `\text{…}`;
5. the ordered sequence of `\[` and `\]`, both whole-file **and per replaced
   range** (the trap of the style card's §4b appendix: a range that covers `\[`
   but stops before `\]` duplicates the delimiter and no other census notices);
6. brace balance, and the `tikzpicture` / `axis` bodies unchanged;
7. the Indonesian prose gate, run on the candidate file before it is written.

Roughly twenty range-overrun bugs, five dropped environment openers, two
`\begin{example[...]}` bracket typos and about a dozen math-span **order** swaps
were caught by these censuses rather than by the build. The order swaps are the
characteristic Indonesian hazard: the language puts the modifier after the head,
so *"$2\pi$-periodic $f$"* wants to become *"$f$ berkala-$2\pi$"* — which
reverses the span order. Every one was reworded to keep the English order
(`fungsi berkala-$2\pi$, sebut $f$, …`).

The English source used as the base had `\omterm{label}{display}` unwrapped to
`display` first, so the translator never saw generated markup; the link layer was
regenerated afterwards from the Indonesian text.

---

## 4. Terminology decisions

### 4.1 Adopted from the style card / coordinator rulings

| English | Indonesian | Note |
|---|---|---|
| convex / concave | `cembung` / `cekung` | 165 occurrences converted from `konveks`/`konkaf`; holds at university register |
| converse (of a theorem) | `konvers` | 20 occurrences converted; the 4 genuine multiplicative reciprocals kept `kebalikan` |
| distribution | `distribusi` | never `sebaran` |
| expectation | `nilai harapan` | never bare `harapan` |
| irrational | `irasional` | never `tak rasional` |
| natural number (`$\N$`) | `bilangan cacah` | the series' single remaining use, `01-sets-structures.tex:164` |
| rank, trace | `rank`, `trace` | kept English per the card — see §7 |

### 4.2 Rulings this book had to make (candidates to promote into the card)

| English | Indonesian | Reasoning |
|---|---|---|
| quotient set / quotient ring / quotient group | `himpunan kuosien`, `ring kuosien`, `grup kuosien` | `kuosien` is the standard Indonesian loan for the algebraic quotient; `hasil bagi` is arithmetic division and would mislead |
| sign of a permutation | `tanda permutasi` | reserved `signatur` for the signature of a quadratic form (ch. 12), exactly as English keeps the two apart |
| countable | `terbilang` | `dapat dihitung` reads as "computable" |
| field (algebraic) vs field (vector field) | `lapangan` vs `medan` | the two senses collide in this volume (ch. 1 and ch. 20); `lapangan` for the algebraic structure, `medan` for the vector field |
| convex hull | `bungkus cembung` | follows the `cembung` ruling |
| barycentre / centerpoint | `barisentrum` / `titik penyeimbang` | ch. 17 and its weekend problem |
| envelope | `selubung` | ch. 18 weekend problem |
| cusp | `titik runcing` | ch. 18 |
| random walk | `jalan acak` | ch. 21 weekend problem |
| variance | `ragam` | `varians` also circulates; `ragam` is the KBBI-registered statistics term |
| random variable | `peubah acak` | not `variabel acak` |
| normal mode | `moda normal` | ch. 16 |
| heads / tails (coin) | `gambar` / `angka` | the Indonesian coin idiom; normalised across the volume (`koin`, not `uang logam`) |
| critical / subcritical / supercritical | `kritis` / `subkritis` / `superkritis` | ch. 23 branching processes |
| nondecreasing | `tidak turun` | matches the Book-4 precedent in `09-integration.tex` |
| memorylessness | `sifat tanpa ingatan` | ch. 22 |
| Year *N* volume | `jilid Tahun ke-N` | the series-wide cross-volume formula |

---

## 5. Link layer

| Quantity | English | Indonesian |
|---|---:|---:|
| Linkable terms after curation | 173 | 173 |
| `\omterm` links inserted | 3 511 | **3 388** |
| Distinct `\omterm` targets | 85 | **85 — exact parity** |
| Files touched | 46 | 46 |
| `--check` idempotent | — | yes |

`AMBIG_POLICY = "drop"`, the university convention. The config carries its own
`NOT_A_TERM` (`teorema`, `lema`, `akibat`, `ketaksamaan`, `rumus`, `kaidah`,
**`aturan`**, `asas`, `identitas`, `paradoks`, `kriteria`, `sifat`, `prinsip`,
`soal`, `masalah`), because the shared defaults are English heads and would let
every Indonesian result-name through.

### 5.1 The four calibration rules of the card, applied

* **Rule 1 (a capitalised display is a separate term and bypasses `STOP`).**
  Every stoplisted homograph is listed in **both** cases, and the `-nya` forms
  are listed too.
* **Rule 2 (`-nya` in a display is a separate term).** Five definitions
  harvested a `-nya` display and so made the bare noun unreachable:
  `hukumnya`, `distribusinya`, `ragamnya`, `kovariansinya`, `panjangnya`.
  Each definition was reworded to `\emph{hukum}`, `\emph{distribusi}`,
  `\emph{ragam}`, `\emph{kovariansi}`, `\emph{panjang}` — worth **+334 links**,
  and it is what lifted `def:b2:randomvar:law` from 19 links to 98 against English's 87, and
  `def:b2:curves:length` from 32 to 75 (English 72).
* **Rule 3 (a capitalised display can make a term unreachable).**
  `\emph{Orde}` in ch. 1 registered the capitalised form only, so the whole
  group-order vocabulary was dark; reworded to `Adapun \emph{orde} …`.
  `\emph{selubung}nya\index{selubung}` in ch. 18 failed the adjacency the
  harvester needs (`\emph{…}\index{…}`) and produced **0** links against
  English's 27; reworded so the pair is adjacent.
* **Rule 4 (`aturan` in `NOT_A_TERM`).** Done, with the whole family.

### 5.2 Divergences from the English target set, and why each is closed

| Target | Symptom | Resolution |
|---|---|---|
| `ex:b2:fourier:zetafourodd` | `gejala Gibbs` linked; English never links the Gibbs phenomenon | `DROP` |
| `pb:b2:diffcalc:1` | `rumus Jacobi` reached through `\emph{}\index{}`, bypassing `NOT_A_TERM` | `DROP`, both cases |
| `pb:b2:funcseq:1` | `teorema Korovkin`, same route | `DROP`, both cases |
| `prop:b2:structures:cyclic` | `fungsi Euler` (Euler's totient) — English has the definition but never cross-links it | `DROP` |
| `thm:b2:fourier:parseval` | `kesamaan Parseval`, a named identity | `DROP` |
| `thm:b2:structures:signature` | bare `tanda permutasi`; English never links bare "signature" either | `DROP`, with the `-nya` form |
| `thm:b2:quadratic:sylvester` | bare `signatur` (the quadratic-form signature) surfaced once the previous drop landed | `DROP`, both cases and `-nya` |
| `thm:b2:nvs:finitedim` | **missing.** The definition of equivalent norms and the finite-dimension theorem both wrote `\index{kesetaraan norma}`, so the two collided and the theorem lost its term | the definition's index key changed to `norma setara` (English already keeps them apart: *equivalent norms* vs *equivalence of norms*) |

After these eight, `diff` of the sorted unique `\omterm{target}` sets is **empty
in both directions**.

### 5.3 Density divergences that remain (the 1-point deduction)

| Target | EN | id | Why |
|---|---:|---:|---|
| `def:b2:funcseq:def` | 112 | 152 | Indonesian says `secara seragam` where English often writes an adjective inside a noun phrase, so the adverb is linkable more often |
| `def:b2:series:def` | 53 | 81 | same shape for `mutlak` / *absolutely* |
| `def:b2:integration:improper` | 24 | 53 | `konvergen` is stoplisted (it is the general word for *convergent*) but still links inside ch. 9, which is denser in Indonesian |
| `def:b2:structures:sn` | 51 | 84 | `siklus` covers both *cycle* and *cycles* and reads naturally more often |
| `def:b2:metric:compact` | 159 | 119 | Indonesian frequently drops a repeated `kompak` that English repeats |
| `def:b2:metric:continuity` | 481 | 402 | same |
| `def:b2:proba:independence` | 117 | 79 | `saling bebas` is a two-word phrase; the shortest Indonesian phrasings elide it |
| `def:b2:reduction:eigen` | 361 | 323 | same |

All eight are *density*, never *sense*: every wrong-sense flood found during
calibration was closed, either by the stoplist (`konvergen`, `normal`, `setara`,
`aljabar`, and the card's homograph list in both cases), by `DROP`
(bare `tertutup`, which is the *closed set* of ch. 4, not the *exact form* of
ch. 20), or by `EXTRA_PROTECT`:

* `seragam` in the **uniform-law** sense (`dipilih seragam`, `pencuplikan
  seragam`, `bobot seragam`, `jumlahnya seragam`, `bebas dan seragam`, …) and in
  the **uniform-continuity** sense (`kekontinuan seragam`) — the exact analogue
  of `book4_en.py`'s `uniformly\s+(?:at\s+random|continuous|in\b)` list;
* `mutlak` inside `nilai mutlak` / `bernilai mutlak` (absolute *value*, not
  absolute convergence);
* `hasil kali Cauchy`, `bagi` as the preposition "for", `kali` as
  "times/occasion", `di belakang titik` as the decimal point.

No protect regex consumes a `$`, per the warning in `protect.py`.

---

## 6. Sampled passages, judged

Five passages read cold, without the English beside them, and judged
*native / near-native / MT*.

1. **`01-sets-structures.tex`, chapter opening.** *"Bab pembuka ini mempertajam
   landasan yang diletakkan pada jilid Tahun ke-1 menjadi perkakas kerja
   sehari-hari: kalkulus himpunan dan kuosien, perbandingan himpunan tak hingga
   (keterbilangan, Cantor–Bernstein) …"* — **native.** `mempertajam … menjadi
   perkakas kerja sehari-hari` is idiomatic Indonesian, not a rendering of
   *sharpens … into working tools*; the colon-list rhythm is the one Indonesian
   textbooks use.
2. **`13-hermitian-forms.tex`, exercise 8.** *"Buktikan bahwa ruang eigen $u$
   bagi nilai eigen yang berbeda saling ortogonal, dan bahwa komplemen ortogonal
   sebuah ruang eigen bersifat stabil terhadap $u$."* — **native.** `saling
   ortogonal` and `bersifat stabil terhadap` are the standard Indonesian
   algebra formulas; an MT pass would have produced `ortogonal satu sama lain`
   and `stabil di bawah`.
3. **`22-discrete-random-variables.tex`, the variance toolkit.** *"…bila $X, Y$
   saling bebas, maka $\operatorname{Cov}(X, Y) = 0$ (sedangkan konversnya
   salah), jadi ragam peubah yang saling bebas itu menjumlah."* — **native.**
   `sedangkan konversnya salah` is exactly how an Indonesian lecturer flags a
   failing converse, and `menjumlah` (intransitive) is the right verb for
   *variances add*.
4. **`23-generating-functions.tex`, the cobweb remark.** *"Entah kurvanya tetap
   di atas diagonalnya pada $\intco01$ …: tangganya tak punya tempat berhenti
   sebelum $1$. Entah kurvanya memotong di suatu $q < 1$ …"* — **native.** The
   `Entah … Entah …` correlative is the Indonesian *either … or …* for an
   exhaustive dichotomy; a machine would have written `Baik … atau …`.
5. **`solutions/id/21-countable-probability.tex`, recurrence of the walk.**
   *"Kejadiannya turun dalam $k$, jadi kekontinuan monoton memberi
   $\P(\text{pulang tak hingga kali}) = 1$: itulah kerekurenannya."* —
   **near-native.** Correct and compact, but `kerekurenannya` is a coined
   ke-/-an nominalisation of a loanword; a human author might have written
   `itulah sifat rekurennya`. It is the one place in the sampled five where the
   ke-/-an machinery shows.

No sampled passage reads as machine translation.

---

## 7. Why not 100

1. **`rank` and `trace` stay English (−1 on terminology).** The style card rules
   them untranslated and I followed the card rather than diverge from the other
   `id` books mid-series. But `peringkat`/`rank` and `teras`/`jejak` do exist in
   Indonesian mathematical writing, and in a 195 000-word book where every other
   noun is Indonesian these two are conspicuous. **This should be settled
   series-wide, not book by book** — my recommendation is to keep them, because
   `peringkat` collides with the ordinary "ranking" that ch. 21's weekend
   problem uses, and `jejak` collides with the *trace* of a path; but the ruling
   deserves to be recorded as a decision rather than a default.
2. **A handful of clause orders are English-shaped (−1 on register).** The
   applier's ordered math-span census is unforgiving: where the natural
   Indonesian sentence would put the modifier after the head and thereby reverse
   two `$…$` spans, the sentence was rebuilt to keep the English order. Twelve
   or so sentences in chapters 12–16 therefore read a shade more literally than
   they would if the census allowed span re-ordering. This is a deliberate
   trade: a wrong span order is a silent mathematical corruption, a slightly
   stiff sentence is not.
3. **Link density still diverges on eight targets (−1 on the link layer).**
   §5.3. Sense parity is exact; density is not, and closing it would mean either
   over-linking Indonesian adverbs or hand-curating several hundred individual
   sites. The remaining gap is linguistic, not curatorial.
4. **The remaining point** is the ordinary distance between a first complete
   edition and one that has been read end to end by a second Indonesian
   mathematician. Nothing specific is known to be wrong.

---

## 8. Files

* `parts/bachelor-2/id/01…23-*.tex` — 23 chapters
* `parts/bachelor-2/solutions/id/01…23-*.tex` — 23 solution files
* `tools/term_config/book4_id.py` — curated term config
* `translation_scores/book_4/id/translation_score.md` — this file

Nothing outside these four paths was touched.
