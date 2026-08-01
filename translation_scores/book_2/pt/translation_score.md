# Translation score — Math Book 2 · Brazilian Portuguese (`pt`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 2 (High School, grades 10–12) |
| **Language** | Brazilian Portuguese (`pt`) |
| **Quality bar** | **native academic** (English is the source of truth; the ES and FR Book 2 editions were consulted as sense/structure references per `translation_instruction.md`) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **MET** |
| **Date** | 2026-07-31; term links regenerated 2026-08-01 after the shared `lang_pt.py` fix |
| **Scope of this pass** | **Full re-translation from English.** The pre-existing `pt/` tree was machine translation with a `Seja` post-fix bolted on; it was **not** used as a draft. All 35 chapters and all 35 solutions files (70 files, 25 634 lines) were re-derived from `parts/grade-1{0,1,2}/*.tex` and `.../solutions/*.tex`, then gated, term-linked, built and reviewed. `tools/term_config/book2_pt.py` was rewritten from a 40-line stub into a curated config. |

## Verdict in one line

Book 2 now reads as a **Brazilian ensino-médio textbook that happens to
mirror an English one**, not as a translated file: 35 chapters, 343 graded
exercises, 35 weekend problems, 378 solutions, all three structural gates
green, **3 872 defined-term links with full target parity against English**,
and a PDF with **0 errors, 0 undefined references and 0 overfull boxes** at
339 pages.

## Why a full re-translation

The `pt/` tree that existed before this pass was unsalvageable. Four
representative defects, all from `grade-11/pt/01-quadratic-functions.tex`
(the file the brief named):

| Pre-existing PT | English | Problem |
|-----------------|---------|---------|
| «os mais simples funções» / «o forma canônica» / «do parábola» | *the simplest functions* / *the canonical form* / *of the parabola* | gender and article agreement broken on the head noun — the most frequent defect, present in every chapter |
| «Todo função quadrática pode ser escrito» | *Every quadratic function can be written* | agreement broken across the whole clause (determiner, noun, participle) |
| «uma expressão do formulário $ax^2+bx+c$» | *an expression of the form* | *form* read as *(paper) form* → «formulário» |
| `\text{where }` left inside display math; `$a $, $ b$` | — | untranslated math text and spurious spaces inside inline math |

Machine artefacts of the *comeu* / *avião* class (sense swaps) were present
throughout. Editing that was not cheaper than writing the book; it was
rewritten. **All four classes above are now zero across the whole tree**
(`formulário`: 0; `\text{where`: 0; stray inline-math spaces: 0; gender sweep
below).

## Structural census — PT vs EN

