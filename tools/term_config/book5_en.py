"""Book 5 (University Year 3) -- FROZEN.

These are the constants the 4325 links in parts/bachelor-3 were generated with.
tools/check_book5_golden.sh regenerates the book and requires the result to be
byte-identical, so treat this file as a fixture: change it only deliberately,
and expect the golden test to fail until you re-bless the output.
"""

# single words that are ordinary English, or whose sense changes by chapter.
# (Their disambiguated phrases -- "compact operator", "closed form" -- survive,
# because those come from the \index entries.)
STOP = {"at", "all", "some", "total", "shape", "section", "direct", "simple",
        "stable", "equivalent", "integer", "index", "law", "generated",
        "converges", "events", "over $A$", "a.e.", "dense", "normal",
        "maximal", "principal", "radical", "content", "characteristic",
        "invariant", "bounded", "action", "basis", "degree", "free",
        "Euclidean", "separable", "closed", "exact", "compact", "prime",
        "irreducible", "primitive", "product", "quotient", "subspace",
        "path", "boundary", "interior"}

# a result is not a term: "Baire's theorem" must not become a link
NOT_A_TERM = ("theorem", "lemma", "inequality", "formula", "criterion",
              "principle", "identity", "rule", "law of", "paradox", "problem")

DERIVED = {
    "continuous": ["continuity", "continuously"], "measurable": ["measurability"],
    "integrable": ["integrability"], "holomorphic": ["holomorphy", "holomorphically"],
    "complete": ["completeness"], "connected": ["connectedness"],
    "equicontinuous": ["equicontinuity"], "orientable": ["orientability"],
    "solvable": ["solvability"], "self-adjoint": ["self-adjointness"],
    "homeomorphism": ["homeomorphic"], "isomorphism": ["isomorphic"],
    "algebraic": ["algebraically"], "topology": ["topological"],
    "transitive": ["transitively"], "faithful": ["faithfully"],
    "meromorphic": ["meromorphically"], "conformal map": ["conformally"],
}

# overloaded words whose first sense dominates the book, so they may be linked
# outside the chapter that pins them down
PRIMARY_OK = {"compact", "closed", "path", "boundary", "interior", "irreducible"}

AMBIG_POLICY = "drop"      # a term defined twice, with no phrase to tell the
                           # senses apart, is not linked at all
EXTRA = {}                 # manual {term: label}; overrides every rule above
DROP = set()               # harvested terms to force out
NO_CAPITAL = set()         # linked mid-sentence but not sentence-initially
MAX_TERM_WORDS = None
MAX_TERM_CHARS = None
EXTRA_PROTECT = []
