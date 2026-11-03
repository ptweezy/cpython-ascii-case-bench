# cpython-ascii-case-bench

Benchmarks for [python/cpython#161155](https://github.com/python/cpython/issues/161155), which speeds up ASCII `str.lower()`/`str.upper()` and `bytes.lower()`/`bytes.upper()` by converting a machine word at a time.

The `bench` workflow builds CPython `main` at the patch's parent commit twice on each GitHub-hosted runner: once unchanged, once with `gh-161155.patch`. Since 2026-11-03 that patch is the PR's latest revision (9433a66), which has `varJ`'s code; before that it was `varG2`, and the first version is `variants/varA.patch`. Then it:

- runs `edge_cases.py`, `check_all.py` and `test_str`, `test_bytes`, `test_userstring` and `test_string` on the patched build. `check_all.py` puts every byte value (every ASCII character for `str`) at every position of every length 0..80, and of lengths around word multiples up to 4,096, and checks `lower()`, `upper()`, `capitalize()` and `casefold()` of `bytes`, `bytearray` and `str` against `translate()`, including unaligned `bytearray` buffers;
- compiles `word_exhaustive_word.c` and `variants/gcheck_G.c` with the runner's C compiler and checks the word-level conversion, and the whole functions at lengths 0 to 80, against a per-byte reference;
- on Linux and macOS, disassembles the word helper in the patched binary and counts its SIMD instructions (`vec_check.sh`), to show whether the compiler vectorized it;
- times both builds with pyperf (`bench.py`), alternating between them one benchmark at a time: `str.lower`, `str.upper`, `bytes.lower` and `bytes.upper` at each length, on inputs that cycle through all 128 ASCII characters (`str`) or all 256 byte values (`bytes`) in a fixed shuffled order, plus two lists of short words.

The `check` workflow compiles `exact/check_exact.c` against the PR's word helpers, copied verbatim from `Objects/bytes_methods.c` with the patch applied (`exact/extract.py`), for both word loops (the one MSVC gets and the other). It checks every byte value at every position of a word on all 256 fills and every pair of values at every pair of positions, then the whole functions at many lengths and source and destination offsets, against a per-byte reference. It runs with gcc and clang on Linux (x86-64, arm64) and macOS (arm64, x86-64), MSVC on Windows (x64, x86, arm64), and under QEMU for 32-bit x86 and ARM and big-endian s390x and 32-bit PowerPC.

The matrix covers Linux, Windows and macOS on x86-64 and arm64, each with a plain release build and a PGO build (PGO+LTO on Linux and macOS), two runs each. Linux and macOS also get a `novec` build: release with the compiler's auto-vectorizer turned off for both trees (gcc `-fno-tree-vectorize`, clang `-fno-vectorize -fno-slp-vectorize`). Windows has none because MSVC doesn't vectorize this loop. Each job uploads its pyperf JSON, a `compare_to` table and the CPU model as an artifact.

```
gh workflow run bench.yml
```

The `variants` workflow compares several versions of the change (the patches in `variants/`) against `main` on each runner. Its `build` input picks release, pgo or novec builds (as in `bench`), and `bench_set` picks the short-string set or the full one:

- `varA` is the change as proposed.
- `varC` moves the word loop into one helper marked `Py_NO_INLINE`, which the lower and upper functions call only for strings of at least one word.
- `varD` is the same helper as plain `static inline`.
- `varE` is `varA` with an early return through the plain byte loop for strings shorter than a word.
- `varG` keeps the existing byte loops unchanged for short strings. For strings of at least a word, it calls one shared `Py_NO_INLINE` helper (a tail call) that converts whole words, the last one overlapping the one before it. `variants/gcheck_G.c` checks it against a per-byte reference.
- `varF` is `varG` with the helper left `static inline`.
- `varG2` is `varG` with the two small helpers marked `Py_ALWAYS_INLINE`. Without it, gcc's PGO+LTO build treats the word helper as cold (the PGO training doesn't reach it) and calls the per-word function instead of inlining it (1.4x instead of 2.1x at 1,024 characters locally); MSVC's PGO build loses some too (1.9x instead of 2.3x). Normal builds compile to the same code as `varG`.
- `varH` is `varG2` with the word loop counting words (indexing an array-of-words type) and its two constants computed before the loop, so MSVC vectorizes it; the word count is unsigned so size-optimized builds don't use a division.
- `varI` keeps `varG2`'s byte-stepping loop except under MSVC, which gets `varH`'s count-by-one loop; counting words makes clang use post-indexed loads and stores on AArch64, which are slower on Apple cores. Both branches compute the constants before the loop and convert the overlapping last word first.
- `varJ` is `varI` with the overlapping last word converted after the loop again, as in `varG2`, so outside MSVC it is `varG2` with the constants passed in. The PR's latest revision (9433a66) is `varJ` with shorter comments.

```
gh workflow run variants.yml
```
