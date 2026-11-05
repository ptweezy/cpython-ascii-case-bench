#!/bin/bash
# The layout test on a local Linux or macOS machine (layout.yml does the
# same on GitHub runners).  Builds main and the variants, relinks each build
# once per shift with a padding object of that many bytes ahead of all of
# Python's own code (same code, every function moved), checks the variants,
# then times every (build, shift): the real-world replay and fixed lengths.
# Needs git, a C compiler and python3 (standard library only).
#
#   realworld/layout_local.sh WORKDIR "varJ varV ..." [configure args...]
#
# Environment: ROUNDS (replay rounds, default 5), LEN_ROUNDS (fixed-length
# rounds, default 3), PADS (default below), REPLAY_CPU (Linux:
# pin timed runs to that logical CPU), JOBS (make -j, default all CPUs),
# LOAD_MAX (if set, each timing phase first waits LOAD_MIN_WAIT seconds,
# default 60, then until two readings 15 s apart have the 1-minute load
# average below LOAD_MAX and, on macOS, nominal thermal pressure; at most
# 60 minutes).
# Results: WORKDIR/results/{layout.md,lengths.md} plus the raw JSON.
set -euo pipefail
H=$(cd "$(dirname "$0")/.." && pwd)
W=$1; VARIANTS=$2; shift 2
CPYTHON_BASE=4e0677ac610d9e890503fc0c0ca8351bfdd5f000
PADS=${PADS:-"0 16 32 48 1024 2064 3104 4080"}
ROUNDS=${ROUNDS:-5}
LEN_ROUNDS=${LEN_ROUNDS:-3}
JOBS=${JOBS:-$(getconf _NPROCESSORS_ONLN)}
mkdir -p "$W/results" && cd "$W"

if [ ! -d base ]; then
  git init -q base
  git -C base fetch -q --depth 1 https://github.com/python/cpython $CPYTHON_BASE
  git -C base checkout -q FETCH_HEAD
fi
for v in $VARIANTS; do
  [ -d $v ] || git -C base worktree add -q --detach ../$v HEAD
  # Apply the patch unless the tree already differs from HEAD; refuse to go
  # on with an unpatched tree (e.g. after a failed apply on an earlier run).
  if git -C $v diff HEAD --quiet; then
    git -C $v apply --cached "$H/variants/$v.patch"
    git -C $v checkout -- .
  fi
  if git -C $v diff HEAD --quiet; then echo "$v: patch not applied"; exit 1; fi
  # A tree (and its build) from an earlier run of a different patch would
  # otherwise be reused silently.
  if ! git -C $v apply --check -R "$H/variants/$v.patch" 2>/dev/null; then
    echo "$v: tree doesn't match variants/$v.patch; delete $W/$v and re-run"; exit 1
  fi
  echo "$v: $(git -C $v diff HEAD --stat | tail -n 1)"
done

for t in base $VARIANTS; do
  if [ ! -x $t/python-pad0 ]; then
    (cd $t && { [ -f Makefile ] || ./configure -q "$@" > ../configure-$t.log 2>&1; } \
      && make -j$JOBS > ../make-$t.log 2>&1) || { tail -n 40 configure-$t.log make-$t.log; exit 1; }
    echo "built $t"
  fi
done

for p in $PADS; do
  if [ "$(uname)" = Darwin ]; then
    printf '.text\n.space %d, 0x90\n' $p > pad$p.s
  else
    printf '.text\n.skip %d, 0x90\n.section .note.GNU-stack,"",@progbits\n' $p > pad$p.s
  fi
  cc -c pad$p.s -o pad$p.o
done
for t in base $VARIANTS; do
  addrs=""
  for p in $PADS; do
    rm -f $t/python-pad$p  # else make -n says it is up to date on a re-run
    cmd=$(cd $t && make -n python-pad$p BUILDPYTHON=python-pad$p | tail -n 1)
    # sed, not ${cmd/.../...}: bash 3.2 (macOS /bin/bash) mangles that here.
    new=$(printf '%s' "$cmd" | sed "s| -o python-pad$p Programs/python.o | -o python-pad$p $PWD/pad$p.o Programs/python.o |")
    if [ "$new" = "$cmd" ]; then echo "no link line for $t: $cmd"; exit 1; fi
    (cd $t && eval "$new") > relink.log 2>&1 || { echo "relink of $t at +$p failed:"; tail -n 20 relink.log; exit 1; }
    addrs="$addrs $(nm $t/python-pad$p | awk '/ _?_Py_bytes_lower$/ {print $1}' | tail -c 6)"
  done
  echo "$t: _Py_bytes_lower at$addrs"
done

for v in $VARIANTS; do
  for p in $PADS; do "$v/python-pad$p" -I "$H/edge_cases.py" > /dev/null; done
  echo "$v: $("$v/python-pad0" -I "$H/edge_cases.py" | tail -n 1) / $("$v/python-pad0" -I "$H/check_all.py")"
done

replay="" lens=""
for t in base $VARIANTS; do
  for p in $PADS; do
    name=$t.p$p; [ $t = base ] && name=main.p$p
    lens="$lens $name=$t/python-pad$p"
    [ $name = main.p0 ] && name=base
    replay="$replay $name=$t/python-pad$p"
  done
done
wait_load() {
  [ -n "${LOAD_MAX:-}" ] || return 0
  local i l th ok=0
  sleep "${LOAD_MIN_WAIT:-60}"
  for i in $(seq 240); do
    l=$(python3 -c "import os; print(round(os.getloadavg()[0], 2))")
    th=""  # macOS thermal pressure level; 0 is nominal
    if command -v notifyutil > /dev/null 2>&1; then
      th=$(notifyutil -g com.apple.system.thermalpressurelevel 2>/dev/null | awk '{print $NF}')
    fi
    if python3 -c "import sys; sys.exit(not $l < $LOAD_MAX)" && { [ -z "$th" ] || [ "$th" = 0 ]; }; then
      ok=$((ok + 1))
      if [ $ok -ge 2 ]; then
        echo "load $l, below $LOAD_MAX, thermal ${th:-n/a} ($(date +%T))"; return 0
      fi
    else
      ok=0
    fi
    sleep 15
  done
  echo "load $l, thermal ${th:-n/a} after 60 minutes; timing anyway ($(date +%T))"
}
wait_load
echo "replay, $ROUNDS rounds ($(date +%T))"
python3 "$H/realworld/replay_drive.py" "$H/realworld/hist" results/layout $ROUNDS $replay > results/layout-drive.txt
python3 "$H/realworld/layout_summary.py" results/layout/times.json | tee results/layout.md
wait_load
echo "fixed lengths, $LEN_ROUNDS rounds ($(date +%T))"
python3 "$H/realworld/len_layout.py" results/lengths.json $LEN_ROUNDS $lens
python3 "$H/realworld/len_layout_summary.py" results/lengths.json | tee results/lengths.md
echo "done ($(date +%T))"
