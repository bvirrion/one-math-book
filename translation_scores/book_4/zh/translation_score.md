# Translation score: One Math Book 4, Simplified Chinese (`zh`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 4 (University Year 2), `one_math_book_4_university_year_2_zh.tex` |
| **Language** | Simplified Chinese (`zh`), mainland textbook usage |
| **Overall score** | **88 / 100**, sampled: 20 passages, seed 1 (15 course, 5 solutions), not read in full |
| **Ship status** | **Pilot tier**: gates green; not read sentence by sentence; figures checked by script and by eye on the 4 pages whose figures carry Chinese labels |
| **Date** | 2026-11-17 |
| **Model** | `claude-haiku-5-5` (Haiku 5.5, effort medium), pilot method: one headless call per section, 1,125 calls (translation and retries over 5 passes); glossary, infrastructure, the 4 hand-finished sections and coordinator `claude-opus-5-5` (Opus 5.5), one coordinator for Books 1–5, no subagents |
| **Canon** | English as committed; no English defect found. |
| **Tokens** | Haiku: 1,125 calls, about $17.1 list price (`draft/pilot-bachelor-2-zh/post2.log`): like Book 3, the year ran across the weekly-limit pause and five passes. Coordinator: shared with the run; weekly plan 6 % at this close (`sources/TRANSLATION_BOOKS_1-5_ZH.md`) |
| **Scope** | 23 chapters + 23 solution files under `parts/bachelor-2/zh/` and `parts/bachelor-2/solutions/zh/`; glossary `sources/GLOSSARY_BOOK_4_ZH.md`; term config `tools/term_config/book4_zh.py` |

## Verdict

Clear university Chinese with the standard terms (收敛半径, 概率母函数, 黑塞矩阵, 符号差, 邓福德分解, 弗勒内标架,
不放回抽取). Proofs and solutions keep their structure (等于收敛级数减去前者，从而也收敛；于是…将收敛，与假设矛盾).
The weaker passages are the English book's flourishes rendered literally (*直觉需要的是指数，而非线性的“尺子”*,
*球的圆润性至关重要*). No sentence in the sample was wrong in mathematical sense.

## Build and gates

- `build/one_math_book_4_university_year_2_zh.pdf`: 365 pp (English 397). Errors 0, undefined 0, overfull 0, nullfont 0,
  missing character 0, invalid-in-math 0, zero-height 0. TeX Live 2026. Index by pinyin.
- `tools/check_translation.sh bachelor-2 zh`: PASSED.
- `link_defined_terms.py --book 4 --lang zh --check`: every file matches; 3,218 links to 88 targets (English 3,511 to 85).
- `pdfsweep.py` against the French PDF: 6 English-only word types: the licence URL, two index keys left in English
  (*Jensen's inequality*, *Stirling's formula*: fixed to 詹森不等式, 斯特林公式) and PDF-extraction artefacts of formulas
  (*lnlnxnn*, *lnkk*, *sodd*).

## What was read

- Text: 20 passages (seed 1); the sweep, number and PDF-sweep reports.
- Numbers: every NUMDIFF line traced; "Year 3" split over two lines is 本科 / 三年级; none lost.
- Figures: the overlap script over every page (its 17 hits were inline fractions in prose); contact sheets of the 4
  pages whose figures carry Chinese labels. One collision fixed (*曲率中心* across the osculating circle, page 180; the
  English label crosses it too).

## Defects found and fixed, by class

| Class | Count | Example | Fix |
|---|---:|---|---|
| Section rejected after 5 passes | 4 | `(X - \lambda_i)^{m_i}（` with the `$` lost; `$f(1,0)$` / `$= 2$` split | by hand from the last reply |
| False rejection | 1 | `\index{谱定理}` inside a display read as changed math | `id_apply.py` blanks `\index` in math |
| Mathematician's name in Latin | 113 | Hoeffding, Frenet, Beta, Abel, Fubini, AM--GM | 霍夫丁, 弗勒内, 贝塔, 阿贝尔, 富比尼, 算术–几何平均不等式 |
| A line absorbing the next English line | 3 | `由此` then `uniformly). Hence` | by hand |
| English word in `\text{}` or prose | 5 | `\text{ even}`, `(\text{cut, both ways})`, `limsup` | 为偶数, 割线，往返各一次, 上极限 |
| English index key | 2 | `\index{Jensen's inequality}` | 詹森不等式 |
| Two names for one notion | 2 | 生成函数 / 母函数, 高斯约化 / 高斯化简 | 母函数, 高斯化简 |
| Roman part numbers | 7 | `Part III ---`, 第 I--II 部分 | 第三部分, 第一至二部分 (sweep) |
| Doubled word across a line break | 1 | 在 / 在 $\C$ 上 | by hand |
| English spaced em dash | ~880 | `--- 请说明理由` | `——` (sweep) |

## Term links

- Dropped as wrong in Chinese: 收敛 (any convergence, linked 224 times to the improper integral against English 20),
  交错 (inside 交错级数), 代数 (inside 线性代数, 代数重数), and three problem results named only in Chinese.
- Declared in `EXTRA` (English reaches them through index-only keys): 共振, 母函数, 阿贝尔求和, 高斯化简, 含参积分,
  沃利斯积分, 狄利克雷核, 邓福德分解, 卡塔兰数, 分支过程, 范数等价.

## Known limits of this edition

- One-character terms are never linked (`CJK_MIN_CHARS = 2`).
- 等价 (equivalent norms) stays soft-stopped: in Chinese it is also asymptotic equivalence and "equivalent statements";
  English links it 13 times.
