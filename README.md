# cpython-ascii-case-bench

Benchmarks for [python/cpython#161155](https://github.com/python/cpython/issues/161155), which speeds up ASCII `str.lower()`/`str.upper()` and `bytes.lower()`/`bytes.upper()` by converting a machine word at a time.

The `bench` workflow builds CPython `main` at the patch's parent commit twice on each GitHub-hosted runner: once unchanged, once with `gh-161155.patch`. Since 2026-11-02 that patch is the overlapping-word version (`varG` below); the first version is `variants/varA.patch`. Then it:

- runs `edge_cases.py` and `test_str`, `test_bytes`, `test_userstring` and `test_string` on the patched build;
- compiles `word_exhaustive_word.c` and `variants/gcheck_G.c` with the runner's C compiler and checks the word-level conversion, and the whole functions at lengths 0 to 80, against a per-byte reference;
- on Linux and macOS, disassembles the word helper in the patched binary and counts its SIMD instructions (`vec_check.sh`), to show whether the compiler vectorized it;
- times both builds with pyperf (`bench.py`), alternating between them one benchmark at a time.

The matrix covers Linux, Windows and macOS on x86-64 and arm64, each with a plain release build and a PGO build (PGO+LTO on Linux and macOS), two runs each. Linux and macOS also get a `novec` build: release with the compiler's auto-vectorizer turned off for both trees (gcc `-fno-tree-vectorize`, clang `-fno-vectorize -fno-slp-vectorize`). Windows has none because MSVC doesn't vectorize this loop. Each job uploads its pyperf JSON, a `compare_to` table and the CPU model as an artifact.

```
gh workflow run bench.yml
```

The `variants` workflow compares several versions of the change (the patches in `variants/`) against `main` on each runner, using release builds and a benchmark set focused on short strings:

- `varA` is the change as proposed.
- `varC` moves the word loop into one helper marked `Py_NO_INLINE`, which the lower and upper functions call only for strings of at least one word.
- `varD` is the same helper as plain `static inline`.
- `varE` is `varA` with an early return through the plain byte loop for strings shorter than a word.
- `varG` keeps the existing byte loops unchanged for short strings. For strings of at least a word, it calls one shared `Py_NO_INLINE` helper (a tail call) that converts whole words, the last one overlapping the one before it. `variants/gcheck_G.c` checks it against a per-byte reference.
- `varF` is `varG` with the helper left `static inline`.

```
gh workflow run variants.yml
```
