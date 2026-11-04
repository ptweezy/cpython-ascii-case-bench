# Old compilers (`oldcc` workflow, run 41813777661)

The word and block helpers of each variant, copied verbatim from `Objects/bytes_methods.c` with the patch applied (`oldcc/make_test.py`), built with every gcc and clang that Ubuntu 16.04, 18.04 and 20.04 package, on x86-64 (`ubuntu-24.04` runner) and arm64 (`ubuntu-24.04-arm`), at -O0, -O1, -O2, -O3 and -Os (and -O2, -O3, -Os with -mavx2 on x86-64), `-std=c11 -Wall`. Each build checks every byte value at every position of every length from 8 to 100 bytes, both cases, at two source/destination offsets (346,327,040 bytes), against a per-byte reference.

- x86-64: gcc 4.7.4, 4.8.5, 4.9.3, 5.4/5.5, 6.5, 7.5, 8.4, 9.4, 10.5; clang 3.5 to 12. 1,184 builds, all correct, no warnings.
- arm64: the same versions. 720 of 740 builds correct, no warnings; clang 3.5.2 crashes (stack dump at end of file) on every file, the PR's included, so it can't build these files at all.
- SIMD instructions in `ascii_case_words` at -Os (a stand-in for code that PGO finds cold): the PR has none with any compiler. `varT` and `varN` keep their vector code with every compiler (22-62). `varR`'s block is vectorized only by clang 5-9 (34-52); gcc 4.7-10 and clang 3.5-4 and 10-12 leave it scalar (0-9, at most its 16-byte loads and stores).

## Ubuntu 16.04.7 LTS, x86_64

Ubuntu 16.04.7 LTS, x86_64, compilers: gcc-4.7 gcc-4.8 gcc-4.9 gcc-5 clang-3.5 clang-3.6 clang-3.7 clang-3.8 clang-3.9 clang-4.0 clang-5.0 clang-6.0 clang-8
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 23 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 80 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 65 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 80 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 65 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 34 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 56 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 34 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 72 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 9 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 9 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 72 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu2) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 72 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 4 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 56 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 4 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 63 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 72 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu 4.9.3-13ubuntu2) 4.9.3 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 4 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 17 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 4 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 13 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 39 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 39 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 39 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 61 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 61 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 39 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 61 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 61 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 59 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 59 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 34 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 132 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 132 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 146 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 146 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 34 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 112 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 112 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 132 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 132 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 142 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 142 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 101 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 101 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 100 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 100 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |

## Ubuntu 18.04.6 LTS, x86_64

Ubuntu 18.04.6 LTS, x86_64, compilers: gcc-4.8 gcc-5 gcc-6 gcc-7 gcc-8 clang-3.9 clang-4.0 clang-5.0 clang-6.0 clang-7 clang-8 clang-9 clang-10
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 72 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 9 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 9 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 72 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu 4.8.5-4ubuntu8) 4.8.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 4 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 17 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 4 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 13 | 0 |
| test-varR.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-5 (Ubuntu 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 19 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varJ.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varN.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varR.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varR.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varT.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-6 (Ubuntu 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 17 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 13 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 17 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 13 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 69 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 61 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 61 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 57 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 59 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 59 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 34 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 116 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 132 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 132 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 146 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 146 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 38 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 99 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 34 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 112 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 112 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 37 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 105 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 132 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 132 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 142 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 142 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 94 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 101 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 101 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 100 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 100 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 41 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |

## Ubuntu 20.04.6 LTS, x86_64

)
)
Ubuntu 20.04.6 LTS, x86_64, compilers: gcc-7 gcc-8 gcc-9 gcc-10 clang-6.0 clang-7 clang-8 clang-9 clang-10 clang-11 clang-12
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 17 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 13 | 0 |
| test-varR.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varT.c | gcc-7 (Ubuntu 7.5.0-6ubuntu2) 7.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varJ.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 54 | 0 |
| test-varN.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 17 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 13 | 0 |
| test-varR.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varT.c | gcc-8 (Ubuntu 8.4.0-3ubuntu2) 8.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 56 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 17 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 15 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 78 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 25 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 83 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 56 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 16 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 52 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 97 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 78 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 100 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 100 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varN.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 9.0.1-12  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 9.0.1-12  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 9.0.1-12  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 41 | 0 |
| test-varR.c | clang version 9.0.1-12  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 9.0.1-12  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 9.0.1-12  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 40 | 0 |
| test-varT.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varT.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 9.0.1-12  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 9.0.1-12  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 9.0.1-12  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 51 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 51 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 33 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 89 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 85 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 85 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 29 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 96 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 51 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 51 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 98 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 74 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 31 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 85 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 85 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 29 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 -mavx2 | 346327040 bytes checked, 0 wrong: ok | 92 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os -mavx2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |

