# Run file — One Math Book 1–5 in Simplified Chinese (`zh`), pilot method

Scope: Books 1–5 (15 years: grade-1 … grade-12, bachelor-1 … bachelor-3) into Simplified Chinese (mainland), by the
pilot method (`../pilot_translation_instruction.md`). Started 2026-11-16. First CJK edition in the project.

| **Model** | `claude-haiku-5-5` (Haiku 5.5, effort medium), pilot method: one headless call per section; glossary and coordinator `claude-opus-5-5` (Opus 5.5) |
|---|---|

Shape: one coordinator (the main session), no subagents, one session; Haiku at most three years at once (`--workers 3`).
**Pause rule for this run (user, 2026-11-16): pause and report when the weekly plan reaches 98 %** (in place of +7 points).

## Usage readings (`claude -p /usage`, all models, current week)

| When | Week used |
|---|---:|
| Run start, 2026-11-16 | 93 % |
| After step 0 (infrastructure, glossaries, trial chapter), Haiku queue started | 93 % |
| After Book 1 closed, 2026-11-17 01:30 (Book 2's years in the queue) | 94 % |
| After Book 2 closed, 2026-11-17 ~02:45 (Books 3–5 in the queue) | 96 % |
| 2026-11-17 08:53, Haiku queue still running | **98 %: run paused** (user rule) |
| Resumed after the user's reset, queue restarted for bachelor-1..3 | 0 % |
| After Book 3 closed, 2026-11-17 ~15:40 (bachelor-2 translated, bachelor-3 in the queue) | 6 % |
| After Book 4 closed, 2026-11-17 15:54 (bachelor-3 in its first pass, 41/46) | 6 % |
| After Book 5 closed, 2026-11-17 ~22:10 (run complete) | 8 % |

## Infrastructure (step 0, 2026-11-16)

- `tools/id_apply.py` ported from `one-physics-book` (+ `zh` prose-gate dispatch); `tools/check_orphan_lines.py` ported.
- Engine: XeLaTeX + xeCJK, Fandol fonts from TeX Live (Song regular/bold, Kai as italic so `\emph` terms show, Hei sans,
  Fang mono), by file name; `latexmkrc` sends `_zh` to XeLaTeX and its index to `upmendex` with `styles/zh-pinyin.ist`
  (pinyin collation, no sort keys in the sources).
- `styles/lang/zh.tex`; a `zh` block at the end of `styles/onemath.sty`: chapter head 第 N 章, part head 第一部分 (patching
  hyperref's `\H@old@part`), solution header 练习 3.2 的解答（第 N 页）, "解答见第 N 页" pointer, `\cref{ch:}` → 第 N 章,
  cleveref conjunctions 和/、/至, reference names in `\text{}` (a `\cref` inside math printed no Chinese).
- Running-header chapter prefix moved into `\om@chapmarkprefix` (same expansion for every other language).
- Term linker: opt-in `CJK` mode (`tools/term_config/lang_zh.py`, `termlink/morphology.py`): Latin/digit/macro boundaries
  only, one line break allowed inside a term, one-character terms never linked. Golden check green.
- Prose gate `tools/check_chinese_prose.py` (gate 9 of `check_translation.sh`): Latin words in visible text, legends,
  ASCII punctuation in Chinese prose. Lights up on English, silent on the Chinese preface.
- Pack `pilot_translation/langs/zh.{md,py}` (the `.py` unit pass converts ASCII punctuation after Chinese to full-width),
  series card `langs/series/one-math-book.zh.md`; `post.py`/`sample.py` know `zh`.
- Glossaries `sources/GLOSSARY_BOOK_{1..5}_ZH.md` (102/144/102/126/147 lines, chapter `00` = by occurrence).

Trial chapter (grade-6 ch. 04, 8 figures): 10 calls, $0.11, no rejection; probe 0/0/0, 0 missing characters, figures
clean. Statement heads changed for zh to 定义 4.1（基本对象） with no full stop (`\newtheoremstyle` in the zh block).
Haiku queue: `draft/zh-queue.sh` (log `draft/zh-queue.log`), years in book order, three at once, up to five passes each.
Sweeps for installed years: `tools/zh_sweeps.py <year> [--fix]` (in `draft/zh-sweeps.py` until the Book 4 close).

## Open defects (kept on disk, cleared as fixed)

- English canon, not fixed: the √(r²−d²) label of the grade-9 sphere-section figure overlaps the radical and the
  ellipse (every edition).

## Per-book log

### Book 1 (grades 1–9): closed 2026-11-17, 88 / 100 pilot tier

- 538 Haiku calls, about $4.0 list; one year (grade 7) needed a sixth pass: a line of `arc (…) -- cycle;` was read as
  English prose by `common.py`'s English check, now skipped as drawing code.
- 401 pp, 0/0/0, missing character 0; gates green for all nine years; 3,923 term links, `--check` clean.
- Score file `translation_scores/book_1/zh/translation_score.md` (defect table there).
- Tooling changes made on the way, all kept for Books 2–5:
  - `langs/zh.py`: no punctuation conversion after `}` (it broke 23 pictures' `};`), none on a line inside a split
    formula, conversion after `\cref{…}`; a refusal for a title left in English.
  - `zh_sweeps.py --fix`: `——` for ` --- `, no space around a Chinese `\emph`/`\omterm`; its census check ignores
    `\allowbreak`.
  - `check_chinese_prose.py`: function names (sin, cos, gcd…) allowed; `xticklabels`/`symbolic x coords` lists skipped.
  - `check_translation.sh`: the drafty-dots gate skips comments (all languages; fr grade-2 still passes).
  - `latexmkrc`: an empty `_zh.idx` no longer stops latexmk (upmendex exits non-zero on 0 entries).
  - `styles/lang/zh.tex`: a Chinese `\today`.
  - `book1_zh.py`: furniture words dropped as in English; 一半 unstopped; 直角边 protected.
- The step that costs most coordinator time is term-link calibration: Haiku makes `\index{}` equal to `\emph{}`, so a
  definition whose English index key names another word (`\emph{divides}\index{divisor}`) loses that sense; list them
  with the emph/index comparison and restore the ones that change a link.

### Book 2 (grades 10–12): closed 2026-11-17, 88 / 100 pilot tier

- 502 Haiku calls, about $5.3 list; grade 11 needed five passes.
- 307 pp, 0/0/0, missing character 0; gates green for the three years; 4,622 term links, `--check` clean.
- Score file `translation_scores/book_2/zh/translation_score.md` (defect table there).
- Tooling changes, kept for Books 3–5:
  - `termlink/harvest.py`: no space between two Chinese characters in a term key, so a term wrapped over two lines
    (`\emph{方向\n向量}`) is the same term as on one line. Golden check green; Book 1 links unchanged.
  - `zh_sweeps.py --fix`: a space before a table row's `\\` after a Chinese character (xeCJK + `tabular`: "Improper
    alphabetic constant"), run back over Book 1 too; the dash fix tracks a formula carried over from the line before;
    its census check ignores spaces inside math.
  - `check_chinese_prose.py`: roman numerals and six Latin words kept on purpose (BANANA, ISBN, Luhn, PageRank,
    TechCorp, sigmoid).
  - `book2_zh.py`: 图像, 近似值, 二分法 unstopped (unambiguous in Chinese); 组合 soft-stopped and 夹逼定理 dropped,
    as English does.
- At 96 % after this book, Book 3's close may reach the 98 % pause: usage is read mid-book from here on.

### Book 3 (University Year 1): closed 2026-11-17, 88 / 100 pilot tier

- 1,182 Haiku calls, about $17.3 list: the year ran across the pause and five passes, and still ended with 10 rejected
  sections (a `$` moved to the next line, `\operatorname{diam}` written `\text{直径}`, two formulas swapped by Chinese
  word order). Finished by hand from each last reply and saved through every check (`fixsec.py`, now
  `pilot_translation/fixsec.py`: dump the last reply, edit, save through every check), then a re-run rebuilt the files with no call. Bachelor-2 ended the
  same way (4 sections).
- 363 pp, 0/0/0, missing character 0; gate green; 3,954 term links to 101 targets (English 3,944 to 106).
- Score file `translation_scores/book_3/zh/translation_score.md` (defect table there).
- Tooling changes, kept for Books 4–5 and run back over Books 1–2:
  - **`termlink/harvest.py`: in CJK mode a term needs `CJK_MIN_CHARS` (2) characters, not 3.** The Latin floor had
    dropped every two-character term defined once (区间, 积分, 互质, 划分, 坐标) in the university books, whose
    `AMBIG_POLICY = drop` has no other path for them. Golden green. Books 1–2 relinked: 3,959 and 4,730 links (+36,
    +108); 中线/重心 dropped in Book 1, as English never links them.
  - Index-only terms (a name with no `\emph`, e.g. *tower law*, *Cantor set*) need a space in the key to be harvested,
    which no Chinese key has: `book3_zh.py` declares 37 of them in `EXTRA`, as French does.
  - **`langs/zh.py` masks `\index{…}`**: the punctuation pass had made `！` of a sub-entry `!` in 25 keys (Books 2–3),
    splitting the index; `zh_sweeps.py --fix` restores them.
  - `zh_sweeps.py --fix`: part numbers 第 III 部分 / Part III → 第三部分 (all books); its census check now compares with
    the Chinese before the fix, not with English (a translated `\emph` inside a display had blocked a whole file).
  - `common.py`: `\operatorname{lcm}(a,b) = ab` is a math line, not English ("a" twice); 3 false rejections.
  - `tools/id_apply.py`: `\index{…}` inside a display is blanked like `\text{…}` (a translated key there).
  - `check_chinese_prose.py`: `\index` keys (also run-on ones) and `\text{ (` skipped; RURRURU, orange, diag allowed.
- Books 1–2 rebuilt after these changes: 401 and 307 pp, 0/0/0.

### Book 4 (University Year 2): closed 2026-11-17, 88 / 100 pilot tier

- 1,125 Haiku calls, about $17.1 list; five passes, then 4 sections finished by hand as in Book 3.
- 365 pp, 0/0/0, missing character 0; gate green; 3,218 term links to 88 targets (English 3,511 to 85).
- Score file `translation_scores/book_4/zh/translation_score.md` (defect table there).
- Haiku kept 113 mathematicians' names in Latin script (Book 3 about 25): converted with one name map over the year's
  prose (outside math, labels and refs), index keys included. Worth giving the model the name list up front: the
  series card names only the famous ones (欧拉, 柯西, 黎曼, 高斯).
- `book4_zh.py`: 收敛, 交错, 代数 dropped (substrings of other terms in Chinese); 11 index-only terms in `EXTRA`.
- `tools/id_apply.py`: `\index{…}` inside a display is blanked like `\text{…}`.
- `zh_sweeps.py --fix`: also `Part III` / `（Part I 与 Part III）` left by the model → 第三部分.

### Book 5 (University Year 3): closed 2026-11-17, 88 / 100 pilot tier

- 1,835 Haiku calls, about $33.0 list: the costliest year. Five passes with 3 workers left 108 then ~60 sections
  rejected; at 18:09 the user agreed to run it alone with `--workers 9` (the same nine calls in flight as three years at
  3 workers): about 230 calls an hour against 90. After four more passes, 24 sections were still rejected.
- The 24 were all "ordered math-span sequence differs". Two scripted rules fixed 12 of them with no other edit: a
  formula split over two lines in English that Haiku reopened with a `$` on the next line, and a `$x` left unclosed at a
  line end where English closes it. The other 12 were finished by hand (formulas swapped by Chinese word order, an extra
  or missing variable, `\index{西罗 $p$-子群}` adding math). Scripts: scratch `leaddollar.py`, `taildollar.py`, since built into the reply check (`repair_dollars` in
  `pilot_translation/common.py`, 2026-11-18).
- 361 pp, 0/0/0, missing character 0; gate green; 3,008 term links to 125 targets (English 4,326 to 130).
- Score file `translation_scores/book_5/zh/translation_score.md` (defect table there).
- 140 Latin names converted (one name map, then 4 by hand); the map now covers about 90 mathematicians.
- `tools/zh_sweeps.py`: the dash rule left alone every line that opens a formula running onto the next; it now treats
  the open tail as math. 76 such lines were also fixed in Books 3–4 (both rebuilt and re-gated).
- `tools/check_chinese_prose.py`: *delta*, *limsup*, *liminf* allowed (math names leaked by split formulas). *theta* and
  *zeta* were tried and withdrawn: they hid three real "theta 函数" / "zeta 值" in prose. The gate's line numbers can
  point at the wrong line, so read the whole file for the word before allowing it.
- `book5_zh.py`: 分布, 几乎处处, 最大公因数 dropped; 定向 restored; 29 `EXTRA` keys.

## Run complete, 2026-11-17

All five books closed at 88 / 100 pilot tier: 401 / 307 / 363 / 365 / 361 pp, all 0/0/0 with missing character 0,
gates green, term links checked. Haiku in all: 538 + 502 + 1,182 + 1,125 + 1,835 = 5,182 calls, about $77 list price.
Weekly plan: 93 % → 98 % (pause) for step 0 and Books 1–2; 0 % → 8 % after the user's reset for Books 3–5. Nothing
committed.

## PAUSED 2026-11-17 08:53 at 98 % of the weekly plan (user rule for this run)

The background queue (`draft/zh-queue.sh`) was stopped at 98 %. Books 1 and 2 are closed. Translated files on disk:

| Year | Files written | Of |
|---|---:|---:|
| bachelor-1 (Book 3) | 34 | 50 |
| bachelor-2 (Book 4) | 27 | 46 |
| bachelor-3 (Book 5) | 14 | 46 |

**To resume** (after the weekly reset, Nov 20 19:00 Amsterdam): `run.py` skips files already written, so restart the queue
for the three bachelor years only (`draft/zh-queue.sh` with grades removed, or `run.py --repo ../one-math-book --year
bachelor-N --lang zh --workers 3 --book-desc "university (bachelor) mathematics"` per year, at most three at once), then
close Books 3, 4, 5 one at a time as Books 1–2 were: `post.py --units`, `repair.py`, `post.py`, NUMDIFF, `sites.py`,
`install.py`, `tools/zh_sweeps.py <year> --fix`, term links (`book{3,4,5}_zh.py` to calibrate against `census.py`; check
the emph/index pairs whose English index key names another word), gates, build, `pdfsweep.py`, figures, sample, score.
Still to do at the very end: CLAUDE.md files, README language lists, lessons into `pilot_translation_instruction.md` and
`translation_instruction.md`, a rebuild of one fr and one hi book to confirm the style changes leave them unchanged, and
the golden check.

## Regression check of the other editions (after the resume)

- `one_math_book_1_primary_middle_school_hi`, rebuilt with the zh changes (TeX Live 2026, scratch): 416 pp, 0/0/0, as
  shipped.
- `one_math_book_3_university_year_1_fr`, rebuilt with the zh changes and from a clean HEAD worktree: both 414 pp,
  2 overfull, `pdftotext` output identical. The style changes leave French untouched. The 2 overfull boxes and the
  one-page difference from the shipped PDF (415 pp, built 2026-08-14) predate this run: an open item for French
  Book 3, not for this run.
