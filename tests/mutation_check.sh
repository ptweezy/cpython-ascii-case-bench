#!/bin/bash
# Mutation check of the tests: build a variant tree with gcc -O3, then rebuild
# it with each mutant of Objects/bytes_methods.c (tests/mutants.py).  For
# each: the proposed tests, then the whole test suite (--fast-ci), and which
# test files fail.  WORKDIR is created; the source tree is copied, not changed.
H=$(cd "$(dirname "$0")/.." && pwd)   # this repository
W=${1:?usage: tests/mutation_check.sh WORKDIR VARIANT_SOURCE_TREE}; SRC=${2:?}
set -u
mkdir -p $W && cd $W
if [ ! -d src ]; then cp -a "$SRC" src; fi
cp "$SRC"/Objects/bytes_methods.c orig.c
names=$(python3 $H/tests/mutants.py orig.c mutants)
tr -d '\r' < $H/tests/proposed_tests.py > proposed_tests.py
mkdir -p build && cd build
[ -f Makefile ] || ../src/configure -q > ../configure.log 2>&1
for m in orig $names; do
  if [ $m = orig ]; then cp ../orig.c ../src/Objects/bytes_methods.c; else cp ../mutants/$m.c ../src/Objects/bytes_methods.c; fi
  make -j14 > ../make-$m.log 2>&1 || { echo "$m: build failed"; continue; }
  p=$(./python ../proposed_tests.py 2>&1 | grep -E "^(OK|FAILED)" | tr '\n' ' ')
  ./python -m test --fast-ci -j14 > ../suite-$m.log 2>&1
  failed=$(sed -n '/test[s]* failed:/,/^$/p' ../suite-$m.log | grep -v "failed:" | tr -s ' \n' ' ')
  res=$(grep -E "^Result:" ../suite-$m.log | tail -n 1)
  echo "$m: proposed tests: $p| suite: $res | failed: $failed"
done
cp ../orig.c ../src/Objects/bytes_methods.c
