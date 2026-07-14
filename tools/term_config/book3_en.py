"""Book 3 -- English. Curation only; the rules live in tools/termlink/.

Every key is optional: anything left out falls back to the defaults in
tools/link_defined_terms.py.

The judgement follows Book 5's: a word earns a link only when *every* use of it
in the book is the notion the definition pins down. Ordinary English in this
register ("a similar argument", "for free"), names of results ("Legendre's
formula"), and words whose sense moves from chapter to chapter are left alone.
"""

# Words whose sense is only safe inside the chapter that pins it down (STOP
# keeps a term chapter-local rather than book-wide).
STOP = {
    "finite",                   # "finite sum/family/union" is not the finite *set* of ch. 2
    "conjugate",                # ch. 3 complex conjugate vs "multiply by the conjugate"
                                # (ch. 11) vs conjugating a matrix (ch. 21)
    "characteristic polynomial",  # ch. 5 defines it for a linear ODE; ch. 22 uses it
                                  # for a matrix (a different object)
}

# Never linked anywhere.
DROP = {
    # --- ordinary English / verbs in this register ---
    "argument",         # "the same argument shows" -- not the argument of a complex number
    "symmetry",         # "by symmetry" -- not the linear-map symmetry of ch. 20
    "similar",          # "a similar computation" -- keep only "similar matrices"
    "direct",           # "a direct computation" -- keep only "direct sum"
    "critical",         # bare adjective; "critical point" survives
    "beats",            # verb ("the factorial beats the geometric term")
    "algebraic", "algebraically",   # "algebraic structure/trick/manipulation"
    "transcendental",   # bare adjective, and mis-targeted (see below)

    # --- names of results: the point is to link definitions, not theorems.
    # (NOT_A_TERM only filters index-only harvests; these came in through
    # \emph{...}\index{...} and have to be dropped by hand.)
    "Kummer's theorem", "Legendre's formula", "De Morgan's laws",
    "Ptolemy's inequality", "Cauchy's functional equation", "functional equation",
    "alternating series estimate",
}
# The notions a weekend problem introduces (the Cantor set, the tower law, the
# normal equations, ...) are NOT dropped: since `pb:` became a statement prefix
# they attach to the problem that introduces them, which is the honest target.

# Terms the harvester misses.
EXTRA = {
    # the definition emphasises a compound ("\emph{continuous at $x_0 \in I$}",
    # "\emph{differentiable at $x_0 \in I$}"), so the bare adjective -- the form
    # the rest of the book actually uses -- is never seen
    "continuous":     "def:b1:continuity:continuous",
    "continuously":   "def:b1:continuity:continuous",
    "differentiable": "def:b1:derivative:def",
    # \index{Euler's constant} sits in exercise 12, *before* the weekend problem
    # that defines gamma, so the nearest preceding statement is an unrelated
    # example about telescoping. Point it at the problem.
    "Euler's constant": "pb:b1:series:1",
}

# Linked mid-sentence, never sentence-initially: each is also an imperative
# ("Set $u = f(0)$.", "Map $P$ to its coefficients.", "Group the non-real roots
# in conjugate pairs.").
NO_CAPITAL = {"set", "map", "group"}

DERIVED = {}

# An overloaded word may not be linked outside the chapter that pins it: "order",
# "kernel" and "rank" are each defined twice, and no first sense dominates.
PRIMARY_OK = set()

AMBIG_POLICY = "drop"

# Fixed English idioms that contain a linkable word in a different sense.
EXTRA_PROTECT = [
    r'closed[- ]form(?:ula)?s?',   # "no closed form" -- not a closed set
    r'\bclosed by\b', r'\bclosed the\b',   # verb
    r'\bopen towards?\b',                  # "a parabola open towards $x > 0$"
    r'\bfor free\b',                       # "we get the converse for free"
    r'\blinear algebra\b', r'\blinear combinations?\b',
    r'\blinear expressions?\b',
    # "linear recurrence" is not protected: it is a term of its own (the ch. 21
    # weekend problem), and longest-first makes it beat the bare "linear".
    # The verb "set", mid-sentence, introducing an assignment: "and set $x = 1$",
    # "$\varepsilon$; set $\delta = \min(\delta_0, 1)$". The noun always carries a
    # determiner ("the set $A = \{\dots\}$", "a level set $\{f = c\}$"), which is
    # what tells the two apart -- so only a trigger token before "set" protects.
    # NB the trailing "$" is a lookahead, never consumed: a protect pattern that
    # eats the opening $ of a formula inverts inline-math masking for the rest of
    # the file (it cost 1100 links before this was caught).
    # (the assignment may be inline math or a display, and "we set" may straddle
    # a line break)
    r'(?:\band|\bwe|\bthen|\bnow|\bHint:|[;,:.]|\n)\s*set(?=\s*(?:\$|\\\[))',
    r'(?<=\$)\s*set(?=\s*(?:\$|\\\[))',
    r'\bwe\s+set\b',
]
