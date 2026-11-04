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

The `variants` workflow compares several versions of the change (the patches in `variants/`) against `main` on each runner. Its `build` input picks release, pgo or novec builds (as in `bench`), or o2 (`CFLAGS=-O2`, which configure puts after its own `-O3`, as distribution builds do: Ubuntu's and Fedora's `python3` record `-O2`), and `bench_set` picks the short-string set or the full one:

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
- `varK`, `varL` and `varM` are the PR's latest revision (9433a66) with an explicit path for strings shorter than a word, instead of the byte loop. gcc's PGO+LTO build stops peeling that loop once long strings no longer go through it (its training count falls under the link-time hot threshold), which costs about 0.5 ns at length 5. `varK` uses a fall-through `switch` over the lengths 7..1. `varL` converts lengths 4..7 as two overlapping 4-byte words and 2..3 as two overlapping 2-byte words, with a 32-bit `ascii_case_bits32()`. `varM` gives `ascii_case_word()` a byte count, so lengths 4..7 take two overlapping 4-byte words and 1..3 the bytes at 0, len/2 and len - 1, and `_Py_bytes_lower()`/`_Py_bytes_upper()` become one line each.
- `varV` is the PR's latest revision with `__builtin_memcpy` instead of `memcpy` in `ascii_case_word()` under gcc and clang. With `_FORTIFY_SOURCE` (on by default in the macOS SDK, and in many Linux distributions' builds), `memcpy` becomes a checked call that keeps clang from vectorizing the word loop; gcc vectorizes it either way.
- `varX` is `varV` with two words per loop iteration outside MSVC, both loaded before either is stored, and the last pair (or, below 16 characters, the last word) overlapping. At `-O2`, gcc keeps a loop over single words scalar (its cheap cost model won't add a remainder loop or an overlap check), but it vectorizes the pair, so distribution builds get the vector loop too. MSVC's branch is unchanged.
- `varY` is `varV` plus a 16-byte path where `_Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR` is defined (gcc or clang on x86-64, ARM64, or ARM32 with NEON; the check that `Python/pystrhex.c` uses for `bytes.hex()`): strings of 16+ characters go through a loop over a GNU vector of words (`vector_size(16)`), with the same bit trick and the last 16 bytes overlapping. It compiles to SSE2 or NEON without the auto-vectorizer, so it stays vectorized at `-O2` and in PGO builds that find the loop cold. Shorter strings and MSVC are unchanged.
- `varP` is the PR's latest revision with strings of 16+ characters converted in 16-byte blocks outside MSVC: each block is an array of words (`size_t x[16 / SIZEOF_SIZE_T]`, memcpy in, `ascii_case_bits()` on each, memcpy out), the last block overlapping. Plain C11, no compiler extensions: gcc and clang turn each block into one SSE2 or NEON operation at -O2, in PGO builds where the loop is cold, and with `_FORTIFY_SOURCE` (so it needs no `__builtin_memcpy`). Suggested by an adversarial review of `varY`.
- `varQ` is `varP` plus `varW`'s overlapping words for strings shorter than a word.
- `varW` is `varL` (overlapping words for strings shorter than a word) plus `varV`'s `__builtin_memcpy`. On shuffled real-world length mixes (`realworld/`), `varL` was the fastest short path on an Apple M4 and on x86 with gcc and clang, release and PGO.

```
gh workflow run variants.yml
```
