#!/usr/bin/env bash
# Build every chapter of a book for the online reader: a --labels-only
# pre-pass (so cross-chapter references, including forward ones, resolve),
# then the full conversion in part order, then the toc. Failures don't
# stop the batch — they are listed at the end so the converter can be
# extended and just those chapters re-run with build_html_chapter.py.
#
# Usage: bash tools/build_html_book.sh <entry.tex> <book-key> /path/to/saas
#   e.g. bash tools/build_html_book.sh one_math_book_2_high_school.tex math-2 ../../saas
set -u
ENTRY="${1:?usage: build_html_book.sh <entry.tex> <book-key> /path/to/saas}"
BOOK="${2:?usage: build_html_book.sh <entry.tex> <book-key> /path/to/saas}"
SAAS="${3:?usage: build_html_book.sh <entry.tex> <book-key> /path/to/saas}"
OUT="$SAAS/resources/onecourse/chapters"
SVG_OUT="$SAAS/public/images/onecourse/chapters"
cd "$(dirname "$0")/.."

# Parts in entry-file order (same pattern build_html_toc.py uses).
mapfile -t PARTS < <(grep -oP '(?<=\\input\{parts/)[a-z0-9-]+(?=/part\})' "$ENTRY")
[ ${#PARTS[@]} -gt 0 ] || { echo "no \\input{parts/<dir>/part} lines in $ENTRY"; exit 1; }

chapters() { # part-dir -> ominput slugs in order
    grep -oP "(?<=\\\\ominput\{$1\}\{)[0-9a-z-]+" "parts/$1/part.tex"
}

# Pass 1: register every chapter's labels.
n=0
for part in "${PARTS[@]}"; do
    for slug in $(chapters "$part"); do
        n=$((n + 1))
        python3 tools/build_html_chapter.py \
            --chapter "parts/$part/$slug.tex" \
            --chapter-number "$n" \
            --book "$BOOK" --languages en,fr,nl \
            --out "$OUT" --svg-out "$SVG_OUT" \
            --labels-only || exit 1
    done
done

# Pass 2: full conversion.
failed=()
n=0
for part in "${PARTS[@]}"; do
    for slug in $(chapters "$part"); do
        n=$((n + 1))
        echo "=== [$n] $part/$slug ==="
        if ! python3 tools/build_html_chapter.py \
            --chapter "parts/$part/$slug.tex" \
            --chapter-number "$n" \
            --book "$BOOK" \
            --languages en,fr,nl \
            --out "$OUT" --svg-out "$SVG_OUT"; then
            failed+=("$n:$part/$slug")
        fi
    done
done

echo
if [ ${#failed[@]} -gt 0 ]; then
    echo "FAILED CHAPTERS (${#failed[@]}):"
    printf '  %s\n' "${failed[@]}"
    exit 1
fi

python3 tools/build_html_toc.py \
    --entry "$ENTRY" \
    --book "$BOOK" --languages en,fr,nl --out "$OUT"
echo "ALL DONE: $n chapters"
