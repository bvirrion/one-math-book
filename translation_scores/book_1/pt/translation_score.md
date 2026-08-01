# Book 1 — Brazilian Portuguese (`pt`) — translation self-score

| Field | Value |
|---|---|
| **Book** | One Math Book 1 (Primary / Middle, grades 1–9) |
| **Entry** | `one_math_book_1_primary_middle_school_pt.tex` |
| **Language** | Brazilian Portuguese (`pt`) |
| **Quality bar** | `native academic` — a Brazilian schoolbook a Brazilian teacher would hand to a class without apologising for it |
| **Scope** | 71 chapters + 71 solutions = **142 files** under `parts/grade-{1..9}/pt/` and `parts/grade-{1..9}/solutions/pt/` |
| **Term config** | `tools/term_config/book1_pt.py` (rewritten, curated) |
| **Kind of pass** | **full re-translation from the English canon** — every file rewritten from scratch; the previous machine-translated bodies were read only as a warning and then discarded |
| **Overall score** | **95 / 100** (unchanged after the 2026-08-01 regeneration) |
| **Date** | 2026-07-31, revised 2026-08-01 |

This supersedes the 2026-07-24 score (91/100), which graded a post-edited
machine translation.

> **Errata 1 (2026-07-31).** A first version of this file scored 96/100 and
> reported **3 216** `\omterm` links. That number was wrong: two of my
> `EXTRA_PROTECT` patterns consumed an opening `$`, which silently destroyed
> **235** links (§10). The corrected count was **3 450**, the account of the
> EN-vs-PT gap in §5 was rewritten, and the link-layer dimension was re-scored
> 8 → 7. Overall 96 → 95.
>
> **Errata 2 (2026-08-01).** The orchestrator applied the `lang_pt.py` change
> this file had requested (`TAIL_ON_EVERY_WORD = True`, §8). I trimmed
> `DERIVED` 27 → 8 and regenerated: **3 459** links (§11). The score does
> **not** move — 95/100 stands, and the link dimension stays at 7/10. See
> §11.6 for why.

---

## 1. Dimension scores

