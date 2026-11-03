# Results for gh-161155 / python/cpython#161201

Every number compares the PR (9433a66) with `main`: time on `main` / time with the PR, so above 1.00x the PR is faster. Columns are geometric means over `str.lower`, `str.upper` and `bytes.lower` at those lengths. Strings shorter than 8 characters run the same loop as on `main` after one length check, so that column shows the noise level, including shifts of a few percent either way from where the code lands in the binary.

The PR converts a machine word at a time for strings of at least one word. Under MSVC the word loop counts words, since MSVC only vectorizes loops that count by one; other compilers step by bytes, because counting words makes clang use post-indexed loads and stores on AArch64, which are slower on Apple cores.

| Machine | Compiler | Build | ≤7 chars | 8-16 | 24-64 | 256 | 1,024 | 64K |
|---|---|---|---|---|---|---|---|---|
| Ryzen 7 9800X3D, Windows 11 | MSVC 19.51 | release | 1.01x | 1.03x | 1.16x | 2.29x | 3.38x | 5.70x |
| Ryzen 7 9800X3D, Windows 11 | MSVC 19.51 | PGO | 1.04x | 1.08x | 1.26x | 2.06x | 2.40x | 2.47x |
| Ryzen 7 9800X3D, Ubuntu 24.04 (WSL2) | gcc 13.3 | release | 1.01x | 1.09x | 1.31x | 3.20x | 4.23x | 6.73x |
| Ryzen 7 9800X3D, Ubuntu 24.04 (WSL2) | gcc 13.3 | PGO+LTO | 1.00x | 1.08x | 1.23x | 2.13x | 1.82x | 2.00x |
| Core i5-12400T, Fedora 44 | gcc 16.2 | release | 1.13x | 1.13x | 1.35x | 2.68x | 3.08x | 5.29x |
| Core i5-12400T, Fedora 44 | gcc 16.2 | PGO+LTO | 0.98x | 1.10x | 1.29x | 1.56x | 1.71x | 2.04x |
| Core i5-12400T, Fedora 44 | clang 22.1 | release | 1.03x | 1.12x | 1.27x | 2.11x | 2.85x | 4.48x |
| Core i5-12400T, Fedora 44 | clang 22.1 | PGO+LTO | 1.00x | 1.11x | 1.37x | 2.15x | 2.26x | 3.15x |
| Apple M4, macOS 27.2 | Apple clang 21 | release | 1.02x | 1.16x | 1.40x | 2.74x | 2.71x | 4.30x |
| Apple M4, macOS 27.2 | Apple clang 21 | PGO+LTO | 1.04x | 1.13x | 1.44x | 3.04x | 3.04x | 4.52x |
| GitHub `windows-2025`, AMD EPYC 9V74 | MSVC 19.51 | release | 0.97x | 1.01x | 1.15x | — | 2.85x | 5.79x |
| GitHub `windows-11-arm`, Cobalt 100 | MSVC 19.51 | release | 0.99x | 1.03x | 1.16x | — | 2.20x | 3.00x |
| GitHub `ubuntu-24.04`, AMD EPYC 7763 | gcc 13.3 | release | 1.02x | 1.08x | 1.36x | — | 3.52x | 6.24x |
| GitHub `ubuntu-24.04-arm`, Neoverse-N2 | gcc 13.3 | release | 1.00x | 1.07x | 1.31x | — | 2.87x | 4.22x |
| GitHub `macos-15`, Apple M1 (Virtual) | Apple clang 17 | release | 1.03x | 1.15x | 1.39x | — | 2.59x | 3.57x |

Still running: the runner PGO and no-auto-vec builds, and the second `macos-15-intel` release job. Their rows will be added here.

## How it was measured

- **Own machines:** `bench_drive.py`, best of 5 interleaved rounds of `timeit`. Each machine builds one tree twice, the same way: once with `main`'s `Objects/bytes_methods.c` and once with the PR's. Lengths: 5; 8, 12, 16; 24, 32, 64; 256; 1,024; 65,536.
- **GitHub-hosted runners:** the `variants` workflow ([release](https://github.com/ptweezy/cpython-ascii-case-bench/actions/runs/41548841945), [PGO](https://github.com/ptweezy/cpython-ascii-case-bench/actions/runs/41548844554) and [auto-vectorization off](https://github.com/ptweezy/cpython-ascii-case-bench/actions/runs/41548847083)) times `main` (4e0677a) and the same tree with the PR's code (`varJ`) using pyperf, in two jobs per runner, combined by geometric mean. Lengths: 1, 3, 5, 7; 8, 11, 15, 16; 32, 64; 1,024; 65,536. Only `str.lower` is timed at 32, 64 and 65,536, and there is no 256 case. "No auto-vec" builds both with `-fno-tree-vectorize` (gcc) or `-fno-vectorize -fno-slp-vectorize` (clang).
