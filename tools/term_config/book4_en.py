"""Book 4 (University Year 2) -- English. Curation only; the rules live in
tools/termlink/.

Every key is optional: anything left out falls back to the defaults in
tools/link_defined_terms.py.
"""

# Single words that are ordinary English in this register, or whose sense
# changes from one chapter to the next. Their disambiguated phrases -- "exact
# form", "closed form", "alternating form", "signature of a quadratic form" --
# survive, because those come from the \index entries.
STOP = {
    # ordinary English far more often than the defined notion
    "order",          # "in order to", "order of summation", "second-order ODE"
    "equivalent",     # "the three conditions are equivalent" (only norms are defined)
    "algebra",        # "linear algebra", "the algebra is mechanical" >> $K$-algebra
    "converges",      # defined for improper integrals (ch. 9); every series use would land there
    # sense changes by chapter
    "alternating",    # alternating form (ch. 2) vs alternating series (ch. 7, 11)
    "signature",      # of a permutation (ch. 1) vs of a quadratic form (ch. 12)
    "exact",          # exact form (ch. 20) vs "the exact value/rate/exponent" (ch. 21-23)
    "regular",        # regular point/arc (ch. 18) vs regular surface (ch. 19)
    "equivalence",    # "equivalence relation/class" (ch. 1) vs equivalence of norms (ch. 5)
}

# Linked mid-sentence but never sentence-initially: guards the imperative
# ("Complete the square", "Complete \cref{...}") in exercises and solutions.
NO_CAPITAL = {"complete"}

# Regular derivations the morphology rules do not generate on their own.
DERIVED = {
    "continuous": ["continuity", "continuously"],
    "complete": ["completeness"],
    "compact": ["compactness"],
    "connected": ["connectedness"],
}

# Manual {term: label}; overrides every rule above. The bare word "symmetric"
# links to the symmetric endomorphism of ch. 12; the phrase names the bilinear
# form of the same chapter, defined a page earlier.
EXTRA = {"symmetric bilinear form": "def:b2:quadratic:def"}

# The terms a weekend problem introduces now attach to the problem itself
# (pb: is a statement prefix in the harvester), so they are kept -- the reader
# jumps from "the astroid" to the problem that builds it. What is dropped here
# is what is a *result*, not a notion: linking "Korovkin's theorem" would link
# a theorem name, which is not the point of \omterm.
DROP = {
    "Gauss's limit formula",                             # ch. 9 problem
    "Korovkin's theorem",                                # ch. 10 problem
    "Hadamard's inequality",                             # ch. 12 problem
    "Courant--Fischer min-max theorem",                  # ch. 13 problem
    "Weyl's perturbation inequalities",
    "Jacobi's formula",                                  # ch. 15 problem
    "Sturm's separation and comparison theorems",        # ch. 16 problem
    "Chernoff bound", "concentration inequalities",      # ch. 22 problem: results
    # named in a figure caption; the nearest statement is "Parseval as a
    # computing device", which is not where Gibbs is explained
    "Gibbs phenomenon",
    # adverbs whose ordinary-English sense is the only one used
    "symmetrically",  # "($x$-elementary: symmetrically)" = "in the same way"
    "cyclically",     # "the cyclic invariance of the trace"
    # STOP would still link these in the chapter that defines them (a
    # stoplisted word stays chapter-local); here even that chapter mixes the
    # senses, so they must go entirely. Their phrases survive.
    "closed",         # ch. 20 alone has "closed form", "closed arc", "closed disk"
    # convexity of a *set* (ch. 17) vs of a *function* (Jensen, ch. 8 and the
    # pgf of ch. 23): the noun is used in both senses, the adjective is not
    "convexity",
}

PRIMARY_OK = set()  # no overloaded word here has a dominant first sense
AMBIG_POLICY = "drop"   # a term defined twice, with no phrase to tell the
                        # senses apart, is not linked at all

# Spans that must not be touched. Two kinds:
#   (a) fixed phrases where a defined word carries another sense;
#   (b) the shared "hyphenated prefix" rule biting on a TeX accent
#       (Ces\`aro-summable) or on a compound whose head changes the sense.
EXTRA_PROTECT = [
    r'Ces\\`aro-summable',          # not the "summable family" of ch. 7
    r'Abel-summable',
    r'conjugate-symmetric',         # a Hermitian form, not a symmetric endomorphism
    r'linear-algebra',              # "a linear-algebra fact", not a $K$-algebra
    r'circle-generated',
    # (a) "complete" as verb ("complete the square") or as "full"
    r'[Cc]omplet(?:e|es|ed|ing)\s+(?:the|it|its|this|these|a|an|into|squares?)\b',
    r'complete\s+(?:theory|formula|picture|power-mean|list|second-order)\b',
    r'chain,\s*complete',
    r'never be complete',
    # "uniformly" = drawn from the uniform law (ch. 21-23), or uniform
    # continuity / uniformity in a parameter -- not uniform convergence
    r'uniformly\s+(?:at\s+random|random|randomly|chosen|continuous|in\b)',
    r'uniformly\)',
    r'drawn uniformly',
    r'(?:doors|toys|steps),\s*uniformly',
    # a protect regex must never *consume* a `$`: the inline-math rule in
    # protect.py pairs dollars, and eating one desynchronizes every `$...$`
    # after it (half the file's prose then reads as math and takes no links).
    # Match around the math with a look-behind instead.
    r'(?<=\\pm1\)\$)\s*uniformly',
    # "differential" as an adjective on a subject, not the differential of a map
    r'differentials?\s+(?:calculus|equations?|geometry|system)\b',
    r'turns differential',
    # "length" of a run / of a lattice path (ch. 21), not arc length
    r'\brun\s+length',
    r'\bpaths?\s+of\s+length',
    r'text of any\s+length',
    # "order" in its ordinary English sense, in the chapter that defines the
    # order of a group element (a stoplisted word is still linked there)
    r'order relations',
    r'(?:reading|cyclic|reversed)\}?\s+order',
    r'order of the (?:factors|tiles)',
    # "cyclic invariance of the trace" is not the cyclic group of ch. 1
    r'cyclic\}?\s+invariance',
    # "law" as the name of a result, not the law of a random variable
    r'(?:strong|weak)\}?\s+law',        # also "the \emph{strong} law"
    r'law\s+of\s+large\s+numbers',
    r'law of rare events',
    r'local laws',
    r'almost-sure law',
    r'(?<=\$)\s+law\b',             # "the $1/\delta^2$ law"
    # "independent of $n$" = does not depend on $n$
    r'independent(?=\s+of\s+\$)',
    # a convex function / curve is not the convex set of ch. 17
    r'convex\s+(?:functions?|curve)',
    # ordinary English in the newly visible text
    r'cycle forever',            # iteration may cycle, not a permutation cycle
    r'symmetric\s+event',        # the mirrored event of a random walk
    r'open the doors',           # "the Year 3 volume will open the doors"
    r'closed forms?\s*\\\[',      # "prove the closed forms \[ q_n = ... \]"
    r'closed form gives',        # an explicit formula, not a closed 1-form
    # "the host opens a door" (Monty Hall), not an open set
    r'\bopens\b',
    r'open problem',
    # paper envelopes in the derangement problem, not the envelope of a family
    # of curves (ch. 18)
    r'right envelope',
    r'envelopes, one each',
]
