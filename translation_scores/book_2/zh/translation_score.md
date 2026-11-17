# Translation score: One Math Book 2, Simplified Chinese (`zh`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 2 (High School, grades 10–12), `one_math_book_2_high_school_zh.tex` |
| **Language** | Simplified Chinese (`zh`), mainland textbook usage |
| **Overall score** | **88 / 100**, sampled: 20 passages, seed 1 (7 from grade 10, 7 from grade 11, 6 from grade 12), not read in full |
| **Ship status** | **Pilot tier**: gates green; not read sentence by sentence; figures sampled (all by script; the 4 on the 30 seeded pages and the 3 pages whose figures carry Chinese labels by eye) |
| **Date** | 2026-11-17 |
| **Model** | `claude-haiku-5-5` (Haiku 5.5, effort medium), pilot method: one headless call per section, 502 calls (translation, retries and repairs); glossary, infrastructure and coordinator `claude-opus-5-5` (Opus 5.5), one coordinator for Books 1–5, no subagents |
| **Canon** | English as committed; no English defect found. |
| **Tokens** | Haiku: 502 calls, about $5.3 list price (per year in `draft/pilot-grade-1{0,1,2}-zh/post2.log`). Coordinator: shared with the run; weekly plan 94 % after Book 1, 96 % after this book (`sources/TRANSLATION_BOOKS_1-5_ZH.md`) |
| **Scope** | 35 chapters + 35 solution files under `parts/grade-{10,11,12}/zh/` and `parts/grade-{10,11,12}/solutions/zh/`; glossary `sources/GLOSSARY_BOOK_2_ZH.md`; term config `tools/term_config/book2_zh.py` |

## Verdict

Clear high-school textbook Chinese with the standard mainland terms (提公因式, 斜截式方程, 等比数列, 首项系数, 二次三项式,
真数, 不放回抽取, 闭途径). Proofs and solutions read as a Chinese teacher would write them (故非等比数列, 解集为…).
The weaker passages are the English book's flourishes rendered literally: *临别礼物* ("a parting gift"), *巧克力条式做法*,
*驯服它的结构*. No sentence in the sample was wrong in sense.

## Build and gates

- `build/one_math_book_2_high_school_zh.pdf`: 307 pp (English 330). Errors 0, undefined 0, overfull 0, nullfont 0,
  missing character 0, invalid-in-math 0, zero-height 0. TeX Live 2026. Index by pinyin: 177 entries.
- `tools/check_translation.sh grade-N zh`: PASSED for N = 10, 11, 12.
- `link_defined_terms.py --book 2 --lang zh --check`: every file matches; 4,730 links (4,622 at the close; +108
  after the Book 3 close let two-character terms defined once be harvested: 中点, 焦点, 准线, 垂心, as English).
- Found at the Book 3 close and fixed: 13 index keys had a full-width `！` (`\index{极限！数列的}`), which made a
  sub-entry a separate entry; the punctuation pass now skips `\index`. Rebuilt 2026-11-17: 307 pp, 0/0/0.
- `pdfsweep.py` against the French PDF: 2 English-only word types, *sigmoid* (kept, as Chinese writes it) and *rxex*
  (a PDF-extraction artefact of an integral, also in English).

## What was read

- Text: 20 passages (seed 1); the sweep, number and PDF-sweep reports.
- Numbers: every NUMDIFF line traced: grades written as words (十二年级), 约两千年前 for "about 2000 years ago",
  五五开 for "50--50", and formulas moved to the neighbouring line; none lost.
- Figures: the overlap script over every figure (its hits were vector arrows in prose); contact sheets of the figures
  on the seeded pages and of every page whose figure carries a Chinese label (3). Two labels touch their line or a
  dot (割线 on page 79, 等差数列 on page 87); not fixed.

## Defects found and fixed, by class

| Class | Count | Example | Fix |
|---|---:|---|---|
| Title left in English | 2 | `\chapter{Functions and Variations}` | `repair.py` |
| A line absorbing the next English line | 2 | `才能判定无理性。` then `can settle irrationality.` | by hand |
| Name or word left in English | 13 | *Chasles*, *Nine Chapters*, *Hemachandra--Fibonacci*, “lottery” | 沙勒, 《九章算术》, 赫马钱德拉–斐波那契, “彩票” |
| English word in `\text{}` | 4 | `\text{if }`, `\text{red}`, `\text{and}` | 若, 红, 且 |
| Noun before `\cref` | 2 | `验证定理\cref{thm:…}` | noun removed |
| Grade named two ways | 4 | 高三 beside 十二年级 | 十二年级 |
| A Chinese character just before a table row's `\\` | 1 build error | `& 顺序无关\\` | a space before `\\` (sweep, all books) |
| Unicode ε in prose | 1 | `；ε、` | `$\varepsilon$` |
| Overfull display | 1 | `\text{ 在区间 }` ×3 | `\text{ 于 }` |
| Space inside inline math | 2 | `$3x + 2y = $ 常数` (as in English) | `$3x + 2y =$` |
| English spaced em dash | ~600 | `--- 这就是` | `——` (sweep) |

## Known limits of this edition

- One-character terms are never linked (`CJK_MIN_CHARS = 2`). English links *root* to the discriminant 20 times in
  grade 12; 根 sits inside 平方根 and 根号, so it is dropped.
- Some notions link to a different year's definition than English (nearest-preceding policy), e.g. 共线向量.
