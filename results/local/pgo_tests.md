# The proposed tests in PGO training: gcc 13 PGO+LTO (Ryzen 7 9800X3D, Zen 5, WSL2)

`realworld/layout_local.sh` with `./configure --enable-optimizations --with-lto` (CPython's default training, `-m test --pgo`, which runs `test_str` and `test_bytes`), 8 shifts, pinned to CPU 4. `varJ` is the PR's code. `varJt` and `varBt` are `varJ` and `varB` with the two proposed tests added to `Lib/test` (`tests/add_tests.py`), so the PGO training runs them; `main`, `varJ` and `varB` don't have them. One PGO build per tree. SIMD: SSE instructions in `ascii_case_words` (objdump).

main / build, geometric mean over shifts (range over shifts of ns / mean):

| Length | main ns | varB | varBt | varJ | varJt |
|---|---|---|---|---|---|
| 8 | 28.5 | 1.00x (0.98-1.05) | 1.03x (0.98-1.04) | 1.01x (0.99-1.03) | 1.06x (0.99-1.01) |
| 16 | 30.1 | 1.07x (0.97-1.04) | 1.11x (0.98-1.04) | 1.06x (0.99-1.03) | 1.09x (0.98-1.02) |
| 24 | 32.3 | 1.11x (0.98-1.04) | 1.16x (0.98-1.05) | 1.10x (0.99-1.01) | 1.12x (0.99-1.01) |
| 32 | 34.1 | 1.17x (0.98-1.05) | 1.22x (0.98-1.04) | 1.14x (1.00-1.01) | 1.18x (0.99-1.01) |
| 64 | 39.7 | 1.35x (0.98-1.04) | 1.42x (0.99-1.05) | 1.26x (1.00-1.00) | 1.36x (0.99-1.01) |
| 128 | 52.9 | 1.70x (0.98-1.03) | 1.80x (0.99-1.04) | 1.43x (0.99-1.01) | 1.74x (0.99-1.02) |
| 256 | 92.3 | 2.67x (0.96-1.05) | 2.84x (0.99-1.03) | 1.94x (0.99-1.02) | 2.68x (0.99-1.01) |
| 1,024 | 260.6 | 3.26x (0.93-1.12) | 4.00x (0.99-1.02) | 1.92x (0.97-1.10) | 2.95x (0.99-1.00) |
| 4,096 | 891.8 | 4.15x (0.93-1.17) | 5.46x (0.99-1.01) | 2.20x (0.95-1.14) | 3.57x (1.00-1.00) |
| 65,536 | 13508.7 | 4.90x (0.93-1.23) | 6.72x (1.00-1.00) | 2.32x (0.95-1.16) | 3.98x (1.00-1.00) |

Short-string mix:

| Build | short ns (mean over shifts) | main / build | 95% interval | doclower main / build |
|---|---|---|---|---|
| main | 34.45 | 1.000x | 0.971-1.031 | 1.00x |
| varB | 33.63 | 1.024x | 0.986-1.062 | 4.68x |
| varBt | 32.59 | 1.057x | 1.022-1.092 | 6.27x |
| varJ | 33.58 | 1.026x | 0.990-1.060 | 2.28x |
| varJt | 33.06 | 1.042x | 1.003-1.081 | 3.84x |

SIMD instructions in `ascii_case_words`: varJ 0, varJt 45, varB 31, varBt 82.

## MSVC 19.51 x64 PGO (`PCbuild\build.bat --pgo`, as python.org's 64-bit installer), Windows 11 on the same machine

`PCbuild/amd64-PRt-pgo` and `PCbuild/amd64-varBt-pgo` were built with the tests added (`explore/win32/build_tests.ps1`); the training ran `test_bytes` and `test_str` with them, and both passed. One layout per build, pinned to CPU 4 at high priority: fixed lengths (5 rounds) and the real-world replay (15 rounds). SIMD: instructions with an xmm operand in `ascii_case_words` (`results/local/msvc_simd.md`).

| Tree | SIMD | 16 | 128 | 1,024 | 64K | Short mix (best / median) |
|---|---|---|---|---|---|---|
| PR | 0 | 1.07x | 1.50x | 2.27x | 2.64x | 1.020x / 1.025x |
| PR + tests | 0 | 1.07x | 1.49x | 2.28x | 2.64x | 1.032x / 1.039x |
| `varB` | 32 | 1.08x | 1.70x | 3.41x | 5.74x | 1.018x / 1.076x |
| `varB` + tests | 32 | 1.05x | 1.66x | 3.38x | 5.72x | 1.009x / 1.075x |

With the tests, MSVC's PGO build still leaves the PR's loop scalar (the same instructions as without them), and nothing measurable changes for either tree.
