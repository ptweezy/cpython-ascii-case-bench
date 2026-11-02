# cpython-ascii-case-bench

Benchmarks for [python/cpython#161155](https://github.com/python/cpython/issues/161155), which speeds up ASCII `str.lower()`/`str.upper()` and `bytes.lower()`/`bytes.upper()` by converting a machine word at a time.

The `bench` workflow builds CPython `main` at the patch's parent commit twice on each GitHub-hosted runner: once unchanged, once with `gh-161155.patch`. Then it:

- runs `edge_cases.py` and `test_str`, `test_bytes`, `test_userstring` and `test_string` on the patched build;
- compiles `word_exhaustive_word.c` with the runner's C compiler and checks the word-level conversion against a per-byte reference;
- times both builds with pyperf (`bench.py`), alternating between them one benchmark at a time.

The matrix covers Linux, Windows and macOS on x86-64 and arm64, each with a plain release build and a PGO build (PGO+LTO on Linux and macOS), two runs each. Each job uploads its pyperf JSON, a `compare_to` table and the CPU model as an artifact.

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
