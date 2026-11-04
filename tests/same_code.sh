#!/bin/bash
# Which variants compile to the same machine code: build each variant's
# helpers (oldcc/make_test.py, from patched Objects/bytes_methods.c trees)
# with gcc and clang and compare the disassembly of ascii_case_words.
#
#   tests/same_code.sh SRC_PREFIX "A=B ..." [more]
#
# SRC_PREFIX/varX is a CPython source tree with variants/varX.patch applied.
# Each A=B pair is compared on x86-64 without AVX2 (gcc, clang), with
# -mavx2, with -march=x86-64-v4, and on aarch64 (clang --target).  With
# "more", also on 32-bit x86, riscv64, ppc64le and s390x (clang --target).
# Cross targets use clang's own stdint.h and two stub headers instead of a
# sysroot.
H=$(cd "$(dirname "$0")/.." && pwd)
P=$1; PAIRS=$2
W=$(mktemp -d)
mkdir "$W/inc"
echo 'int printf(const char *, ...);' > "$W/inc/stdio.h"
printf '%s\n' '#include <stddef.h>' 'void *memcpy(void *, const void *, size_t);' \
  'void *memset(void *, int, size_t);' 'int memcmp(const void *, const void *, size_t);' > "$W/inc/string.h"
X="-nostdlibinc -isystem $W/inc --target"
TARGETS=("x86-64:" "x86-64 AVX2:-mavx2" "x86-64 AVX-512:-march=x86-64-v4" "aarch64:$X=aarch64-linux-gnu")
if [ "$3" = more ]; then
  TARGETS+=("i686:$X=i686-linux-gnu" "riscv64:$X=riscv64-linux-gnu" "ppc64le:$X=powerpc64le-linux-gnu" "s390x:$X=s390x-linux-gnu")
fi
dis() {  # object -> ascii_case_words body without addresses
  objdump -d --no-show-raw-insn "$1" | awk '/<ascii_case_words[.>]/{p=1; next} /^$/{p=0} p' \
    | sed -E 's/^ *[0-9a-f]+:\t?//; s/<[^>]*>//g; s/ +# .*//'
}
dis_llvm() {  # up to the next function; skips local labels (RISC-V .Lpcrel_hi)
  llvm-objdump-18 -d --no-show-raw-insn --no-addresses "$1" \
    | awk '/^<ascii_case_words>:/{p=1; next} /^<[^.].*>:$/ || /^Disassembly/{p=0} p && NF && !/^<\./' \
    | sed -E 's/<[^>]*>//g'
}
echo "| Pair | Target | Compiler | Flags | Same machine code |"
echo "|---|---|---|---|---|"
for pair in $PAIRS; do
  a=${pair%=*}; b=${pair#*=}
  for t in $a $b; do python3 "$H/oldcc/make_test.py" "$P/$t/Objects/bytes_methods.c" "$W/$t.c"; done
  for target in "${TARGETS[@]}"; do
    name=${target%%:*}; tf=${target#*:}
    cross=; case "$tf" in *--target*) cross=1;; esac
    for cc in gcc clang; do
      [ -n "$cross" ] && [ $cc = gcc ] && continue
      for f in -O2 -O3 -Os; do
        for t in $a $b; do $cc -std=c11 $f $tf -c "$W/$t.c" -o "$W/$t.o" 2> /dev/null || echo "build failed: $cc $f $tf $t"; done
        if [ -n "$cross" ]; then dis_llvm "$W/$a.o" > "$W/a.s"; dis_llvm "$W/$b.o" > "$W/b.s"
        else dis "$W/$a.o" > "$W/a.s"; dis "$W/$b.o" > "$W/b.s"; fi
        if [ ! -s "$W/a.s" ]; then same="(function not found)"
        elif cmp -s "$W/a.s" "$W/b.s"; then same="yes ($(wc -l < "$W/a.s") instructions)"
        else same="no"; fi
        echo "| $a = $b | $name | $($cc --version | head -n 1 | sed 's/ (.*//') | $f | $same |"
      done
    done
  done
done
rm -rf "$W"
