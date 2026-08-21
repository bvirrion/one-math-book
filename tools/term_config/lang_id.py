"""Indonesian morphology.

Indonesian is the simplest morphology this repository has had to describe, and
the simplicity is the point: a noun marks neither number nor gender, and an
adjective agrees with nothing. "bilangan prima" is both "a prime number" and
"prime numbers", so -- unlike es/pt/fr, where the tail had to go on every word
of a phrase -- there is no plural tail to place at all.

What does attach is the enclitic possessive/definite -nya, and it attaches
once, to the END of the phrase ("turunannya", "himpunan penyelesaiannya"),
never to each word. Hence TAIL_ON_EVERY_WORD = False.

Two known, accepted gaps, both the same shape as the gender gap es/pt carry:

  * Plural by reduplication. "bilangan-bilangan" is reached anyway, because
    HEAD lets a hyphenated first element in front of a single-word term. A
    MULTI-word term reduplicates its head noun ("bilangan-bilangan prima")
    and HEAD is empty for multi-word terms, so those forms are unreachable;
    declare the handful a book actually uses in that book's DERIVED.
  * Affixed derivations (konvergen -> kekonvergenan, turun -> penurunan,
    diferensiabel -> keterdiferensialan). DERIVE is off: the Indonesian
    ke-/-an circumfix is regular enough to generate but not regular enough to
    generate SAFELY, so declare the ones that occur in EXTRA or DERIVED.
"""
WORD_TAIL = r'(?:-?nya)?'
TAIL_ON_EVERY_WORD = False
HEAD = r'(?:[^\W\d_]+-)?'
DERIVE = False
