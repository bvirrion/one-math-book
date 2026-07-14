"""Book 2 -- en. Curation only; the rules live in tools/termlink/.

Every key is optional: anything left out falls back to the defaults in
tools/link_defined_terms.py (empty sets, AMBIG_POLICY "drop").
"""

# Ordinary language in this register, or a word whose sense in the book is not
# the sense the definition gives it.
STOP = {
    # parity of an integer -- and "even though", "not even defined". The
    # harvested sense is the parity of a *function* (def:g11:func:parity), so
    # "even" and "odd" would point at the wrong notion nearly everywhere.
    # "even function" / "odd function" survive as phrases.
    "even", "odd",
    # harvested from the sum of two *vectors* (def:g10:vectors:sum); the word is
    # used for the sum of numbers, of a series, of the roots... everywhere.
    "sum",
    # "arithmetic sequence" and "geometric sequence" are kept; the bare
    # adjectives mean number theory ("the arithmetic chapter") and geometry
    # ("a geometric interpretation").
    "arithmetic", "geometric",
    # ordinary emphasis inside definitions, harvested as leaf-matching terms
    "all", "strictly", "simultaneously",
    # outside the combinatorics chapter every use is a *linear* / *integer*
    # combination (Bezout, coplanar vectors) -- not "k elements chosen from n"
    "combination",
    # "the region bounded by the curve", "bounded intervals": the participle,
    # not a bounded sequence. "bounded above" / "bounded below" survive.
    "bounded",
    # the statistical range (max - min); elsewhere "range" is the set of values
    # a function takes ("$\\cos$ has range $[-1,1]$")
    "range",
}
# NB a STOPped word is still linked inside the chapter that defines it (the
# shared rule keeps chapter-local senses), which is what we want: "even",
# "geometric", "bounded", "sum" are right there and wrong everywhere else.

NO_CAPITAL = set()    # no term of this book doubles as an imperative
                      # ("Expand", "Factor", "Solve", "Sketch" are not terms;
                      # the sentence-initial "Mean", "Median", "Range", "Tree"
                      # that do occur are the noun and should be linked)

EXTRA = {}            # manual {term: label}; overrides every rule

DROP = {
    "(Squeeze theorem)",   # a result, not a term (and the parenthesis is noise)
    "Expanding",           # duplicate of "expanding": [Ee] is handled by the rule
}

DERIVED = {}          # {base: [other forms]}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"   # a spiral curriculum re-defines its terms
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans no link may touch. (Headings are masked by the shared rule.)
EXTRA_PROTECT = [
    r'\bmeans\b',                  # the verb ("solving means finding..."), not
                                   # the plural of the statistical mean
    r'\bmean\s+equal\b',           # "equal ordinates mean equal points": the
                                   # bare verb, the one place it occurs
    r'\b[Ss]quare\s+roots?\b',     # not a root of a polynomial
    r'\b[Cc]ube\s+roots?\b',
]
