"""Book 1 -- fr. Curation only; the rules live in tools/termlink/.

Every key is optional: anything left out falls back to the defaults in
tools/link_defined_terms.py (empty sets, AMBIG_POLICY "drop").

The traps are not the English ones. "droite" is both the line and the right-hand
side, "reste" is both the remainder and the verb "to be left over", "echelle" is
both the scale of a map and the ladder that leans against the wall in every
Pythagoras exercise. Each word was read in context before being kept or dropped.

Terms harvested from parts/grade-1..3/fr are spelled with TeX escapes
(carr\\'e, z\\'ero), those from parts/grade-4..9/fr in UTF-8 (carré): a word
defined in both trees is harvested twice, so both spellings appear below.
"""

# Never linked: ordinary French, or a word this book uses in another sense far
# more often than in the sense its definition gives it.
STOP = {
    # "a droite" (to the right) is as common as the geometric line; and the
    # useful phrases -- "droites parallèles", "droites perpendiculaires",
    # "angle droit" -- keep their own links.
    "droite",
    # "les côtés opposés du rectangle", "l'angle opposé à l'hypoténuse":
    # geometry owns this word. The opposite of a relative number is a small
    # minority of the uses, and "opposés par le sommet" keeps its own link.
    "opposé", "opposés",
    # def:g4:numbers:classes is the group of three digits; grade 7 groups data
    # into (statistical) classes and grade 8 averages two school classes.
    "classes",
    # the ladder, not the map: "une échelle de $5$ m s'appuie contre un mur",
    # "l'échelle est l'hypoténuse", plus "l'échelle qui commence à $0$" (the
    # axis of a graph) and "chaque pas de l'échelle des unités". More than half
    # the uses are not def:g7:prop:scale; "facteur d'échelle" keeps its link.
    "échelle",

    # ---- the furniture ----------------------------------------------------
    # Real definitions, but the everyday furniture of the page: they occur in
    # nearly every sentence of every geometry chapter, and linking each one
    # turns the exercises solid blue. The compounds a child can really forget
    # survive and carry the link: "angle droit", "triangle rectangle",
    # "triangle isocèle", "triangle équilatéral", "racine carrée",
    # "angles alternes-internes", "angles opposés par le sommet".
    "angle", "triangle", "rectangle", "cercle", "carré", "carr\\'e",
}

# Linked mid-sentence, not sentence-initially: "Arrondir $8.276$ à l'unité" is
# an instruction, not a use of the noun.
NO_CAPITAL = {"arrondir"}

EXTRA = {}            # manual {term: label}; overrides every rule


# STOP is deliberately *soft*: a stoplisted word is kept out of the global
# vocabulary but still links inside the chapter that defines it. For most of the
# words above that is not wanted either, so they are hard-dropped as well. These
# are the exceptions -- words that are ordinary language everywhere in the book
# *except* in their own chapter, where every single use is the term:
SOFT = {
    "échelle",   # parts/grade-7/05: every use there is the scale of a map or model
    "classes",   # parts/grade-4/01: the groups of three digits
}

DROP = (set(STOP) - SOFT) | {
    # \emph{valeur d'un chiffre dépend de sa place}\index{valeur de position}
    # in parts/grade-6/fr/01: the sentence is not a term.
    "valeur d'un chiffre dépend de sa place",
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
    # "reste": the verb, which this book uses constantly ("il reste $7$
    # cerises", "elle reste vraie", "chaque chiffre reste dans sa colonne",
    # "il reste à les multiplier"). The noun -- "$52 \div 6 = 8$ reste $4$",
    # "le reste est plus petit que le diviseur" -- keeps its link.
    r'(?:ne|il|elle|on|qui)\s+reste',
    r'reste\s+(?:ouvert|vrai|dans|(?:\\`a|à)\s)',
    # "cube": "$a$ au cube" is the operation, not the solid
    r'au\s+cube',
    # "pair": "paires" is the plural of *paire* (a pair), not of *pair* (even)
    r'\bpaires\b',
    # "face": "quelqu'un face à toi", "le côté ouvert fait toujours face"
    r'face\s+(?:\\`a|à|au)\b', r'fait\s+(?:\w+\s+)?face',
    # "cube": the unit of volume, not the solid
    r'(?:m|d|c|mill)?(?:è|\\`e)tres?\s+cubes?',
    # "divise": the ordinary verb ("on divise $29$ par $6$", "divise par $2$")
    r'[Oo]n\s+divise', r'divise[sz]?\s+par', r'divise-le',
    # prose cross-references to the other books of the series
    r"volumes?\s+de\s+lyc(?:é|\\'e)e",
]
