# AVX-512 without PGO: clang 18.1 -O3 -march=x86-64-v4 (Ryzen 7 9800X3D, Zen 5, WSL2)

`realworld/layout_local.sh WORK "varJ varB varB5" CC=clang "CFLAGS=-march=x86-64-v4"`, 8 shifts, REPLAY_CPU=4. Every build passed edge_cases.py (253,814 cases) and check_all.py (1,495,930 cases). clang splits 64-byte vectors into two 32-byte halves here (its tuning prefers 256-bit vectors).

Vector registers in `ascii_case_words` (objdump, instructions with a zmm / ymm operand): varJ (PR) 0 / 36, varB 0 / 72, varB5 0 / 108.

## Fixed lengths

main / build, geometric mean over shifts (range over shifts of ns / mean):

| Length | main ns | varB | varB5 | varJ |
|---|---|---|---|---|
| 8 | 35.2 | 1.03x (0.98-1.02) | 1.04x (0.99-1.01) | 1.04x (0.99-1.03) |
| 16 | 37.4 | 1.09x (0.99-1.02) | 1.10x (0.99-1.01) | 1.10x (0.98-1.03) |
| 24 | 40.3 | 1.14x (0.98-1.02) | 1.15x (0.99-1.03) | 1.14x (0.99-1.02) |
| 32 | 41.9 | 1.20x (0.98-1.02) | 1.19x (0.98-1.03) | 1.19x (0.99-1.03) |
| 64 | 46.3 | 1.34x (0.99-1.02) | 1.36x (0.99-1.01) | 1.27x (0.99-1.02) |
| 128 | 56.4 | 1.62x (0.99-1.01) | 1.64x (0.99-1.01) | 1.39x (0.99-1.03) |
| 256 | 77.1 | 2.15x (0.99-1.01) | 2.17x (0.99-1.01) | 1.85x (0.99-1.02) |
| 1,024 | 215.9 | 3.69x (0.97-1.06) | 3.91x (0.99-1.01) | 3.27x (0.99-1.02) |
| 4,096 | 727.0 | 8.27x (0.96-1.08) | 8.74x (0.99-1.00) | 8.16x (0.99-1.01) |
| 65,536 | 10871.4 | 14.40x (0.95-1.17) | 15.22x (1.00-1.00) | 15.17x (1.00-1.00) |

## Short-string replay

###   run : 

Short mix, ns per call (geometric mean of the short workloads), per shift:

| Build | +0 | +16 | +32 | +48 | +1024 | +2064 | +3104 | +4080 | range |
|---|---|---|---|---|---|---|---|---|---|
| main | 40.4 | 40.4 | 40.9 | 40.2 | 39.7 | 41.1 | 40.7 | 39.5 | 4% |
| varB | 39.2 | 38.5 | 37.7 | 38.3 | 38.4 | 39.3 | 38.5 | 39.0 | 4% |
| varB5 | 38.5 | 38.4 | 38.9 | 37.6 | 39.0 | 38.1 | 38.4 | 39.3 | 4% |
| varJ | 38.4 | 38.5 | 40.2 | 38.6 | 39.5 | 39.3 | 39.0 | 40.7 | 6% |

| Build | short ns (mean over shifts) | main / build | 95% interval | doclower main / build |
|---|---|---|---|---|
| main | 40.37 | 1.000x | 0.988-1.013 | 1.00x |
| varB | 38.63 | 1.045x | 1.032-1.058 | 11.32x |
| varB5 | 38.52 | 1.048x | 1.035-1.061 | 11.83x |
| varJ | 39.27 | 1.028x | 1.010-1.044 | 11.61x |
