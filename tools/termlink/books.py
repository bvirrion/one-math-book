"""Which files a book is made of, and in which order.

The order matters: a term is never linked in a chapter that comes *before* the
chapter defining it. Within one year the two-digit filename prefix would do, but
a book spans several years (Book 1 has nine), and grade-3/01 and grade-9/01 are
both "chapter 01". So the sequence is read from the book's own entry file, which
is the same order the reader meets the chapters in.
"""
import os
import re

ENTRY = {
    1: "one_math_book_1_primary_middle_school.tex",
    2: "one_math_book_2_high_school.tex",
    3: "one_math_book_3_university_year_1.tex",
    4: "one_math_book_4_university_year_2.tex",
    5: "one_math_book_5_university_year_3.tex",
}

LANGS = {1: ("en", "fr", "nl", "es", "pt", "hi"), 2: ("en", "fr", "nl", "es", "pt", "hi"),
         3: ("en", "fr", "nl", "es", "pt", "hi"), 4: ("en", "fr", "nl", "es", "pt", "hi"),
         5: ("en", "fr", "nl", "es", "pt", "hi")}


def years(book):
    """The year directories the entry file inputs, in reading order."""
    src = open(ENTRY[book], encoding="utf8").read()
    return re.findall(r'\\input\{parts/([^/}]+)/part\}', src)


def chapters(book):
    """[(year, stem)] in reading order, from each parts/<year>/part.tex.

    Grade years include with \\ominput{<year>}{<stem>} (language-aware), the
    bachelor years with a plain \\input{parts/<year>/<stem>}.
    """
    out = []
    for year in years(book):
        part = open("parts/%s/part.tex" % year, encoding="utf8").read()
        for m in re.finditer(
                r'\\ominput\{([^}]+)\}\{([^}]+)\}'
                r'|\\input\{parts/([^/}]+)/([^}/]+)\}', part):
            y, stem = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
            if stem == "part":
                continue
            out.append((y, stem))
    return out


def files(book, lang):
    """[(path, seq, is_solutions)] for the whole book in the given language.

    seq is the chapter's position in the book (1-based), shared by a chapter and
    its solutions file. A translated file that does not exist is skipped rather
    than falling back to English: linking the English body under --lang fr would
    put French links in a file the French book never inputs.
    """
    out = []
    for seq, (year, stem) in enumerate(chapters(book), start=1):
        if lang == "en":
            course = "parts/%s/%s.tex" % (year, stem)
            sols = "parts/%s/solutions/%s.tex" % (year, stem)
        else:
            course = "parts/%s/%s/%s.tex" % (year, lang, stem)
            sols = "parts/%s/solutions/%s/%s.tex" % (year, lang, stem)
        for path, is_sol in ((course, False), (sols, True)):
            if os.path.exists(path):
                out.append((path, seq, is_sol))
    return out
