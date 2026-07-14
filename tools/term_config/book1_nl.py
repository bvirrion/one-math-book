"""Book 1 -- nl. Curation only; the rules live in tools/termlink/.

Every key is optional: anything left out falls back to the defaults in
tools/link_defined_terms.py (empty sets, AMBIG_POLICY "drop").

Dutch writes its compounds solid, and the harvester will not link "hoek" inside
"driehoek" -- so the compound nouns (getallenlijn, geodriehoek, grondvlak) are
harmless here, and Dutch needs fewer guards than French. What it does need
guarding against is the adverb: "even" is both *even* (the number) and *equally*
("even ver", "even waarschijnlijk", "de kosten even delen"), and "net" is both
the net of a solid and *just* ("net na het eerste cijfer").
"""

# Never linked: ordinary Dutch, or a word this book uses in another sense far
# more often than in the sense its definition gives it.
STOP = {
    # "het vlak" is the plane, "een vlak veld" is flat, "het grondvlak" is the
    # base: the face of a solid is a minority of the singular's uses. The
    # plural "vlakken" is always the faces, and keeps its link.
    "vlak",
    # "de omgekeerde" is the *converse of a theorem* in fourteen of its
    # nineteen uses (Pythagoras, Thales, the midpoint theorem) and the
    # reciprocal of a fraction in the other five. STOP is soft, so the
    # reciprocal still links inside the chapter that defines it
    # (grade-8/02-fractions-all-operations) and nowhere else -- which is
    # exactly the split we want.
    "omgekeerde",
    # the protractor's scale, the pan of a balance, the scale of a graph axis:
    # "op de schaal", "aan de ene schaal", "de verkeerde schaal gelezen". Only
    # a third of the uses are def:g7:prop:scale, and "schaalfactor" keeps its
    # own link.
    "schaal",

    # ---- the furniture ----------------------------------------------------
    # Real definitions, but the everyday furniture of the page: they occur in
    # nearly every sentence of every geometry chapter, and linking each one
    # turns the exercises solid blue. The compounds a child can really forget
    # survive and carry the link: "rechte hoek", "rechthoekige driehoek",
    # "gelijkbenige driehoek", "gelijkzijdige driehoek", "vierkantswortel",
    # "overstaande hoeken", "symmetrieas".
    "hoek", "driehoek", "vierkant", "rechthoek", "cirkel",
}

# Linked mid-sentence, not sentence-initially: "Afronden op het dichtstbijzijnde
# duizendtal" is an instruction, not a use of the noun.
NO_CAPITAL = {"afronden"}

EXTRA = {}            # manual {term: label}; overrides every rule


# STOP is deliberately *soft*: a stoplisted word is kept out of the global
# vocabulary but still links inside the chapter that defines it. For most of the
# words above that is not wanted either, so they are hard-dropped as well. These
# are the exceptions -- words that are ordinary language everywhere in the book
# *except* in their own chapter, where every single use is the term:
SOFT = {
    "omgekeerde",  # parts/grade-8/02: the reciprocal of a fraction, all four uses
    "vlak",        # parts/grade-2/05 and grade-5/07: the face of a solid
    "schaal",      # parts/grade-7/05: the scale of a map or model
}

DROP = (set(STOP) - SOFT) | {
    # \emph{waarde van een cijfer hangt af van zijn plaats}\index{plaatswaarde}
    # in parts/grade-6/nl/01: the sentence is not a term.
    "waarde van een cijfer hangt af van zijn plaats",
}

DERIVED = {}          # {base: [other forms]}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"   # a spiral curriculum re-defines its terms
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans no link may enter: the uses where a good term means something else.
EXTRA_PROTECT = [
    # NB: every space here is \s+ -- the sources wrap at 72 columns, and a
    # phrase split across two lines slips past a literal space.
    # "even": the adverb, "equally" -- "beide even ver", "even waarschijnlijk",
    # "een andere snede werkt even goed", "de kosten even delen".
    r'even\s+(?:ver|goed|waarschijnlijk|veel|groot|lang|snel|zwaar|duur)\b',
    r'\bdelen\b[^.]{0,45}\beven\b', r'\beven\b[^.]{0,12}\bdelen\b',
    # "net": the adverb, "just" -- "net na het eerste cijfer", "net voorbij"
    r'net\s+(?:na|onder|boven|voorbij|eronder|erboven|als|zoals|zo)\b',
    # "rest": the verb ("het rest om ze te vermenigvuldigen")
    r'\brest\s+om\b',
    # "balk": the fraction strip of parts/grade-6/nl/03 and the bar of a figure,
    # not the solid ("breuken van dezelfde balk", "de steel onder de balk")
    r'dezelfde\s+balk', r'hele\s+balk', r'balk\s+in\s+\$\d+\$\s+gelijke\s+delen',
    r'onder\s+de\s+balk', r'uiteinde\s+van\s+de\s+balk',
    # prose cross-references to the other books of the series
    r'High\s+School-volume',
]
