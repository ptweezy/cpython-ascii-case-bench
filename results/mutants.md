# Mutation check of the tests

`tests/mutation_check.sh` on `varB` (gcc 13.3 `-O3`, x86-64 without AVX2, so the 16-byte vector block), WSL2 on the Ryzen 7 9800X3D. Each mutant is one small bug in `Objects/bytes_methods.c` (`tests/mutants.py`). For each: the proposed tests (`tests/proposed_tests.py`), then the whole test suite (`python -m test --fast-ci`). The unchanged build passes both.

| Mutant | Proposed tests | Whole test suite | test_bytes, test_str, test_userstring, test_string |
|---|---|---|---|
| 'Z' and 'z' not converted (any length of 8+) | fail | 7 test files fail (e.g. test_base64, test_clinic, test_codecs, test_locale) | **pass** |
| 'A' and 'a' not converted (any length of 8+) | fail | 36 test files fail (e.g. test__opcode, test_argparse, test_base64, test_bigmem) | **pass** |
| last, overlapping block skipped (16+ bytes) | (no build) | CPython's own build fails: a build step's interpreter gets garbage in its strings | |
| last, overlapping word skipped (8-15 bytes) | (no build) | CPython's own build fails: a build step's interpreter gets garbage in its strings | |
| word loop stops one word early (9-15 bytes) | fail | 80 test files fail (e.g. test__opcode, test_argparse, test_base64, test_bigmem) | **pass** |
| block doesn't mask bytes >= 0x80 (16+ bytes: some non-ASCII bytes flipped) | fail | **passes** | **pass** |
| block shifts by 3 instead of 2 (16+ bytes) | fail | 41 test files fail (e.g. test_argparse, test_base64, test_bigmem, test_capi) | **pass** |

So the proposed tests catch every mutant that builds. None of those fails the tests of `str` and `bytes` themselves (all four ran and passed each time); the suite catches four only through other modules (`base64`, `codecs`, `argparse`, ...), and `block_no_ascii_mask` passes the whole suite.
