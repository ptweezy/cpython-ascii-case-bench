# Old compilers: varB and varO (`oldcc` workflow, run 41825995796)

As [`oldcc.md`](oldcc.md), for the PR (`varJ`), `varB` and `varO`. Each build checks every byte value at every position of every length from 8 to 100 bytes, both cases, at two offsets.

| Target | Test | Builds | Correct | With warnings |
|---|---|---|---|---|
| arm64 | varB | 185 | 178 | 0 |
| arm64 | varJ | 185 | 180 | 0 |
| arm64 | varO | 185 | 178 | 0 |
| x86-64 | varB | 296 | 296 | 0 |
| x86-64 | varJ | 296 | 296 | 0 |
| x86-64 | varO | 296 | 296 | 0 |

SIMD instructions in `ascii_case_words` at `-Os` (a stand-in for code that PGO finds cold), over every compiler that built it: `varB` 40-48 on arm64, 29-62 on x86-64, 24-57 with `-mavx2`; the PR 0 with every compiler.

Builds that failed (no build gave a wrong result):

- arm64, varB: Ubuntu clang version 3.5.2-3ubuntu1 -O0
- arm64, varB: Ubuntu clang version 3.5.2-3ubuntu1 -O1
- arm64, varB: Ubuntu clang version 3.5.2-3ubuntu1 -O2
- arm64, varB: Ubuntu clang version 3.5.2-3ubuntu1 -O3
- arm64, varB: Ubuntu clang version 3.5.2-3ubuntu1 -Os
- arm64, varB: gcc-4.8 -Os
- arm64, varJ: Ubuntu clang version 3.5.2-3ubuntu1 -O0
- arm64, varJ: Ubuntu clang version 3.5.2-3ubuntu1 -O1
- arm64, varJ: Ubuntu clang version 3.5.2-3ubuntu1 -O2
- arm64, varJ: Ubuntu clang version 3.5.2-3ubuntu1 -O3
- arm64, varJ: Ubuntu clang version 3.5.2-3ubuntu1 -Os
- arm64, varO: Ubuntu clang version 3.5.2-3ubuntu1 -O0
- arm64, varO: Ubuntu clang version 3.5.2-3ubuntu1 -O1
- arm64, varO: Ubuntu clang version 3.5.2-3ubuntu1 -O2
- arm64, varO: Ubuntu clang version 3.5.2-3ubuntu1 -O3
- arm64, varO: Ubuntu clang version 3.5.2-3ubuntu1 -Os
- arm64, varO: gcc-4.8 -Os

clang 3.5 on arm64 crashes on every file, the PR's included. gcc 4.8.5 on arm64 at `-Os` stops with an internal compiler error (`in process_insert_insn, at gcse.c:2108`) on the 32-byte vector block of `varB` and `varO`; with `varN`'s 16-byte vector on arm64 the same compiler builds and passes ([`oldcc.md`](oldcc.md)). gcc 4.8 has no `<stdatomic.h>`, which CPython's default build needs (for mimalloc).

## Ubuntu 16.04.7 LTS, x86_64

Ubuntu 16.04.7 LTS, x86_64, compilers: gcc-4.7 gcc-4.8 gcc-4.9 gcc-5 clang-3.5 clang-3.6 clang-3.7 clang-3.8 clang-3.9 clang-4.0 clang-5.0 clang-6.0 clang-8
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 80 | 0 |
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 65 | 0 |
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 23 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 158 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 121 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 137 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 160 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 121 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 72 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 158 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 139 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 137 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 166 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 103 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 72 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 158 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 142 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 137 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 168 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 106 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 158 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 107 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 140 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 104 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 39 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 68 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 39 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 68 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 122 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 122 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 67 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 120 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 120 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 120 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 34 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 59 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 59 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 67 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 157 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 157 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 63 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 148 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 148 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |

## Ubuntu 18.04.6 LTS, x86_64

Ubuntu 18.04.6 LTS, x86_64, compilers: gcc-4.8 gcc-5 gcc-6 gcc-7 gcc-8 clang-3.9 clang-4.0 clang-5.0 clang-6.0 clang-7 clang-8 clang-9 clang-10
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 72 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 158 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 139 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 137 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 166 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 103 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 158 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 107 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 140 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 104 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varO.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varB.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varB.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varO.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 63 | 0 |
| test-varO.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 93 | 0 |
| test-varO.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 56 | 0 |
| test-varO.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varO.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varO.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 65 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 142 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 67 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 142 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 67 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 67 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 120 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 120 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 120 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 34 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 59 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 59 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 67 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 157 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 157 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 63 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 148 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 148 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |

