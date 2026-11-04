# Apple M4 (Parker's Mac), Apple clang 21.0.0, SDK 27.2, release builds, bench 29fafa7
Layout run 1: 8 shifts, 5 replay rounds, 3 length rounds. Background: mediaanalysisd ~115% CPU, load 4.8-7.3 on 10 cores; not pinned.

| Build | short main/build | 95% interval | doclower |
|---|---|---|---|
| PR (varJ) | 1.051x | 1.033-1.069 | 3.13x |
| PR+bm (varV) | 1.035x | 1.017-1.053 | 5.59x |
| ovl+bm (varW) | 1.057x | 1.036-1.080 | 5.56x |
| varX | 1.023x | 1.001-1.042 | 4.54x |
| varY | 1.022x | 1.004-1.041 | 5.58x |

| Length | main ns | PR | PR+bm | ovl+bm | varX | varY |
|---|---|---|---|---|---|---|
| 8 | 35.7 | 0.91x | 0.92x | 0.96x | 0.92x | 0.91x |
| 16 | 37.9 | 1.10x | 1.01x | 1.10x | 1.11x | 1.07x |
| 24 | 40.8 | 1.16x | 1.13x | 1.18x | 1.11x | 1.10x |
| 32 | 42.4 | 1.22x | 1.19x | 1.22x | 1.17x | 1.19x |
| 64 | 47.2 | 1.37x | 1.36x | 1.35x | 1.37x | 1.40x |
| 128 | 58.6 | 1.57x | 1.63x | 1.62x | 1.64x | 1.66x |
| 256 | 87.9 | 2.00x | 2.32x | 2.31x | 2.34x | 2.37x |
| 1,024 | 238.1 | 2.26x | 3.62x | 3.58x | 3.25x | 3.59x |
| 4,096 | 816.4 | 3.19x | 4.94x | 4.92x | 4.06x | 4.80x |
| 65,536 | 12485.6 | 3.43x | 5.76x | 5.76x | 4.59x | 5.67x |