| Item | EN | PT |
|------|---:|---:|
| Chapter files | 35 | **35** |
| Solutions files | 35 | **35** |
| `\begin{definition}` | 120 | **120** |
| `\begin{theorem}` | 64 | **64** |
| `\begin{proposition}` | 82 | **82** |
| `\begin{method}` | 55 | **55** |
| `\begin{proof}` | 146 | **146** |
| `\begin{exercise}` | 343 | **343** |
| `\begin{problem}` (weekend problems) | 35 | **35** |
| `\begin{solution}` | 378 | **378** |
| `pb:` labels | 35 | **35** |
| `\textbf{Part/Parte N ---}` headers | 140 | **140** |
| `enumerate[resume]` | 105 | **105** |
| `\begin{tikzpicture}` | 87 | **87** |
| `\begin{omfigure}` | 80 | **80** |
| `\admitted` | 3 | **3** |
| Source lines (bodies + solutions) | — | 25 634 |
| `\omterm` links | 3 906 | **3 872** |
| Distinct `\omterm` targets | 123 | **124** (EN ⊂ PT) |
| PDF pages | 330 | **339** (ES 343, FR 343) |

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | `check_translation.sh` PASSES for grade-10, grade-11 and grade-12: file completeness, identical label sets *and order*, per-environment census, exercise↔solution key parity, no duplicate labels, no `\end{…>` typos, no drafty `...`. All 35 solution-file headers match their chapter's `\chapter{…}` title exactly (scripted compare). Every weekend problem keeps its four-part skeleton and its ~20 questions one for one |
| Terminology | **97** | Brazilian school-mathematics vocabulary, taken from Brazilian practice rather than transposed: *função do segundo grau / trinômio do segundo grau*, *forma canônica*, *quadro de sinais*, *taxa de variação média*, *reta secante*, *primitiva*, *ponto de inflexão*, *progressão aritmética / geométrica* with *razão*, *mdc*, *primos entre si*, *divisão euclidiana*, *lema de Gauss*, *pequeno teorema de Fermat*, *afixo*, *forma algébrica / trigonométrica / exponencial*, *raízes $n$-ésimas da unidade*, *retas reversas*, *vetor normal*, *lei da probabilidade total*, *falácia do promotor*, *ensaio de Bernoulli*, *distribuição binomial*, *desvio padrão*, *lei dos grandes números*, *média amostral*, *intervalo de flutuação*, *ausência de memória*, *paradoxo da inspeção*, *escore z*, *passeio* / *grafo orientado* / *matriz de adjacência*. Brazilian, not European, throughout: **0** occurrences of `travagem`, `autocarro`, `ecrã`, `telemóvel`, `comboio`, `betão`, `ficheiro`, `rapariga` |
| Register / tone | **96** | Brazilian upper-secondary register: **2nd-person imperative** in every exercise and problem stem (*Calcule, Determine, Mostre, Demonstre, Deduza, Resolva, Verifique, Explique, Conclua, Compare*), applied uniformly across all three years — what a Brazilian exercise list actually says. Chapter hooks are written, not rendered: «Uma matriz é uma máquina que come um estado e devolve o seguinte», «Por que os cassinos sempre ganham no fim, e por que as pesquisas de opinião funcionam?», «Fatie um cubo e você espera quadrados e retângulos --- e, no entanto, um corte famoso produz um hexágono regular». Uniform *você* address, no *tu* and no *vós* leakage |
| LaTeX hygiene | **99** | 0 fatal errors, 0 undefined references, **0 overfull boxes**, 119 underfull (EN 120, ES 118, FR 117 — series norm). **0** TeX accent escapes anywhere in the `pt` tree (UTF-8 only): English's `Bienaym\'e`, `Vi\`ete`, `\"Otzi` are *Bienaymé*, *Viète*, *Ötzi*. The one overfull box the first build produced (the modulus-properties display in `grade-12/pt/09`, where «(desigualdade triangular)» is longer than «(triangle inequality)») was fixed at source by splitting the display in two, not by fudging spacing |
| Cross-refs / rule compliance | **98** | Every `\label{…}`, every `\cref`/`\ref` target and every `\begin{solution}{…}` key is byte-identical to English — the label diff is empty for all three years. **0 curriculum, exam or country names** in visible text; cross-volume pointers are uniformly «o volume do ensino fundamental» / «do ensino médio» / «dos volumes de graduação», and intra-book pointers are «o ano 10 / 11 / 12», matching the part titles in `styles/lang/pt.tex`. The only bare `\ref` is the mandated `\section*{Capítulo \ref{ch:…} --- …}` solutions header |
| Figures | **98** | TikZ/pgfplots drawing code copied byte for byte (87 `tikzpicture`, 80 `omfigure`, both = EN); only node text, legends, axis labels and `{\small …}` captions are Portuguese. Coded node labels were localized where the code is a word and left where it is a name: *S/F* stays *S/F* (sucesso/fracasso) in the Bernoulli tree, *D/T* stays *D/T* (doente / teste) in the screening tree, *true/false positives* → «positivos verdadeiros» / «falsos positivos». Decimal points inside figures left as in EN so text and figures agree |
| Solutions | **97** | All 378 present, each with the `\emph{1.}` / `\textbf{1.}`…`\textbf{20.}` numbering of its English twin and the same numerical answers, spot-checked value by value across the volume: Cassini's $(-1)^n$, $\gcd(1071,462)=21$ with $u=-3,\ v=7$, $n \equiv 23 \pmod{105}$, the regular hexagon's $\frac{3\sqrt3}{4}$, the $109.5^\circ$ diamond angle, the $\frac16$ Bayes screening verdict, the $27\sigma$ casino, $\frac{13\,000}{200}=65$ for the inspection paradox, $5\,094$ positives out of $100\,000$ |
| MT-artifact freedom | **97** | **0 residual English** in prose (the only English tokens in the tree are TikZ/pgfplots keywords such as `fill between`, `name path`, `function`). **0 gender/article agreement errors**: a scripted sweep of 40 feminine and 38 masculine head nouns against masculine and feminine determiners over all 70 files (with `\omterm` wrappers stripped first) returns 6 hits, all of them the *preposition* «a» (*resistente a valores extremos*, *termo a termo*, *caso a caso*) — zero real slips. English participial and nominal chains were re-cast as Portuguese finite clauses rather than transposed: *"Long considered the purest of pure mathematics…"* → «G.\,H.~Hardy gabava-se, em 1940, de que a teoria dos números era “imaculada” por aplicações»; *"the drift outruns the noise"* → «a deriva supera o ruído». Idioms localized, not calqued: *the house always wins* → «a casa sempre ganha», *gambler's fallacy* → «falácia do apostador», *free lunch* → «almoço grátis», *too close to call* → «empate técnico», *skew lines* → «retas reversas», *bumped passenger* → «passageiro preterido» |

