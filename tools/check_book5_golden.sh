#!/bin/sh
# Book 5's 4325 links are the fixture the linker is held to: regenerate them from
# the unwrapped sources and the result must match, byte for byte, what is on disk.
#
# Every book shares tools/termlink/, so a rule changed to suit one book silently
# changes the others. Run this before committing anything under tools/.
#
#   sh tools/check_book5_golden.sh
#
# It writes nothing (--check regenerates in memory), so it is safe to run while
# another book is being generated.
set -e
cd "$(dirname "$0")/.."
python3 tools/link_defined_terms.py --book 5 --check
