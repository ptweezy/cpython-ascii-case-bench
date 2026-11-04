# ThinkCentre (Fedora, gcc 16): varT and varU

Reported by the ThinkCentre session. Raw files on that machine under
`scratchpad/benchrepo/results/`: `spec-tu-gcc-fedora-spec/plain.tsv`,
`pgo-tu-gcc-fedora-pgo/plain.tsv`, `replay-spec-tu-gcc-fedora-spec.txt`,
`replay-pgo-tu-gcc-fedora-pgo.txt`, `*-checks.txt`, `layout-clang-plain.log`
(WORKDIR `~/abench/layout-clang-plain`).

Every tree passes edge_cases (253814) and check_all (1495930).

## Vector instructions in ascii_case_words

| set | T | U |
|---|---|---|
| gcc-fedora-spec (gcc 16 -O3 PGO LTO, Fedora flags) | 86 insns, 32 xmm | same |
| gcc-fedora-pgo | 86 insns, 32 xmm | same |

ascii_case_words stays a separate lto_priv symbol. _Py_bytes_lower: T 17 insns
(tail jump), U 90 insns, both 0 xmm. varP and varQ have 0 xmm in these sets.

Plain clang -O3, ascii_case_words:

| tree | insns | xmm |
|---|---|---|
| J | 100 | 30 |
| P | 147 | 65 |
| Q | 147 | 65 |
| T | 114 | 53 |
| U | 114 | 53 |

## 1. gcc-fedora-spec (pyperf geomean, main / variant)

| sizes | J | P | T | Q | U |
|---|---|---|---|---|---|
| all | 1.24 | 1.35 | 1.51 | 1.36 | 1.53 |
| 16 and under | 1.05 | 1.06 | 1.06 | 1.07 | 1.08 |
| 32-64 | 1.32 | 1.39 | 1.53 | 1.39 | 1.52 |
| 256 and up | 1.90 | 2.65 | 4.10 | 2.64 | 4.14 |

bytes.lower, ns:

| length | main | J | P | T | Q | U |
|---|---|---|---|---|---|---|
| 5 | 17.9 | 18.0 | 18.8 | 18.9 | 17.2 | 17.2 |
| 64 | 31.2 | 23.6 | 21.5 | 19.3 | 21.6 | 19.7 |
| 1,024 | 281.8 | 167.1 | 121.9 | 83.9 | 120.6 | 85.0 |
| 64K | 14478 | 7546 | 5429 | 2719 | 5485 | 2723 |

Workloads, ns:

| workload | main | J | P | T | Q | U |
|---|---|---|---|---|---|---|
| words | 20225 | 19563 | 19841 | 19838 | 21219 | 20612 |
| headers | 7969 | 7537 | 7389 | 7310 | 7263 | 7292 |

Replay (15 rounds), median main / build:

| workload | J | P | T | Q | U |
|---|---|---|---|---|---|
| doclower | 1.86 | 2.49 | 4.73 | 2.49 | 4.70 |
| http | 1.13 | 1.08 | 1.13 | 1.16 | 1.21 |
| words | 1.02 | 0.97 | 1.01 | 1.09 | 1.13 |
| urls | 1.06 | 0.99 | 1.04 | 1.08 | 1.12 |
| email | 1.03 | 0.99 | 1.03 | 1.08 | 1.13 |
| paths | 1.02 | 0.96 | 1.01 | 1.05 | 1.07 |
| pgotask | 1.01 | 0.96 | 1.00 | 1.05 | 1.07 |
| html | 1.01 | 0.96 | 0.99 | 1.04 | 1.05 |

## 2. gcc-fedora-pgo (pyperf geomean, main / variant)

| sizes | J | P | T | Q | U |
|---|---|---|---|---|---|
| all | 1.23 | 1.34 | 1.47 | 1.36 | 1.52 |
| 16 and under | 1.06 | 1.09 | 1.06 | 1.11 | 1.11 |
| 32-64 | 1.33 | 1.41 | 1.49 | 1.41 | 1.52 |
| 256 and up | 1.79 | 2.39 | 3.71 | 2.40 | 3.73 |

bytes.lower, ns:

| length | main | J | P | T | Q | U |
|---|---|---|---|---|---|---|
| 1,024 | 280.8 | 164.2 | 122.7 | 86.6 | 122.6 | 85.8 |
| 64K | 14542 | 7273 | 5454 | 2690 | 5340 | 2718 |

Replay, median main / build:

| workload | J | P | T | Q | U |
|---|---|---|---|---|---|
| doclower | 1.89 | 2.48 | 4.71 | 2.49 | 4.71 |
| http | 1.06 | 1.10 | 1.06 | 1.13 | 1.11 |
| words | 0.99 | 1.01 | 0.97 | 1.08 | 1.07 |
| urls | 1.02 | 1.04 | 1.00 | 1.08 | 1.05 |
| email | 1.00 | 1.04 | 0.99 | 1.08 | 1.06 |
| paths | 0.98 | 1.01 | 0.96 | 1.05 | 1.03 |
| pgotask | 0.99 | 1.02 | 0.98 | 1.06 | 1.04 |
| html | 0.97 | 1.01 | 0.96 | 1.04 | 1.03 |

## 3. layout_local, plain clang -O3 (8 shifts, 5 rounds)

| build | short ns | main / build | 95% interval | range over shifts |
|---|---|---|---|---|
| main | 49.49 | 1.000 | - | 9% |
| J | 47.43 | 1.043 | 1.004-1.077 | 13% |
| P | 47.00 | 1.053 | 1.023-1.083 | 9% |
| Q | 45.27 | 1.093 | 1.065-1.123 | 7% |
| T | 47.58 | 1.040 | 1.009-1.070 | 9% |
| U | 46.05 | 1.075 | 1.033-1.111 | 15% (51.4 at +4080, about 45.4 elsewhere) |

doclower main / build: J 4.10, P 3.25, Q 3.25, T 4.15, U 4.15.

Fixed lengths, main / build:

| length | J | P | Q | T | U |
|---|---|---|---|---|---|
| 256 | 1.75 | 1.71 | 1.72 | 1.82 | 1.81 |
| 1,024 | 2.42 | 2.13 | 2.16 | 2.45 | 2.38 |
| 4,096 | 3.32 | 2.61 | 2.61 | 3.22 | 3.21 |
| 65,536 | 4.08 | 3.17 | 3.16 | 4.12 | 4.12 |
