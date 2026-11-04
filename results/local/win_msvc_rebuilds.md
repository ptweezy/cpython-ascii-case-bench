# MSVC 19.51 x64 (Ryzen 7 9800X3D): PGO rebuild noise, and the Release block

Four x64 PGO builds each of the PR and `varB` (`PCbuild\build.bat --pgo`, as python.org's 64-bit installer; `explore/win32/build_rebuilds.ps1` builds them alternately), and the x64 Release builds of `main`, the PR, `varR` and `varB`. Every build passed edge_cases.py and check_all.py. Fixed lengths: the four rebuilds of a tree are its "shifts" (5 rounds); the replay: 15 rounds. Pinned to CPU 4 at high priority.

## PGO: short strings over four rebuilds each

Geometric mean over the eight short workloads, main / build:

| | Build 1 | Build 2 | Build 3 | Build 4 | Geometric mean |
|---|---|---|---|---|---|
| PR, best | 1.010x | 1.038x | 1.026x | 1.040x | 1.029x |
| `varB`, best | 1.012x | 1.024x | 1.012x | 1.024x | 1.018x |
| PR, median | 1.008x | 1.041x | 1.038x | 1.084x | 1.042x |
| `varB`, median | 1.009x | 1.025x | 1.026x | 1.072x | 1.033x |

`varB` / PR: 0.990x (best), 0.991x (median); per workload (best) config 0.962x, urls 0.982x, http 0.985x, email 0.994x, words 0.993x, html, paths and pgotask 1.00x. The rebuilds of one tree spread over 3% by best times and 7% by median.

A likely part of the 1%: in the PGO build, `varB`'s `ascii_case_words` adjusts the stack, saves `xmm6` (callee-saved in the Windows x64 ABI) and splats its two constants into vector registers on every call, before the `len >= 16` test, so strings of 8 to 15 bytes pay about 8 more instructions than with the PR.

```
##### x64-pgo-rebuilds lengths (12:35:18)
main / build, geometric mean over shifts (range over shifts of ns / mean):

| Length | main ns | PR | varB |
|---|---|---|---|
| 8 | 33.8 | 1.03x (0.99-1.03) | 1.02x (0.98-1.02) |
| 16 | 34.9 | 1.05x (0.98-1.03) | 1.06x (0.98-1.02) |
| 24 | 38.0 | 1.10x (0.98-1.03) | 1.11x (0.99-1.01) |
| 32 | 38.8 | 1.12x (0.97-1.04) | 1.16x (0.99-1.02) |
| 64 | 47.8 | 1.27x (0.96-1.05) | 1.40x (0.98-1.01) |
| 128 | 59.8 | 1.45x (0.97-1.04) | 1.69x (0.98-1.03) |
| 256 | 114.0 | 2.29x (0.97-1.04) | 2.94x (0.97-1.02) |
| 1,024 | 272.7 | 2.30x (0.99-1.00) | 3.37x (0.98-1.04) |
| 4,096 | 857.7 | 2.45x (0.97-1.01) | 4.42x (0.99-1.03) |
| 65,536 | 12723.6 | 2.67x (0.97-1.01) | 5.72x (1.00-1.00) |
##### x64-pgo-rebuilds replay (12:35:25)

best ns per call: | Workload | base | PR1 | PR2 | PR3 | PR4 | varB1 | varB2 | varB3 | varB4 |
| config | 38.0 | 37.2 | 36.1 | 36.3 | 36.3 | 38.4 | 37.5 | 38.1 | 37.6 |
| doclower | 3225.6 | 1279.6 | 1239.5 | 1281.9 | 1284.5 | 648.5 | 643.7 | 649.1 | 640.1 |
| email | 37.1 | 37.4 | 35.8 | 36.2 | 36.3 | 36.9 | 36.5 | 36.7 | 36.5 |
| html | 36.3 | 36.5 | 36.1 | 37.0 | 35.6 | 36.5 | 36.0 | 36.5 | 36.0 |
| http | 37.6 | 34.5 | 33.8 | 34.2 | 34.1 | 34.6 | 34.6 | 34.9 | 34.6 |
| paths | 35.3 | 35.8 | 34.8 | 35.2 | 34.7 | 35.3 | 34.8 | 35.3 | 35.0 |
| pgotask | 38.6 | 38.8 | 37.5 | 38.5 | 37.2 | 38.2 | 37.7 | 38.3 | 37.7 |
| urls | 36.6 | 35.9 | 34.8 | 34.9 | 34.7 | 36.0 | 35.6 | 35.9 | 35.4 |
| words | 37.9 | 38.4 | 37.6 | 37.6 | 37.1 | 38.2 | 37.7 | 38.1 | 37.7 |

main / build (best): | Workload | PR1 | PR2 | PR3 | PR4 | varB1 | varB2 | varB3 | varB4 |
| config | 1.02x | 1.05x | 1.05x | 1.05x | 0.99x | 1.01x | 1.00x | 1.01x |
| doclower | 2.52x | 2.60x | 2.52x | 2.51x | 4.97x | 5.01x | 4.97x | 5.04x |
| email | 0.99x | 1.03x | 1.03x | 1.02x | 1.00x | 1.02x | 1.01x | 1.02x |
| html | 0.99x | 1.01x | 0.98x | 1.02x | 1.00x | 1.01x | 1.00x | 1.01x |
| http | 1.09x | 1.12x | 1.10x | 1.11x | 1.09x | 1.09x | 1.08x | 1.09x |
| paths | 0.99x | 1.01x | 1.00x | 1.02x | 1.00x | 1.02x | 1.00x | 1.01x |
| pgotask | 1.00x | 1.03x | 1.00x | 1.04x | 1.01x | 1.02x | 1.01x | 1.02x |
| urls | 1.02x | 1.05x | 1.05x | 1.05x | 1.01x | 1.03x | 1.02x | 1.03x |
| words | 0.99x | 1.01x | 1.01x | 1.02x | 0.99x | 1.01x | 1.00x | 1.01x |

median ns per call: | Workload | base | PR1 | PR2 | PR3 | PR4 | varB1 | varB2 | varB3 | varB4 |
| config | 40.9 | 40.2 | 39.0 | 38.4 | 37.4 | 41.1 | 40.1 | 40.5 | 38.6 |
| doclower | 3241.8 | 1289.6 | 1246.3 | 1290.1 | 1289.6 | 653.1 | 652.8 | 660.4 | 649.1 |
| email | 39.5 | 39.9 | 38.6 | 38.8 | 37.2 | 39.8 | 39.1 | 38.8 | 37.4 |
| html | 38.8 | 39.6 | 38.3 | 39.0 | 36.8 | 39.3 | 38.5 | 38.4 | 36.9 |
| http | 40.7 | 37.9 | 36.4 | 36.0 | 34.8 | 37.5 | 37.2 | 37.2 | 35.6 |
| paths | 38.2 | 38.7 | 37.3 | 37.3 | 35.9 | 38.2 | 37.7 | 37.4 | 36.0 |
| pgotask | 40.9 | 41.2 | 40.3 | 41.1 | 38.5 | 40.8 | 40.5 | 40.5 | 38.4 |
| urls | 39.4 | 38.1 | 37.0 | 36.8 | 35.6 | 38.6 | 38.0 | 38.0 | 36.4 |
| words | 40.7 | 41.1 | 39.7 | 40.1 | 38.3 | 41.1 | 40.3 | 40.3 | 38.4 |

main / build (median): | Workload | PR1 | PR2 | PR3 | PR4 | varB1 | varB2 | varB3 | varB4 |
| config | 1.02x | 1.05x | 1.06x | 1.09x | 0.99x | 1.02x | 1.01x | 1.06x |
| doclower | 2.51x | 2.60x | 2.51x | 2.51x | 4.96x | 4.97x | 4.91x | 4.99x |
| email | 0.99x | 1.02x | 1.02x | 1.06x | 0.99x | 1.01x | 1.02x | 1.06x |
| html | 0.98x | 1.01x | 0.99x | 1.05x | 0.99x | 1.01x | 1.01x | 1.05x |
| http | 1.08x | 1.12x | 1.13x | 1.17x | 1.09x | 1.10x | 1.09x | 1.14x |
| paths | 0.99x | 1.02x | 1.02x | 1.07x | 1.00x | 1.01x | 1.02x | 1.06x |
| pgotask | 0.99x | 1.02x | 0.99x | 1.06x | 1.00x | 1.01x | 1.01x | 1.07x |
| urls | 1.03x | 1.06x | 1.07x | 1.11x | 1.02x | 1.04x | 1.04x | 1.08x |
| words | 0.99x | 1.03x | 1.02x | 1.06x | 0.99x | 1.01x | 1.01x | 1.06x |
##### x64-rel lengths (12:36:54)
main / build, geometric mean over shifts (range over shifts of ns / mean):

| Length | main ns | PR | varB | varR |
|---|---|---|---|---|
| 8 | 49.7 | 1.01x (1.00-1.00) | 0.97x (1.00-1.00) | 0.98x (1.00-1.00) |
| 16 | 51.5 | 1.03x (1.00-1.00) | 0.99x (1.00-1.00) | 0.99x (1.00-1.00) |
| 24 | 54.1 | 1.06x (1.00-1.00) | 1.04x (1.00-1.00) | 1.03x (1.00-1.00) |
| 32 | 55.7 | 1.09x (1.00-1.00) | 1.07x (1.00-1.00) | 1.06x (1.00-1.00) |
| 64 | 62.7 | 1.21x (1.00-1.00) | 1.19x (1.00-1.00) | 1.19x (1.00-1.00) |
| 128 | 74.6 | 1.39x (1.00-1.00) | 1.39x (1.00-1.00) | 1.37x (1.00-1.00) |
| 256 | 109.8 | 1.95x (1.00-1.00) | 1.84x (1.00-1.00) | 1.84x (1.00-1.00) |
| 1,024 | 277.2 | 2.90x (1.00-1.00) | 2.53x (1.00-1.00) | 2.52x (1.00-1.00) |
| 4,096 | 865.0 | 4.46x (1.00-1.00) | 3.18x (1.00-1.00) | 3.14x (1.00-1.00) |
| 65,536 | 12701.6 | 5.71x (1.00-1.00) | 3.88x (1.00-1.00) | 3.89x (1.00-1.00) |
##### x64-rel replay (12:37:00)

best ns per call: | Workload | base | PR | varR | varB |
| config | 58.5 | 56.1 | 59.0 | 59.3 |
| doclower | 3248.8 | 668.6 | 921.4 | 919.8 |
| email | 56.9 | 56.2 | 57.2 | 57.6 |
| html | 56.3 | 55.0 | 57.3 | 57.6 |
| http | 59.1 | 53.9 | 55.2 | 55.6 |
| paths | 56.2 | 54.7 | 55.8 | 55.9 |
| pgotask | 58.2 | 57.4 | 58.5 | 58.4 |
| urls | 57.0 | 54.5 | 56.2 | 56.5 |
| words | 58.6 | 57.2 | 58.5 | 58.9 |

main / build (best): | Workload | PR | varR | varB |
| config | 1.04x | 0.99x | 0.99x |
| doclower | 4.86x | 3.53x | 3.53x |
| email | 1.01x | 0.99x | 0.99x |
| html | 1.02x | 0.98x | 0.98x |
| http | 1.10x | 1.07x | 1.06x |
| paths | 1.03x | 1.01x | 1.00x |
| pgotask | 1.01x | 1.00x | 1.00x |
| urls | 1.04x | 1.01x | 1.01x |
| words | 1.02x | 1.00x | 0.99x |

median ns per call: | Workload | base | PR | varR | varB |
| config | 60.3 | 57.8 | 60.5 | 61.2 |
| doclower | 3255.5 | 673.9 | 926.8 | 931.4 |
| email | 59.9 | 57.8 | 58.9 | 59.0 |
| html | 57.6 | 57.0 | 58.6 | 58.6 |
| http | 61.0 | 55.7 | 57.2 | 57.8 |
| paths | 57.5 | 56.1 | 58.0 | 58.6 |
| pgotask | 60.7 | 59.1 | 60.0 | 60.4 |
| urls | 58.4 | 56.1 | 57.7 | 58.0 |
| words | 60.6 | 59.0 | 60.1 | 61.0 |

main / build (median): | Workload | PR | varR | varB |
| config | 1.04x | 1.00x | 0.99x |
| doclower | 4.83x | 3.51x | 3.50x |
| email | 1.04x | 1.02x | 1.02x |
| html | 1.01x | 0.98x | 0.98x |
| http | 1.10x | 1.07x | 1.06x |
| paths | 1.02x | 0.99x | 0.98x |
| pgotask | 1.03x | 1.01x | 1.00x |
| urls | 1.04x | 1.01x | 1.01x |
| words | 1.03x | 1.01x | 0.99x |
done 12:37:57
```

## Release: the block loop's address

The x64 Release build of `varB` (built here for the first time) measures 3.88x `main` at 64K against the PR's 5.71x, the same as `varR` (3.89x). The block loop is the same sequence of 16 instructions in `varB`, `varR` and `varS` (registers aside), but `varS` measured 6.47x. In the `varB` and `varR` DLLs the loop starts at the same address, 0x18015af90 (16 bytes into a 64-byte line); in `varS`'s at 0x18015aff0 (48 bytes in). So this build's result is most likely code placement (`varB`'s own loop can't be moved to test it: Windows builds are one layout each). On five runner jobs (EPYC 7763, 9V74, 9V45 and Xeon 8573C) the same code measured 1.06-1.08x the PR at 64K (`results/msvc_runners_varB.md`).
