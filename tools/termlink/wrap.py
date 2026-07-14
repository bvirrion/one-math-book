"""Wrapping the uses: every occurrence of a linkable term becomes
\\omterm{<label>}{<term>}, in the course text, the exercises, the problems and
the solutions, so a reader can jump to the definition from wherever they are.
"""
import collections
import re

from . import morphology
from .harvest import DEF_RE

OMTERM = re.compile(r'\\omterm\{[^{}]*\}\{((?:[^{}]|\{[^{}]*\})*)\}')


def unwrap(s):
    """Strip the wrapping back to plain text. Matches every label prefix, not
    just def: -- Book 5 links 455 terms to thm:/ex:/prop:/... -- the display
    argument may straddle a newline (108 of Book 5's links do), and it may hold
    a brace group: the escaped Dutch tree writes quoti\\"{e}nt, and a display
    this does not match is neither unwrapped nor protected, so every regenerate
    cycle wraps it once more, one nesting deeper."""
    prev = None
    while prev != s:
        prev, s = s, OMTERM.sub(lambda m: m.group(1), s)
    return s


def segments(s, is_solutions):
    """Every exercise / problem / solution, and every section of running text."""
    envs = ["solution"] if is_solutions else ["exercise", "problem"]
    spans, covered = [], bytearray(len(s))
    for env in envs:
        for m in re.finditer(r'\\begin\{%s\}.*?\\end\{%s\}' % (env, env), s, re.S):
            spans.append([(m.start(), m.end())])
            for i in range(m.start(), m.end()):
                covered[i] = 1
    cuts = [0] + [m.start() for m in re.finditer(r'\\section\{', s)] + [len(s)]
    for a, b in zip(cuts, cuts[1:]):
        ranges, start = [], None
        for i in range(a, b):
            if not covered[i] and start is None:
                start = i
            if covered[i] and start is not None:
                ranges.append((start, i))
                start = None
        if start is not None:
            ranges.append((start, b))
        if ranges:
            spans.append(ranges)
    return spans


def in_force(seq, terms, local, primary, nearest):
    """The terms linkable in this chapter: the global ones, plus the overloaded
    words whose sense this chapter pins down (or whose earlier sense still
    holds)."""
    out = dict(terms)
    for t, chmap in local.items():
        if seq in chmap:
            out[t] = chmap[seq]
        elif t in primary and min(chmap) <= seq:
            out[t] = primary[t]
    for t, pairs in nearest.items():
        earlier = [lab for s, lab in pairs if s <= seq]
        if earlier:
            out[t] = earlier[-1]
    return out


def wrap_file(path, seq, is_sol, terms, def_seq, local, primary, nearest,
              mask, lang, langcfg, no_capital, load=None):
    s = load(path) if load else open(path, encoding="utf8").read()
    m = mask(s)
    self_spans = collections.defaultdict(list)
    for d in DEF_RE.finditer(s):
        lab = re.search(r'\\label\{(def:[^}]*)\}', d.group(0))
        if lab:
            self_spans[lab.group(1)].append((d.start(), d.end()))

    active = in_force(seq, terms, local, primary, nearest)
    edits = []
    for ranges in segments(s, is_sol):
        # longest first: "compact operator" must beat "operator"
        for term, lab in sorted(active.items(), key=lambda kv: -len(kv[0])):
            if def_seq.get(lab, float("inf")) > seq:
                continue                                   # used before defined
            pat = morphology.pattern(term, lang, langcfg, no_capital)
            for (a, b) in ranges:
                for mt in pat.finditer(s, a, b):
                    i, j = mt.start(), mt.end()
                    if any(m[k] for k in range(i, j)):
                        continue
                    if any(a2 <= i < b2 for a2, b2 in self_spans.get(lab, [])):
                        continue
                    if any(not (j <= i2 or j2 <= i) for i2, j2, _ in edits):
                        continue
                    edits.append((i, j, lab))
                    for k in range(i, j):
                        m[k] = 1
    for i, j, lab in sorted(edits, reverse=True):
        s = s[:i] + "\\omterm{" + lab + "}{" + s[i:j] + "}" + s[j:]
    return s, [lab for _, _, lab in edits]