## Ubuntu 20.04.6 LTS, x86_64

)
)
Ubuntu 20.04.6 LTS, x86_64, compilers: gcc-7 gcc-8 gcc-9 gcc-10 clang-6.0 clang-7 clang-8 clang-9 clang-10 clang-11 clang-12
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varB.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 65 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 142 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 67 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varO.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varB.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 142 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 67 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varO.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 56 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 142 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 67 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 56 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 56 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 130 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 71 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varB.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 9.0.1-12  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 9.0.1-12  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 9.0.1-12  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varO.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 9.0.1-12  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 9.0.1-12  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 9.0.1-12  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 143 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 85 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 85 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 29 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 138 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 56 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 135 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 135 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |

## Ubuntu 16.04.7 LTS, aarch64

Ubuntu 16.04.7 LTS, aarch64, compilers: gcc-4.7 gcc-4.8 gcc-4.9 gcc-5 clang-3.5 clang-3.6 clang-3.7 clang-3.8 clang-3.9 clang-4.0 clang-5.0 clang-6.0 clang-8
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 588 | 0 |
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varB.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 12 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 588 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varO.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 492 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -Os | **build failed** | | |
    test-varB.c: In function 'ascii_case_words':
    test-varB.c:129:1: internal compiler error: in process_insert_insn, at gcse.c:2108
     }
     ^
    Please submit a full bug report,
    with preprocessed source if appropriate.
    See <file:///usr/share/doc/gcc-4.8/README.Bugs> for instructions.
    Preprocessed source stored into /tmp/cc8TRqJu.out file, please attach this to your bugreport.
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 12 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 492 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -Os | **build failed** | | |
    test-varO.c: In function 'ascii_case_words':
    test-varO.c:108:1: internal compiler error: in process_insert_insn, at gcse.c:2108
     }
     ^
    Please submit a full bug report,
    with preprocessed source if appropriate.
    See <file:///usr/share/doc/gcc-4.8/README.Bugs> for instructions.
    Preprocessed source stored into /tmp/ccE33p3c.out file, please attach this to your bugreport.
| test-varB.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 216 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 47 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 49 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varB.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 216 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 47 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 49 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 216 | 0 |
| test-varB.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varB.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 216 | 0 |
| test-varO.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varO.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffbf508c71c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -mrelax-all -disable-free -disable-llvm-verifier -main-file-name test-varB.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O0 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varB-95afd6.o -x c test-varB.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varB.c'.
    4.	Running pass 'Fast Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varB-f0b453.c
    clang: note: diagnostic msg: /tmp/test-varB-f0b453.sh
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff30187731c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varB.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O1 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varB-96a107.o -x c test-varB.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varB.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varB-db3fc5.c
    clang: note: diagnostic msg: /tmp/test-varB-db3fc5.sh
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffd61e7e71c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varB.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O2 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varB-1798f3.o -x c test-varB.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varB.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varB-5fe1b3.c
    clang: note: diagnostic msg: /tmp/test-varB-5fe1b3.sh
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffc39310d1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varB.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O3 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varB-94cdeb.o -x c test-varB.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varB.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varB-e767a8.c
    clang: note: diagnostic msg: /tmp/test-varB-e767a8.sh
| test-varB.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffcf653f91c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varB.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -Os -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varB-570bda.o -x c test-varB.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varB.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varB-027a56.c
    clang: note: diagnostic msg: /tmp/test-varB-027a56.sh
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff71d18c71c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -mrelax-all -disable-free -disable-llvm-verifier -main-file-name test-varJ.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O0 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varJ-fb6f38.o -x c test-varJ.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varJ.c'.
    4.	Running pass 'Fast Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varJ-eb9a25.c
    clang: note: diagnostic msg: /tmp/test-varJ-eb9a25.sh
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff24bcf2d1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varJ.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O1 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varJ-38804c.o -x c test-varJ.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varJ.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varJ-0a5adb.c
    clang: note: diagnostic msg: /tmp/test-varJ-0a5adb.sh
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffa68a8531c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varJ.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O2 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varJ-68f417.o -x c test-varJ.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varJ.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varJ-5693d4.c
    clang: note: diagnostic msg: /tmp/test-varJ-5693d4.sh
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff3b412fa1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varJ.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O3 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varJ-99f9ec.o -x c test-varJ.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varJ.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varJ-c6b529.c
    clang: note: diagnostic msg: /tmp/test-varJ-c6b529.sh
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff6ff55ce1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varJ.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -Os -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varJ-860405.o -x c test-varJ.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varJ.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varJ-b55b57.c
    clang: note: diagnostic msg: /tmp/test-varJ-b55b57.sh
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff118728a1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -mrelax-all -disable-free -disable-llvm-verifier -main-file-name test-varO.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O0 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varO-f3ca81.o -x c test-varO.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varO.c'.
    4.	Running pass 'Fast Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varO-d9d5c1.c
    clang: note: diagnostic msg: /tmp/test-varO-d9d5c1.sh
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff4c0ac6a1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varO.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O1 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varO-40a6d7.o -x c test-varO.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varO.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varO-8f6ef5.c
    clang: note: diagnostic msg: /tmp/test-varO-8f6ef5.sh
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff1257cf91c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varO.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O2 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varO-36fedb.o -x c test-varO.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varO.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varO-391ccb.c
    clang: note: diagnostic msg: /tmp/test-varO-391ccb.sh
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff0cb08201c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varO.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O3 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varO-6126cb.o -x c test-varO.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varO.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varO-4d9699.c
    clang: note: diagnostic msg: /tmp/test-varO-4d9699.sh
