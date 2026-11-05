#!/bin/bash
# Disassemble the helpers (ascii_case_words, ascii_case_blocks) in a built
# tree's python binary and count their SIMD instructions, to show whether
# the compiler vectorized the loop.  Usage: vec_check.sh TREE
tree=$1
case "$(uname -s)" in
  Linux)  bin=$tree/python
          objdump -d --no-show-raw-insn "$bin" |
            awk '/^[0-9a-f]+ <ascii_case_(words|blocks)/ {f=1; print; next}
                 /^[0-9a-f]+ </ {f=0} f' > fn.txt ;;
  Darwin) bin=$tree/python.exe
          otool -tV "$bin" |
            awk '/^_ascii_case_(words|blocks)/ {f=1; print; next}
                 /^_[^ \t]*:$/ {f=0} f' > fn.txt ;;
esac
grep -E '^[0-9a-f_]' fn.txt | grep -E 'ascii_case_(words|blocks)' | sed 's/^/function: /'
total=$(grep -cE '^\s*[0-9a-f]+:?\s' fn.txt)
simd=$(grep -cE 'xmm|ymm|zmm|v[0-9]+\.[0-9]*[bhsd]|[ ,[]q[0-9]+' fn.txt)
echo "$tree: $total instructions in the helpers, $simd use SIMD registers"
