# The compact variants: which one to offer

The `cmp*` variants (see the README) try to keep `varB`'s gains in PGO builds at about the PR's size, in plain C. This is the final round, run on 2026-11-04 and 05, with the two proposed tests in every tree that has them (`PRt`, `cmpBt`, `cmpRt`, `cmpDt`), because CPython's PGO training runs `test_str` and `test_bytes` and the tests change what gcc's PGO does with the loop ([`local/pgo_tests.md`](local/pgo_tests.md)).

Speedups are time on `main` / time with the build at 65,536 characters ("64K"), unless noted. "vs PR" is that divided by the PR's speedup in the same job.

## Recommendation: `cmpD` plus the two tests

`cmpD` adds 57 non-blank lines to `bytes_methods.c` (the PR adds 56), with one `#if` (the PR has one), plain C11 and no compiler extensions. On 64-bit targets it converts 16-byte blocks of two words, then the remaining words, then the overlapping last word. The `#if` picks the block's form: two separate words for gcc, a two-iteration array loop for clang and MSVC. Each compiler gets the form it vectorizes where PGO finds the code cold:

- gcc 16 PGO leaves the array loop scalar (`cmpB`), but vectorizes two separate words (`cmpC`).
- Apple clang 21 with the SDK's `_FORTIFY_SOURCE` leaves two separate words scalar (`cmpC`), but vectorizes the array loop (`cmpB`).
- MSVC vectorizes only the loop form.

Under clang it compiles to `cmpB`'s machine code (x86-64, AVX2, AVX-512 and aarch64 at `-O2`, `-O3` and `-Os`), and under gcc to `cmpC`'s (`tests/same_code.sh`). Under MSVC x64 it compiles to the same instructions as `cmpB` (149 instructions with 52 SIMD at `/O2`; 78 with 18 SIMD at `/O1 /Oi`, as in PGO-cold code). So `cmpB`'s results stand for `cmpD` under clang and MSVC x64, and `cmpC`'s under gcc. MSVC ARM64 wasn't checked by disassembly; its preprocessed source is the same loop as `cmpB`'s.

## PGO builds with the tests

The configuration distribution and python.org builds would get once the tests land.

