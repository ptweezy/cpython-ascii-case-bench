# Apple M4, Apple clang 21.0.0, SDK 27.2, release, bench 440b4dd: layout run 2
8 shifts, 15 replay rounds, 3 length rounds. Quieter (no mediaanalysisd during timing; load 2.8-5.5 on 10 cores; WindowServer/WebKit background). Not pinned.

| Build | short main/build | 95% interval | doclower |
|---|---|---|---|
| PR (varJ) | 1.058x | 1.045-1.070 | 3.14x |
| PR+bm (varV) | 1.050x | 1.036-1.063 | 5.60x |
| ovl+bm (varW) | 1.085x | 1.070-1.100 | 5.59x |
| varY | 1.043x | 1.029-1.056 | 5.62x |
| varP | 1.041x | 1.027-1.054 | 5.62x |
| varQ | 1.069x | 1.052-1.088 | 5.63x |

| Length | main ns | PR | varP | varQ | PR+bm | ovl+bm | varY |
|---|---|---|---|---|---|---|---|
| 8 | 35.8 | 0.93x | 0.94x | 0.95x | 0.94x | 0.92x | 0.95x |
| 16 | 38.1 | 1.11x | 1.09x | 1.14x | 1.08x | 1.09x | 1.09x |
| 24 | 40.6 | 1.17x | 1.08x | 1.17x | 1.11x | 1.17x | 1.12x |
| 32 | 42.2 | 1.22x | 1.15x | 1.21x | 1.18x | 1.18x | 1.12x |
| 64 | 46.7 | 1.33x | 1.37x | 1.37x | 1.32x | 1.33x | 1.36x |
| 128 | 58.4 | 1.56x | 1.65x | 1.67x | 1.62x | 1.60x | 1.66x |
| 256 | 87.3 | 1.99x | 2.37x | 2.39x | 2.29x | 2.28x | 2.36x |
| 1,024 | 238.5 | 2.28x | 3.56x | 3.64x | 3.58x | 3.57x | 3.57x |
| 4,096 | 815.6 | 3.19x | 4.79x | 4.82x | 4.92x | 4.92x | 4.80x |
| 65,536 | 12406.6 | 3.44x | 5.63x | 5.64x | 5.74x | 5.74x | 5.62x |
