#!/usr/bin/env python3
"""Link defined terms to their definitions (Book 5 / parts/bachelor-3).

Wraps a term as \\omterm{def:...}{term} so it links to the definition that
introduces it. Every occurrence is linked -- in the course text, exercises,
problems and solutions -- so a reader can always jump from a term to the place
it is defined.

    python3 tools/link_defined_terms.py            # dry run: report only
    python3 tools/link_defined_terms.py --apply    # rewrite the sources

Run from the repository root. Idempotent: terms already wrapped are left alone.
The intended workflow after adding chapters/definitions is
`git checkout parts/bachelor-3/` then re-run with --apply.

Where terms come from (both sources are inside `definition` environments):

  * \\emph{term}\\index{...}  -- the convention in CONTRIBUTING.md. A bare \\emph
    is ordinary emphasis: linking those made "countable" point at the
    sigma-algebra definition.
  * the \\index{...} entries themselves, which give the canonical, usually
    multi-word phrase ("compact operator", "compact space", "closed form").
    These disambiguate: the bare word "compact" is NOT linked, but each of its
    two phrases links to its own definition.

Never linked: a term defined in two places with no phrase to tell them apart;
words whose sense changes by chapter (basis, degree, Euclidean, separable);
ordinary English ("free", as in "for free"); anything inside math, comments,
macro arguments, environment names or their key arguments (wrapping a term
inside \\begin{solution}{exo:...} once blew up the build).
"""
import re, glob, collections, json, sys

APPLY = "--apply" in sys.argv
ROOT  = "parts/bachelor-3"

# --------------------------------------------------------------------------
# 1. harvest terms from definition environments
# --------------------------------------------------------------------------
defs   = collections.defaultdict(list)      # term -> [(label, chapter)]
def_ch = {}                                 # label -> chapter

def index_display(entry):
    """\\index{sort key@display} -> display; skip subentries."""
    entry = re.sub(r'\s+', ' ', entry).strip()
    if "!" in entry: return None
    if "@" in entry: entry = entry.split("@", 1)[1]
    return entry.strip() or None

for f in sorted(glob.glob(ROOT + "/[0-9]*.tex")):
    ch = int(f.split("/")[-1][:2])
    s = open(f).read()
    for lab in re.findall(r'\\label\{(def:[^}]*)\}', s):
        def_ch[lab] = ch
    for m in re.finditer(r'\\begin\{definition\}(.*?)\\end\{definition\}', s, re.S):
        body = m.group(1)
        lab = re.search(r'\\label\{(def:[^}]*)\}', body)
        if not lab: continue
        lab = lab.group(1)
        for e in re.finditer(r'\\emph\{([^{}]+)\}\s*\\index\{', body):
            defs[re.sub(r'\s+', ' ', e.group(1)).strip()].append((lab, ch))
        for e in re.finditer(r'\\index\{([^{}]*)\}', body):
            d = index_display(e.group(1))
            if d: defs[d].append((lab, ch))
        # some definitions introduce their term with \emph and no adjacent
        # \index. Recover those when the emphasis agrees with the definition's
        # own label leaf (def:b3:measure:measure <-> "measure space") -- a much
        # tighter test than "any \emph", which would relink "countable".
        leaf = lab.split(":")[-1].lower()
        for e in re.finditer(r'\\emph\{([^{}]+)\}(\s*\\index\{)?', body):
            if e.group(2): continue
            term = re.sub(r'\s+', ' ', e.group(1)).strip()
            key = re.sub(r'[^a-z]', '', term.lower())
            if key and len(key) >= 4 and (key.startswith(leaf) or leaf.startswith(key)):
                defs[term].append((lab, ch))

# --------------------------------------------------------------------------
# 2. curate
# --------------------------------------------------------------------------
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

ambig = {t for t, v in defs.items() if len({l for l, _ in v}) > 1}
terms = {t: v[0][0] for t, v in defs.items()
         if t not in STOP and t not in ambig and len(t) >= 3}

# --------------------------------------------------------------------------
# 2b. more terms, more forms
# --------------------------------------------------------------------------
# (i) notions introduced outside a definition environment -- a theorem or an
#     example often introduces one (\emph{$p$-group}\index{...}); the link
#     targets the statement that introduces it.
outside_ch = {}
for f in sorted(glob.glob(ROOT + "/[0-9]*.tex")):
    ch = int(f.split("/")[-1][:2])
    s_ = open(f).read()
    body = re.sub(r'\\begin\{definition\}.*?\\end\{definition\}',
                  lambda m: " " * len(m.group(0)), s_, flags=re.S)
    for e in re.finditer(r'\\emph\{([^{}]+)\}\s*\\index\{', body):
        t = re.sub(r'\s+', ' ', e.group(1)).strip()
        labs = re.findall(r'\\label\{((?:thm|prop|lem|cor|ex|met|rem):[^}]*)\}', s_[:e.start()])
        if not labs or t in STOP or t in terms or len(t) < 3: continue
        terms[t] = labs[-1]; def_ch[labs[-1]] = ch; outside_ch[t] = ch

