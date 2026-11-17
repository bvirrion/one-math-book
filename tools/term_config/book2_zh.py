"""Book 2 -- Simplified Chinese. Curation only; the rules live in tools/termlink/.

Written 2026-11-16 for the pilot run (sources/TRANSLATION_BOOKS_1-5_ZH.md) before the translation existed, from the
English config's choices and the Chinese homographs the glossary creates; refined at the book's close against the link
census. Chinese is matched in CJK mode (lang_zh.py): no word boundary inside Han text, so a word that is also part of a
common compound or an everyday verb must be stopped or dropped here. One-character terms are never linked.
"""

# result names are never terms (the English NOT_A_TERM, in Chinese)
NOT_A_TERM = ("定理", "引理", "推论", "不等式", "公式", "法则", "判别法", "准则", "恒等式", "现象")

STOP = {
    "坐标",      # inside 坐标系 and 坐标轴, which carry their own sense
    "组合",      # as English "combination": ordinary outside the combinatorics chapter (线性组合, 组合起来)
}
# 图像 (graph of a function), 近似值 and 二分法 were stopped before the translation existed; the census showed them
# unambiguous in Chinese (图 is the graph of graph theory), so they link as in English.

DROP = {
    "根",        # inside 平方根, 根号, 特征根: English links "root" to the discriminant, Chinese cannot
    "夹逼定理",  # a result's name, as English drops "(Squeeze theorem)"
}

EXTRA = {}          # manual {term: label}, added at the book's close
NO_CAPITAL = set()
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 20

EXTRA_PROTECT = [
    r'平方(?=厘米|分米|毫米|千米|米)',
]