| Build (shipped as) | PR | `cmpD` | `cmpD` vs PR | `cmpB` vs PR |
|---|---|---|---|---|
| MSVC x64 PGO, `--tail-call-interp` (python.org Windows 3.15+), 4 runner jobs | 2.1-4.0x | 5.0-8.4x | 2.09-2.46x | same code |
| same, local Ryzen 7 9800X3D | 2.84x | 5.91x | 2.08x | same code |
| MSVC ARM64 PGO (python.org Windows ARM64), 2 jobs | 2.94-3.03x | 3.78-3.86x | 1.27-1.28x | same source |
| gcc 13 PGO+LTO x86-64 (Ubuntu 24.04, Debian), 2 jobs | 8.23-8.25x | 7.01-7.76x | 0.85-0.94x | 1.00-1.06x |
| gcc 13 PGO+LTO arm64, 2 jobs | 4.27x | 4.36-4.37x | 1.02x | 0.99x |
| gcc 16 PGO+LTO x86-64 (fedora:44; Fedora, Arch) | 5.93x | 6.66x | 1.12x | **0.45x** |
| gcc 16 PGO+LTO arm64 | 4.22x | 4.18x | 0.99x | 0.98x |
| clang 21 PGO+LTO x86-64 (uv's Pythons), 2 jobs | 3.23-3.44x | 7.75-7.84x | 2.25-2.43x | same code |
| Apple clang 17 PGO+LTO, M1 (python.org macOS) | 3.61x | 7.58x | 2.10x | same code |
| Apple clang 17 PGO+LTO, Intel | 3.02x | 5.69x | 1.88x | same code |

The `cmpD` cells for MSVC and clang are `cmpBt`'s measurements (same code). With the tests, gcc 16 PGO vectorizes the PR's word loop, but still not `cmpB`'s array loop (0 SIMD instructions): `cmpBt` is 2.68x `main` against the PR's 5.93x, and `cmpRt` 2.42x. That rules out `cmpB` and `cmpR`.

## PGO builds without the tests

Builds whose training doesn't reach the loop (from the first compact round, `cmpC`'s gcc numbers for `cmpD`'s gcc code):

| Build | `cmpD` vs PR |
|---|---|
| MSVC x64 PGO (4 jobs, without `--tail-call-interp`) | about 1.9x (`cmpA`, same x64 code) |
| gcc 13 PGO+LTO x86-64 | about 2.6x |
| gcc 16 PGO+LTO x86-64, fedora:44 runner | 2.46x (4.41x `main` against 1.79x) |
| gcc 16 PGO+LTO x86-64, ThinkCentre, Fedora's own recipe, 7 rebuilds | about 2.8x (5.2-5.4x `main` against 1.92x) |
| clang 21 PGO+LTO x86-64 | about 2.4x |
| Apple clang 21 PGO+LTO, M4 (8 layouts) | 1.69x (`cmpB`: 5.76x `main` against 3.41x) |

## Builds without PGO

| Build | PR | `cmpD` | vs PR |
|---|---|---|---|
| gcc 13 `-O3` x86-64 | 7.45x | 7.46x | 1.00x |
| gcc 13 `-O3` arm64 | 4.16x | 4.17x | 1.00x |
| clang 18 `-O3` x86-64 (`cmpB`'s code) | 7.45x | 5.92x | 0.79x |
| clang 18 `-O3` arm64 (`cmpB`'s code) | 4.66x | 3.71x | 0.80x |
| clang `-march=x86-64-v3` (`cmpB`'s code) | 9.46x | 5.39x | 0.57x |
| gcc `-march=x86-64-v3` | 14.89x | not measured (`cmpB`: 9.07x) | |
| MSVC x86 Release (python.org 32-bit Windows; same code as `cmpB`), one local layout | 4.46x | 5.09x | 1.14x |

## Without vectorization

As asked on the issue: gcc `-fno-tree-vectorize` and clang `-fno-vectorize -fno-slp-vectorize`, release builds, 8 layouts per job. Every build has 0 SIMD instructions in `ascii_case_words`.

| Build | PR | `cmpD` | `cmpD` at 16 chars | `cmpD` short mix |
|---|---|---|---|---|
| gcc 13 x86-64 | 2.45x | 3.12x | 1.06x | 1.049x |
| gcc 13 arm64 | 3.39x | 3.97x | 1.05x | 1.028x |
| clang 18 x86-64 | 2.96x | 3.04x | 1.09x | 1.036x |
| clang 18 arm64 | 3.20x | 3.21x | 1.07x | 1.024x |

`cmpD` is faster than `main` at every length measured (16 to 64K) in all four, and at least as fast as the PR at 64K.

## Short strings

Pooled over 33 runner jobs that measured `cmpD`'s code (`cmpD`, `cmpDt`, or `cmpB`/`cmpBt` under clang, `cmpC` under gcc) and the PR in the same job, the real-world short-string mix is 0.995x the PR (geometric mean; 95% interval 0.986-1.005; per job 0.951-1.082). Strings shorter than 8 bytes take the unchanged byte loop. Code that compiles identically (`cmpA` and `cmpB` under gcc) has measured up to 6% apart in a single job, so one job can show a few percent either way.

## Why not the others

- **`cmpB`** (46 lines, no `#if`): 0.45x the PR under gcc 16 PGO with the tests (above), a shipped Tier-1 build (Fedora 45+, Arch).
- **`cmpR`** (55 lines): the same gcc 16 failure (0.41x), 0.85x the PR under gcc 13 PGO with the tests, and no arm64 gain (1.01-1.02x).
- **`cmpC`** (56 lines): Apple clang 21 leaves its separate words scalar: 1.07x the PR on the M4, against `cmpB`'s 1.69x.
- **`cmpM`** (35 lines): 0.85-0.94x the PR on macOS at 64K, which is why the PR stopped counting by one outside MSVC. **`cmpMi`** (44 lines) compiles to the PR's loops, so it keeps the scalar PGO loop.
- **`cmpT`** (`varB`'s code, 88 lines, 5 `#if`s, GNU vectors, an `__AVX2__` branch): the fastest in most cells, but over twice the size, and against the reviewers' recent choices: on [#122902](https://github.com/python/cpython/pull/122902) a `vector_size(16)` variant was declined as more complexity for the gain, PEP 7 asks for no compiler extensions, and BLAKE2's SIMD is being removed ([#160392](https://github.com/python/cpython/pull/160392)). It stays available as a follow-up if a core developer asks for it.

## `cmpD`'s weak spots

All are still several times faster than `main`:

- gcc 13 PGO on x86-64 with the tests: 0.85-0.94x the PR (7.0-7.8x `main`), because the tests let gcc 13 vectorize the PR's loop too.
- clang without PGO: 0.79-0.80x the PR (3.7-5.9x `main`).
- AVX2 builds without PGO: `cmpB`'s code is 0.57-0.61x the PR (5.4-9.1x `main`); gcc with AVX2 not measured for `cmpD`.
- arm64 Linux gcc PGO: about equal to the PR (0.99-1.02x with the tests).

## Notes

- Correctness: every runner build of `cmpD`'s code passed `edge_cases.py` (253,814 cases) and `check_all.py` (1,495,930 cases); the trees with the tests also ran them in their PGO training. The old-compiler workflow (gcc 4.7-16, clang 3.4-22) was run on `varB`, `varT` and `cmpA`, not on `cmpD`.
- Invalid runs: the `k-novec` and `k-novec-D` jobs were labelled "novec" but built as plain release (the layout workflow ignored that build type); the real no-vectorization runs are `k-gcc-novec` and `k-clang-novec`, with the flags passed as `cflags`. A local MSVC ARM64 cross-build silently produced x64 code and was discarded.
- MSVC results from a single local build are dominated by code placement (Win32 PGO: `cmpB` and `cmpR` compile to the same instructions and measured 1.30x and 1.02x `main`); the runner rows above are means over several jobs.
