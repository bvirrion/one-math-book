"""Book 3 -- id. Curation only; the rules live in tools/termlink/.

Indonesian shares the canon's alphabet and has essentially no inflection, so
the harvest is clean; what it needs is (a) the result-name heads filtered out
through NOT_A_TERM, (b) the style card's homograph stoplist -- LISTED IN BOTH
CASES, because a capitalised display is a separate harvest entry that bypasses
STOP -- and (c) hand declarations for the ke-/-an derivations lang_id.py
refuses to generate.

The Book 3 traps are its own, not Book 4's:

* "peta" is the image of a linear map (ch. 20) and the ordinary word for a
  map/chart ("peta kontur", "peta konturnya" in ch. 25).
* "titik" opens a dozen phrases -- titik asal, titik tetap, titik kritis,
  titik singular, titik runcing, titik sentuh -- and is itself a definition
  in the topology chapter.
* "bidang" is the geometric plane (ch. 24-25) and never the algebraic field,
  which is "lapangan" throughout.
* "tetap" is "constant" and the everyday "remains/stays": "titik tetap",
  "tetapan", "tetap saja".
* "rank" and "trace" are deliberately English (style card, sec. 7.3); they are
  ordinary tokens to the harvester and behave normally.

University book: AMBIG_POLICY = "drop", like book3_en/fr/nl.
"""

# Indonesian result-names are "X <nama>" phrases, so the bare head noun filters
# them (no solid compounding to substring-match into, unlike Dutch). "aturan"
# is the Indonesian "regle": aturan rantai, aturan Cramer, aturan hasil bagi.
NOT_A_TERM = ("teorema", "lema", "akibat", "ketaksamaan", "rumus",
              "kaidah", "aturan", "asas", "identitas", "paradoks",
              "kriteria", "sifat", "prinsip", "soal", "masalah",
              "hukum")

STOP = {
    # ---- the style card's homograph list, IN BOTH CASES ---------------------
    # (rule 4b.1: a capitalised display is a separate harvest entry)
    "bidang", "Bidang",          # the geometric plane / field of study
    "kali", "Kali",              # times, occasion -- a function word first
    "bagi", "Bagi",              # "for" as often as "divide"
    "sisi", "Sisi",              # side, face, "di sisi lain", "dua sisi"
    "pangkat", "Pangkat",        # exponent, but also rank/degree in prose
    "akar", "Akar",              # root of a polynomial / square root
    "titik", "Titik",            # point, full stop, head of a dozen phrases
    "tetap", "Tetap",            # constant / "tetap saja", "titik tetap"
    "luas", "Luas",              # area and the adjective "broad"
    "naik", "Naik", "turun", "Turun",   # monotonicity and the plain verbs
    "prima", "Prima",            # prime and "kondisi prima"
    "modus", "Modus",            # statistical mode and "modus operandi"
    "deret", "Deret",            # series, but also "berderet"
    "rata-rata", "Rata-rata",    # the mean and the adverb "on average"
    "peta", "Peta",              # image of a map and an ordinary map/chart
    "orde", "Orde",              # order of a pole/group and "orde besar"
    "skala", "Skala",            # scale of an axis, of a drawing
    # -nya forms of the same words (rule 4b.2: -nya in a display is a new term)
    "bidangnya", "kalinya", "sisinya", "titiknya", "akarnya", "petanya",
    "ordenya", "skalanya", "deretnya", "luasnya", "tetapnya", "pangkatnya",
    # ---- ordinary emphasis harvested from inside definitions ----------------
    "jumlah", "Jumlah",          # sum of numbers, of a series, of vectors
    "hasil kali", "Hasil kali",  # product of numbers, of matrices, of sets
    "gabungan", "Gabungan",      # union of sets and "gabungan linear"
    "terbatas", "Terbatas",      # the participle far more often than bounded
    "tegas", "serentak", "tepat", "semua",
    # ---- adjectives that are ordinary mathematical language ----------------
    # "normal" is the normal vector of a curve (ch. 24), the normal equations
    # (ch. 25) and the ordinary adjective.
    "normal", "Normal", "normalnya",
    # "setara" is the everyday "the following are equivalent".
    "setara", "Setara", "setaranya",
    # "aljabar" is the branch of mathematics (aljabar linear, an algebraic
    # argument) far more often than the algebra-over-a-field structure.
    "aljabar", "Aljabar", "aljabarnya",
    # "reguler" is a regular point of a curve (ch. 24) and the ordinary word.
    "reguler", "Reguler", "regulernya",
    # "hingga" is the finite SET of ch. 2 and, far more often, the ordinary
    # "berdimensi hingga", "jumlah hingga", "sampai/hingga" -- EN stops
    # "finite" for the same reason. 166 wrong-sense links before this.
    "hingga", "Hingga", "hingganya",
    # "urutan" is the order RELATION of ch. 1 and the everyday "urutan ini",
    # "dalam urutan menurun" (EN: "order" is not linked in that sense either).
    "urutan", "Urutan", "urutannya",
    # "kutub" is the POLE of a rational fraction (ch. 9) and the POLAR of
    # ch. 3/24/25 ("kurva kutub", "koordinat kutub", "bentuk kutub"): STOP is
    # soft, so ch. 9 keeps every link and the polar chapters lose 13 wrong ones.
    "kutub", "Kutub", "kutubnya", "Kutubnya",
    # ch. 5 defines the characteristic polynomial of a linear ODE; ch. 21-22
    # use the phrase for a matrix -- a different object (EN stops it too).
    "polinomial karakteristik", "Polinomial karakteristik",
}
# NB a STOPped word is still linked inside the chapter that defines it -- which
# is what lets "titik" and "peta" behave chapter by chapter.

