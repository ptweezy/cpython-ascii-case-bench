"""Write mutants of a variant's Objects/bytes_methods.c.

    python3 mutants.py BYTES_METHODS_C OUTDIR

Each mutant is one small bug in the word or block code; OUTDIR/<name>.c.
"""
import os, sys

src = open(sys.argv[1]).read()
out = sys.argv[2]
os.makedirs(out, exist_ok=True)

MUTANTS = {
    # 'Z' and 'z' (the last letter) are not converted, in every path.
    "z_unconverted": ("gt = (0x80 - first - 26) * ones;", "gt = (0x80 - first - 25) * ones;"),
    # 'A' and 'a' (the first letter) are not converted, in every path.
    "a_unconverted": ("size_t ge = (0x80 - first) * ones,", "size_t ge = (0x80 - first - 1) * ones,"),
    # The last, overlapping block is skipped: tails of 16+ strings stay.
    "no_last_block": ("        ascii_case_block(result, cptr, len - ASCII_CASE_BLOCK, ge, gt);\n", ""),
    # The last, overlapping word is skipped: tails of 8..15 strings stay.
    "no_last_word": ("    ascii_case_word(result, cptr, len - SIZEOF_SIZE_T, ge, gt);\n}", "}"),
    # The word loop stops one word early: 9..15-byte strings lose their head.
    "word_loop_short": ("for (i = 0; i < len - SIZEOF_SIZE_T; i += SIZEOF_SIZE_T) {",
                        "for (i = 0; i < len - 2 * SIZEOF_SIZE_T; i += SIZEOF_SIZE_T) {"),
    # The vector block doesn't mask out bytes >= 0x80: some non-ASCII bytes
    # in strings of 16+ bytes get bit 0x20 flipped.
    "block_no_ascii_mask": ("~(b + ASCII_CASE_SPLAT(gt)) & ~x\n", "~(b + ASCII_CASE_SPLAT(gt))\n"),
    # The vector block shifts by 3: letters in 16+ strings get 0x10 flipped.
    "block_shift": (">> ASCII_CASE_SPLAT(2);", ">> ASCII_CASE_SPLAT(3);"),
}
for name, (old, new) in MUTANTS.items():
    assert src.count(old) == 1, (name, src.count(old))
    open(os.path.join(out, name + ".c"), "w").write(src.replace(old, new))
print(" ".join(MUTANTS))
