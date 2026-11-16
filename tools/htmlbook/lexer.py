"""Parse a One Math Book chapter (or solutions) file into a node tree.

The book sources are disciplined by construction — every macro and
environment lives in styles/onemath.sty and CONTRIBUTING.md forbids
chapter-local definitions — so this is a targeted parser for that closed
vocabulary, not a general TeX engine.  Any command or environment outside
the vocabulary raises ParseError with file:line context: the converter
must fail loudly rather than silently drop book content.

Node shapes (plain dicts, `t` = type):

Blocks:
  {"t":"para",     "inl":[...]}
  {"t":"dmath",    "tex":str}
  {"t":"section",  "inl":[...], "star":bool}
  {"t":"env",      "kind":str, "title":[...]|None, "label":str|None,
                   "body":[blocks], "difficulty":int|None, "sol_key":str|None}
  {"t":"list",     "kind":"itemize"|"enumerate", "resume":bool,
                   "items":[[blocks]]}
  {"t":"figure",   "tikz":str, "caption":[...]}
  {"t":"table",    "colspec":str, "header":[cells]|None, "rows":[[cells]]}
                   (a cell is an inline list)

Inlines:
  {"t":"text",  "s":str}
  {"t":"math",  "tex":str}
  {"t":"emph",  "inl":[...], "index":str|None}
  {"t":"bold",  "inl":[...]}
  {"t":"term",  "label":str, "inl":[...]}
  {"t":"cref",  "label":str}
"""

import re
from pathlib import Path

STATEMENT_KINDS = (
    "definition", "theorem", "proposition", "lemma", "corollary",
    "method", "example", "notation", "remark",
)
# Environments whose bodies are parsed recursively as blocks.
BLOCK_ENVS = STATEMENT_KINDS + ("proof", "exercise", "problem", "solution",
                                 "interviewq", "question")
# Interview books (styles/ivbook.sty, quant 18-20): run-in leads of an answer
# -> (lead text, is there a first argument in italics?).
IV_RUNINS = {"iqwrong": ("Classic wrong answer", False),
             "iqwhy": ("Why it matters", False),
             "iqfollow": ("Follow-up", True)}
LIST_ENVS = ("itemize", "enumerate")
# Quant-book boxes (styles/onequant.sty) -> number of mandatory arguments:
# dated{YYYY-MM}{title}, strategyfile{title}, predictorcard{title}.
QUANT_BOXES = {"dated": 2, "strategyfile": 1, "predictorcard": 1,
               "tutorial": 0, "build": 0}
# Chemistry- and Earth-book asides (styles/onechemistry.sty, oneearth.sty),
# unnumbered: recall (no argument), inthefield/inthelab/history ([optional
# title]), safety ({GHS pictograms} in chemistry, no argument in Earth).
ASIDE_BOXES = ("recall", "inthefield", "inthelab", "history", "safety")
# Pictures that are not tikzpicture environments (chemistry books): a
# chemfig reaction scheme, a molecular-orbital diagram, the periodic table,
# a lone structure. Compiled like a tikzpicture, from their raw source.
CHEM_PICTURE = re.compile(
    r"\\begin\{(tikzpicture|circuitikz|MOdiagram)\}"
    r"|\\(schemestart|omperiodictable|chemfig|setchemfig"
    r"|tdplotsetmaincoords)(?![a-zA-Z])")


class ParseError(Exception):
    pass


class Cursor:
    def __init__(self, text, filename):
        self.s = text
        self.i = 0
        self.filename = filename

    def line(self, i=None):
        return self.s.count("\n", 0, self.i if i is None else i) + 1

    def err(self, msg):
        ctx = self.s[self.i:self.i + 60].replace("\n", "\\n")
        raise ParseError(f"{self.filename}:{self.line()}: {msg} (at: {ctx!r})")


def strip_comments(text):
    """Remove unescaped %-comments (keep the newline). A comment-only line
    inside a picture goes whole: TeX reads no blank line there, while a \\par
    breaks \\addplot and the option lists."""
    text = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}",
                  lambda m: re.sub(r"^[ \t]*%.*\n", "", m.group(0), flags=re.M),
                  text, flags=re.S)
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == "\\" and i + 1 < n:
            out.append(text[i:i + 2])
            i += 2
        elif c == "%":
            j = text.find("\n", i)
            i = n if j < 0 else j
        else:
            out.append(c)
            i += 1
    return "".join(out)


def drop_print_tweaks(text):
    """Line-breaking and range tweaks the translations add for print, and
    the \\qty{3} slip: LaTeX takes the next token as the unit and prints
    the same thing, so only a number is meant. An unbraced \\foreach runs to
    the next `;`, past its \\edef…\\temp: brace it, or the next \\addplot (the
    2,176-point cyclone scatter) is drawn once per value."""
    text = re.sub(r"(\\foreach\s*\\\w+\s+in\s*\{[^{}]*\}\s*)"
                  r"(\\edef\\(\w+)\{(?:[^{}]|\{[^{}]*\})*\}\\\3\b)",
                  r"\1{\2}", text)
    text = re.sub(r"\\begingroup\\emergencystretch=[\d.]+em\\relax\s*"
                  r"(.*?)\\par\\endgroup", r"\1" + "\n\n", text, flags=re.S)
    # (\tabcolsep: a tighter table for the print page)
    text = re.sub(r"\\setlength\{\\(?:emergencystretch|tabcolsep)\}"
                  r"\{[^{}]*\}%?", "", text)
    text = re.sub(r"\{\\sisetup\{range-phrase=\{\\text\{--\}\}\}"
                  r"(\\\[.*?\\\])\}", r"\1", text, flags=re.S)
    return re.sub(r"\\qty\{([^{}]*)\}(?!\s*\{)", r"\1", text)


def read_group(cur):
    """Read a balanced {...} group; skips leading whitespace (an argument
    may start on the next source line). Returns the group content."""
    s = cur.s
    while cur.i < len(s) and s[cur.i] in " \n\t":
        cur.i += 1
    if cur.i >= len(s) or s[cur.i] != "{":
        cur.err("expected '{'")
    depth, start = 0, cur.i + 1
    i = cur.i
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                cur.i = i + 1
                return s[start:i]
        i += 1
    cur.err("unbalanced '{'")


def read_optional(cur):
    """Read a balanced [...] group if present ('{' groups may nest inside)."""
    s = cur.s
    if cur.i >= len(s) or s[cur.i] != "[":
        return None
    depth_sq, depth_br = 0, 0
    start = cur.i + 1
    i = cur.i
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth_br += 1
        elif c == "}":
            depth_br -= 1
        elif c == "[" and depth_br == 0:
            depth_sq += 1
        elif c == "]" and depth_br == 0:
            depth_sq -= 1
            if depth_sq == 0:
                cur.i = i + 1
                return s[start:i]
        i += 1
    cur.err("unbalanced '['")


CMD_RE = re.compile(r"\\([a-zA-Z]+)\s*")

# Text symbols of the quant books (textcomp / onequant.sty).
QUANT_SYMBOLS = {
    "pounds": "£", "textyen": "¥", "textdegree": "°", "textmu": "µ",
    "textquotedbl": '"', "textvisiblespace": "␣",
    # chemistry books
    "AA": "\u00c5", "textperthousand": "\u2030",
    # Earth books
    "textquoteleft": "\u2018", "textquoteright": "\u2019",
    "textcopyright": "\u00a9", "textbackslash": "\\",
}
# An italic aside group: {\small\itshape\color{omIq} ...}
ITSHAPE_GROUP = re.compile(r"\{\s*(?:\\(?:small|footnotesize)\s*)?\\itshape\b")
ITSHAPE_SWITCHES = re.compile(
    r"^\s*(?:\\(?:small|footnotesize)\s*)?\\itshape\b\s*"
    r"(?:\\color\{[^{}]*\}\s*)?")


def find_inline_math_end(s, start):
    """Index of the `$` closing the inline math opened at s[start] — the
    first unescaped `$` at brace depth 0 (LaTeX re-enters math inside
    \\text{...}, e.g. $\\sum_{\\text{$k$ even}}$). Returns -1 if none."""
    depth = 0
    i = start + 1
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == "$" and depth == 0:
            return i
        i += 1
    return -1


def find_env_end(cur, name):
    """Return (body, end_pos) for the environment `name` starting after its
    \\begin (cursor already past \\begin{name}[opt]); handles same-name
    nesting; leaves cursor after \\end{name}."""
    s = cur.s
    depth = 1
    i = cur.i
    begin_pat = "\\begin{" + name + "}"
    end_pat = "\\end{" + name + "}"
    start = i
    while i < len(s):
        b = s.find(begin_pat, i)
        e = s.find(end_pat, i)
        if e < 0:
            cur.err(f"missing \\end{{{name}}}")
        if 0 <= b < e:
            depth += 1
            i = b + len(begin_pat)
            continue
        depth -= 1
        if depth == 0:
            body = s[start:e]
            cur.i = e + len(end_pat)
            return body
        i = e + len(end_pat)
    cur.err(f"missing \\end{{{name}}}")


def split_top_level(body, sep_cmd, filename):
    """Split env body on a top-level command (\\item) — outside math, braces
    and nested environments. Returns list of chunks (first chunk = preamble
    before the first separator)."""
    chunks, buf = [], []
    i, n = 0, len(body)
    depth_br = 0
    env_depth = 0
    in_math = False
    sep = "\\" + sep_cmd
    while i < n:
        c = body[i]
        if c == "\\":
            if body.startswith("\\begin{", i):
                env_depth += 1
            elif body.startswith("\\end{", i):
                env_depth -= 1
            if (not in_math and depth_br == 0 and env_depth == 0
                    and body.startswith(sep, i)
                    and not body[i + len(sep):i + len(sep) + 1].isalpha()):
                chunks.append("".join(buf))
                buf = []
                i += len(sep)
                continue
            buf.append(body[i:i + 2])
            i += 2
            continue
        if c == "$":
            in_math = not in_math
        elif not in_math:
            if c == "{":
                depth_br += 1
            elif c == "}":
                depth_br -= 1
        buf.append(c)
        i += 1
    chunks.append("".join(buf))
    return chunks


def column_alignments(colspec, filename):
    """tabular colspec -> one of "l"/"c"/"r" per column: p{}/m{}/b{}/X
    columns are left-aligned text; @{} >{} <{} and | are layout only;
    *{n}{spec} repeats."""
    spec = colspec
    while True:
        m = re.search(r"\*\{(\d+)\}\{([^{}]*)\}", spec)
        if not m:
            break
        spec = spec[:m.start()] + m.group(2) * int(m.group(1)) + spec[m.end():]
    spec = re.sub(r"[@<>!]\{(?:[^{}]|\{[^{}]*\})*\}|\|", "", spec)
    spec = re.sub(r"[pmb]\{(?:[^{}]|\{[^{}]*\})*\}|X", "l", spec)
    spec = re.sub(r"\s+", "", spec)
    if not re.fullmatch(r"[lcr]+", spec):
        raise ParseError(f"{filename}: unsupported tabular colspec "
                         f"{colspec!r}")
    return list(spec)


def count_stars(opt):
    """Difficulty option like `$\\star$` / `$\\star\\star\\star$` -> 1..3."""
    return opt.count("\\star")


