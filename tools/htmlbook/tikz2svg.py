"""Compile a tikzpicture to SVG (text as paths, so no font dependencies).

Each figure is compiled standalone with the same colors and math macros as
styles/onemath.sty, then converted with dvisvgm --pdf --no-fonts, falling
back to pdftocairo -svg. Figures are keyed by a content hash so identical
pictures across language editions build once.
"""

import hashlib
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from .lexer import ParseError

# Mirrors the color and math-macro blocks of styles/onemath.sty. If a figure
# uses something missing here, pdflatex errors and the build stops — the
# fail-loudly contract, not silent drift.
PREAMBLE = r"""
\documentclass[tikz]{standalone}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepgfplotslibrary{fillbetween}
\usetikzlibrary{arrows.meta,calc,angles,quotes,patterns}
\usetikzlibrary{shapes.geometric,shapes.misc,fit,backgrounds,matrix}
\pgfplotsset{
  omaxis/.style={
    axis lines=middle,
    tick label style={font=\small},
    label style={font=\small},
    xlabel={$x$}, ylabel={$y$},
    xlabel style={below right}, ylabel style={above left},
    samples=100,
  },
}
\definecolor{omDef}{RGB}{0,84,147}
\definecolor{omThm}{RGB}{150,20,30}
\definecolor{omProp}{RGB}{190,90,20}
\definecolor{omMeth}{RGB}{20,110,60}
\definecolor{omExo}{RGB}{80,80,80}
\definecolor{ocMint}{HTML}{06D6A0}
\definecolor{ocYellow}{HTML}{FFD166}
\definecolor{ocRed}{HTML}{EF476F}
\definecolor{ocBlue}{HTML}{118AB2}
\definecolor{ocInk}{HTML}{1F2430}
\colorlet{ocPaleBlue}{ocBlue!14!white}
\colorlet{ocDarkBlue}{ocBlue!80!black}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\Q}{\mathbb{Q}}
\newcommand{\R}{\mathbb{R}}
\newcommand{\C}{\mathbb{C}}
\DeclarePairedDelimiter{\abs}{\lvert}{\rvert}
\DeclarePairedDelimiter{\norm}{\lVert}{\rVert}
\DeclarePairedDelimiter{\floor}{\lfloor}{\rfloor}
\newcommand{\intcc}[2]{\left[#1,\,#2\right]}
\newcommand{\intoo}[2]{\left(#1,\,#2\right)}
\newcommand{\intco}[2]{\left[#1,\,#2\right)}
\newcommand{\intoc}[2]{\left(#1,\,#2\right]}
\newcommand{\intint}[2]{[\![#1,\,#2]\!]}
\newcommand{\dd}{\mathop{}\!\mathrm{d}}
% Defined-term links (\omterm, from link_defined_terms.py) can land inside
% figure text; in an SVG they render as their display text.
\providecommand{\omterm}[2]{#2}
\newcommand{\eu}{\mathrm{e}}
\newcommand{\iu}{\mathrm{i}}
\newcommand{\vect}[1]{\overrightarrow{#1}}
\newcommand{\scal}[2]{\vect{#1}\cdot\vect{#2}}
\newcommand{\conj}[1]{\overline{#1}}
\renewcommand{\P}{\mathbb{P}}
\newcommand{\E}{\mathbb{E}}
\newcommand{\V}{\mathbb{V}}
\newcommand{\pcond}[2]{\P_{#1}\!\left(#2\right)}
\DeclareMathOperator{\Rea}{Re}
\DeclareMathOperator{\Ima}{Im}
\DeclareMathOperator{\Arg}{arg}
\DeclareMathOperator{\lcm}{lcm}
\begin{document}
"""

# Figures whose source contains Devanagari (localized node text in hi
# editions) cannot go through pdfTeX; they compile with XeLaTeX and the
# same bundled font the Hindi book uses. Latin-script figures stay on the
# historical pdflatex path so their SVGs are byte-stable.
DEVANAGARI = re.compile(r"[ऀ-ॿ]")

