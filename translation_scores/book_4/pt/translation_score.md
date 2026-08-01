# Translation score — Math Book 4 · Portuguese (`pt`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 4 (University Year 2, `bachelor-2`) |
| **Language** | Brazilian Portuguese (`pt`) |
| **Quality bar** | **native academic** (English is the source of truth; the `es` and `fr` editions of the same book were used as method comparands, never as sources) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **met; no blockers remain** |
| **Date** | 2026-07-31; term-link layer regenerated 2026-08-01 after the `lang_pt.py` flip |
| **Scope of this pass** | **Full re-translation from English.** All 23 chapters and all 23 solution files re-derived from the English canon with a structure-preserving placeholder pipeline; the pre-existing `pt/` bodies were consulted only to see what had to be undone, never edited in place. The term-link config was rewritten from scratch. First time this edition has been scored under the native-academic bar. |

## Verdict in one line

A freshly derived, native-register Brazilian second-year course: exact
structural mirror of English, a curated term-link layer whose target set is
identical to English's in both directions, and a build with zero errors, zero
undefined references and zero overfull boxes.

## What the previous edition looked like

The 90/100 pass this replaces was machine translation with the failure modes
the brief named, all of which are gone: 250 × `Deixar` for *Seja/Sejam*,
`Desde que` for *Como/Uma vez que*, **`contabilidade`** for *enumerabilidade*,
`conversa` for *recíproca*, `aula` for *classe*, untranslated `coset`, English
word order (*"no Ano 1 volume"*, *"equivalência e ordem relações"*, *"tools of
the trade"*), unconjugated infinitives (*"anéis de quociente **dirigir**
aritmética"*), English inside display math (`\text{where }`, `\text{ if }`,
`\text{ and }`, `\text{ for all }`, `(\text{equality for injective } f)`),
`mapa` for *aplicação* and `campo` for *corpo*. Automated sweeps for every one
of those strings now return **0 hits**; the surviving `contabilidade` (11
sites) is the ordinary Portuguese noun for *bookkeeping*, used where English
uses that word ("dispositivo de contabilidade", "contabilidade radial"), and
every `campo` (13 sites) is a vector or force field.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror: 23 chapters / 23 solution files both sides; 276 `exo:` + 23 `pb:` labels EN and PT; 299 `\begin{solution}{…}` both sides; 30 `tikzpicture` both sides. `check_translation.sh bachelor-2 pt` **PASSED** |
| Terminology | **97** | Brazilian university register throughout: *corpo* (never *campo* for a field), *aplicação* (never *mapa*), *anel*, *classe lateral* (never *coset*), *autovalor / autovetor / autoespaço*, *posto*, *traço*, *núcleo*, *fecho*, *enumerável*, *somável*, *envoltória convexa*, *transformação de Abel*, *relações de Girard*, *desigualdade do valor médio*, *regra da cadeia*, *wronskiano*, *ressonância*, *forma quadrática*, *baricentro*, *passeio aleatório*, *função geradora*, *prole total*, *evento* (Brazilian usage, not the Iberian *suceso*), *esperança*, *desvio padrão*. No MT sense swaps found in sampling |
| Register / tone | **96** | Reads as a Brazilian second-year course, not a translation: «Esses resultados estruturais são curtos, afiados e muito queridos pelos examinadores»; «uma carta, duas curvas desenhadas, e o plano tangente inteiro é gerado»; «Um bêbado encontra o caminho de casa; um pássaro bêbado talvez não»; «probabilidades pequenas são um domínio em que a intuição precisa da exponencial, não da régua» |
| LaTeX hygiene | **99** | 0 fatal errors, 0 undefined references, **0 overfull boxes**. 0 TeX accent escapes (`Bézout`, `Fejér`, `Cesàro`, `Möbius`, `Hölder`, `Arzelà`, `Schrödinger`, `Lindelöf`, `Pólya` all UTF-8); all 46 files valid UTF-8; no nested `\omterm`; no drafty `...` |
| Cross-refs / rule compliance | **99** | `\label`, `\cref`/`\ref` targets and `\begin{solution}{key}` byte-identical to English. 0 duplicate labels. No cross-volume `\cref` leakage (`…b1:`, `…b3:`, `…g1x:` all empty). No curriculum or country names in visible text — cross-volume references read "volume do primeiro ano de graduação" / "volume do terceiro ano de graduação" / "volume do ensino médio" throughout (78 sites) |
| Term-link layer | **96** | `tools/term_config/book4_pt.py` rewritten from 34 lines to a curated config, then trimmed against the 2026-08-01 `lang_pt.py` flip. 3 677 links, **85 targets — identical set to English, both directions**. `--check` green and idempotent |
| Figures | **98** | TikZ/pgfplots drawing code byte-identical to English; only node text, legends, axis labels and captions localized |
| Solutions | **97** | All 299 solutions present, native and complete; localized `\section*{Capítulo … --- <título>}` headers with `ch:…` slugs unchanged |
| MT-artifact freedom | **97** | Automated English-word sweep over the 46 files returns 0 prose hits (the residual matches are TikZ option words: `below`, `left`, `right`, `very thin`). The four English `\index{}` keys that survived inside display math (`Euler's theorem`, `Stirling's formula`, `Jensen's inequality`, `spectral theorem`) were found and localized; the EN ∩ PT index-key intersection is now **1 key** (`ideal`, genuinely identical) |