## Ubuntu 16.04.7 LTS, aarch64

Ubuntu 16.04.7 LTS, aarch64, compilers: gcc-4.7 gcc-4.8 gcc-4.9 gcc-5 clang-3.5 clang-3.6 clang-3.7 clang-3.8 clang-3.9 clang-4.0 clang-5.0 clang-6.0 clang-8
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 12 | 0 |
| test-varJ.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 236 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varN.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O0 | 346327040 bytes checked, 0 wrong: ok | 236 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O1 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -O3 | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varT.c | gcc-4.7 (Ubuntu/Linaro 4.7.4-3ubuntu12) 4.7.4 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 12 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 170 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 170 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu2) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varJ.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varR.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -O3 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-4.9 (Ubuntu/Linaro 4.9.3-13ubuntu2) 4.9.3 | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 50 | 0 |
| test-varN.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varR.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O0 | 346327040 bytes checked, 0 wrong: ok | 50 | 0 |
| test-varT.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -O3 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-5 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffebdb20e1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -mrelax-all -disable-free -disable-llvm-verifier -main-file-name test-varJ.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O0 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varJ-4e1cf5.o -x c test-varJ.c 
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
    clang: note: diagnostic msg: /tmp/test-varJ-788727.c
    clang: note: diagnostic msg: /tmp/test-varJ-788727.sh
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff628ce001c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varJ.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O1 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varJ-cc833a.o -x c test-varJ.c 
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
    clang: note: diagnostic msg: /tmp/test-varJ-9000c1.c
    clang: note: diagnostic msg: /tmp/test-varJ-9000c1.sh
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff6b5f8b01c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varJ.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O2 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varJ-af0a34.o -x c test-varJ.c 
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
    clang: note: diagnostic msg: /tmp/test-varJ-b2f69f.c
    clang: note: diagnostic msg: /tmp/test-varJ-b2f69f.sh
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffa6bba8a1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varJ.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O3 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varJ-1f101f.o -x c test-varJ.c 
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
    clang: note: diagnostic msg: /tmp/test-varJ-a16423.c
    clang: note: diagnostic msg: /tmp/test-varJ-a16423.sh
| test-varJ.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffc3ad6471c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varJ.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -Os -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varJ-00f232.o -x c test-varJ.c 
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
    clang: note: diagnostic msg: /tmp/test-varJ-26f83e.c
    clang: note: diagnostic msg: /tmp/test-varJ-26f83e.sh
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000fff7f74251c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -mrelax-all -disable-free -disable-llvm-verifier -main-file-name test-varN.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O0 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varN-7d942f.o -x c test-varN.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varN.c'.
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
    clang: note: diagnostic msg: /tmp/test-varN-797096.c
    clang: note: diagnostic msg: /tmp/test-varN-797096.sh
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffcb571a31c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varN.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O1 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varN-7c87b0.o -x c test-varN.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varN.c'.
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
    clang: note: diagnostic msg: /tmp/test-varN-247a13.c
    clang: note: diagnostic msg: /tmp/test-varN-247a13.sh
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000fff912d0b1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varN.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O2 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varN-f3a504.o -x c test-varN.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varN.c'.
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
    clang: note: diagnostic msg: /tmp/test-varN-ad95f8.c
    clang: note: diagnostic msg: /tmp/test-varN-ad95f8.sh
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff4bc87731c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varN.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O3 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varN-74c53d.o -x c test-varN.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varN.c'.
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
    clang: note: diagnostic msg: /tmp/test-varN-16ac2e.c
    clang: note: diagnostic msg: /tmp/test-varN-16ac2e.sh
| test-varN.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff2a0f0021c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varN.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -Os -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varN-fb0b27.o -x c test-varN.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varN.c'.
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
    clang: note: diagnostic msg: /tmp/test-varN-2b6326.c
    clang: note: diagnostic msg: /tmp/test-varN-2b6326.sh
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff5800f121c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -mrelax-all -disable-free -disable-llvm-verifier -main-file-name test-varR.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O0 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varR-693ca1.o -x c test-varR.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varR.c'.
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
    clang: note: diagnostic msg: /tmp/test-varR-9d3221.c
    clang: note: diagnostic msg: /tmp/test-varR-9d3221.sh
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff119c8301c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varR.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O1 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varR-3c42e1.o -x c test-varR.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varR.c'.
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
    clang: note: diagnostic msg: /tmp/test-varR-fcc06b.c
    clang: note: diagnostic msg: /tmp/test-varR-fcc06b.sh
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff55afede1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varR.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O2 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varR-40f854.o -x c test-varR.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varR.c'.
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
    clang: note: diagnostic msg: /tmp/test-varR-f544b3.c
    clang: note: diagnostic msg: /tmp/test-varR-f544b3.sh
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffd9796dd1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varR.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O3 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varR-60c561.o -x c test-varR.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varR.c'.
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
    clang: note: diagnostic msg: /tmp/test-varR-70a5b8.c
    clang: note: diagnostic msg: /tmp/test-varR-70a5b8.sh
