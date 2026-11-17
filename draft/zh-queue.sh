#!/bin/bash
# Haiku queue for the zh pilot run: years in book order, at most three run.py at once, each re-run up to 5 passes
# until it reports 0 rejected sections. Logs in draft/pilot-<year>-zh/run.log. Waits on PIDs, never pgrep.
cd /home/bvirrion/repositories/one-course/pilot_translation || exit 2
R=../one-math-book
desc() { case $1 in
  grade-[1-5]) echo "primary school mathematics textbook (${1/grade-/grade }, young children)";;
  grade-[6-9]) echo "middle school mathematics textbook (${1/grade-/grade })";;
  grade-1[0-2]) echo "high school mathematics textbook (${1/grade-/grade })";;
  bachelor-*) echo "university mathematics textbook (year ${1#bachelor-} of a mathematics bachelor)";;
esac; }
one() {
  local y=$1 RUN=$R/draft/pilot-$1-zh
  mkdir -p $RUN
  for pass in $(seq 1 ${PASSES:-5}); do
    python3 run.py --repo $R --year $y --lang zh --workers ${W:-3} --book-desc "$(desc $y)" >> $RUN/run.log 2>&1
    tail -1 $RUN/run.log | grep -q "0 with a rejected section; 0 stopped" && { echo "$(date +%H:%M) $y done (pass $pass)"; return; }
    grep -q "stopped on a failed call" <(tail -1 $RUN/run.log) && ! tail -1 $RUN/run.log | grep -q " 0 stopped" && sleep 600
  done
  echo "$(date +%H:%M) $y NOT CLEAN after ${PASSES:-5} passes"
}
YEARS="${YEARS:-grade-1 grade-2 grade-3 grade-4 grade-5 grade-6 grade-7 grade-8 grade-9 grade-10 grade-11 grade-12 bachelor-1 bachelor-2 bachelor-3}"
pids=()
for y in $YEARS; do
  while [ ${#pids[@]} -ge 3 ]; do
    wait -n; alive=(); for p in "${pids[@]}"; do kill -0 $p 2>/dev/null && alive+=($p); done; pids=("${alive[@]}")
  done
  one $y & pids+=($!)
done
wait
echo "$(date +%H:%M) queue finished"