**Overall: 96.** Weighting register, terminology and MT-artifact freedom above
structure (structure being separately gated), the edition ships.

## Structural / build gates

> **Measurement note.** pdfTeX writes `build/*.log` as ISO-8859 text, so a
> plain `grep -c` treats it as binary and prints nothing (which reads as
> "0"). **All counts below were taken with `grep -a`.**

> **Babel caveat.** `brazilian/portuguese.ldf` is not installed in this
> environment, so `styles/onemath.sty` correctly falls back to building
> Portuguese **without babel** (English hyphenation patterns; UI strings still
> come from `styles/lang/pt.tex`). The overfull/underfull counts and the page
> total below are therefore *provisional*: with `texlive-lang-portuguese`
> installed, Portuguese hyphenation will change line breaking. No overfull box
> survives even with English hyphenation, which is the harder case.

| Gate | Command | Result |
|------|---------|--------|
| Structure, grade-10 | `bash tools/check_translation.sh grade-10 pt` | **PASSED** |
| Structure, grade-11 | `bash tools/check_translation.sh grade-11 pt` | **PASSED** |
| Structure, grade-12 | `bash tools/check_translation.sh grade-12 pt` | **PASSED** |
| Build | `latexmk one_math_book_2_high_school_pt.tex` | exit 0 |
| Fatal errors | `grep -ac '^!' build/…_pt.log` | **0** |
| Undefined references | `grep -aci 'undefined' build/…_pt.log` | **0** |
| Overfull `\hbox` | `grep -ac 'Overfull' build/…_pt.log` | **0** |
| Underfull `\hbox` | `grep -ac 'Underfull' build/…_pt.log` | 119 (EN 120, ES 118, FR 117 — series norm) |
| `Missing character … nullfont` | `grep -ac 'Missing character'` | 50 — **identical in EN, ES and FR**; a shared-figure artefact, not a PT defect |
| PDF | `build/one_math_book_2_high_school_pt.pdf` | **339 pp**, 2.6 MB |
| Term links | `link_defined_terms.py --book 2 --lang pt --unwrap --apply` then `--apply` | **3 872** links across 70 files; targets `def 3621, prop 101, pb 66, thm 36, met 31, ex 17` (EN 3 906 — a 34-link gap, 0.9 %) |
| Term-link idempotence | `link_defined_terms.py --book 2 --lang pt --check` | «every file matches what the config generates» |
| Omterm target parity vs EN | `diff` of sorted target sets | **EN ⊂ PT — zero English targets missing.** One PT-only target, `thm:g12:contdist:memoryless` («ausência de memória»), which ES and FR also carry: English's one-word *memorylessness* is skipped by the index-only harvest, the Portuguese phrase is not |
| Exercise ↔ solution parity | per-chapter `diff` of label lists | all 35 chapters match |
| Chapter-title parity body ↔ solutions header | scripted compare | all 35 pairs match |
| Duplicate labels | `grep -rho 'label{…}' \| uniq -d` | none |
| TeX accent escapes | gate + targeted grep | **0** |
| European-Portuguese lexicon | targeted grep (`travagem`, `autocarro`, `ecrã`, `telemóvel`, `comboio`, `betão`, `ficheiro`, `rapariga`) | **0** |
| Curriculum / exam / country names | targeted grep | **0** |
| Residual English prose | whole-word grep over 35 English function words | **0** (only TikZ keywords) |
| Gender/article agreement | scripted 78-noun × 12-determiner sweep, links stripped | **0** real slips |

