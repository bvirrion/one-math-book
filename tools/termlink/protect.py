"""Spans of a source file that must never be touched.

Everything a link would break: math, comments, macro arguments, environment
names and their key arguments (wrapping a term inside \\begin{solution}{exo:...}
once blew up the build).

Deliberately NOT protected, because links are wanted there: tabular bodies (a
grade book puts real prose in its cells, and Book 5 links two terms inside a
table row), omfigure captions (Book 5 has 27 links in captions), and method
bodies (imperative prose -- exactly where a young reader needs the link).

Writing a pattern (here or in a book's EXTRA_PROTECT): NEVER CONSUME A `$`.
The whole list is one alternation scanned left to right, so a pattern that eats
an opening $ leaves the inline-math rule pairing the *closing* $ with the next
formula's opening one -- and from there every span is masked inside out for the
rest of the file. It reports no error; the link count just quietly collapses
(one such pattern cost Book 3 a thousand links before it was noticed). Match a
trailing $ with a lookahead, never with a literal.
"""
import re

MATH_ENVS = (r'align\*?|alignat\*?|equation\*?|gather\*?|multline\*?|aligned|'
             r'cases|dcases|subequations|tikzpicture|array|matrix|pmatrix|'
             r'bmatrix|Bmatrix|vmatrix|Vmatrix|smallmatrix|psmallmatrix|'
             r'bsmallmatrix|verbatim|lstlisting|axis|scope')

GROUP = r'(?:[^{}]|\{[^{}]*\})'      # a brace group, one level of nesting

BASE_PROTECT = [
    # A comment runs to end of LINE. The whole list is compiled with re.S, so
    # `%.*` would run to end of FILE -- and a line-final % is the standard way
    # to kill the space after a tikzpicture, so that one % silently swallowed
    # the rest of the chapter (it did, in 90 of 354 files). \% is not a comment.
    r'(?<!\\)%[^\n]*',
    r'\$\$.*?\$\$', r'(?<!\\)\$(?:\\.|[^$\\])*\$',
    # (?<!\\) or the row break \\[4pt] reads as the start of display math and
    # masks everything up to the next real \] -- 3.4 KB of prose in
    # parts/bachelor-1/02-counting.tex alone.
    r'(?<!\\)\\\[.*?\\\]',
    r'\\begin\{(' + MATH_ENVS + r')\}.*?\\end\{\1\}',
    # the second argument takes a brace group too: an \omterm display of
    # quoti\"{e}nt that this does not match would be re-wrapped on every run
    r'\\(?:label|index|cref|Cref|ref|eqref|input|ominput|ominputsol|hyperref'
    r'|href|hypertarget|hyperlink|omterm|texorpdfstring)\{[^{}]*\}(?:\{' + GROUP + r'*\})?',
    # a heading may nest \texorpdfstring{}{} or \ref{}; without the nesting the
    # heading is not masked and the link ends up in the contents and the
    # running head, where it has no business being
    r'\\(?:chapter|section|subsection|part)\*?\{' + GROUP + r'*\}',
    # a defining \emph{term}\index{...} is never linked: inside the definition
    # of "outer measure", the inner word "measure" must not link away.
    r'\\emph\{' + GROUP + r'*\}\s*\\index\{' + GROUP + r'*\}',
    # a braced optional title -- \begin{theorem}[{Ideals of $K[X]$}] -- must be
    # taken whole, or the guard stops at the first ] and leaves an odd number of
    # $ behind, which desynchronises inline-math masking for the rest of the file
    r'\\begin\{[a-zA-Z*]+\}\[(?:\{[^{}]*\}|[^\]{}])*\]',
    # one level of nesting, so a column spec \begin{tabular}{>{\bfseries}l} is
    # masked whole
    r'\\begin\{[a-zA-Z*]+\}\{' + GROUP + r'*\}',
    r'\\(?:begin|end)\{[a-zA-Z*]+\}',
]


def masker(extra=()):
    rx = re.compile("|".join(list(BASE_PROTECT) + list(extra)), re.S)

    def mask(s):
        m = bytearray(len(s))
        for mt in rx.finditer(s):
            for i in range(mt.start(), mt.end()):
                m[i] = 1
        return m

    return mask
