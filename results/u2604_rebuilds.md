# gcc 15 PGO+LTO rebuilds on the Ubuntu 26.04 runner (EPYC 7763)

The same four trees (`main`, PR = `varJ`, `varR` = `varP`, `varT`), built from the same source four times: build 1 in run 41786095430 (before `control.py` existed), builds 2-4 in run 41798822983 (three jobs, `keep_binaries` on). Each build is relinked at 8 shifts and timed over all of them.

main / build, geometric mean over shifts. Short mix: `realworld/replay.py`. Control: string operations that never reach the case code (`realworld/control.py`).

| Build | short mix: PR | `varR` | `varT` | control: PR | `varR` | `varT` | 64K: PR | `varR` | `varT` |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.997x | 1.024x | 0.860x | — | — | — | 3.97x | 13.25x | 13.47x |
| 2 | 0.973x | 0.970x | 0.977x | 0.993x | 0.923x | 0.987x | 3.97x | 13.24x | 13.48x |
| 3 | 1.099x | 1.042x | 1.034x | 1.172x | 1.129x | 1.154x | 3.97x | 13.25x | 13.48x |
| 4 | 0.838x | 1.010x | 0.979x | 0.988x | 0.975x | 1.002x | 3.97x | 13.24x | 13.47x |

In build 3, `main` itself was the slow one: every tree is 1.13-1.17x faster than it on the control operations. Long strings don't move: 64K is the same in all four builds.

The binaries differ between rebuilds of the same tree (builds 2 and 3, from the uploaded `binaries` artifacts):

| Tree | `.text` bytes, build 2 | build 3 | `_PyEval_EvalFrameDefault` bytes, build 2 | build 3 |
|---|---|---|---|---|
| `main` | 3,066,217 | 3,063,881 | 63,748 | 63,936 |
| `varR` | 3,061,673 | 3,062,889 | 63,465 | 63,398 |
| `varT` | 3,061,577 | 3,068,265 | 63,345 | 63,807 |
