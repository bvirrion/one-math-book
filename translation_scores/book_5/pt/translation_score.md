# Translation score — Math Book 5 · Brazilian Portuguese (`pt`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 5 (University Year 3, `bachelor-3`) |
| **Language** | Brazilian Portuguese (`pt`) |
| **Quality bar** | **native academic** (English is the source of truth; the ES and FR Book 5 editions were used only as intra-series references for how far a translation of this book may reasonably depart from English clause order) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **met** |
| **Date** | 2026-08-01 (re-generated the same day against `lang_pt.TAIL_ON_EVERY_WORD = True`) |
| **Scope of this pass** | **Full re-translation from the English canon.** All 46 files (23 chapters + 23 solution files) re-derived through a structure-preserving mask/translate/unmask pipeline; the pre-existing `pt/` bodies were never edited in place and were not used as a source. Term-link config `tools/term_config/book5_pt.py` rewritten from scratch. |

## Verdict in one line

A complete, structurally exact, natively-written Brazilian third-year
course: every chapter and every solution re-derived from English through
a pipeline that makes byte-preservation of math, labels, solution keys
and figure code a property of the method rather than of vigilance, with a
freshly curated term-link layer that reaches **exact `\omterm` target
parity** with English (130 targets on both sides) at 99.1 % of English's
link volume.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror: 23 chapters + 23 solution files; **722 `\label`s identical to English in set *and* order**; 299 `exo:`/`pb:` labels ↔ 299 `\begin{solution}{…}` keys, byte-identical on both sides; weekend problem present in all 23 chapters. `check_translation.sh bachelor-3 pt` **PASSED** |
| Terminology | **97** | Brazilian L3 register across all nine subject areas: *corpo* (never *campo*), *aplicação* (never *mapa*), *classes laterais à esquerda* (never *cosets*), *recíproca* (never *conversa*), *enumerável / não enumerável / enumerabilidade* (never *contabilidade*), *grupo solúvel*, *domínio de integridade*, *DIP/DFU*, *caráter*, *fecho*, *mensurável*, *quase em toda parte (q.t.p.)*, *quase certamente (q.c.)*, *base hilbertiana*, *função holomorfa*, *resíduo*, *subvariedade*, *bordo*, *índice de rotação*, *pullback*, *teorema central do limite*. No MT sense swaps found in sampling |
| Register / tone | **96** | Reads as a Brazilian third-year lecture course: *Seja $f$…* / *Sejam…* (the 329 `Deixar` calques of the previous edition are gone — the word does not occur once), *Suponha que…*, *Diz-se que…*, *Note que…*, *tem-se*, *donde*, *ao passo que*, *de modo que*; exercise stems in the imperative (*Mostre que*, *Demonstre*, *Calcule*, *Deduza*). *Como* / *Uma vez que* for causal *Since* — no *Desde* calque anywhere |
| LaTeX hygiene | **97** | 0 fatal errors, 0 undefined references. **0 TeX accent escapes** — every accent UTF-8: Hölder (48), Möbius (17), Cesàro (12), Rouché (11), Lévy (11), Carathéodory (10), Grönwall (9), Poincaré (6), Cramér (3), Pólya (3), Apéry (2), Dieudonné (2), Scheffé (2), Sierpiński, Šmulian. 5 overfull boxes remain, all one running-header artifact, matching the Dutch edition box for box — see *Known state: five overfull boxes* |
| Cross-refs / rule compliance | **99** | `\label`, `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English **by construction** (masked before translation). **All 1 207 `\cref` calls** carry the Portuguese article with a non-breaking tie where one is due (`o~`, `a~`, `do~`, `no~`, `pelo~`, …, keyed by the `\crefname` gender map in `styles/lang/pt.tex`) — **0 bare article + space + `\cref`** left. Zero curriculum or country names in visible text; cross-volume references are prose-only (*o volume do segundo ano*) |
| Figures | **98** | All 15 `tikzpicture`s and 7 `tabular` blocks match English exactly in count; **drawing code byte-identical** (masked as hard environments). Only node text, table headers and captions localized — the 4 English table headers that survive byte-preservation were found by audit and translated (*grupos de ordem $n$*; *partição / forma de Jordan / fatores invariantes*; *sim/não* in the Banach census; *intervalo / peso / fórmula / norma$^2$ / hábitat* in the orthogonal-polynomials dictionary) |
| Solutions | **97** | All 299 solutions present, complete and natively written; localized `\section*{Capítulo \ref{ch:…} --- <título>}` headers with `ch:…` slugs unchanged. Solution-side link volume 1 583 vs English 1 581 (100.1 %) |
| MT-artifact freedom | **96** | **0 residual English** after stripping labels, environment names, macros and math from all 46 files. **216 `\text{…}` strings inside protected math translated** in a dedicated post-pass (`\text{a.s.}`→`\text{q.c.}`, `\text{where }`→`\text{em que }`, `\text{ odd}`→`\text{ ímpar}`, …). Index keys 100 % Portuguese: the EN∩PT index-key intersection is **2 of 309** (`ideal`, `pullback` — genuinely identical words) |

**Overall: 96** — weighted toward register + terminology + MT-artifact
freedom, since structure is already gated mechanically by
`check_translation.sh` and the label/solution-key diffs.

## Structural / build gates (run 2026-08-01)

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-3 pt` | **PASSED** |
| `sh tools/check_book5_golden.sh` | **PASSED** — "every file matches what the config generates"; the English sources were never touched |
| `python3 tools/link_defined_terms.py --book 5 --lang pt --check` | **PASSED**, and idempotent (`--unwrap --apply` → `--apply` → `--apply` inserts 0) |
| `lang_pt.TAIL_ON_EVERY_WORD = True` | **APPLIED by the orchestrator**; Book 5 regenerated against it, `EXTRA` trimmed 126 → 84 |
| `latexmk one_math_book_5_university_year_3_pt.tex` | exit 0 |
| Fatal errors (`grep -ac '^!'`) | **0** |
| Undefined references (`grep -aci 'undefined'`) | **0** |
| Overfull `\hbox` (`grep -ac 'Overfull'`) | **5** — all five are the *same* ch. 7 running-header mark, 2.72 pt each; the Dutch edition has the identical five. No prose, display or figure is over-wide. See *Known state: five overfull boxes* |
| Underfull `\vbox` from `\output` | 52 — page-breaking noise, not a defect |
| `Missing character … nullfont` | 10 — same count in the English, French and Spanish builds; preamble artifact, not pt-specific |
| PDF | `build/one_math_book_5_university_year_3_pt.pdf`, **411 pp** (EN 395, FR 404, NL 417, ES 418) |
| `\omterm` **target parity** vs English | **exact** — 130 distinct targets on both sides; `set(PT) − set(EN)` and `set(EN) − set(PT)` are both **empty** |
| Term links | **4 288** across 46 files (EN 4 326 → **99.1 %**; ES 4 449, FR 4 251) |
| Exercise ↔ solution parity | 299 / 299 both sides, key by key |
| `\label` set and order | identical to English (722) |
| Duplicate labels | none |
| `\end{proof>` typo class | none |
| Drafty `...` in prose | none |
| TeX accent escapes (`\'e`, `\"o`, …) | **0** |

