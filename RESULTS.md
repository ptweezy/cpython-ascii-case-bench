# Results for gh-161155 / python/cpython#161201

Every number compares the PR (9433a66) with `main`: time on `main` / time with the PR, so above 1.00x the PR is faster. Columns are geometric means over `str.lower`, `str.upper` and `bytes.lower` at those lengths. Strings shorter than 8 characters take the same code path as on `main`, so that column shows the noise level.

The PR converts a machine word at a time for strings of at least one word. Under MSVC the word loop counts words, since MSVC only vectorizes loops that count by one; other compilers step by bytes, because counting words makes clang use post-indexed loads and stores on AArch64, which are slower on Apple cores.

## GitHub-hosted runners (pyperf)

The `variants` workflow is timing `main` (4e0677a) and the PR's code (`varJ`) on each runner: [release](https://github.com/ptweezy/cpython-ascii-case-bench/actions/runs/41548841945), [PGO](https://github.com/ptweezy/cpython-ascii-case-bench/actions/runs/41548844554) and [auto-vectorization off](https://github.com/ptweezy/cpython-ascii-case-bench/actions/runs/41548847083). The tables will appear here when the runs finish.

## Local machines (timeit)

`bench_drive.py`: best of 5 interleaved rounds of `timeit`, `main` (e4dba41 on these machines) and the PR built the same way on the same machine.

| Machine | Compiler | Build | ≤7 chars | 8-16 | 24-64 | 256 | 1,024 | 64K |
|---|---|---|---|---|---|---|---|---|
| Ryzen 7 9800X3D, Windows 11 | MSVC 19.51 | release | 1.01x | 1.03x | 1.16x | 2.29x | 3.38x | 5.70x |
| Ryzen 7 9800X3D, Ubuntu 24.04 (WSL2) | gcc 13.3 | release | 1.01x | 1.09x | 1.31x | 3.20x | 4.23x | 6.73x |
| Ryzen 7 9800X3D, Ubuntu 24.04 (WSL2) | gcc 13.3 | PGO+LTO | 1.00x | 1.08x | 1.23x | 2.13x | 1.82x | 2.00x |
| Core i5-12400T, Fedora 44 | gcc 16.2 | release | 1.13x | 1.13x | 1.35x | 2.68x | 3.08x | 5.29x |
| Core i5-12400T, Fedora 44 | gcc 16.2 | PGO+LTO | 0.98x | 1.10x | 1.29x | 1.56x | 1.71x | 2.04x |
| Core i5-12400T, Fedora 44 | clang 22.1 | release | 1.03x | 1.12x | 1.27x | 2.11x | 2.85x | 4.48x |
| Core i5-12400T, Fedora 44 | clang 22.1 | PGO+LTO | 1.00x | 1.11x | 1.37x | 2.15x | 2.26x | 3.15x |