## The term-link config, rewritten

`tools/term_config/book2_pt.py` grew from a 40-line stub (2 939 links and a
large wrong-sense tail) to a curated config. Three homographs are
**Portuguese-only** and are most of the story:

| Homograph | Wrong sense | Handling | Effect |
|-----------|-------------|----------|--------|
| **módulo** | the Latin *modulo n* of the arithmetic chapter (English keeps *modulus*/*modulo* apart, French *module*/*modulo*) | `EXTRA_PROTECT` on `módulo` + its argument | wrong links in `grade-12/…/10-arithmetic` went **34 → 0**; **50** suppressed book-wide, measured (ES ships 35) |
| **amplitude** | the amplitude of an oscillation / of a seismic wave, vs the statistical range | soft `STOP` alone — it confines the term to the chapter that defines it | 5 wrong links removed. (The five phrase guards this file used to carry alongside the `STOP` were **measured to suppress nothing** and were deleted — see the 2026-08-01 addendum.) |
| **intervalo** | the *gap between two buses* of the inspection paradox | 9 phrase guards confined to `grade-12/…/16` | **22** wrong links suppressed, measured by deleting the group; ES ships 12 of them |

Plus the Portuguese idiom trap **«no máximo» / «no mínimo»** (= *at most* /
*at least*, not the extrema of a function): **27** wrong links suppressed,
measured, with a negative lookahead so the genuine «no máximo local» survives. `ímpar` and
`par` are soft-`STOP`ped to chapter-local, exactly as English keeps *odd* and
*even* chapter-local. `NOT_A_TERM` gained `lei da` so that «lei da
probabilidade total» counts as a result, not a notion — the parity of
English's own `law of`. `DERIVED` declares the gender×number forms Portuguese
inflects and English does not (*contínua/contínuo/contínuas/contínuos*,
*convexa*, *côncava*, *monótona*, *limitada*, *derivável*), plus the two
aliases that close the last target gaps: `fatorial → fatoriais` and
`frequência relativa → frequência/frequências`. All `EXTRA_PROTECT` patterns
obey the "never consume a `$`" rule of `tools/termlink/protect.py` (every
math-adjacent guard ends in a lookahead).

Two source-side changes were made *for* the link layer, both improvements in
their own right: **«escore $z$» → «escore z»** (a display containing math can
never be linked, since the shared rule masks math; ES writes «puntuación z»
for the same reason), and «usa a lei normal» → «usa a distribuição normal» in
the `grade-12/16` hook.

### Addendum — 2026-08-01: `lang_pt.py` `TAIL_ON_EVERY_WORD` fix

`tools/term_config/lang_pt.py` was flipped to `TAIL_ON_EVERY_WORD = True`
**by the orchestrator** (APPLIED, not by this pass — the file is shared and was
not edited here). Portuguese agrees every word of a noun phrase, so with the
tail on the last word only the regex asked for *"número primos"* and **no
plural of a multiword term was ever generated**. Book 2 was regenerated
against the corrected rule.

**1 — Workarounds trimmed.** Of 11 `DERIVED` bases and 6 `EXTRA` entries, the
compound-plural workarounds were removed and the genuinely irregular forms
kept:

| Removed (WORD_TAIL now spells it) | Kept, and why |
|---|---|
| `"número primo": ["números primos"]` — the whole entry | `"permutação": ["permutações"]` (-ão → -ões) |
| `"contínuas"`, `"contínuos"`, `"convexas"`, `"convexos"`, `"côncavas"`, `"côncavos"`, `"monótonas"`, `"monótonos"`, `"limitadas"`, `"limitados"` — regular plurals of the base or of the declared masculine | `"contínua": ["contínuo"]` etc. — **gender**, which the flag does not touch; the masculine's own plural now comes free |
| `"frequências"` — regular plural of the declared `"frequência"` | `"derivável": ["deriváveis"]` (-vel → -veis), `"fatorial": ["fatoriais"]` (-al → -ais), `"distribuição normal": ["distribuições normais"]` (both words irregular) |
| — | `EXTRA` untouched: `"vetores normais"` (-al → -ais), `"invertíveis"` (-vel → -veis), `"ortogonal"`/`"coplanar"`/`"colinear"` (singulars the tail cannot *strip* back to) |

**2 — The `ordem de grandeza` check, done by measurement, not by re-reading.**
For every linkable term, the true Brazilian plural (-ão → -ões, -al → -ais,
-m → -ns, -r → -res, -vel → -veis) was counted in the sources and compared with
the number actually linked. The audit found **22 terms with unlinked irregular
plurals**, worth ~240 occurrences — exactly the trap physics hit with
*ordem de grandeza*. Fourteen of them are unambiguous and were declared:
`equação → equações` (49 links alone), `imagem → imagens`,
`pré-imagem → pré-imagens`, `aproximação → aproximações`,
`interseção → interseções`, `união → uniões`, `integral → integrais`,
`ortonormal → ortonormais`, `parte real → partes reais`,
`função afim → funções afins`, `função quadrática`, `função ímpar`,
`equação diferencial`, `número natural`. Four candidate entries with **zero**
occurrences in the sources were dropped again rather than left as decoration.
Re-run of the audit afterwards: **0 unambiguous irregular plurals unlinked**
(the single remaining hit, `números naturais`, is the defining
`\emph{}\index{}` span itself, which is protected by design).

**3 — Counts.** 3 716 → **3 872** links (+156), **0 links lost**, 36 new
display forms. English is 3 906: the residual gap is **34 links (0.9 %)**,
against 190 before the flip. Target parity is unchanged: **EN ⊂ PT**, with the
same single PT-only extra.

**4 — Every newly reachable link was audited before being kept.** The 36 new
display forms are all compound plurals of correct sense (`equações`,
`pré-imagens`, `pontos fixos`, `pontos médios`, `desvios padrão`, `escores z`,
`coeficientes angulares`, `integrais`, `partes reais`, `funções afins`,
`ensaios de Bernoulli`, `vetores diretores`, …). The four curated guards were
re-verified **on unwrapped source**, since an already-inserted link hides the
evidence of itself:

| Guard | After the flip |
|---|---|
| **módulo** (arithmetic *modulo n*) | 0 wrong links in `grade-12/…/10-arithmetic`; the plural `módulos primos` is covered by the existing `\s+primos?` guard |
| **amplitude** | still chapter-local: links appear only in `grade-10/…/08-statistics`, including the newly reachable `amplitudes` |
| **intervalo** (bus gap) | all 9 links in `grade-12/…/16` are the mathematical interval; the newly reachable `intervalos longos` is covered by the existing plural alternation |
| **«no máximo» / «no mínimo»** | the flip exposed a pre-existing miss: the guard was `\bno\s+…`, so the sentence-initial `«No máximo $4$»` in `grade-10/solutions/pt/09` was linked. Widened to `\b[Nn]o\s+…`; the genuine «no máximo local» still links (verified, 1 hit) |