# (i-bis) canonical \index phrases attached to a non-definition statement --
#     notions introduced in an example or a proposition ("Beta function",
#     "Poisson kernel"). Theorem names ("Baire's theorem") are NOT terms and are
#     excluded: the request is to link definitions, not results.
NOT_A_TERM = ("theorem", "lemma", "inequality", "formula", "criterion",
              "principle", "identity", "rule", "law of", "paradox", "problem")
for f in sorted(glob.glob(ROOT + "/[0-9]*.tex")):
    ch = int(f.split("/")[-1][:2])
    s_ = open(f).read()
    body = re.sub(r'\\begin\{definition\}.*?\\end\{definition\}',
                  lambda m: " " * len(m.group(0)), s_, flags=re.S)
    for e in re.finditer(r'\\index\{([^{}]*)\}', body):
        d = index_display(e.group(1))
        if not d or d in terms or d in STOP: continue
        if " " not in d or len(d) < 5: continue
        if any(k in d.lower() for k in NOT_A_TERM): continue
        labs = re.findall(r'\\label\{((?:thm|prop|lem|cor|ex|met|rem):[^}]*)\}', s_[:e.start()])
        if labs:
            terms[d] = labs[-1]; def_ch[labs[-1]] = min(def_ch.get(labs[-1], ch), ch)

# (ii) derived forms: continuity <- continuous, measurability <- measurable, ...
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
for base_t, forms in DERIVED.items():
    if base_t in terms:
        for v in forms: terms.setdefault(v, terms[base_t])

# and the regular derivations, generated then kept only if they really occur:
# holomorphic -> holomorphically, measurable -> measurability, ...
_corpus = " ".join(open(f).read() for f in
                   glob.glob(ROOT + "/[0-9]*.tex") + glob.glob(ROOT + "/solutions/[0-9]*.tex"))
def _derive(t):
    out = []
    if " " in t or "$" in t: return out
    if t.endswith("ic"):    out += [t + "ally"]
    if t.endswith("ous"):   out += [t[:-3] + "ously"]
    if t.endswith("able"):  out += [t[:-4] + "ability", t[:-1] + "y"]
    if t.endswith("ible"):  out += [t[:-4] + "ibility"]
    if t.endswith("ive"):   out += [t[:-1] + "ely"]
    if t.endswith("ent"):   out += [t[:-1] + "ce"]
    if t.endswith("al"):    out += [t + "ly"]
    return out
for base_t in list(terms):
    for v in _derive(base_t):
        if v not in terms and re.search(r'(?<![\w\\])' + re.escape(v) + r'(?![\w])', _corpus):
            terms[v] = terms[base_t]

# (iii) overloaded words: linked only where the sense is pinned down -- inside a
#     chapter that defines it (compact = space in ch6, = operator in ch15), and,
#     for a few whose primary sense dominates the book, elsewhere too.
PRIMARY_OK = {"compact", "closed", "path", "boundary", "interior", "irreducible"}
local = collections.defaultdict(dict)      # term -> {chapter: label}
for t, v in defs.items():
    if t in terms: continue
    by_ch = collections.defaultdict(set)
    for lab, ch in v: by_ch[ch].add(lab)
    for ch, labs in by_ch.items():
        if len(labs) == 1: local[t][ch] = next(iter(labs))
primary = {t: sorted(m.items())[0][1] for t, m in local.items() if t in PRIMARY_OK}

# --------------------------------------------------------------------------
# 3. wrap
# --------------------------------------------------------------------------
PROTECT = [
    r'%.*',
    r'\$\$.*?\$\$', r'(?<!\\)\$(?:\\.|[^$\\])*\$',
    r'\\\[.*?\\\]',
    r'\\begin\{(align\*?|equation\*?|gather\*?|multline\*?|tikzpicture|pmatrix|smallmatrix|psmallmatrix|array)\}.*?\\end\{\1\}',
    r'\\(?:label|index|cref|Cref|ref|eqref|input|ominput|ominputsol|hyperref|href|hypertarget|hyperlink|omterm|texorpdfstring)\{[^{}]*\}(?:\{[^{}]*\})?',
    r'\\(?:chapter|section|subsection|part)\*?\{[^{}]*\}',
    # a defining \emph{term}\index{...} is never linked: inside the definition
    # of "outer measure", the inner word "measure" must not link away.
    r'\\emph\{[^{}]*\}\s*\\index\{[^{}]*\}',
    r'\\begin\{[a-z*]+\}\[[^\]]*\]',
    r'\\begin\{[a-zA-Z*]+\}\{[^{}]*\}',
    r'\\(?:begin|end)\{[a-zA-Z*]+\}',
]
PROT_RE = re.compile("|".join(PROTECT), re.S)

