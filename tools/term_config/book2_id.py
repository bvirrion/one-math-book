"""Book 2 -- id. Curation only; the rules live in tools/termlink/.

Indonesian is written in the same alphabet as the English canon and has no
inflection to speak of, so the harvest is unusually clean: what it does need
is a stoplist for the words that are ordinary language here (the homographs
of the style card) and a DERIVED table for the ke-/-an derivations and the
reduplicated plurals that lang_id.py deliberately does not generate.

School book, spiral curriculum: nearest-preceding policy, like book2_en.
"""

# Result names: Indonesian uses the "X <nama>" phrase order, so the bare head
# noun is enough -- there is no solid compounding to substring-match into
# (contrast Dutch). "hukum" alone is kept out: "hukum peluang total" and
# "hukum bilangan besar" are results, not definitions.
NOT_A_TERM = ("teorema", "lema", "akibat", "ketaksamaan", "rumus",
              "kaidah", "aturan", "asas", "identitas", "hukum", "paradoks",
              "soal", "sifat")

STOP = {
    # ---- the homograph list of the style card -------------------------------
    # "bidang" is the plane of geometry, the face of a solid, and the ordinary
    # "bidang empat"/"di bidang ini"; the chapter that defines it still links.
    "bidang",
    # "kali" = times / occasion; "bagi" = for / divide; both are function words
    # long before they are operations.
    "kali", "bagi",
    # "sisi" = side of a polygon, face of a cube, and "di sisi lain".
    "sisi",
    # "luas" = area, but also the adjective "wide/broad".
    "luas",
    # "naik"/"turun" are the monotonicity words and the ordinary verbs
    # ("harganya naik", "turun dari bus").
    "naik", "turun",
    # "titik" = point, but also full stop, and the head of a dozen phrases.
    "titik",
    # "modus" = the statistical mode and ordinary "modus operandi".
    "modus",
    # parity of an integer -- and "bilangan genap", "banyaknya suku ganjil".
    # The harvested sense is the parity of a *function*; the phrases
    # "fungsi genap"/"fungsi ganjil" survive.
    "genap", "ganjil",
    # "deret" = series, but "deret ukur"/"deret hitung" are the defined ones.
    "deret",
    # "rata-rata" is the arithmetic mean, the sample mean, the expectation and
    # the adverb "rata-rata orang"; chapter locality keeps the right one.
    "rata-rata",
    # "skala" = scale of a drawing, of an axis, of a measurement.
    "skala",
    # ---- ordinary emphasis harvested from inside definitions ---------------
    "semua", "tegas", "serentak", "tepat",
    # ---- adjectives that name a chapter, not a notion -----------------------
    # "aritmetika"/"geometri" as the branches (the arithmetic chapter, a
    # geometric argument); "barisan aritmetika"/"deret ukur" survive as phrases.
    "aritmetika", "geometri",
    # "jumlah" is the sum of numbers, of a series, of roots, of vectors.
    "jumlah",
    # "gabungan" is the union of sets and the ordinary "gabungan linear".
    "gabungan",
    # "terbatas" is the participle ("selang terbatas", "daerah terbatas") far
    # more often than the bounded-sequence property.
    "terbatas",
    # "jangkauan" is the statistical range; elsewhere "daerah hasil" is used,
    # but the word also means ordinary reach ("di luar jangkauan").
    "jangkauan",
    # "peluang" is the probability measure and the everyday "kemungkinan".
    "peluang",
}
# NB a STOPped word is still linked inside the chapter that defines it, which
# is exactly what makes "bidang", "titik" and "rata-rata" behave.

NO_CAPITAL = set()   # Indonesian imperatives take -lah/-kan ("Hitunglah",
                     # "Faktorkanlah") and never collide with a term; the
                     # sentence-initial "Median", "Modus", "Ragam" are nouns.

EXTRA = {}           # manual {term: label}; overrides every rule

DROP = {
    # The name of \cref{thm:g12:contdist:memoryless}, not a defined notion.
    # English writes it as one word ("memorylessness") and the index-only
    # harvest skips single words; the Indonesian phrase has a space, so it
    # slips in and has to be dropped by hand.
    "ketiadaan ingatan",
}

# lang_id.py generates neither the ke-/-an circumfix nor the reduplicated
# plural of a multi-word term; declare the ones this book actually uses.
DERIVED = {
    "fungsi": ["fungsi-fungsi"],
    "bilangan prima": ["bilangan-bilangan prima"],
    "vektor": ["vektor-vektor"],
    "peubah acak": ["peubah-peubah acak"],
    "himpunan bagian": ["himpunan-himpunan bagian"],
}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"   # a spiral curriculum re-defines its terms
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans no link may touch. (Headings are masked by the shared rule.)
EXTRA_PROTECT = [
    # "akar kuadrat"/"akar pangkat tiga" are the square/cube roots, not the
    # roots of a polynomial.
    r'\bakar\s+kuadrat\w*',
    r'\bakar\s+pangkat\s+tiga\b',
    # "bagi" as the preposition "for", and "membagi" as plain division prose.
    r'\bbagi\s+(?:setiap|semua|sebarang|tiap|kedua|para|sang)\b',
    # "kali" as "times/occasion", never the multiplication term.
    r'\b(?:sekali|dua kali|tiga kali|berkali-kali|kali ini|tiap kalinya)\b',
    # "titik" as the punctuation mark ("tiga angka di belakang titik").
    r'\bdi\s+belakang\s+titik\b',
    # "turun" as "derive/descend" in the mathematical-writing sense.
    r'\bditurunkan\s+dari\b',
]
