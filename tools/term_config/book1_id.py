"""Book 1 -- id (Indonesian). Curation only; the rules live in tools/termlink/.

Every key is optional: anything left out falls back to the defaults in
tools/link_defined_terms.py. School book, spiral curriculum, so AMBIG_POLICY is
"nearest-preceding": a term re-defined in grade 4 and again in grade 6 links to
whichever definition the reader has already met.

This is a curation, not a translation of book1_en.py -- the Indonesian traps
are not the English ones:

* "sisi" is the busiest word in the book (677 uses): a side of a polygon, a
  face of a solid, a side of an equation, and "di sisi lain". It is harvested
  as the solid's face (def:g5:solids:def) and would be wrong nearly everywhere.
* "garis" is the ordinary word for any line, including "garis bilangan" (the
  number line, a different object) and "garis pandang". The compounds a child
  can genuinely forget -- "ruas garis", "garis sumbu", "garis berat",
  "garis sejajar", "garis tegak lurus" -- keep their own links.
* "setengah" is the everyday word: "setengah putaran", "setengah bola",
  "setengah lingkaran", "setengah jam". The fraction sense is a minority.
* "siku-siku", "sama kaki", "sama sisi" are only ever fragments of the
  compounds "sudut siku-siku", "segitiga siku-siku", "segitiga sama kaki",
  "segitiga sama sisi", which carry the links themselves.
* "membagi" is the plain verb ("membagi dua", "membagi kuenya"); the
  arithmetic relation is carried by "habis dibagi" and "pembagi".
* "bayangan" means image AND shadow AND optical image: the shadow of a stick
  in grade 7, the pinhole image in grade 9. Kept SOFT, so it links only in
  the chapter that defines it (parts/grade-6/id/06), where every use is the
  reflection.
* Book 2 paid for this one: a CAPITALISED display is a separate harvest entry
  and bypasses STOP, so every stoplisted word is listed in both cases.
"""

# Heads of Indonesian result-names: "aturan kosinus", "sifat distributif",
# "ketaksamaan segitiga" are named results, not defined terms.
NOT_A_TERM = ("teorema", "lema", "sifat", "kaidah", "ketaksamaan", "rumus",
              "kriteria", "asas", "aturan", "hukum", "paradoks", "soal")

# Never linked: in this book these words are ordinary Indonesian far more often
# than they are the term whose definition happened to introduce them.
# Both cases of every entry: the harvest keys on the literal display string.
STOP = {
    "sisi", "Sisi",
    "garis", "Garis",
    "sudut", "Sudut",
    "setengah", "Setengah",
    "membagi", "Membagi",
    "bayangan", "Bayangan",
    # fragments of compounds that carry the link themselves
    "siku-siku", "Siku-siku",
    "sama kaki", "Sama kaki",
    "sama sisi", "Sama sisi",
    # ---- the furniture ---------------------------------------------------
    # Real definitions (a child meets them in Kelas 1-6), but by the time they
    # are used they are the everyday furniture of the page: linking each one
    # turns the geometry exercises solid blue. The compounds survive:
    # "sudut siku-siku", "segitiga siku-siku", "segitiga sama kaki",
    # "akar kuadrat", "sudut bertolak belakang", "sumbu simetri".
    "persegi", "Persegi",
    "persegi panjang", "Persegi panjang",
    "segitiga", "Segitiga",
    "lingkaran", "Lingkaran",
    # ---- the homographs of the style card, §4 ----------------------------
    "luas", "Luas",              # area / wide
    "skala", "Skala",            # scale of a map / a scale to weigh with
    "rata-rata", "Rata-rata",    # the mean / on average
    "kelas", "Kelas",            # a group of three digits / a school class
    # Listed for the record: these never reach the harvest in this book (they
    # occur only inside compounds), but a later chapter must not resurrect
    # them silently.
    "kali", "bagi", "naik", "turun", "titik", "prima",
}