> **Build-environment caveat.** No Portuguese `.ldf` is installed on this
> machine, so the book builds **without babel** (`onemath` warns:
> "brazilian/portuguese.ldf not found"). Portuguese words are therefore
> hyphenated with English patterns. The overfull-box count and the
> 411-page total are consequently *provisional*: with
> `texlive-lang-portuguese` installed both can only improve, and the five
> remaining overfull boxes are header truncation rather than prose, so
> they are unaffected either way.

## Method

The job was a full re-translation of ~138 000 English prose words, not a
repair of the previous `pt/` bodies. To make structural fidelity a
property of the process rather than of attention, every file went through
a mask → author → unmask pipeline:

1. **Mask.** A char-by-char walk protects, and replaces with numbered
   placeholders: `%` comment lines; hard environments (`tikzpicture`,
   `tabular`, `align`, `equation`, `gather`, `multline`, `cases`, all
   matrix environments, `verbatim`); `\begin{solution}{key}`; every
   reference command (`\label`, `\ref`, `\cref`, `\Cref`, `\eqref`,
   `\includegraphics`, …); list `\begin{…}[…]` options; and all math
   (`\[…\]`, `\(…\)`, `$$…$$`, `$…$`). Placeholders carry a short preview
   (`⟦123:cref:thm⟧`) so the author can see what a slot holds without
   being able to edit it.