class Parser:
    def __init__(self, filename, text, iv=None):
        self.filename = filename
        # interview books: English UI word -> the edition's word
        # (LangStrings.iv_strings; empty for English)
        self.iv = iv or {}
        self.chapter_title = None      # inline list
        self.chapter_label = None
        # \setchemfig{...} in force (chemistry books): prefixed to the
        # source of every chemfig picture that follows it
        self.chem_setup = ""
        text = drop_print_tweaks(strip_comments(text))
        self.cur = Cursor(text, filename)

    # ---------------------------------------------------------------- blocks

    def parse(self):
        """Parse the whole file; returns list of blocks."""
        return self.parse_blocks(self.cur.s, self.cur)

    def parse_blocks(self, body, outer_cur=None):
        cur = Cursor(body, self.filename)
        if outer_cur is not None:
            cur = outer_cur if body is outer_cur.s else cur
        blocks = []
        parbuf = []  # raw tex accumulated for the current paragraph

        def flush():
            raw = "".join(parbuf).strip()
            parbuf.clear()
            if raw:
                inl = self.parse_inlines(raw)
                if inl:
                    blocks.append({"t": "para", "inl": inl})

        s = cur.s
        while cur.i < len(s):
            c = s[cur.i]
            if c == "\n":
                # blank line = paragraph break
                m = re.match(r"\n\s*\n", s[cur.i:])
                if m:
                    flush()
                    cur.i += m.end()
                else:
                    parbuf.append(" ")
                    cur.i += 1
                continue
            if c == "$":
                # consume the whole inline-math segment: a \begin{cases}
                # inside $...$ must not be mistaken for a block environment
                end = find_inline_math_end(s, cur.i)
                if end < 0:
                    cur.err("unbalanced $")
                parbuf.append(s[cur.i:end + 1])
                cur.i = end + 1
                continue
            if c == "\\":
                if s.startswith("\\begin{", cur.i):
                    flush()
                    blocks.append(self.parse_env(cur))
                    continue
                if s.startswith("\\[", cur.i):
                    flush()
                    end = s.find("\\]", cur.i + 2)
                    if end < 0:
                        cur.err("missing \\]")
                    blocks.append(
                        {"t": "dmath", "tex": s[cur.i + 2:end].strip()})
                    cur.i = end + 2
                    continue
                if s.startswith(("\\chapter{", "\\chapter["), cur.i):
                    flush()
                    cur.i += len("\\chapter")
                    read_optional(cur)   # [short title]: toc and running head
                    self.chapter_title = self.parse_inlines(read_group(cur))
                    continue
                m = re.match(r"\\(sub)?section(\*?)\{", s[cur.i:])
                if m:
                    flush()
                    cur.i += len("\\section") + len(m.group(1) or "") \
                        + len(m.group(2))
                    title = read_group(cur)
                    blocks.append({"t": "subsection" if m.group(1) else "section",
                                   "inl": self.parse_inlines(title),
                                   "star": bool(m.group(2))})
                    continue
                m = re.match(r"\\(sfield|bfield|paragraph)\s*\{", s[cur.i:])
                if m:
                    # \sfield{Name} / \bfield{Name} (quant strategy files and
                    # build boxes): a new paragraph led by "Name." in bold;
                    # \paragraph{Title.} is the same run-in heading
                    flush()
                    cur.i += m.end() - 1
                    name = read_group(cur)
                    if m.group(1) == "paragraph":
                        parbuf.append("\\textbf{" + name + "}\\ ")
                    else:
                        parbuf.append("\\omfieldlead{" + name + "}\\ ")
                    continue
                m = re.match(r"\\iqlookfor\s*\{", s[cur.i:])
                if m:
                    # interview-question solutions: "What the interviewer is
                    # looking for: …" (its own paragraph in print)
                    flush()
                    cur.i += m.end() - 1
                    blocks.append({"t": "lookfor",
                                   "inl": self.parse_inlines(read_group(cur))})
                    continue
                m = re.match(r"\\(iqwrong|iqwhy|iqfollow)\s*\{", s[cur.i:])
                if m:
                    # interview books: "Classic wrong answer. …" and friends,
                    # each its own paragraph in print
                    flush()
                    cur.i += m.end() - 1
                    lead, has_ask = IV_RUNINS[m.group(1)]
                    lead = self.iv.get(lead, lead)
                    ask = self.parse_inlines(read_group(cur)) if has_ask \
                        else None
                    blocks.append({"t": "ivrunin", "lead": lead, "ask": ask,
                                   "body": self.parse_blocks(read_group(cur))})
                    continue
                m = re.match(r"\\ivtestsection\s*\{", s[cur.i:])
                if m:
                    # interview books, timed tests: an unnumbered section
                    flush()
                    cur.i += m.end() - 1
                    name, count, minutes = [read_group(cur) for _ in range(3)]
                    blocks.append({"t": "section", "star": True,
                                   "inl": self.parse_inlines(
                                       f"Section {name} --- {count} questions, "
                                       f"{minutes} minutes")})
                    continue
                m = re.match(r"\\ivfamily\s*\{", s[cur.i:])
                if m:
                    # drill keys: "Family (items 3, 8). How to do them."
                    flush()
                    cur.i += m.end() - 1
                    name, items, how = [read_group(cur) for _ in range(3)]
                    parbuf.append(f"\\textbf{{{name}}} (items {items}). {how}")
                    flush()
                    continue
                m = re.match(r"\\ivround\s*\{", s[cur.i:])
                if m:
                    # played games: "Round 1." leads what the interviewer says
                    flush()
                    cur.i += m.end() - 1
                    parbuf.append(f"\\textbf{{{self.iv.get('Round', 'Round')} "
                                  f"{read_group(cur)}.}}\\ ")
                    continue
                m = re.match(r"\\ivsays\s*\{", s[cur.i:])
                if m:
                    cur.i += m.end() - 1
                    says = "\\textit{Interviewer:} ``#1''"
                    parbuf.append(self.iv.get(says, says)
                                  .replace("#1", read_group(cur)))
                    flush()
                    continue
                m = re.match(r"\\ivstop\b", s[cur.i:])
                if m:
                    flush()
                    cur.i += m.end()
                    blocks.append({"t": "ivstop"})
                    continue
                m = re.match(r"\\ivlookup\s*\{", s[cur.i:])
                if m:
                    flush()
                    cur.i += m.end() - 1
                    blocks.append(self.parse_iv_lookup(read_group(cur)))
                    continue
                m = re.match(r"\\omcode\s*\{", s[cur.i:])
                if m:
                    flush()
                    cur.i += m.end() - 1
                    blocks.append(self.parse_listing(cur))
                    continue
                m = re.match(r"\\(setchemfig|tdplotsetmaincoords)\s*\{",
                             s[cur.i:])
                if m:
                    # chemfig settings / tikz-3dplot view: they apply to
                    # the pictures that follow
                    cur.i += m.end() - 1
                    self.chem_setup += f"\\{m.group(1)}" + "".join(
                        "{" + read_group(cur) + "}"
                        for _ in range(2 if m.group(1)[0] == "t" else 1))
                    continue
                m = re.match(r"\\admitted\b", s[cur.i:])
                if m:
                    # zero-arg macro: a whole "Admitted at this level" proof
                    flush()
                    blocks.append({"t": "admitted"})
                    cur.i += m.end()
                    continue
                m = re.match(r"\\(footnotesize|small)\b\s*", s[cur.i:])
                if m:
                    # size switch (a quant table in a box): CSS owns sizing;
                    # trailing space consumed as a command's would be
                    cur.i += m.end()
                    continue
                m = re.match(r"\\(medskip|smallskip|bigskip|noindent|par"
                             r"|clearpage)\b",
                             s[cur.i:])
                if m:
                    # purely presentational in print; paragraph flow in HTML
                    if m.group(1) != "noindent":
                        flush()
                    cur.i += m.end()
                    continue
                m = re.match(r"\\phantomsection\s*\\label\{([^{}]*)\}",
                             s[cur.i:cur.i + 200])
                if m:
                    # Earth books: a term defined in the running text, the
                    # target of its \omterm links
                    flush()
                    blocks.append({"t": "anchor", "label": m.group(1)})
                    cur.i += m.end()
                    continue
                if s.startswith("\\label{", cur.i):
                    cur.i += len("\\label")
                    label = read_group(cur)
                    if self.chapter_label is None and not blocks \
                            and not "".join(parbuf).strip():
                        self.chapter_label = label
                    elif blocks and not "".join(parbuf).strip() \
                            and blocks[-1]["t"] in ("section", "subsection") \
                            and "label" not in blocks[-1]:
                        # \section{...}\label{sec:...}
                        blocks[-1]["label"] = label
                    else:
                        # a label placed late in an environment body (the
                        # style file's page-break workaround): surface it
                        # as a node for parse_env to attach; anywhere else
                        # the emitter fails loudly on it
                        flush()
                        blocks.append({"t": "label", "name": label})
                    continue
                # anything else: part of the running paragraph text
                parbuf.append(self.take_inline_atom(cur))
                continue
            parbuf.append(c)
            cur.i += 1
        flush()
        return blocks

    def take_inline_atom(self, cur):
        """Consume one inline-level backslash construct as raw text (validated
        later by parse_inlines) — used while accumulating a paragraph."""
        s = cur.s
        if s.startswith("$", cur.i):  # unreachable; math has no backslash lead
            pass
        m = CMD_RE.match(s, cur.i)
        if m:
            name = m.group(1)
            start = cur.i
            cur.i = m.end()
            # commands with brace groups: consume their groups too so a
            # nested \begin inside an argument can't fool the block scanner
            n_groups = {"omterm": 2, "cref": 1, "Cref": 1, "ref": 1,
                        "eqref": 1, "emph": 1, "textbf": 1, "index": 1,
                        "label": 1, "textsuperscript": 1, "footnote": 1,
                        "up": 1, "chaptermark": 1,
                        "texorpdfstring": 2, "hspace": 1, "rule": 2,
                        "texttt": 1, "rotatebox": 2, "multicolumn": 3, "underline": 1,
                        "textit": 1, "ensuremath": 1, "numrange": 2,
                        "textsubscript": 1,
                        "H": 1, "c": 1, "v": 1, "textsc": 1,
                        "text": 1, "textcolor": 2, "pageref": 1, "omve": 1,
                        "omlith": 1, "omwx": 1,
                        "path": 1, "si": 1, "money": 2,
                        "omfieldlead": 1,
                        "ce": 1, "pu": 1, "cip": 1, "termsym": 3, "kv": 3,
                        "chemfig": 1, "omorbs": 1, "babelsublr": 1,
                        "url": 1, "enlargethispage": 1, "markboth": 2,
                        "foreignlanguage": 2, "mbox": 1,
                        "shortstack": 1}.get(name, 0)
            if name in ("H", "c", "v") \
                    and (cur.i >= len(s) or s[cur.i] != "{"):
                n_groups = 0  # bare-letter accent form (\v S)
            out = [s[start:cur.i]]
            if name in ("omwx", "shortstack") \
                    and s[cur.i:cur.i + 1] == "[":
                # an optional argument kept with the command
                out.append("[" + read_optional(cur) + "]")
            for _ in range(n_groups):
                while cur.i < len(s) and s[cur.i] in " \n":
                    cur.i += 1
                out.append("{" + read_group(cur) + "}")
            return "".join(out)
        # escaped char like \, \\ \& \% \_ or "\ "
        out = s[cur.i:cur.i + 2]
        cur.i += 2
        return out

    def parse_listing(self, cur):
        """\\omcode{path}{first}{last}{caption}, optionally followed by
        \\label{lst:...}: lines first..last of a tested source file (quant
        books), read and highlighted by the emitter."""
        path = read_group(cur).strip()
        first = read_group(cur).strip()
        last = read_group(cur).strip()
        caption = read_group(cur)
        if not (first.isdigit() and last.isdigit()):
            cur.err(f"\\omcode line range {first!r}..{last!r} is not numeric")
        label = None
        m = re.match(r"[ \t]*\n?[ \t]*\\label\{", cur.s[cur.i:])
        if m:
            cur.i += m.end() - 1
            label = read_group(cur)
        return {"t": "listing", "path": path, "first": int(first),
                "last": int(last), "caption": self.parse_inlines(caption),
                "label": label}

    # ------------------------------------------------------------------ envs

    def parse_env(self, cur):
        s = cur.s
        cur.i += len("\\begin")
        name = read_group(cur)

        if name == "equation":
            # numbered display equation; the label (if any) becomes an
            # anchored \tag'd formula
            body = find_env_end(cur, "equation")
            label = None
            m = re.search(r"\\label\{([^{}]*)\}", body)
            if m:
                label = m.group(1)
                body = body[:m.start()] + body[m.end():]
            return {"t": "dmath", "tex": body.strip(), "label": label}
        if name == "equation*":
            return {"t": "dmath", "tex": find_env_end(cur, name).strip()}
        if name in ("align*", "gather*"):
            # display-math blocks; KaTeX renders them natively in display
            # mode, so keep the whole environment verbatim
            body = find_env_end(cur, name)
            return {"t": "dmath",
                    "tex": f"\\begin{{{name}}}" + body + f"\\end{{{name}}}"}
        if name == "multline*":
            # KaTeX has no multline: the same lines, centred
            body = find_env_end(cur, name)
            return {"t": "dmath",
                    "tex": "\\begin{gather*}" + body + "\\end{gather*}"}
        if name == "description":
            # \item[Label.] text -> a bullet with a bold lead-in
            chunks = split_top_level(find_env_end(cur, name), "item",
                                     self.filename)
            if chunks[0].strip():
                raise ParseError(
                    f"{self.filename}: text before first \\item in {name}")
            items = []
            for chunk in chunks[1:]:
                icur = Cursor(chunk, self.filename)
                lead = read_optional(icur)
                if lead is None:
                    icur.err("description \\item without a [label]")
                items.append(self.parse_blocks(
                    "\\textbf{" + lead + "} " + chunk[icur.i:].lstrip()))
            return {"t": "list", "kind": "itemize", "resume": False,
                    "items": items}
        if name == "ivtrains":
            # interview books: what a chapter trains, under its title; a
            # plain paragraph, so it also feeds the page description
            blocks = self.parse_blocks(find_env_end(cur, name))
            if len(blocks) != 1 or blocks[0]["t"] != "para":
                raise ParseError(
                    f"{self.filename}: ivtrains must be one paragraph")
            return {**blocks[0], "css": "om-iv-trains"}
        if name in ("ivdrillsheet", "ivdrillkey"):
            return self.parse_iv_drills(name, find_env_end(cur, name))
        if name == "omfigure":
            body = find_env_end(cur, "omfigure")
            return self.parse_figure(body)
        if name == "figure":
            read_optional(cur)  # float placement ([ht]...): print-only
            body = find_env_end(cur, "figure")
            return self.parse_figure(body, floated=True)
        if name == "center":
            body = find_env_end(cur, "center")
            if "\\begin{tabular}" not in body and CHEM_PICTURE.search(body):
                # a picture centred in the text (chemistry exercises): a
                # figure without caption
                pictures, rest = self.take_pictures(body)
                if self.FIGURE_SPACING.sub("", rest).strip():
                    # structures with their names set under them: one
                    # picture, as composed in print
                    pictures = ["\\centering\n" + self.chem_setup
                                + body.strip()]
                return {"t": "figure", "tikzs": pictures, "label": None,
                        "caption": []}
            if re.match(r"\s*\\begin\{tikzpicture\}", body):
                # a picture and, under it, its table (Earth books)
                pictures, rest = self.take_pictures(body)
                if "\\begin{tabular}" in rest:
                    table = self.parse_center(
                        re.sub(r"^(\s|\\smallskip\b|\\medskip\b)*", "", rest))
                    return {"t": "figure", "tikzs": pictures, "label": None,
                            "caption": [], "table": table}
            if "\\begin{tabular}" not in body \
                    and self.INCLUDEGRAPHICS.search(body):
                # a photo centred in a box (Earth books), caption optional
                return self.parse_figure(body)
            return self.parse_center(body)
        if name == "table":
            read_optional(cur)  # float placement: print-only
            return self.parse_table_float(find_env_end(cur, "table"))
        if name == "tabular":
            # a bare tabular (inside a quant box, after a size switch)
            start = cur.i - len("\\begin{tabular}")
            find_env_end(cur, "tabular")
            return self.parse_center(s[start:cur.i])
        if name in ("omsources", "tutsteps"):
            # quant lists: "Sources and further reading" (an itemize under
            # its heading) and tutorial steps ("Step N." labels)
            body = find_env_end(cur, name)
            chunks = split_top_level(body, "item", self.filename)
            if chunks[0].replace("\\sloppy", "").strip():
                raise ParseError(
                    f"{self.filename}: text before first \\item in {name}")
            return {"t": "list",
                    "kind": "itemize" if name == "omsources" else "steps",
                    "resume": False, "sources": name == "omsources",
                    "items": [self.parse_blocks(c) for c in chunks[1:]]}
        if name in QUANT_BOXES:
            # Earth books: \begin{dated}{2026}, the year alone and no title
            year_only = name == "dated" \
                and re.match(r"\s*\{\d{4}\}", s[cur.i:]) is not None
            n_args = 1 if year_only else QUANT_BOXES[name]
            args = [read_group(cur) for _ in range(n_args)]
            title, asof = None, None
            if name == "dated":
                asof = args[0].strip()
                if not year_only and not re.fullmatch(r"\d{4}-\d{2}", asof):
                    cur.err(f"dated box date {asof!r} is not YYYY-MM")
            if args and not year_only:
                title = self.parse_inlines(args[-1])
            label = None
            m = re.match(r"\s*\\label\{", s[cur.i:])
            if m:
                cur.i += m.end() - 1
                label = read_group(cur)
            body_blocks = self.parse_blocks(find_env_end(cur, name))
            return {"t": "env", "kind": name, "title": title, "label": label,
                    "difficulty": None, "sol_key": None, "asof": asof,
                    "body": body_blocks}
        if name in ASIDE_BOXES:
            title, pics = None, []
            if name == "safety" and s[cur.i:cur.i + 1] != "{":
                pass    # Earth books: no pictogram argument
            elif name == "safety":
                arg = read_group(cur)
                gcur = Cursor(arg, self.filename)
                while gcur.i < len(arg):
                    m = re.match(r"(\s|\\q?quad\b|\\,)*\\ghs\b\s*",
                                 arg[gcur.i:])
                    if not m:
                        if arg[gcur.i:].strip():
                            gcur.err("safety pictograms: only \\ghs allowed")
                        break
                    gcur.i += m.end()
                    pics.append({"t": "pic", "src": self.chem_setup
                                 + self.picture_command(gcur, "ghs")})
            elif name != "recall":
                opt = read_optional(cur)
                if opt and opt.strip():
                    title = self.parse_inlines(opt.strip())
            body = find_env_end(cur, name)
            widths, side = None, "start"
            photo, body = self.leading_photo(body)
            if self.MINIPAGE.search(body):
                # a portrait beside the text: photo minipage(s), then (or
                # before) one text minipage
                pics, widths, side, body = self.parse_aside_minipages(body)
            body_blocks = self.parse_blocks(body)
            if photo:
                body_blocks.insert(0, photo)
            return {"t": "env", "kind": name, "title": title, "label": None,
                    "difficulty": None, "sol_key": None, "pics": pics,
                    "pic_widths": widths, "pics_side": side,
                    "body": body_blocks}
        if name == "MOdiagram":
            # a molecular-orbital diagram outside an omfigure
            start = cur.i - len("\\begin{MOdiagram}")
            find_env_end(cur, name)
            return {"t": "figure", "label": None, "caption": [],
                    "tikzs": [self.chem_setup + s[start:cur.i]]}
        if name == "omchartable":
            # {group}{class colspec}{class headers}: a math array (the
            # style file sets it in $…$ inside a center block)
            group, colspec, heads = [read_group(cur) for _ in range(3)]
            rows = find_env_end(cur, name)
            return {"t": "dmath", "tex": (
                f"\\begin{{array}}{{l|{colspec}|l|l}}\\hline {group} & "
                f"{heads} & & \\\\ \\hline {rows} \\hline\\end{{array}}")}
        if name in LIST_ENVS:
            opt = read_optional(cur)
            resume = bool(opt) and "resume" in opt
            alpha = False
            for o in (opt or "").split(","):
                if o.strip() == "label=(\\alph*)":
                    alpha = True    # Earth books: (a), (b)…
                # beginpenalty (chemistry): a print page-break hint
                elif o.strip() and o.strip() != "resume" \
                        and not re.fullmatch(r"beginpenalty=\d+|leftmargin=\*"
                                             r"|(itemsep|topsep)=[\d.]+pt",
                                             o.strip()):
                    raise ParseError(
                        f"{self.filename}: unsupported list option [{opt}]")
            body = find_env_end(cur, name)
            chunks = split_top_level(body, "item", self.filename)
            # \sloppy before the first \item: a print line-breaking hint
            if chunks[0].replace("\\sloppy", "").strip():
                raise ParseError(
                    f"{self.filename}: text before first \\item in {name}")
            items = [self.parse_blocks(cchunk) for cchunk in chunks[1:]]
            node = {"t": "list", "kind": name, "resume": resume,
                    "items": items}
            if alpha:
                node["alpha"] = True
            return node
        if name in BLOCK_ENVS:
            title, sol_key, difficulty = None, None, None
            roles = firm = level = None
            if name == "solution":
                sol_key = read_group(cur)
            else:
                opt = read_optional(cur)
                if opt is not None:
                    if name in ("interviewq", "question"):
                        # [$\star\star$ \iqroles{trader} \iqfirm{market maker}]
                        difficulty = count_stars(opt)
                        rest = re.sub(r"\$(\\star)*\$", "", opt)
                        mr = re.search(r"\\iqroles\{([^{}]*)\}", rest)
                        mf = re.search(r"\\iqfirm\{([^{}]*)\}", rest)
                        roles = self.parse_inlines(mr.group(1)) if mr else None
                        firm = self.parse_inlines(mf.group(1)) if mf else None
                        ml = re.search(r"\\iqlevel\{([^{}]*)\}", rest)
                        level = self.parse_inlines(ml.group(1)) if ml else None
                        rest = re.sub(r"\\iq(roles|firm|level)\{[^{}]*\}", "",
                                      rest)
                        if difficulty == 0 or rest.strip():
                            raise ParseError(
                                f"{self.filename}: unsupported interviewq "
                                f"option {opt!r}")
                    elif name == "exercise":
                        difficulty = count_stars(opt)
                        if difficulty == 0:
                            raise ParseError(
                                f"{self.filename}: exercise option {opt!r} "
                                "is not a star difficulty")
                    else:
                        o = opt.strip()
                        if o.startswith("{") and o.endswith("}"):
                            o = o[1:-1]
                        if o == "\\omnameProof":
                            title = None  # explicit default title
                        else:
                            title = self.parse_inlines(o)
            label = None
            m = re.match(r"\s*\\label\{", s[cur.i:])
            if m:
                cur.i += m.end() - 1
                label = read_group(cur)
            body = find_env_end(cur, name)
            body_blocks = self.parse_blocks(body)
            # adopt a label written late in the body (page-break pattern)
            for node in body_blocks[:]:
                if node["t"] == "label":
                    if label is None:
                        label = node["name"]
                    body_blocks.remove(node)
            node = {"t": "env", "kind": name, "title": title, "label": label,
                    "difficulty": difficulty, "sol_key": sol_key,
                    "body": body_blocks}
            if name in ("interviewq", "question"):
                node["roles"], node["firm"] = roles, firm
                node["level"] = level
            return node
        cur.err(f"unknown environment {name!r}")

    def parse_iv_drills(self, name, body):
        """Interview-book drill sheet or key: a print table of \\ivdrill /
        \\ivkey cells filled column by column. On the web it is one list in
        item order, which reflows on a phone."""
        macro = "\\ivdrill" if name == "ivdrillsheet" else "\\ivkey"
        items = []
        for row in split_top_level(body, "\\", self.filename):
            row = re.sub(r"^\s*\[[^\]]*\]", "", row).replace("\\hline", "")
            for cell in re.split(r"(?<!\\)&", row):
                # a strut for a tall fraction (print-only)
                cell = re.sub(r"\\rule\[[^\]]*\]\{[^{}]*\}\{[^{}]*\}", "",
                              cell).strip()
                if not cell:
                    continue
                cur = Cursor(cell, self.filename)
                if not cell.startswith(macro + "{"):
                    cur.err(f"unsupported cell in {name}: {cell[:60]!r}")
                cur.i = len(macro)
                number, tex = read_group(cur), read_group(cur)
                options = None
                if cell.startswith("\\ivoptions{", cur.i):
                    cur.i += len("\\ivoptions")
                    options = [read_group(cur) for _ in range(4)]
                if cell[cur.i:].strip():
                    cur.err(f"unsupported cell in {name}: {cell[:60]!r}")
                inl = self.parse_inlines(tex)
                for node in inl:
                    if node["t"] == "math":  # print's \everymath{\displaystyle}
                        node["tex"] = "\\displaystyle " + node["tex"]
                items.append({"n": int(number), "inl": inl, "options": [
                    self.parse_inlines(f"${o}$") for o in options
                ] if options else None})
        items.sort(key=lambda item: item["n"])
        return {"t": "ivdrills", "key": name == "ivdrillkey", "items": items}

    def parse_iv_lookup(self, body):
        """Played games: a scrambled table of results (\\ivcell{4.5}{L} …)."""
        pattern = r"\\ivcell\{([^{}]*)\}\{([^{}]*)\}"
        rest = re.sub(pattern, "", body)
        if re.sub(r"\\quad\b|\s", "", rest):
            raise ParseError(f"{self.filename}: unsupported \\ivlookup "
                             f"content {rest.strip()[:60]!r}")
        return {"t": "ivlookup", "cells": [
            (self.parse_inlines(a), self.parse_inlines(b))
            for a, b in re.findall(pattern, body)]}

    def parse_table_float(self, body):
        """A `table` float (quant books): one tabular plus \\caption and
        \\label, numbered "Table N.M" with LaTeX's table counter."""
        caption, label = [], None
        mcap = re.search(r"\\caption\{", body)
        if mcap:
            gcur = Cursor(body, self.filename)
            gcur.i = mcap.end() - 1
            caption = self.parse_inlines(read_group(gcur))
            body = body[:mcap.start()] + body[gcur.i:]
        mlab = re.search(r"\\label\{([^{}]*)\}", body)
        if mlab:
            label = mlab.group(1)
            body = body[:mlab.start()] + body[mlab.end():]
        body = re.sub(r"\\centering|\\small\b|\\footnotesize\b"
                      r"|\\setlength\{\\tabcolsep\}\{[^{}]*\}"
                      r"|\\renewcommand\{\\arraystretch\}\{[\d.]+\}",
                      " ", body)
        table = self.parse_center(body)
        numbered = mcap is not None
        if table["t"] == "tablefloat" and label:
            # a legend in place of \caption (one Arabic table): the label
            # is still cited, so it stays numbered like the other editions
            caption, table, numbered = table["caption"], table["table"], True
        if table["t"] not in ("table", "tables"):
            raise ParseError(f"{self.filename}: table float without tabular")
        return {"t": "tablefloat", "table": table, "caption": caption,
                "label": label, "numbered": numbered}

    FIGURE_SETUP = re.compile(
        r"\\(setchemfig|tdplotsetmaincoords|pgfplotsset|tikzset|colorlet"
        r"|pgfplotstableread|pgfplotstablegetelem)\s*\{")

    def expand_photo_macro(self, body):
        """A photo-grid macro defined inside the figure (Earth books):
        expand its calls, the photo's file name is `images/…/#1` until then."""
        m = re.search(r"\\newcommand\{(\\[a-zA-Z]+)\}\[(\d)\]\{", body)
        if not m:
            return body
        cur = Cursor(body, self.filename)
        cur.i = m.end() - 1
        definition = read_group(cur)
        if "\\includegraphics" not in definition:
            return body
        rest = body[:m.start()] + body[cur.i:]
        call = re.compile(re.escape(m.group(1)) + r"(?![a-zA-Z])")
        out, pos = [], 0
        for found in iter(lambda: call.search(rest, pos), None):
            out.append(rest[pos:found.start()])
            cur = Cursor(rest, self.filename)
            cur.i = found.end()
            text = definition
            for n in range(1, int(m.group(2)) + 1):
                text = text.replace(f"#{n}", read_group(cur))
            out.append(text)
            pos = cur.i
        return "".join(out) + rest[pos:]

    def parse_figure(self, body, floated=False):
        """Figure-level settings before the pictures (chemistry books:
        \\pgfplotsset styles, \\setchemfig, the tikz-3dplot view) are
        prefixed to every picture of the figure, minipages included."""
        saved = self.chem_setup
        body = self.expand_photo_macro(body)
        pictures = [(m.start(), m.end()) for m in re.finditer(
            r"\\begin\{(tikzpicture|circuitikz)\}.*?\\end\{\1\}", body,
            re.S)]
        pos = 0
        while True:
            m = self.FIGURE_SETUP.search(body, pos)
            if not m:
                break
            if any(a <= m.start() < b for a, b in pictures):
                pos = m.end()
                continue
            cur = Cursor(body, self.filename)
            cur.i = m.end() - 1
            groups = 2 if m.group(1) in ("tdplotsetmaincoords", "colorlet",
                                         "pgfplotstablegetelem") else 1
            setup = f"\\{m.group(1)}" + "".join(
                "{" + read_group(cur) + "}" for _ in range(groups))
            trailer = {
                # \pgfplotstableread{file}\macro
                "pgfplotstableread": r"\s*\\[a-zA-Z]+",
                # \pgfplotstablegetelem{0}{col}\of{\tab}\let\x\pgfplotsretval
                "pgfplotstablegetelem":
                    r"\s*\\of\s*(\{[^{}]*\}|\\[a-zA-Z]+)\s*"
                    r"\\let\\[a-zA-Z]+\\pgfplotsretval",
            }.get(m.group(1))
            if trailer:
                tail = re.match(trailer, body[cur.i:])
                if not tail:
                    cur.err(f"unsupported \\{m.group(1)} form")
                setup += tail.group(0).strip() + "\n"
                cur.i += tail.end()
            self.chem_setup += setup
            body = body[:m.start()] + body[cur.i:]
            shift = cur.i - m.start()
            pictures = [(a - shift if a > m.start() else a,
                         b - shift if b > m.start() else b)
                        for a, b in pictures]
            pos = m.start()
        try:
            return self.parse_figure_body(body, floated)
        finally:
            self.chem_setup = saved

    def parse_figure_body(self, body, floated=False):
        """An omfigure holds one or more pictures — tikzpictures, or raster
        photos via \\includegraphics (side-by-side pictures are separated by
        \\qquad/\\quad) — plus a {\\small ...} caption.

        Every picture source (tikz env or the literal \\includegraphics
        command) lands in "tikzs" in order; the FigureBuilder tells them
        apart. A raster figure may also carry a labelled photo grid: a
        {\\small ...} sub-caption right after the leading picture, then a
        tabular whose rows alternate \\includegraphics cells and
        {\\footnotesize label} cells (physics-1 solar system) — parsed into
        "grid" = [[{"src", "label"}, ...], ...]."""
        tikzs, widths, sublabels = [], {}, {}
        table = None
        # \makebox[0.32\linewidth]{\includegraphics…}: print-only cell width
        rest = re.sub(r"\\makebox\[[^\]]*\]\{(\\includegraphics"
                      r"(?:\[[^\]]*\])?\{[^{}]*\})\}", r"\1", body)
        composed = self.composed_picture(rest)
        if composed:
            tikzs, rest = [composed[0]], composed[1]
        elif "\\begin{minipage}" in rest:
            # side-by-side sub-figures, each in a minipage (biology)
            tikzs, widths, sublabels, table, rest = \
                self.parse_minipage_figure(rest)
        pictures, rest = self.take_pictures(rest)
        tikzs += pictures
        if tikzs and table is None and self.INCLUDEGRAPHICS.search(rest):
            # photos in the same figure as a chart (Earth books)
            tikzs += [m.group(0) for m in self.INCLUDEGRAPHICS.finditer(rest)]
            rest = self.INCLUDEGRAPHICS.sub("", rest)
        # \resizebox{\linewidth}{!}{<picture>}: print-only fit to the text
        # width — the SVG scales to its column by itself
        rest = re.sub(r"\\resizebox\{[^{}]*\}\{[^{}]*\}\{\s*\}", "", rest)
        grid = None
        if not tikzs:
            tikzs, grid, sublabels, rest = self.parse_raster_figure(rest)
        if not tikzs and grid is None \
                and re.search(r"\\begin\{(center|tabular)\}", rest):
            # a table set as a figure (the genetic-code table)
            table, rest = self.parse_table_figure(rest)
        math = None
        if not tikzs and table is None:
            mm = re.search(r"\\begin\{(align\*|equation\*|gather\*)\}", rest)
            if mm:
                end_pat = f"\\end{{{mm.group(1)}}}"
                e = rest.find(end_pat, mm.start())
                if e < 0:
                    raise ParseError(f"{self.filename}: missing {end_pat}")
                e += len(end_pat)
                math = rest[mm.start():e]
                if mm.group(1) == "equation*":
                    math = math[len("\\begin{equation*}"):
                                -len("\\end{equation*}")].strip()
                rest = rest[:mm.start()] + rest[e:]
        if not tikzs and table is None and math is None and grid is None:
            raise ParseError(
                f"{self.filename}: omfigure without tikzpicture, "
                "\\includegraphics or tabular")
        if floated:
            # floats: \caption{...} + optional \label, \centering etc.
            label = None
            mcap = re.search(r"\\caption\{", rest)
            caption_text = ""
            if mcap:
                gcur = Cursor(rest, self.filename)
                gcur.i = mcap.end() - 1
                caption_text = read_group(gcur)
                rest = rest[:mcap.start()] + rest[gcur.i:]
            mlab = re.search(r"\\label\{([^{}]*)\}", rest)
            if mlab:
                label = mlab.group(1)
                rest = rest[:mlab.start()] + rest[mlab.end():]
            rest = re.sub(
                r"\\centering|\\leavevmode|\\qquad|\\quad|\\hfill",
                " ", rest)
            if rest.strip():
                raise ParseError(
                    f"{self.filename}: unsupported figure content "
                    f"{rest.strip()[:60]!r}")
            return {"t": "figure", "tikzs": tikzs, "label": label,
                    "caption": self.parse_inlines(caption_text)}
        # what remains is the caption (plus separators like \qquad)
        caption = re.sub(r"\\qquad|\\quad|\\hfill|\\medskip|\\smallskip"
                         r"|\\bigskip|\\par\b|\\footnotesize\b"
                         r"|\\vspace\*?\{[^{}]*\}"
                         r"|\\setlength\{\\tabcolsep\}\{[^{}]*\}"
                         r"|\\renewcommand\{\\arraystretch\}\{[\d.]+\}",
                         " ", rest).strip()
        label, numbered, aliases = None, False, []
        bare = re.sub(r"\\centering|\\hspace\*?\{[^{}]*\}", " ",
                      caption).strip()
        if bare.startswith("\\omcaption"):
            # print layout around quant pictures (\centering, \hspace
            # between side-by-side pictures)
            caption = bare
        if caption.startswith("\\omcaption"):
            # quant books: \omcaption{text}\label{fig:...} steps the figure
            # counter ("Figure N.M.") whether or not a label follows
            gcur = Cursor(caption, self.filename)
            gcur.i = len("\\omcaption")
            text = read_group(gcur)
            after = caption[gcur.i:].strip()
            labels = re.findall(r"\\label\{([^{}]*)\}", after)
            if re.sub(r"\\label\{[^{}]*\}", "", after).strip():
                raise ParseError(f"{self.filename}: unsupported text after "
                                 f"\\omcaption: {after[:60]!r}")
            caption, numbered = text, True
            # a second \label names the same figure (an alias anchor)
            label, aliases = (labels[0], labels[1:]) if labels else (None, [])
        # Earth books: a \label after the caption of a figure print leaves
        # unnumbered. It only serves \pageref: an anchor, not a number.
        anchor = None
        m3 = re.search(r"\s*\\label\{(fig:[^{}]*)\}\s*$", caption)
        if m3:
            anchor = m3.group(1)
            caption = caption[:m3.start()]
        m2 = re.fullmatch(r"\{\\small\s+(.*)\}", caption, re.S)
        if m2:
            caption = m2.group(1)
        node = {"t": "figure", "tikzs": tikzs, "label": label,
                "caption": self.parse_inlines(caption)}
        if anchor:
            node["anchor"] = anchor
        if numbered:
            node["numbered"] = True
        if aliases:
            node["aliases"] = aliases
        if grid is not None:
            node["grid"] = grid
        if sublabels:
            node["sublabels"] = sublabels
        if widths:
            node["widths"] = widths
        if table is not None:
            node["table"] = table
        if math is not None:
            node["math"] = math
        return node

    # The books' text width (a4paper, inner/outer 2.2cm): minipage widths
    # are fractions of it, and figures inside a minipage size their
    # \\linewidth-relative pictures from it.
    TEXT_WIDTH_PT = 472

    MINIPAGE = re.compile(
        r"\\begin\{minipage\}(?:\[[a-z]\])?\{([\d.]+)\\(?:line|text|column)width\}")

    def parse_minipage_figure(self, body):
        """Sub-figures in `\\begin{minipage}[b]{0.48\\linewidth}` blocks
        (\\hfill-separated): each holds one tikzpicture or one
        \\includegraphics plus an optional {\\small ...} sub-caption.
        Returns (sources, widths, sublabels, rest) — `widths` maps a
        picture index to its fraction of the text width; a tikz source
        gets a matching \\linewidth prefix so `width=0.9\\linewidth`
        pictures inside it keep their print proportion."""
        tikzs, widths, sublabels = [], {}, {}
        table = None
        rest = body
        while True:
            m = self.MINIPAGE.search(rest)
            if not m:
                break
            cur = Cursor(rest, self.filename)
            cur.i = m.end()
            inner = find_env_end(cur, "minipage")
            rest = rest[:m.start()] + rest[cur.i:]
            width = float(m.group(1))
            pics, after = self.take_pictures(inner)
            if len(pics) > 1:
                # pictures stacked in one column (chemistry spectra): one
                # picture, set in a minipage of the printed width
                src = (f"\\begin{{minipage}}{{{width}\\linewidth}}"
                       "\\centering\n" + "\\par\n".join(pics)
                       + "\n\\end{minipage}")
                inner = after
            elif pics:
                src = (f"\\setlength{{\\linewidth}}"
                       f"{{{round(width * self.TEXT_WIDTH_PT)}pt}}%\n"
                       + pics[0])
                inner = after
            else:
                im = self.INCLUDEGRAPHICS.search(inner)
                if not im and "\\begin{tabular}" in inner and table is None:
                    # a table beside the picture (chemistry statistics)
                    table = self.parse_center(re.sub(
                        r"\\centering|\\vspace\{0pt\}", " ", inner))
                    continue
                if not im:
                    # the text beside a picture (a portrait's legend):
                    # it is the figure's caption
                    rest = rest[:m.start()] + re.sub(
                        r"^\s*\\vspace\{0pt\}", "", inner) + rest[m.start():]
                    continue
                src = im.group(0)
                inner = inner[:im.start()] + inner[im.end():]
            idx = len(tikzs)
            tikzs.append(src)
            widths[idx] = width
            sub = re.sub(r"\\centering|\\par\b|\\smallskip|\\medskip"
                         r"|\\bigskip|\\vspace\*?\{[^{}]*\}"
                         r"|\\\\(?:\[[^\]]*\])?", " ", inner).strip()
            m2 = re.fullmatch(r"\{\\(?:small|footnotesize|scriptsize)\s+(.*)\}",
                              sub, re.S)
            if m2:
                sub = m2.group(1)
            if sub:
                sublabels[idx] = self.parse_inlines(sub)
        return tikzs, widths, sublabels, table, rest

    def leading_photo(self, body):
        """A box opening on a centred photo and its {\\small caption}, above
        the text (Earth books). Returns (figure node or None, the rest)."""
        m = re.match(r"\s*\\centering\s*(\\includegraphics"
                     r"(?:\[[^\]]*\])?\{[^{}]*\})", body)
        if not m:
            return None, body
        rest = re.sub(r"^(\s|\\par\b|\\smallskip\b)*", "", body[m.end():])
        caption = []
        if rest.startswith("{\\small"):
            cur = Cursor(rest, self.filename)
            group = read_group(cur)
            caption = self.parse_inlines(re.sub(r"^\\small\s+", "", group))
            rest = rest[cur.i:]
        rest = re.sub(r"^(\s|\\par\b|\\medskip\b|\\smallskip\b"
                      r"|\\raggedright\b)*", "", rest)
        return ({"t": "figure", "tikzs": [m.group(1)], "label": None,
                 "caption": caption}, rest)

    def parse_aside_minipages(self, body):
        """A box body made of side-by-side minipages: picture ones (one
        \\includegraphics each) and exactly one text minipage. Returns
        (pic nodes, their widths, "start"|"end" = side of the pictures,
        the text)."""
        pics, widths, texts, first = [], [], [], None
        rest = body
        # Earth books: a bare \includegraphics beside the text minipage, and
        # the photo's {\small caption} under them
        bare = self.INCLUDEGRAPHICS.search(body)
        first_minipage = self.MINIPAGE.search(body)
        if bare and bare.start() < first_minipage.start():
            width = re.search(r"width=([\d.]+)\\linewidth", bare.group(0))
            if not width:
                raise ParseError(f"{self.filename}: a picture beside a "
                                 "minipage needs width=N\\linewidth")
            rest = body[:bare.start()] + body[bare.end():]
            legend = re.search(r"\{\\small\s+(.*)\}\s*$", rest, re.S)
            caption = None
            if legend:
                caption = self.parse_inlines(legend.group(1))
                rest = rest[:legend.start()]
            pics.append({"t": "pic", "src": bare.group(0),
                         "caption": caption})
            widths.append(float(width.group(1)))
            first = "pics"
        while True:
            m = self.MINIPAGE.search(rest)
            if not m:
                break
            cur = Cursor(rest, self.filename)
            cur.i = m.end()
            inner = find_env_end(cur, "minipage")
            rest = rest[:m.start()] + rest[cur.i:]
            inner = re.sub(r"^\s*\\vspace\{0pt\}", "", inner)
            stacked = list(self.INCLUDEGRAPHICS.finditer(inner))
            if len(stacked) > 1 and "\\begin{tikzpicture}" not in inner:
                # photos stacked in one column, each with its legend (Earth
                # books): the column's width once, a 0 for each further photo
                for i, pic in enumerate(stacked):
                    end = stacked[i + 1].start() if i + 1 < len(stacked) \
                        else len(inner)
                    legend = re.sub(r"\\par\b|\\centering|\\smallskip", " ",
                                    inner[pic.end():end]).strip()
                    m2 = re.fullmatch(r"\{\\(?:footnotesize|small|scriptsize)"
                                      r"\s+(.*)\}", legend, re.S)
                    if m2:
                        legend = m2.group(1)
                    pics.append({"t": "pic", "src": pic.group(0),
                                 "caption": self.parse_inlines(legend)
                                 if legend else None})
                    widths.append(float(m.group(1)) if i == 0 else 0.0)
                first = first or "pics"
                continue
            # a tikzpicture drawing over the photo (Earth books) is the
            # picture itself, at the minipage's width
            im = re.search(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}",
                           inner, re.S) or self.INCLUDEGRAPHICS.search(inner)
            if im:
                # the photo, with an optional {\footnotesize legend}
                legend = re.sub(r"\\par\b|\\centering|\\smallskip"
                                r"|\\\\(\[[^\]]*\])?", " ",
                                inner[:im.start()] + inner[im.end():]).strip()
                m2 = re.fullmatch(r"\{\\(?:footnotesize|small|scriptsize)"
                                  r"\s+(.*)\}", legend, re.S)
                if m2:
                    legend = m2.group(1)
                src = im.group(0)
                if src.startswith("\\begin{tikzpicture}"):
                    width_pt = float(m.group(1)) * self.TEXT_WIDTH_PT
                    src = f"\\setlength{{\\linewidth}}{{{width_pt:g}pt}}{src}"
                pics.append({"t": "pic", "src": src,
                             "caption": self.parse_inlines(legend)
                             if legend else None})
                widths.append(float(m.group(1)))
                first = first or "pics"
            else:
                texts.append(inner)
                first = first or "text"
        leftover = re.sub(r"\\hfill|\\hspace\{[^{}]*\}|\\par\b|\\smallskip\b",
                          "", rest)
        if len(texts) != 1 or not pics or leftover.strip():
            raise ParseError(f"{self.filename}: unsupported minipage layout "
                             "in a box")
        return pics, widths, "start" if first == "pics" else "end", texts[0]

    def parse_table_figure(self, body):
        """An omfigure whose picture is a tabular (in a center block or
        bare): returns (table node, rest) — `rest` is the caption."""
        m = re.search(r"\\begin\{center\}", body)
        if m:
            cur = Cursor(body, self.filename)
            cur.i = m.end()
            inner = find_env_end(cur, "center")
            table = self.parse_center(inner)
            return table, body[:m.start()] + body[cur.i:]
        m = re.search(r"\\begin\{tabular\}", body)
        cur = Cursor(body, self.filename)
        cur.i = m.end()
        read_group(cur)   # colspec; parse_center re-reads it
        find_env_end(cur, "tabular")
        table = self.parse_center(body[m.start():cur.i])
        return table, body[:m.start()] + body[cur.i:]

    INCLUDEGRAPHICS = re.compile(
        r"\\includegraphics(?:\[((?:[^\[\]{}]|\{[^{}]*\})*)\])?\s*\{([^{}]*)\}")

    def parse_raster_figure(self, body):
        """Extract \\includegraphics pictures from an omfigure body.

        Returns (sources, grid, sublabels, rest): `sources` are the literal
        \\includegraphics commands of the free-standing pictures (in
        order), `grid` the optional labelled photo table (rows of
        {"src", "label"} dicts) or None, `sublabels` = {index: inlines} for
        a {\\small ...} sub-caption attached to a leading picture, and
        `rest` the leftover text (the caption)."""
        rest = re.sub(r"\\medskip|\\smallskip|\\bigskip|\\centering", " ",
                      body)
        grid = None
        mt = re.search(r"\\begin\{tabular\}", rest)
        if mt and not self.INCLUDEGRAPHICS.search(rest[mt.start():]):
            return [], None, {}, body   # a table figure (parse_table_figure)
        if mt:
            cur = Cursor(rest, self.filename)
            cur.i = mt.start() + len("\\begin")
            read_group(cur)   # "tabular"
            read_group(cur)   # colspec (layout only)
            tab_body = find_env_end(cur, "tabular")
            grid = self.parse_photo_grid(tab_body)
            before, rest = rest[:mt.start()], rest[cur.i:]
        else:
            before = rest
            rest = ""
        sources = []
        while True:
            m = self.INCLUDEGRAPHICS.search(before)
            if not m:
                break
            sources.append(m.group(0))
            before = before[:m.start()] + before[m.end():]
        if not sources and grid is None:
            return [], None, {}, body
        sublabels = {}
        if grid is not None:
            # text left before the tabular is the leading picture's
            # sub-caption; the real caption follows the tabular
            sub = re.sub(r"\\qquad|\\quad|\\hfill"
                         r"|\\setlength\{\\tabcolsep\}\{[^{}]*\}", " ",
                         before).strip()
            m2 = re.fullmatch(r"\{\\small\s+(.*)\}", sub, re.S)
            if m2:
                sub = m2.group(1)
            if sub:
                if not sources:
                    raise ParseError(
                        f"{self.filename}: figure sub-caption without a "
                        "leading picture")
                sublabels[len(sources) - 1] = self.parse_inlines(sub)
        else:
            rest = before
        return sources, grid, sublabels, rest

    def parse_photo_grid(self, body):
        """Rows alternate picture cells and {\\footnotesize label} cells."""
        # `\\[4pt]` row spacing leaves a leading [4pt] on the next chunk
        rows_raw = [re.sub(r"^\s*\[[^\]]*\]", "", r).strip() for r in
                    split_top_level(body, "\\", self.filename)]
        rows_raw = [r for r in rows_raw if r]
        grid = []
        i = 0
        while i < len(rows_raw):
            pics = [c.strip() for c in
                    self.split_raw_cells(rows_raw[i])]
            if not all(self.INCLUDEGRAPHICS.fullmatch(c) for c in pics):
                raise ParseError(
                    f"{self.filename}: photo grid row is not all "
                    f"\\includegraphics: {rows_raw[i][:60]!r}")
            labels = [""] * len(pics)
            if i + 1 < len(rows_raw) and not self.INCLUDEGRAPHICS.search(
                    rows_raw[i + 1]):
                labels = [c.strip() for c in
                          self.split_raw_cells(rows_raw[i + 1])]
                if len(labels) != len(pics):
                    raise ParseError(
                        f"{self.filename}: photo grid label row has "
                        f"{len(labels)} cells for {len(pics)} pictures")
                i += 1
            row = []
            for src, lab in zip(pics, labels):
                m2 = re.fullmatch(r"\{\\(?:footnotesize|small|scriptsize)"
                                  r"\s+(.*)\}", lab, re.S)
                if m2:
                    lab = m2.group(1)
                row.append({"src": src, "label": self.parse_inlines(lab)})
            grid.append(row)
            i += 1
        if not grid:
            raise ParseError(f"{self.filename}: empty photo grid")
        return grid

    def split_raw_cells(self, raw):
        """Top-level `&` split without inline parsing."""
        cells, buf, depth = [], [], 0
        i, n = 0, len(raw)
        while i < n:
            c = raw[i]
            if c == "\\":
                buf.append(raw[i:i + 2])
                i += 2
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            elif c == "&" and depth == 0:
                cells.append("".join(buf))
                buf = []
                i += 1
                continue
            buf.append(c)
            i += 1
        cells.append("".join(buf))
        return cells

    def parse_center(self, body):
        """A center block holds one or more tabulars (side-by-side tables
        are separated by \\qquad), optionally after an \\arraystretch
        row-height tweak (print-only; CSS handles it in HTML)."""
        body = body.strip()
        while True:
            # print-only row height and sizing, in either order
            stripped = re.sub(r"^\\renewcommand\{\\arraystretch\}"
                              r"\{[\d.]+\}\s*", "", body)
            stripped = re.sub(r"^\\small\s+", "", stripped)
            # {\small \begin{tabular}…} as one group (Earth books)
            group = re.fullmatch(r"(?:\{\s*(?:\\small\s+)?|\\babelsublr\{\s*)"
                                 r"(\\begin\{tabular\}.*)\}",
                                 stripped, re.S)
            if group:
                stripped = group.group(1).strip()
            if stripped == body:
                break
            body = stripped
        if "\\begin{tabular}" not in body:
            # a centred line of text (a displayed DNA sequence)
            return {"t": "centered", "inl": self.parse_inlines(body)}
        tables = []
        cur = Cursor(body, self.filename)
        while True:
            rest = cur.s[cur.i:]
            stripped = re.match(
                r"(\s|\\qquad\b|\\quad\b|\\small\b|\\footnotesize\b"
                r"|\\scriptsize\b|\\smallskip\b|\\medskip\b"
                r"|\\setlength\{[^{}]*\}\{[^{}]*\})*",
                rest).end()
            cur.i += stripped
            if cur.i >= len(cur.s):
                break
            if tables and not cur.s.startswith("\\begin{tabular}", cur.i):
                # quant books: an unnumbered caption paragraph under the
                # table(s), still inside the center block
                caption = re.sub(r"^(\s|\\(par|smallskip|medskip|small"
                                 r"|footnotesize)\b)*", "",
                                 cur.s[cur.i:]).strip()
                m2 = re.fullmatch(r"\{\\(?:small|footnotesize)\s+(.*)\}",
                                  caption, re.S)
                if m2:
                    caption = m2.group(1)
                table = tables[0] if len(tables) == 1 \
                    else {"t": "tables", "tables": tables}
                return {"t": "tablefloat", "table": table, "label": None,
                        "numbered": False,
                        "caption": self.parse_inlines(caption)}
            if not cur.s.startswith("\\begin{tabular}", cur.i):
                raise ParseError(
                    f"{self.filename}: only tabular is supported inside "
                    "center")
            cur.i += len("\\begin")
            read_group(cur)  # "tabular"
            colspec = read_group(cur)
            tab_body = find_env_end(cur, "tabular")
            tables.append(self.parse_tabular(colspec, tab_body))
        if not tables:
            raise ParseError(f"{self.filename}: empty center block")
        if len(tables) == 1:
            return tables[0]
        return {"t": "tables", "tables": tables}

    def parse_tabular(self, colspec, body):
        """Rows are dicts {"cells": [...], "rule": bool} — `rule` marks a
        row preceded by a mid-table \\hline (sign tables draw one above
        the final sign row)."""
        rows_raw = split_top_level(body, "\\", self.filename)
        header, rows = None, []
        pending_rule = False
        booktabs = bool(re.search(r"\\(toprule|midrule|bottomrule)\b", body))
        for raw in rows_raw:
            # \\[8pt] row spacing leaves its [length] on the next row
            raw = re.sub(r"^\s*\[-?[\d.]+\s*(?:pt|ex|em|mm|cm)\]", "", raw)
            # booktabs (quant books): \midrule separates like \hline (after
            # the first row it marks the header); the outer \toprule /
            # \bottomrule and partial \cmidrule are print-only
            raw = re.sub(r"\\(toprule|bottomrule)\b|\\cmidrule(\([a-z]*\))?"
                         r"\{[^{}]*\}", "", raw)
            raw = re.sub(r"\\midrule\b", "\\\\hline", raw)
            had_hline = "\\hline" in raw
            raw = raw.replace("\\hline", "").strip()
            if had_hline and len(rows) == 1 and header is None:
                # an \hline right after the first row marks it as the header
                header = rows.pop()["cells"]
                had_hline = False
            if not raw:
                pending_rule = pending_rule or had_hline
                continue
            rows.append({"cells": self.split_cells(raw),
                         "rule": had_hline or pending_rule})
            pending_rule = False
        node = {"t": "table", "colspec": colspec, "header": header,
                "rows": rows}
        if booktabs:
            # booktabs tables (quant books) are text tables: keep the
            # colspec's column alignment (l/c/r, p{} = left)
            node["booktabs"] = True
            node["align"] = column_alignments(colspec, self.filename)
        return node

    def split_cells(self, raw):
        cells, buf = [], []
        in_math, depth = False, 0
        i, n = 0, len(raw)
        while i < n:
            c = raw[i]
            if c == "\\":
                buf.append(raw[i:i + 2])
                i += 2
                continue
            if c == "$":
                in_math = not in_math
            elif c == "{" and not in_math:
                depth += 1
            elif c == "}" and not in_math:
                depth -= 1
            elif c == "&" and not in_math and depth == 0:
                cells.append(self.parse_cell("".join(buf).strip()))
                buf = []
                i += 1
                continue
            buf.append(c)
            i += 1
        cells.append(self.parse_cell("".join(buf).strip()))
        return cells

    def parse_cell(self, raw):
        """A table cell; \\multicolumn{n}{spec}{...} becomes one spanning
        node (the emitter turns it into colspan)."""
        m = re.fullmatch(r"\\multicolumn\{(\d+)\}\{(?:[^{}]|\{[^{}]*\})*\}"
                         r"\{(.*)\}", raw, re.S)
        if m:
            return [{"t": "span", "cols": int(m.group(1)),
                     "inl": self.parse_inlines(m.group(2))}]
        return self.parse_inlines(raw)

    def accented_letter(self, cur, combining):
        """Accent argument: a {X} group or a bare next letter (\\v S)."""
        import unicodedata
        src = cur.s
        if cur.i < len(src) and src[cur.i] == "{":
            inner = read_group(cur)
        elif cur.i < len(src) and src[cur.i].isalpha():
            inner = src[cur.i]
            cur.i += 1
        else:
            cur.err("accent command needs a letter")
        if len(inner) != 1 or not inner.isalpha():
            cur.err(f"unsupported accent argument {inner!r}")
        return unicodedata.normalize("NFC", inner + combining)

    def picture_command(self, cur, name):
        """Raw source of an inline picture command, cursor past its name:
        \\chemfig{…}, \\omorbs{…}, \\ghs[size]{GHSnn}, or \\tikz followed by
        a {…} group or one path up to its `;`."""
        opt = read_optional(cur)
        src = f"\\{name}" + (f"[{opt}]" if opt is not None else "")
        if name != "tikz" or cur.s[cur.i:cur.i + 1] == "{":
            return src + "{" + read_group(cur) + "}"
        start, depth = cur.i, 0
        while cur.i < len(cur.s):
            c = cur.s[cur.i]
            if c == "\\":
                cur.i += 2
                continue
            depth += {"{": 1, "}": -1}.get(c, 0)
            cur.i += 1
            if c == ";" and depth == 0:
                return src + cur.s[start:cur.i]
        cur.err("\\tikz path without a closing ';'")

    FIGURE_SPACING = re.compile(
        r"\\(?:qquad|quad|hfill|medskip|smallskip|bigskip|par|centering)\b"
        r"|\\[hv]space\*?\{[^{}]*\}")

    def composed_picture(self, body):
        """A chemistry figure composed by hand — structures, math arrows,
        "+" signs and \\chemmove arrows joining them — is one picture: its
        whole source up to the closing {\\small caption} compiles at once.
        Returns (source, caption) or None for every other figure."""
        bare = re.sub(r"\\begin\{(tikzpicture|circuitikz)\}.*?\\end\{\1\}",
                      "", body, flags=re.S)
        # a tabular of tikzpictures and their labels (Earth books) as well
        grid = re.search(r"\\begin\{tabular\}.*\\begin\{tikzpicture\}"
                         r".*\\end\{tabular\}", body, re.S)
        if not grid and (
                not re.search(
                    r"\\(chemfig|schemestart|chemmove|newcommand|def)\b", bare)
                or ("\\begin{minipage}" in body
                    and "\\newcommand" not in body and "\\def" not in body)):
            return None
        pic, caption = body.rstrip(), ""
        for m in re.finditer(r"\{\\small\b", pic):
            cur = Cursor(pic, self.filename)
            cur.i = m.start()
            read_group(cur)
            if not pic[cur.i:].strip():
                # the closing {\small …} group is the caption
                pic, caption = pic[:m.start()], pic[m.start():]
                break
        _, leftover = self.take_pictures(pic)
        if not self.FIGURE_SPACING.sub("", leftover).strip() \
                and "\\chemmove" not in bare:
            # pictures side by side: the usual path (but \chemmove arrows
            # may join nodes of neighbouring structures: one picture)
            return None
        return "\\centering\n" + self.chem_setup + pic.strip(), caption

    def take_pictures(self, body):
        """Split the pictures out of a figure body, in document order:
        tikzpicture/circuitikz environments as they are, and the chemistry
        books' MOdiagram, reaction scheme (\\schemestart…\\schemestop, with
        the \\chemmove arrows drawn on it), \\omperiodictable and lone
        \\chemfig structures; a \\setchemfig before them is prefixed to the
        source of each. Returns (sources, rest)."""
        sources, setup, rest = [], self.chem_setup, body
        pos = 0
        while True:
            m = CHEM_PICTURE.search(rest, pos)
            if not m:
                break
            env, cmd = m.group(1), m.group(2)
            cur = Cursor(rest, self.filename)
            cur.i = m.end()
            if env:
                end_pat = f"\\end{{{env}}}"
                e = rest.find(end_pat, m.start())
                if e < 0:
                    raise ParseError(f"{self.filename}: missing {end_pat}")
                cur.i = e + len(end_pat)
            elif cmd in ("setchemfig", "tdplotsetmaincoords"):
                # settings for the pictures that follow (chemfig sizes,
                # the 3-D view of tikz-3dplot crystal cells)
                setup += f"\\{cmd}" + "".join(
                    "{" + read_group(cur) + "}"
                    for _ in range(2 if cmd == "tdplotsetmaincoords" else 1))
                rest = rest[:m.start()] + rest[cur.i:]
                pos = m.start()
                continue
            elif cmd == "schemestart":
                e = rest.find("\\schemestop", m.start())
                if e < 0:
                    raise ParseError(f"{self.filename}: missing \\schemestop")
                cur.i = e + len("\\schemestop")
            elif cmd == "omperiodictable":
                read_optional(cur)
            else:
                read_group(cur)
            # curved arrows drawn over the structure just set
            while True:
                mm = re.match(r"\s*\\chemmove\b\s*", rest[cur.i:])
                if not mm:
                    break
                cur.i += mm.end()
                read_optional(cur)
                read_group(cur)
            src = rest[m.start():cur.i]
            sources.append(src if env in ("tikzpicture", "circuitikz")
                           and not setup else setup + src)
            rest = rest[:m.start()] + rest[cur.i:]
            pos = m.start()
        return sources, rest

    # --------------------------------------------------------------- inlines

    def parse_inlines(self, raw):
        cur = Cursor(raw, self.filename)
        return self._inlines(cur, until=None)

    def _inlines(self, cur, until):
        s = cur.s
        out = []
        text = []

        def emit_text():
            if text:
                joined = re.sub(r"\s+", " ", "".join(text))
                if joined:
                    out.append({"t": "text", "s": joined})
                text.clear()

        while cur.i < len(s):
            c = s[cur.i]
            if until and s.startswith(until, cur.i):
                break
            if c == "$":
                end = find_inline_math_end(s, cur.i)
                if end < 0:
                    cur.err("unbalanced $")
                emit_text()
                out.append({"t": "math", "tex": s[cur.i + 1:end].strip()})
                cur.i = end + 1
                continue
            if s.startswith("\\[", cur.i):
                # display math nested in an inline context (e.g. \emph)
                end = s.find("\\]", cur.i + 2)
                if end < 0:
                    cur.err("missing \\]")
                emit_text()
                out.append({"t": "math", "tex": s[cur.i + 2:end].strip(),
                            "display": True})
                cur.i = end + 2
                continue
            if c == "\\":
                m = CMD_RE.match(s, cur.i)
                if not m:
                    nxt = s[cur.i + 1:cur.i + 2]
                    following = s[cur.i + 2:cur.i + 3]
                    if nxt in ("'", "`", "^", '"', "~", "=") \
                            and (following.isalpha() or following == "{"):
                        # accents in prose, bare (\'e) or braced (\'{e})
                        import unicodedata
                        combining = {"'": "\u0301", "`": "\u0300",
                                     "^": "\u0302", '"': "\u0308",
                                     "~": "\u0303", "=": "\u0304"}[nxt]
                        if following == "{":
                            cur.i += 2
                            letter = read_group(cur)
                            if not letter:
                                # \^{} and \~{}: the plain character
                                text.append(nxt)
                                continue
                            if len(letter) != 1 or not letter.isalpha():
                                cur.err(f"unsupported accent argument "
                                        f"{letter!r}")
                        else:
                            letter = following
                            cur.i += 3
                        text.append(unicodedata.normalize(
                            "NFC", letter + combining))
                        continue
                    if nxt == "(":
                        # \( … \) inline math
                        end = s.find("\\)", cur.i + 2)
                        if end < 0:
                            cur.err("missing \\)")
                        emit_text()
                        out.append({"t": "math",
                                    "tex": s[cur.i + 2:end].strip()})
                        cur.i = end + 2
                        continue
                    if nxt in (" ", "\n", ""):    # "\ " explicit space
                        # ("" = trailing "\<newline>" whose newline was
                        # stripped at a paragraph boundary)
                        text.append(" ")
                    elif nxt in (",", ";"):        # thin/thick space
                        text.append(" ")
                    elif nxt == "\\":
                        text.append(" ")  # forced line break
                    elif nxt in ("%", "&", "_", "#", "$", "{", "}"):
                        text.append(nxt)
                    elif nxt == "-":
                        pass  # discretionary hyphen: hyphenation hint only
                    else:
                        cur.err(f"unsupported escape '\\{nxt}'")
                    cur.i += 2
                    continue
                name = m.group(1)
                cur.i = m.end()
                if name == "omterm":
                    emit_text()
                    label = read_group(cur)
                    inner = read_group(cur)
                    out.append({"t": "term", "label": label,
                                "inl": self.parse_inlines(inner)})
                elif name in ("cref", "Cref"):
                    # cleveref runs with [capitalize]: identical output
                    emit_text()
                    out.append({"t": "cref", "label": read_group(cur)})
                elif name == "eqref":
                    # amsmath: "(N.M)" linked, no kind name
                    emit_text()
                    out.append({"t": "eqref", "label": read_group(cur)})
                elif name in ("emph", "textit"):
                    # \textit (foreign words in some translations) = \emph
                    emit_text()
                    inner = read_group(cur)
                    node = {"t": "emph", "inl": self.parse_inlines(inner),
                            "index": None}
                    # attach an immediately following \index{...}
                    m2 = re.match(r"\s*\\index\{", s[cur.i:])
                    if m2:
                        cur.i += m2.end() - 1
                        node["index"] = read_group(cur)
                    out.append(node)
                elif name == "textbf":
                    emit_text()
                    inner = read_group(cur)
                    out.append({"t": "bold", "inl": self.parse_inlines(inner)})
                elif name == "texttt":
                    # monospace runs (DNA/RNA sequences)
                    emit_text()
                    inner = read_group(cur)
                    out.append({"t": "code", "inl": self.parse_inlines(inner)})
                elif name == "underline":
                    emit_text()
                    inner = read_group(cur)
                    out.append({"t": "u", "inl": self.parse_inlines(inner)})
                elif name == "rotatebox":
                    # print-only rotation (tall table headers): keep the text
                    read_group(cur)
                    inner = read_group(cur)
                    emit_text()
                    out.extend(self.parse_inlines(inner))
                elif name in ("O", "o"):
                    text.append("\u00d8" if name == "O" else "\u00f8")
                elif name == "index":
                    # standalone index entry: metadata only, no visible text
                    read_group(cur)
                elif name in ("dots", "ldots"):
                    text.append("…")
                elif name == "texteuro":
                    text.append("€")
                elif name == "euro":
                    # onequant.sty: \texteuro\, (thin space before the amount)
                    text.append("€ ")
                elif name in QUANT_SYMBOLS:
                    text.append(QUANT_SYMBOLS[name])
                elif name == "allowbreak":
                    pass  # line-break hint only
                elif name == "path":
                    # url.sty \path{...}: a verbatim file path
                    emit_text()
                    out.append({"t": "code",
                                "inl": [{"t": "text", "s": read_group(cur)}]})
                elif name == "si":
                    # siunitx v2 name of \unit
                    emit_text()
                    out.append({"t": "math",
                                "tex": "\\unit{" + read_group(cur) + "}"})
                elif name == "money":
                    # \money{USD}{2400000} -> USD 2 400 000
                    currency = read_group(cur)
                    text.append(currency + " ")
                    emit_text()
                    out.append({"t": "math",
                                "tex": "\\num{" + read_group(cur) + "}"})
                elif name == "omfieldlead":
                    # lead-in of \sfield / \bfield (see parse_blocks)
                    emit_text()
                    out.append({"t": "field",
                                "inl": self.parse_inlines(read_group(cur))})
                elif name == "ref":
                    # bare number reference ("chapter~\ref{ch:...}")
                    emit_text()
                    out.append({"t": "ref", "label": read_group(cur)})
                elif name == "newline":
                    # a line break in a p{} table cell
                    emit_text()
                    out.append({"t": "br"})
                elif name == "pageref":
                    # "on page~\pageref{fig:…}": the edition's printed page
                    emit_text()
                    out.append({"t": "pageref", "label": read_group(cur)})
                elif name == "omve":
                    # "vertical exaggeration ×2.5" (oneearth.sty)
                    emit_text()
                    out.append({"t": "omve",
                                "tex": f"\\times {read_group(cur)}"})
                elif name == "text":
                    # \text in prose (amstext accepts it): its content
                    emit_text()
                    out.extend(self.parse_inlines(read_group(cur)))
                elif name == "textcolor":
                    # a coloured row of a table: print emphasis only
                    read_group(cur)
                    emit_text()
                    out.extend(self.parse_inlines(read_group(cur)))
                elif name == "quad":
                    text.append(" ")
                elif name == "qquad":
                    text.append("  ")
                elif name in ("textsuperscript", "up"):
                    # \up{e}: babel-french's superscript (99\up{e} centile)
                    emit_text()
                    inner = read_group(cur)
                    out.append({"t": "sup", "inl": self.parse_inlines(inner)})
                elif name == "textsubscript":
                    # vitamin B\textsubscript{12}
                    emit_text()
                    inner = read_group(cur)
                    out.append({"t": "sub", "inl": self.parse_inlines(inner)})
                elif name == "footnote":
                    emit_text()
                    inner = read_group(cur)
                    out.append({"t": "footnote",
                                "inl": self.parse_inlines(inner)})
                elif name == "texorpdfstring":
                    # the TeX branch is what the book renders
                    emit_text()
                    tex_arg = read_group(cur)
                    read_group(cur)  # pdf-string branch, unused
                    out.extend(self.parse_inlines(tex_arg))
                elif name == "checkmark":
                    text.append("✓")
                elif name == "markboth":
                    read_group(cur)      # running heads (print-only)
                    read_group(cur)
                elif name == "chaptermark":
                    read_group(cur)      # a shorter running head (print-only)
                elif name == "slash":
                    text.append("/")     # a breakable slash in print
                elif name in ("hfill", "leavevmode", "centering",
                              "begingroup", "endgroup", "sloppy",
                              "vfill", "newpage", "nopagebreak",
                              "hfil", "break", "raggedright"):
                    pass  # print-layout commands: no HTML equivalent
                elif name == "ensuremath":
                    # \ensuremath{\mathrm{CO_2}} in prose = inline math
                    emit_text()
                    out.append({"t": "math", "tex": read_group(cur)})
                elif name == "hspace":
                    read_group(cur)
                    text.append(" ")
                elif name == "rule":
                    # struts like \rule{0pt}{11pt} (table row spacing)
                    read_group(cur)
                    read_group(cur)
                elif name == "small":
                    pass  # size switch inside a group; CSS owns sizing
                elif name == "textsc":
                    emit_text()
                    inner = read_group(cur)
                    out.append({"t": "sc",
                                "inl": self.parse_inlines(inner)})
                elif name == "linebreak":
                    text.append(" ")
                elif name == "guillemotleft":
                    text.append("\u00ab")
                elif name == "guillemotright":
                    text.append("\u00bb")
                elif name in ("oe", "OE"):
                    text.append("\u0153" if name == "oe" else "\u0152")
                elif name == "c":
                    # cedilla accent, braced or bare letter
                    text.append(self.accented_letter(cur, "\u0327"))
                elif name == "v":
                    # caron accent (\v{S}mulian, \v Smulian)
                    text.append(self.accented_letter(cur, "\u030c"))
                elif name == "H":
                    # Hungarian umlaut accent (Erd\H{o}s)
                    text.append(self.accented_letter(cur, "̋"))
                elif name in ("ce", "pu"):
                    # mhchem (chemistry books): one formula rendered by
                    # KaTeX's mhchem extension — an LTR island, as print's
                    # \babelsublr keeps it in the Arabic editions
                    emit_text()
                    out.append({"t": "math",
                                "tex": f"\\{name}{{{read_group(cur)}}}"})
                elif name == "cip":
                    # CIP descriptor: (R) with the italic letter
                    text.append("(")
                    emit_text()
                    out.append({"t": "emph", "index": None,
                                "inl": self.parse_inlines(read_group(cur))})
                    text.append(")")
                elif name in ("termsym", "kv"):
                    # term symbol ^3P_2 / Kröger-Vink V_O^{••}
                    a, b, c = [read_group(cur) for _ in range(3)]
                    emit_text()
                    tex = (f"{{}}^{{{a}}}\\mathrm{{{b}}}_{{{c}}}"
                           if name == "termsym" else
                           f"\\mathrm{{{a}}}_{{\\mathrm{{{b}}}}}^{{{c}}}")
                    out.append({"t": "math", "tex": tex})
                elif name in ("chemfig", "omorbs", "ghs", "tikz", "omlith",
                              "omwx"):
                    # a small picture in the running text (a structure,
                    # orbital boxes, a hazard pictogram, an atom model; a
                    # lithology swatch, a weather symbol)
                    emit_text()
                    out.append({"t": "pic", "src": self.chem_setup
                                + self.picture_command(cur, name)})
                elif name == "setchemfig":
                    self.chem_setup += "\\setchemfig{" + read_group(cur) + "}"
                elif name == "babelsublr":
                    # Arabic editions: a left-to-right run (the HTML's math
                    # islands are LTR already) — keep its content
                    emit_text()
                    out.extend(self.parse_inlines(read_group(cur)))
                elif name == "protect":
                    pass
                elif name == "enlargethispage":
                    read_group(cur)      # page-fitting hint (print-only)
                elif name == "foreignlanguage":
                    read_group(cur)      # the language: hyphenation only
                    emit_text()
                    out.extend(self.parse_inlines(read_group(cur)))
                elif name == "vspace":
                    # vertical spacing / a conditional page break (print)
                    if s.startswith("*", cur.i):
                        cur.i += 1
                    read_group(cur)
                elif name == "penalty":
                    m2 = re.match(r"\s*-?\d+\s*", s[cur.i:])
                    if not m2:
                        cur.err("unsupported \\penalty value")
                    cur.i += m2.end()
                elif name == "mbox":
                    # an unbreakable run: its text. \textdir TLT (Arabic
                    # editions) keeps a range or unit left to right, which
                    # the HTML must say too: "3–5" would flip otherwise
                    emit_text()
                    inner = read_group(cur)
                    m2 = re.match(r"\s*\\textdir\s*TLT\s*", inner)
                    if m2:
                        out.append({"t": "ltr", "inl": self.parse_inlines(
                            inner[m2.end():])})
                    else:
                        out.extend(self.parse_inlines(inner))
                elif name == "shortstack":
                    # stacked lines in a table head (Earth books)
                    if s.startswith("[", cur.i):
                        read_optional(cur)
                    emit_text()
                    out.extend(self.parse_inlines(
                        read_group(cur).replace("\\\\", "\\newline ")))
                elif name == "textminus":
                    text.append("\u2212")
                elif name == "textquotesingle":
                    text.append("'")     # straight, as in code
                elif name == "textasciitilde":
                    text.append("~")
                elif name == "textsterling":
                    text.append("\u00a3")
                elif name in ("footnotesize", "scriptsize"):
                    pass  # size switch inside a group; CSS owns sizing
                elif name == "begin" and s.startswith("{tabular}", cur.i):
                    # a one-column tabular inside a table cell (a hazard
                    # pictogram over its label): its rows, line-broken
                    cur.i += len("{tabular}")
                    read_optional(cur)
                    read_group(cur)          # colspec: layout only
                    rows = split_top_level(find_env_end(cur, "tabular"),
                                           "\\", self.filename)
                    emit_text()
                    for k, row in enumerate(rows):
                        row = re.sub(r"^\s*\[[^\]]*\]", "", row).strip()
                        if k and row:
                            out.append({"t": "br"})
                        out.extend(self.parse_inlines(row))
                elif name == "emergencystretch":
                    # paragraph-breaking tolerance (print-only)
                    m2 = re.match(r"\s*=?\s*[\d.]+\s*(em|pt)\s*", s[cur.i:])
                    if not m2:
                        cur.err("unsupported \\emergencystretch value")
                    cur.i += m2.end()
                elif name == "url":
                    emit_text()
                    out.append({"t": "code",
                                "inl": [{"t": "text", "s": read_group(cur)}]})
                else:
                    cur.err(f"unsupported command \\{name}")
                continue
            if c == "~":
                text.append(" ")
                cur.i += 1
                continue
            if s.startswith("---", cur.i):
                text.append("—")
                cur.i += 3
                continue
            if s.startswith("--", cur.i):
                text.append("–")
                cur.i += 2
                continue
            if s.startswith("``", cur.i):
                text.append("“")
                cur.i += 2
                continue
            if s.startswith("''", cur.i):
                text.append("”")
                cur.i += 2
                continue
            if c == "`":
                text.append("‘")
                cur.i += 1
                continue
            if c == "'":
                text.append("’")
                cur.i += 1
                continue
            m = ITSHAPE_GROUP.match(s, cur.i) if c == "{" else None
            if m:
                # {\small\itshape\color{omIq} Assessor: …} (quant mock
                # interviews): an italic aside; size and colour are print-only
                emit_text()
                inner = ITSHAPE_SWITCHES.sub("", read_group(cur), count=1)
                out.append({"t": "emph", "inl": self.parse_inlines(inner),
                            "index": None})
                continue
            if c in "{}":
                # bare group braces: transparent (e.g. {27} in prose)
                cur.i += 1
                continue
            text.append(c)
            cur.i += 1
        emit_text()
        return out


