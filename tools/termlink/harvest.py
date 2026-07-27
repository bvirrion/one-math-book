"""Which terms are linkable, and to which definition.

Sources, in order of trust:

  * \\emph{term}\\index{...} inside a `definition` -- the convention in
    CONTRIBUTING.md. A bare \\emph is ordinary emphasis: linking those made
    "countable" point at the sigma-algebra definition.
  * the \\index{...} entries themselves, which give the canonical, usually
    multi-word phrase ("compact operator", "compact space"). These disambiguate:
    the bare word "compact" is not linked, but each of its phrases links to its
    own definition.
  * a bare \\emph agreeing with the definition's own label leaf
    (def:b3:measure:measure <-> "measure space").
  * \\emph{term}\\index{...} outside a definition -- a theorem or an example often
    introduces a notion; the link targets that statement.

Theorem names ("Baire's theorem") are not terms: the point is to link
definitions, not results.
"""
import collections
import os
import re

from . import morphology

DEF_RE = re.compile(r'\\begin\{definition\}(.*?)\\end\{definition\}', re.S)
# one level of brace nesting: the escaped Dutch tree writes quoti\"{e}nt, and a
# term stopping at the first brace would harvest nothing at all there.
G = r'(?:[^{}]|\{[^{}]*\})'
EMPH_INDEX = r'\\emph\{(' + G + r'+)\}\s*\\index\{'
EMPH = r'\\emph\{(' + G + r'+)\}(\s*\\index\{)?'
INDEX = r'\\index\{(' + G + r'*)\}'
# pb: is here because a weekend problem introduces notions of its own (the
# Cantor set, the Rayleigh quotient). Without it their \index entries were
# attributed to the last statement before the problem -- an unrelated remark
# pages away, which is a wrong link, not a missing one.
STMT_LABEL = r'\\label\{((?:thm|prop|lem|cor|ex|met|rem|pb):[^}]*)\}'
ANY_LABEL = r'\\label\{([a-z]+:[^}]*)\}'


def index_display(entry):
    """\\index{sort key@display} -> display; skip subentries."""
    entry = re.sub(r'\s+', ' ', entry).strip()
    if "!" in entry:
        return None
    if "@" in entry:
        entry = entry.split("@", 1)[1]
    return entry.strip() or None


def _too_long(term, cfg):
    if cfg.MAX_TERM_WORDS and len(term.split()) > cfg.MAX_TERM_WORDS:
        return True
    if cfg.MAX_TERM_CHARS and len(term) > cfg.MAX_TERM_CHARS:
        return True
    return False


def read(path):
    return open(path, encoding="utf8").read()


def _en_twin(path, lang):
    """parts/<year>[/solutions]/<lang>/NN-slug.tex -> the English twin path.

    The language directory is always the last one before the filename, so
    dropping it yields the canonical English body. Returns None for English.
    """
    parts = path.replace("\\", "/").split("/")
    if lang == "en" or len(parts) < 2 or parts[-2] != lang:
        return None
    return "/".join(parts[:-2] + parts[-1:])


def _bare_emph_ordinals(body, leaf):
    """Positions, among a definition body's bare \\emph's, that name the term.

    This is the English rule of record: a bare \\emph counts only when it agrees
    with the definition's own label leaf. Returns the ordinals so a translation
    can harvest the *same* emphases without re-testing them against an English
    leaf it cannot match.
    """
    out, i = set(), 0
    for e in re.finditer(EMPH, body):
        if e.group(2):
            continue
        term = re.sub(r'\s+', ' ', e.group(1)).strip()
        key = re.sub(r'[^a-z]', '', morphology.to_text(term).lower())
        if key and len(key) >= 4 and (key.startswith(leaf) or leaf.startswith(key)):
            out.add(i)
        i += 1
    return out


def bare_emph_map(files, lang):
    """{def label: {ordinal}} harvested from the English twins of `files`.

    A bare \\emph is accepted in a translation when the English twin accepted
    the emphasis in the same position. Matching on the English label leaf
    cannot work once the term is translated ("clases" vs the leaf "classes"),
    which silently dropped every such definition from the translated editions;
    the structural mirror the translation gates enforce makes the ordinal
    correspondence exact.
    """
    out = {}
    if lang == "en":
        return out
    for path, _, is_sol in files:
        if is_sol:
            continue
        twin = _en_twin(path, lang)
        if not twin or not os.path.exists(twin):
            continue
        s = read(twin)
        for m in DEF_RE.finditer(s):
            body = m.group(1)
            lab = re.search(r'\\label\{(def:[^}]*)\}', body)
            if not lab:
                continue
            ords = _bare_emph_ordinals(body, lab.group(1).split(":")[-1].lower())
            if ords:
                out[lab.group(1)] = ords
    return out