2. **Author.** The Portuguese is written against the masked English —
   never against the old `pt/` file, which was consulted for nothing.
3. **Unmask + verify.** Reinsertion is checked: every placeholder must be
   consumed **exactly once**. This caught three real defects that would
   have silently dropped or duplicated formulas (a doubled ⟦276⟧ in ch. 2,
   a doubled ⟦19⟧ in ch. 9, a tripled ⟦206⟧ in solutions 1). A per-file
   verifier then compares the environment sequence, the `\label` list and
   the `\begin{solution}{}` key list against English, and flags
   zero-width characters, TeX accent escapes and residual English words.
4. **Post-passes.** (a) UTF-8 de-accenting of any `\'e`-style escape;
   (b) a dedicated `\text{…}` pass over the 216 prose strings living
   inside protected math; (c) a `tikzpicture`/`tabular` audit for English
   node text and table headers; (d) an article-tie pass putting a
   non-breaking `~` between every article or contracted preposition and
   the `\cref` it governs (110 insertions).

`tools/check_translation.sh bachelor-3 pt` was run after every few
chapters, not only at the end.

## Term-link layer (`tools/term_config/book5_pt.py`)

The previous config contained `DROP = set(STOP)`, which hard-dropped every
stoplisted word everywhere and destroyed the soft, chapter-local linking
that `STOP` exists to provide. It was replaced by a curated config:

* **`STOP` (127 entries)** — a genuine Portuguese mirror of
  `book5_en.STOP` (ordinary words, and words whose sense changes by
  chapter), plus the homographs English never has to arbitrate: *módulo*
  (module vs. modulus), *argumento* (of a complex number vs. of a proof),
  *grau*, *base*, *simples*, *unitário*, *ordem*, *álgebra*, *norma*,
  *integral*. Soft on purpose: each is still linked inside the chapter
  that defines it.
* **`PRIMARY_OK` (16)** — the Portuguese forms of English's *compact,
  closed, path, boundary, interior, irreducible*.
* **`DROP` (37)** — harvested Portuguese `\index` entries that name a
  *result* rather than a notion, or that English refuses through its own
  `NOT_A_TERM` filter. Each carries, in a comment, the target it would
  have reached, so the parity argument is auditable line by line.
* **`EXTRA` (84, trimmed from 126 — see *The `TAIL_ON_EVERY_WORD` flip*
  below)** — what the `(?:e?s)?`-on-every-word rule still cannot spell.
  Two classes only: **irregular plurals** — `-ão/-ões` (*representações,
  funções, aplicações, extensões, soluções*), `-al/-ais` (*ideais,
  normais, maximais, duais, diferenciais*), `-vel/-veis` (*irredutíveis,
  solúveis, variáveis, mensuráveis, integráveis, deriváveis*),
  *anel/anéis* — and **gender variants**, which `WORD_TAIL` never
  reaches (*contínuo/contínua*, *perfeito/perfeita*,
  *reflexivo/reflexiva*), together with the abstract nouns English gets
  from `DERIVED` (*continuidade, compacidade, completude, conexidade,
  holomorfia, mensurabilidade, integrabilidade, solubilidade,
  orientabilidade, autoadjunção*). Regular `-r/-res` is **not** declared:
  *operador* + *es* is generated by the rule.
