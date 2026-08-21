"""Book 4 -- id. Curation only; the rules live in tools/termlink/.

Indonesian shares the canon's alphabet and has essentially no inflection, so
the harvest is clean; what it needs is (a) the result-name heads filtered out
of NOT_A_TERM, (b) the style card's homograph stoplist -- LISTED IN BOTH CASES,
because a capitalised display is a separate term that bypasses STOP -- and
(c) hand declarations for the ke-/-an derivations lang_id.py refuses to
generate.

University book: AMBIG_POLICY = "drop", like book4_en/fr/nl.
"""

# Indonesian result-names are "X <nama>" phrases, so the bare head noun filters
# them (no solid compounding to substring-match into, unlike Dutch). "aturan"
# is the Indonesian "regle": aturan rantai, aturan Cramer, aturan hasil bagi.
NOT_A_TERM = ("teorema", "lema", "akibat", "ketaksamaan", "rumus",
              "kaidah", "aturan", "asas", "identitas", "paradoks",
              "kriteria", "sifat", "prinsip", "soal", "masalah")

STOP = {
    # ---- the style card's homograph list, IN BOTH CASES ---------------------
    # (rule 4b.1: a capitalised display is a separate harvest entry)
    "bidang", "Bidang",          # plane / field of study / "di bidang ini"
    "kali", "Kali",              # times, occasion -- a function word first
    "bagi", "Bagi",              # "for" as often as "divide"
    "sisi", "Sisi",              # side, face, "di sisi lain"
    "pangkat", "Pangkat",        # exponent, but also rank/degree in prose
    "akar", "Akar",              # root of a polynomial / square root / origin
    "titik", "Titik",            # point, full stop, head of a dozen phrases
    "tetap", "Tetap",            # "fixed" and the ordinary "tetap saja"
    "luas", "Luas",              # area and the adjective "broad"
    "naik", "Naik", "turun", "Turun",   # monotonicity and the plain verbs
    "prima", "Prima",            # prime and "kondisi prima"
    "modus", "Modus",            # statistical mode and "modus operandi"
    "deret", "Deret",            # series, but also "deret ukur"/"berderet"
    "rata-rata", "Rata-rata",    # mean, expectation, and the adverb
    "peta", "Peta",              # image of a map and an ordinary map
    "orde", "Orde",              # order of a group/pole and "orde besar"
    "skala", "Skala",            # scale of an axis, of a drawing
    # -nya forms of the same words (rule 4b.2: -nya in a display is a new term)
    "bidangnya", "kalinya", "sisinya", "titiknya", "akarnya", "petanya",
    "ordenya", "skalanya", "deretnya", "luasnya",
    # ---- ordinary emphasis harvested from inside definitions ----------------
    "jumlah", "Jumlah",          # sum of numbers, of a series, of vectors
    "hasil kali", "Hasil kali",  # product of numbers, of sets, of groups
    "gabungan", "Gabungan",      # union of sets and "gabungan linear"
    "terbatas", "Terbatas",      # the participle far more often than bounded
    "peluang", "Peluang",        # the measure and the everyday "kemungkinan"
    "tegas", "serentak", "tepat", "semua",
    # ---- adjectives that are ordinary mathematical language ----------------
    # "konvergen" is the general word for convergent (series, sequences,
    # integrals, products); the definition it reaches is the CONVERGENCE OF AN
    # IMPROPER INTEGRAL, so outside chapter 9 every link is a wrong sense.
    "konvergen", "Konvergen", "konvergennya",
    # "normal" is normal convergence (ch. 8), a normal endomorphism (ch. 13),
    # the principal normal of a curve (ch. 18) and the ordinary adjective.
    "normal", "Normal", "normalnya",
    # "setara" is the everyday "the following are equivalent"; the harvested
    # sense is the equivalence of NORMS.
    "setara", "Setara", "setaranya",
    # "aljabar" is the branch of mathematics (linear algebra, an algebraic
    # argument) far more often than the algebra-over-a-field structure.
    "aljabar", "Aljabar", "aljabarnya",
}
# NB a STOPped word is still linked inside the chapter that defines it -- which
# is what lets "titik" and "orde" behave chapter by chapter.

NO_CAPITAL = set()   # Indonesian imperatives take -lah/-kan ("Hitunglah",
                     # "Buktikanlah") and never collide with a term.

EXTRA = {}

