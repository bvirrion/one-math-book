# Translation score: One Math Book 1, Simplified Chinese (`zh`)

| Field | Value |
|-------|--------|
| **Book** | One Math Book 1 (Primary / Middle, grades 1–9), `one_math_book_1_primary_middle_school_zh.tex` |
| **Language** | Simplified Chinese (`zh`), mainland textbook usage |
| **Overall score** | **88 / 100**, sampled: 20 passages, seed 1 (7 from grade 3, 7 from grade 6, 6 from grade 9), not read in full |
| **Ship status** | **Pilot tier**: gates green; not read sentence by sentence; figures sampled (all 168 by script, the 13 on the 40 seeded pages by eye) |
| **Date** | 2026-11-17 |
| **Model** | `claude-haiku-5-5` (Haiku 5.5, effort medium), pilot method: one headless call per section, 538 calls (translation, retries and repairs); glossary, infrastructure and coordinator `claude-opus-5-5` (Opus 5.5), one coordinator for Books 1–5, no subagents |
| **Canon** | English as committed. One English figure defect seen, not fixed: the √(r²−d²) label of the sphere section (grade 9, solids) sits on the radical and the ellipse in every edition. |
| **Tokens** | Haiku: 538 calls, about $4.0 list price (per year in `draft/pilot-grade-*-zh/post2.log`). Coordinator: shared with the run; weekly plan 93 % at the start, 94 % after this book (`sources/TRANSLATION_BOOKS_1-5_ZH.md`) |
| **Scope** | 71 chapters + 71 solution files under `parts/grade-{1..9}/zh/` and `parts/grade-{1..9}/solutions/zh/`; preface `frontmatter/preface.zh.tex`; glossary `sources/GLOSSARY_BOOK_1_ZH.md`; term config `tools/term_config/book1_zh.py` |

## Verdict

Natural mainland schoolbook Chinese. The young grades speak in short, warm sentences (数一数, 想一想, 照样子抄写); the
middle-school chapters use the plain textbook register (设…，则…, 称…为…, 由此可得), exercise stems in 求 / 计算 / 证明 /
判断…并说明理由. Word order is Chinese, not English: words move between the lines of a sentence, which the line
structure allows. Names take their standard forms (泰勒斯, 梅雷骑士, 爱丽丝, 汤姆). The weak points are a few calques
(*一个免费的错误检测器* for "a free error detector") and some long sentences that keep English clause order. No
sentence in the sample was wrong in sense.

## Build and gates

- `build/one_math_book_1_primary_middle_school_zh.pdf`: 401 pp (English 400). XeLaTeX + xeCJK, Fandol fonts. Errors 0,
  undefined 0, overfull 0, nullfont 0, missing character 0, invalid-in-math 0, zero-height 0. TeX Live 2026.
- Index sorted by pinyin (upmendex, `styles/zh-pinyin.ist`): 105 entries.
- `tools/check_translation.sh grade-N zh`: PASSED for N = 1…9, gate 9 (`check_chinese_prose.py`) included.
- `link_defined_terms.py --book 1 --lang zh --check`: every file matches. 3,959 links (3,923 at the close; +36 after
  the Book 3 close let two-character terms defined once be harvested, e.g. 筝形, 斜率, 截面; 中线/重心 dropped as English
  does). Rebuilt 2026-11-17: 401 pp, 0/0/0. Part numbers 第 III 部分 → 第三部分 (sweep).
- `pdfsweep.py` against the French PDF: 1 English-only word type, *november*, from `\today`; fixed (a Chinese `\today`
  in `styles/lang/zh.tex`).

## What was read

- Text: 20 passages (seed 1), three chapter openings (grade 2 ch. 4, grade 5 ch. 1, grade 8 ch. 5), the sweep, number
  and PDF-sweep reports.
- Numbers: every NUMDIFF line traced. All are numbers written as words in Chinese (*Grade 6* → 六年级, *week 2* → 第二周,
  *Way 1* → 方法一) or a formula moved to the neighbouring line; none lost.
- Figures: a script compared every text box in all 168 figure clusters for overlaps (0 label collisions; its hits were
  prose fractions), then the figures on the 40 pages of `sample.py --pages 400` were read on contact sheets.

## Defects found and fixed, by class

| Class | Count | Example | Fix |
|---|---:|---|---|
| Title left in English | 12 | `\section*{Chapter \ref{…} --- Fractions}` | `repair.py`; 3 by hand; a title rule in `langs/zh.py` |
| A line absorbing the next English line | 4 | `…350 克。` then `the apples' side.` | by hand |
| `;` → `；` after a node's `}` in a picture | 23 files | `{苹果};` | restored; `convert()` no longer converts after `}` |
| ASCII brackets inside a Chinese `\text{}` | 5 files | `\text{(同号)}` | → （）|
| English month/day/sport names on symbolic axes | 3 | `symbolic x coords={Jan,…}` | `xticklabels={1月,…}`, keys kept |
| English spaced em dash in Chinese prose | 745 | `相等 --- 这里` | → `——` (sweep) |
| Space between Chinese and `\emph`/`\omterm` | 25 | `就 \emph{退位}` | sweep |
| A definition's index key changed with its `\emph` | 1 | `\emph{整除}\index{整除}` (English: `\index{divisor}`) | `\index{因数}`, restoring the link sense |
| Over-linking of everyday shape words | ~300 links | 正方形, 三角形, 长方形, 直线 | `DROP`, as English does |
| Overfull: long number list in inline math | 1 | divisors of 48 and 60 | `\allowbreak` after two commas |
| Stray English in prose | 2 | *Elements*, *Part I* | 《几何原本》, 第 I 部分 |

## Known limits of this edition

- One-character terms are never linked (`CJK_MIN_CHARS = 2`): 和 *sum*, 积 *product*, 差 *difference*, 零 *zero*, 商, 圆,
  角. English links *sum* 51 times in grade 7 alone. 和 is also "and", so a link would be wrong more often than right.
- Some notions link to a different year's definition than English (nearest-preceding policy on a Chinese word that
  covers two English words, e.g. 整除 for *divides* and *divisible*).
