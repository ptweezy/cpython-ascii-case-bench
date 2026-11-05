# Which loop to offer for gh-161155

> **Update, 2026-11-05:** the recommendation is now `cmpD` (57 lines in `bytes_methods.c`, plain C, one `#if`) plus the two proposed tests, not `varB`. `cmpD` keeps most of `varB`'s gains in the shipped PGO builds at about the PR's size, without GNU vectors. See [`results/compact.md`](results/compact.md). The rest of this document is the data behind `varB`, which stays available as a follow-up.

This compares the PR's word loop ([python/cpython#161201](https://github.com/python/cpython/pull/161201); its `bytes_methods.c` as of 9433a66, which later commits only merge `main` into) with the variants in `variants/`, in the builds that ship CPython to users. Speedups are time on `main` / time with the variant, so above 1.00x is faster than `main`. "64K" is 65,536 characters.

Names used below:
- **PR**: the PR's code, measured as the PR itself or as `varJ` (the same code with two lines of longer comments).
- **count-by-one loop**: the PR's MSVC-only word loop, which counts words by one so that MSVC vectorizes it at `/O2`.
- **`varB`** (recommended): a block of 16 or 32 bytes on x86-64 and arm64 (gcc, clang and MSVC, not clang-cl), the PR's code elsewhere (see the summary). **`varB5`**: `varB` plus a 64-byte block under `__AVX512F__`.
- **`varR`**: one plain-C 16-byte block (an array of words) for every compiler, without the count-by-one loop. **`varP`**: the same block outside MSVC, with the PR's MSVC branch; on gcc and clang it compiles to `varR`'s code.
- **`varT`**: the block as a 16-byte GNU vector on gcc and clang for x86-64 and arm64. **`varN`**: `varT` with 32 bytes under `__AVX2__`. **`varO`**: 32 bytes for every gcc and clang build on x86-64 and arm64.
- **`varS`**, **`varU`**, **`varQ`**: `varR`, `varT` and `varP` plus overlapping 4- and 2-byte words for strings shorter than 8 bytes.

## Summary

- **Most major binary builds don't vectorize the PR's loop.**
  - A plain `./configure && make` (gcc `-O3`) turns it into SSE2 or NEON code: 4.15-7.60x faster than `main` at 64K on the runners.
  - Most major binary builds use PGO instead: python.org's 64-bit Windows and macOS installers, Debian, Ubuntu, Fedora, RHEL, Arch, Alpine's package, the Debian-based Docker `python` images and uv's x86-64 and arm64 glibc Pythons. PGO's training rarely reaches this loop, so gcc and clang optimize it for size and leave it scalar; MSVC's x64 PGO build leaves it scalar even when the training reaches it (ARM64 not counted). Without the proposed tests, `ascii_case_words` has no SIMD instructions in any PGO build whose code was counted (gcc 13-16; clang 18 and 21; Apple clang 17; MSVC x64 and x86). In the 64-bit PGO builds measured, the PR is 1.8-4.0x faster than `main` at 64K.
  - Apple clang leaves it scalar also without PGO: the macOS SDK enables `_FORTIFY_SOURCE`, which makes `memcpy` a checked call (0 SIMD instructions in the release builds on both Macs).
  - Builds without PGO include python.org's 32-bit Windows installer, FreeBSD's packages, nixpkgs, Docker's `-alpine` images and uv's musl Pythons.