DROP = {
    # bare "tertutup" is the closed SET of chapter 4; the term it reaches is the
    # EXACT form of chapter 20 ("bentuk tertutup" keeps that link and is enough).
    "tertutup", "Tertutup", "tertutupnya",
    # Result-names and weekend-problem notions the English tree never links;
    # each reaches the harvester through an \emph{...}\index{...} pair, which
    # bypasses NOT_A_TERM.
    "gejala Gibbs",         # ex:b2:fourier:zetafourodd -- never linked in EN
    "titik penyeimbang",    # pb:b2:affine:1 -- EN "centerpoint" not harvested
    "fungsi Euler",         # prop:b2:structures:cyclic -- EN "Euler's totient
                            # function" exists but is never cross-linked
    "rumus Jacobi", "Rumus Jacobi",        # pb:b2:diffcalc:1 -- a named formula
    "teorema Korovkin", "Teorema Korovkin",  # pb:b2:funcseq:1 -- a named theorem
    "kesamaan Parseval",    # thm:b2:fourier:parseval -- a named identity
    # the sign of a permutation: EN never links bare "signature" either (it is
    # also the signature of a quadratic form, ch. 12).
    "tanda permutasi", "Tanda permutasi", "tanda permutasinya",
    # bare "signatur" is the signature of a quadratic form (Sylvester, ch. 12)
    # AND, in ch. 1, the sign of a permutation: EN never links the bare word.
    "signatur", "Signatur", "signaturnya", "Signaturnya",
}

# lang_id.py generates neither the ke-/-an circumfix nor the reduplicated
# plural of a multi-word term; declare the ones this book actually uses.
DERIVED = {}

PRIMARY_OK = set()
AMBIG_POLICY = "drop"          # the university convention (books 3, 4, 5)
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

EXTRA_PROTECT = [
    # "bagi" as the preposition "for", never the division operation.
    r'\bbagi\s+(?:setiap|semua|sebarang|tiap|kedua|para)\b',
    # "kali" as "times/occasion".
    r'\b(?:sekali|dua kali|tiga kali|berkali-kali|kali ini|tiap kalinya)\b',
    # "hasil kali" inside the fixed phrase "hasil kali Cauchy" (a construction
    # on series, not the product of numbers).
    r'\bhasil\s+kali\s+Cauchy\b',
    # "titik" as the decimal point.
    r'\bdi\s+belakang\s+titik\b',
    # "turun" as "derive" in the mathematical-writing sense.
    r'\bditurunkan\s+dari\b',
    # "seragam" = drawn from the UNIFORM LAW (ch. 20-23), or uniform
    # CONTINUITY / uniformity in a parameter -- never uniform convergence.
    # (The English config carries the same list for "uniformly".)
    r'\bseragam\s+acak\b',
    r'\bacak\s+seragam\b',
    r'\b(?:dipilih|ditarik|diambil|dicuplik|terambil|tercuplik|memilih'
    r'|menarik|mengambil|mencuplik|mengetik)\s+(?:secara\s+)?seragam\b',
    r'\b(?:pencuplikan|penarikan|pengambilan|pemilihan|cuplikan|ukuran'
    r'|bobot|hukum|distribusi|peluang|huruf|peringkat)'
    r'\s+(?:yang\s+(?:tak\s+)?)?seragam\b',
    r'\b[Jj]umlah\w*\s+(?:yang\s+)?seragam\b',
    r'\b(?:mungkin|pernah|persis|setimbang|pertamanya|bolanya)\}?\s+seragam\b',
    r'\bbebas\s+dan\s+seragam\b',
    r'\bluas\s+yang\s+seragam\b',
    r'\bberhukum\s+seragam\b',
    r'\b[Kk]ekontinuan\s+seragam\b',
    r'\bkontinu\s+seragam\b',
    r'\bseragam\s+di\s+antara\b',
    r'\bsecara\s+seragam\s+dalam\b',
    r'\bseragam\)',
    r'(?:pintu|mainan|kotak|dadu|bola)\w*,\s*secara\s+seragam',
    r'\bsecara\s+seragam\.\s+Tunjukkan\b',
    r'\bsecara\s+seragam,\s+di\b',
    # "mutlak" inside "nilai mutlak" (absolute value), not absolute convergence.
    r'\b(?:ber)?nilai\s+mutlak\w*',
]
