"""Book 1 -- Simplified Chinese. Curation only; the rules live in tools/termlink/.

Written 2026-11-16 for the pilot run (sources/TRANSLATION_BOOKS_1-5_ZH.md) before the translation existed, from the
English config's choices and the Chinese homographs the glossary creates; refined at the book's close against the link
census. Chinese is matched in CJK mode (lang_zh.py): no word boundary inside Han text, so a word that is also part of a
common compound or an everyday verb must be stopped or dropped here. One-character terms are never linked.
"""

# result names are never terms (the English NOT_A_TERM, in Chinese)
NOT_A_TERM = ("定理", "引理", "推论", "不等式", "公式", "法则", "判别法", "准则", "恒等式", "现象")

STOP = {
    "展开",      # "expanding" is grade 8's; the word is ordinary elsewhere (展开图 is its own term)
    "零",
    "质量",      # mass; also "quality"
    "对称",      # the adjective; 对称轴 and 对称中心 are their own terms
}

DROP = {
    "中线", "重心",  # the g8 midpoint problem's words, which English never links (2-character floor, Book 3 close)
    "方程",      # inside 方程组 and 微分方程, which Book 1 does not define
    # the furniture, as in book1_en.py: square, triangle, rectangle and line are on nearly every geometry line (the first
    # census linked def:g3:shapes:shapes 117 times in grade 7 against 19 in English); the compounds keep the link
    # (直角三角形, 等腰三角形, 平行四边形, 垂直平分线).
    "正方形", "三角形", "长方形", "直线",
}
# Not linkable in Chinese: 和 (sum), 积 (product), 差 (difference), 零 (zero), 商, 圆, 角 are one character, and 和 is also
# "and". English links "sum" 51 times in grade 7 alone; the Chinese edition does not (CJK_MIN_CHARS, lang_zh.py).

EXTRA = {}          # manual {term: label}, added at the book's close
NO_CAPITAL = set()
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 20

EXTRA_PROTECT = [
    r'直角边',                               # the legs of a right triangle, not the right angle
    r'平方(?=厘米|分米|毫米|千米|米|公里)',   # a unit (square centimetre), not the square of a number
    r'立方(?=厘米|分米|毫米|千米|米)',
]
