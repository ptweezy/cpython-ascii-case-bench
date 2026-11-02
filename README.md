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
