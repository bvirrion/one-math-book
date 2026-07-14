"""Book 1 -- en. Curation only; the rules live in tools/termlink/.

Every key is optional: anything left out falls back to the defaults in
tools/link_defined_terms.py (empty sets, AMBIG_POLICY "drop").

The register is the whole point here. In a book for six- to fifteen-year-olds
most of the vocabulary of the definitions is also ordinary English -- a box of
pencils, the edge of a ruler, one step per line -- so a word earns a link only
when it means, in nearly every one of its uses in this book, the thing its
definition defines. The few good words with a handful of bad uses are kept and
their bad uses masked (EXTRA_PROTECT) rather than thrown away.
"""

# Never linked: in this book these words are ordinary language far more often
# than they are the defined term.
STOP = {
    # "the number line", "one operation per line", "the three angles line up",
    # "a vertical grid line" -- the geometric line (def:g6:lines:objects) is a
    # minority of the uses, and the number line is a different object.
    "line",
    # "count the factors", "count the steps", "each wrong answer counts -3":
    # the verb, everywhere. The statistical count survives as "frequency".
    "count",
    # geometry owns this word: "the side opposite the right angle", "opposite
    # sides are parallel". The opposite of a relative number (def:g7:negatives)
    # is a small minority; the plural "opposites", which is only ever the
    # relative-number sense, is kept.
    "opposite",
    # def:g4:numbers:classes is the group of three digits; but grade 7 groups
    # data into (statistical) classes and grade 8 averages two school classes.
    "classes",
    # "lay one edge of the set square along d", "the middle of one edge" of a
    # triangle: the edge of a solid (def:g5:solids:def) loses on volume. Still
    # indexed in the source, so it reaches the printed index.
    "edge", "edges",

    # ---- the furniture ----------------------------------------------------
    # These five are real definitions (a child meets them in Grade 1-6) but by
    # the time they are used they are the everyday furniture of the page: they
    # occur in nearly every sentence of every geometry chapter (square 304,
    # triangle 212, angle 181, rectangle 168, circle 95 uses), and linking each
    # one turned the Grade 7 "Triangles and Angles" exercises solid blue. The
    # compounds that a child really can forget survive, and carry the link:
    # "right angle", "right triangle", "isosceles triangle", "equilateral
    # triangle", "alternate angles", "vertically opposite angles", "square
    # root", "axis of symmetry".
    "square", "triangle", "rectangle", "circle", "angle",
}

# Linked mid-sentence, not sentence-initially: "Round $8.276$ to the unit" is an
# instruction, not a use of the noun.
NO_CAPITAL = {"round"}

EXTRA = {}            # manual {term: label}; overrides every rule


# STOP is deliberately *soft*: a stoplisted word is kept out of the global
# vocabulary but still links inside the chapter that defines it. For most of the
# words above that is not wanted either, so they are hard-dropped as well. These
# are the exceptions -- words that are ordinary language everywhere in the book
# *except* in their own chapter, where every single use is the term:
SOFT = {
    "edge", "edges",   # parts/grade-5/07: "12 edges", "faces + vertices = edges + 2"
    "classes",         # parts/grade-4/01: the groups of three digits, all six uses
}

DROP = (set(STOP) - SOFT) | {
    # \emph{value of a digit depends on its place}\index{place value} in
    # parts/grade-6/01: the sentence is not a term (the term is "place value").
    "value of a digit depends on its place",
}

DERIVED = {}          # {base: [other forms]}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"   # a spiral curriculum re-defines its terms
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans no link may enter: the uses where a good term means something else.
EXTRA_PROTECT = [
    # NB: every space here is \s+ -- the sources wrap at 72 columns, and a
    # phrase split across two lines ("mètres\ncubes") slips past a literal space
    # and the link lands anyway.
    # "square"
    r'set\s+squares?',                     # the drawing tool
    r'hundred-squares?',                   # the 100-cell grid
    r'squares?\s+(?:centi|milli|kilo)?met(?:re|er)s?',   # units of area
    r'squares?\s+units?',
    r'squares?\s+of\s+the',                # squaring: "the square of the hypotenuse"
    r'square\s+of\s+a\s+relative\s+number',
    r'square\s+of\s+\$n\$',
    # "box": a box of pencils, 6 boxes of 100 pencils, a box of 12 balls.
    # The solid is nearly always singular ("a box $10$ cm long").
    r'\bboxes\b', r'[Bb]ox\s+contains',
    # "mean": the verb
    r'\bmeans\b',
    # "even": the adverb
    r'even\s+though', r'even\s+when', r'even\s+once', r'even\s+a\s',
    r'even\s+end\s+to\s+end', r'[Ee]ven\s+better',
    r'out\s+even',                         # "the division comes out even"
    # "half": the clock idiom
    r'[Hh]alf\s+past',
    # "round": the adjective, and a round of sharing
    r'perfectly\s+round', r'round\s+table', r'th\s+round',
    # "sum": the verb ("the three angles sum to $180^\circ$")
    r'[Ss]ums?\s+to\s',
    # "scale": the verb, and the pair of pans -- not the scale of a map
    r'[Ss]cales?\s+by\s+\$', r'balanced\s+scale',
    # "difference": the first place two numbers differ
    r'first\s+difference',
    # prose cross-references to the other books of the series
    r'High\s+School\s+volume',
]