# Figures with Arabic node text need the same stack as the Arabic book
# itself: LuaLaTeX + babel's Lua bidi (bidi=basic), with layout=graphics so
# the pgfpicture is not mirrored and only the node text reads RTL
# (onemath.sty documents why XeTeX's "bidi" package is not an option).
# onchar=ids fonts applies the Arabic font and direction to Arabic runs
# inside the otherwise-LTR standalone document. Static faces only — the
# variable font segfaults LuaHBTeX on musl (see arabic_style_card.md).
ARABIC = re.compile(r"[؀-ۿ]")

FONTS_DIR = Path(__file__).resolve().parents[2] / "assets" / "fonts"

FONTSPEC_BLOCK = rf"""\usepackage{{fontspec}}
\setmainfont{{NotoSansDevanagari}}[
  Path={FONTS_DIR}/,
  Extension=.ttf,
  UprightFont=*-Regular,
  BoldFont=*-Bold,
  ItalicFont=*-Regular,
  BoldItalicFont=*-Bold,
  Script=Devanagari,
]
"""

ARABIC_BLOCK = r"""\usepackage[bidi=basic,layout=graphics]{babel}
\babelprovide[onchar=ids fonts]{arabic}
\babelfont[arabic]{rm}[
  Path=./,
  Extension=.ttf,
  UprightFont=*-Regular,
  BoldFont=*-Bold,
  ItalicFont=*-Regular,
  BoldItalicFont=*-Bold,
  SmallCapsFont=*-Regular,
  Script=Arabic,
]{NotoNaskhArabic}
"""

# The faces named in ARABIC_BLOCK, copied beside fig.tex before compiling:
# this luaotfload (3.18) resolves the bracketed [Path/file] lookup only
# relative to the cwd — with an absolute Path= the PDF backend dies at
# ship-out with "cannot find file ''".
ARABIC_FACES = ("NotoNaskhArabic-Regular.ttf", "NotoNaskhArabic-Bold.ttf")


def tikz_hash(tikz):
    normalized = re.sub(r"\s+", " ", tikz).strip()
    # pictures embedded in the tikz (\\includegraphics inside a node, the
    # biology label overlays) are part of the figure: key on their bytes too
    for m in RASTER_RE.finditer(tikz):
        path = Path(m.group(2).strip())
        if path.exists():
            normalized += hashlib.sha1(path.read_bytes()).hexdigest()
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:12]


def stage_rasters(tikz, tmp):
    """Rewrite \\includegraphics inside a tikzpicture to web-sized JPEGs
    copied beside fig.tex (the compile runs in a temp dir, and the
    embedded bitmap should be as light as a standalone photo)."""
    def repl(m):
        opts, path = m.group(1), m.group(2).strip()
        data, _, _ = build_raster(path, "")
        name = f"img-{hashlib.sha1(data).hexdigest()[:12]}.jpg"
        (tmp / name).write_bytes(data)
        return "\\includegraphics" + (f"[{opts}]" if opts else "") \
            + "{" + name + "}"
    return RASTER_RE.sub(repl, tikz)


def _run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          errors="replace")