def expand_generated(text, path):
    """Interview books: inline the script-written files of a chapter
    (\\input{parts/<dir>/generated/<name>}) and expand \\ivscoreline, a macro
    for a whole table row. Any other \\input stays an error."""
    root = next((d.parent for d in Path(path).resolve().parents
                 if d.name == "parts"), None)

    def inline(m):
        target = root / (m.group(1) + ".tex")
        if not target.exists():
            raise ParseError(f"{path}: missing generated file {target}")
        return target.read_text(encoding="utf-8")
    if root is not None:
        text = re.sub(r"\\input\{(parts/[a-z0-9-]+/generated/[^{}]+)\}",
                      inline, text)
    # sloppypar: a paragraph with looser line breaking in print; it starts
    # and ends a paragraph, as blank lines do
    text = re.sub(r"\\(?:begin|end)\{sloppypar\}", "\n\n", text)
    return re.sub(r"\\ivscoreline\{([^{}]*)\}",
                  lambda m: m.group(1) + " & & & & & \\\\[8pt]\\hline", text)


def parse_chapter(path, iv=None):
    """Parse a chapter file; returns (title_inlines, chapter_label, blocks).
    `iv`: the interview books' localized run-in words (LangStrings)."""
    with open(path, encoding="utf-8") as f:
        text = expand_generated(f.read(), path)
    p = Parser(str(path), text, iv)
    blocks = p.parse()
    if p.chapter_title is None or p.chapter_label is None:
        raise ParseError(f"{path}: missing \\chapter{{...}}\\label{{...}}")
    return p.chapter_title, p.chapter_label, blocks


def parse_solutions(path, iv=None):
    """Parse a solutions file; returns dict sol_key -> body blocks."""
    with open(path, encoding="utf-8") as f:
        text = expand_generated(f.read(), path)
    # Drop the \section*{Chapter \ref{...} --- ...} header (it repeats the
    # chapter title and its \ref cannot be resolved standalone). The title
    # may span lines, so strip the balanced group, not a single line.
    m = re.match(r"\s*\\section\*", text)
    if m:
        cur = Cursor(text, str(path))
        cur.i = m.end()
        read_group(cur)
        text = text[cur.i:]
    p = Parser(str(path), text, iv)
    blocks = p.parse()
    solutions = {}
    for b in blocks:
        if b["t"] == "subsection" and b["star"]:
            continue    # a print heading of the solutions appendix
        if b["t"] != "env" or b["kind"] != "solution":
            raise ParseError(
                f"{path}: unexpected top-level content in solutions file")
        solutions[b["sol_key"]] = b["body"]
    return solutions