NO_CAPITAL = set()   # Indonesian imperatives take -lah/-kan ("Hitunglah",
                     # "Buktikanlah") and never collide with a term.

EXTRA = {
    # the definition emphasises a compound ("\emph{kontinu di $x_0 \in I$}",
    # "\emph{dapat diturunkan di $x_0 \in I$}"), so the bare adjective -- the
    # form the rest of the book actually uses -- is never harvested. EN carries
    # the same two declarations for "continuous" / "differentiable".
    "kontinu":            "def:b1:continuity:continuous",
    "dapat diturunkan":   "def:b1:derivative:def",
    # \index{konstanta Euler} sits in exercise 12, *before* the weekend problem
    # that defines gamma, so the nearest preceding statement is an unrelated
    # example about telescoping. Point it at the problem, as EN does.
    "konstanta Euler":    "pb:b1:series:1",
    # "sifat" heads Indonesian result-names and is in NOT_A_TERM, which also
    # filters the one genuine "sifat X" TERM of the book.
    "sifat Archimedes":   "thm:b1:reals:archimedes",
    # same reason: "hukum" is a result-name head, and the tower law is the one
    # genuine "hukum X" term of the book (EN: "tower law", pb:b1:findim:1).
    "hukum menara":       "pb:b1:findim:1",
    # EN's "supplementary (subspace)" is a noun in Indonesian ("pelengkap"),
    # which the definition never emphasises on its own. "pelengkap ortogonal"
    # (ch. 23) is a longer term and still wins where it applies.
    "pelengkap":          "def:b1:vspaces:sum",
    "saling melengkapi":  "def:b1:vspaces:sum",
}

DROP = {
    # ---- ordinary Indonesian in this register (EN drops the same words) -----
    # "argumen" is the reasoning ("argumen yang sama menunjukkan", "argumen
    # diagonal") far more often than the argument of a complex number.
    "argumen", "Argumen", "argumennya", "Argumennya",
    # "simetri" is "lewat kesetangkupan"/"secara simetri", not the involution
    # of ch. 20 (the term that earns a link there is "proyeksi").
    "simetri", "Simetri", "simetrinya", "Simetrinya",
    # "langsung" is "perhitungan langsung", "secara langsung", "sinar langsung"
    # -- the direct SUM keeps its link through "jumlah langsung".
    "langsung", "Langsung", "langsungnya", "Langsungnya",
    # bare "kritis"; "titik kritis" survives and is the term.
    "kritis", "Kritis", "kritisnya",
    # bare "transenden": the adjective, and mis-targeted (EN drops it).
    "transenden", "Transenden", "transendennya",
    # "serupa" is the everyday "perhitungan yang serupa"; EN links neither the
    # bare "similar" nor "similar matrices".
    "serupa", "Serupa", "serupanya",
    "matriks yang serupa", "Matriks yang serupa",
    # ---- names of results: the point is to link definitions, not theorems ---
    # (NOT_A_TERM only filters the index-only harvest; these arrive through
    # \emph{...}\index{...} and have to be dropped by hand -- exactly as in
    # book3_en.py.)
    "teorema Kummer", "Teorema Kummer",
    "rumus Legendre", "Rumus Legendre",
    "hukum De Morgan", "Hukum De Morgan",
    "ketaksamaan Ptolemeus", "Ketaksamaan Ptolemeus",
    "persamaan fungsional Cauchy", "Persamaan fungsional Cauchy",
    "persamaan fungsional", "Persamaan fungsional",
    # "permutasi kacau" (derangement) is two words in Indonesian and one in
    # English, so the index-only harvest -- which needs a space -- picks it up
    # here and not there. EN links it nowhere; match that.
    "permutasi kacau", "Permutasi kacau", "permutasi kacaunya",
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
    # "titik" as the decimal point.
    r'\bdi\s+belakang\s+titik\b',
    # "turun" as "derive" in the mathematical-writing sense.
    r'\bditurunkan\s+dari\b',
    # "penutup" as "closing/concluding", not the topological closure: the
    # solutions' recurring "Inti gagasan penutupnya" is EN's "The closing
    # insight" (25 wrong-sense links before this).
    r'[Ii]nti\s+gagasan\s+penutupnya',
    # "membagi ... dengan/oleh" is the division OPERATION, not the relation.
    r'\bdengan\s+membagi\w*\b',
]
