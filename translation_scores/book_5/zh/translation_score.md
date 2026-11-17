# Translation score: One Math Book 5, Simplified Chinese (`zh`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 5 (University Year 3), `one_math_book_5_university_year_3_zh.tex` |
| **Language** | Simplified Chinese (`zh`), mainland textbook usage |
| **Overall score** | **88 / 100**, sampled: 20 passages, seed 1 (11 course, 9 solutions), not read in full |
| **Ship status** | **Pilot tier**: gates green; not read sentence by sentence; figures checked by script and by eye on the 3 pages whose figures carry Chinese labels |
| **Date** | 2026-11-17 |
| **Model** | `claude-haiku-5-5` (Haiku 5.5, effort medium), pilot method: one headless call per section, 1,835 calls (translation and retries over 9 passes: 5 with 3 workers, then 4 with 9 workers, user ruling 18:09); glossary, infrastructure, the 24 hand-finished sections and coordinator `claude-opus-5-5` (Opus 5.5), one coordinator for Books 1–5, no subagents |
| **Canon** | English as committed; no English defect found. |
| **Tokens** | Haiku: 1,835 calls, about $33.0 list price (`draft/pilot-bachelor-3-zh/post2.log`): the hardest year (measure theory, topology, Galois theory, complex analysis), with formulas the model kept moving; 108 sections were still rejected after its first pass. Coordinator: shared with the run; weekly plan 8 % at this close (`sources/TRANSLATION_BOOKS_1-5_ZH.md`) |
| **Scope** | 23 chapters + 23 solution files under `parts/bachelor-3/zh/` and `parts/bachelor-3/solutions/zh/`; glossary `sources/GLOSSARY_BOOK_5_ZH.md`; term config `tools/term_config/book5_zh.py` |

## Verdict

Clear university Chinese with the standard terms (稳定子, 不变因子, 塔律, 依分布收敛, 巴拿赫极限, 恒等定理,
强大数定律, 单位分解). Proofs keep their logic and connectives (故…；但…。于是…；由此推出…；事实上…不可能成功).
The weaker passages are, as in Books 3–4, the English book's flourishes rendered literally (*正二十面体尾声*).
No sentence in the sample was wrong in mathematical sense.

## Build and gates

- `build/one_math_book_5_university_year_3_zh.pdf`: 361 pp (English 395). Errors 0, undefined 0, overfull 0, nullfont 0,
  missing character 0, invalid-in-math 0, zero-height 0. TeX Live 2026. Index by pinyin.
- `tools/check_translation.sh bachelor-3 zh`: PASSED.
- `link_defined_terms.py --book 5 --lang zh --check`: every file matches; 3,008 links to 125 targets (English 4,326 to 130).
- `pdfsweep.py` against the French PDF: before the fixes, *theta*, *zeta* in prose (fixed: 西塔函数, 泽塔函数值); after,
  the licence URL and PDF-extraction artefacts of formulas (*autk*, *phkk*, *ntlnn*, *lgal*), and *even* inside
  `\mathrm{even}`, as in English.

## What was read

- Text: 20 passages (seed 1); the sweep, number and PDF-sweep reports.
- Numbers: every NUMDIFF line traced; "Year 1--2" is 本科一、二年级; none lost.
- Figures: the overlap script over every page (its 26 hits were inline fractions and sums in prose); contact sheets of
  the 3 pages whose figures carry Chinese labels; no collision.

## Defects found and fixed, by class

| Class | Count | Example | Fix |
|---|---:|---|---|
| Section rejected after 9 passes | 24 | a formula split over two lines reopened with a `$`; `$x` left open at a line end; `$H$` and `$p$` swapped by Chinese word order | by hand from the last reply; 12 of them by two scripted rules alone (a reopened formula, an unclosed one) |
| Mathematician's name in Latin | 140 | Sylow, Fubini, Rouch\'e, Gr\"onwall, M\"obius, Thomae, De Branges | 西罗, 富比尼, 儒歇, 格朗沃尔, 默比乌斯, 托马, 德布朗日 |
| One name spelled two ways | 1 | 德布朗热 / 德布朗日 | 德布朗日 |
| Half a line left in English | 5 | `$X^n - 1$ by exact order`, `needed.`, `factorizes:` | by hand |
| Greek word or letter in prose | 4 | 雅可比 theta 函数, 奇数阶 zeta 值, `ζ 值` (missing glyph) | 西塔函数, 泽塔函数值 |
| Space inside inline math | 10 | `$A = $ 第一枚` | `$A =$` |
| A word doubled across a line break | 3 | `若` / `若 $d(x, x')` | by hand |
| Roman part numbers | all | `I--VI 各部分` | 第一至六部分 (sweep and by hand) |
| English spaced em dash | ~670 | `--- 即调和级数` | `——` (sweep; the rule now also reaches lines that leave a formula open, and 76 such lines in Books 3–4) |

## Term links

- Dropped as wrong in Chinese: 分布 (law: inside every 正态/均匀/泊松分布 and 分布函数, 203 links against English 29),
  几乎处处 (linked to the L¹ definition 115 times against English 2), 最大公因数 (reached the Bézout lemma, which
  English never links); 定向 restored (orientation, English 27).
- Declared in `EXTRA` (English reaches them through index-only keys or theorem titles): 29 keys, among them 类方程,
  伽马函数, 单位分解, 诺伊曼级数, 完全域, 柯西–黎曼方程, 伽罗瓦对应, 塔律, 交错群, 恒等定理, 若尔当标准形,
  李雅普诺夫函数, 极大解, 乘积测度, 洛朗级数, 弗雷德霍姆择一定理, 拉格朗日乘子, 序列紧性.

## Known limits of this edition

- One-character terms are never linked (`CJK_MIN_CHARS = 2`): 模 (module, English 17 links), 流 (flow, English 5).
- 30 % fewer links than English: law and almost everywhere (dropped above), and *perfect* (English 23), which Chinese
  writes as 完全域 only twice.
- 稳定 (stable) links 36 times against English 16: in Chinese it is also the plain verb.