One further wrong-sense occurrence surfaced with `imagens` and was fixed **at
source rather than with another lexical guard**: the `grade-10/…/06-vectors`
figure caption «Duas imagens da soma» is English's *"Two pictures of the sum"*,
not the image of a function — now «Duas visões da soma».

**5 — All four silent-failure rules verified on this config.** `EXTRA_PROTECT`
was audited against every known way a protect pattern fails without erroring:

| Rule | Result |
|---|---|
| 1. never consume a `$` | **PASS** — every math-adjacent guard ends in a lookahead (the failure that cost physics 270 links and Book 1 235) |
| 2. never write a literal space (`re.S` + LaTeX line wrapping) | **PASS** — `\s+` throughout |
| 3. audit on **unwrapped** source | done: the corpus was unwrapped in memory (residual `\omterm` = 0) before every match count below, since an inserted wrong link hides the evidence of itself |
| 4. a pattern that matches nothing, or suppresses nothing, is dead | **two found and removed** — see below |

Rule 4 was applied twice, in both of its forms. `[Mm][óo]dulos?\s+(?=\d)`
matched **zero** times: every modulus in this book is written in math mode
(`módulo $9$`, 44×), never as a bare digit (0×) — a pattern that looked
protective and never fired, exactly Book 4's `polin[óo]mios` failure.
And the **five «amplitude» guards matched text but suppressed nothing**: the
soft `STOP` already confines the term to its defining chapter, so deleting all
five moved the link count by **0**. Both were removed; the config went 24 → 18
patterns and the link count did not change, which is the correct verification
for removing a dead pattern.

Every surviving group was then measured by deleting it and re-running the
linker — a guard is kept only if the number moves:

| Guard group | Wrong-sense links it actually suppresses |
|---|---:|
| `módulo` (2 patterns) | **50** |
| `no máximo` / `no mínimo` | **27** |
| `intervalo` (9 patterns) | **22** |
| `raiz quadrada` / `raiz cúbica` | **9** |
| `divide o risco` | 2 |
| `identidade complementar` | 2 |
| `os dois extremos` | 1 |
| **total** | **113** |

On the Portuguese accent trap behind rule 4: the three character classes in
this file (`[ií]`, `[úu]`, `[óo]`) were checked against **every spelling that
occurs in the corpus** — `raiz` 58 / `raízes` 90, `cúbica(s)` 10, `módulo(s)`
70 — and none of those words takes a circumflex, unlike *polinômio*, *ângulo*,
*têm*. No accent hole.

**6 — Residual gap, and why it is not a defect.** Two classes stay out of
reach, both documented in the new `lang_pt.py` docstring:

* **Gender.** `WORD_TAIL` covers number only; a term harvested as `contínua` is
  unreachable as `contínuo` unless declared. This book declares the five that
  occur, so its gender loss is ~0 — but the mechanism is manual.
* **Irregular plurals of *ambiguous* terms.** `DERIVED` and `EXTRA` only extend
  the *unambiguous* map, so a spiral term such as `função` (defined in grade 10
  *and* grade 11) cannot receive `funções` without forcing one of the two
  senses on every use and breaking `nearest-preceding`. Measured cost: **105
  occurrences** — `funções` 65, `variáveis aleatórias` 12, `distribuições` 9,
  `quartis` 9, `deriváveis` 6, `coeficientes binomiais` 2,
  `progressões aritméticas/geométricas` 2. This is the whole of the remaining
  34-link gap against English and more; closing it needs a `-ão → -ões` rule in
  the shared morphology, not a per-book config.