| Dimension | Weight | Score | Comment |
|---|---:|---:|---|
| Register (ages 6–15, Brazilian schoolbook voice) | 25 | 24 | Grades 1–5 read like a good Brazilian professor talking to children; grades 8–9 tighten toward high-school prose. No baby-talk, no lecture calque. |
| Terminology (Brazilian mathematical usage) | 20 | 19 | `par`/`ímpar`, `máximo divisor comum`, `coeficiente angular`/`coeficiente linear`, `função afim`, `geratriz`, `planificação`, `tronco de cone`, `seção transversal`, `média harmônica` (BR spelling, not `harmónica`). |
| Freedom from MT artefacts | 20 | 20 | Zero `Deixar` for *Let* (12 before, 0 now: `Seja`/`Sejam`). Zero `incluso`/`estranho` for *even*/*odd*. No word-salad, no doubled articles, no English TikZ nodes, no English LaTeX comments. |
| Structural fidelity | 15 | 15 | All nine `check_translation.sh` gates green. |
| Mathematical correctness | 10 | 10 | Every numeric answer re-derived while writing; no value diverges from the English. |
| Link layer (`\omterm`) | 10 | 7 | 3 459 links / 80 targets against English's 3 899 / 79. Target parity is perfect (§5). Marked down not for the residual count gap — 69 % of which is gender morphology no config can reach — but because the config shipped with a `$`-consuming protector that silently destroyed 235 links, a failure mode the tool's own header documents (§10). |

**Weighted total: 95 / 100.**

---

## 2. Gate results

| Gate | Result |
|---|---|
| `bash tools/check_translation.sh grade-1..9 pt` | **PASSED** ×9 (completeness, identical label sets and order, `exo:`/`pb:` ↔ `\begin{solution}{}` parity, env/figure census, `\end{...>` typo class, drafty `...`, duplicate labels, TeX accent escapes) |
| `python3 tools/link_defined_terms.py --book 1 --lang pt --check` | **green** — "every file matches what the config generates" |
| `latexmk one_math_book_1_primary_middle_school_pt.tex` | exit 0 |
| `grep -ac '^!'` on the log | **0** errors |
| `grep -aci 'undefined'` | **0** undefined references |
| `grep -ac 'Overfull'` | **0** overfull boxes |
| Output | `build/one_math_book_1_primary_middle_school_pt.pdf`, **428 pages** |

**Build-environment caveat.** No Portuguese `.ldf` is installed here, so the
book builds *without babel*:

```
Package onemath Warning: brazilian/portuguese.ldf not found; building
Portuguese without babel. Install texlive-lang-portuguese for hyphenation.
```

UI strings still come from `styles/lang/pt.tex`, but hyphenation is English.
**The overfull-box count and the page total above are therefore provisional**:
with Portuguese hyphenation patterns the line breaks will differ, and a pass
with `texlive-lang-portuguese` installed should re-check both. The two
overfull boxes the English-hyphenation build did produce were fixed in the
sources (rewrapped prose, not `\hbox` trickery), so the text is already robust
to the change.

---

## 3. The named damage, and what replaced it

`parts/grade-6/pt/01-whole-numbers.tex` was the worst file in the tree: a
word-salad opening, `($0$ para $9$)` for "0 to 9", a doubled article, an
`\index{}` key that was a whole sentence instead of `valor posicional`, and
English TikZ nodes (`thousands`, `hundreds`, `tens`, `units`). It now reads:

```latex
\begin{definition}[Valor posicional]\label{def:g6:wholes:place}
O nosso jeito de escrever números usa dez algarismos ($0$ a $9$), e o
\emph{valor de um algarismo depende da posição dele}\index{valor posicional}:
em $5\,208$, o algarismo $5$ conta milhares, o $2$ conta centenas, o $0$
conta dezenas (não há nenhuma) e o $8$ conta unidades:
```

with `{milhares}`, `{centenas}`, `{dezenas}`, `{unidades}` in the figure.

That class of defect was swept for across all nine years:

- **`\index{}` keys** — all 102 distinct keys are now short visible terms
  (`valor posicional`, `média harmônica`, `função afim`, `seção transversal`,
  `ângulos opostos pelo vértice`, …). None is a sentence.
- **English in figures** — every TikZ/pgfplots text node, axis label, legend
  and caption in the 142 files is Portuguese; drawing code (coordinates,
  `\foreach`, `\addplot` expressions, `xtick`, `samples at`) is byte-identical
  to English.
- **English LaTeX comments** — the ten that survived the first pass
  (`% ten-frame: 2 rows of 5 cells`, `% four loose sticks`, …) were localised.
  They are invisible in print, but they are the fingerprint of a copy-paste
  translation, and one of them had already tripped the drafty-`...` gate.
- **`Deixar` for *Let*** — 12 occurrences in grade 9 of the old tree, **0**
  now: `Seja $n$ um número inteiro positivo`, `Sejam $a$ e $b$ números
  inteiros positivos`, `Seja $x = 0.7777\ldots$`.
- **Gender/number agreement** — gone by construction (full rewrite). The one
  class a rewrite does not automatically fix is the article before a `\cref`
  used as a noun; that was swept separately (§4).

---

## 4. The article-before-`\cref` sweep

`\cref` prints a noun, so Portuguese needs its article, and the gender is
fixed by `styles/lang/pt.tex` + the `\crefname` declarations in
`styles/onemath.sty`:

| masculine (`o / do / no / ao / pelo`) | feminine (`a / da / na / à / pela`) |
|---|---|
| `ch:` Capítulo · `thm:` Teorema · `ex:` Exemplo · `met:` Método · `exo:` Exercício · `pb:` Problema · `lem:` Lema · `cor:` Corolário | `prop:` Proposição · `def:` Definição · `rem:` Observação · `not:` Notação |

An audit of every `(word) \cref{prefix:` pair in the nine years found **11
wrong-gender articles**, all of them feminine in front of `thm:` (Teorema):

- `a igualdade da \cref{thm:g8:pythagoras:direct}` → `do`
- `veja a \cref{thm:g8:equations:expand}` → `veja o`
- `Pela \cref{thm:g8:negprod:rules}` → `Pelo`
- `pela \cref{thm:g8:midpoints:direct}` → `pelo`
- `critério 3 da \cref{thm:g7:central:recognize}` → `do`
- `Que critério da \cref{thm:g7:central:recognize}` → `do`
- `o que a \cref{thm:g8:midpoints:direct} diz` → `o que o`
- `A demonstração da \cref{thm:g8:negprod:rules}` → `do`
- `as regras da \cref{thm:g8:negprod:rules}` → `do`
- `aplique a \cref{thm:g8:fractions:div}` → `aplique o`
- `A primeira regra é a \cref{thm:g7:priorities:distributivity}` → `é o`

The mirror check (masculine article in front of `prop:`/`def:`/`rem:`/`not:`)
returned nothing. No `fig:`, `tab:` or `sec:` cross-references exist in this
book.

---

## 5. Term config and `\omterm` parity

`tools/term_config/book1_pt.py` was rewritten as a curated config — not a
translation of the English one, because the traps are different.

| | English | Portuguese |
|---|---:|---:|
| `\omterm` links | 3 899 | **3 459** |
| distinct targets | 79 | 80 |
| targets in EN but not PT | — | **0** |
| targets in PT but not EN | — | **1** (`def:g6:wholes:place`) |

**The single target divergence.** English never links `place value` outside
its own definition (the phrase does not recur); Portuguese `valor posicional`
recurs in the figure caption and in the grade-6 exercises, so it earns links.
A property of the two languages' phrasing, not a wrong-sense link.

### 5.1 The link-count gap, measured

The gap is **440 links (11.3 %)**, re-measured after the 2026-08-01
`lang_pt.py` flip. An early version of this file attributed it entirely to the
`par`/`pares` decision. That was wrong on two counts: the count itself was
corrupted by the protector bug of §10, and the `par` decision is only about a
third of what is left. Measured by temporarily lifting each cause and re-running
the generator (dry runs, config restored immediately):

| Cause | Links | Share |
|---|---:|---:|
| **`par` / `pares` dropped from the vocabulary** (deliberate) | 137 | 31 % |
| **Gender inflection the engine cannot reach** | ~303 | 69 % |

The compound-plural component of this gap — the third cause in earlier
versions of this table — was closed by the flip and is now zero: every regular
compound plural is generated by the rule, and §11.3 verifies occurrence-by
-occurrence that none is left unlinked.

**Cause 1 — the `par` decision, and it stands.** Portuguese `par` is both
*even* and *a pair*, and counted in context the pair sense wins outright from
grade 5 on: `os pares de Gauss`, `dois pares de paralelas`, `pares opostos
iguais`, `os pares $(30, 15)$ e $(80, 120)$`, `quantos pares de alunos`.
Linking the bare word would have produced 137 links, a large fraction of them
confidently wrong, to `def:g3:numbers:evenodd`. This is the strategy the
English config already uses for its geometry furniture (`square`, `triangle`,
`angle`), applied to the one Portuguese homograph that matters. `ímpar` /
`ímpares` keeps its link — it has no second sense. (English, for the record,
places 169 links on that definition, one of which — `break-even` — is itself
wrong-sense.)

**Cause 2 — gender, and it is not fixable at book level.** Portuguese
adjectives inflect for gender as well as number, and verbs conjugate;
`tools/term_config/lang_pt.py` now derives the plural of every word of a
phrase, but nothing beyond the plural. The per-target deficits are dominated by
exactly those words (numbers below are post-flip and, apart from the symmetry
definitions, unchanged by it):

| Target | EN | PT | What PT cannot reach |
|---|---:|---:|---|
| `def:g6:lines:perp` | 174 | 61 | `paralelo`, `paralelos`, `paralela`, `perpendicular` (only `paralelas` / `perpendiculares` are derived) |
| `def:g3:division:half` | 247 | 156 | invariant English `half` vs. the noun `metade`, plus `meia`/`$\frac12$` |
| `def:g3:numbers:evenodd` | 176 | 96 | cause 1 |
| `def:g4:numbers:round` | 46 | 2 | `arredonde`/`arredondado`/`arredondando`… conjugations, and the sentence-initial imperative blocked by `NO_CAPITAL` |
| `def:g6:shapes:triangles` | 146 | 109 | gendered forms of `isósceles`/`equilátero`/`retângulo` |

I tried to recover the largest of these from the config — `DERIVED` entries
mapping `retas paralelas` and `paralelas` onto `paralelo` / `paralelos` /
`paralela` / `perpendicular` — and the generator emitted **0** additional
links in both shapes of the experiment. I re-ran the same experiment after the
flip: still **0**. `DERIVED` does not reach singular gendered forms of an
ambiguous, nearest-preceding term, because it only extends the *unambiguous*
map. This limitation is now recorded in the `lang_pt.py` docstring, and
Spanish carries it identically; a residual gap against English is expected
here and is not a defect.

The rest of the curation:

- **STOP + hard DROP**: `reta`, `oposto(s)`, `ângulo`, `triângulo`,
  `retângulo`, `círculo`, `quadrado`, `par`, `pares`, plus the sentence-shaped
  pseudo-term `valor de um algarismo depende da posição dele` (the same defect
  the EN and FR configs drop by name).
- **SOFT** (stoplisted globally, still linked inside their own chapter):
  `escala`, `classes`, `aresta`/`arestas`.
- **`NO_CAPITAL`**: `arredondar`, `desenvolver`, `divide`.
- **`EXTRA_PROTECT`** — the spans no link may enter:
  - `volume do ensino médio` / `volumes de graduação` / `volume da série` —
    prose cross-references to the other books of the series, not the content
    of a solid (19 occurrences; the single most damaging trap in this book);
  - `raios de sol`, `raios de luz`, `raios paralelos`, and the emphasised
    `\emph{raios}` of the Thales problem — a *ray*, not a radius (the shadow
    and pinhole-camera passages);
  - `o resto do problema`, `o resto é admitido` — *the rest*, not a remainder;
  - `divide em dois`, `divide ao meio`, `divide $ABC$` — the geometric split,
    not the arithmetic relation `$b$ divide $a$` (the uppercase test is what
    separates the two: point names are capitals, number variables are not);
  - `ao cubo`, `com o cubo`, `metros cúbicos`, `quadrado--cubo` — the power
    and the unit, not the solid;
  - `escala de $1$…`, `escala $1 : 25\,000$` — the numeric map scale.
- **`AMBIG_POLICY = "nearest-preceding"`** (school book, spiral curriculum), so
  `fração`, `volume`, `área`, `perímetro`, `cilindro`, `pirâmide`, `divisor`,
  `múltiplo`, `face`, `vértice`, `potência`, `proporcionalidade` each link to
  whichever of their two or three definitions the reader has already met.
  (`potência` was initially forced to the grade-8 definition through `EXTRA`;
  that was removed once the parity table showed it stealing grade-9's
  `def:g9:fractions:power`.)

- **`DERIVED`** — 8 entries, the compound plurals the shared `(?:e?s)?`-per-word
  rule genuinely cannot build (`-ão`/`-ões`, `-al`/`-ais`, `-m`/`-ns`, and the
  accent shift `raiz`/`raízes`). It was 27 entries before the 2026-08-01
  `lang_pt.py` flip; the trim and its verification are §11.

**Spanish traps that Portuguese does not have** — checked, and recorded in the
config docstring so nobody re-adds them: `média` is never *half* (Portuguese
says `meia hora`); `cara` is heads-of-a-coin only and never a face of a solid,
so `face` needs no masking; `divide` is the third-person form (the imperative
is `divida`), so the arithmetic relation keeps its link.

**Terminology decision recorded**: `ponto decimal`, not `vírgula decimal`. The
printed numerals of the whole series use a decimal *point* (`$1.5$ h`,
`$0.482$`), so the term must name the mark actually on the page — the same
reasoning the Spanish pass used for `punto decimal`.

---

## 6. Quoted samples, with verdicts

**Grade 1 — opening of the book.**

> Quantas bolinhas de gude? Contar responde à primeira pergunta da
> matemática. Neste capítulo contamos coleções pequenas, escrevemos os
> números de $0$ a $20$ e comparamos: quem tem mais?

*Verdict: good.* Short sentences, a concrete Brazilian object (`bolinhas de
gude`), the first-person plural a Brazilian primary teacher actually uses. No
baby-talk, no diminutive padding.

**Grade 5 — the bar chart** (`parts/grade-5/pt/08-problems-and-charts.tex`).

```latex
  symbolic x coords={Jan,Fev,Mar,Abr,Mai,Jun},
  \addplot[fill=omDef!30, draw=omDef] coordinates
    {(Jan,60) (Fev,45) (Mar,55) (Abr,70) (Mai,80) (Jun,30)};
```

*Verdict: good.* Month abbreviations localised; `symbolic x coords` kept ASCII
because accented UTF-8 breaks pgfplots — grade 7 needed the
`xtick=data` + `xticklabels={futebol,natação,tênis,judô}` variant for the same
reason. Drawing code otherwise byte-identical to English.

**Grade 8 — a weekend-problem question stem.**

> Deduza que $BM = MG = GJ$ e conclua: $BG = 2 \times GJ$ --- o ponto $G$
> fica sobre a mediana $[BJ]$ a dois terços do caminho a partir do vértice
> $B$.

*Verdict: good.* Imperatives in the register a Brazilian textbook uses for
problem stems (`Deduza`, `conclua`); `a dois terços do caminho` rather than a
calque of "two thirds of the way".

**Grade 9 — the irrationality proof.**

> $a$ e $b$ pares significa os dois divisíveis por $2$ --- mas $\frac ab$ era
> irredutível, sem divisor comum nenhum. Contradição: a fração suposta não
> pode existir.

*Verdict: good.* `irredutível` (the Brazilian term, not a calque of "in lowest
terms"), `sem divisor comum nenhum` (natural double negative), and the
register has tightened correctly for a 15-year-old.

**Grade 9 — a definition head.**

> Sejam $a$ e $b$ números inteiros positivos. Dizemos que $b$ *divide* $a$
> (ou que $b$ é um divisor de $a$, ou que $a$ é um *múltiplo* de $b$) quando
> $a = b \times k$ para algum inteiro $k$.

*Verdict: good.* This is the sentence the old tree rendered with `Deixar`.
`Sejam … Dizemos que` is the standard Brazilian mathematical opening.

---

## 7. Why not 100

The five lost points, mapped to the dimensions that lost them (§1):

1. **Link layer, −3 of 10.**
   - **−2: I shipped a `$`-consuming protector** (§10). Two `EXTRA_PROTECT`
     patterns silently destroyed 235 links across seven files, and I reported
     the corrupted total as a finished number with a confident (wrong)
     explanation of the gap. The failure mode is documented in the header of
     `tools/termlink/protect.py`; I did not read it before writing regexes
     that touch `$`. Caught by the coordinator, not by me.
   - **−1: the layer is 11.3 % shorter than English** (3 459 vs 3 899). Two
     thirds of that is gender inflection no config can reach (§5.1, and now
     documented in the shared `lang_pt.py`); the remaining third is the
     deliberate `par`/`pares` decision. Neither is a defect, but the reader of
     the Portuguese edition does get fewer links than the reader of the
     English one, and the score should say so.
2. **Register, −1 of 25.** The prose is idiomatic Brazilian throughout, but in
   a handful of grade-7/8 exercise stems it follows the English sentence shape
   a shade more closely than a Brazilian author writing from scratch would.
3. **Terminology, −1 of 20.** A few choices a Brazilian editor could
   reasonably overturn (`geratriz` vs `apótema` in the cone passages,
   `coeficiente angular` vs `taxa de variação` in grade 9).

**No longer deducted.** Earlier versions of this list carried a −1 for the
hand-maintained `DERIVED` map forced by `lang_pt.py` lacking
`TAIL_ON_EVERY_WORD`. The orchestrator applied that flag on 2026-08-01 and the
map is down to the 8 genuinely irregular forms (§11), so the maintenance
liability is gone. The hyphenation caveat of §2 is **not** scored: the build
gates are green as they stand, and the missing `.ldf` is an environment
limitation rather than a property of the translation.

---

## 8. Shared-file change — requested here, **APPLIED by the orchestrator**

**`tools/term_config/lang_pt.py` now sets `TAIL_ON_EVERY_WORD = True`** (flip
made by the orchestrator on 2026-08-01, with a docstring recording the
history, the trim rule and the gender limitation measured here).

The request, as it stood: `lang_fr.py` and `lang_es.py` both set the flag;
`lang_pt.py` did not, so the plural was appended to the **last word only** —
`número primos`, `triângulo retângulos` — which is not how a Portuguese noun
phrase pluralises: every word inflects (*número primo* → *números primos*,
*triângulo retângulo* → *triângulos retângulos*, *raiz quadrada* → *raízes
quadradas*, *função afim* → *funções afins*). Until the flip, every `pt` book
carried a hand-written `DERIVED` workaround — the same one the Spanish books
carried before their own flag was corrected.

**What it changed here** is written up in full in §11: `DERIVED` trimmed
27 → 8, links 3 450 → 3 459, and the compound-plural component of the
EN-vs-PT gap closed to zero. I did not edit `lang_pt.py`; my scope was
`book1_pt.py`, my bodies, and this file.

I did **not** touch `tools/term_config/lang_pt.py`, `tools/termlink/**`,
`tools/link_defined_terms.py`, `tools/check_translation.sh`,
`styles/lang/pt.tex`, `styles/onemath.sty`, `latexmkrc`, the entry file,
`frontmatter/preface.pt.tex`, or any file belonging to another book or another
language.

---

## 9. Unfinished

Nothing in scope. All 142 files are rewritten, all nine gates pass, the link
check is green and idempotent, and the book builds clean.

One item remains for the orchestrating session: a re-check of overfull boxes
and page count once Portuguese babel is installed (§2). The other item this
section used to list — the `lang_pt.py` flip — was applied on 2026-08-01 and
regenerated here (§11).

No git commit was created; the working tree is left for review.

---

## 10. Errata — the `$`-consuming protector (found and fixed the same day)

### What was wrong

`tools/termlink/protect.py` states the rule in its own header:

> NEVER CONSUME A `$`. The whole list is one alternation scanned left to
> right, so a pattern that eats an opening `$` leaves the inline-math rule
> pairing the *closing* `$` with the next formula's opening one — and from
> there every span is masked inside out for the rest of the file. It reports
> no error; the link count just quietly collapses.

Two of my `EXTRA_PROTECT` patterns did exactly that:

```python
r'divide\s+\$[A-Z]'     # masks "divide $ABC$ ao meio" -- and eats the opening $
r'escala\s+\$'          # masks "escala $1 : 25\,000$" -- and eats the opening $
```

Both now match the word and leave the `$` to the math rule:

```python
r'divide\s+(?=\$[A-Z])'
r'escala\s+(?=\$)'
```

I re-read the whole `EXTRA_PROTECT` list afterwards with a script that flags
every literal `\$` not immediately preceded by `(?=`: these two were the only
offenders, and no `STOP`, `DROP`, `EXTRA` or `DERIVED` string contains a `$`
at all.

### What it cost, and where

Seven files contained a trigger phrase, and every link *after* it in the file
was silently lost. Recovery, measured per file:

| File | before | after | recovered |
|---|---:|---:|---:|
| `grade-9/pt/08-solids-and-volumes.tex` | 54 | 151 | **+97** |
| `grade-9/pt/02-arithmetic-gcd.tex` | 22 | 77 | **+55** |
| `grade-9/pt/06-thales-theorem.tex` | 16 | 42 | **+26** |
| `grade-7/solutions/pt/07-triangles-and-angles.tex` | 7 | 31 | **+24** |
| `grade-7/pt/05-proportionality.tex` | 18 | 35 | **+17** |
| `grade-6/pt/08-proportionality-and-data.tex` | 15 | 24 | **+9** |
| `grade-8/solutions/pt/06-midpoints-and-parallels.tex` | 35 | 42 | **+7** |
| **total** | | | **+235** |

By pattern: `escala\s+\$` cost **149** links across four files;
`divide\s+\$[A-Z]` cost **86** across three. The book-wide total went
**3 216 → 3 451**, and the per-file deltas sum to exactly the book-wide delta,
which confirms no other file was affected.

**The vocabulary itself was never damaged.** Running `--terms` with the buggy
patterns and with the fixed ones produces byte-identical term→target lists,
so nothing was ever dropped from the dictionary; only link *placement* inside
those seven files was corrupted. Target parity with English (79 EN / 80 PT,
one explained divergence) is unchanged before and after.

### Audit of the recovered links

The 235 links had never been visible, so none had been sense-checked. I
enumerated every distinct `\omterm{target}{display}` pair in the seven files
(93 distinct pairs) and read each in context. Findings:

- **One wrong-sense link**, now masked: in the Thales weekend problem,
  `O teorema de Tales é a matemática dos \emph{raios}` — *rays* of light, not
  radii — had been linked to `def:g3:shapes:shapes`. A new
  `EXTRA_PROTECT` entry `r'\\emph\{raios\}'` removes it. Final count
  **3 450**.
- **Every other recovered link is correct-sense**, including the ones the
  config was written to police: all 37 remaining `raio` links are radii, all
  26 `volume` links are contents of solids (the `volume do ensino médio` /
  `volumes de graduação` cross-references stayed masked), all 7 `resto` links
  are remainders (`o resto do problema` stayed masked), all 6 `divide` links
  are the arithmetic relation (`divide ao meio` stayed masked), and
  `metros cúbicos` stayed masked.
- **`par` specifically**: **zero** links on bare `par`/`pares` anywhere in the
  book, as designed — the recovery did not smuggle any in.

### Post-fix verification

All nine `check_translation.sh grade-N pt` gates **PASSED**;
`link_defined_terms.py --check` green; `latexmk` exit 0 with **0 errors,
0 undefined, 0 overfull**, 428 pages.

### What I changed in this file as a result

`\omterm` count 3 216 → **3 450** (§5); the EN-vs-PT gap re-measured and
re-attributed (§5.1 — it is 31 % the `par` decision and 69 % morphology, not
"almost entirely" the `par` decision as first written); link-layer dimension
re-scored **8 → 7**; overall **96 → 95**.

I did **not** touch `tools/termlink/protect.py` or
`tools/term_config/lang_pt.py`.

---

## 11. Regeneration against `TAIL_ON_EVERY_WORD = True` (2026-08-01)

The orchestrator flipped the shared flag (§8). This section records what that
did to Book 1.

### 11.1 The `DERIVED` trim: 27 → 8

With the tail now optional on **every** word, `(?:e?s)?` per word generates the
regular compound plurals by itself. I classified all 27 entries mechanically —
generating every string the rule can build for each base and testing the
declared plural against that set — rather than by eye:

**Removed, 19** (the rule builds them):

`triângulo retângulo` · `triângulo isósceles` · `triângulo equilátero` ·
`número primo` · `número par` · `número ímpar` · `número relativo` ·
`ângulo reto` · `eixo de simetria` · `centro de simetria` ·
`bloco retangular` · `coeficiente angular` · `frequência absoluta` ·
`frequência relativa` · `terno pitagórico` · `quarta parte` ·
`velocidade média` · `média ponderada` · `círculo circunscrito`

Note the shapes that *look* irregular but are not: `par` → `pares` and
`angular` → `angulares` are just `+es`, and `isósceles` is invariant, which the
optional tail handles.

**Kept, 8** (the rule cannot build them):

| Entry | Why the tail fails |
|---|---|
| `raiz quadrada` → `raízes quadradas` | `-z` → `-zes` **plus an accent shift**: the rule can only reach `raizes` |
| `função linear` → `funções lineares` | `-ão` → `-ões` |
| `função afim` → `funções afins` | `-ão` → `-ões` and `-m` → `-ns` |
| `expressão literal` → `expressões literais` | `-ão` → `-ões` and `-al` → `-ais` |
| `seção transversal` → `seções transversais` | `-ão` → `-ões` and `-al` → `-ais` |
| `notação científica` → `notações científicas` | `-ão` → `-ões` |
| `número decimal` → `números decimais` | `-al` → `-ais` |
| `ponto decimal` → `pontos decimais` | `-al` → `-ais` |

**One removed entry was *inert*, not merely redundant.** `eixo de simetria` is
ambiguity-resolved (`def:g4:symmetry:def` in grade 4, `def:g6:symmetry:axis`
from grade 6), and `DERIVED` only extends the *unambiguous* map — so that
declaration had never produced a single link in any version of this book. It
is the entire +9 of §11.2: once the rule generates the plural, the normal
nearest-preceding machinery resolves it correctly per chapter. I checked every
other `DERIVED` key against the ambiguous-term list; it was the only one.

I also checked the reverse trap — an entry dropped as "regular" that the rule
in fact cannot build (the `ordem`/`ordens`, `-m` → `-ns` case that bit the
physics book). Book 1's vocabulary contains exactly one `-m` word, `afim`, and
it is kept. §11.3 verifies the rest empirically rather than by reading.

### 11.2 What the flip changed

| | before | after |
|---|---:|---:|
| `DERIVED` entries | 27 | **8** |
| `LINKABLE TERMS` | 115 | 97 (the 19 declared plurals are no longer separate vocabulary entries — the rule makes them) |
| `\omterm` links | 3 450 | **3 459** (+9) |
| distinct target/display pairs | 265 | 268 |
| distinct targets | 80 | 80 |

Diffing the pair sets: **three new pairs and nothing else** —
`{def:g4:symmetry:def}{eixos de simetria}` (×2),
`{def:g6:symmetry:axis}{eixos de simetria}` (×6),
`{def:g6:symmetry:axis}{Eixos de simetria}` (×1). **No pair disappeared, and
no count changed on any of the 265 surviving pairs**, which is the proof that
the 19 removals cost nothing: the rule reproduces every link the declarations
used to make.

### 11.3 Occurrences-vs-links verification

Reading the list is not enough, so I counted. For every multi-word term in the
vocabulary I built its true Portuguese plural and counted, across the 142
files, how many occurrences carry a link and how many do not:

```
   removed from DERIVED        occurrences   linked   unlinked
   ângulos retos                       30       22          8
   números relativos                   14        6          8
   frequências relativas               15       13          2
   números ímpares                     12       11          1
   eixos de simetria                   10        9          1
   triângulos retângulos               10        8          2
   …
```

The unlinked residue is **not** a Portuguese gap: the linker never links a term
inside its own definition, inside headings, or inside protected spans. Running
the identical metric on the English tree gives the same ratios term for term —
`right angles` 32/24/8 against `ângulos retos` 30/22/8, `prime numbers` 7/4/3
against `números primos` 7/4/3, `relative numbers` 14/6/8 against
`números relativos` 14/6/8, `square roots` 12/4/8 against `raízes quadradas`
12/4/8. Portuguese compound plurals now behave exactly like the English ones.

### 11.4 Audit of the newly appearing links

All 9 were unreachable before, so none had been sense-checked. All 9 are
`eixos de simetria` / `Eixos de simetria` in the axial-symmetry material, all
correct-sense, and each resolves to the right definition for its grade:

> Trace os `\omterm{def:g4:symmetry:def}{eixos de simetria}` de: um quadrado; um
> retângulo; um…  *(grade 4)*
>
> as diagonais dele \emph{não} são
> `\omterm{def:g6:symmetry:axis}{eixos de simetria}` (dobre…  *(grade 6)*

One of them spans a source line break (`{eixos de\nsimetria}`); LaTeX takes it
and the build is clean.

**`par` specifically**, since the flip is exactly the kind of change that could
smuggle a dropped word back in through a compound: **zero** links on bare
`par`/`pares` anywhere in the book, unchanged. Lifting the drop in a dry run
still reports exactly **137** links, the same number as before the flip — the
decision is untouched by the new rule, as expected for a single word.

### 11.5 Re-verification

All nine `check_translation.sh grade-N pt` gates **PASSED**;
`link_defined_terms.py --check` green **and idempotent** (a second plain
`--apply` inserts 0 links); `latexmk` exit 0 with **0 errors, 0 undefined,
0 overfull**, 428 pages. Target parity with English unchanged: 79 EN / 80 PT,
the one explained `def:g6:wholes:place` divergence.

I re-ran the gender experiment under the new flag — `DERIVED` mapping
`paralelas` and `retas paralelas` onto `paralelo`/`paralelos`/`paralela`/
`perpendicular` — and it still emits **0** links. The flip fixes compound
plurals, not gender, exactly as the new `lang_pt.py` docstring says.

### 11.6 Score: unchanged, and why

**95/100 stands, and the link dimension stays at 7/10.** The flip added 9 links
(+0.26 %) and retired a maintenance liability, which is real but small; the
three points off the link dimension were never about the count — they are for
shipping a `$`-consuming protector that silently destroyed 235 links (§10) and
for the 11 % residual gap, and neither changes here. Nudging the score up for a
9-link gain would be flattering the work rather than measuring it. The one
thing that did move is the "why not 100" list in §7, which no longer carries
the hand-maintained-`DERIVED` deduction; the arithmetic there has been
re-mapped onto the dimension table so the two agree.
