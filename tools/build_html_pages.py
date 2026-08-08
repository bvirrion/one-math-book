#!/usr/bin/env python3
"""Extract printed-page maps for the online reader from LaTeX build files.

Usage (from the repo root, after `latexmk` has built the PDFs):

    python3 tools/build_html_pages.py \
        --entry one_math_book_2_high_school.tex \
        --book math-2 \
        --languages en,fr,nl,es,pt,hi \
        --build build \
        --out ../../saas/resources/onecourse/chapters

Reads build/<entry-stem>[_<lang>].aux (label -> printed page) and the
matching .toc (section/chapter/part -> page), joins them to the published
chapters in the reader manifest, and writes one sidecar file per language:

    <out>/pages/<book>/<lang>.json

mapping every HTML anchor the fragments already carry (ch-*, sec-N-M and
the manifest `labels` boxes/exercises) to its page in that language's PDF
edition. Solution labels never appear in the manifest, so appendix pages
are excluded automatically.

Strict on purpose, like build_html_toc.py: a label missing from the aux, a
chapter number disagreeing with the manifest, or an anchor landing outside
its chapter's page range aborts the run — rebuild the PDF or the HTML
instead of letting the script guess. Each language is built fully in
memory before anything is written.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from htmlbook.model import anchor_for  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

ARABIC = re.compile(r"^\d+$")


def fail(msg):
    sys.exit(f"error: {msg}")


def brace_groups(text, pos):
    """Successive balanced {...} groups starting at pos; returns (groups,
    end_pos). Stops at the first character that does not open a group."""
    groups = []
    while pos < len(text) and text[pos] == "{":
        depth, start = 0, pos
        while pos < len(text):
            ch = text[pos]
            if ch == "\\":
                pos += 2
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
            pos += 1
        if depth != 0:
            fail(f"unbalanced braces in {text!r}")
        groups.append(text[start + 1:pos])
        pos += 1
        while pos < len(text) and text[pos] == " ":
            pos += 1
    return groups, pos


def parse_aux(path):
    """{label: (number, page)} for arabic-paged \\newlabel entries, plus
    the maximum arabic page seen across ALL labels (solutions included)."""
    pages, max_page = {}, 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("\\newlabel{"):
            continue
        groups, _ = brace_groups(line, len("\\newlabel"))
        if len(groups) != 2:
            continue
        label, payload = groups
        if "@" in label:  # cleveref @cref twins
            continue
        fields, _ = brace_groups(payload, 0)
        if len(fields) < 2 or not ARABIC.match(fields[1]):
            continue  # roman front-matter pages
        pages[label] = (fields[0], int(fields[1]))
        max_page = max(max_page, int(fields[1]))
    if not pages:
        fail(f"{path}: no arabic-paged \\newlabel entries found")
    return pages, max_page


def parse_toc(path):
    """Ordered [(kind, number_or_None, page)] for arabic-paged part /
    chapter / section lines (appendix and unnumbered chapters included:
    they bound the last real chapter's page range)."""
    parsed = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\\contentsline \{(part|chapter|section)\}", line)
        if not m:
            continue
        kind = m.group(1)
        groups, _ = brace_groups(line, line.index("}") + 1)
        if len(groups) < 2:
            fail(f"{path}: cannot parse contentsline: {line!r}")
        title, page = groups[0], groups[1]
        if not ARABIC.match(page):
            continue
        number = None
        nm = re.match(r"\\numberline \{([^{}]*)\}", title)
        if nm:
            number = nm.group(1)
        parsed.append((kind, number, int(page)))
    if not parsed:
        fail(f"{path}: no arabic-paged contentsline entries found")
    return parsed


def build_language(book, lang, chapters, aux_path, toc_path):
    """The pages/<book>/<lang>.json payload, fully validated."""
    aux, aux_max = parse_aux(aux_path)
    toc = parse_toc(toc_path)
    total_pages = max(aux_max, max(p for _, _, p in toc))

    # Chapter boundaries: ordered chapter/part toc entries.
    bounds = [(number, page) for kind, number, page in toc
              if kind in ("chapter", "part")]

    out, prev_start = {}, 0
    for chapter in sorted(chapters, key=lambda c: c["number"]):
        key, number, ch_label = chapter["key"], chapter["number"], chapter["label"]
        if ch_label not in aux:
            fail(f"{aux_path.name}: chapter label {ch_label!r} not in aux — "
                 "rebuild the PDF (latexmk) or the HTML")
        aux_number, start = aux[ch_label]
        if aux_number != str(number):
            fail(f"{aux_path.name}: {ch_label!r} is chapter {aux_number} in "
                 f"the PDF but {number} in the manifest — renumbering drift")
        if start <= prev_start:
            fail(f"{aux_path.name}: chapter {key!r} starts on page {start}, "
                 f"not after the previous chapter ({prev_start})")
        prev_start = start

        # end = next chapter/part boundary after this chapter's own entry
        idx = next((i for i, (n, _) in enumerate(bounds) if n == str(number)),
                   None)
        if idx is None:
            fail(f"{toc_path.name}: chapter {number} has no toc line")
        end = total_pages
        if idx + 1 < len(bounds):
            end = max(start, bounds[idx + 1][1] - 1)

        anchors = {f"ch-{key}": start}
        for label in chapter["labels"]:
            if label not in aux:
                fail(f"{aux_path.name}: label {label!r} (chapter {key}) not "
                     "in aux — label drift, rebuild the PDF or the HTML")
            page = aux[label][1]
            if not start <= page <= end:
                fail(f"{aux_path.name}: label {label!r} on page {page}, "
                     f"outside chapter {key!r} range {start}-{end}")
            anchors[anchor_for(label)] = page

        # Sections from the toc: numbers N.M with N == chapter number map
        # to the fragment ids sec-N-M (emit_html numbers h2 ids by the
        # LaTeX section counter, so starred sections — headings without a
        # toc line — never shift the mapping). Validate against the
        # manifest headings: numbered toc sections can't exceed them.
        headings = chapter["languages"].get(lang, {}).get("headings")
        if headings is None:
            fail(f"manifest: chapter {key!r} has no {lang!r} edition")
        sections = [(n, p) for kind, n, p in toc
                    if kind == "section" and n
                    and n.split(".")[0] == str(number)]
        if len(sections) > len(headings):
            fail(f"{toc_path.name}: chapter {key!r} has {len(sections)} "
                 f"toc sections but only {len(headings)} headings in the "
                 f"manifest [{lang}] — stale PDF or HTML, rebuild")
        for i, (n, page) in enumerate(sections, start=1):
            m = n.split(".", 1)[1]
            if m != str(i):
                fail(f"{toc_path.name}: toc section {n!r} is the {i}th "
                     f"numbered section of chapter {key!r} — non-"
                     "sequential numbering, extend build_html_pages.py")
            if not start <= page <= end:
                fail(f"{toc_path.name}: section {n} on page {page}, "
                     f"outside chapter {key!r} range {start}-{end}")
            anchors[f"sec-{number}-{m}"] = page
        if headings and not sections:
            print(f"notice: {toc_path.name}: chapter {key!r} has no toc "
                  "sections — sec-* anchors skipped")

        out[key] = {"start": start, "end": end, "anchors": anchors}

    return {
        "book": book,
        "language": lang,
        "source": aux_path.name,
        "total_pages": total_pages,
        "chapters": out,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entry", required=True,
                    help="book entry file, e.g. one_math_book_2_high_school.tex")
    ap.add_argument("--book", required=True, help="manifest book key")
    ap.add_argument("--languages", default="en,fr,nl,es,pt,hi")
    ap.add_argument("--build", default="build",
                    help="LaTeX output directory holding the .aux/.toc files")
    ap.add_argument("--out", required=True,
                    help="directory containing manifest.json")
    args = ap.parse_args()

    langs = [lang.strip() for lang in args.languages.split(",")]
    manifest_path = Path(args.out) / "manifest.json"
    if not manifest_path.exists():
        fail(f"{manifest_path} not found — run build_html_chapter.py first")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    chapters = manifest["books"].get(args.book, {}).get("chapters")
    if not chapters:
        fail(f"book {args.book!r} has no published chapters in the manifest")

    stem = Path(args.entry).stem
    build_dir = REPO_ROOT / args.build

    payloads = {}
    for lang in langs:  # everything validated before anything is written
        suffix = "" if lang == "en" else f"_{lang}"
        aux_path = build_dir / f"{stem}{suffix}.aux"
        toc_path = build_dir / f"{stem}{suffix}.toc"
        for path in (aux_path, toc_path):
            if not path.exists():
                fail(f"{path} not found — run latexmk for the {lang!r} "
                     "edition first")
        payloads[lang] = build_language(args.book, lang, chapters,
                                        aux_path, toc_path)

    pages_dir = Path(args.out) / "pages" / args.book
    pages_dir.mkdir(parents=True, exist_ok=True)
    for lang, payload in payloads.items():
        path = pages_dir / f"{lang}.json"
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
            + "\n",
            encoding="utf-8")
        n_anchors = sum(len(c["anchors"])
                        for c in payload["chapters"].values())
        print(f"pages [{lang}]: {len(payload['chapters'])} chapters, "
              f"{n_anchors} anchors, {payload['total_pages']} pages "
              f"-> {path}")


if __name__ == "__main__":
    main()