* **`AMBIG_POLICY = "drop"`, deliberately.** At third-year level a word two
  chapters define differently is a genuine ambiguity, not a spiral
  re-definition, and a wrong link costs more than a missing one; the
  `local` mechanism still links such a word inside the chapter that pins
  it down, which is exactly English's behaviour. `nearest-preceding` (the
  school-book policy) would point every later use of *irredutível* at
  whichever of its two definitions happened to come last.
* **`EXTRA_PROTECT = [r'por\s+completo']`** — the adverb *entirely*, never
  the adjective *complete*. Checked against all four silent-failure rules,
  none of which any gate catches:
  1. **Consumes no `$`.** A pattern that eats an opening dollar leaves the
     inline-math rule pairing the closing one with the next formula's
     opening dollar, masking every later span inside out.
  2. **No literal space** — `\s+`, so it still matches when the phrase
     straddles a line break (the list is compiled with `re.S`).
  3. **Audited on unwrapped source** through `termlink.wrap.unwrap`:
     3 occurrences, 3 matched.
  4. **Verified live by a moved number** — the strongest of the four,
     because a pattern that matches nothing looks exactly like one that
     works. Regenerating with `EXTRA_PROTECT = []` gives **4 291** links
     and three wrong ones, `por \omterm{def:b3:complete:complete}{completo}`
     in chs. 11, 15 and solutions 15; with the pattern, **4 288** and none.
     The protection is worth exactly 3 links, and it is doing that work.
  Rule 1's accented-vowel corollary (`[ôóo]`, `[âáa]` — *polinômio*,
  *ângulo*) does not apply here: this pattern contains no character class
  and no accented letter.

### The `TAIL_ON_EVERY_WORD` flip (applied by the orchestrator, 2026-08-01)

`tools/term_config/lang_pt.py` — a shared file, **not edited here** — was
changed from `TAIL_ON_EVERY_WORD = False` to `True`, so the optional
`(?:e?s)?` now goes on every word of a phrase instead of the last one
alone. Book 5 was regenerated against it.

**Trim.** Each of the 126 `EXTRA` entries was checked *against the rule*
rather than by eye, by asking `termlink.morphology.pattern` — the code the
linker itself uses — whether some harvested term with the same target now
matches the declared surface form. **42 came back redundant and were
deleted; 84 stay.** The split matters:

* **25 were redundant only because of the flip** — the regular compound
  plurals (*espaços compactos, espaços métricos completos, formas
  fechadas, grupos quocientes, módulos livres, operadores autoadjuntos,
  produtos semidiretos, séries de composição, subgrupos de Sylow,
  vetores gaussianos*, …).
* **17 were already dead weight before it** and should never have been
  declared (*algébricos, completos, conexos, contínuas, gaussianos,
  holomorfas, meromorfas, resíduos*, …): the harvest reached them the
  whole time. Finding these was a side benefit of checking the rule
  instead of trusting the earlier note.
* **28 of the 56 multi-word entries stay**, because their plural is
  irregular, not because of the flag: *funções holomorfas* (`-ão/-ões`),
  *ideais maximais* (`-al/-ais`), *variáveis aleatórias* (`-vel/-veis`),
  *anéis quocientes*, *subgrupos normais*, *soluções maximais*,
  *representações irredutíveis*, *extensões de Galois*, *formas
  diferenciais*, *espaços duais*, *aplicações contínuas*, … The earlier
  claim in this file that "56 evaporate when the flag flips" was
  **wrong**; the measured number is 25.

Regular `-r/-res` was explicitly *not* treated as irregular: `(?:e?s)?`
spells *operador* → *operadores*, so no such entry was kept. The trap in
this family is the other direction — a form that looks regular but is not
(`-m/-ns`: the rule would ask for *ordemes*) — and the check catches it
because it runs the real pattern rather than a guess.

**Verification, not assumption.** Two independent checks:

1. *Occurrences vs. links.* For each of the 42 removed keys, occurrences
   in unwrapped source were counted against links now carrying that
   display. 38 came back clean immediately; the 4 that did not were
   investigated one by one and all four are correct:
   *conexos por caminhos* — its single occurrence sits **inside the
   `definition` environment that defines it**, where the linker suppresses
   self-links and lets the shorter *conexos* claim the span; English does
   character-for-character the same thing inside the same definition
   (`\omterm{def:b3:topology:connected}{path-connected}`).
   *conjunto aberto* — its only occurrence is the `\index{conjunto
   aberto}` of the definition itself.
   *formas fechadas* — 2 occurrences, both meaning *closed-form
   expressions* in chs. 10–11, which precede the ch. 21 definition of a
   closed differential form; the linker's forward-reference rule leaves
   them alone, and **English leaves the identical two sentences
   unlinked**. Linking them would have been a wrong-sense link.
   *grupos quocientes* — 0 real occurrences.
2. *A/B regeneration.* Running the linker's own `harvest` + `wrap_file`
   with the 42 entries restored gives **4 288 links and the identical
   target set**: the deleted entries were worth **exactly 0** links. The
   trim removed configuration, not linking.

**Net effect of the flip: 4 279 → 4 288 links (+9), targets 130 → 130.**
Nine phrases became reachable (*tabelas de caracteres* +3, *produtos
exteriores* +2, *corpos de decomposição* +2, *fechos algébricos* +2,
*produtos internos* +2, *lei das torres*, *formas de Jordan*, *corpos
finitos*, *normas de operador* +1 each), and three counts fell by 6 in
total — every one of them a **re-attribution to the more specific
phrase**, not a loss: *caracteres* −3 → *tabelas de caracteres*
(`character` → `representations:table`), *algébricos* −2 → *fechos
algébricos* (`galois:algebraic` → `galois:closure`), *módulos* −1 →
*módulos livres* / *módulos finitamente gerados* (`modules:module` →
`modules:free`). Every one of those three is a better link than the one
it replaced.

**The two exposed decisions were re-audited, since the flip could have
reopened either:**

* ***irredutíveis*** — still **0** links, as intended. `-vel/-veis` is
  irregular, so per-word tails do not reach it; the −68 gap stands, and no
  representation-theory use has been silently pointed at the
  ring-divisibility definition.
* ***aberto*** — still **0** bare-adjective links; the +183 wrong-context
  path has **not** reopened by another route. The phrase *conjunto(s)
  aberto(s)* links as a phrase, exactly as before.

### Link-volume audit (per file, not just the total)

Measured per file rather than book-wide, because a corrupted or
under-protected file shows up as one chapter with an implausibly low
count while the total still looks defensible:

| | EN | PT | ratio |
|---|---:|---:|---:|
| chapters | 2 745 | 2 705 | 98.5 % |
| solutions | 1 581 | 1 583 | 100.1 % |
| **book** | **4 326** | **4 288** | **99.1 %** |

Every one of the 46 files lands between **87 %** and **118 %** of its
English twin; no file collapsed. The four lowest are
`solutions/04-field-extensions-galois` (87 %), `05-representations`
(89 %), `20-submanifolds` (89 %) and `02-rings-arithmetic` (90 %), and
the cause was
**measured, not inferred** — each candidate was lifted in a dry run and
the delta observed:

* **−35 links, `def:b3:rings:divisibility`; −33, `def:b3:representations:rep`.**
  Both are the plural *irredutíveis*. English stoplists *irreducible* and
  lets the `local` rule link it per chapter; the plural comes free because
  `WORD_TAIL` appends `s`. Portuguese `-vel → -veis` is irregular, so the
  plural is unreachable, and `EXTRA` is global — declaring *irredutíveis*
  would send 11 representation-theory uses to the ring-divisibility
  definition. **A missing link was preferred to a wrong one.**
