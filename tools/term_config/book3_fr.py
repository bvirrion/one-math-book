"""Book 3 -- fr. Curation only; the rules live in tools/termlink/.

Every key is optional: anything left out falls back to the defaults in
tools/link_defined_terms.py.

The traps are not the English ones. "premier" is the prime *and* the ordinal
("le premier terme", "du premier ordre"), "fini" is the finite set *and* the
"accroissements finis", "argument" is the argument of a complex number *and*
"le même argument s'applique", "unitaire" is the monic polynomial *and* the unit
vector, "symétrie" is the linear involution *and* "par symétrie". Each word was
read in context in parts/bachelor-1/fr/ before being kept or dropped.

The other half of the work is the reverse: tools/term_config/lang_fr.py sets
DERIVE = False (the English -ic/-able/-ent derivations mean nothing here) and
WORD_TAIL = (?:e?s)?, which spells "", "s" and "es" -- but *not* the feminine
singular "e". So every real French variant has to be declared by hand:
continu -> continue/continûment, dérivable -> dérivabilité, convexe ->
convexité, injective -> injectif/injectivité/injection, orthogonal ->
orthogonaux. Missing those is how a French edition quietly loses a thousand
links.
"""

# Kept out of the book-wide vocabulary, but STILL linked inside the chapter that
# defines them (STOP is soft): each of these is the notion in its own chapter and
# ordinary French everywhere else.
STOP = {
    # ch. 6 = prime; everywhere else the ordinal. 168 uses from ch. 6 on, and
    # outside arithmetic almost none of them is a prime: "le premier terme",
    # "du premier ordre" (ch. 5, 16, 17), "les $n$ premiers chiffres" (ch. 10,
    # 12), "le premier anneau non commutatif" (ch. 7). "nombre premier",
    # "premiers entre eux" and "décomposition en facteurs premiers" are terms of
    # their own and keep their links everywhere.
    "premier",
    # ch. 2 = the finite set. Elsewhere: "le théorème des accroissements finis"
    # (the mean value theorem -- ch. 14, 25), "un nombre fini de points",
    # "une réunion finie", "C'est fini." The compounds that matter -- "ensemble
    # fini", "dimension finie", "de dimension finie" -- are terms of their own.
    "fini",
    # ch. 3 = the argument of a complex number. From ch. 4 on it is the register
    # word: "le même argument s'applique", "un argument de dimension",
    # "l'argument diagonal", "les arguments de compacité".
    "argument",
    # ch. 8 = a monic polynomial. From ch. 23 on it is a *unit* vector ("la
    # seconde, unitaire et orthogonale à elle", "des produits de vecteurs
    # unitaires"). "polynôme unitaire" is a term of its own.
    "unitaire",
    # ch. 20 = the linear involution $s^2 = \\mathrm{id}$. From ch. 23 on it is
    # plane geometry ("axes de symétrie", "symétrie centrale") and from ch. 25
    # the register ("contrôle par symétrie"). "symétrie glissée" keeps its link.
    "symétrie",
}

# Never linked anywhere.
DROP = {
    # "une isométrie directe" (ch. 23, $\\det = 1$ -- not a direct sum), "une
    # étude directe du signe", "une conséquence directe". The notion that earns a
    # link is "somme directe", which is a term of its own and wins by being
    # longer.
    "directe",
    # harvested from "matrices équivalentes", but "les assertions suivantes sont
    # équivalentes" is the commonest sentence in the book. "matrices
    # équivalentes" and "fonctions équivalentes" keep their own links.
    "équivalentes",
    # harvested from "nombre algébrique" (the weekend problem of ch. 1), but 50
    # of its 57 uses are the ordinary adjective: "une structure algébrique",
    # "la forme algébrique" of a complex number (ch. 3), "un calcul algébrique",
    # "toute manipulation algébrique", "l'aire algébrique" of a determinant,
    # "les opérations algébriques". "nombre algébrique" is a term of its own.
    "algébrique",
}

# Terms the harvester cannot see, and the French variants DERIVE = False will
# never generate.
EXTRA = {
    # the definition emphasises the compound -- \\emph{continue en $x_0 \\in I$},
    # \\emph{dérivable en $x_0 \\in I$} -- whose pattern is pure inline math and
    # therefore never matches. The bare adjective, which is what the other
    # twelve chapters actually write, is never harvested at all.
    "continu":       "def:b1:continuity:continuous",   # + continus, continues
    "continue":      "def:b1:continuity:continuous",   # the feminine WORD_TAIL misses
    "continûment":   "def:b1:continuity:continuous",
    "dérivable":     "def:b1:derivative:def",
    "dérivabilité":  "def:b1:derivative:def",
    "convexité":     "def:b1:derivative:convex",
    # the word ch. 18-23 write nine times out of ten; only the full "sous-espace
    # vectoriel" is harvested. "sous-espace engendré" and "sous-espaces
    # supplémentaires" are longer and still win.
    "sous-espace":   "def:b1:vspaces:subspace",
    # def:b1:logic:inj defines injective/surjective/bijective; the nouns are what
    # the proofs use ("l'injectivité se teste sur le noyau", "une bijection de
    # $G$ sur lui-même").
    "injectivité":   "def:b1:logic:inj",
    "surjectivité":  "def:b1:logic:inj",
    "bijectivité":   "def:b1:logic:inj",
    "injection":     "def:b1:logic:inj",
    "surjection":    "def:b1:logic:inj",
    "bijection":     "def:b1:logic:inj",
    # \\emph{divise} and \\index{divisibilité} are separated by "$a$ (on note $b
    # \\mid a$)", so the pair is never harvested and only the noun survives.
    "divise":        "def:b1:arith:divides",
    "divisent":      "def:b1:arith:divides",
    "congru":        "def:b1:arith:congruence",
}

