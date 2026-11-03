# Results for gh-161155 / python/cpython#161201

## Latest revision (9433a66)

The PR now gives MSVC (and only MSVC) a word loop that counts by one, which it vectorizes; MSVC skips loops that step by 8 bytes. The two per-call constants are computed before the loop, since with the multiplication inside the loop MSVC vectorizes it with an AVX-512 instruction and runs the vector loop only on AVX-512 CPUs. Other compilers keep the previous byte-stepping loop: counting words makes clang use post-indexed loads and stores on AArch64, which measured 6-8% slower at 64 KB on an Apple M4. Outside MSVC the code is the previous revision's with the constants passed in; Apple clang compiles it to the same instructions.

Previous revision (a907379) time / latest revision time, geometric means over `str.lower`, `str.upper` and `bytes.lower` (best of 5 interleaved rounds of `timeit`, both builds on the same machine):

| Machine | Compiler | Build | ≤7 chars | 8-16 | 24-64 | 256 | 1,024 | 64K |
|---|---|---|---|---|---|---|---|---|
| Ryzen 7 9800X3D, Windows 11 | MSVC 19.51 | release | 1.02x | 1.01x | 1.02x | 1.21x | 1.48x | 2.33x |
| Ryzen 7 9800X3D, Windows 11 | MSVC 19.51 | PGO | 1.02x | 1.06x | 1.08x | 1.07x | 1.02x | 1.06x |
| Ryzen 7 9800X3D, Ubuntu 24.04 (WSL2) | gcc 13.3 | release | 1.01x | 1.00x | 1.00x | 1.08x\* | 1.26x\* | 1.44x\* |
| Ryzen 7 9800X3D, Ubuntu 24.04 (WSL2) | gcc 13.3 | PGO+LTO | 1.02x | 1.02x | 1.02x | 1.01x | 1.01x | 1.00x |
| Core i5-12400T, Fedora 44 | gcc 16.2 | release | 0.99x | 1.00x | 0.99x | 0.99x | 1.00x | 1.00x |
| Core i5-12400T, Fedora 44 | gcc 16.2 | PGO+LTO | 1.00x | 1.01x | 1.00x | 1.00x | 0.99x | 1.00x |
| Core i5-12400T, Fedora 44 | clang 22.1 | release | 1.02x | 1.00x | 1.00x | 1.00x | 1.01x | 1.01x |
| Core i5-12400T, Fedora 44 | clang 22.1 | PGO+LTO | 1.05x | 1.00x | 1.00x | 0.98x | 0.98x | 1.01x |
| Apple M4, macOS 27.2 | Apple clang 21 | release | 1.01x | 1.01x | 1.01x | 1.00x | 1.03x | 0.99x |
| Apple M4, macOS 27.2 | Apple clang 21 | PGO+LTO | 0.99x | 1.01x | 1.01x | 1.00x | 0.96x† | 0.97x† |

\* gcc 13 put the previous revision's `str.lower`/`bytes.lower` word loop in a separate copy that ran about 40% slower than its `str.upper` one; `str.upper` alone is 1.02-1.03x. That is code placement, not a change in the loop.  
† Apple clang compiles the function to the same instructions as before (release build checked); in repeated PGO runs on this machine these rows varied by up to ±6%.

Latest revision against `main` (e4dba41), same method:

| Machine | Compiler | Build | ≤7 chars | 8-16 | 24-64 | 256 | 1,024 | 64K |
|---|---|---|---|---|---|---|---|---|
| Ryzen 7 9800X3D, Windows 11 | MSVC 19.51 | release | 1.01x | 1.03x | 1.16x | 2.29x | 3.38x | 5.70x |
| Ryzen 7 9800X3D, Ubuntu 24.04 (WSL2) | gcc 13.3 | release | 1.01x | 1.09x | 1.31x | 3.20x | 4.23x | 6.73x |
| Ryzen 7 9800X3D, Ubuntu 24.04 (WSL2) | gcc 13.3 | PGO+LTO | 1.00x | 1.08x | 1.23x | 2.13x | 1.82x | 2.00x |

The pyperf tables below are for the previous revision; a pyperf run of the latest one on the same runners is in progress (`variants` workflow, `varJ`, which has the same code).

## Previous revision (a907379)


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