def build_svg(tikz):
    """Compile one tikzpicture; returns (svg_text, width_px, height_px)."""
    with tempfile.TemporaryDirectory(prefix="omfig-") as tmp:
        tmp = Path(tmp)
        preamble, engine = PREAMBLE, "pdflatex"
        if DEVANAGARI.search(tikz):
            preamble = PREAMBLE.replace(
                "\\begin{document}", FONTSPEC_BLOCK + "\\begin{document}")
            engine = "xelatex"
        elif ARABIC.search(tikz):
            preamble = PREAMBLE.replace(
                "\\begin{document}", ARABIC_BLOCK + "\\begin{document}")
            engine = "lualatex"
            for face in ARABIC_FACES:
                shutil.copy(FONTS_DIR / face, tmp / face)
        has_raster = bool(RASTER_RE.search(tikz))
        if has_raster:
            tikz = stage_rasters(tikz, tmp)
        (tmp / "fig.tex").write_text(
            preamble + tikz + "\n\\end{document}\n", encoding="utf-8")
        res = _run([engine, "-interaction=nonstopmode", "fig.tex"], tmp)
        if res.returncode != 0 or not (tmp / "fig.pdf").exists():
            tail = res.stdout[-2500:]
            raise ParseError(f"{engine} failed for a figure:\n{tail}")

        svg_path = tmp / "fig.svg"
        res = _run(["dvisvgm", "--pdf", "--no-fonts", "--exact-bbox",
                    "-o", str(svg_path), "fig.pdf"], tmp)
        if has_raster and svg_path.exists() \
                and "<image" not in svg_path.read_text(encoding="utf-8"):
            # dvisvgm dropped the embedded bitmap: let cairo embed it
            svg_path.unlink()
            res = _run(["pdftocairo", "-svg", "fig.pdf", str(svg_path)], tmp)
        if res.returncode != 0 or not svg_path.exists():
            res = _run(["pdftocairo", "-svg", "fig.pdf", str(svg_path)], tmp)
            if res.returncode != 0 or not svg_path.exists():
                raise ParseError(
                    "both dvisvgm and pdftocairo failed to convert a "
                    f"figure:\n{res.stderr[-2000:]}")
        svg = svg_path.read_text(encoding="utf-8")
        return svg, *_svg_size(svg)


def _svg_size(svg):
    """Width/height in CSS px (1pt = 4/3 px), from the SVG root element."""
    m = re.search(r"<svg[^>]*>", svg)
    if not m:
        raise ParseError("no <svg> root element in converted figure")
    root = m.group(0)

    def dim(name):
        dm = re.search(rf"""{name}=["']([\d.]+)(pt|px)?["']""", root)
        if not dm:
            raise ParseError(f"figure SVG has no {name} attribute")
        value = float(dm.group(1))
        if dm.group(2) != "px":
            value *= 4.0 / 3.0
        return round(value)

    return dim("width"), dim("height")


RASTER_MAX_WIDTH = 1200   # px; photos are downscaled to at most this
RASTER_RE = re.compile(r"\\includegraphics(?:\[((?:[^\[\]{}]|\{[^{}]*\})*)\])?\s*\{([^{}]*)\}")


def is_raster(source):
    return source.lstrip().startswith("\\includegraphics")


def raster_sizing(source):
    """Print sizing hint carried into the HTML: `width=0.52\\linewidth` →
    {"rel_width": 0.52}; `height=3.1cm` → {"height_cm": 3.1}; else {}."""
    m = RASTER_RE.fullmatch(source.strip())
    opts = (m and m.group(1)) or ""
    mw = re.search(r"width\s*=\s*([\d.]+)\s*\\(?:line|text|column)width",
                   opts)
    if mw:
        return {"rel_width": float(mw.group(1))}
    mh = re.search(r"height\s*=\s*([\d.]+)\s*(cm|mm)", opts)
    if mh:
        h = float(mh.group(1)) / (10 if mh.group(2) == "mm" else 1)
        return {"height_cm": h}
    return {}


def raster_trim(opts):
    """`trim={l b r t}, clip` (bp; graphicx order left-bottom-right-top) →
    an ffmpeg crop filter. Photos carry no density, so 1 bp = 1 px, which
    is exactly how pdfTeX sizes them (a 1280 px jpg is 1280 bp wide)."""
    if not re.search(r"\bclip\b", opts or ""):
        return None
    m = re.search(r"trim\s*=\s*\{?\s*([\d.]+)bp\s+([\d.]+)bp\s+([\d.]+)bp"
                  r"\s+([\d.]+)bp\s*\}?", opts)
    if m:
        l, b, r, t = (float(v) for v in m.groups())
        return f"crop=iw-{l + r}:ih-{t + b}:{l}:{t}"
    # `viewport=llx lly urx ury` (bp, bottom-left origin): the kept box is
    # (urx-llx) x (ury-lly) with its top edge at ih-ury in ffmpeg's
    # top-left coordinates.
    m = re.search(r"viewport\s*=\s*\{?\s*([\d.]+)(?:bp)?\s+([\d.]+)(?:bp)?"
                  r"\s+([\d.]+)(?:bp)?\s+([\d.]+)(?:bp)?\s*\}?", opts)
    if not m:
        raise ParseError(f"unsupported clip/trim option: [{opts}]")
    llx, lly, urx, ury = (float(v) for v in m.groups())
    return f"crop={urx - llx}:{ury - lly}:{llx}:ih-{ury}"


