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

STATEMENT_KINDS = (
    "definition", "theorem", "proposition", "lemma", "corollary",
    "method", "example", "notation", "remark",
)
# Environments whose bodies are parsed recursively as blocks.
BLOCK_ENVS = STATEMENT_KINDS + ("proof", "exercise", "problem", "solution")
LIST_ENVS = ("itemize", "enumerate")


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
    """Remove unescaped %-comments (keep the newline)."""
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


def read_group(cur):
    """Read a balanced {...} group; cursor must be on '{'. Returns content."""
    s = cur.s
    if s[cur.i] != "{":
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


def count_stars(opt):
    """Difficulty option like `$\\star$` / `$\\star\\star\\star$` -> 1..3."""
    return opt.count("\\star")


class Parser:
    def __init__(self, filename, text):
        self.filename = filename
        self.chapter_title = None      # inline list
        self.chapter_label = None
        text = strip_comments(text)
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
                end = cur.i
                while True:
                    end = s.find("$", end + 1)
                    if end < 0:
                        cur.err("unbalanced $")
                    if s[end - 1] != "\\":
                        break
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
                if s.startswith("\\chapter{", cur.i):
                    flush()
                    cur.i += len("\\chapter")
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
                m = re.match(r"\\admitted\b", s[cur.i:])
                if m:
                    # zero-arg macro: a whole "Admitted at this level" proof
                    flush()
                    blocks.append({"t": "admitted"})
                    cur.i += m.end()
                    continue
                m = re.match(r"\\(medskip|smallskip|bigskip|noindent|par)\b",
                             s[cur.i:])
                if m:
                    # purely presentational in print; paragraph flow in HTML
                    if m.group(1) != "noindent":
                        flush()
                    cur.i += m.end()
                    continue
                if s.startswith("\\label{", cur.i):
                    cur.i += len("\\label")
                    label = read_group(cur)
                    if self.chapter_label is None and not blocks and not parbuf:
                        self.chapter_label = label
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
                        "emph": 1, "textbf": 1, "index": 1, "label": 1,
                        "textsuperscript": 1, "footnote": 1,
                        "texorpdfstring": 2, "hspace": 1, "rule": 2,
                        "H": 1, "c": 1, "textsc": 1}.get(name, 0)
            out = [s[start:cur.i]]
            for _ in range(n_groups):
                while cur.i < len(s) and s[cur.i] in " \n":
                    cur.i += 1
                out.append("{" + read_group(cur) + "}")
            return "".join(out)
        # escaped char like \, \\ \& \% \_ or "\ "
        out = s[cur.i:cur.i + 2]
        cur.i += 2
        return out

    # ------------------------------------------------------------------ envs

    def parse_env(self, cur):
        s = cur.s
        cur.i += len("\\begin")
        name = read_group(cur)

        if name in ("align*", "gather*"):
            # display-math blocks; KaTeX renders them natively in display
            # mode, so keep the whole environment verbatim
            body = find_env_end(cur, name)
            return {"t": "dmath",
                    "tex": f"\\begin{{{name}}}" + body + f"\\end{{{name}}}"}
        if name == "omfigure":
            body = find_env_end(cur, "omfigure")
            return self.parse_figure(body)
        if name == "figure":
            read_optional(cur)  # float placement ([ht]...): print-only
            body = find_env_end(cur, "figure")
            return self.parse_figure(body, floated=True)
        if name == "center":
            body = find_env_end(cur, "center")
            return self.parse_center(body)
        if name in LIST_ENVS:
            opt = read_optional(cur)
            resume = bool(opt) and "resume" in opt
            if opt and opt.strip() not in ("resume",):
                raise ParseError(
                    f"{self.filename}: unsupported list option [{opt}]")
            body = find_env_end(cur, name)
            chunks = split_top_level(body, "item", self.filename)
            if chunks[0].strip():
                raise ParseError(
                    f"{self.filename}: text before first \\item in {name}")
            items = [self.parse_blocks(cchunk) for cchunk in chunks[1:]]
            return {"t": "list", "kind": name, "resume": resume,
                    "items": items}
        if name in BLOCK_ENVS:
            title, sol_key, difficulty = None, None, None
            if name == "solution":
                sol_key = read_group(cur)
            else:
                opt = read_optional(cur)
                if opt is not None:
                    if name == "exercise":
                        difficulty = count_stars(opt)
                        if difficulty == 0:
                            raise ParseError(
                                f"{self.filename}: exercise option {opt!r} "
                                "is not a star difficulty")
                    else:
                        o = opt.strip()
                        if o.startswith("{") and o.endswith("}"):
                            o = o[1:-1]
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
            return {"t": "env", "kind": name, "title": title, "label": label,
                    "difficulty": difficulty, "sol_key": sol_key,
                    "body": body_blocks}
        cur.err(f"unknown environment {name!r}")

    def parse_figure(self, body, floated=False):
        """An omfigure holds one or more tikzpictures (side-by-side plots
        are two pictures separated by \\qquad) plus a {\\small ...} caption."""
        tikzs = []
        end_pat = "\\end{tikzpicture}"
        rest = body
        while True:
            m = re.search(r"\\begin\{tikzpicture\}", rest)
            if not m:
                break
            e = rest.find(end_pat, m.start())
            if e < 0:
                raise ParseError(
                    f"{self.filename}: missing \\end{{tikzpicture}}")
            tikzs.append(rest[m.start():e + len(end_pat)])
            rest = rest[:m.start()] + rest[e + len(end_pat):]
        if not tikzs:
            raise ParseError(f"{self.filename}: omfigure without tikzpicture")
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
        caption = re.sub(r"\\qquad|\\quad|\\hfill", " ", rest).strip()
        m2 = re.fullmatch(r"\{\\small\s+(.*)\}", caption, re.S)
        if m2:
            caption = m2.group(1)
        return {"t": "figure", "tikzs": tikzs, "label": None,
                "caption": self.parse_inlines(caption)}

    def parse_center(self, body):
        """A center block holds one or more tabulars (side-by-side tables
        are separated by \\qquad), optionally after an \\arraystretch
        row-height tweak (print-only; CSS handles it in HTML)."""
        body = body.strip()
        body = re.sub(r"^\\renewcommand\{\\arraystretch\}\{[\d.]+\}\s*",
                      "", body)
        body = re.sub(r"^\\small\s+", "", body)  # print-only sizing
        tables = []
        cur = Cursor(body, self.filename)
        while True:
            rest = cur.s[cur.i:]
            stripped = re.match(r"(\s|\\qquad\b|\\quad\b)*", rest).end()
            cur.i += stripped
            if cur.i >= len(cur.s):
                break
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
        for raw in rows_raw:
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
        return {"t": "table", "colspec": colspec, "header": header,
                "rows": rows}

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
                cells.append(self.parse_inlines("".join(buf).strip()))
                buf = []
                i += 1
                continue
            buf.append(c)
            i += 1
        cells.append(self.parse_inlines("".join(buf).strip()))
        return cells

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
                end = s.find("$", cur.i + 1)
                if end < 0:
                    cur.err("unbalanced $")
                emit_text()
                out.append({"t": "math", "tex": s[cur.i + 1:end].strip()})
                cur.i = end + 1
                continue
            if c == "\\":
                m = CMD_RE.match(s, cur.i)
                if not m:
                    nxt = s[cur.i + 1:cur.i + 2]
                    following = s[cur.i + 2:cur.i + 3]
                    if nxt in ("'", "`", "^", '"', "~") \
                            and (following.isalpha() or following == "{"):
                        # accents in prose, bare (\'e) or braced (\'{e})
                        import unicodedata
                        combining = {"'": "\u0301", "`": "\u0300",
                                     "^": "\u0302", '"': "\u0308",
                                     "~": "\u0303"}[nxt]
                        if following == "{":
                            cur.i += 2
                            letter = read_group(cur)
                            if len(letter) != 1 or not letter.isalpha():
                                cur.err(f"unsupported accent argument "
                                        f"{letter!r}")
                        else:
                            letter = following
                            cur.i += 3
                        text.append(unicodedata.normalize(
                            "NFC", letter + combining))
                        continue
                    if nxt in (" ", "\n", ""):    # "\ " explicit space
                        # ("" = trailing "\<newline>" whose newline was
                        # stripped at a paragraph boundary)
                        text.append(" ")
                    elif nxt == ",":               # thin space
                        text.append(" ")
                    elif nxt in ("%", "&", "_", "#", "$"):
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
                elif name == "emph":
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
                elif name == "index":
                    # standalone index entry: metadata only, no visible text
                    read_group(cur)
                elif name in ("dots", "ldots"):
                    text.append("…")
                elif name == "quad":
                    text.append(" ")
                elif name == "qquad":
                    text.append("  ")
                elif name == "textsuperscript":
                    emit_text()
                    inner = read_group(cur)
                    out.append({"t": "sup", "inl": self.parse_inlines(inner)})
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
                elif name in ("hfill", "leavevmode", "centering"):
                    pass  # print-layout commands: no HTML equivalent
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
                    # cedilla accent: \c{c} -> c-cedilla
                    import unicodedata
                    inner = read_group(cur)
                    if len(inner) != 1 or not inner.isalpha():
                        cur.err(f"unsupported \\c{{{inner}}}")
                    text.append(unicodedata.normalize(
                        "NFC", inner + "\u0327"))
                elif name == "H":
                    # Hungarian umlaut accent (Erd\H{o}s)
                    inner = read_group(cur)
                    mapped = {"o": "ő", "O": "Ő", "u": "ű", "U": "Ű"}
                    if inner not in mapped:
                        cur.err(f"unsupported \\H{{{inner}}}")
                    text.append(mapped[inner])
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
            if c in "{}":
                # bare group braces: transparent (e.g. {27} in prose)
                cur.i += 1
                continue
            text.append(c)
            cur.i += 1
        emit_text()
        return out


def parse_chapter(path):
    """Parse a chapter file; returns (title_inlines, chapter_label, blocks)."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    p = Parser(str(path), text)
    blocks = p.parse()
    if p.chapter_title is None or p.chapter_label is None:
        raise ParseError(f"{path}: missing \\chapter{{...}}\\label{{...}}")
    return p.chapter_title, p.chapter_label, blocks


def parse_solutions(path):
    """Parse a solutions file; returns dict sol_key -> body blocks."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # Drop the \section*{Chapter \ref{...} --- ...} header (it repeats the
    # chapter title and its \ref cannot be resolved standalone). The title
    # may span lines, so strip the balanced group, not a single line.
    m = re.match(r"\s*\\section\*", text)
    if m:
        cur = Cursor(text, str(path))
        cur.i = m.end()
        read_group(cur)
        text = text[cur.i:]
    p = Parser(str(path), text)
    blocks = p.parse()
    solutions = {}
    for b in blocks:
        if b["t"] != "env" or b["kind"] != "solution":
            raise ParseError(
                f"{path}: unexpected top-level content in solutions file")
        solutions[b["sol_key"]] = b["body"]
    return solutions