| test-varO.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff317a42f1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varO.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -Os -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varO-84f11b.o -x c test-varO.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varO.c'.
    4.	Running pass 'Greedy Register Allocator' on function '@main'
    clang: error: unable to execute command: Segmentation fault (core dumped)
    clang: error: clang frontend command failed due to signal (use -v to see invocation)
    Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2)
    Target: aarch64-unknown-linux-gnu
    Thread model: posix
    clang: note: diagnostic msg: PLEASE submit a bug report to http://bugs.debian.org/ and include the crash backtrace, preprocessed source, and associated run script.
    clang: note: diagnostic msg: 
    ********************
    
    PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
    Preprocessed source(s) and associated run script(s) are located at:
    clang: note: diagnostic msg: /tmp/test-varO-3aa864.c
    clang: note: diagnostic msg: /tmp/test-varO-3aa864.sh
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 90 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 90 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 90 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 90 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 90 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 90 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 90 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 90 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 118 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varB.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 118 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 114 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varB.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 114 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varO.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |

## Ubuntu 18.04.6 LTS, aarch64

Ubuntu 18.04.6 LTS, aarch64, compilers: gcc-4.8 gcc-5 gcc-6 gcc-7 gcc-8 clang-3.9 clang-4.0 clang-5.0 clang-6.0 clang-7 clang-8 clang-9 clang-10
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varB.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 492 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varB.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -Os | **build failed** | | |
    test-varB.c: In function 'ascii_case_words':
    test-varB.c:129:1: internal compiler error: in process_insert_insn, at gcse.c:2108
     }
     ^
    Please submit a full bug report,
    with preprocessed source if appropriate.
    See <file:///usr/share/doc/gcc-4.8/README.Bugs> for instructions.
    Preprocessed source stored into /tmp/cc6WYhPr.out file, please attach this to your bugreport.
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 12 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 492 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varO.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -Os | **build failed** | | |
    test-varO.c: In function 'ascii_case_words':
    test-varO.c:108:1: internal compiler error: in process_insert_insn, at gcse.c:2108
     }
     ^
    Please submit a full bug report,
    with preprocessed source if appropriate.
    See <file:///usr/share/doc/gcc-4.8/README.Bugs> for instructions.
    Preprocessed source stored into /tmp/ccIqSpUD.out file, please attach this to your bugreport.
| test-varB.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 216 | 0 |
| test-varB.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varB.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 216 | 0 |
| test-varO.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varO.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varB.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 160 | 0 |
| test-varB.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varB.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varJ.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 160 | 0 |
| test-varO.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varO.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varB.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varB.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varO.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varO.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varB.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varB.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 80 | 0 |
| test-varB.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varO.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 80 | 0 |
| test-varO.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 90 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 90 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varO.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 118 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varB.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 118 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 73 | 0 |
| test-varO.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 114 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varB.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 114 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varO.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |

## Ubuntu 20.04.6 LTS, aarch64

)
)
)
)
Ubuntu 20.04.6 LTS, aarch64, compilers: gcc-7 gcc-8 gcc-9 gcc-10 clang-6.0 clang-7 clang-8 clang-9 clang-10 clang-11 clang-12
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varB.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varB.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varB.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varO.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varO.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varB.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varB.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 80 | 0 |
| test-varB.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varO.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 80 | 0 |
| test-varO.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 80 | 0 |
| test-varB.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 80 | 0 |
| test-varO.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 80 | 0 |
| test-varB.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 152 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 80 | 0 |
| test-varO.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 44 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 126 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 108 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varB.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 108 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varO.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
