# Results for gh-161155 / python/cpython#161201

pyperf on GitHub-hosted runners ([run 41484117093](https://github.com/ptweezy/cpython-ascii-case-bench/actions/runs/41484117093)). `main` at 4e0677a and the patch are built and timed on the same runner, two runs per runner. Ratios are time on `main` / time with the patch; columns are geometric means over `str.lower`, `str.upper` and `bytes.lower` at those lengths.

Release builds:

| Runner | 1-7 chars | 8-16 | 32 | 1,024 | 64K |
|---|---|---|---|---|---|
| Linux x86-64 (AMD EPYC), gcc 13 | 0.99x | 1.06x | 1.24x | 3.57x | 4.92x |
| Linux arm64 (Neoverse-N2), gcc 13 | 1.00x | 1.09x | 1.24x | 2.86x | 4.19x |
| Windows x86-64 (AMD EPYC), MSVC 19.51 | 1.00x | 1.02x | 1.09x | 2.10x | 2.55x |
| Windows arm64 (Cobalt 100), MSVC 19.51 | 1.00x | 1.04x | 1.12x | 2.19x | 2.99x |
| macOS arm64 (M1), Apple clang 17 | 1.05x | 1.15x | 1.21x | 2.67x | 3.51x |
| macOS x86-64 (i7-8700B), Apple clang 17 | 0.96x | 1.01x | 1.11x | 2.00x | 3.07x |

PGO builds (PGO+LTO on Linux and macOS):

| Runner | 1-7 chars | 8-16 | 32 | 1,024 | 64K |
|---|---|---|---|---|---|
| Linux x86-64 (AMD EPYC, Intel Xeon), gcc 13 | 1.00x | 1.08x | 1.17x | 2.29x | 2.33x |
| Linux arm64 (Neoverse-N2), gcc 13 | 1.00x | 1.10x | 1.29x | 2.49x | 3.46x |
| Windows x86-64 (AMD EPYC), MSVC 19.51 | 1.03x | 1.10x | 1.22x | 2.70x | 2.38x |
| Windows arm64 (Cobalt 100), MSVC 19.51 | 1.00x | 1.07x | 1.17x | 2.33x | 2.98x |
| macOS arm64 (M1), Apple clang 17 | 1.04x | 1.11x | 1.42x | 2.78x | 3.42x |
| macOS x86-64 (i7-8700B), Apple clang 17 | 0.98x | 1.02x | 1.06x | 1.83x | 2.75x |

Release builds with auto-vectorization disabled in both trees (gcc `-fno-tree-vectorize`, clang `-fno-vectorize -fno-slp-vectorize`):

| Runner | 1-7 chars | 8-16 | 32 | 1,024 | 64K |
|---|---|---|---|---|---|
| Linux x86-64 (AMD EPYC), gcc 13 | 1.03x | 1.10x | 1.22x | 2.33x | 2.65x |
| Linux arm64 (Neoverse-N2), gcc 13 | 0.99x | 1.08x | 1.21x | 2.53x | 3.39x |
| macOS arm64 (M1), Apple clang 17 | 1.06x | 1.15x | 1.37x | 3.04x | 3.24x |
| macOS x86-64 (i7-8700B), Apple clang 17 | 0.94x | 0.99x | 1.10x | 1.85x | 2.96x |

Only the Linux release builds (gcc 13 `-O3`) vectorize the word loop; MSVC, Apple clang 17 and gcc PGO+LTO keep it scalar. The macOS x86-64 runner is noisy (5 to 13% per-sample variation on `main`). Raw pyperf JSON is in the run's artifacts.
