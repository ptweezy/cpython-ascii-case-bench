# AVX-512 without PGO: gcc 13.3 -O3 -march=x86-64-v4 (Ryzen 7 9800X3D, Zen 5, WSL2)

`realworld/layout_local.sh WORK "varJ varB varB5" "CFLAGS=-march=x86-64-v4"`, 8 shifts, REPLAY_CPU=4. `varB5` is `varB` with a 64-byte vector block under `__AVX512F__` (`variants/varB5.patch`). Every build passed edge_cases.py (253,814 cases) and check_all.py (1,495,930 cases).

Vector registers in `ascii_case_words` (objdump, instructions with a zmm / ymm operand): varJ (PR) 12 / 12, varB 12 / 36, varB5 36 / 12.

## Fixed lengths

main / build, geometric mean over shifts (range over shifts of ns / mean):

| Length | main ns | varB | varB5 | varJ |
|---|---|---|---|---|
| 8 | 34.4 | 1.03x (0.99-1.01) | 1.03x (0.98-1.01) | 1.03x (0.98-1.02) |
| 16 | 36.4 | 1.08x (0.99-1.01) | 1.08x (0.99-1.03) | 1.09x (0.99-1.02) |
| 24 | 38.3 | 1.11x (0.99-1.01) | 1.11x (0.98-1.04) | 1.11x (0.98-1.01) |
| 32 | 39.7 | 1.18x (0.99-1.01) | 1.14x (0.98-1.04) | 1.14x (0.98-1.02) |
| 64 | 45.4 | 1.37x (0.99-1.01) | 1.37x (0.98-1.04) | 1.31x (0.98-1.01) |
| 128 | 58.1 | 1.72x (0.99-1.01) | 1.72x (0.98-1.05) | 1.62x (0.98-1.02) |
| 256 | 97.9 | 2.82x (0.99-1.01) | 2.85x (0.98-1.04) | 2.70x (0.98-1.02) |
| 1,024 | 266.6 | 4.61x (0.96-1.05) | 4.97x (0.99-1.02) | 4.54x (0.99-1.03) |
| 4,096 | 887.7 | 9.16x (0.98-1.05) | 12.13x (0.99-1.01) | 9.40x (0.99-1.02) |
| 65,536 | 13292.6 | 15.84x (0.95-1.06) | 20.43x (0.99-1.01) | 15.24x (0.99-1.01) |

## Short-string replay

###   run : 

Short mix, ns per call (geometric mean of the short workloads), per shift:

| Build | +0 | +16 | +32 | +48 | +1024 | +2064 | +3104 | +4080 | range |
|---|---|---|---|---|---|---|---|---|---|
| main | 39.6 | 39.8 | 39.5 | 39.0 | 40.2 | 38.4 | 38.8 | 37.0 | 9% |
| varB | 37.5 | 38.0 | 41.5 | 37.4 | 37.3 | 35.8 | 36.2 | 36.2 | 16% |
| varB5 | 36.3 | 36.0 | 36.1 | 36.2 | 36.7 | 37.6 | 37.4 | 38.4 | 7% |
| varJ | 36.9 | 36.3 | 36.6 | 38.9 | 36.2 | 37.3 | 39.5 | 37.4 | 9% |

| Build | short ns (mean over shifts) | main / build | 95% interval | doclower main / build |
|---|---|---|---|---|
| main | 39.02 | 1.000x | 0.977-1.024 | 1.00x |
| varB | 37.44 | 1.042x | 1.004-1.074 | 13.06x |
| varB5 | 36.82 | 1.060x | 1.036-1.082 | 16.39x |
| varJ | 37.39 | 1.044x | 1.016-1.071 | 13.07x |
