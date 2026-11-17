# Translation score: One Math Book 3, Simplified Chinese (`zh`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 3 (University Year 1), `one_math_book_3_university_year_1_zh.tex` |
| **Language** | Simplified Chinese (`zh`), mainland textbook usage |
| **Overall score** | **88 / 100**, sampled: 20 passages, seed 1 (15 course, 5 solutions), not read in full |
| **Ship status** | **Pilot tier**: gates green; not read sentence by sentence; figures checked by script and by eye on the 10 pages whose figures carry Chinese labels |
| **Date** | 2026-11-17 |
| **Model** | `claude-haiku-5-5` (Haiku 5.5, effort medium), pilot method: one headless call per section, 1,182 calls (translation, retries over 5 passes, 2 repairs); glossary, infrastructure, the 10 hand-finished sections and coordinator `claude-opus-5-5` (Opus 5.5), one coordinator for Books 1–5, no subagents |
| **Canon** | English as committed; no English defect found. |
| **Tokens** | Haiku: 1,182 calls, about $17.3 list price (`draft/pilot-bachelor-1-zh/post2.log`), three times Book 2's: the year ran across the weekly-limit pause and five passes, and 10 sections were still rejected after them. Coordinator: shared with the run; weekly plan 0 % at the resume, 6 % at this close (`sources/TRANSLATION_BOOKS_1-5_ZH.md`) |
| **Scope** | 25 chapters + 25 solution files under `parts/bachelor-1/zh/` and `parts/bachelor-1/solutions/zh/`; glossary `sources/GLOSSARY_BOOK_3_ZH.md`; term config `tools/term_config/book3_zh.py` |

## Verdict

Clear university Chinese with the standard terms (线性无关, 张成的子空间, 补子空间, 等距变换, 相邻数列, 比值判别法,
过渡矩阵, 欧几里得除法). Proofs keep their structure and their logical words (下面分两个方向证明, 由…可得, 从而).
The weaker passages are, as in Books 1–2, the English book's flourishes rendered literally (*求交则不然*,
*原理相同，只是形式不同*); one sample sentence was garbled (*对三角形作变换时三角形也相应地变换它们*) and is fixed.
No sentence in the sample was wrong in mathematical sense.

## Build and gates

- `build/one_math_book_3_university_year_1_zh.pdf`: 363 pp (English 395). Errors 0, undefined 0, overfull 0, nullfont 0,
  missing character 0, invalid-in-math 0, zero-height 0. TeX Live 2026. Index by pinyin.
- `tools/check_translation.sh bachelor-1 zh`: PASSED.
- `link_defined_terms.py --book 3 --lang zh --check`: every file matches; 3,954 links to 101 targets (English 3,944 to 106).
- `pdfsweep.py` against the French PDF: 3 English-only word types, *span* (`\operatorname{span}`, as in English),
  *rurruru* (a lattice path written as its letters) and *coshcosh* (a PDF-extraction artefact).

## What was read

- Text: 20 passages (seed 1); the sweep, number and PDF-sweep reports.
- Numbers: every NUMDIFF line traced. "Year 2/3 volume" is written 本科二/三年级分册, "Route 1" 路线一, "8-puzzle"
  八数码, and the rest moved to a neighbouring line; none lost.
- Figures: the overlap script over every page (its 19 hits were inline fractions and sums in prose); contact sheets of
  the 10 pages whose figures carry Chinese labels. One collision fixed (*r₁ 的轴* on *r₁(M)*, page 219).

## Defects found and fixed, by class

| Class | Count | Example | Fix |
|---|---:|---|---|
| Section rejected after 5 passes | 10 | a `$` moved to the next line; `\operatorname{diam}` written `\text{直径}`; two formulas swapped by Chinese word order | by hand from the last reply, saved through every check |
| False rejection | 3 | `\gcd(a,b) \times \operatorname{lcm}(a,b) = ab` read as English ("a" twice) | `common.py`: `\operatorname{…}` is not prose |
| Full-width `！` in an index key | 12 (+13 in Book 2) | `\index{秩！族的}` | `zh.py` masks `\index`; sweep restores `!` |
| Title or heading left in English | 6 | `[Operations plus one algebraic trick]`, `\textbf{Part I ---` | by hand; 第一部分 |
| Roman part numbers | ~200 (all books) | 第 III 部分 | sweep: 第三部分 |
| Mathematician's name in Latin | ~25 | Lipschitz, Taylor--Young, Gram, Monge | 利普希茨, 泰勒–杨, 格拉姆, 蒙日 |
| Two names for one notion | 2 | 康托集 / 康托尔集, 几何级数 / 等比级数 | 康托尔集, 等比级数 |
| A word doubled across a line break | 2 | `其` / `其存在性` | by hand |
| Greek letter or `。` in a Latin font | 2 | ζ in prose; `。` inside a display | 泽塔函数; `.` |
| Space inside inline math | 4 | `$\det = 0 = $` (as in English) | `$\det = 0 =$` |
| English spaced em dash | ~860 | `--- 亦可` | `——` (sweep) |

## Known limits of this edition

- One-character terms are never linked (`CJK_MIN_CHARS = 2`): 秩 (rank), 核/像 (kernel/image), 环 (ring), 阶 (order)
  reach no link where English has 172; 命题 (statement) is dropped because it also names every proposition (English 90).
- Index-only terms (a theorem's name with no `\emph`) are declared by hand in the config's `EXTRA`, as in French.
- Some justified lines in long exercise items stretch their characters apart where a long formula cannot break.
