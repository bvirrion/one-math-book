# Translation score — Math Book 3 · Brazilian Portuguese (`pt`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 3 (University Year 1, `bachelor-1`) |
| **Language** | Brazilian Portuguese (`pt`) |
| **Quality bar** | **native academic** (English is the source of truth; the FR and ES editions were consulted only as sense references, never as sources) |
| **Overall score** | **96 / 100** |
| **Ship threshold** | ≥ 95 — **MET** |
| **Date** | 2026-08-01 (re-translation pass 2026-07-31; `TAIL_ON_EVERY_WORD` regeneration round 2026-08-01) |
| **Scope of this pass** | **Full re-translation from English** of all 50 files (25 chapters + 25 solution files), a rebuilt `tools/term_config/book3_pt.py`, regenerated `\omterm` links, and a hygiene / register / MT-artifact audit. The previous `pt/` bodies were discarded, not used as a draft. **Second round (2026-08-01):** the orchestrator applied the `lang_pt.py` fix this file had requested, and the config was trimmed and the links regenerated against it. |

## Verdict in one line

Structurally byte-exact against English, written in native Brazilian
first-year university register, with the defined-term link map now within
1.2 % of the English density and every gate green.

## Why the old edition was replaced rather than repaired

The `pt/` tree that existed was machine output with damage in every register
band, not a draft with defects: `Deixar` 317× for *Let* (→ `Seja`/`Sejam`),
`Desde` for *Since* (→ `Como`/`Uma vez que`), `contabilidade` for
*countability* (→ `enumerabilidade`), `conversa` for *converse* (→
`recíproca`), `aula` for *equivalence class* (→ `classe`), `mapa` for *map*
(→ `aplicação`), `campo` for the algebraic *field* (→ `corpo`), English left
inside display math (`\text{where }`, `\text{ if }`, `\text{ for all }`),
English word order across line breaks (*"no Ano 1 volume"*, *"equivalência e
ordem relações"*, *"ferramentas de trabalho do comércio"*), and spaces
injected inside inline math (`$ K $`). Every one of those classes is gone,
because none of the text survived.

## Dimension scores

| Dimension | Score /100 | Notes |
|-----------|----------:|--------|
| Structural fidelity | **99** | Exact mirror: 25 chapters, 25 solution files, **300** `exo:` labels EN / 300 PT, **25** `pb:` / 25, **325** `\begin{solution}{…}` on both sides; the `\label{}` **and** `\cref`/`\Cref` multisets are byte-identical to English (`diff` empty). `check_translation.sh bachelor-1 pt` **PASSED** |
| Terminology | **96** | Consistent Brazilian university register: *aplicação* (never *mapa*), *corpo* (never *campo*), *aplicação linear*, *núcleo e imagem*, *família livre* / *linearmente dependente*, *espaço gerado*, *subespaços suplementares*, *teorema da base incompleta*, *teorema do núcleo e da imagem*, *fórmula de Grassmann*, *posto*, *forma escalonada*, *pivô*, *matriz ampliada*, *expansão assintótica*, *somas de Riemann*, *frações parciais*, *cúspide*, *ponto de sela*, *mínimos quadrados*, *equações normais*, *reflexão deslizante*, *grupo diedral*. No sense swaps found in sampling |
| Register / tone | **96** | Reads as a Brazilian first-year lecture course: `Seja`/`Sejam`, `Demonstre`, `Deduza`, `Mostre`, `Calcule`; `se e somente se`; `isto é`; `logo`/`donde`/`ao passo que`; `a ideia de fechamento` for the book's recurring *closing insight*. Brazilian orthography throughout (`fato`, `objeto`, `direta`, `ótima`, `leem-se`), zero European forms (`ficheiro`, `ecrã`, `facto`, `óptimo`, `directa`, `objecto`: 0 hits) |
| LaTeX hygiene | **99** | 0 fatal errors, 0 undefined references, **0 Overfull `\hbox`**; **0** TeX accent escapes (UTF-8 throughout: `Cesàro`, `Pólya`, `limaçon`, `Nicômaco` written as characters); no `\end{proof>` typo class, no drafty `...` |
| Cross-refs / rule compliance | **98** | `\label`, `\cref`/`\Cref` targets and `\begin{solution}{key}` byte-identical to English. Articles supplied by hand in front of every `\cref` per the label-prefix gender map (masc. `o/do/no/ao/pelo` for thm, lem, cor, met, ex, exo, pb, ch, alg; fem. `a/da/na/à/pela` for prop, def, rem, not, fig, tab, sec). No country or curriculum name in visible text (0 hits for *francês*, *Brasil*, *PCSI*, *lycée*, *ENEM*, *vestibular*); cross-volume references are prose-only — *volume do ensino médio* ×7, *volume do segundo ano de graduação* ×19, *volume do terceiro ano de graduação* ×10 |
| Defined-term links | **96** | `--check` **green** and idempotent (a second `--apply` inserts 0). **3 897** links across 50 files against English's **3 944** (98.8 %); the per-file distribution tracks English chapter by chapter (largest single-file gap 12, no collapsed file). Target set: every English target is used in Portuguese; three targets are used in Portuguese that English happens not to use (`def:b1:structures:law`, `thm:b1:matrices:conjugation`, `thm:b1:poly:vieta` — 3+1+2 links, all verified correct-sense). After the 2026-08-01 flip the total is unchanged and the config is no longer brittle |
| Figures | **97** | All 33 `tikzpicture` environments present and their drawing code byte-identical (coordinates, `\draw`, `\addplot`, styles untouched); only node text, axis labels, legends and captions localized. The anagram exercise keeps `\textsc{orange}`/`\textsc{banana}` untranslated, as FR and NL do, because the count depends on the letters |
| Solutions | **96** | All 325 solutions present, complete and native; headers `\section*{Capítulo \ref{ch:…} --- <título>}` with the `ch:…` slug unchanged and the title matching the chapter's own `\chapter{}` |
| MT-artifact freedom | **95** | An English-function-word sweep over all 50 files now returns **only** TikZ syntax (`.. controls (…) and (…)`, `circle (r and r)`). 11 genuine English fragments surviving inside masked inline math were found and fixed in this pass (see below); none remains, but the sweep is heuristic, so a residual fragment in an unscanned form cannot be excluded with certainty |

**Overall: 96** (weights: register 0.18, terminology 0.18, MT-freedom 0.16,
defined-term links 0.12, cross-refs/rule compliance 0.10, LaTeX hygiene 0.08,
solutions 0.08, figures 0.05, structure 0.05 → 96.5 before the flip, 96.5
after: links moved 95 → 96 on brittleness and target correctness, but the link
*count* did not move, so **96 / 100 stands unchanged**).

Register, terminology and MT-artifact freedom carry more than half the weight
on purpose: a translation can be structurally perfect and still be unusable
prose, and that is exactly what the previous edition was.

## Structural / build gates

| Gate | Result |
|------|--------|
| `bash tools/check_translation.sh bachelor-1 pt` | **PASSED** |
| `python3 tools/link_defined_terms.py --book 3 --lang pt --unwrap --apply` then `--apply` | 3 897 removed → **3 897 links across 50 files** (EN: 3 944 — 98.8 %) after the `TAIL_ON_EVERY_WORD` flip; 4 258 → 3 897 in the first round |
| `python3 tools/link_defined_terms.py --book 3 --lang pt --check` | **green** — "every file matches what the config generates"; a repeat `--apply` inserts **0 links**, so the pass is idempotent |
| `latexmk one_math_book_3_university_year_1_pt.tex` | exit 0 |
| Fatal errors — `grep -ac '^!'` | **0** |
| Undefined references — `grep -aci 'undefined'` | **0** |
| Overfull `\hbox` — `grep -ac 'Overfull'` | **0** |
| Underfull `\hbox` | 119 (ragged-right noise; ES 122, EN/FR in the same band) |
| PDF | `build/one_math_book_3_university_year_1_pt.pdf`, **410 pp** (EN 395, FR 416, NL 411, ES 413) — +3.8 %, normal Portuguese expansion, no MT padding |
| Exercise / problem / solution census vs EN | 300/300, 25/25, 325/325 |
| `\label` / `\cref` / solution-key multisets vs EN | identical (`diff` empty) |
| `tikzpicture` census vs EN | 33/33 |
| TeX accent escapes (`\'e`, `` \`a ``, `\c{c}`, …) | **0** |
| `\index{}` keys translated | 229 keys, EN∩PT intersection = **3** (`\index{integral}`, `\index{interior}`, `\index{Z/nZ@$\Z/n\Z$}` — genuinely identical in both languages) |

**Build-environment caveat.** No Portuguese `.ldf` is installed here, so
`onemath.sty` emits *"brazilian/portuguese.ldf not found; building Portuguese
without babel"* and the book is typeset with **English hyphenation patterns**.
The zero-Overfull result and the 410-page total are therefore *provisional*:
on a machine with `texlive-lang-portuguese`, Portuguese hyphenation will break
words English cannot, so line breaks, the underfull count and the page total
will all shift slightly (almost certainly in the good direction). The entry
file's `\setlength{\emergencystretch}{5em}` was left untouched, as instructed.
The 10 `Missing character … nullfont` warnings are identical in the EN, FR,
NL, ES and PT logs — a shared-source artefact, not a Portuguese defect.

## Term configuration rebuilt (`tools/term_config/book3_pt.py`)

The stub that existed (23 lines: 7 stoplist words, `EXTRA = {}`, `DROP =
set(STOP)`, `NO_CAPITAL = set()`, no `DERIVED`, no `EXTRA_PROTECT`) both
under- and over-linked. It was replaced by a curated config written against
the English term list word by word, and every entry carries its reason in a
comment. Final shape after the 2026-08-01 trim: **`NOT_A_TERM`** 12 heads,
**`STOP`** 4, **`DROP`** 16, **`EXTRA`** 19 (was 45), **`DERIVED`** 14,
**`EXTRA_PROTECT`** 13, `MAX_TERM_WORDS = 8`, `MAX_TERM_CHARS = 60`.

* **`NOT_A_TERM`** — result heads (*teorema*, *lema*, *desigualdade*,
  *fórmula*, *critério*, *regra*, *princípio*, *identidade*, *paradoxo*,
  *problema*, *estimativa*, *conjectura*). Because `critério` is on that list,
  *critério da razão* (English *ratio test*, a notion the book uses as a noun)
  had to be restored through `EXTRA`.
* **`STOP`** (soft: still linked inside the defining chapter) — *conjugado*
  (complex conjugate in ch. 3, conjugate expression in ch. 11, algebraic
  conjugates in ch. 19, conjugation of an isometry in ch. 23),
  *polinômio característico* (ch. 5 for an ODE, ch. 21 for a matrix — a
  different object), *finito/finita* (the finite set of ch. 2 versus "um
  número finito de pontos" everywhere else). English STOPs exactly *finite*,
  *conjugate* and *characteristic polynomial*.
* **`DROP`** — the bare adjectives Portuguese harvests out of a compound and
  English never links: *algébrico*, *transcendente*, *crítico*, *direta*,
  *equivalentes*, *semelhantes*; plus *argumento* (72 uses, nearly all "o
  mesmo argumento", "um argumento de dimensão" — English DROPs *argument* for
  the same reason), *simetria* (ch. 20's linear involution against "eixos de
  simetria" and "por simetria" — English DROPs *symmetry*), *batimentos*
  (English DROPs the corresponding *beats*), and the seven result names that
  reach the harvest through `\emph{}\index{}` and bypass `NOT_A_TERM`
  (*teorema de Kummer*, *fórmula de Legendre*, *leis de De Morgan*,
  *desigualdade de Ptolomeu*, *estimativa das séries alternadas*, *equação
  funcional*, *equação funcional de Cauchy*) — the same seven English drops.
* **`EXTRA`** — 9 real gaps plus **10** irregular plural compounds (was 36
  before the flip; see the trim section below):
  *contínuo/contínua/continuamente* and *derivável/derivabilidade* (the
  definitions emphasise `\emph{contínua em $x_0 \in I$}` /
  `\emph{derivável em $x_0 \in I$}`, pure inline math that can never match
  running prose), *critério da razão* → `thm:b1:series:ratio`,
  *constante de Euler* → `pb:b1:series:1` (the nearest preceding statement is
  an unrelated telescoping example; English resolves it to the problem, so the
  Portuguese must too or the same words point at two places), and the two
  over-long ODE names *equação diferencial linear de primeira ordem* /
  *equação linear de segunda ordem com coeficientes constantes*.
* **`DERIVED`** — the forms `WORD_TAIL = (?:e?s)?` cannot spell: the feminine
  (*aberta*, *fechada*, *densa*, *mônica*, *conjugada*), the masculine of an
  `-a` head (*injetivo*, *sobrejetivo*, *bijetivo*, *convexo*), the
  `-al → -ais` plural (*ortogonais*, *ortonormais*), the adverb
  (*ortogonalmente*), the singular of a plural head (*suplementar*) and the
  verb (*dividem*). The nouns *injeção* / *bijeção* / *injetividade* were
  deliberately **not** derived: English links only the adjectives, and adding
  the nouns pushed `def:b1:logic:inj` from 179 (EN) to 319 links.
* **`EXTRA_PROTECT`** — 13 spans, every `$` matched by a **lookahead only**,
  never consumed (the failure mode documented in `tools/termlink/protect.py`,
  which has already cost this book a thousand links once). The Portuguese-only
  trap is *módulo*: Portuguese spells *modulus* and *modulo* the same way, so
  `r'módulo\s+(?=\$)'` separates "reduza $X^n$ módulo $D$" from "o módulo de
  $z$" without touching the opening `$`. The rest are familiar: *álgebra
  linear* / *combinação linear* (protecting the bare *linear*), *exercício de
  aplicação* (protecting *aplicação*), *corpo não enumerável*, *forma/resto
  integral*, *no interior de …*, *queda livre* (physics, not the free family
  of ch. 18), and a numeration-base guard.
* **`NO_CAPITAL = {"aplicação"}`** — *Aplicações* opens the section that
  *applies* a theorem; it is not the map of `def:b1:logic:map`.
* **`AMBIG_POLICY = "drop"`** — the university convention (books 3, 4, 5),
  and here it is not merely inherited: *posto* is `def:b1:findim:rank` in
  ch. 19 and `def:b1:linmaps:rank` in ch. 20, with no dominant first sense,
  exactly like English *rank*. Under `drop` the word still links inside each
  defining chapter, so both targets survive on both sides and the target sets
  match; under `nearest-preceding` every ch. 20–22 occurrence would have
  pointed at the ch. 19 definition.

### Link-count reconciliation against English

| | EN | PT |
|---|---:|---:|
| total `\omterm` | 3 944 | 3 897 |
| distinct targets used | 106 | 109 |

The four material per-target divergences, all deliberate:

* `def:b1:logic:statement` — EN 90, PT 20. English links *statement* in two
  senses: the logical proposition of ch. 1 and "the statement of the theorem".
  Portuguese splits them (*proposição* vs *enunciado*/*afirmação*), and linking
  *enunciado* to the ch. 1 definition would be a wrong-sense link. Kept split.
* `def:b1:euclid:isometry` — EN 19, PT 44. English's `WORD_TAIL` cannot spell
  *isometry → isometries*, so the English edition silently loses every plural;
  Portuguese links both. Here Portuguese is *more* complete than English.
* `def:b1:counting:objects` — EN 60, PT 32: English links bare *permutation*
  in combinatorial prose where Portuguese writes *permutação* less often
  (*disposições*, *arranjos*, *reordenações* in ch. 2).
* `def:b1:logic:map` — EN 169, PT 112: *aplicação linear* is a term of its own
  and wins on length, and `NO_CAPITAL` suppresses the section-opening
  *Aplicações*.

## Sampled prose — verdicts

> Perto de um ponto, uma função suave vale tanto quanto um polinômio --- com um
> erro controlável. As fórmulas de Taylor tornam isso exato em três versões
> (resto integral, resto de Lagrange, resto de Young), e as *expansões
> assintóticas* resultantes, manipuladas algebricamente, tornam-se a ferramenta
> mais afiada da análise elementar. (ch. 16 opening)

**Native.** Idiomatic word order, no calque of *as good as*, and the three
remainders carry their standard Brazilian names.

> Trinta segundos de aritmética deste tipo, depois de invocar qualquer
> identidade de determinantes, são o seguro contra erros mais barato
> disponível. (ch. 22, after the numeric check of multiplicativity)

**Native.** The English *"the cheapest error insurance available"* is rendered
as an idiom, not word for word.

> a contabilidade ordem a ordem detecta tais conspirações, o olho nunca.
> (ch. 16, on composing expansions)

**Native.** *bookkeeping → contabilidade* and *eyeballing → o olho* keep the
register's dry humour; note this is a different word from the old edition's
`contabilidade` for *countability*, which was a sense error.

> Indução decrescente sobre $d = \dim F$, de $d = n$ até $d = 0$. […] As somas
> $F' = F \oplus \operatorname{Vect}(x)$ e $G' = G \oplus \operatorname{Vect}(x)$
> são diretas […] e têm dimensão $d + 1$. (solutions, ch. 19, common
> supplementary)

**Native.** Standard Brazilian proof register (*indução decrescente*, *somas
diretas*, *pela hipótese de indução*), math untouched.

> (1) Linear: as coordenadas são expressões lineares. (2) Não linear:
> $u(2(1,1)) = 4 \neq 2 = 2u(1,1)$. (solutions, ch. 20)

**Native.** Terse solution register, matching the English's clipped style.

## English fragments repaired in this pass

The translation pipeline masks inline math byte-for-byte, which preserves
`\text{…}` inside a masked span. Eleven such fragments survived the first
assembly and were fixed by hand:

| File | Was | Now |
|------|-----|-----|
| `pt/14-differentiation.tex` | `\text{coefficients}` | `\text{coeficientes}` |
| `pt/18-vector-spaces.tex` (×2) | `\text{ bounded}` | `\text{ limitada}` |
| `pt/19-finite-dimension.tex` | `\text{ and }` | `\text{ e }` |
| `pt/24-plane-curves.tex` | `\text{slope}` | `\text{inclinação}` |
| `pt/25-two-variable-functions.tex` | `\text{tangent}` | `\text{tangente}` |
| `solutions/pt/01-logic-sets-maps.tex` | `\text{ and }` | `\text{ e }` |
| `solutions/pt/08-polynomials.tex` | `\text{integer}` | `\text{inteiro}` |
| `solutions/pt/17-numerical-series.tex` | `\text{gap}` | `\text{diferença}` |
| `solutions/pt/18-vector-spaces.tex` | `\text{lower degrees}` | `\text{graus inferiores}` |
| `solutions/pt/22-determinants-systems.tex` | `\text{column of }` | `\text{coluna de }` |
| `solutions/pt/24-plane-curves.tex` | `\text{trigonometric polynomial in }` | `\text{polinômio trigonométrico em }` |

Display-math `\text{}` and every TikZ node / legend / axis label were
extracted as translation units by construction and were localized in the
first pass.

## Shared-file change requested — **APPLIED by the orchestrator (2026-08-01)**

This file previously asked for one line in `tools/term_config/lang_pt.py`:

```python
TAIL_ON_EVERY_WORD = False   ->   True
```

The orchestrator applied it (with a docstring recording the history, the trim
rule and the gender limitation) and all five Portuguese math books were
regenerated against it in parallel. **The request is resolved; nothing remains
outstanding on any shared file.**

### Trim performed here

The 36 plural compounds this book had declared as a work-around were each
re-checked *against the rule*, not assumed regular — the test is whether
`(?:e?s)?` appended to **every** word of the harvested singular spells the
plural exactly:

* **26 removed** as now generated: *forma/sistema linear*, *curva
  parametrizada*, *curva polar*, *ponto crítico*, *ponto de sela*, *produto
  interno*, *espaço euclidiano*, *número primo/algébrico/transcendente*,
  *conjunto aberto/fechado/finito*, *família livre*, *soma direta*, *série
  geométrica*, *classe de equivalência*, *cota superior*, *parte inteira*,
  *lei de composição*, *polinômio mônico*, *sequência recorrente*, *reta de
  regressão*, *domínio de integridade*, *mudança de base*.
* **10 kept**, because the tail cannot spell them:

  | Kept | Irregularity |
  |------|--------------|
  | *aplicações lineares* | head `-ão → -ões` **and** tail `-r → -res` |
  | *frações racionais* | `-ão → -ões` **and** `-al → -ais` |
  | *relações de equivalência* | `-ão → -ões` |
  | *reflexões deslizantes* | `-ão → -ões` |
  | *integrações por partes* | `-ão → -ões` |
  | *funções escada* | `-ão → -ões` + invariable apposition |
  | *espaços vetoriais* | `-al → -ais` |
  | *números irracionais* | `-al → -ais` |
  | *coeficientes binomiais* | `-al → -ais` |
  | *conjuntos enumeráveis* | `-vel → -veis` |

The keep/remove split was not eyeballed: a script re-derived
`\s+`-joined `word(?:e?s)?` for each singular and tested `fullmatch` against
the declared plural, and the result was then confirmed against the link counts
(below), which is the check the physics book's `ordem de grandeza` miss showed
is the one that actually catches an error.

### Regeneration result

| | before flip | after flip | EN |
|---|---:|---:|---:|
| total `\omterm` | 3 897 | **3 897** | 3 944 |
| `EXTRA` entries | 45 | **19** | — |

The total is **unchanged** — as expected, since the 26 deleted declarations
were replaced one-for-one by generated forms. Six targets moved, net zero, and
each shift is a *compound* now winning on length over the bare word it used to
be split into:

| Target | Δ | Cause |
|---|---:|---|
| `pb:b1:matrices:1` | +2 | *recorrências lineares* now generated |
| `def:b1:linmaps:def` | −2 | …so it no longer links as bare *lineares* |
| `pb:b1:vspaces:1` | +2 | *polinômios a valores inteiros* now generated |
| `def:b1:poly:def` | −2 | …so it no longer links as bare *polinômios* |
| `def:b1:vspaces:span` | +1 | *espaços gerados* now generated |
| `def:b1:structures:group` | −1 | *grupos abelianos* is now one link, not *grupos* + *abelianos* |

All four new surfaces were read in context and are correct-sense; every one is
a strict improvement, because the link now points at the statement that
defines the *compound* rather than at a component word's definition.

### Decisions re-verified after the flip

* **`def:b1:logic:statement` still 20 links, and every linked surface is
  *proposição*.** Zero occurrences of *enunciado* or *afirmação* acquired a
  link. The flip could not have undone this split in any case: the tail cannot
  spell *proposição → proposições* (`-ão → -ões`), so the plural was
  unreachable before and remains unreachable now — the deliberate split is
  intact but it rests on an irregularity, not on a rule, which is worth
  knowing if `DERIVED` is ever extended.
* **`AMBIG_POLICY = "drop"` still doing its job for *posto*:** 16 links to
  `def:b1:findim:rank` (ch. 19) and 12 to `def:b1:linmaps:rank` (ch. 20), each
  confined to its defining chapter, both targets alive on both sides.
  *posto* is a single word, so the flip could not affect it — verified rather
  than assumed.

`WORD_TAIL = (?:e?s)?` still cannot reach gender variants (*aberto* →
*aberta*) or the `-al → -ais` plural; those stay in `DERIVED` here, and
`lang_pt.py`'s docstring now records the limitation. It is *one* contributor to
the residual 47-link gap against English, and not the largest — the deliberate
*proposição* / *enunciado* split (−70) dominates it, partly offset by
Portuguese linking plurals English cannot reach (*isometrias*, +25). Neither is
a defect; see the reconciliation table above.

## Why not 100 — ordered gap list

1. **The `\cref` article map is hand-applied, not enforced.** Every one of the
   ~1 400 `\cref` sites got its article by hand from the label-prefix gender
   map. The build cannot detect a wrong article (`o Proposição`), and no
   automated check exists, so a handful of misgenders across 50 files cannot
   be excluded. This is the single largest residual risk and the reason
   cross-refs scores 98 rather than 100.
2. **`def:b1:logic:statement` is under-linked by design** (20 vs 90). The
   split *proposição* / *enunciado* is right, but a Portuguese reader loses
   ~70 links English readers get. Closing it honestly would need a second
   definition target, which would break label parity.
3. **No Portuguese hyphenation in this environment.** Zero Overfull boxes were
   measured with English patterns; the real Portuguese build may surface a few.
4. **The MT-artifact sweep is heuristic.** It greps English function words and
   the known damage classes; a residual calque phrased in fully Portuguese
   words (an unidiomatic preposition, say) would pass it. Five long passages
   were re-read end to end; the other ~1.5 MB was sampled.
5. ~~36 `EXTRA` plural entries are a work-around, not a fix.~~ **Resolved
   2026-08-01.** `TAIL_ON_EVERY_WORD` is now `True`, 26 of the 36 declarations
   were deleted, and regular compound plurals are generated. The 10 that remain
   are genuinely irregular (`-ão → -ões`, `-al → -ais`, `-vel → -veis`), so a
   future chapter using a *regular* compound plural now links automatically;
   only a new *irregular* compound would still need declaring.
6. **Three targets are used in Portuguese that English does not use**
   (`def:b1:structures:law`, `thm:b1:matrices:conjugation`,
   `thm:b1:poly:vieta`, 6 links total). All three are correct-sense — the
   Portuguese prose simply repeats *lei de composição*, *matrizes semelhantes*
   and *relações de Girard* where English does not repeat its equivalents —
   but it is a superset, not exact parity.
7. **Index keys were translated, and the sort order was not audited.** 229
   keys, EN∩PT = 3. Accented Brazilian keys sort under `makeindex`'s byte
   order; no `@`-sort keys were added except where English had them
   (`irracionalidade!de cos 1@de $\cos 1$`). The printed index has not been
   proof-read letter by letter.

## Status

**Meets the ship threshold (≥ 95): 96 / 100** — unchanged after the
2026-08-01 regeneration round (the link count did not move; the link dimension
rose 95 → 96 on brittleness and target correctness, which does not carry the
total past 96). No git commit was created; the working tree is left for human
review.