**Score: unchanged at 96/100.** This round changed link coverage and one figure
caption, not prose: terminology, register and MT-artifact freedom are measured
on the same text as before. The link improvement is real but sits inside
dimensions already at 97–99, and the newly documented ambiguous-plural gap
offsets it.

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| `grade-10/pt/01-numbers-and-sets.tex`, chapter hook — «A matemática começa com os números, e nem todos os números são da mesma espécie: os que servem para contar, os negativos, as frações e números como $\sqrt 2$ ou $\pi$ que nenhuma fração consegue exprimir.» | **native** — «os que servem para contar» is the Portuguese way to nominalize; a translator produces «os números de contagem». «consegue exprimir» for *can express* is the idiomatic modal, not «pode expressar» |
| `grade-11/pt/01-quadratic-functions.tex`, the file the brief named — «As funções quadráticas são as mais simples depois das lineares, e as primeiras cujos gráficos são de fato curvos. Este capítulo desenvolve a caixa de ferramentas completa para elas: a forma canônica, o discriminante, o sinal de uma expressão do segundo grau e a geometria da parábola.» | **native** — every determiner now agrees (*as mais simples*, *a forma canônica*, *o discriminante*, *da parábola*); the relative «cujos gráficos» is the compact Portuguese construction, and *of the form* is «da forma», never «do formulário» |
| `grade-12/pt/10-arithmetic.tex`, weekend-problem opening — «G.\,H.~Hardy gabava-se, em 1940, de que a teoria dos números era “imaculada” por aplicações. Oitenta anos depois, cada bipe de código de barras, cada pagamento com cartão e cada mensagem cifrada o desmentem.» | **native** — *gabar-se de que* with its preposition and the imperfect, and the tricolon in Portuguese rhythm; *boasted* is not calqued as «se vangloriou» |
| `grade-12/solutions/pt/16-continuous-distributions.tex`, q14 — «*o intervalo que por acaso você inspeciona não é um intervalo típico, porque você tinha mais chance de cair em um intervalo grande.*» | **native** — «por acaso» carries English's *you happen to* idiomatically; the imperfect «tinha» is the correct Portuguese tense for the counterfactual sampling frame |
| `grade-12/pt/11-matrices-graphs.tex`, problem opening — «Uma matriz é uma máquina que come um estado e devolve o seguinte --- e suas \emph{potências} guardam, portanto, futuros inteiros.» | **near-native** — lively and correct, but «come» is colloquial in an otherwise academic sentence; an editor might prefer «consome». Kept because the English is deliberately colloquial there too |

## Why not 100 — ordered gap list

1. **«razão» collapses two English terms.** In Brazilian usage the ratio of a
   *progressão aritmética* and of a *progressão geométrica* are both «razão»,
   so the harvest sees one word defined twice in one chapter and drops it.
   English links *common difference* and *common ratio* separately; Portuguese
   cannot without inventing terminology no Brazilian textbook uses. The prose
   is right; two link families are lost.
2. **Decimal point, not decimal comma.** `0.5`, `1.96`, `95.4` keep the
   English point. Brazilian school books print `0,5`. This is a deliberate
   series-wide convention (EN, ES, FR and NL all do it, and the point is baked
   into the shared TikZ/pgfplots figures, which are copied byte for byte), so
   changing it in PT alone would break figure/text consistency — but it is the
   single most visible non-native detail on the page. See "Shared-file notes".
3. **`\gcd` prints "gcd", not "mdc".** In math mode the shared `\gcd` operator
   is used throughout; the prose says *máximo divisor comum* / *mdc*. ES
   (*mcd*), FR (*pgcd*) and NL (*ggd*) have exactly the same gap, because
   `\gcd` is LaTeX's own operator and is not language-aware in
   `styles/onemath.sty`. Fixing it is a **shared-file** change, deliberately
   not made here.
4. **The percent convention is inherited, not normalized.** PT has 56
   `$x\,\%$` against 64 bare `$x\%$` — English itself is split 105/62, and the
   split does not fall the same way file by file. No rendering risk (PT loads
   no babel, so the `spanish.ldf` `\%` hazard does not apply), but a reader can
   meet both spellings within a few pages. Normalizing would mean diverging
   from the canonical source position by position.
5. **Irregular plurals of *ambiguous* terms are unreachable.** `DERIVED` and
   `EXTRA` extend only the unambiguous term map, so a spiral term such as
   *função* (defined in grade 10 and again in grade 11) cannot be given its
   irregular plural *funções* without forcing one sense on every use and
   breaking `nearest-preceding`. Measured cost: 105 occurrences — and it is,
   with gap 1, the whole of the remaining 34-link gap against English. Closing
   it needs a `-ão → -ões` rule in the shared morphology (see the 2026-08-01
   addendum), which is a shared-file change.
