"""Book 3 -- Simplified Chinese. Curation only; the rules live in tools/termlink/.

Written 2026-11-16 for the pilot run (sources/TRANSLATION_BOOKS_1-5_ZH.md) before the translation existed, from the
English config's choices and the Chinese homographs the glossary creates; refined at the book's close against the link
census. Chinese is matched in CJK mode (lang_zh.py): no word boundary inside Han text, so a word that is also part of a
common compound or an everyday verb must be stopped or dropped here. One-character terms are never linked.
"""

# result names are never terms (the English NOT_A_TERM, in Chinese)
NOT_A_TERM = ("定理", "引理", "推论", "不等式", "公式", "法则", "判别法", "准则", "恒等式", "现象")

STOP = {
    "共轭复数", "特征多项式", "有限集",
}

DROP = {
    "命题",      # "statement" -- and the name of every numbered proposition
    "对称",      # "by symmetry" -- not the linear-map symmetry
    "相似",      # "a similar computation"
    "直和",
    "拍",
    # English links none of these: "law" of composition is stoplisted there, the argument of a complex number is
    # ambiguous, and the two problem results are names (NOT_A_TERM), harvested here through their \emph.
    "运算", "辐角", "勒让德公式", "库默尔定理",
}

# English links these through index-only keys; the index-only harvest needs a space in the key, which no Chinese key
# has, so they are declared here (as French does for its own gaps). Calibrated against census.py, 2026-11-17.
EXTRA = {
    "超越数": "pb:b1:logic:1", "代数数": "pb:b1:logic:1",
    "正规方程": "pb:b1:multivar:1", "回归直线": "pb:b1:multivar:1", "最小二乘": "pb:b1:multivar:1",
    "滑移反射": "pb:b1:euclid:1", "二面体群": "pb:b1:euclid:1",
    "塔律": "pb:b1:findim:1",
    "欧几里得算法": "met:b1:arith:euclid",
    "希尔伯特矩阵": "pb:b1:det:1", "柯西行列式": "pb:b1:det:1",
    "线性递推": "pb:b1:matrices:1", "斐波那契数": "pb:b1:matrices:1",
    "康托尔集": "pb:b1:topology:1",
    "欧拉常数": "pb:b1:series:1",
    "差商": "pb:b1:vspaces:1", "整值多项式": "pb:b1:vspaces:1",
    "品质因数": "pb:b1:diffeq:1",
    "等比级数": "ex:b1:series:geometric",
    "范德蒙德行列式": "ex:b1:det:vandermonde",
    "高斯消元": "met:b1:det:gauss",
    "过渡矩阵": "def:b1:matrices:changeofbasis", "基变换": "def:b1:matrices:changeofbasis",
    # named results English reaches through index-only keys
    "分部积分": "thm:b1:integration:parts", "黎曼和": "thm:b1:integration:riemann",
    "增长比较": "prop:b1:functions:powerrules", "阿基米德性质": "thm:b1:reals:archimedes",
    "相邻数列": "thm:b1:seq:adjacent", "交错级数": "thm:b1:series:alternating", "比值判别法": "thm:b1:series:ratio",
    "黎曼级数": "thm:b1:series:riemann", "拉格朗日插值": "thm:b1:poly:lagrange", "余子式展开": "thm:b1:det:cofactor",
    "切比雪夫多项式": "pb:b1:poly:1", "交错群": "pb:b1:structures:1", "小数展开": "pb:b1:reals:1",
    "海伦方法": "ex:b1:seq:heron",
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
