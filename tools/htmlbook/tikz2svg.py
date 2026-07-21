"""Compile a tikzpicture to SVG (text as paths, so no font dependencies).

Each figure is compiled standalone with the same colors and math macros as
styles/onemath.sty, then converted with dvisvgm --pdf --no-fonts, falling
back to pdftocairo -svg. Figures are keyed by a content hash so identical
pictures across language editions build once.
"""

import hashlib
import re
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


def tikz_hash(tikz):
    normalized = re.sub(r"\s+", " ", tikz).strip()
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:12]


def _run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def build_svg(tikz):
    """Compile one tikzpicture; returns (svg_text, width_px, height_px)."""
    with tempfile.TemporaryDirectory(prefix="omfig-") as tmp:
        tmp = Path(tmp)
        (tmp / "fig.tex").write_text(
            PREAMBLE + tikz + "\n\\end{document}\n", encoding="utf-8")
        res = _run(["pdflatex", "-interaction=nonstopmode", "fig.tex"], tmp)
        if res.returncode != 0 or not (tmp / "fig.pdf").exists():
            tail = res.stdout[-2500:]
            raise ParseError(f"pdflatex failed for a figure:\n{tail}")

        svg_path = tmp / "fig.svg"
        res = _run(["dvisvgm", "--pdf", "--no-fonts", "--exact-bbox",
                    "-o", str(svg_path), "fig.pdf"], tmp)
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


class FigureBuilder:
    """Builds each distinct tikzpicture once, writes SVGs into svg_dir."""

    def __init__(self, svg_dir, url_prefix):
        self.svg_dir = Path(svg_dir)
        self.url_prefix = url_prefix.rstrip("/")
        self.cache = {}    # tikz source -> figure info dict

    def figure_info(self, tikz):
        if tikz in self.cache:
            return self.cache[tikz]
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