def build_raster(path, opts=""):
    """Transcode a photo (jpg/png) to a web-sized JPEG with ffmpeg; returns
    (jpeg_bytes, width, height). Rasters are keyed by the hash of the
    source file (+ crop) so an unchanged photo is never re-encoded."""
    src = Path(path).resolve()
    if not src.exists():
        raise ParseError(f"raster figure not found: {path}")
    filters = [f for f in (raster_trim(opts),
                           f"scale='min({RASTER_MAX_WIDTH},iw)':-2") if f]
    with tempfile.TemporaryDirectory(prefix="omimg-") as tmp:
        out = Path(tmp) / "img.jpg"
        res = _run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src),
                    "-vf", ",".join(filters),
                    "-q:v", "3", "-pix_fmt", "yuvj420p", str(out)], tmp)
        if res.returncode != 0 or not out.exists():
            raise ParseError(f"ffmpeg failed for {path}:\n{res.stderr[-1500:]}")
        data = out.read_bytes()
    return data, *_jpeg_size(data)


def _jpeg_size(data):
    """(width, height) from the first SOF marker of a JPEG stream."""
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg = int.from_bytes(data[i + 2:i + 4], "big")
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h = int.from_bytes(data[i + 5:i + 7], "big")
            w = int.from_bytes(data[i + 7:i + 9], "big")
            return w, h
        i += 2 + seg
    raise ParseError("could not read JPEG dimensions")


class FigureBuilder:
    """Builds each distinct picture once: tikzpictures compile to SVG,
    \\includegraphics photos transcode to JPEG; both land in svg_dir."""

    def __init__(self, svg_dir, url_prefix):
        self.svg_dir = Path(svg_dir)
        self.url_prefix = url_prefix.rstrip("/")
        self.cache = {}    # tikz source -> figure info dict

    def figure_info(self, tikz):
        if tikz in self.cache:
            return self.cache[tikz]
        if is_raster(tikz):
            return self.raster_info(tikz)
        h = tikz_hash(tikz)
        # identical picture, differently keyed source (whitespace): reuse
        for info in self.cache.values():
            if info["hash"] == h:
                self.cache[tikz] = info
                return info
        svg, width, height = build_svg(tikz)
        self.svg_dir.mkdir(parents=True, exist_ok=True)
        filename = f"fig-{h}.svg"
        (self.svg_dir / filename).write_text(svg, encoding="utf-8")
        info = {"hash": h, "file": filename, "width": width,
                "height": height, "url": f"{self.url_prefix}/{filename}"}
        self.cache[tikz] = info
        return info

    def raster_info(self, source):
        m = RASTER_RE.fullmatch(source.strip())
        if not m:
            raise ParseError(f"malformed \\includegraphics: {source!r}")
        opts = m.group(1) or ""
        path = Path(m.group(2).strip())   # relative to the book repo root
        if not path.exists():
            raise ParseError(f"raster figure not found: {path}")
        crop = raster_trim(opts) or ""
        h = hashlib.sha1(path.read_bytes() + crop.encode()).hexdigest()[:12]
        sizing = raster_sizing(source)
        for info in self.cache.values():
            if info["hash"] == h:
                info = {k: v for k, v in info.items()
                        if k not in ("rel_width", "height_cm")}
                info.update(sizing)
                self.cache[source] = info
                return info
        filename = f"img-{h}.jpg"
        target = self.svg_dir / filename
        if target.exists():
            width, height = _jpeg_size(target.read_bytes())
        else:
            data, width, height = build_raster(path, opts)
            self.svg_dir.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        info = {"hash": h, "file": filename, "width": width,
                "height": height, "url": f"{self.url_prefix}/{filename}",
                **sizing}
        self.cache[source] = info
        return info
