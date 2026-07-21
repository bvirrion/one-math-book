#!/usr/bin/env bash
# Build every chapter of book 2 for the online reader, in part.tex order
# (cross-chapter references resolve against already-built chapters), then
# regenerate the toc. Failures don't stop the batch — they are listed at
# the end so the converter can be extended and just those chapters re-run.
#
# Usage: bash tools/build_html_book.sh /path/to/saas
set -u
SAAS="${1:?usage: build_html_book.sh /path/to/saas}"
OUT="$SAAS/resources/onecourse/chapters"
SVG_OUT="$SAAS/public/images/onecourse/chapters"
cd "$(dirname "$0")/.."

# Pass 1: register every chapter's labels so cross-chapter references —
# including forward ones — resolve during the full pass.
n=0
for part in grade-10 grade-11 grade-12; do
    for slug in $(grep -oP "(?<=\\\\ominput\{$part\}\{)[0-9a-z-]+" "parts/$part/part.tex"); do
        n=$((n + 1))
        python3 tools/build_html_chapter.py \
            --chapter "parts/$part/$slug.tex" \
            --chapter-number "$n" \
            --book math-2 --languages en,fr,nl \
            --out "$OUT" --svg-out "$SVG_OUT" \
            --labels-only || exit 1
    done
done

# Pass 2: full conversion.
failed=()
n=0
for part in grade-10 grade-11 grade-12; do
    for slug in $(grep -oP "(?<=\\\\ominput\{$part\}\{)[0-9a-z-]+" "parts/$part/part.tex"); do
        n=$((n + 1))
        echo "=== [$n] $part/$slug ==="
        if ! python3 tools/build_html_chapter.py \
            --chapter "parts/$part/$slug.tex" \
            --chapter-number "$n" \
            --book math-2 \
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
    --entry one_math_book_2_high_school.tex \
    --book math-2 --languages en,fr,nl --out "$OUT"
echo "ALL DONE: $n chapters"