**Overall: 96** — weighted toward terminology, register, term-link quality and
MT-artifact freedom, since structure is already gated by
`check_translation.sh`.

## Structural / build gates (measured 2026-07-31; link counts re-measured 2026-08-01)

> **Note for whoever re-measures these:** the pdfTeX log is ISO-8859-encoded,
> so a plain `grep -c` treats it as binary and prints nothing, which reads as
> "0". Use `grep -a`, or read the log from Python with `errors='replace'`
> (what was done here).

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-2 pt` | **PASSED** |
| `latexmk one_math_book_4_university_year_2_pt.tex` | exit 0 |
| Fatal errors (`grep -ac '^!'`) | **0** |
| Undefined references (`grep -aci 'undefined'`) | **0** |
| Overfull `\hbox` (`grep -ac 'Overfull'`) | **0** |
| PT PDF | `build/one_math_book_4_university_year_2_pt.pdf`, **409 pp** (EN 397, FR 417, ES 418, NL 419) — normal Portuguese expansion, no MT padding |
| `python3 tools/link_defined_terms.py --book 4 --lang pt --check` | **green** — 3 677 links across 46 files, every file matches the config, idempotent |
| `\omterm` first-arg parity vs English | **identical sets, both directions** (85 targets) |
| Exercise ↔ solution key parity | **0 divergences** (276 `exo:` + 23 `pb:` ↔ 299 `\begin{solution}`) |
| Duplicate labels in the `pt` tree | **0** |
| Cross-volume `\cref` leakage | **0** |
| TeX accent escapes / non-UTF-8 files | 0 / 0 |
| Index keys: EN ∩ PT intersection | **1 key** (`ideal`) |
| Article + `\cref` agreement | 294 article-before-`\cref` sites, **all** with a non-breaking `~`, **0 gender disagreements** (`o/do/no/ao/pelo` for `thm/lem/cor/met/ex/exo/pb/ch`, `a/da/na/à/pela` for `prop/def/rem/not/fig/tab/sec`) |
| European-Portuguese sweep | 0 hits for `travagem`, `autocarro`, `ecrã`, `telemóvel`, `comboio`, `betão`, `ficheiro`, `rapariga`, `facto`, `contacto`, `acção`; the single `óptica` was corrected to `ótica` |

**Babel caveat (important when re-measuring):** `brazilian/portuguese.ldf` is
**not installed** on this machine —
`Package onemath Warning: brazilian/portuguese.ldf not found; building
Portuguese without babel`. The book therefore builds with **English
hyphenation patterns**. The overfull/underfull counts and the 409-page total
above are consequently **provisional**: with `texlive-lang-portuguese`
installed, line breaking will change, most of the 108 underfull boxes should
disappear, and new overfull boxes could in principle appear. The two overfull
boxes this pass did produce were fixed by tightening prose (see below); the
`_pt` entry file has **no `\emergencystretch`**, unlike the FR/NL/ES entries,
so there is no elastic hiding a bad line here.

**Not gated, for the record:** 108 underfull `\hbox`/`\vbox` warnings. This is
the series norm (EN 104, ES 112) and is aggravated here by the missing
hyphenation patterns.

## What was rewritten, and how

1. **Everything.** All 46 body/solution files are fresh derivations from the
   English canon. The method: each English file was mechanically split into a
   *skeleton* of prose with `@@N@@` placeholders and a *slot table*, with every
   `$…$`, `\[…\]`, math environment, `tikzpicture`, `\label`, `\cref`, `\index`
   sort key, `\includegraphics`, `\begin{solution}{key}` and the **first
   argument of every `\omterm`** protected byte-for-byte; the prose was then
   authored in Portuguese against the skeleton and rebuilt, with the builder
   refusing any file with a missing, duplicated or extra placeholder. TikZ node
   texts, `xlabel=`/`ylabel=`/`title=`/`\addlegendentry` and captions were
   lifted into the slot table and translated there, so figure *drawing* code is
   provably byte-identical while figure *text* is Portuguese.
2. **`tools/term_config/book4_pt.py`** — rewritten from 34 lines to a curated
   config. The inherited file had `DROP = set(STOP)`, which hard-dropped every
   stoplisted word (destroying the soft "still linked in its defining chapter"
   behaviour), an empty `DERIVED`, an empty `EXTRA` and an empty
   `EXTRA_PROTECT`. Three Portuguese-specific problems were solved:
   - **`TAIL_ON_EVERY_WORD` was `False`** in the shared `lang_pt.py`, so the
     optional plural tail was tried on the *last word only* and *forma
     quadrática → formas quadráticas*, *espaço métrico → espaços métricos*,
     *anel quociente → anéis quociente* were all missed. 76 phrase plurals were
     declared by hand. **The flag was flipped to `True` by the orchestrator on
     2026-08-01** and this table was trimmed accordingly — see the addendum.
   - **Gender agreement and nominalisation**: *compacto/compacta/compacidade*,
     *completo/completa/completude*, *conexo/conexa/conexidade*,
     *contínua/contínuo/continuidade/continuamente*,
     *enumerável/enumeráveis/enumerabilidade*, *somável/somabilidade*,
     *independentes/independente/independência*, … — 21 adjective families.
   - **Targets English reaches through a bare word the Portuguese definition
     does not emphasise**: `def:b2:structures:algebra` (English links the bare
     *algebra*; the Portuguese definition emphasises `$K$-álgebra`),
     `def:b2:structures:generated` (English links the bare *order*),
     `def:b2:hermitian:adjoint` (*unitary*). Declared in `EXTRA` and fenced
     with `EXTRA_PROTECT`.
   The eight targets the brief listed as never linked in Portuguese —
   `def:b2:linalg:det`, `def:b2:series:summable`,
   `def:b2:structures:quotientring`, `def:b2:surfaces:param`,
   `def:b2:proba:conditional`, `def:b2:diffeq:wronskian`,
   `def:b2:nvs:equivalent`, `def:b2:structures:algebra` — are all linked now.
3. **`AMBIG_POLICY` decision: kept `"drop"`, deliberately.** The brief asked
   for this to be decided rather than inherited. `"drop"` is right here for two
   independent reasons. (a) It is what `book4_en.py` uses, and the gate this
   edition is measured against is *sense parity with English*: under
   `"nearest-preceding"` the Portuguese book would link words English leaves
   alone, and the two books would disagree about what a term means. (b) The two
   terms the harvester reports as defined twice in this book are exactly the
   ones that would be mis-sent: *compacto* (a compact space in ch. 4, a compact
   operator later) and *adjunto* (the Euclidean adjoint of ch. 12 and the
   Hermitian adjoint of ch. 13, defined 40 pages apart with no phrase to
   separate them). `"nearest-preceding"` would silently point half of chapter
   13's `adjunto` at chapter 12's definition. The university convention
   (books 3, 4, 5) exists for exactly this case, and it is the right one.
4. **Wrong-sense link hunt.** Every high-frequency term's link displays were
   read in context. Real wrong-sense links found and killed:
   - *fechada* → `def:b2:multint:exact`: the Portuguese ch. 20 definition
     emphasises the bare adjective, which then followed every *curva fechada*,
     *conjunto fechado* and *intervalo fechado* in the book (16 sites). Hard-
     `DROP`ped, exactly as English hard-drops *closed*; the phrase *forma
     fechada* still carries the target.
   - *converge* → `def:b2:integration:improper`: 55 sites in chapters 10, 11,
     14, 20, 21 and 23, all about **series**, not improper integrals. The word
     is harvested from the chapter-9 definition and stoplisted, so it is
     correctly chapter-local on its own; the damage came from *also* declaring
     it in `EXTRA`, and `STOP` is honoured for **harvested** terms only, so the
     `EXTRA` copy linked everywhere. Removing the `EXTRA` entry deleted the 55
     cross-chapter links and left the 20 correct ones inside chapter 9 —
     `def:b2:integration:improper` now stands at **24 links, exactly English's
     24**.
   - *conjunto unitário* (a singleton), *média unitária*, *bissetriz unitária*,
     *vetor/disco/círculo/esfera unitária* → the unitary endomorphism of
     ch. 13 (17 sites).
   - *álgebra linear* → `$K$-álgebra`; *evento simétrico* → symmetric
     endomorphism; *teoria/análise/demonstração completa* and *por completo* →
     complete metric space; *equações/cálculo/geometria diferencial* → the
     differential of a map; *singularidade pontual* / *massa pontual* →
     pointwise; *lei fraca/forte dos grandes números* → the law of a random
     variable; *caminhos de comprimento n* → arc length; *ordem de
     soma/grandeza/leitura*, *de ordem 2*, *primeira ordem* → the order of a
     group element; *escolhidos uniformemente* → uniform convergence.
5. **A protector bug worth recording.** Two of the first-draft `EXTRA_PROTECT`
   patterns ended in a literal `\$` (`ordem\s+\$`, `de\s+ordem\s+(?:\$|…)`).
   The shared `tools/termlink/protect.py` compiles the whole list as one
   alternation, so a pattern that *consumes* an opening `$` leaves the
   inline-math rule pairing the closing `$` with the next formula's opening
   one — every span after it is masked inside out for the rest of the file. It
   reports no error; the link count just collapses (chapter 1 fell from its
   proper 138 links to 32). Both were rewritten as lookaheads, and a third
   (`formas fechadas\s*\\\[`) was rewritten the same way so as not to eat a
   `\[`. The file's own docstring warns about this; it is worth repeating that
   the failure is completely silent.
6. **Two overfull boxes fixed by tightening prose** (there is no
   `\emergencystretch` in the `_pt` entry file, and that file is off-limits):
   `pt/13-hermitian-forms.tex` (0.58 pt — "uma vantagem de $\C$" → "vantagem de
   $\C$") and `pt/18-curves.tex` (92.4 pt — the local-shape `tabular`'s third
   column, whose Portuguese descriptions ran longer than the English; two cells
   shortened, keeping the mathematical content). No structural change: the
   `tabular` column spec is still `{c c l}`, byte-identical to English.
7. **Four English `\index{}` keys localized.** `Euler's theorem`, `Stirling's
   formula`, `Jensen's inequality` and `spectral theorem` sat *inside display
   math*, where the pipeline correctly refuses to touch anything; one of them
   (`\text{Euler's theorem\index{Euler's theorem}}`) was visible English in a
   display. All four were found by an EN ∩ PT index-key intersection sweep and
   translated, taking the intersection from 5 keys to 1.
8. **294 non-breaking spaces** inserted between a Portuguese article and its
   `\cref` (`do~\cref{thm:…}`), matching the FR/ES convention, after auditing
   every site for gender: masculine `o/do/no/ao/pelo` for *Teorema, Lema,
   Corolário, Método, Exemplo, Exercício, Problema, Capítulo*; feminine
   `a/da/na/à/pela` for *Proposição, Definição, Observação, Notação, Figura,
   Tabela, Seção*. Nine genuine disagreements were fixed by hand first
   (e.g. «como **a** \cref{exo:…} prevê» → «como **o** …»; «mais uma face
   **da** \cref{ch:…}» → «**do** …»; «o padrão **do** \cref{prop:…}» →
   «**da** …»).

## Samples (native / near-native / MT)

| Sample | Verdict |
|--------|---------|
| `pt/08-real-functions.tex`, chapter opening | **native** — «compensa conhecer a paisagem de uma variável com mais detalhe do que o primeiro ano exigia: quão descontínua pode ser uma função monótona, quão regular deve ser uma função convexa, e de que propriedades especiais gozam as derivadas… Esses resultados estruturais são curtos, afiados e muito queridos pelos examinadores.» `quão + adjetivo` and `gozar de` are native academic Portuguese, not calques of "how discontinuous" / "enjoy"; the inversion «de que propriedades … gozam as derivadas» is a register no MT produces |
| `pt/16-differential-equations.tex`, statement of Cauchy–Lipschitz | **native** — «\emph{lipschitziana na segunda variável}, uniformemente na primeira»; «Então, para todo $(t_0, y_0) \in I \times \R^n$, o problema de Cauchy … tem exatamente uma solução $y \colon I \to \R^n$ de classe $C^1$.» Correct Brazilian phrasing of a hypothesis chain, with the adjective agreeing across the ellipsis |
| `pt/19-surfaces.tex`, proof of the gradient/normal proposition | **native** — «todos os vetores velocidade são ortogonais ao gradiente, de modo que a direção tangente está contida no plano $\nabla f(M_0)^\perp$»; and from the same chapter, «uma carta, duas curvas desenhadas, e o plano tangente inteiro é gerado» |
| `solutions/pt/21-countable-probability.tex`, `pb:b2:proba:1` q. 24 | **native** — «Um bêbado encontra o caminho de casa; um pássaro bêbado talvez não.» The idiomatic rendering of Kakutani's line, not a literal "homem bêbado" |
| `solutions/pt/23-generating-functions.tex`, `pb:b2:genfun:1` q. 16 | **native** — «Criticalidade significa deriva nula: o processo está sempre à beira tanto da extinção quanto da explosão, e as flutuações na escala $\sqrt{}$ da aleatoriedade sem deriva produzem precisamente esses expoentes.» «à beira tanto … quanto …» is native correlative syntax |
| `pt/21-countable-probability.tex`, the Chevalier de Méré example | **native** — «probabilidades pequenas são um domínio em que a intuição precisa da exponencial, não da régua» |

No sample scored **MT**; no sample scored merely **near-native**.

## Why not 100 — ordered gap list

1. **Register judgement is sampling-based, not exhaustive.** Terminology and
   register were graded from openings, definitions, proofs, remarks, exercise
   stems and solutions across all 23 chapters, but not by reading all 409 pages
   end to end. A Brazilian lecturer reading the whole book would very likely
   find a handful of sentences to tighten. This is the single largest reason
   the score is 96 and not higher.
2. **The build has no Portuguese hyphenation.** `brazilian/portuguese.ldf` is
   not installed here, so every line-breaking measurement in the gate table —
   0 overfull, 108 underfull, 409 pages — is provisional, and two of those
   numbers are quality claims. This cannot be resolved from inside the
   repository (see "Shared-file changes wanted" below).
3. ~~`lang_pt.py` should set `TAIL_ON_EVERY_WORD = True`.~~ **Resolved
   2026-08-01** — the orchestrator flipped the flag and this book's `DERIVED`
   table was trimmed from 175 declared forms to 91. It is listed here only to
   keep the numbering of the items below stable.
4. **Link volume is 3 677 vs English's 3 511 (+4.7 %).** The target set is
   identical in both directions and every divergence over ±5 was read in
   context and is correct-sense. The largest, with their causes: *autovalores /
   autovetores / espectros* (+34: English writes the irregular *spectra*, which
   its own morphology misses, and uses the compound *eigen-* where Portuguese
   repeats the noun); *completude/completa* (+21, all metric completeness);
   *funções geradoras* (+14); *enumerável* (+13); *álgebra/álgebras* (+9: all
   eleven surviving links are genuine `$K$`-algebras — *álgebras de Lie*,
   *álgebras normadas*, *a álgebra das circulantes*, *a álgebra de séries*,
   *a álgebra comutativa $\{aI+bA\}$* — where English's stoplist confines the
   word to chapter 1). No target is under-linked by more than 4. Correct-sense
   but not byte-parallel; not an error, and not a perfect mirror either.
5. **Two prose micro-tightenings diverge from the English wording**, both to
   remove overfull boxes without an `\emergencystretch`:
   `pt/13-hermitian-forms.tex` (four characters) and the two shortened cells of
   the parity table in `pt/18-curves.tex`. Mathematical content unchanged; the
   page shape is not byte-parallel to English at those two spots.
6. **English `%` comment lines remain in the PT bodies** (TikZ construction
   notes). **Deliberate**: byte-identical to the English source, as in the
   `fr`, `nl` and `es` editions, so the drawing code stays diffable across all
   editions. Invisible in the PDF.
7. **108 underfull boxes.** Cosmetic loose lines; the series norm (EN 104,
   ES 112), aggravated by item 2.

## Shared-file changes wanted but NOT made

Both are deliberately left for the user; neither is a blocker.

1. ~~**`tools/term_config/lang_pt.py`: `TAIL_ON_EVERY_WORD` should be
   `True`.**~~ **APPLIED by the orchestrator, 2026-08-01.** Resolved; see the
   addendum below for what it changed here.
2. **Install `texlive-lang-portuguese` on the build host.** (Still open.) Without it,
   `onemath.sty` warns and falls back to English hyphenation for the whole
   Portuguese book. This is a machine-configuration change, not a repository
   one, but it is the prerequisite for the overfull/underfull numbers above to
   become final rather than provisional.

## What is at ship level

Everything. Structure, terminology, register, LaTeX hygiene, cross-references,
rule compliance, the term-link layer, figures, solutions and MT-artifact
freedom are all ≥ 96; the `\omterm` target set matches English exactly in both
directions; the article-before-`\cref` layer is complete, non-breaking and
gender-correct; the index no longer shares orphan English keys with the
English edition; and the build is clean on all three gated counts.
**No blockers remain — this edition ships.**

Working tree left uncommitted for human review; no git commit was created.

---

## Addendum — 2026-08-01, regeneration against the `lang_pt.py` flip

The orchestrator set `TAIL_ON_EVERY_WORD = True` in the shared
`tools/term_config/lang_pt.py` (the item this report had flagged). Book 4 was
regenerated against it. **`lang_pt.py` was not edited here.**

### 1. `DERIVED` trimmed: 135 → 65 entries, 175 → 91 declared forms

Every declared form was tested mechanically against the pattern the *base
term alone* now generates (`termlink.morphology.pattern` with the new
`lang_pt`), and kept only if the pattern cannot reach it.

**Removed — 84 forms, all regular plurals the per-word tail now generates:**
every `-o/-a → -os/-as` adjective plural (*compactos, conexos, hermitianos,
convexas, …*), every regular noun plural (*ciclos, curvaturas, autovalores,
espectros, determinantes, leis, comprimentos, …*) and, the bulk of it, 46
regular phrase plurals — *espaços métricos compactos*, *formas quadráticas*,
*matrizes jacobianas*, *planos tangentes*, *círculos osculadores*,
*polinômios característicos*, *endomorfismos hermitianos*, *quocientes de
Rayleigh*, *passeios aleatórios simples*, *desvios padrão* (head-only plural,
reached because the tail is optional per word), … Five `EXTRA` keys went the
same way: *formas bilineares simétricas*, *álgebras*, *unitários*,
*unitárias*, *autoadjuntos*.

**Kept — 91 forms, in four classes the tail provably cannot reach:**

| Class | n | Examples |
|---|---:|---|
| **Gender** (the documented `WORD_TAIL` limitation) | 51 | contínua→contínuo/contínuos, hermitiano→hermitiana(s), simétrico→simétrica(s), convexa→convexo(s), gerado→gerada(s), transposta→transposto |
| **Irregular `-l → -is`** | 22 | ideal→ideais, dual→duais, potencial→potenciais, enumerável→enumeráveis, somável→somáveis, diagonalizável→diagonalizáveis, polinômio minimal→polinômios minimais, espaço amostral→espaços amostrais, convergência normal→convergências normais |
| **Nominalisation / adverb** in -idade, -ude, -ência | 11 | compacidade, completude, conexidade, continuidade, independência, somabilidade |
| **Irregular `-ão → -ões`, `-m → -ns`, and singulars-from-plurals** | 7 | torção→torções, transposição→transposições, afim→afins, anel quociente→**anéis** quociente, integrais de Wallis→integral de Wallis |

**Verification, not assumption** (the `ordem de grandeza` trap). A sweep
generated, for every one of the 255 linkable terms, the mechanically-correct
irregular plural of each word (`-ão→-ões`, `-vel→-veis`, `-al→-ais`,
`-el→-eis`, `-il→-is`, `-m→-ns`, `-r/-z/-s→-es`, else `-s`), searched the
unwrapped `pt` tree for it, and asked whether **any** linkable pattern matches
it. Result: **0 plurals present in the text are unreachable.** A first run of
the same sweep against each term's *own* pattern returned 24 hits — every one
of them a form still declared in `DERIVED` (afins, enumeráveis, funções
geradoras, ideais, duais, anéis quociente, …), which is the trim confirming
itself rather than a gap.

### 2. Link count: 3 684 → 3 677, and what moved

The flip on its own produced **one** new link and it was wrong, so the honest
summary is that the flip changed nothing for this book (every phrase plural
had already been declared by hand) and the regeneration was an opportunity to
find seven links that had been wrong all along.

| Step | Links | Note |
|---|---:|---|
| Before the flip | 3 684 | |
| After the flip + `DERIVED` trim | 3 685 | **+1, and suspect** |
| After protecting the mangled construction | 3 684 | flip is a no-op for this book |
| After the wrong-sense audit below | **3 677** | −7 genuine errors |

**The one new link, audited and rejected.** `def:b2:reduction:charpoly`
attached to the display *"polinômios característico"* in `pt/03-reduction.tex`.
"os polinômios característico e minimal" is correct Portuguese — a plural head
with two coordinated singular adjectives — but the per-word *optional* tail
matches head + first adjective and stops, leaving "e minimal" outside the link,
and English links neither word at that spot. Protected as a fixed phrase.

*Writing that protect pattern reproduced the class of bug reported earlier, in
a new form:* the first version was `polin[óo]mios…` and silently matched
nothing, because the word is **polinômios** with **ô**, not ó. It was caught
only by re-running and seeing the count fail to move. **Rule for `pt` protect
patterns: when a character class stands in for an accented vowel, list every
accent the word can carry (`[ôóo]`, `[íi]`, `[êé e]`), and always confirm the
link count actually moved.** As instructed, every pattern was authored and
tested against **unwrapped** source (`\omterm` stripped), and the whole
`EXTRA_PROTECT` list was re-audited for the two rules from the coordinator's
sweep: **0 patterns consume a `$`**, **0 patterns contain a literal space**.

**Seven wrong-sense links found and killed** — these were live when this
edition was first scored, and were missed because the earlier audit sampled
link contexts rather than reading all of them:

| Link | Sites | Why wrong |
|---|---:|---|
| *cilindro unitário* → unitary endomorphism | 1 | the **unit** cylinder of `pt/19-surfaces.tex` |
| *$N$ unitário ortogonal a $T$* → unitary endomorphism | 1 | the **unit** normal of the Frenet frame |
| *álgebra* → `$K$`-algebra, in the "algebra the discipline / the computation" sense | 5 | «a geometria era audível na **álgebra**:», «Uma direção é **álgebra**:», «invalida a **álgebra** seguinte», «é **álgebra** polinomial pura», «a identidade é **álgebra** direta» |

`cilindro` was added to the unit-noun list, plus `unitári[oa]s?\s+ortogonal`,
`[áa]lgebra\s*:` and `[áa]lgebra\s+(?:seguinte|polinomial|direta)`.

### 3. Wrong-sense classes re-verified after regeneration

| Class | Expected | Measured |
|---|---|---|
| bare *fechada / fechado* → `def:b2:multint:exact` | 0 | **0** (only *forma fechada* ×3, *formas fechadas* ×5, *forma exata* ×1, *exata(s)* ×10) |
| *converge* → `def:b2:integration:improper` outside chapter 9 | 0 | **0** — all 20 are in `pt/09-integration.tex` (13) and its solutions (7); target total **24, exactly English's 24** |
| *unitário/unitária* in the "unit" sense | 0 | **0** — 23 remaining link sites, all unitary endomorphisms, matrices or groups |
| *álgebra linear* / discipline sense | 0 | **0** — 11 remaining links, every one a genuine `$K$`-algebra |
| *adjunto* (ambiguous ch. 12 / ch. 13) | 0 under `AMBIG_POLICY = "drop"` | **0** |
| *compacto* (ambiguous) | one target only | **156 links, all → `def:b2:metric:compact`** |

### 4. Gates re-run after regeneration

| Gate | Result |
|---|---|
| `check_translation.sh bachelor-2 pt` | **PASSED** |
| `latexmk one_math_book_4_university_year_2_pt.tex` | exit 0 |
| errors / undefined / overfull | **0 / 0 / 0** (underfull 108, unchanged) |
| PDF | **409 pp**, unchanged |
| `--check` | green, and idempotent across a second `--unwrap --apply` + `--apply` cycle |
| `\omterm` target parity vs English | **85 targets, identical sets both directions** |

### 5. Score

**96 / 100 stands.** The link dimension is re-affirmed at **96**, not raised:
the layer is now demonstrably cleaner (seven wrong-sense links gone, one
mis-shaped link prevented, `def:b2:integration:improper` shown to be at exact
parity rather than under-linked as this report previously stated — that claim
was an unverified assumption and is corrected above), but those seven errors
were present when the 96 was first awarded, so the number is now accurate
rather than generous. No other dimension moved: no prose changed in this
round, only `tools/term_config/book4_pt.py` and the generated `\omterm` layer.

No commits; the working tree is left for review.