* **−31, `def:b3:topology:topology`.** English writes the phrase *open
  set(s)* (43 links); Brazilian Portuguese nominalises it as the bare
  adjective *um aberto*. Declaring bare *aberto*/*abertos* was tried and
  measured: it produced **+183** links (164 → 347) because it also fires
  inside *bola aberta*, *intervalo aberto*, *semiplano aberto*. Reverted.
* The remaining per-target gaps are all ≤ 6 and are ordinary
  irregular-plural losses of the same kind (*ações*, *completamentos*).

Surpluses are small and semantically correct (largest:
`def:b3:topology:continuity`, 727 vs 716, because *contínua/contínuo/
contínuas/contínuos* are four surface forms of one English word).

### Wrong-sense audit

Sampled the high-frequency single-word displays and their idiomatic traps
on **unwrapped** source: *à medida que* (0 occurrences), *livre de
quadrados* (ch. 4 only — *livre* links only in ch. 3, so no hit), *por
completo* (protected), *de base*, *em ordem*, *por partes*, *de forma*
(none of these words is linked outside its defining chapter). The
distribution of `{centro}` was compared file by file against English
`{center}` and matches it (English makes the same chapter-crossing
choice); `{fecho}` never fires inside *fecho algébrico*. No wrong-sense
link found.

## Samples

**1 — chapter opening, ch. 9 (measure theory).**

> Qual é o comprimento de um subconjunto de $\R$? A resposta ingênua ---
> atribuir a todo conjunto um comprimento invariante por translação que
> estenda o dos intervalos --- é \emph{impossível}: a construção de
> Vitali, no fim deste capítulo, produz um conjunto sem comprimento
> coerente. A teoria da medida é a retirada disciplinada: restringimos a
> atenção a uma classe rica de conjuntos \emph{mensuráveis}, sobre a qual
> existe, e é única, uma noção de comprimento enumeravelmente aditiva.

*Verdict: native.* Rhetorical question, em-dash aside, colon-and-gloss —
the Brazilian textbook cadence; *enumeravelmente aditiva* is the standard
term (the previous edition wrote *contabilidade*).

**2 — algebra, solutions ch. 3.**

> Se $M = A^n$, a projeção se restringe a um isomorfismo: $C$ seria um
> subgrupo de $\Z$ cujo elemento não nulo $x$ satisfaz $nx = 0$. Mas $\Z$
> é sem torção: $C = 0$, forçando $M = 0$ --- falso.

*Verdict: native.* *sem torção*, *forçando*, and the terse *--- falso.*
are how a Brazilian solutions manual closes a contradiction.

**3 — group theory, ch. 1 (the sentence class that broke the old draft).**

> Sejam $G$ um grupo finito e $p$ um primo tal que $p \mid \abs G$ \dots{}
> os dois conjuntos de classes laterais à esquerda coincidem, e a
> recíproca de Lagrange falha para $A_4$.

*Verdict: native.* The three named defects of the previous edition are
gone in one sentence: *Sejam* (not *Deixar*), *classes laterais à
esquerda* (not *cosets*), *recíproca* (not *conversa*).

**4 — analysis, solutions ch. 12 (Hardy's inequality).**

> A média de uma função não crescente é não crescente, de modo que $Hg$ o
> é \dots{} Para uma sequência não negativa geral, seja $(a_n^*)$ seu
> rearranjo não crescente (possível quando $a \in \ell^p$, o que podemos
> supor --- caso contrário, ambos os membros são infinitos).

*Verdict: native.* *de modo que … o é*, *ambos os membros*, *caso
contrário* — idiomatic connectives, no English clause order surviving.

**5 — probability, solutions ch. 22 (closing paragraph).**

> Em $\alpha = 1$, a série converge q.c.\ embora $\sum\abs{X_n}$ divirja
> com certeza: os sinais conspiram para se cancelar, com probabilidade
> um --- convergência por cancelamento, invisível a qualquer teste
> absoluto e, pela lei zero--um, com um veredicto determinístico ainda
> assim.

*Verdict: native.* Concessive *embora* + subjunctive, *q.c.*, *lei
zero--um*, and a closing appositive that reads as written, not rendered.

## Why not 100

Ordered by cost to the reader.

1. **~34 unreachable plural links (*irredutíveis*).** Portuguese
   `-vel → -veis` is irregular, `EXTRA` is global, and the word is
   genuinely ambiguous between ch. 2 and ch. 5. The clean fix is a
   per-chapter `EXTRA` — an enhancement to `tools/termlink/`, deliberately
   not attempted: that directory is shared by five books and gated by
   `check_book5_golden.sh`.
2. **31 unreachable *open set* links.** Brazilian usage nominalises
   *aberto*; linking it fires on every *bola aberta*. Measured, rejected.
3. **5 overfull boxes**, all one running header (below). Cosmetic, and
   fixable in one line by whoever owns the entry file.
4. **28 `EXTRA` entries still spelling out compound plurals.** Down from
   56: the `TAIL_ON_EVERY_WORD` flip retired 25 of them and the audit
   found 17 more that had always been dead. The 28 that remain are
   genuinely irregular (`-ão/-ões`, `-al/-ais`, `-vel/-veis`,
   *anel/anéis*) and only a Portuguese-aware pluraliser in
   `tools/termlink/morphology.py` could remove them.
5. **Build without babel** makes the page count and hyphenation quality
   provisional (see caveat above).
6. Register is uniformly Brazilian, but a native reviewer would still find
   a handful of places where a longer Portuguese connective could be
   traded for a shorter one; the translation is faithful before it is
   terse.

## Known state: five overfull boxes

**Not a defect to be fixed here, and deliberately not hidden.** The build
reports five `Overfull \hbox` warnings. All five are the *same* running
header, on five pages of ch. 7, at **2.72 pt** each — no prose, no
display, no figure is over-wide anywhere in the book.

Mechanism: `\omHeadMarkCapped` truncates the chapter mark to
`\headwidth − width(\bookline) − 1.5em`. For ch. 7 (*Espaços completos:
Baire, Ascoli, Stone--Weierstrass*) the truncated mark plus its `\,\dots`
overshoots by 2.72 pt. **The Dutch edition ships with exactly the same
five boxes on the same chapter** (its bookline is the same length as
Portuguese's, 48 characters); French's is longer still at 51 and lands
differently. This is a matched, known state across the series, not a
Portuguese regression.

The one lever is `\bookline` in the entry file, which this agent does not
own and has left byte-identical. Measured, for the record: rebuilding with
`Livro 5: Matemática universitária -- Ano 3` gives `Overfull \hbox` = 0
with nothing else changed (the experiment was reverted immediately). That
is a **visible cover-and-header naming change** — it would break the
parallel with the Portuguese editions of Books 3 and 4 (*Graduação 1*,
*Graduação 2*) and with every other language's pattern — so it is the
user's call, not a translator's, and the orchestrator is carrying it
upward with this measurement attached.

Two fixes were tried on this side and rejected: shortening the chapter
title (a content change that would drop one of the three names), and
`\chapter[short]{long}` — worse than the disease, because
`tools/termlink/protect.py` protects `\chapter{…}` but not
`\chapter[…]{…}`, so the optional form gets `\omterm` links inserted
*into the running header and the table of contents*.

Nothing is requested of any shared file: `styles/lang/pt.tex`,
`styles/onemath.sty`, `tools/termlink/**`,
`tools/term_config/lang_pt.py`, `tools/link_defined_terms.py`,
`tools/check_translation.sh`, `latexmkrc`, `.github/**`,
`frontmatter/preface.pt.tex` and the entry file were **not touched**.

## Files changed

| Path | Change |
|------|--------|
| `parts/bachelor-3/pt/*.tex` (23) | fully re-translated |
| `parts/bachelor-3/solutions/pt/*.tex` (23) | fully re-translated |
| `tools/term_config/book5_pt.py` | rewritten as a curated config |
| `translation_scores/book_5/pt/translation_score.md` | this file |

## Status

**Meets the ship threshold (≥ 95): 96 / 100 — unchanged after the
regeneration.** The link dimension moved by +9 links (98.9 % → 99.1 % of
English) on an unchanged, exact 130/130 target parity; that is inside the
noise of any dimension score, and no other dimension was touched, so
re-scoring would be false precision. Working tree left uncommitted for
human review; no git commit was created.
