"""Book 5 -- id. Curation only; the rules live in tools/termlink/.

Indonesian shares the canon's alphabet and inflects almost nothing, so the
harvest is clean.  What it needs is (a) the Indonesian result-name heads in
NOT_A_TERM, (b) the style card's homograph stoplist LISTED IN BOTH CASES
(a capitalised display is a separate harvest entry that bypasses STOP), and
(c) the handful of ke-/-an derivations lang_id.py refuses to generate.

University book: AMBIG_POLICY = "drop", like book5_en/fr/nl.
"""

# Indonesian result-names are "<head> <nama>" phrases, so the bare head noun
# filters them: teorema Baire, lema Zorn, ketaksamaan Holder, rumus Stirling.
# "hukum" is in the list for "hukum bilangan besar"; the two laws English does
# link ("tower law", "zero--one law") come back through EXTRA below.
NOT_A_TERM = ("teorema", "lema", "akibat", "ketaksamaan", "rumus",
              "kaidah", "aturan", "asas", "identitas", "paradoks",
              "kriteria", "sifat", "prinsip", "soal", "masalah", "hukum")

STOP = {
    # ---- the English config's stoplist, term by term ------------------------
    "semua", "Semua", "beberapa", "Beberapa", "total", "Total",
    "rupa", "Rupa", "seksi", "Seksi", "langsung", "Langsung",
    "sederhana", "Sederhana", "stabil", "Stabil", "setara", "Setara",
    "bulat", "Bulat", "indeks", "Indeks", "konvergen", "Konvergen",
    "kejadian", "Kejadian", "padat", "Padat", "normal", "Normal",
    "maksimal", "Maksimal", "pokok", "Pokok", "utama", "Utama",
    "radikal", "Radikal", "kandungan", "Kandungan",
    "karakteristik", "Karakteristik", "invarian", "Invarian",
    "terbatas", "Terbatas", "aksi", "Aksi", "basis", "Basis",
    "derajat", "Derajat", "bebas", "Bebas", "terpisahkan", "Terpisahkan",
    "tertutup", "Tertutup", "eksak", "Eksak", "kompak", "Kompak",
    "prima", "Prima", "tak tereduksi", "Tak tereduksi",
    "primitif", "Primitif", "hasil kali", "Hasil kali",
    "kuosien", "Kuosien", "subruang", "Subruang", "lintasan", "Lintasan",
    "batas", "Batas", "interior", "Interior",
    # ---- the style card's homograph list, IN BOTH CASES (rule 4b.1) --------
    "bidang", "Bidang", "kali", "Kali", "bagi", "Bagi", "sisi", "Sisi",
    "pangkat", "Pangkat", "akar", "Akar", "titik", "Titik",
    "tetap", "Tetap", "luas", "Luas", "naik", "Naik", "turun", "Turun",
    "modus", "Modus", "deret", "Deret", "rata-rata", "Rata-rata",
    "peta", "Peta", "orde", "Orde", "skala", "Skala",
    # -nya forms of the same words (rule 4b.2: -nya in a display is a new term)
    "bidangnya", "kalinya", "sisinya", "titiknya", "akarnya", "petanya",
    "ordenya", "skalanya", "deretnya", "luasnya", "batasnya", "petanya",
    # ---- ordinary Indonesian harvested from inside definitions -------------
    "aljabar", "Aljabar", "aljabarnya",   # the BRANCH far more often than the
                                          # algebra-over-a-field structure
    "pusat", "Pusat", "pusatnya",         # centre of a group vs. "limit pusat",
                                          # "berpusat", "titik pusat"
    "distribusi", "Distribusi",           # the law of a variable vs. "fungsi
                                          # distribusi", "distribusi Gauss"
    "peluang", "Peluang",                 # the measure vs. the everyday word
    "jumlah", "Jumlah", "gabungan", "Gabungan",
    "tegas", "serentak", "tepat",
    # "sekawan" is BOTH the associate of ring theory (ch. 2) and the ordinary
    # "conjugate" (complex conjugate, harmonic conjugate, conjugate exponents):
    # a homograph English does not have.  Stopped, so it links only in ch. 2.
    "sekawan", "Sekawan", "sekawannya",
    # English writes "a.e." (stoplisted there) where Indonesian spells the
    # phrase out; without this it links 100 times against English's 2.
    "hampir di mana-mana", "Hampir di mana-mana",
    # Indonesian writes both "Euclidean" and "Euclid's" as "Euclid", so the
    # ring-theory adjective cannot be told from "geometri Euclid", "lema
    # Euclid", "tolok ukur Euclid".  Stopped, so it links only in ch. 2.
    "Euclid", "Euclidnya",
    "seragam", "Seragam", "mulus", "Mulus", "terurut", "Terurut",
}
# NB a STOPped word is still linked inside the chapter that defines it -- which
# is what lets "titik" and "orde" behave chapter by chapter.

NO_CAPITAL = set()   # Indonesian imperatives take -lah/-kan and never collide.

EXTRA = {
    # rule 7: a term whose head word is in NOT_A_TERM is unreachable, and
    # "aturan" is a substring of "keteraturan".  English links all three.
    "hukum menara": "thm:b3:galois:tower",
    "hukum nol--satu": "thm:b3:probability:zeroone",
    "keteraturan ukuran Lebesgue": "thm:b3:measure:regularity",
}

DROP = {
    # English never links "ruler and compass": it reaches the harvester only
    # through the corollary's \index entry.
    "penggaris dan jangka",
}

# lang_id.py generates neither the ke-/-an circumfix nor the reduplicated
# plural of a multi-word term; declare the ones this book actually uses.
DERIVED = {
    "kontinu": ["kekontinuan"],
    "terukur": ["keterukuran"],
    "holomorfik": ["keholomorfikan"],
    "lengkap": ["kelengkapan"],
    "homeomorfisma": ["homeomorfik"],
    "isomorfisma": ["isomorfik"],
    "meromorfik": ["kemeromorfikan"],
    "terorientasikan": ["keterorientasian"],
    "terselesaikan": ["keterselesaian"],
    "swa-adjoin": ["keswa-adjoinan"],
    "ekuikontinu": ["keekuikontinuan"],
    "topologi": ["topologis"],
    "transitif": ["secara transitif"],
}

# overloaded words whose first sense dominates the book, so they may be linked
# outside the chapter that pins them down (mirrors the English PRIMARY_OK).
# "batas" is deliberately absent: unlike English "boundary" it is also the
# ordinary "bound" (batas atas, batas gabungan, batas ekor), and a primary
# link sent 25 of its 40 occurrences to the wrong sense in chapters 22--23.
PRIMARY_OK = {"kompak", "tertutup", "lintasan", "interior", "tak tereduksi"}

AMBIG_POLICY = "drop"          # the university convention (books 3, 4, 5)
MAX_TERM_WORDS = None
MAX_TERM_CHARS = None

EXTRA_PROTECT = [
    # "bagi" as the preposition "for", never the division operation.
    r'\bbagi\s+(?:setiap|semua|sebarang|sembarang|tiap|kedua|para)\b',
    # "kali" as "times/occasion".
    r'\b(?:sekali|dua kali|tiga kali|berkali-kali|kali ini|setiap kalinya)\b',
    # "titik" as the decimal point.
    r'\bdi\s+belakang\s+titik\b',
    # "ukuran" as plain size, never the measure of chapter 9.
    r'\bukuran\s+(?:cuplikan|sampel|abjad|langkah|matriks|blok)\b',
]