def mask(s):
    m = bytearray(len(s))
    for mt in PROT_RE.finditer(s):
        for i in range(mt.start(), mt.end()): m[i] = 1
    return m

def pattern(term):
    """Match the term, allowing a plural on the last word, a capitalised first
    letter (sentence start), and a hyphenated prefix ("non-measurable"), which
    is linked whole. Never split an existing hyphenated compound in two, or
    "torsion-free" becomes two links."""
    body = re.escape(term).replace(r'\ ', r'\s+')
    if term[:1].isalpha() and term[:1].islower():
        body = "[" + term[0].upper() + term[0] + "]" + body[1:]
    tail = "" if term.endswith(("s", "$", "]", ")")) else r'(?:e?s)?'
    head = r'(?:[A-Za-z]+-)?' if " " not in term else ""
    return re.compile(r'(?<![\w\\@-])(' + head + body + tail + r')(?![\w-])')

def segments(s, is_solutions):
    """Independent 'first use' scopes: every exercise / problem / solution, and
    every section of the running text."""
    envs = ["solution"] if is_solutions else ["exercise", "problem"]
    spans, covered = [], bytearray(len(s))
    for env in envs:
        for m in re.finditer(r'\\begin\{%s\}.*?\\end\{%s\}' % (env, env), s, re.S):
            spans.append([(m.start(), m.end())])
            for i in range(m.start(), m.end()): covered[i] = 1
    # the rest, cut at \section boundaries
    cuts = [0] + [m.start() for m in re.finditer(r'\\section\{', s)] + [len(s)]
    for a, b in zip(cuts, cuts[1:]):
        ranges = []
        start = None
        for i in range(a, b):
            if not covered[i] and start is None: start = i
            if covered[i] and start is not None: ranges.append((start, i)); start = None
        if start is not None: ranges.append((start, b))
        if ranges: spans.append(ranges)
    return spans

total = collections.Counter()
for f in sorted(glob.glob(ROOT + "/[0-9]*.tex") + glob.glob(ROOT + "/solutions/[0-9]*.tex")):
    is_sol = "/solutions/" in f
    ch = int(f.split("/")[-1][:2])
    s = open(f).read()
    m = mask(s)
    self_spans = collections.defaultdict(list)
    for d in re.finditer(r'\\begin\{definition\}.*?\\end\{definition\}', s, re.S):
        lab = re.search(r'\\label\{(def:[^}]*)\}', d.group(0))
        if lab: self_spans[lab.group(1)].append((d.start(), d.end()))

    # terms in force for this chapter: the global ones, plus the overloaded
    # words whose sense this chapter pins down (or whose primary sense holds).
    in_force = dict(terms)
    for t, chmap in local.items():
        if ch in chmap:        in_force[t] = chmap[ch]
        elif t in primary and min(chmap) <= ch: in_force[t] = primary[t]

    edits = []
    for ranges in segments(s, is_sol):
        # longest first: "compact operator" must beat "operator"
        for term, lab in sorted(in_force.items(), key=lambda kv: -len(kv[0])):
            if def_ch.get(lab, 99) > ch: continue           # used before defined
            pat = pattern(term)
            for (a, b) in ranges:
                for mt in pat.finditer(s, a, b):
                    i, j = mt.start(), mt.end()
                    if any(m[k] for k in range(i, j)): continue
                    if any(a2 <= i < b2 for a2, b2 in self_spans.get(lab, [])): continue
                    if any(not (j <= i2 or j2 <= i) for i2, j2, _ in edits): continue
                    edits.append((i, j, lab)); total[f] += 1
                    for k in range(i, j): m[k] = 1
    for i, j, lab in sorted(edits, reverse=True):
        s = s[:i] + "\\omterm{" + lab + "}{" + s[i:j] + "}" + s[j:]
    if APPLY: open(f, "w").write(s)

print("terms harvested        : %d" % len(defs))
print("dropped (defined twice): %d" % len(ambig))
print("dropped (stoplist)     : %d" % len([t for t in defs if t in STOP]))
print("LINKABLE TERMS         : %d" % len(terms))
print("links %s: %d across %d files"
      % ("inserted" if APPLY else "to insert", sum(total.values()), len(total)))