- **The recommendation, `varB`,** converts strings of at least one block in blocks of 16 or 32 bytes, the last block overlapping the one before, and keeps the PR's code everywhere else:
  - gcc and clang on 64-bit x86 and arm64: a GNU vector of words, 32 bytes on arm64 (two NEON registers) and with AVX2, 16 bytes (SSE2) on x86-64 without AVX2. A vector type stays SIMD where the compiler optimizes for size, as in PGO builds and at `-Os`.
  - MSVC on x64 and ARM64: a 16-byte array of two words, which MSVC vectorizes also in x64 PGO builds (32 SIMD instructions, against the PR's 0). On ARM64 the instructions weren't counted; the block runs at 1.28-1.32x the PR at 64K in PGO and Release builds.
  - Everything else (32-bit targets, clang-cl, ppc64le, s390x, riscv64, wasm32), and strings shorter than one block: the PR's word loop, unchanged, including its MSVC branch. On 32-bit x86, riscv64, ppc64le and s390x, `varB` compiles to the PR's machine code ([`results/varB_equiv.md`](results/varB_equiv.md)).

  It adds 112 non-blank lines to `bytes_methods.c`, against the PR's 56.
- **Long strings:**
  - In every 64-bit PGO build whose code was counted (all but MSVC on ARM64), `varB`'s code is vectorized where the PR's isn't. At 64K it is 1.3-1.4x faster than the PR on Neoverse N2 (Linux and Windows), 2.1x on Apple M1, and 1.6-5.4x on x86-64 (5.4x in RHEL 10's configuration, gcc 14 `-O3` with AVX2; 2.6-5.0x in uv's x86-64-v4 build).
  - Without PGO the PR's loop is usually vectorized too, and the two are about equal. Where it isn't, the block is faster: 1.7-2.1x the PR on macOS (`_FORTIFY_SOURCE`), 1.2-2.7x at gcc `-O2` (measured with `varP`'s block). With MSVC on ARM64 (instructions not counted) it is 1.31x the PR.
  - From 256 characters up (256, 1,024, 4,096 and 64K), `varB`'s code is at least 0.988x the PR in 49 of the 52 runner layout jobs that measured it, and at least 0.989x in all 18 MSVC runner jobs (256, 1,024 and 64K), PGO or not. The other three are gcc `-O3 -march=x86-64-v4` (AVX-512) without PGO, where gcc widens the PR's loop to 64-byte registers: 0.91x the PR at 1,024 on a Xeon 6975P, and 0.92x and 0.94x at 4,096 on two EPYC 9V45 jobs (1.00-1.24x at 64K). Locally, without PGO, clang 18 with AVX-512 gives 0.95x at 64K, and gcc 13 with AVX-512 and clang 22 `-O3` (i5-12400T) give 0.97x at 4,096. One local result is lower: MSVC x64 Release on the Ryzen 7 9800X3D, 0.94x at 256 down to 0.68x at 64K. That is most likely code placement: in `varS` the same 16-instruction loop, 48 rather than 16 bytes into a cache line, measured 1.13x the PR on that machine (see the notes below the table).
  - In PGO builds `varB` pulls ahead from about 64 characters: 2-20% faster than the PR at 64 and 5-29% at 128 in `varB`'s own PGO layout jobs ([`results/runner_jobs.md`](results/runner_jobs.md)), and 1-17% at 64 in the 12 MSVC PGO runner jobs.
  - On 32-bit Windows (python.org's 32-bit installer) it compiles to the PR's code and runs at the PR's speed.
- **AVX-512** (`-march=x86-64-v4`): uv ships opt-in x86-64-v4 Pythons, built with PGO and LTO by python-build-standalone's own clang 23; measured here with Ubuntu 26.04's clang 21. There the PR's loop is scalar, and `varB`'s 32-byte block is 2.6-5.0x the PR at 64K (EPYC 9V74, Xeon 6975P, Xeon Platinum 8370C). Without PGO, gcc widens the PR's loop to 64-byte registers, and `varB` is 0.91-1.07x the PR at 1,024, 0.92-1.18x at 4,096 and 1.00-1.24x at 64K on the runners. `varB5`, which adds a 64-byte block under `__AVX512F__` (5 more lines), helps without PGO on AMD Zen 5 (1.3x `varB` at 64K with gcc on the EPYC 9V45 and the Ryzen 7 9800X3D; 0.97x on the Zen 4 EPYC 9V74), but in uv's configuration it is 0.78x `varB` at 64K on the Xeon 6975P and 0.39x on the Xeon 8370C, so it is not offered.
- **Why not the simpler variants** (each was a step toward `varB`; see "How `varB` got here"):
  - **`varR`** (one plain-C block for every compiler, 11 lines over the PR) stays scalar in gcc 16 PGO builds on x86-64 (gcc 16 PGO+LTO, the compiler of Fedora 44's and Arch's `python3`: 2.6-2.7x `main` against `varB`'s 5.3-6.7x). Without PGO it is 20-22% slower than the PR at 64K under clang (FreeBSD's packages, self-built Linux Pythons) and 0.47-0.61x the PR with AVX2. On 32-bit Windows it is 17% slower than the PR in a Release build and 0.56x `main` in a PGO build.
  - **`varT`** (GNU vector, 16 bytes everywhere) fixes gcc 16 and clang, but with AVX2 it is 0.59-0.62x the PR without PGO and 0.55-0.63x `varB` with PGO, it is 7-8% slower than the PR under clang without PGO on Neoverse N2, and it shares `varR`'s 32-bit Windows problem.
  - **`varN`** (`varT` + 32-byte vectors with AVX2) still has the Neoverse N2 and 32-bit Windows problems.
  - **`varO`** (32-byte vectors for every gcc and clang build on x86-64 and arm64) is what `varB` uses on arm64, but on x86-64 without AVX2 gcc lowers the 32-byte vector badly: 0.41-0.53x `main` at 64K in gcc PGO builds, and 12-25% slower than `varN` from 32 to 64K characters at gcc `-O3`.
- **Short strings:** on the real-world short-string mix, pooled over the layout jobs, `varB`'s code is 0.994x the PR on x86-64 without AVX2 (33 layout runs, 4 of them local; 95% interval 0.979-1.010) and 1.000x on arm64 (11 jobs, 0.994-1.007): no measured difference. With AVX2 or AVX-512 it is 0.989x (12 jobs, 0.962-1.016); the lowest is 0.87x in the RHEL `-O2` job (0.83x for `varO`, the same code), where operations that never reach the case code differ by 4.5%, a third of the gap; not explained. Rebuilding the same source with gcc 15 PGO moves the short-string result by up to 31%, so single PGO builds say little about short strings. On MSVC x64 PGO, over four local rebuilds each, `varB` is 0.99x the PR, within the spread between rebuilds of one tree (3% by best times, 7% by median); part of it is likely vector setup that MSVC runs on every call. The runner jobs, one build each, give 0.97x (8 jobs, best times, 95% interval 0.94-1.00), and the local x64 Release build 0.97x.
- **The proposed tests change PGO.** CPython's PGO training runs `test_str` and `test_bytes`, so tests with long strings make the loop hot. With them, gcc 13 PGO+LTO vectorizes the PR's loop (2.32x → 3.98x `main` at 64K on the Ryzen 7 9800X3D), and `varB` gains too (4.90x → 6.72x). `varB` stays 1.69x the PR at 64K and 1.36x at 1,024. MSVC's PGO build (python.org's 64-bit Windows installer) leaves the PR's loop scalar with the tests too: 2.64x `main` at 64K with or without them, against `varB`'s 5.7x. Debian's and Ubuntu's own training runs the whole test suite, so it would run the tests too (not measured); builds without PGO get none of this.
- **How often long strings occur:** in the eight everyday workloads of the replay (words, HTTP headers, URLs, e-mail addresses, paths, HTML tags, config keys, CPython's PGO task), the median string has 2-12 characters, and strings of 64+ characters carry at most 4% of the characters. Long strings come from whole documents, logs or data files being case-converted.
- **Correctness:**
  - Every build of every variant on the runners passed `edge_cases.py` (253,814 cases) at every code layout and `check_all.py` (1,495,930 cases) once; so did the local builds.
  - The helpers alone pass an exhaustive check (every byte value at every position of every length from one word to 100 bytes, both cases, two offsets) with gcc and clang at `-O0` to `-O3` and `-Os`, with and without AVX2, and with MSVC for x64 and x86 at `/O2` and `/O1 /Oi` ([`results/local/msvc_helpers.md`](results/local/msvc_helpers.md)).
  - Old compilers: the helpers of the PR, `varR`, `varT`, `varN`, `varB` and `varO` build without warnings and pass that check with every gcc and clang that Ubuntu 16.04-20.04 package (gcc 4.7-10, clang 3.5-12), on x86-64 and arm64 ([`results/oldcc.md`](results/oldcc.md), [`results/oldcc_varB.md`](results/oldcc_varB.md)). Two exceptions, neither a wrong result: clang 3.5 on arm64 crashes on all of these files, the PR's included; gcc 4.8 on arm64 at `-Os` stops with an internal compiler error on the 32-byte vector of `varB` and `varO` (gcc 4.8 has no `<stdatomic.h>`, so CPython builds there only without mimalloc). At `-Os` (a stand-in for code that PGO finds cold), `varB` stays vectorized with every one of these compilers that builds it (29-62 SIMD instructions on x86-64, 40-48 on arm64), the PR's loop with none.
  - Review found one bug in a draft of `varT`: on x32 and arm64_32, which define `__x86_64__` or `__aarch64__` with a 4-byte `size_t`, the vector block skipped half the letters. The vector block is used only when `SIZEOF_SIZE_T == 8`.
- **Tests:** seven bugs were planted in `varB`'s code as gcc 13 builds it for x86-64 without AVX2 (16-byte vector block): three in the block, two in the word loop, two in the range constants both use. Two break CPython's own build. None of the existing tests of `str` and `bytes` (`test_bytes`, `test_str`, `test_userstring`, `test_string`) fails for any of the other five; the whole suite catches four of them only through other modules, and misses the fifth. [`tests/proposed_tests.py`](tests/proposed_tests.py) adds two tests (six test cases, 0.09 s) that catch all five ([`results/mutants.md`](results/mutants.md)). The 32-byte and MSVC blocks were not mutation-tested.
- **Portability and PEP 7:** PEP 7 asks for no compiler-specific extensions. `varB` uses one, the GNU vector type, behind `#if defined(__GNUC__) && (defined(__x86_64__) || defined(__aarch64__)) && SIZEOF_SIZE_T == 8`, with every constant splatted explicitly (no mixing of vectors and scalars, the construct that broke `bytes.hex()` on old clang in gh-148474). `Python/pystrhex.c` uses the same extension for `bytes.hex()`, behind a configure check (`_Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR`, gcc 12+ or clang), and stops at 16 bytes on purpose: its comment says AVX2 or AVX-512 "adds a ton of complication". `varB`'s 32-byte size with AVX2 departs from that, although it is a vector size in the same code rather than a second code path. It would be the first code in CPython that tests `__AVX2__`, and no CPython CI job compiles the core with AVX2 (see "Which CI jobs build each path").
- **Recommendation:** `varB`, with the two proposed tests. If maintainers don't want the GNU vector type, two plain-C fallbacks follow from the measurements: `varB` with only its MSVC block (the Windows gain, the PR's code everywhere else; measured costs: the MSVC x64 Release code-placement result above, and about 1-3% on short strings under MSVC x64), or `varB` with the array block also for 64-bit gcc and clang (adds the gains of gcc 13-15 and clang PGO builds, but gives up `varB`'s gain under gcc 16 PGO on x86-64, 2.6-2.7x instead of 5.3-6.7x `main`, and brings back `varR`'s losses to the PR under clang without PGO and with AVX2).

## Long strings, in the builds people run

Speedup over `main` at 64K. Unless marked otherwise, rows are `realworld/len_layout.py` (`str.lower()` on letters, the mean over 8 code layouts per job; see "How it was measured"). "SIMD" is the number of SSE/AVX/NEON instructions in `ascii_case_words` for PR / `varR` / `varT` / `varB` where it was counted ("—" where it wasn't).

The `varB` column is `varB`'s machine code: `varB` itself where a job measured it, otherwise the tree that compiles to the same code in that job ([`results/varB_equiv.md`](results/varB_equiv.md)): `varN` or `varT` on x86-64 without AVX2, `varN` or `varO` with AVX2, `varO` on arm64. "= `varT`" means `varT`'s cell is `varB`'s code, "= PR" that `varB` compiles to the PR's code (32-bit targets); "—" means the job measured none of these. On arm64 `varN` compiles to `varT`'s code, so some arm64 `varT` cells (the gcc `-O3` Neoverse N2 rows) are `varN` measurements. On gcc and clang `varP` compiles to `varR`'s code, and some jobs measured `varP`.

| Build | Closest shipped build | Machine, method | SIMD | PR | `varR` | `varT` | `varB` |
|---|---|---|---|---|---|---|---|
| **PGO builds** | | | | | | | |
| MSVC 19.51 PGO, x64 | python.org 64-bit Windows | Ryzen 7 9800X3D (Zen 5), 4 builds each of the PR and `varB`, 1 of `varR`, 1 layout each | 0 / 32 / = `varR` / 32 | 2.67x | 5.71x | = `varR` | 5.72x |
| | | EPYC 7763 (Zen 3), 4 jobs, pyperf `str.lower` | — | 2.26-3.97x | 5.28x | = `varR` | 4.99-8.85x |
| | | EPYC 9V74 (Zen 4), 3 jobs, pyperf `str.lower` | — | 2.08-2.14x | 5.34x | = `varR` | 4.86-5.34x |
| | | EPYC 9V45 (Zen 5), pyperf `str.lower` | — | 2.38x | — | — | 5.36x |
| | | Xeon Platinum 8573C, 2 jobs, pyperf `str.lower` | — | 2.99-3.18x | — | — | 5.06-5.08x |
| MSVC 19.51 PGO, ARM64 | python.org ARM64 Windows | Cobalt 100 (Neoverse N2), 6 jobs, pyperf `str.lower` | not counted | 2.97-3.03x | 3.83-3.88x | = `varR` | 3.84-3.93x |
| MSVC 19.51 PGO, x86 (32-bit) | uv's 32-bit Windows Pythons (python-build-standalone `i686-pc-windows-msvc`, built with VS 2022) | Ryzen 7 9800X3D, 1 layout | 0 / 0 / = `varR` / = PR | 1.02x | **0.56x** | = `varR` | = PR |
| Apple clang 17 PGO+LTO, fortify | python.org macOS (its 3.14 installers report Apple clang 16) | Apple M1, 5 jobs | 0 / — / vector / vector | 3.55-3.65x | 7.19-7.65x | 7.22-7.57x | 7.37x |
| | its x86-64 slice | Intel i7-8700B, 3 jobs | 0 / — / 41 / 41 | 2.64-2.71x | 5.39x | 4.85-4.99x | 5.05-5.29x |
| gcc 13 PGO+LTO | Ubuntu 24.04's compiler, CPython's training | Ryzen 7 9800X3D | 0 / 31 / 31 / 31 | 2.32x | 5.09x | 4.91x | 4.90x |
| | | EPYC 7763, 3 jobs | 0 / — / 31 / 31 | 2.51-2.53x | 7.41x | 7.41-7.42x | 7.36-7.42x |
| | | EPYC 9V74 | — | 2.46x | 7.09x | 7.10x | = `varT` |
| | | EPYC 9V45 (Zen 5) | — | 2.32x | 4.85x | — | — |
| | | Xeon Platinum 8573C | — | 2.77x | 6.23x | — | — |
| | | Neoverse N2, 5 jobs | 0 / — / 26 / 50 | 3.37-3.38x | 4.36x | 4.39x | 4.58-4.61x |
| gcc 13 PGO+LTO, Debian's training | Ubuntu 24.04's `python3` | EPYC 7763, 4 layouts | 0 / 31 / 31 / = `varT` | 2.46x | 6.47x | 6.34x | = `varT` |
| gcc 14 PGO+LTO | Debian 13's compiler | EPYC 7763 | 0 / 36 / 37 / = `varT` | 1.81x | 6.01x | 6.04x | = `varT` |
| gcc 14 PGO+LTO, `-O2` | Docker `python` images (Debian) | EPYC 9V45 | 0 / 36 / 37 / = `varT` | 2.39x | 5.11x | 5.15x | = `varT` |
| gcc 15 PGO+LTO | Ubuntu 26.04's compiler | EPYC 7763, 4 builds | 0 / 26 / 26 / = `varT` | 3.97x | 13.24-13.25x | 13.47-13.48x | = `varT` |
| | | Neoverse N2 | 0 / 26 / 26 / — | 3.34x | 4.24x | 4.26x | — |
| gcc 16 PGO+LTO | Fedora 44, Arch (both `-O3`) | EPYC 7763, `fedora:44` container, 2 jobs | 0 / **0** / 32 / 32 | 1.79-1.85x | **2.58x** | 6.47-6.67x | 6.47-6.67x |
| | | i5-12400T, Fedora's own build recipe, pyperf `bytes.lower`, 1 layout | 0 / **0** / 32 / = `varT` | 1.92x | **2.67x** | 5.32x | = `varT` |
| | | Neoverse N2, `fedora:44` container, 2 jobs | 0 / 26 / 26 / 46 | 3.36x | 4.27x | 4.29-4.30x | 4.45x |
| clang PGO+LTO | uv's Pythons (python-build-standalone) | EPYC 7763, clang 18 | 0 / 55 / 53 / = `varT` | 3.42x | 7.92x | 7.91x | = `varT` |
| | | Xeon 6975P, clang 18 | 0 / — / 53 / 53 | 2.96x | — | 5.17x | 5.18x |
| | | EPYC 9V74, clang 21 | 0 / 55 / 53 / = `varT` | 3.24x | 7.84x | 7.79x | = `varT` |
| | | Neoverse N2, clang 21, 2 jobs | 0 / 47 / 47 / 80 | 3.23-3.24x | 4.33x | 4.28-4.33x | 4.64x |
| clang 21 PGO+LTO, `-march=x86-64-v3` | uv's x86-64-v3 Pythons (opt-in) | EPYC 9V74 | 0 / 48 / 46 / 48 | 3.10x | 8.34x | 8.33x | **14.54x** |
| clang 21 PGO+LTO, `-march=x86-64-v4` | uv's x86-64-v4 Pythons (opt-in) | EPYC 9V74 | 0 / — / — / 36 | 3.11x | — | — | **15.59x** (`varB5` 15.09x) |
| | | Xeon 6975P | 0 / — / — / 36 | 3.23x | — | — | **8.56x** (`varB5` 6.66x) |
| | | Xeon Platinum 8370C (Ice Lake) | 0 / — / — / 36 | 3.36x | — | — | **15.62x** (`varB5` **6.15x**) |
| gcc 14 PGO+LTO, `-O3 -march=x86-64-v3` | RHEL 10's `python3` | EPYC 7763 | 0 / 28 / 28 / 32 | 2.30x | 7.05x | 7.80x | **12.31x** |
| | the same at `-O2` (none known) | EPYC 7763 | 0 / — / 28 / 32 | 3.03x | — | 7.04x | **12.83x** |
| **Builds without PGO** | | | | | | | |
| MSVC 19.51 Release, x86 (32-bit) | python.org 32-bit Windows | Ryzen 7 9800X3D, 1 layout | 46 / 43 / = `varR` / 46 | 4.42x | **3.67x** | = `varR` | 4.44x |
| MSVC 19.51 Release, x64 | conda-forge's Windows build of 3.15 (VS 2022) | Ryzen 7 9800X3D, 1 layout | 45 / 35 / = `varR` / 70 | 5.71x | **3.89x** | = `varR` | **3.88x** |
| | | EPYC 7763, 2 jobs, pyperf `str.lower` | — | 5.39-5.49x | 5.86x | = `varR` | 5.76x |
| | | EPYC 9V74, pyperf `str.lower` | — | 5.41x | — | — | 5.87x |
| | | EPYC 9V45, 2 jobs, pyperf `str.lower` | — | 5.61-5.68x | 6.17x | = `varR` | 6.03x |
| | | Xeon Platinum 8573C, 2 jobs, pyperf `str.lower` | — | 5.02-5.06x | — | — | 5.34-5.38x |
| MSVC 19.51 Release, ARM64 | conda-forge's Windows ARM64 build of 3.15 (VS 2022, cross-compiled) | Cobalt 100, 3 jobs, pyperf `str.lower` | not counted | 2.96-3.01x | 3.83-3.84x | = `varR` | 3.92x |
| clang 18 `-O2` + ThinLTO | FreeBSD's packages (built with clang 19 on 14.4 and 15.1; 14.5's base clang is 21) | Ryzen 7 9800X3D | 30 / 99 / 83 / 83 | 6.32x | **4.92x** | 6.29x | 6.30x |
| | | EPYC 7763 | 30 / 99 / 83 / 83 | 7.49x | **5.99x** | 7.45x | 7.45x |
| | | EPYC 9V45 | 30 / — / 83 / 83 | 6.26x | — | 6.25x | 6.26x |
| | | Neoverse N2, 2 jobs | 22 / 72 / 48 / 64 | 4.61-4.62x | **3.67x** | 4.30-4.31x | 4.61x |
| clang 18 `-O3` | self-built Linux | Ryzen 7 9800X3D | 30 / 99 / 83 / = `varT` | 6.34x | **4.93x** | 6.31x | = `varT` |
| | | EPYC 9V74 | 30 / 99 / 83 / 83 | 7.61x | **6.00x** | 7.56x | 7.57x |
| | | EPYC 7763 | 30 / — / 83 / 83 | 7.40x | — | 7.44x | 7.44x |
| | | Neoverse N2, 2 jobs | 22 / 72 / 48 / 64 | 4.66x | **3.71x** | 4.29x | 4.65x |
| clang 22 `-O3` | self-built Linux | i5-12400T | 30 / 65 / 53 / = `varT` | 4.08x | **3.17x** | 4.12x | = `varT` |
| gcc 13 `-O3` | `./configure` default | Ryzen 7 9800X3D | 19 / 48 / 52 / = `varT` | 5.50x | 6.12x | 5.90x | = `varT` |
| | | EPYC 7763 | 19 / — / — / 52 | 7.60x | — | — | 7.61x |
| | | EPYC 9V45, 4 jobs | — | 5.79-5.85x | 6.20-6.27x | 5.83x | = `varT` |
| | | EPYC 9V74, 2 jobs | 19 / — / 52 / 52 | 7.40x | 7.42x | 7.42x | 7.43x |
| | | Neoverse N2, 5 jobs | 14 / — / 40 / 64 | 4.15-4.16x | 4.22x | 4.27x | 4.50x |
| gcc 15 `-O3` | `./configure` on Ubuntu 26.04 | Neoverse N2 | 14 / — / 26 / 62 | 4.15x | — | 4.26x | 4.49x |
| gcc 13 `-O2` | none known (shipped `-O2` builds use PGO) | EPYC 7763 | — | 2.94x | 7.58x | — | — |
| | | EPYC 9V74 | — | 2.72x | 7.47x | — | — |
| | | Neoverse N2, 2 jobs | — | 3.39x | 4.22x | — | — |
| Apple clang 17 `-O3`, fortify | self-built macOS | Apple M1, 4 jobs | 0 / — / — / vector | 3.60-3.65x | 7.64-7.82x | 7.60x | 7.39x |
| | | Intel i7-8700B, 5 jobs | 0 / — / 29 / 29 | 2.82-3.38x | 5.59-5.73x | 5.68-5.69x | 5.06-5.68x |
| gcc 13 `-O3 -march=x86-64-v3` | self-built for AVX2 | EPYC 9V74 | 36 / 63 / 68 / — | 14.55x | **8.32x** | **8.63x** | — |
| | | EPYC 7763 | 36 / 63 / 68 / 68 | 14.92x | **9.05x** | **9.17x** | 15.03x |
| clang 18 `-O3 -march=x86-64-v3` | self-built for AVX2 | EPYC 7763, 2 jobs | 46 / 112 / 92 / 96 | 12.44-12.50x | **5.87-5.88x** | **7.71-7.72x** | 12.68x |
| gcc 13 `-O3 -march=x86-64-v4` | self-built for AVX-512 | Ryzen 7 9800X3D | zmm/ymm: 12/12 / — / — / 12/36 | 15.24x | — | — | 15.84x (`varB5` 20.43x) |
| | | EPYC 9V45, 2 jobs | 24 / — / — / 48 | 15.19-15.69x | — | — | 15.57-15.73x (`varB5` 20.22-20.60x) |
| | | EPYC 9V74 | 24 / — / — / 48 | 12.38x | — | — | 15.18x (`varB5` 14.76x) |
| | | Xeon 6975P | 24 / — / — / 48 | 7.65x | — | — | 9.46x (`varB5` 8.59x); at 1,024 the PR 3.59x, `varB` **3.26x**, `varB5` 3.70x |
| clang 18 `-O3 -march=x86-64-v4` | self-built for AVX-512 | Ryzen 7 9800X3D | zmm/ymm: 0/36 / — / — / 0/72 | 15.17x | — | — | 14.40x (`varB5` 15.22x) |

Notes:
- "Closest shipped build" names the build whose compiler and PGO setting the row matches. Shipped builds also differ in flags: Alpine's package and the Debian-based Docker images build at `-O2`; Debian, Ubuntu, Fedora, RHEL and Arch at `-O3`, all with `_FORTIFY_SOURCE`. Debian and Ubuntu use their own PGO training (the "Debian's training" row), the others CPython's default. uv's Linux and macOS Pythons (python-build-standalone) are built with its own clang 23, full LTO rather than ThinLTO, and on Linux x86-64 also BOLT.
- Apple M1 PGO: `varB` itself wasn't measured. In the first `varB` run the M1 job started, but the PR's PGO build failed at the ThinLTO link (`ld: ThinLTO file ... too small`, a race between two links that write to the same `.lto` directory, which also hit `main`'s build in an earlier macOS PGO job), so `varB` was never built; GitHub's macOS arm64 runners didn't start any of the retries. The cell is `varO`, which compiles to the same machine code on arm64.
- Intel Mac PGO: without AVX2, `varT` and `varN` (the `varB` cell) are the same machine code; in the same jobs they measured 4.85x and 5.15x (one job) and 4.99x and 5.05x (another), so the gap between the `varT` and `varB` cells in that row is run-to-run noise.
- MSVC x64 PGO on the EPYC 7763: in one job `main` itself was slow at 64K (42.4 us against 24.0-25.0 us in the other three), so that job gives the PR 3.97x and `varB` 8.85x; without it, the PR is 2.26-2.40x and `varB` 4.99-5.29x (`varB` / PR is 2.21-2.23 in all three `varB` jobs).
- "vector" in the Apple M1 SIMD cells: Apple's objdump writes NEON arithmetic as `and.16b v0, v1, v2`, which the count missed until commit 0d3d982 (it found the q-register loads and stores, 4-6 per block loop, and none in the PR).
- On Apple M1 the 32-byte block measured the same as or 2-4% below the 16-byte one (`varT`, `varN`) from 256 to 64K characters. `varB` uses 32 bytes on arm64 for Neoverse N2, where clang without PGO unrolls the PR's loop to 32 bytes per iteration and a 16-byte block is 7-8% slower than the PR.
- The 32-bit Windows rows are why `varB` keeps the PR's loop on 32-bit targets: with four 4-byte words, MSVC leaves the plain-C block scalar in the PGO build (0 SIMD instructions; 0.56x `main`), and in the Release build it vectorizes it only behind a run-time CPU check, through a stack copy, 17% slower than the PR's loop (43 SIMD instructions against 46; [`results/local/msvc_simd.md`](results/local/msvc_simd.md), [`results/local/win_msvc_varB.md`](results/local/win_msvc_varB.md)).
- MSVC without PGO, x64, one layout per build: `varB` is 1.06-1.08x the PR at 64K in all five runner jobs ([`results/msvc_runners_varB.md`](results/msvc_runners_varB.md)), but 0.68x on the Ryzen 7 9800X3D, as is `varR` there, while `varS`, with the same 16-instruction block loop, measured 6.47x on the same machine. In the `varB` and `varR` builds the loop starts at the same address, 16 bytes into a 64-byte line; in `varS`'s, 48 bytes in ([`results/local/win_msvc_rebuilds.md`](results/local/win_msvc_rebuilds.md)). So that build's number is most likely code placement; `varB`'s own loop couldn't be moved to test it, since Windows builds are one layout each. In the two x64 Release runner jobs (EPYC 7763, EPYC 9V45) `varR` measured 1.07x and 1.10x the PR at 64K ([`results/msvc_runners.md`](results/msvc_runners.md)), and `varS` 1.09x and 0.91x (run 41760501953's artifacts).
- At 1,024 characters the differences are smaller. In most x86-64 PGO runner jobs the ratio to the PR at 1,024 is roughly the square root of the one at 64K (less shrinkage on the Ryzen 7 9800X3D and for gcc 16's scalar `varR`): gcc 13 PGO+LTO on the EPYC 7763 (3 jobs) is PR 1.92-2.02x, `varR` 3.55x, `varT` 3.72-3.73x, `varB` 3.65-3.78x; clang 21 PGO+LTO with AVX2 is PR 2.48x, `varR` 4.06x, `varT` 4.15x, `varN` 5.06x. On AVX2 builds without PGO the losses of `varR` and `varT` mostly disappear (0.85-0.97x the PR at 1,024), and under clang without PGO, fortify or AVX2, `varR` is 4-12% slower than the PR at 1,024, against 20-22% at 64K.
- Every layout-workflow job, at 16, 32, 256, 1,024, 4,096 and 64K, is in [`results/runner_jobs.md`](results/runner_jobs.md); local runs are in [`results/local/`](results/local) and [`results/thinkcentre/`](results/thinkcentre).

## Short strings

The real-world short-string mix (`realworld/replay.py`: the eight everyday workloads above, shuffled), main / build, the mean over 8 code layouts per job (4 in the Debian-training job). [`results/short_pool.md`](results/short_pool.md) lists every row.

`varB`'s code (`varB`, or the tree with the same machine code in that job), ratio to the PR, pooled over the layout runs (runner jobs, plus 4 local runs in the "x86-64 without AVX2" row and so in "all"):

| Target | Runs | Geometric mean | 95% interval | Runs ahead of the PR | Lowest |
|---|---|---|---|---|---|
| x86-64 without AVX2 | 33 | 0.994x | 0.979-1.010 | 13 | 0.863x |
| x86-64 with AVX2 or AVX-512 | 12 | 0.989x | 0.962-1.016 | 5 | 0.871x |
| arm64 | 11 | 1.000x | 0.994-1.007 | 7 | 0.976x |
| all | 56 | 0.994x | 0.983-1.005 | 25 | 0.863x |

The other variants, over the jobs that measured each next to the PR:

| | PR | `varR` | `varT` | `varS` | `varU` |
|---|---|---|---|---|---|
| Geometric mean, 39 rows (35 runner jobs, 4 local runs) | 1.024x | 1.028x | 1.014x | | |
| Ratio to the PR, 95% interval | | 1.004 (0.991-1.017) | 0.990 (0.975-1.005) | | |
| Geometric mean, the 13 rows with all five | 1.027x | 1.032x | 1.026x | 1.047x | 1.048x |
| Ratio to the PR, 95% interval | | 1.005 (0.987-1.022) | 0.998 (0.981-1.017) | 1.019 (0.998-1.040) | 1.021 (0.999-1.043) |

- The two lowest are PGO builds. 0.863x is `varT` in the first Ubuntu 26.04 rebuild below, which had no control measurement; in the three other rebuilds the same tree measured 0.98-1.03x `main`. 0.871x is `varN` in the RHEL `-O2` job. There `varN`'s build is also slower on operations that never reach the case code (4.5%), but that is only part of the gap, and `varO`, the same machine code in its own build, measured 0.834x the PR. The cause wasn't found, and the job wasn't rebuilt. The lowest non-PGO job is 0.93x on the Intel Mac, where `varB`'s layouts after the first ran 8-12% slower than it while `main`'s and the PR's didn't; the next Intel Mac release job measured `varB` at 1.006x `main` and the PR at 1.008x, with `varT` (the same machine code) at 1.013x.
- The overlapping short-string path of `varS` and `varU` (4- and 2-byte words for strings under 8 bytes) gains about 2% for 39 more lines: a possible follow-up.
- MSVC: Windows builds can't be relinked with padding, so each build is one layout. On the Ryzen 7 9800X3D, over four x64 PGO builds each, pinned, `varB` is 0.99x the PR on the short mix by best and by median times, while rebuilds of the same tree spread over 3% by best times and 7% by median; per workload it ranges from 0.96x (config keys) to 1.00x ([`results/local/win_msvc_rebuilds.md`](results/local/win_msvc_rebuilds.md)). Part of that 1% is likely setup that MSVC places at the top of `varB`'s function, before the length test: a stack adjustment, saving `xmm6`, and two constants splatted into vector registers, so calls for 8 to 15 bytes pay for it too. On the runners (one build and one layout per job; the replay pinned to one CPU at high priority) `varB` / PR is 0.97x on x64 PGO (8 jobs, best times, 95% interval 0.94-1.00; median 0.98x, 0.93-1.03), 1.01x on x64 Release (5 jobs, best times; 1.00x by median) and 0.99x on ARM64 PGO (4 jobs, best times, 0.98-1.01; 0.94x by median, 0.87-1.02) ([`results/msvc_runners_varB.md`](results/msvc_runners_varB.md)). In the local x64 Release build, the one with the badly placed block loop, `varB` is 0.97x the PR by best and by median times.

Rebuilding identical source with PGO is a larger effect than any difference between the variants. On the Ubuntu 26.04 runner (gcc 15 PGO+LTO, EPYC 7763), four builds of each tree gave these short-mix results ([`results/u2604_rebuilds.md`](results/u2604_rebuilds.md)):

| Build | PR | `varR` | `varT` | Operations that never reach the case code: PR, `varR`, `varT` |
|---|---|---|---|---|
| 1 | 0.997x | 1.024x | **0.860x** | not measured |
| 2 | 0.973x | **0.970x** | 0.977x | 0.993x, **0.923x**, 0.987x |
| 3 | 1.099x | 1.042x | 1.034x | 1.172x, 1.129x, 1.154x (`main` itself was the slow build) |
| 4 | **0.838x** | 1.010x | 0.979x | 0.988x, 0.975x, 1.002x |

The PR's result moves from 0.838x to 1.099x of `main` between rebuilds. The binaries differ: `_PyEval_EvalFrameDefault` is 63,748 bytes in one build of `main` and 63,936 in the next. Long strings don't move (64K: 3.97x, 13.24-13.25x, 13.47-13.48x in all four builds).

## The proposed tests change what PGO sees

CPython's PGO training (`-m test --pgo`, for `./configure --enable-optimizations` and for `PCbuild\build.bat --pgo`) runs `test_str` and `test_bytes`. The proposed tests convert thousands of strings of 1 to 1,000 characters, so with them the training reaches the block and word loops, and PGO optimizes them as hot code. gcc 13 PGO+LTO, Ryzen 7 9800X3D, 8 layouts, `main` without the tests ([`results/local/pgo_tests.md`](results/local/pgo_tests.md); `tests/add_tests.py` adds the tests):

| Tree | SIMD | 16 | 128 | 1,024 | 64K | Short mix |
|---|---|---|---|---|---|---|
| PR | 0 | 1.06x | 1.43x | 1.92x | 2.32x | 1.026x |
| PR + tests | 45 | 1.09x | 1.74x | 2.95x | 3.98x | 1.042x |
| `varB` | 31 | 1.07x | 1.70x | 3.26x | 4.90x | 1.024x |
| `varB` + tests | 82 | 1.11x | 1.80x | 4.00x | 6.72x | 1.057x |

MSVC 19.51 x64 PGO (`PCbuild\build.bat --pgo`), the same machine, one layout per build: the tests change nothing. With them the PR's `ascii_case_words` has the same instructions as without (0 SIMD), and the PR stays at 2.64x `main` at 64K and 2.27-2.28x at 1,024; `varB` is 5.72-5.74x and 3.38-3.41x.

- With the tests, gcc vectorizes the PR's loop, and `varB` gains too: gcc converts the first blocks before the loop and tests the loop condition at the bottom (82 SIMD instructions instead of 31), though the loop still converts one block per iteration; the cause of the gain wasn't isolated. `varB` with the tests is 1.69x the PR with the tests at 64K and 1.36x at 1,024.
- Without the tests `varB`'s 64K result varies over the layouts (0.93-1.23x of its mean); with them it doesn't (1.00-1.00x). The cause wasn't established.
- This reaches builds whose PGO training runs these tests, with a compiler whose PGO then vectorizes the hot loop. Measured: gcc 13 on x86-64 does, MSVC x64 doesn't. Not measured: clang (uv's Pythons and python.org's macOS installer use CPython's training), MSVC ARM64, other gcc versions, and Debian's and Ubuntu's own training, which runs the whole test suite. Builds without PGO get none of this. It also depends on what the tests happen to run; changing the training to fix the PR's loop would work the same way, and break the same way.

## Which CI jobs build each path

CPython's GitHub Actions (`build.yml` on the PR's base), for a change to `Objects/bytes_methods.c`:

| Code path in `varB` | Built and tested by |
|---|---|
| 16-byte GNU vector (gcc and clang, x86-64 without AVX2) | Ubuntu x86-64 and macOS Intel (debug builds), the sanitizer jobs, Android x86_64 |
| 32-byte GNU vector on arm64 | Ubuntu arm64 and macOS arm64 (debug builds), Ubuntu (installed) on arm64 (gcc `-O3`, runs the test suite), Android aarch64, iOS |
| 32-byte GNU vector with AVX2 | none: no job compiles the core with AVX2 (only code that picks its path at run time gets it: HACL*'s SIMD256 files, with `-mavx2` or `/arch:AVX2`, and on Windows zlib-ng's AVX2 and AVX-512 files) |
| MSVC block, x64 and ARM64 | Windows x64 (Debug, and Release with the tail-calling interpreter), Windows arm64 (Debug) |
| The PR's count-by-one loop (MSVC: 8-15 bytes on 64-bit, from 4 bytes on 32-bit) | every Windows job; Win32 (Debug) for every length |
| The PR's word loop (gcc and clang: 8-15 bytes, or 8-31 with AVX2 and on arm64; on 32-bit targets from 4 bytes, on other 64-bit targets from 8) | every Linux and macOS job; WASI and Emscripten (wasm32, debug) for every length |

The debug builds run the same code paths at `-O0`/`-Og`. The 32-byte AVX2 path would be tested only by builds that enable AVX2 and run the proposed tests.

## Patch size, and which code each platform gets

| | PR | `varR` | `varT` | `varN` | `varB` |
|---|---|---|---|---|---|
| Non-blank lines added to `bytes_methods.c` | 56 | 67 | 87 | 96 | 112 |
| gcc/clang, x86-64 | word loop | 16-byte array block | 16-byte GNU vector | GNU vector, 32 bytes with AVX2 | as `varN` |
| gcc/clang, arm64 | word loop | 16-byte array block | 16-byte GNU vector | as `varT` | 32-byte GNU vector |
| MSVC, x64 or ARM64 | count-by-one word loop | 16-byte array block | as `varR` | as `varR` | 16-byte array block, then the PR's loop |
| 32-bit targets, clang-cl, other 64-bit targets | word loop (count-by-one under MSVC) | 16-byte array block | as `varR` | as `varR` | as the PR |

Line counts are for the variant patches against CPython 4e0677ac; `varJ.patch` adds 58 (longer comments), `varO.patch` 90, `varB5.patch` 117. `varS` and `varU` add 106 and 126.

Not measured: ppc64le, s390x, riscv64, armv7, wasm32, clang-cl, MinGW/MSYS2 and Cygwin (gcc on Windows), Intel icx, iOS, Android, and the x86-64 slice of python.org's universal2 macOS installer as built (a PGO build; the Intel Mac rows use the same compiler family). Under `varB`, ppc64le, s390x, riscv64, armv7, wasm32, clang-cl and icx on Windows (which, like clang-cl, doesn't define `__GNUC__`) keep the PR's code; MinGW, Cygwin and icx on Linux (which define `__GNUC__`) and the arm64 builds for iOS and Android get the GNU vector of their target (16 bytes on x86-64 without AVX2, 32 on arm64), as do python.org's x86_64 Android package and iOS simulator slice (16 bytes).

## How `varB` got here

1. The PR's loop is scalar in PGO builds. `varP` and `varR` added a plain-C 16-byte block that compilers vectorize also in cold code (`varR` for every compiler, `varP` outside MSVC). An adversarial review of an earlier GNU-vector variant (`varY`, [`results/varY_review.md`](results/varY_review.md)) proposed it.
2. gcc 16 PGO (Fedora, Arch) leaves that block scalar on x86-64, and clang without PGO or `_FORTIFY_SOURCE` (FreeBSD's packages, self-built Linux Pythons) reshuffles it (20-22% slower than the PR at 64K without AVX2). `varT` writes the block as a GNU vector on gcc and clang.
3. On AVX2 builds gcc and clang widen the PR's loop to 32 bytes but keep `varT`'s vectors at 16. `varN` uses 32-byte vectors under `__AVX2__`.
4. On 32-bit Windows the plain-C block is slower than the PR's loop: MSVC vectorizes it at `/O2` only through a stack copy behind a CPU check (Release: 17% slower than the PR) and leaves it scalar in PGO builds (0.56x `main`); the platforms nobody measured would get it too. `varB` keeps the array block to 64-bit MSVC and the PR's code everywhere else outside gcc and clang on x86-64 and arm64.
5. On Neoverse N2, clang without PGO unrolls the PR's loop by two (32 bytes per iteration), so `varT`'s and `varN`'s one-vector loop was 7-8% slower than the PR at 64K. `varO` tried 32-byte vectors for every gcc and clang build on x86-64 and arm64: on arm64 it matches or beats the PR with every compiler measured (gcc 13, 15 and 16, clang 18 and 21; Apple clang 17 with PGO, and without PGO as `varB`, which has the same code on arm64), but on x86-64 without AVX2 gcc lowers the 32-byte vector badly (0.41-0.53x `main` at 64K in gcc PGO builds). `varB` takes 32-byte vectors on arm64 and keeps 16 bytes on x86-64 without AVX2.
6. `varB` was then measured as itself on the runners (Linux, macOS and Windows, x86-64 and arm64, PGO and not); on x86-64 and arm64 it also compiles to the same machine code as the variant measured before for that target ([`results/varB_equiv.md`](results/varB_equiv.md)).

## How it was measured

- **Code placement.** On these machines, moving identical code by a few bytes changes its speed by more than the variants differ: on the EPYC 9V45 runner, `varT`'s 64K time varies by a factor of 1.72 across 8 code layouts of the same build, and on the Ryzen 7 9800X3D the PR's 64K time by 0.82-1.40x of its mean. So most numbers here are means over 8 code layouts: each build is relinked with a padding object of 0, 16, 32, 48, 1,024, 2,064, 3,104 or 4,080 bytes linked ahead of Python's object files (each 16-byte offset in a 64-byte cache line, at two page offsets). That usually moves Python's code together, so it doesn't vary where functions sit relative to each other. In gcc PGO builds, though, the linker places hot functions (`.text.hot`, such as `_PyEval_EvalFrameDefault`) and cold parts (`.text.unlikely`) ahead of the padding; there the shift moves `ascii_case_words` and other ordinary code but not the interpreter loop. Either way the per-job intervals understate the uncertainty. [`realworld/layout_local.sh`](realworld/layout_local.sh) does this on Linux and macOS, and the `layout` workflow does it on GitHub runners. Windows builds can't be relinked this way, so MSVC rows are single layouts, and the MSVC runner rows are pyperf runs (`bench.py`).
- **Whole-build differences.** PGO builds also differ as a whole between rebuilds (see "Short strings"). The `layout` workflow times string operations that never reach the case code (`realworld/control.py`) to show when that happens.
- **Machines:**
  - Ryzen 7 9800X3D (Zen 5): Windows 11 for MSVC 19.51; WSL2 Ubuntu 24.04 for gcc 13.3 and clang 18.1.
  - Core i5-12400T, Fedora 44: gcc 16.2, clang 22.1, and Fedora's own `python3` build recipe.
  - GitHub-hosted runners: AMD EPYC 7763 / 9V74 / 9V45, Intel Xeon 6975P / Platinum 8573C / Platinum 8370C, Neoverse N2, Cobalt 100, Apple M1, Intel i7-8700B. Fedora 44 rows ran in a `fedora:44` container on the runner.
- **Workloads:** fixed lengths (`realworld/len_layout.py`), the real-world replay (`realworld/replay.py`) and pyperf micro-benchmarks (`bench.py`). The layout runs, local and on runners, are pinned to one CPU on Linux and Windows (Windows at high priority); macOS can't pin. The pyperf runs (MSVC runner rows, the i5 Fedora row) are not pinned.
- **Vectorized or not:** the `layout` workflow records the SSE/AVX/NEON instruction count in `ascii_case_words` for every tree (`results/simd.txt` in each job's artifact) since commit 35413ad (on macOS only since c52fe0b, before which it read a missing file and shows 0; Apple's NEON arithmetic syntax and AVX-512 zmm registers only since 0d3d982); earlier jobs have no count. Local counts are in the `results/local` files.

## Other variants, and why not

- **`varV` (the PR + `__builtin_memcpy`):** fixes only the macOS fortify case. It does nothing for PGO builds.
- **`varW` (`varV` + overlapping short path):** good on short strings, but the same long-string gaps as `varV`.
- **`varX` (two named words per iteration):** gcc vectorizes it also at `-O2` and in gcc 16 PGO builds (Fedora's recipe on the i5-12400T: 31 SIMD instructions, about the speed of `varY`; [`results/thinkcentre/fedora_spec.md`](results/thinkcentre/fedora_spec.md)), but under Apple clang on an M4 it is 0.80-0.81x `varV`, `varW` and `varY` at 64K ([`results/m4/run1.md`](results/m4/run1.md)), and its MSVC branch is the PR's.
- **`varY` (a 16-byte GNU vector loop gated by a configure macro):** fast, but it mixes vectors with scalars, which clang before 5.0 rejects (the gh-148474 break), and its configure macro is only set for gcc 12+ and clang.
- **`varP`/`varQ`:** `varR`/`varS` with the PR's MSVC branch kept. Same code as `varR`/`varS` on gcc and clang.
- **`varB5`** (`varB` + a 64-byte vector under `__AVX512F__`): 1.3x `varB` at 64K with gcc and AVX-512 without PGO on AMD Zen 5, and it fixes `varB`'s 0.91x at 1,024 on the Xeon 6975P there, but at 64K it is 0.91x `varB` on that Xeon and 0.97x on the EPYC 9V74 (Zen 4). In uv's x86-64-v4 configuration (measured with clang 21 PGO+LTO) it is 0.78x `varB` at 64K on the Xeon 6975P and 0.39x on the Xeon 8370C, consistently over the 8 layouts. Not offered.
- **`#pragma optimize("t", on)` around the count-by-one loop** of the PR's earlier revision 91c788f (not re-run on 9433a66): MSVC's PGO build still leaves it scalar (0 SIMD instructions).
- **Changing the PGO training instead of the code:** see "The proposed tests change what PGO sees". It helps only where the PGO training runs the loop with a compiler whose PGO then vectorizes it: gcc did, MSVC didn't (the loop stays scalar with the tests), clang wasn't measured. It also lasts only as long as the training reaches the loop.
- **SSE2/NEON intrinsics:** not tried. CPython's string code has none, and on gcc and clang the GNU vector type already compiles to the same instructions. Intrinsics would also reach MSVC on 32-bit x86, where `varB` keeps the PR's loop (scalar in PGO builds), at the cost of a separate path per architecture.

## Files

- Patches against CPython 4e0677ac: `variants/varB.patch` (recommended), `variants/varB5.patch` (`varB` + a 64-byte AVX-512 block; not offered), `variants/varN.patch`, `variants/varO.patch`, `variants/varT.patch`, `variants/varR.patch`, and the short-path versions `variants/varS.patch`, `variants/varU.patch`.
- Tests: [`tests/proposed_tests.py`](tests/proposed_tests.py), and the same tests placed where a PR would put them: [`tests/add_tests.py`](tests/add_tests.py), [`tests/tests.patch`](tests/tests.patch). The mutation check: [`tests/mutation_check.sh`](tests/mutation_check.sh), [`tests/mutants.py`](tests/mutants.py). Same machine code: [`tests/same_code.sh`](tests/same_code.sh).
- Raw data: workflow artifacts on the [runs page](https://github.com/ptweezy/cpython-ascii-case-bench/actions) (GitHub deletes them 90 days after each run, from early February 2027), plus `results/` and the scripts in `analysis/` that derive the tables from them.
