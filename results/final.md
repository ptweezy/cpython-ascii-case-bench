# The PR's final code, measured

This page measures the code proposed for [python/cpython#161201](https://github.com/python/cpython/pull/161201) against the PR's previous revision (9433a66). Trees:

- `finalt` / `final`: the proposed code (`variants/finalt.patch`, `variants/final.patch`).
- `PRt` / `varJ`: the previous revision. `varJ` differs from the PR head only in comment wording and one explicit cast, and compiles to the same machine code with gcc 13, clang 18 and MSVC x64 and x86.
- The `t` trees include the two new tests, and so does CPython's PGO training (it runs `test_str` and `test_bytes`). PGO numbers are with the tests in both trees.

The proposed commit has the same C code as `final`, token for token. After review, its comments were reworded, and its tests build the expected uppercase table from a literal and inline the list of lengths; they test the same cases.

Speedups are time on `main` / time with the build. "Layout" jobs relink each build at 8 code offsets and report the geometric mean (`realworld/layout_local.sh`, `.github/workflows/layout.yml`); "pyperf" jobs use one layout per build. Run IDs are in the table at the end.

## `str.lower()` at 1,024 characters, PGO builds with the tests

| Build | Who ships it | Jobs | Previous | Proposed | Proposed / previous |
|---|---|---|---|---|---|
| MSVC x64 PGO, `--tail-call-interp` | python.org Windows | 4 pyperf | 2.32x | 3.84x | 1.65x (1.55-1.78) |
| MSVC ARM64 PGO | python.org Windows ARM64 | 2 pyperf | 2.37x | 2.72x | 1.15x |
| Apple clang 17 PGO+LTO, M1 | python.org macOS | 1 layout | 2.57x | 4.05x | 1.58x |
| Apple clang 21 PGO+LTO, M4 MacBook Air | python.org macOS | 1 layout, local | 2.43x | 4.11x | 1.69x |
| Apple clang 17 PGO+LTO, Intel | python.org macOS | 1 layout | 1.70x | 2.07x | 1.22x |
| clang 21 PGO+LTO, x86-64 | uv | 2 layout | 2.51-2.56x | 3.59-4.11x | 1.40-1.64x |
| gcc 13 PGO+LTO, x86-64 | Ubuntu 24.04, Debian | 2 layout | 2.95-3.35x | 2.75-3.72x | 0.93-1.11x |
| gcc 16 PGO+LTO, x86-64 (fedora:44) | Fedora, Arch | 2 layout | 2.99-3.76x | 3.32-3.69x | 0.98-1.11x |
| gcc 16, Fedora 44's own python3 recipe | Fedora | pyperf, local | 3.40x | 3.49x | 1.03x |
| gcc 16 PGO+LTO, x86-64 | | 1 layout, local | 3.05x | 3.07x | 1.01x |
| gcc 13 and 16 PGO+LTO, arm64 | | 4 layout | 2.68-2.71x | 2.68-2.72x | 0.99-1.01x |

At 64K characters: Apple M4 3.38x to 5.71x (1.69x), M1 3.65x to 7.69x (2.11x), Intel Mac 2.86x to 5.26x (1.84x), clang 21 2.82-3.59x to 6.16-6.37x (1.77-2.18x). On gcc PGO x86-64 it varies by job, from 0.84x to 1.24x the previous revision (whole-build PGO variation; both are vectorized with the tests), and it is a tie on the local Fedora recipe and gcc 16 layout runs (0.98-1.03x). On gcc arm64 it is 0.99-1.02x.

`str.upper()` gives the same ratios. Windows x64: 1.60-1.65x the previous revision at 1,024 for `str` and `bytes`, `lower()` and `upper()`. MacBook Air PGO: `upper()` 1.73x at 1,024 and 1.65x at 64K. Fedora recipe: 0.99-1.03x at 64K. The `u-*` runs repeat every layout run with `upper()` timed too; per run, `upper()` is within 0.04 of `lower()` at 1,024 and 64K, except on the macOS runners at 64K, where it is a little ahead (2.03x against 1.93x). Geometric mean over each run's jobs, proposed / previous at 1,024 and at 64K:

| Run | `lower()` | `upper()` |
|---|---|---|
| clang 21 PGO+LTO | 1.58x, 2.25x | 1.57x, 2.25x |
| Apple clang 17 PGO+LTO (M1, Intel) | 1.39x, 1.93x | 1.43x, 2.03x |
| fedora:44 gcc 16 PGO+LTO | 1.03x, 1.10x | 1.03x, 1.07x |
| gcc 13 PGO+LTO | 0.95x, 0.98x | 0.96x, 0.98x |
| gcc 13 release | 1.03x, 1.04x | 1.03x, 1.04x |
| gcc 13 `-fno-tree-vectorize` | 1.11x, 1.19x | 1.11x, 1.19x |
| clang 18 `-fno-vectorize -fno-slp-vectorize` | 0.99x, 0.99x | 0.99x, 0.99x |
| clang 18 release | 0.92x, 0.80x | 0.92x, 0.81x |

## Builds without PGO

| Build | Previous | Proposed | Proposed / previous |
|---|---|---|---|
| gcc 13 `-fno-tree-vectorize`, x86-64 / arm64 (1,024) | 2.13x / 2.26x | 2.50x / 2.40x | 1.17x / 1.06x |
| clang 18 `-fno-vectorize -fno-slp-vectorize`, x86-64 / arm64 (1,024) | 2.25x / 2.25x | 2.21x / 2.25x | 0.98x / 1.00x |
| same, 64K | gcc 2.45x / 3.39x, clang 2.76x / 3.20x | gcc 3.10x / 3.97x, clang 2.72x / 3.21x | 0.99-1.27x |
| Apple clang 21 release (SDK `_FORTIFY_SOURCE`), M4, 1,024 / 64K | 2.28x / 3.50x | 3.67x / 5.67x | 1.61x / 1.62x |
| clang 18 `-O3`, x86-64 / arm64, 64K | 6.14x / 4.66x | 4.84x / 3.71x | 0.79x / 0.80x |
| clang 22 `-O3`, x86-64 (local), 64K | 4.08x | 3.16x | 0.77x |

With the auto-vectorizer off, neither revision has vector instructions in `ascii_case_words`. The proposed code is 0.99-1.03x `main` at 8 characters (0.99x in one job, where one of the 8 layouts was an outlier), 1.05-1.07x at 16 and 1.11-1.13x at 32. Plain clang `-O3` without PGO or `_FORTIFY_SOURCE` is the one configuration where it is clearly slower than the previous revision, because clang reorganizes the two-word loop. It is still 3.2-4.8x faster than `main` there.

## Short strings

Over 42 jobs (38 runner layout jobs from the `f-*` and `u-*` runs, the MacBook Air's two runs and the local gcc and clang layout runs), the real-world short-string mix (`realworld/`) is 1.001x the previous revision (geometric mean; 95% interval 0.988-1.014; per job 0.891-1.119). Divided by the control (string operations that never reach this code, `realworld/control.py`), the 38 runner jobs give 1.002x (0.993-1.012). Strings shorter than 8 bytes take the unchanged byte loop.

Whole-build PGO variation is large here: the previous revision's own short mix measured 1.065x `main` in one gcc 13 PGO arm64 job and 1.151x in the same job of the repeat run. The one build where the proposed code is behind in all four jobs is gcc 13 PGO+LTO on arm64: 0.975x on the short mix and 0.970x at 16 characters after the control adjustment (0.946x and 0.942x before it). On gcc 13 PGO x86-64 it is 1.014x, and on every other build 0.99-1.03x. On Windows x64 PGO, 8 and 16 characters are 0.98-1.00x the previous revision.

## Vector instructions in `ascii_case_words`

| Build | Previous | Proposed |
|---|---|---|
| gcc 13 PGO+LTO (tests), x86-64 / arm64 | 45 / 34 | 54 / 44 |
| gcc 16 PGO+LTO (tests), x86-64 / arm64 | 96 / 188 | 88 / 68 |
| gcc 16, Fedora recipe (tests), x86-64 | 49 | 44 |
| clang 21 PGO+LTO (tests) | 0 | 42 |
| Apple clang 17 PGO+LTO (tests), Intel / M1 | 0 / 0 | 30 / 24 |
| Apple clang 21 PGO+LTO / release, M4 (NEON lines) | 0 / 0 | 20 / 12 |
| MSVC x64 `/O1 /Oi` (as in PGO-cold code) / `/O2` | 0 / 45 | 18 / 52 |

Without the tests in the training, the previous revision has 0 in every PGO build counted, including gcc. MSVC ARM64 was timed but not disassembled.

## Correctness

- Every build above passed `edge_cases.py` (253,814 cases) and `check_all.py` (1,495,930 cases, `lower()`, `upper()`, `capitalize()` and `casefold()` of `bytes`, `bytearray` and `str`).
- The code, run with ASan and UBSan against a reference, passed 80 million cases, including a 32-bit simulation. CPython's CI warning flags and MSVC `/W4` give no warnings.
- Mutation check (gcc and clang `-O3`): of 10 planted bugs, the existing tests miss 6 that the new tests catch, 3 break the build itself (Python can't build its modules), and 1 is caught by both. One equivalent change passes both, as it should.
- Machine code: identical to `final` with gcc 13 and clang 18 (x86-64, AVX2, AVX-512, aarch64, i686, riscv64, ppc64le and s390x, at `-O2`, `-O3` and `-Os`) and with MSVC 19.51 x64 and x86 (`/O2`, `/O1 /Oi`).

## Runs

| Name | Run | What |
|---|---|---|
| f-gcc-pgo | 41972540849 | layout, gcc 13 PGO+LTO, x86-64 and arm64, 2 jobs each |
| f-f44-pgo | 41972543970 | layout, fedora:44 gcc 16 PGO+LTO, x86-64 and arm64, 2 jobs each |
| f-clang21-pgo | 41972548232 | layout, clang 21 PGO+LTO, ubuntu-26.04, 2 jobs |
| f-mac-pgo | 41972551726 | layout, Apple clang PGO+LTO, M1 and Intel |
| f-win-pgo | 41972555332 | pyperf, MSVC x64 PGO `--tail-call-interp`, 4 jobs |
| f-winarm-pgo | 41972559306 | pyperf, MSVC ARM64 PGO, 2 jobs |
| f-gcc-novec | 41972563056 | layout, gcc 13 release `-fno-tree-vectorize` |
| f-clang-novec | 41972566638 | layout, clang 18 release `-fno-vectorize -fno-slp-vectorize` |
| f-clang-rel | 41972570399 | layout, clang 18 release |
| u-* | 41975079453 to 41975102968 | the layout runs again, with `str.upper()` in the fixed lengths |

Local machines: an Apple M4 MacBook Air (Apple clang 21, PGO+LTO and release, 15 replay rounds and 9 fixed-length rounds, timing only at nominal thermal pressure) and a Lenovo ThinkCentre (Fedora 44, gcc 16.2.1 and clang 22; Fedora's python3 recipe with pyperf n=90 and a 45-round replay, and gcc PGO+LTO and clang `-O3` layout runs).