# Linked mid-sentence, not sentence-initially: "Bulatkan ke persepuluhan"
# opens an instruction, it is not a use of the term.
NO_CAPITAL = {"bulatkan"}

# Manual {term: label}; overrides every rule. Kept small.
EXTRA = {
    # single-word \index{} keys are skipped by the index-only harvest (it
    # requires a space), and my displays are the -nya forms, so the bare
    # nouns need declaring by hand.
    "gradien": "prop:g9:linfunc:affinegraph",
    "penampang": "prop:g9:solids:sections",
    # the definitions open their sentence, so only the capitalised display
    # was harvested; the lower-case verb is the form the book actually uses.
    "membulatkan": "def:g4:numbers:round",
    "menjabarkan": "def:g9:algebra:expand",
    # the book says "bulatkan"/"dibulatkan" far more often than the
    # dictionary form the definition registered
    "bulatkan": "def:g4:numbers:round",
    "dibulatkan": "def:g4:numbers:round",
}

# STOP is deliberately *soft*: a stoplisted word is kept out of the global
# vocabulary but still links inside the chapter that defines it. For most of
# the words above that is not wanted either, so they are hard-dropped as well.
# These are the exceptions -- ordinary language everywhere in the book *except*
# in their own chapter, where every single use is the term:
SOFT = {
    "kelas", "Kelas",          # parts/grade-4/id/01: the groups of three digits
    "luas", "Luas",            # parts/grade-4/id/08, grade-6/id/07
    "skala", "Skala",          # parts/grade-7/id/05: every use is the map scale
    "rata-rata", "Rata-rata",  # parts/grade-9/id/09: the statistical mean
    "bayangan", "Bayangan",    # parts/grade-6/id/06: every use is the reflection
}

DROP = set(STOP) - SOFT

DERIVED = {
    # the grade-2 definition names the quantity "kapasitas"; from grade 8 on
    # the prose calls a tank's capacity its "daya tampung", which is what an
    # Indonesian reader expects there.
    "kapasitas": ["daya tampung"],
}
PRIMARY_OK = set()
AMBIG_POLICY = "nearest-preceding"   # a spiral curriculum re-defines its terms
MAX_TERM_WORDS = 5
MAX_TERM_CHARS = 40

# Spans no link may enter: the uses where a good term means something else.
# NB: every space here is \s+ -- the sources wrap at 72 columns, and a phrase
# split across two lines slips past a literal space and the link lands anyway.
EXTRA_PROTECT = [
    # "sisa": the everyday "what is left", not the remainder of a division.
    # Indonesian uses one word where English alternates remainder / the rest /
    # what remains, so the arithmetic sense keeps its link and these do not.
    r'[Ss]isa\s+soalnya',
    r'[Ss]isa(?:nya)?\s+diterima\s+tanpa\s+bukti',
    r'[Ss]isa\s+(?:uang|voucer|ruang|penungguan|jatah|potongan)',
    r'[Ss]isanya\s+(?:berjalan|jelas|masih|berupa|membelah)',
    r'menyimpan\s+sisanya',
    r'mengerjakan\s+sisanya',
    r'[Ss]isa\s+ini\b',
    r'[Ss]isanya:\s+(?=\$)',      # lookahead: never consume the opening $
    # "balok": the building blocks of a number, not a cuboid
    r'balok\s+pembangun',
    # "jumlah": the plain "amount/number of", not the sum of the definition
    r'jumlah\s+seluruhnya',
    # "volume": the books of this series, not the content of a solid
    r'volume\s+di\s+tingkat\s+universitas',
    # "kubus": the power and the unit, not the solid
    r'meter\s+kubik', r'sentimeter\s+kubik',
    # "kecepatan": the road-sign speed limit is still the term, but the
    # chapter title of the series cross-reference is not
    r'[Kk]ecepatan\s+cahaya',
]