# Linked mid-sentence, never sentence-initially: "Application~:" and
# "Applications." open a paragraph that *applies* a theorem -- they are not the
# map of def:b1:logic:map.
NO_CAPITAL = {"application"}

# WORD_TAIL spells "", "s", "es" -- never the feminine singular "e", and never a
# masculine in -if / -aux. These are the forms that really occur in the book.
DERIVED = {
    "injective":       ["injectif"],
    "surjective":      ["surjectif"],
    "bijective":       ["bijectif"],
    "orthogonal":      ["orthogonaux"],
    "supplémentaires": ["supplémentaire"],
    "conjugué":        ["conjuguée"],
}

PRIMARY_OK = set()

AMBIG_POLICY = "drop"          # the university convention (books 3, 4, 5)

# Spans no link may enter: the uses where a good term means something else.
# NB every space is \s+ -- the sources wrap at 72 columns, and a phrase split
# across two lines ("corps\nnon dénombrable") slips past a literal space and the
# link lands anyway. And no pattern may CONSUME a "$": that inverts inline-math
# masking for the rest of the file (it cost Book 3 a thousand links in English).
EXTRA_PROTECT = [
    # "divise": the ordinary verb -- "on divise, $a = bq + r$", "on divise par
    # $x$ et on recommence". The relation -- "$p_i$ divise $N$" -- keeps its link.
    r'[Oo]n\s+divise',
    r'se\s+divisent', r"divisent\s+l'erreur",
    # "argument": the one non-complex use inside ch. 3 itself.
    r'même\s+argument',
    # "premier": the ordinal uses inside ch. 6 itself -- "un premier aperçu",
    # "le premier exemple non trivial", "un premier pas", "le premier avant-goût",
    # "les premiers entiers", "le premier membre" (the left-hand side!), "en
    # lisant les restes du dernier au premier". NB "ordre" is deliberately NOT in
    # this list: it would mask the middle of "équation différentielle linéaire du
    # premier ordre" and kill that term's own link.
    r'premiers?\s+(?:membres?|aperçus?|avant-goûts?|exemples?|pas|entiers)',
    r'dernier\s+au\s+premier',
    # "premier avec $n$" is coprimality, not primality ("premiers entre eux" is
    # the term that means it, and it keeps its link).
    r'premiers?\s+avec',
    # "corps": the field, 51 times out of 52. The one exception is the Cantor set
    # -- "un squelette dénombrable à l'intérieur d'un corps non dénombrable".
    r'corps\s+non\s+dénombrable',
    # "module": the modulus of a complex number, except the modulus of
    # continuity of ch. 13, which is a different object.
    r"module\s+(?:lipschitzien|d'oscillation)",
    # "application": the map, except where it means a *use* of a theorem.
    r"exercice\s+d'application", r'seule\s+application\s+de',
    # "linéaire": the linear map, except in these two fixed compounds, which name
    # something else. "application/forme/système/récurrence linéaire" are terms of
    # their own and win by being longer.
    r'algèbre\s+linéaire', r'combinaisons?\s+linéaires?',
    # "supplémentaire": the complementary subspace, except "un travail
    # supplémentaire" (ch. 22).
    r'travail\s+supplémentaire',
    # "conjugué": the complex conjugate, except the conjugate expression of
    # ch. 11, the algebraic conjugates of ch. 19 and group conjugation in ch. 23.
    # The trailing $ is a LOOKAHEAD -- never consumed.
    r'quantités\s+conjuguées', r'conjugués\s+bien\s+choisis',
    r'[Ll]es\s+conjugués(?=\s+\$)',
    # "image": the image of a map, except the picture of ch. 24 ("une image
    # complète à partir de trois calculs").
    r'une\s+image\s+complète',
    # "intégrale": the integral, except "la forme intégrale" (of Taylor's
    # remainder), where it is an adjective.
    r'forme\s+intégrale',
    # "ensemble": the set, except "dans leur ensemble" / "dans un ensemble" (as a
    # whole).
    r'dans\s+(?:leur|un)\s+ensemble',
    # "intérieur": the topological interior -- written "l'intérieur $\mathring
    # A$", "d'intérieur vide", "un point intérieur à $I$". "à l'intérieur du /
    # de la / des ..." is the ordinary preposition ("roulant à l'intérieur du
    # cercle unité", "à l'intérieur de la parenthèse"); "l'intérieur de $A$" is
    # NOT matched by this, and no $ is consumed.
    r"l'intérieur\s+d(?:u|es|e\s+la|'un)\b",
    r'boucles?\s+intérieures?', r'[Dd]éveloppement\s+intérieur',
]
