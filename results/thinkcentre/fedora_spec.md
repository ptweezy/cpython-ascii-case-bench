# ThinkCentre (i5-12400T, Fedora 44, gcc 16.2.1): Fedora's real python3 recipe
-O3 + PGO + LTO + _FORTIFY_SOURCE=3 (optflags minus -O2 in CFLAGS_NODIST, EXTRA_CFLAGS=-O3), pyperf n=30.
Vector code in ascii_case_words: PR 0, PR+bm 0, varX 31, varY 32 xmm (the PGO profile leaves the PR's loop cold).

| sizes (pyperf geomean main/variant) | PR | PR+bm | varX | varY |
|---|---|---|---|---|
| all | 1.24x | 1.21x | 1.48x | 1.51x |
| 16 and under | 1.05x | 1.02x | 1.03x | 1.06x |
| 32-64 | 1.32x | 1.31x | 1.50x | 1.53x |
| 256 and up | 1.90x | 1.89x | 4.01x | 4.06x |

| bytes.lower ns | main | PR | PR+bm | varX | varY |
|---|---|---|---|---|---|
| 1 | 16.5 | 16.5 | 16.5 | 16.7 | 16.5 |
| 5 | 17.8 | 18.0 | 20.3 | 19.1 | 18.3 |
| 16 | 21.3 | 18.4 | 18.2 | 17.9 | 17.4 |
| 64 | 31.3 | 23.6 | 23.8 | 20.2 | 19.7 |
| 256 | 79.5 | 52.0 | 52.7 | 28.9 | 26.5 |
| 1,024 | 266.4 | 164.6 | 166.6 | 89.0 | 89.2 |
| 64K | 14487 | 7554 | 7599 | 2687 | 2747 |

Replay main/build, best (median): doclower PR 1.86, PR+bm 1.87, varX 4.81, varY 4.80; http 1.12 (1.09) / 1.11 (1.08) / 1.13 (1.16) / 1.13 (1.17); urls 1.06/1.04/1.06/1.04; email 1.03/1.02/1.07/1.05; words 1.01/0.99/1.02/1.02; pgotask 1.00/0.99/1.04/1.01.
