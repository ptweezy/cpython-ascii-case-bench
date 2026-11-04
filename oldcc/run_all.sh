#!/bin/bash
# Runs inside an Ubuntu container (see .github/workflows/oldcc.yml): install
# every gcc and clang the release packages, then build each test-*.c in the
# current directory with each compiler at several optimization levels (and
# with AVX2 on x86-64), run it, and count the SIMD instructions in
# ascii_case_words.  Exits nonzero if any build fails or any check fails.
set -u
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq > /dev/null
cands="gcc-4.7 gcc-4.8 gcc-4.9 gcc-5 gcc-6 gcc-7 gcc-8 gcc-9 gcc-10
       clang-3.3 clang-3.4 clang-3.5 clang-3.6 clang-3.7 clang-3.8 clang-3.9 clang-4.0
       clang-5.0 clang-6.0 clang-7 clang-8 clang-9 clang-10 clang-11 clang-12"
if ! apt-get install -y -qq gcc libc6-dev binutils > /tmp/apt.log 2>&1; then
  echo "apt-get install gcc failed"; tail -n 20 /tmp/apt.log; exit 1
fi
# One package at a time, so that one that won't install skips only itself.
avail=""
for p in $cands; do
  apt-cache show "$p" > /dev/null 2>&1 || continue
  if apt-get install -y -qq --no-install-recommends "$p" > /tmp/apt.log 2>&1 && command -v "$p" > /dev/null; then
    avail="$avail $p"
  else
    echo "($p would not install: $(tail -n 1 /tmp/apt.log))"
  fi
done
. /etc/os-release
echo "$PRETTY_NAME, $(uname -m), compilers:$avail"
flagsets=("-O0" "-O1" "-O2" "-O3" "-Os")
if [ "$(uname -m)" = x86_64 ]; then flagsets+=("-O2 -mavx2" "-O3 -mavx2" "-Os -mavx2"); fi
fail=0
echo "| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |"
echo "|---|---|---|---|---|---|"
for p in $avail; do
  ver=$($p --version 2>&1 | head -n 1)
  for t in test-*.c; do
    for f in "${flagsets[@]}"; do
      log=$($p -std=c11 -Wall $f "$t" -o /tmp/t 2>&1)
      if [ $? -ne 0 ]; then
        echo "| $t | $ver | $f | **build failed** | | |"
        echo "$log" | head -n 20 | sed 's/^/    /'
        fail=1
        continue
      fi
      res=$(/tmp/t) || fail=1
      simd=$(objdump -d --no-show-raw-insn /tmp/t | awk '/<ascii_case_words>:/{p=1; next} p && /^$/{exit} p' \
             | grep -cE '%[xy]mm[0-9]|[[:space:],]v[0-9]+\.|[[:space:],]q[0-9]+[,[:space:]]|[[:space:],]q[0-9]+$')
      nwarn=$(printf '%s\n' "$log" | grep -c 'warning:')
      echo "| $t | $ver | $f | $res | $simd | $nwarn |"
      if [ "$nwarn" -gt 0 ]; then printf '%s\n' "$log" | grep 'warning:' | head -n 5 | sed 's/^/    /'; fi
    done
  done
done
exit $fail
