"""Book 5 -- Simplified Chinese. Curation only; the rules live in tools/termlink/.

Written 2026-11-16 for the pilot run (sources/TRANSLATION_BOOKS_1-5_ZH.md) before the translation existed, from the
English config's choices and the Chinese homographs the glossary creates; refined at the book's close against the link
census. Chinese is matched in CJK mode (lang_zh.py): no word boundary inside Han text, so a word that is also part of a
common compound or an everyday verb must be stopped or dropped here. One-character terms are never linked.
"""

# result names are never terms (the English NOT_A_TERM, in Chinese)
NOT_A_TERM = ("定理", "引理", "推论", "不等式", "公式", "法则", "判别法", "准则", "恒等式", "现象")

STOP = {
    "中心",      # the centre of a group; also "centred at"
    "指数",      # the index of a subgroup; also exponent / exponential
    "稳定", "可解", "完备", "密度",
}

DROP = {
    "表示",      # representation; the everyday verb "denotes"
    "作用",      # action; the everyday "effect, acts"
    "分布",      # law (English 29 links); inside every 正态/均匀/泊松分布, 分布函数, 依分布收敛: 203 links
    "几乎处处",  # linked to the L1 definition 115 times against English 2
    "最大公因数",  # reaches the Bezout lemma; English never links gcd
}

EXTRA = {          # index-only or title-only terms (no \emph in Chinese), added at the book's close (census)
    "类方程": "cor:b3:groups:classeq",
    "伽马函数": "ex:b3:lebesgue:gamma",
    "拓扑学家的正弦曲线": "ex:b3:topology:sinecurve",
    "极坐标": "ex:b3:product:polar",
    "单位分解": "lem:b3:forms:partition",
    "正交多项式": "pb:b3:hilbert:1",
    "诺伊曼级数": "prop:b3:banach:neumann",
    "调和函数": "prop:b3:conformal:harmonicholo",
    "完全域": "prop:b3:galois:perfect",
    "柯西–黎曼方程": "prop:b3:holomorphic:cauchyriemann",
    "柯西--黎曼方程": "prop:b3:holomorphic:cauchyriemann",
    "伽罗瓦对应": "thm:b3:galois:fundamental",
    "塔律": "thm:b3:galois:tower",
    "交错群": "thm:b3:groups:ansimple",
    "恒等定理": "thm:b3:holomorphic:identity",
    "若尔当标准形": "thm:b3:modules:jordan",
    "李雅普诺夫函数": "thm:b3:ode:lyapunov",
    "矩阵指数": "thm:b3:ode:matrixexp",
    "极大解": "thm:b3:ode:maximal",
    "0--1 律": "thm:b3:probability:zeroone",
    "乘积测度": "thm:b3:product:existence",
    "洛朗级数": "thm:b3:residues:laurent",
    "洛朗展开": "thm:b3:residues:laurent",
    "卡索拉蒂--魏尔斯特拉斯": "thm:b3:residues:riemanncw",
    "卡索拉蒂–魏尔斯特拉斯": "thm:b3:residues:riemanncw",
    "弗雷德霍姆择一定理": "thm:b3:spectral:fredholm",
    "弗雷德霍姆择一性": "thm:b3:spectral:fredholm",
    "拉格朗日乘子": "thm:b3:submanifolds:lagrange",
    "序列紧性": "thm:b3:topology:metriccompact",
}
NO_CAPITAL = set()
DERIVED = {}
PRIMARY_OK = set()
AMBIG_POLICY = "drop"
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 20

EXTRA_PROTECT = [
    r'表示为', r'表示成', r'记作',
]