6. **`EXTRA_PROTECT` guards are lexical, not syntactic.** The «módulo»,
   «intervalo» and «no máximo» guards enumerate the phrase shapes that actually
   occur (113 wrong links suppressed, each group measured); a future chapter
   using one of those words in the same wrong sense with a new phrase shape
   would be linked wrongly until the config is extended. A syntactic guard is
   out of scope for a per-book config. Mitigation in place: every pattern is
   annotated in `book2_pt.py` with the count it suppresses, so a guard that
   silently stops firing after an edit shows up as a changed number.
7. **339 pp against EN's 330 (+2.7 %).** Portuguese runs longer than English
   by nature and the figure sits *below* ES (343) and FR (343), so density is
   in series norm — but two or three of the longest solution files
   (`grade-12/16`, `grade-12/15`, `grade-12/13`) could each be tightened by a
   line or two.
8. **119 underfull boxes, and provisional line breaking.** Reported for
   completeness: English itself has 120 and every language edition is in the
   same range. The count will move once Portuguese hyphenation is available
   (see the babel caveat above).

## Shared-file notes

Nothing outside my scope was edited. `styles/onemath.sty`,
`styles/lang/pt.tex`, `styles/onephysics.sty`, `latexmkrc`,
`.github/workflows/`, `tools/termlink/`, `tools/link_defined_terms.py`,
`tools/check_translation.sh`, the other books' `book<N>_pt.py`, the entry file
`one_math_book_2_high_school_pt.tex` and `frontmatter/preface.pt.tex` are all
untouched. **`tools/term_config/lang_pt.py` was flipped by the orchestrator,
not here**, and was not edited by this pass. `git status` confirms this pass
changed exactly 71 files: the 70 bodies under `parts/grade-1{0,1,2}/pt/` and
`parts/grade-1{0,1,2}/solutions/pt/`, plus `tools/term_config/book2_pt.py`.

Three shared-file / environment changes would raise the ceiling and are left
for the owner to decide:

- **Install `texlive-lang-portuguese`.** Not a repo change: `onemath.sty`
  already emits the right warning and falls back cleanly. With the `.ldf`
  present, Portuguese hyphenation replaces English and the line-breaking
  numbers above become final. (Same situation as FR/NL on a minimal install.)
- **`\gcd` → `mdc` / `mcd` / `pgcd` / `ggd`** — a `\booklang`-switched
  `\DeclareMathOperator` in `styles/onemath.sty` would fix gap 3 for PT, ES,
  FR and NL at once.
- **Decimal separator** — a language-aware decimal macro (or a
  `\DeclareMathSymbol`-level comma) would fix gap 2 for PT/ES/FR/NL, but only
  if the shared TikZ figures are migrated to it in the same change.
- **A `-ão → -ões` (and `-al → -ais`, `-m → -ns`, `-vel → -veis`) rule in
  `tools/termlink/morphology.py` for `pt`** would close gap 5 — the 105
  occurrences that per-book `DERIVED`/`EXTRA` cannot reach because the terms
  are spiral-ambiguous. Portuguese needs it more than Spanish does, since
  `-ão` is its commonest noun ending.

**`frontmatter/preface.pt.tex` — one change needed, not made.** The preface is
otherwise good native Portuguese («O estilo é conciso e rigoroso: cursos
construídos a partir de definições, exemplos, proposições e teoremas…»), but
one phrase is European rather than Brazilian: «do primeiro ano do ensino
fundamental ao último **da secundária**». Brazilian usage is «do ensino
médio», which is also the wording this edition uses for every cross-volume
pointer in the 70 bodies. The file is shared across all PT editions and is
off-limits to this pass, so the fix is reported here rather than applied
(one-word change: `da secundária` → `do ensino médio`).

## Status

**Meets the ship threshold (≥ 95).** No git commit was created; the working
tree is left for human review.