def harvest(files, cfg, lang, langcfg, load=read):
    """-> (terms, def_seq, local, primary, nearest, stats)

    terms   : {term: label}          linked everywhere from its chapter on
    def_seq : {label: chapter seq}
    local   : {term: {seq: label}}   overloaded word, sense pinned by a chapter
    primary : {term: label}          overloaded word whose first sense dominates
    nearest : {term: [(seq, label)]} AMBIG_POLICY = "nearest-preceding"
    """
    course = [(p, seq) for p, seq, is_sol in files if not is_sol]
    bare_ok = bare_emph_map(files, lang)       # label -> {ordinal}, non-English
    defs = collections.defaultdict(list)      # term -> [(label, seq)]
    def_seq = {}                              # label -> seq
    all_seq = {}                              # every label -> seq, for EXTRA

    for path, seq in course:
        s = load(path)
        for lab in re.findall(ANY_LABEL, s):
            all_seq.setdefault(lab, seq)
        for lab in re.findall(r'\\label\{(def:[^}]*)\}', s):
            def_seq[lab] = seq
        for m in DEF_RE.finditer(s):
            body = m.group(1)
            lab = re.search(r'\\label\{(def:[^}]*)\}', body)
            if not lab:
                continue
            lab = lab.group(1)
            for e in re.finditer(EMPH_INDEX, body):
                defs[re.sub(r'\s+', ' ', e.group(1)).strip()].append((lab, seq))
            for e in re.finditer(INDEX, body):
                d = index_display(e.group(1))
                if d:
                    defs[d].append((lab, seq))
            leaf = lab.split(":")[-1].lower()
            # English decides by its own label leaf; a translation defers to the
            # ordinals its English twin accepted (empty set = accept none, so a
            # term that merely happens to look like the English leaf is not
            # picked up by accident).
            ords = None if lang == "en" else bare_ok.get(lab, frozenset())
            i = 0
            for e in re.finditer(EMPH, body):
                if e.group(2):
                    continue
                term = re.sub(r'\s+', ' ', e.group(1)).strip()
                if ords is None:
                    key = re.sub(r'[^a-z]', '', morphology.to_text(term).lower())
                    ok = (key and len(key) >= 4
                          and (key.startswith(leaf) or leaf.startswith(key)))
                else:
                    ok = i in ords
                if ok:
                    defs[term].append((lab, seq))
                i += 1

    ambig = {t for t, v in defs.items() if len({l for l, _ in v}) > 1}
    terms = {t: v[0][0] for t, v in defs.items()
             if t not in cfg.STOP and t not in ambig and len(t) >= 3
             and not _too_long(t, cfg)}

    # notions introduced outside a definition environment
    for path, seq in course:
        s = load(path)
        body = DEF_RE.sub(lambda m: " " * len(m.group(0)), s)
        for e in re.finditer(EMPH_INDEX, body):
            t = re.sub(r'\s+', ' ', e.group(1)).strip()
            labs = re.findall(STMT_LABEL, s[:e.start()])
            if (not labs or t in cfg.STOP or t in terms or len(t) < 3
                    or _too_long(t, cfg)):
                continue
            terms[t] = labs[-1]
            def_seq[labs[-1]] = seq
        for e in re.finditer(INDEX, body):
            d = index_display(e.group(1))
            if not d or d in terms or d in cfg.STOP or _too_long(d, cfg):
                continue
            if " " not in d or len(d) < 5:
                continue
            if any(k in d.lower() for k in cfg.NOT_A_TERM):
                continue
            labs = re.findall(STMT_LABEL, s[:e.start()])
            if labs:
                terms[d] = labs[-1]
                def_seq[labs[-1]] = min(def_seq.get(labs[-1], seq), seq)

    # derived forms, kept only if they really occur in the book
    for base, forms in cfg.DERIVED.items():
        if base in terms:
            for v in forms:
                terms.setdefault(v, terms[base])
    corpus = " ".join(load(p) for p, _, _ in files)
    for base in list(terms):
        for v in morphology.derive(base, langcfg):
            if v not in terms and re.search(
                    r'(?<![\w\\])' + re.escape(v) + r'(?![\w])', corpus):
                terms[v] = terms[base]

    # overloaded words: linked only where the sense is pinned down
    local = collections.defaultdict(dict)
    nearest = {}
    for t, v in defs.items():
        if t in terms:
            continue
        by_seq = collections.defaultdict(set)
        for lab, seq in v:
            by_seq[seq].add(lab)
        for seq, labs in by_seq.items():
            if len(labs) == 1:
                local[t][seq] = next(iter(labs))
    if cfg.AMBIG_POLICY == "nearest-preceding":
        # a spiral curriculum re-defines its terms: a grade-8 use of "fraction"
        # must land on the grade-6 re-definition, not grade-4's. Dropping them
        # (the Book 3-5 rule) would throw away a fifth of Books 1-2's terms.
        for t, chmap in local.items():
            if t not in cfg.STOP:
                nearest[t] = sorted(chmap.items())
    primary = {t: sorted(m.items())[0][1]
               for t, m in local.items() if t in cfg.PRIMARY_OK}

    for t in cfg.DROP:
        terms.pop(t, None)
        local.pop(t, None)
        nearest.pop(t, None)
        primary.pop(t, None)
    terms.update(cfg.EXTRA)      # manual entries win over every rule above
    for lab in cfg.EXTRA.values():
        # so EXTRA can point a term at a theorem or a weekend problem, not only
        # at a definition: wrap_file drops a term whose label has no chapter.
        if lab not in def_seq and lab in all_seq:
            def_seq[lab] = all_seq[lab]

    stats = {
        "harvested": len(defs),
        "ambiguous": len(ambig),
        "stoplisted": len([t for t in defs if t in cfg.STOP]),
        "linkable": len(terms),
    }
    return terms, def_seq, local, primary, nearest, stats