| test-varR.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff96ee4171c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varR.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -Os -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varR-613cde.o -x c test-varR.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varR.c'.
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
    clang: note: diagnostic msg: /tmp/test-varR-801468.c
    clang: note: diagnostic msg: /tmp/test-varR-801468.sh
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O0 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff2c8ac971c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -mrelax-all -disable-free -disable-llvm-verifier -main-file-name test-varT.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O0 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varT-9da77b.o -x c test-varT.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varT.c'.
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
    clang: note: diagnostic msg: /tmp/test-varT-7ddcf1.c
    clang: note: diagnostic msg: /tmp/test-varT-7ddcf1.sh
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O1 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffb8b9e9b1c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varT.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O1 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -o /tmp/test-varT-e34385.o -x c test-varT.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varT.c'.
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
    clang: note: diagnostic msg: /tmp/test-varT-26f2bd.c
    clang: note: diagnostic msg: /tmp/test-varT-26f2bd.sh
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O2 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff8285fd01c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varT.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O2 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varT-16efbc.o -x c test-varT.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varT.c'.
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
    clang: note: diagnostic msg: /tmp/test-varT-b158bc.c
    clang: note: diagnostic msg: /tmp/test-varT-b158bc.sh
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -O3 | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ffcc5e3981c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varT.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O3 -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varT-ac6b07.o -x c test-varT.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varT.c'.
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
    clang: note: diagnostic msg: /tmp/test-varT-2b4eb1.c
    clang: note: diagnostic msg: /tmp/test-varT-2b4eb1.sh
