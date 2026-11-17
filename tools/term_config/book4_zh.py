"""Book 4 -- Simplified Chinese. Curation only; the rules live in tools/termlink/.

Written 2026-11-16 for the pilot run (sources/TRANSLATION_BOOKS_1-5_ZH.md) before the translation existed, from the
English config's choices and the Chinese homographs the glossary creates; refined at the book's close against the link
census. Chinese is matched in CJK mode (lang_zh.py): no word boundary inside Han text, so a word that is also part of a
common compound or an everyday verb must be stopped or dropped here. One-character terms are never linked.
"""

# result names are never terms (the English NOT_A_TERM, in Chinese)
NOT_A_TERM = ("定理", "引理", "推论", "不等式", "公式", "法则", "判别法", "准则", "恒等式", "现象")

STOP = {
    "等价",      # asymptotic equivalence and equivalent norms; ordinary "equivalent statements"
    "对偶空间",
}

DROP = {
    # wrong sense in Chinese (Book 4 close): 收敛 is any convergence, not the improper integral's (224 links against
    # English 20); 交错 sits in 交错级数; 代数 in 线性代数 and 代数重数. Problem results named only in Chinese.
    "收敛", "交错", "代数", "科罗夫金定理", "外尔扰动不等式", "柯朗–费希尔极小极大定理",
    "弧长",
    "符号",      # the signature of a permutation; also any "symbol"
}

# English reaches these through index-only keys, which the harvest takes only with a space (none in Chinese).
EXTRA = {
    "共振": "pb:b2:diffeq:1",
    "母函数": "ex:b2:powerseries:fibonacci",
    "阿贝尔求和": "thm:b2:series:abel", "阿贝尔分部求和": "thm:b2:series:abel",
    "高斯化简": "thm:b2:quadratic:gauss",
    "含参积分": "thm:b2:integration:continuity",
    "沃利斯积分": "pb:b2:multint:1",
    "狄利克雷核": "lem:b2:fourier:kernel",
    "邓福德分解": "thm:b2:reduction:dunford",
    "卡塔兰数": "ex:b2:powerseries:catalan",
    "分支过程": "pb:b2:genfun:1",
    "范数等价": "thm:b2:nvs:finitedim",
}
NO_CAPITAL = set()
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "drop"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 20

EXTRA_PROTECT = [
    r'线性代数', r'线性组合',
]