| test-varT.c | Ubuntu clang version 3.5.2-3ubuntu1 (tags/RELEASE_352/final) (based on LLVM 3.5.2) | -Os | **build failed** | | |
    0  libLLVM-3.5.so.1 0x0000ff24b6e621c4 llvm::sys::PrintStackTrace(_IO_FILE*) + 68
    Stack dump:
    0.	Program arguments: /usr/lib/llvm-3.5/bin/clang -cc1 -triple aarch64-unknown-linux-gnu -emit-obj -disable-free -disable-llvm-verifier -main-file-name test-varT.c -mrelocation-model static -mdisable-fp-elim -fmath-errno -masm-verbose -mconstructor-aliases -fuse-init-array -target-cpu generic -target-feature +neon -target-abi aapcs -target-linker-version 2.26 -dwarf-column-info -resource-dir /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2 -internal-isystem /usr/include/clang/3.5.2/include/ -internal-isystem /usr/local/include -internal-isystem /usr/lib/llvm-3.5/bin/../lib/clang/3.5.2/include -internal-externc-isystem /usr/bin/../lib/gcc/aarch64-linux-gnu/5.4.0/include -internal-externc-isystem /usr/include/aarch64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -Os -Wall -std=c11 -fdebug-compilation-dir /w -ferror-limit 19 -fmessage-length 0 -mstackrealign -fno-signed-char -fobjc-runtime=gcc -fdiagnostics-show-option -vectorize-loops -vectorize-slp -o /tmp/test-varT-8142d5.o -x c test-varT.c 
    1.	<eof> parser at end of file
    2.	Code generation
    3.	Running pass 'Function Pass Manager' on module 'test-varT.c'.
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
    clang: note: diagnostic msg: /tmp/test-varT-525f9c.c
    clang: note: diagnostic msg: /tmp/test-varT-525f9c.sh
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | Ubuntu clang version 3.6.2-3ubuntu2 (tags/RELEASE_362/final) (based on LLVM 3.6.2) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | Ubuntu clang version 3.7.1-2ubuntu2 (tags/RELEASE_371/final) (based on LLVM 3.7.1) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varR.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varR.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 3.9.1-4ubuntu3~16.04.2 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varN.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 71 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 71 | 0 |
| test-varR.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O0 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -O3 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varT.c | clang version 4.0.0-1ubuntu1~16.04.2 (tags/RELEASE_400/rc1) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varN.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 71 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 71 | 0 |
| test-varR.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varT.c | clang version 5.0.0-3~16.04.1 (tags/RELEASE_500/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu16.04.1 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |

## Ubuntu 18.04.6 LTS, aarch64

Ubuntu 18.04.6 LTS, aarch64, compilers: gcc-4.8 gcc-5 gcc-6 gcc-7 gcc-8 clang-3.9 clang-4.0 clang-5.0 clang-6.0 clang-7 clang-8 clang-9 clang-10
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 12 | 0 |
| test-varJ.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 170 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varN.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varR.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 170 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varT.c | gcc-4.8 (Ubuntu/Linaro 4.8.5-4ubuntu8) 4.8.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varJ.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 50 | 0 |
| test-varN.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varR.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O0 | 346327040 bytes checked, 0 wrong: ok | 50 | 0 |
| test-varT.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -O3 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-5 (Ubuntu/Linaro 5.5.0-12ubuntu1) 5.5.0 20171010 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varJ.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 50 | 0 |
| test-varN.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varR.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O0 | 346327040 bytes checked, 0 wrong: ok | 50 | 0 |
| test-varT.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -O3 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-6 (Ubuntu/Linaro 6.5.0-2ubuntu1~18.04) 6.5.0 20181026 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varN.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varN.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 15 | 0 |
| test-varR.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varT.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varT.c | gcc-7 (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varN.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varN.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 15 | 0 |
| test-varR.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varT.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varT.c | gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varR.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O0 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O2 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -O3 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varN.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 71 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 71 | 0 |
| test-varR.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 62 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 30 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 55 | 0 |
| test-varT.c | clang version 4.0.1-10 (tags/RELEASE_401/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 27 | 0 |
| test-varJ.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varN.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 71 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 71 | 0 |
| test-varR.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 42 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 60 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 53 | 0 |
| test-varT.c | clang version 5.0.1-4 (tags/RELEASE_501/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 6.0.0-1ubuntu2 (tags/RELEASE_600/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 7.0.0-3~ubuntu0.18.04.1 (tags/RELEASE_700/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 8.0.0-3~ubuntu18.04.2 (tags/RELEASE_800/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 34 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1~18.04.2  | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |

## Ubuntu 20.04.6 LTS, aarch64

)
)
)
)
Ubuntu 20.04.6 LTS, aarch64, compilers: gcc-7 gcc-8 gcc-9 gcc-10 clang-6.0 clang-7 clang-8 clang-9 clang-10 clang-11 clang-12
| test | compiler | flags | result | SIMD insns in ascii_case_words | warnings |
|---|---|---|---|---|---|
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varN.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varN.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 15 | 0 |
| test-varR.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varT.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varT.c | gcc-7 (Ubuntu/Linaro 7.5.0-6ubuntu2) 7.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varN.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varN.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 15 | 0 |
| test-varR.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varT.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varT.c | gcc-8 (Ubuntu/Linaro 8.4.0-3ubuntu2) 8.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varN.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 15 | 0 |
| test-varR.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varT.c | gcc-9 (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 64 | 0 |
| test-varJ.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varN.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 14 | 0 |
| test-varR.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O0 | 346327040 bytes checked, 0 wrong: ok | 46 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O2 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -O3 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varT.c | gcc-10 (Ubuntu 10.5.0-1ubuntu1~20.04) 10.5.0 | -Os | 346327040 bytes checked, 0 wrong: ok | 24 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 6.0.1-14 (tags/RELEASE_601/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 7.0.1-12 (tags/RELEASE_701/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 36 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O1 | 346327040 bytes checked, 0 wrong: ok | 28 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 8.0.1-9 (tags/RELEASE_801/final) | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varR.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 34 | 0 |
| test-varT.c | clang version 9.0.1-12  | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 9.0.1-12  | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | clang version 9.0.1-12  | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 9.0.1-12  | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 9.0.1-12  | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | clang version 10.0.0-4ubuntu1  | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O0 | 346327040 bytes checked, 0 wrong: ok | 66 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | Ubuntu clang version 11.0.0-2~ubuntu20.04.1 | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 22 | 0 |
| test-varJ.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varN.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 58 | 0 |
| test-varR.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 8 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O0 | 346327040 bytes checked, 0 wrong: ok | 76 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O1 | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O2 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -O3 | 346327040 bytes checked, 0 wrong: ok | 48 | 0 |
| test-varT.c | Ubuntu clang version 12.0.0-3ubuntu1~20.04.5 | -Os | 346327040 bytes checked, 0 wrong: ok | 26 | 0 |
