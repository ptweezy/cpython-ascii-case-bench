# Adversarial review of varY (30 agents: 4 reviewers, 26 skeptics)

| # | Lens | Claimed | Verdict | Final severity | Finding |
|---|---|---|---|---|---|
| 1 | correctness | minor | confirmed | minor | No in-tree test exercises the new >=16-byte vector path, its overlapping tail, the case-boundary bytes, or unaligned starts |
| 2 | correctness | info | refuted | info | ASCII_CASE_MEMCPY hunk does nothing on platforms that have the vector path; its macOS comment is misleading |
| 3 | correctness | info | confirmed | info | clang emits an unreachable auto-vectorized copy of the word loop for 8..15 bytes |
| 4 | correctness | info | confirmed | info | Comment at lines 280-281 overstates: clang -O2 does vectorize the word loop |
| 5 | correctness | info | confirmed | info | varY reuses the pystrhex macro without updating its configure comment, and relies on vector features the probe does not test |
| 6 | correctness | info | confirmed | info | Residual risk: not executed on real ARM32/aarch64/big-endian hardware |
| 7 | portability | minor | confirmed | minor | The gate lets in clang < 5, which cannot compile varY's vector-plus-scalar operations |
| 8 | portability | minor | confirmed | info | Reusing the shufflevector macro shuts out GCC 4.7-11, so the stated gcc -O2 motivation goes uncovered on many current LTS distros |
| 9 | portability | minor | confirmed | minor | The macro's name, description and configure comment do not match this use, and lower()/upper() become tied to a check owned by bytes.hex() |
| 10 | portability | minor | confirmed | minor | ASCII_CASE_MEMCPY no longer serves its stated purpose wherever the vector path is on, and makes clang emit about 230 bytes of unreachable vector code |
| 11 | portability | info | confirmed | info | Windows (MSVC and clang-cl) never get the vector path, so a Windows PGO build that finds the loop cold is not fixed |
| 12 | performance | major | confirmed | minor | With -O3 and AVX2 (x86-64-v3/v4), the PR's auto-vectorized loop uses wider vectors than varY's fixed 16-byte vectors, so varY does about 2x the work per byte on long strings |
| 13 | performance | minor | confirmed | minor | clang still vectorizes varY's 8..15 word loop, which can never reach the vector part; this adds dead code and an unconditional push/pop |
| 14 | performance | minor | confirmed | minor | On AArch64, clang does not unroll varY's vector loop; the PR's auto-vectorized loop does 32 B per iteration with ldp/stp |
| 15 | performance | minor | confirmed | minor | Gating on _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR leaves gcc 11 and older builds without the vector path, though varY only needs vector_size |
| 16 | performance | info | confirmed | info | In size-optimized or cold gcc code, varY's loop mixes floating-point-domain logic ops with integer SIMD adds |
| 17 | review-readiness | major | confirmed | major | Not necessary as written: a plain-C 16-byte block gets the same SIMD without GNU vectors, the configure macro, or __builtin_memcpy |
| 18 | review-readiness | major | confirmed | minor | No tests exercise the word or vector paths; the SIMD precedent shipped boundary tests |
| 19 | review-readiness | major | confirmed | major | Mixing scalars with GNU vector operands repeats the construct that broke pystrhex.c on older clang (gh-148474) |
| 20 | review-readiness | major | confirmed | major | Precedent shows maintainers resist SIMD in core on cost/benefit grounds; varY would be the second site |
| 21 | review-readiness | minor | confirmed | minor | Reusing _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR: misleading name, gcc >= 12 requirement, stale configure documentation |
| 22 | review-readiness | minor | confirmed | minor | ASCII_CASE_MEMCPY does nothing useful where varY's vector path exists, and its comment names macOS, where it does not apply |
| 23 | review-readiness | minor | confirmed | minor | Comments overstate or go stale: '-O2' applies to GCC only; the Apple-cores rationale is moot under varY |
| 24 | review-readiness | minor | confirmed | minor | More #if paths, duplicated logic, and a generic 64-bit long-string path that GitHub CI no longer runs |
| 25 | review-readiness | minor | confirmed | info | NEWS entry and patch scope do not reflect the SIMD change |
| 26 | review-readiness | info | confirmed | info | AI-tools policy points that matter for presenting varY |

## 1. No in-tree test exercises the new >=16-byte vector path, its overlapping tail, the case-boundary bytes, or unaligned starts

**Claim.** varY adds a third code path: a 16-byte vector loop plus an overlapping final 16 bytes. On ARM32 NEON and x32 the vector has 4 lanes, not 2. No regression test in Lib/test checks it. The only lower()/upper() checks in string_tests.py use 'HeLLo' (5 bytes), which only reaches the byte loop. Nothing checks the boundary bytes '@','[','`','{' or the high-bit look-alikes 0xC1/0xDA/0xE1/0xFA at lengths >= 8 or >= 16. If a later edit breaks the vector path, CI would catch it only by accident, and the 4-lane variant has no CI coverage at all.

**Evidence.** Lib/test/string_tests.py:451-459 is the whole generic test (checkequal('hello', 'HeLLo', 'lower') and the 'HELLO' equivalents). test_str.py:911-955 tests non-ASCII cases only. test_bytes.py:3093/3113 is a free-threading smoke test that checks only c[0]/c[-1]. git diff --stat on the PR branch shows no Lib/test/test_bytes.py, test_str.py or string_tests.py change for gh-161155. The out-of-tree checkers catch these bugs. Mutating ascii_case_words' gt from -26 to -25 makes my harness fail at 'len=8 pos=3 in=5a got=5a want=7a'. Moving the tail to len-15 fails at len=16. Neither mutant would fail any in-tree test.

**Suggestion.** Add a compact test to string_tests.py or test_bytes.py. Cover lengths 0..40 (byte loop, word loop, vector loop and overlapping tail). Fill with the bytes b'@AZ[`az{' plus 0xC1, 0xDA, 0xE1, 0xFA. Compare against a translate()-based reference for bytes, bytearray and ASCII str. Get unaligned starts from bytearray 'del ba[:k]' for k in 0..15, plus capitalize(), which calls _Py_bytes_lower(result + 1, s + 1, len - 1).

**Verifier (confirmed, minor).** I couldn't refute the core of the finding. Its headline overstates things, though.

What holds up:
- Neither the PR nor varY adds a test. `git diff --stat fcbd4c1^2 HEAD` lists only Objects/bytes_methods.c and the NEWS entry, and varY.patch changes only bytes_methods.c.
- string_tests.py:451-459 checks only 'HeLLo', 'hello' and 'HELLO', which are 5 bytes and so reach only the byte loop.
- string_tests.test_capitalize uses strings whose len-1 is at most 6.
- test_str.py:909-955 adds only non-ASCII cases.
- The free-threading test in test_bytes.py (~3093/3113) checks only c[0] or c[-1], and it runs only on GIL-disabled builds.
- No in-tree test checks '@', '[', '`', '{' or the high-bit bytes 0xC1/0xDA/0xE1/0xFA at lengths >= 8.
- My mutation harness confirms the gap. Each of these mutants passes every input that the in-tree lower/upper/capitalize tests feed in, yet fails a simple reference check at len 8 or 16:
  - the reviewer's gt -25 ('Z' not converted)
  - the reviewer's tail at len-15
  - ge at first-1 ('@' and '`' converted)
  - gt -27 ('[' and '{' converted)
  - dropping `& ~x` (high-bit bytes converted)
- The 4-lane claim is correct. On x32, size_t is 4 bytes and x32 also defines `__x86_64__`, so the configure check defines the macro.

What is overstated:
- "No in-tree test exercises the >=16-byte vector path, its overlapping tail … or unaligned starts" is wrong. Lib/test/test_bigmem.py runs by default in dry-run mode with size 5147 (`bigmemtest`: `maxsize = 5147` when `real_max_memuse` is 0).
- I ran its test_lower, test_upper and test_capitalize for str, bytes and bytearray on ~/abench/g2-varY/python, where the macro is defined. All 9 ran and passed; none was skipped.
- These tests do reach the vector path:
  - 'A'*5147 lower and 'a'*5147 upper, checking every byte. 5147 % 16 = 11, so the last 16-byte block overlaps.
  - bytes/bytearray capitalize of '-'*5147 + ' abc def ghi', which calls `_Py_bytes_lower(result+1, s+1, 5158)` from an unaligned start.
- They catch gross breakage of the vector path. In the harness they fail when the tail is omitted, when the stride is 32, and when the first block is skipped.
- So the vector loop, its tail and unaligned starts do have some in-tree coverage. What is missing is coverage of the boundary bytes, of tail placement at lengths ≡ 0 mod 16, and of the high-bit look-alikes.

Not verified:
- Whether some unrelated test in the full suite would catch the reviewer's two mutants by accident. Checking that needs mutant builds and a full test run, which this task's limits forbid. The finding already says such catches would be "by accident".
- Whether any CI or buildbot runs a 4-lane build (ARM32 with NEON, or x32). I could not check this offline.

Context:
- The boundary-byte gap also exists in the PR's word loop as it stands. Only the vector-path and 4-lane parts are specific to varY.
- The suggested test (lengths 0..40, the boundary and look-alike bytes, a translate() reference, `del ba[:k]` for unaligned starts, and capitalize) would catch every mutant above.
- Severity is minor: this is a coverage gap, not a bug.

## 2. ASCII_CASE_MEMCPY hunk does nothing on platforms that have the vector path; its macOS comment is misleading

**Claim.** The comment at lines 260-261 justifies __builtin_memcpy with macOS's default _FORTIFY_SOURCE. But macOS x86-64 and arm64 builds define _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR. There, anything >= 16 bytes takes the explicit vector path, which stays SIMD with plain fortified memcpy. The word loop then handles only 8..15 bytes, which is at most one iteration. So on macro platforms the hunk only re-enables clang's auto-vectorized copy of that loop, and that copy can never run. The hunk only matters for clang + fortify on platforms without the macro (riscv64, ppc64le, s390x, i686, ARM32 without NEON). It removes no runtime check.

**Evidence.** I made a copy of varY with ASCII_CASE_MEMCPY forced back to memcpy and compiled it with -D_FORTIFY_SOURCE=2/3. Result for ascii_case_words: 'clang FORTIFY=2 varY-with-plain-memcpy: memcpy_chk=0 calls=0 xmm=29 movdqu/movups=4 insns=121'. gcc gives xmm=33. The PR's word loop under clang fortify is scalar (xmm=0), and neither the PR nor varY has any __memcpy_chk call ('memcpy_chk calls=0' in all 8 gcc/clang x FORTIFY 2/3 x PR/varY builds). So __builtin_memcpy drops no fortify check.

**Suggestion.** For a minimal change (AGENTS.md), drop the ASCII_CASE_MEMCPY hunk from varY. Or keep it with the comment reworded to name the case it affects: clang with _FORTIFY_SOURCE on targets without the vector path.

**Verifier (refuted, info).** The finding's main claim is that on platforms with the vector path, the hunk does nothing except add an auto-vectorized copy of the word loop that can never run. That is wrong on x86-64, the most common platform with the macro. It is right on arm64.

1. **x86-64, clang 18, fortify on.** I checked both glibc's inline-wrapper fortify and the macOS SDK's macro form (`#define memcpy(d,...) __builtin___memcpy_chk(d,...,__builtin_object_size(d,0))`). The hunk changes the live loop for len >= 16.
   - With `__builtin_memcpy` (varY as written), clang unrolls the 16-byte vector loop 2x (`addq $32`).
   - With plain fortified memcpy, the loop is not unrolled (`addq $16`). At `_FORTIFY_SOURCE=0`, plain memcpy gives the same code as varY. So fortify is what stops the unroll: the `__memcpy_chk` call is still in the loop when the unroller runs, and it is folded away only later.
   - Both versions are SIMD, and neither has a `__memcpy_chk` call. The finding's own numbers (121 vs 165 instructions) include this unroll, not just dead code.
   - llvm-mca-18 static estimate in cycles per 16 bytes, unrolled vs not unrolled: znver3/znver4 2.26 vs 2.52 (about 10% better unrolled); skylake 3.34 vs 3.35 and alderlake 2.68 vs 2.69 (no difference). This is a model, not a measurement. Timing runs were not allowed.
   - So on x86-64 Linux with clang+fortify, and on Intel macOS, the hunk changes the hot path. Dropping it would undo the unroll.
2. **arm64 (Apple and Linux targets).** The finding holds exactly. The live 16-byte NEON loop is byte-identical with or without the hunk. The only difference is an auto-vectorized word loop that runs only for len >= 65, which can't happen after the len >= 16 return. On arm64 macOS, the comment's named case, the hunk adds dead code only.
3. **ARM32 with NEON.** Here size_t is 4 bytes, so the word loop covers 4..15 bytes and runs up to 3 times, not "at most one iteration" as the finding says. The vectorized copy is still unreachable (it needs len >= 17). With the hunk, the live vector loop differs only in register names, and the prologue saves 2 more registers (r9, r10).
4. **gcc 13 (fortify 2 and 3, -O2 and -O3).** Same instruction count either way; only register allocation differs. The hunk has no real effect under gcc.
5. **"Removes no runtime check."** Confirmed: no `__memcpy_chk` appears in any build.

What survives from the finding: the comment at lines 260-261 is misleading. It credits the hunk with letting clang vectorize the word loop under macOS fortify. On macro platforms that loop never runs vectorized. The hunk's real effect there is the 2x unroll of the 16-byte vector loop on x86-64, and nothing on arm64. Rewording the comment is still worthwhile. Dropping the hunk "for a minimal change" is not justified by "does nothing", because it would remove the x86-64 unroll.

## 3. clang emits an unreachable auto-vectorized copy of the word loop for 8..15 bytes

**Claim.** When the macro is defined, ascii_case_words reaches the word loop only for len <= 15. clang does not use that range: it emits a 2x16-byte vectorized version of the word loop whose entry test can never pass. That is about 35 dead instructions in a hot function. The cause is keeping the loop, not __builtin_memcpy: the build without fortify has it either way (165 instructions in both cases). gcc sees the range and emits straight-line code (one optional word plus the tail word).

**Evidence.** clang -O2 varY ascii_case_words, branch .LBB8_1 (len <= 15): 'addq $-9, %rdx ; cmpq $24, %rdx ; jb .LBB8_7'. This always jumps to the scalar loop because len-9 <= 6, so the paddq/movdqu body at .LBB8_5 is unreachable. In the gcc -O2 asm the len <= 15 branch is just two scalar word blocks with no loop.

**Suggestion.** Optional. When the macro is defined and SIZEOF_SIZE_T == 8, handle 8..15 bytes as 'if (len > 8) ascii_case_word(result, cptr, 0, ge, gt); ascii_case_word(result, cptr, len - 8, ge, gt);' and keep the loop for other builds. ARM32 and x32 have 4-byte words and still need the loop for 4..15 bytes.

**Verifier (confirmed, info).** I couldn't refute this. The finding holds, though two of its details are slightly off.

In varY's ascii_case_words, the 16-byte block returns whenever len >= 16. When _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR is defined, the word loop and the final ascii_case_word therefore only ever see len 8..15. clang 18 doesn't use that range and still loop-vectorizes the word loop.

In the clang -O2 asm, the len <= 15 path goes: `cmpq $9,%rdx; jl .LBB8_8` (len < 9 skips to the tail word), then `addq $-9,%rdx; cmpq $24,%rdx; jb .LBB8_7`. On this path len is 9..15, so len-9 is 0..6, which is below 24 unsigned, and the jump to the scalar loop is always taken. Blocks %bb.3 to %bb.6 can never run: the alias check, the vector setup, the 2x16-byte paddq/movdqu loop at .LBB8_5 and the remainder test.

Corrections:
1. The dead code is 45 instructions, not "about 35". The 4-instruction entry test does execute.
2. "Not __builtin_memcpy" is only true without fortify. Without fortify the count is 165 whether varY uses `__builtin_memcpy` or plain `memcpy`. With -D_FORTIFY_SOURCE=2, plain memcpy gives 121 instructions and no dead loop, but only because fortify blocks vectorization entirely, which is what varY's `__builtin_memcpy` is there to undo.

The dead block is never executed, and the len <= 15 path jumps over it, so the cost is code size only. "info" is the right severity.

The gcc part of the finding is also right. gcc 13 at -O2 and -O3 emits straight-line code for len <= 15 (an optional word at 0, then the word at len-8), with no loop, 90 instructions.

The suggested change works. Replacing the len <= 15 code with `if (len > 8) word(0); word(len-8); return;` (under the macro and `SIZEOF_SIZE_T == 8`) cuts clang's ascii_case_words from 165 to 110 instructions with no dead loop, at -O2, -O2 with fortify, and -O3. It compiled cleanly with -Wall. I did not run a correctness test on that change, but by inspection it covers bytes 0..len-1 for every len from 8 to 15.

## 4. Comment at lines 280-281 overstates: clang -O2 does vectorize the word loop

**Claim.** 'Compilers leave a loop over single words scalar at -O2' is true for gcc, but not for clang without fortify. The accurate statement: gcc at -O2, clang under _FORTIFY_SOURCE, and PGO builds whose training finds the loop cold.

**Evidence.** PR file compiled with _FORTIFY_SOURCE undefined, xmm uses in ascii_case_words: 'PR gcc -O2: xmm=0', 'PR gcc -O3: xmm=19', 'PR clang -O2: xmm=30', 'PR clang -O3: xmm=30'. PR clang -O2 with FORTIFY=2/3: xmm=0.

**Suggestion.** Reword to something like: 'gcc leaves a loop over single words scalar at -O2, as does clang under _FORTIFY_SOURCE and PGO builds that find it cold.'

**Verifier (confirmed, info).** The finding holds, and the comment is more wrong than the finding says. The comment is varY bytes_methods.c lines 279-281: "Compilers leave a loop over single words scalar at -O2, and in PGO builds whose training finds it cold." That is true only for gcc.

1. **gcc:** gcc 13 at -O2 leaves the word loop scalar (xmm=0). gcc -O3 vectorizes it (xmm=19). _FORTIFY_SOURCE makes no difference to gcc.

2. **clang:** clang 18 at -O2 vectorizes the word loop on every target I tried: x86-64 (SSE2, 2x16 B per iteration), aarch64 Linux and arm64-apple-macos (NEON, 4x16 B). The loop gets a runtime check for length and for overlap between source and destination, so it only goes SIMD above about 33 bytes on x86-64 and about 65 on arm64. Shorter strings still run the scalar loop. The comment does not say any of this; it says the loop is scalar outright.

3. **The PR file reproduces the reviewer's numbers exactly.** It uses plain memcpy. clang -O2/-O3 give xmm=30 with fortify off and xmm=0 with -D_FORTIFY_SOURCE=2 or 3.

4. **The suggested rewording is wrong for varY.** varY sets ASCII_CASE_MEMCPY to __builtin_memcpy under gcc/clang, which gets around fortify. Its word loop (compiled with the macro removed from pyconfig.h) vectorizes under clang -O2 at FORTIFY=U, 2 and 3 (xmm=30 each time). So "clang under _FORTIFY_SOURCE" leaves the loop scalar only in the PR, not in varY. varY's own comment at lines 260-261 even says the __builtin_memcpy change exists so clang can vectorize the word loop, which contradicts lines 280-281.

For varY the accurate wording is roughly: "gcc leaves a loop over single words scalar at -O2, and so do PGO builds whose training finds it cold; clang only vectorizes it for longer strings." The PGO part was not tested here. This is a comment-accuracy issue only, with no effect on behaviour, so severity info is right.

## 5. varY reuses the pystrhex macro without updating its configure comment, and relies on vector features the probe does not test

**Claim.** configure.ac:5492-5494 says the macro is 'Used for SIMD-accelerated bytes.hex() in Python/pystrhex.c'. varY makes bytes_methods.c depend on it too. varY also mixes vector and scalar operands (x & (0x7f*ones), '>> 2', and the '(ascii_case_vec){0} + ge' broadcast) and uses a vector of size_t. The configure probe tests neither. pystrhex.c avoids mixing: it uses explicit splat helpers and vector-vector ops only. Today every compiler that passes the probe (gcc >= 12, which added __builtin_shufflevector, and clang) supports these, so there is no current bug. It is only a coupling: if the probe changes, varY changes with it silently.

**Evidence.** configure.ac:5492-5525. Python/pystrhex.c:50-60 (v16u8_splat) and :81 '(data >> four) & mask_0f'. My splat test printed correct lanes on gcc 13 and clang 18: 'lanes=2 vge[i]=3f3f3f3f3f3f3f3f vgt[i]=2525252525252525 m>>2=2020202020202020' for 8-byte size_t, and 4 lanes of 3f3f3f3f/25252525/20202020 for 4-byte size_t.

**Suggestion.** Add 'and ASCII lower()/upper() in Objects/bytes_methods.c' to the configure.ac comment (and regenerate nothing else). Optionally note in bytes_methods.c that the macro implies gcc >= 12 or clang, which is what makes the vector-scalar operators safe.

**Verifier (confirmed, info).** I could not refute any factual part of the finding.

(1) The configure.ac comment (lines 5493-5495; the finding says 5492-5494, one line off) says the macro is "Used for SIMD-accelerated bytes.hex() in Python/pystrhex.c". varY.patch changes only Objects/bytes_methods.c, so after varY that comment is out of date.

(2) The probe compiles only a v16u8 initializer and one __builtin_shufflevector call. It does not test a size_t vector or any operation that mixes a vector with a scalar.

(3) varY does mix them: `x & (0x7f * ones)`, `>> 2`, `& (0x80 * ones)` and `(ascii_case_vec){0} + ge`.

(4) pystrhex.c does avoid mixing. It builds its constants with the v16u8_splat/v16s8_splat helpers and uses only vector-vector operations, e.g. `(data >> four) & mask_0f`.

(5) No current bug. varY compiles cleanly with gcc 13 and clang 18 under -Wall -Wextra -Wpedantic; the only warnings are pre-existing ones near lines 501 and 730 and in the included stringlib code. A standalone test of the size_t-vector operations gave the expected lanes on both compilers. GCC added __builtin_shufflevector in version 12 and has long accepted vector-scalar operands, so on every compiler I can test, the claim that anything passing the probe supports these operations holds. So the finding is a correct documentation and coupling note, and info is the right severity.

One correction to the suggestion, not the claim: "regenerate nothing else" is wrong. Autoconf copies `#` comments from configure.ac into the generated configure script; the same comment is at configure:20321. Editing it in configure.ac therefore also requires `make regen-configure`. Otherwise the "Check for changes" step in .github/workflows/build.yml, which flags out-of-date generated files, would fail.

## 6. Residual risk: not executed on real ARM32/aarch64/big-endian hardware

**Claim.** WSL has no qemu-user, no ARM gcc cross compiler, and no -m32 multilib. I checked ARM32 NEON, aarch64, aarch64_be, armv8 big-endian and x32 by clang cross-compiling and reading the asm. I covered the 4-lane semantics by running the same code on x86-64 with size_t mapped to uint32_t. I did not check gcc's ARM32 code generation or any -Wpsabi notes it might print in Py_DEBUG builds, where the vector arguments of ascii_case_vec16 are not force-inlined.

**Evidence.** 'which qemu-arm qemu-arm-static arm-linux-gnueabihf-gcc' found nothing. 'gcc -m32' fails with 'cannot find Scrt1.o'. clang --target=aarch64-linux-gnu_ilp32 is rejected by clang 18 (data layout error).

**Suggestion.** If the Raspberry Pi or ARM CI buildbots run the suggested regression test, this gap closes. Alternatively, run vy_test.c with -DVEC under qemu-arm with an armhf gcc.

**Verifier (confirmed, info).** I couldn't refute this. The gap the finding describes is real: nothing on this machine can run ARM code, and there's no gcc for ARM. I narrowed the gap, though, and the leftover risk is small.

Premises (checked):
- WSL has no qemu-*, no arm/aarch64 gcc, and no /usr/lib/gcc-cross. binfmt_misc holds only WSLInterop, llvm-18-runtime and python3.12 handlers, and the docker-desktop distro has the same list.
- Windows has no ARM gcc and no qemu. Python has capstone, which only disassembles; unicorn isn't installed.
- Docker Desktop 29.9.2 is installed and running, but it has no local images and no qemu binfmt handler. Running an ARM container would mean pulling an image, which is a download I'm not cleared to make. With the user's OK, a `--platform linux/arm/v7` or `linux/arm64` gcc container could close the gap on this PC.

What narrows the risk:
1. **Byte order and lane width can't matter.** Each byte is computed on its own with no carry: b <= 0x7f, so b+ge <= 0xbe ('A') or 0x9e ('a'), and b+gt <= 0xa4 or 0x84. I wrote a standalone check of the varY vec16 expression with 4x32 and 2x64 lanes, each in little-endian and in big-endian lane order (simulated with bswap). It tried every adjacent byte pair at every position, with three fill values, for both 'A' and 'a': 377,487,360 checks, 0 failures. Any remaining ARM/BE risk lies in the compiler's code generation, not the algorithm.
2. **Py_DEBUG diagnostics.** Py_ALWAYS_INLINE is empty under Py_DEBUG (pyport.h:338-343), so ascii_case_vec16 becomes a real function taking vector arguments.
   - x86-64: the full varY bytes_methods.c with -DPy_DEBUG, under gcc 13 and clang 18 at -O0, -Og and -O2 with -Wpsabi, gives no diagnostics in lines 245-380.
   - ARM, clang 18 only: armv7 NEON (hard and softfp), armebv7, aarch64 and aarch64_be at -O0 and -Og give no diagnostics, and at -O0 vec16 is a real out-of-line function.
   - gcc for ARM32/aarch64 is still untested. From memory of GCC's arm.cc and aarch64.cc (not verified here), the ABI notes there are about aggregates, over-aligned or bit-field members, C++17 empty bases and (aarch64) enums. For a non-aggregate vector, arm_needs_doubleword_align uses the TYPE_MAIN_VARIANT alignment and can't produce the "changed in GCC 7.1" note. Those notes are inform() calls, so they can't fail a -Werror build. The function is also static, so no ABI crosses the file.
3. **CI and real-world reach.**
   - CPython's own CI runs ubuntu-26.04-arm with `--with-pydebug` and a compiler-warning check, plus the full test suite. If varY goes into the PR, aarch64 gcc in Py_DEBUG gets built and run automatically.
   - Not covered by CI: gcc on ARM32 with NEON, and big-endian. The configure check requires __ARM_NEON on ARM32, which the default armhf flags of Debian (vfpv3-d16) and 32-bit Raspberry Pi OS (armv6) don't turn on. Only an explicit -mfpu=neon or -march=native build reaches that path.
   - pystrhex.c already returns 16-byte vectors from static inline functions that aren't force-inlined (v16u8_splat) under the same macro. That covers vector returns but not vector arguments.

Bottom line: the finding is accurate as an info-level note about untested platforms. What actually remains is gcc's ARM32-NEON and big-endian code generation, which nothing here can run.

## 7. The gate lets in clang < 5, which cannot compile varY's vector-plus-scalar operations

**Claim.** The configure check only proves that __builtin_shufflevector exists, and clang has had that builtin since about 2.x/3.0. varY's vector code mixes a GNU vector with a scalar at varY lines 291 (`x & (0x7f * ones)`), 292 (`... & (0x80 * ones)`, `>> 2`) and 309-310 (`(ascii_case_vec){0} + ge`). Clang only gained GCC-compatible scalar-to-vector splats in D25866 (r302935, May 2017, so clang 5.0). Before that it rejected these with 'cannot convert between vector values of different size'. A clang 3.x/4.x build on x86-64 or aarch64 would pass configure and then fail to compile bytes_methods.c. CPython only documents 'a C11 compiler' (Doc/using/configure.rst:15), so no rule excludes those versions. The existing user of this macro, Python/pystrhex.c, avoids the issue: it builds splats from explicit initializers (v16u8_splat / v16s8_splat, lines 50-60) and shifts vector by vector (`data >> four`).

**Evidence.** I could not test old clang (WSL only has gcc 13.3 and clang 18.1.3). D25866 changed vector-cast.c, whose old expectation was `f2 += d;` -> 'cannot convert between vector values of different size'. Its FIXME says scalar splatting 'should also work for regular vector types as supported in GCC'. Under clang 18 the code is clean, including -flax-vector-conversions=none. GCC is not at risk here: the macro needs GCC >= 12, and GCC has had vector-scalar operations since 4.7 (gcc-4.7/changes.html: 'it is possible to replace the vector with the generating element').

**Suggestion.** Build the constants without vector-scalar operations, the way pystrhex.c does. Add a splat helper, e.g. `#if SIZEOF_SIZE_T == 8  (ascii_case_vec){x, x}  #else  (ascii_case_vec){x, x, x, x}`. Splat 0x7f*ones and 0x80*ones once in ascii_case_words and pass them in. Shift by a splatted 2, or replace `(... & 0x80s) >> 2` with `& 0x20s` applied after the shift. Any clang that passes the configure check then compiles the code.

**Verifier (confirmed, minor).** I could not refute the finding, and its core premise checks out against clang's own source.

1. The gate does not exclude old clang. The configure.ac check (lines 5496-5526) tests only the target architecture, then links a `__builtin_shufflevector` call on `v16u8` GNU vectors. clang has had that builtin for many years. There is no compiler-version check, so clang 3.x/4.x on x86-64, aarch64, or ARM32 with NEON would define `_Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR`.

2. clang 4.x rejects GNU-vector-with-scalar `&` and `+`. I read `Sema::CheckVectorOperands` in release/4.x `clang/lib/Sema/SemaExpr.cpp`. Its scalar splat is guarded by `if (!RHSVecType && isa<ExtVectorType>(LHSVecType))` and the mirror case. The FIXME directly above it reads: "this should also work for regular vector types as supported in GCC." The only other route is the lax-conversion block, which requires the scalar and the vector to have the same total size. A 64-bit (or 32-bit on ARM32) `size_t` never matches a 16-byte vector, so the code reaches `err_typecheck_vector_not_convertable`. In release/5.x the same function has a new `else` branch calling `tryGCCVectorConvertAndSplat` for non-ext vectors, which is D25866, shipped in clang 5.0.

3. varY depends on exactly that splat. A clang-18 AST dump of varY's vector code shows `<VectorSplat>` implicit casts on the GNU vector type for `(ascii_case_vec){0} + ge`, `+ gt` (lines 309-310), `x & (0x7f * ones)` (line 291) and `& (0x80 * ones)` (line 292). These are the operations clang 4.x lacks, so clang < 5 would pass configure and then fail on bytes_methods.c. pystrhex.c, the existing user of the macro, avoids the problem: it builds splats with explicit initializers and only combines vectors with vectors.

One inaccuracy in the finding: the `>> 2` shift is not a problem. In clang 4.x, `checkVectorShift` already splats a scalar shift amount for any vector type ("...else expand RHS to match the number of elements in LHS", `CK_VectorSplat`), with no OpenCL gate. So the suggestion to rework the shift is unnecessary for clang 4. Only the splats for `+ ge`, `+ gt`, `& 0x7f*ones` and `& 0x80*ones` need explicit initializers, e.g. `(ascii_case_vec){x, x}` when `SIZEOF_SIZE_T == 8`, else four elements.

Severity stays minor. clang 4 dates from 2017. CPython names no minimum clang version, and I did not establish whether clang 4 can build the rest of current main. mimalloc headers still carry `__clang_major__ < 4` handling, so very old clang is not formally excluded. GCC is unaffected: the macro needs GCC >= 12, and GCC has supported vector-scalar operations since 4.7.

## 8. Reusing the shufflevector macro shuts out GCC 4.7-11, so the stated gcc -O2 motivation goes uncovered on many current LTS distros

**Claim.** Under GCC, _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR is defined only from GCC 12 on, because GCC 12 added __builtin_shufflevector and the check uses AC_LINK_IFELSE on a program that calls it. varY needs only vector_size, vector-scalar operations (GCC 4.7+) and a SIMD architecture, and never calls __builtin_shufflevector. GCC 8-11 therefore fall back to the PR's word loop, which is scalar at -O2 (GCC < 12 does not enable -ftree-vectorize at -O2 at all). Affected builds include RHEL 8 (gcc 8), RHEL 9, Amazon Linux 2023 and Ubuntu 22.04 (gcc 11), Debian 11 and manylinux2014 devtoolset (gcc 10). This is not a regression against the PR; those builds just get none of varY's benefit.

**Evidence.** GCC 12 release notes: 'Support for `__builtin_shufflevector` compatible with the clang language extension was added.' The check is configure.ac:5493-5526 (AC_LINK_IFELSE over a test program calling __builtin_shufflevector). On older GCC the call is an implicit int-returning function assigned to a v16u8, which fails to compile or link, so the result is 'no'.

**Suggestion.** If varY is adopted, gate it with a preprocessor test in bytes_methods.c instead of the configure macro, e.g. `#if (defined(__GNUC__) || defined(__clang__)) && (defined(__x86_64__) || defined(__aarch64__) || (defined(__arm__) && defined(__ARM_NEON)))`. If the scalar operations are kept, also require GCC >= 4.7 / clang >= 5. With explicit splats (previous finding) no version test is needed.

**Verifier (confirmed, info).** I could not refute the mechanism.

1. The gate. configure.ac:5493-5526 sets _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR only if AC_LINK_IFELSE succeeds on a program that calls __builtin_shufflevector. GCC added that builtin in GCC 12 (PR c/88601, listed in the GCC 12 release notes). Without it the test cannot compile: the call becomes an implicit int-returning function, and assigning int to v16u8 is a hard error. I reproduced that failure mode with gcc 13 by renaming the builtin, so the check returns "no" on GCC up to 11. Clang has always had the builtin, so clang builds are unaffected.

2. varY's vector code. The vector path (ascii_case_vec16 and the splats in ascii_case_words) never calls __builtin_shufflevector. It uses only vector_size(16), vector-with-scalar arithmetic, bitwise ops and >>. That support is in GCC long before 12. I can't confirm the exact first version (4.7) without an old compiler, but GCC 8 and later certainly have it.

3. The fallback is scalar at -O2. GCC before 12 does not turn on -ftree-vectorize at -O2 (GCC 12 made it the default with the very-cheap cost model). I mimicked that with gcc 13 -O2 -fno-tree-vectorize on varY's bytes_methods.c:
- With the macro defined, ascii_case_words still has 33 xmm instructions. Explicit vectors don't need the auto-vectorizer.
- With the macro removed, it has 0, both at plain -O2 and without the vectorizer. So even gcc 13 leaves the PR's word loop scalar at -O2.
So GCC 8-11 builds at -O2 (or with a cold PGO profile) get none of varY's benefit, while a preprocessor gate would have given them SIMD. pystrhex.c already has the same gap.

Why only info, not minor: the practical impact is overstated. Main is 3.16 (patchlevel.h), released around Oct 2027. Several distros on the list won't ship it at all: Debian 11 (LTS ends Aug 2026), Ubuntu 22.04 (standard support ends Apr 2027) and RHEL 8. manylinux2014's interpreters are build tools whose speed doesn't matter. Distros that will package 3.16 at -O2 (Debian 13/14, Ubuntu 24.04+, Fedora, RHEL 10) use GCC 12 or newer, where the macro is defined. From-source builds use CPython's default OPT of -O3, so the "-O2" case there needs explicit flags. The cases that are plausibly left are app-stream Pythons built with gcc 11 (Amazon Linux 2023, maybe RHEL 9) and PGO builds from source on gcc 8-11 hosts.

It is not a regression against the PR, and the finding says so itself. Its suggestion is sound if broader coverage is wanted, but reusing the configure macro is a deliberate trade-off: it keeps varY consistent with pystrhex.c.

## 9. The macro's name, description and configure comment do not match this use, and lower()/upper() become tied to a check owned by bytes.hex()

**Claim.** The macro is technically a usable proxy: its #error part (x86-64, aarch64, or ARM32 with NEON) is exactly the 'native 128-bit SIMD' condition varY wants. Its other part, that __builtin_shufflevector exists, has nothing to do with varY. It is too strict for GCC and too loose for old clang (findings above). The documentation is also stale. configure.ac:5495 says 'Used for SIMD-accelerated bytes.hex() in Python/pystrhex.c.' pyconfig.h.in:2145 describes __builtin_shufflevector. varY's comment at lines 279-281 doesn't explain why a shufflevector macro gates code with no shuffles. If someone later narrows the check for a shuffle-specific reason (a __builtin_shufflevector codegen bug, a new arch condition), str/bytes lower()/upper() would change silently.

**Evidence.** varY.patch changes only Objects/bytes_methods.c. Running grep for 'shufflevector' in varY's code finds only the two #ifdef lines (278, 307) and no call. The macro is defined only by configure: the only hits are configure.ac:5493-5526 and pyconfig.h.in:2145-2147, with none in PC/, Include/, Android/, iOS/, Apple/, Platforms/, Tools/ or Mac/.

**Suggestion.** Prefer a local preprocessor gate, which needs no configure dependency (see the previous finding). If the macro is kept, add a one-line comment at varY line 278 explaining the reuse, and update the configure.ac:5495 comment to list bytes_methods.c as a user.

**Verifier (confirmed, minor).** I checked each factual premise and found no mistake.

1. varY's code never calls __builtin_shufflevector. A grep of varY's bytes_methods.c finds the name only on the two `#ifdef _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR` lines (278 and 307). The gated code uses only GNU vector_size arithmetic: `&`, `~`, `+`, `>>` and a splat through `(ascii_case_vec){0} + ge`. So the "__builtin_shufflevector exists" half of the configure probe has nothing to do with varY. Only the `#error` arch filter (x86-64, aarch64, or ARM32 with NEON) matches what varY needs.

2. The documentation is stale exactly as stated. configure.ac:5495 says "Used for SIMD-accelerated bytes.hex() in Python/pystrhex.c." The AC_DEFINE text at configure.ac:5523-5525 and pyconfig.h.in:2145-2146 both describe __builtin_shufflevector support. varY.patch touches only Objects/bytes_methods.c, so none of this is updated. varY's comment at 279-281 says "(SSE2 or NEON)" but never explains why a shuffle macro gates code with no shuffles.

3. The macro comes only from configure. `git grep -i shufflevector` (excluding the generated configure) finds only configure.ac, pyconfig.h.in and Python/pystrhex.c. Nothing in PC/ or Include/ defines it. pystrhex.c is its only other user, and it does call __builtin_shufflevector (lines 99 and 101). So lower()/upper() really do become tied to a check that bytes.hex() owns.

4. The coupling risk is real, but its effect is performance only. If the check is narrowed (or widened), varY falls back to (or newly takes) the vector path. The PR's word loop is still there after the #ifdef block, so output is unchanged and no test would notice. "Change silently" is therefore accurate in the sense of a silent speed regression, not a correctness bug. That fits severity minor, bordering on info.

5. "Too strict for GCC" is plausible from what I know: GCC added __builtin_shufflevector in GCC 12, so GCC 11 and older on x86-64 fail the probe even though they support varY's vector_size ops. I could not test this, because WSL has only gcc 13 and clang 18. I did not re-check the "too loose for old clang" point; it comes from a separate finding.

The suggested fix is cheap and correct: add a one-line comment at line 278 explaining the reuse and add bytes_methods.c to the configure.ac comment, or use a local preprocessor gate instead.

## 10. ASCII_CASE_MEMCPY no longer serves its stated purpose wherever the vector path is on, and makes clang emit about 230 bytes of unreachable vector code

**Claim.** The comment at varY lines 260-261 justifies __builtin_memcpy by the macOS SDK's _FORTIFY_SOURCE. But every macOS build (Apple clang on arm64, x86_64 and universal2) defines the macro, so it takes the explicit-vector path, and that path stays SIMD under fortify even with plain memcpy. In those builds the word loop handles only 8..15 bytes, so it runs at most once. With __builtin_memcpy, clang still auto-vectorizes that loop, with runtime trip-count and alias checks that need len >= 33, so the vector body can never run. The result is dead code that grows ascii_case_words. The same happens on x32: 4-byte words, loop over 4..15 bytes, vectorized by clang. GCC is unaffected. Where it does help is clang plus fortify on architectures that lack the macro (Linux clang on i686, ppc64le, s390x, riscv64).

**Evidence.** clang 18 -O3 -D_FORTIFY_SOURCE=2, macro on: with __builtin_memcpy, ascii_case_words is 0x2cf bytes with 83 xmm instructions; with plain memcpy it is 0x1e8 bytes with 29 xmm instructions, still SIMD. Macro off with plain memcpy: 0 xmm, which is the PR problem varY fixes. In the built objects, cf-varY's ascii_case_words is 0x2e0 bytes and cf-PR's is 0x129. Disassembly of the macro-on path: after `cmp $0xf,%rdx; jle` (len <= 15) comes `add $-9,%rdx; cmp $0x18,%rdx; jb scalar` and then a 4-word vector loop, so it needs len - 9 >= 24. With gcc -O2/-O3, builtin vs plain memcpy gives identical xmm counts (33/33 and 33/33 macro on; 0/0 at -O2 and 19/19 at -O3 macro off).

**Suggestion.** In the vector build, handle 8..15 bytes without a loop: two overlapping words (`ascii_case_word(result, cptr, 0, ...)` and `ascii_case_word(result, cptr, len - SIZEOF_SIZE_T, ...)`) when size_t is 8 bytes, and up to four words when it is 4. Otherwise, limit __builtin_memcpy to builds without the vector path. Either way, reword the comment, since its macOS rationale no longer applies under varY.

**Verifier (confirmed, minor).** I couldn't refute it. Every factual claim reproduced, including on arm64 macOS, the target the comment names.

1. **Macro coverage.** The configure.ac check (lines 5505-5506) passes for `__x86_64__` or `__aarch64__`. Clang defines `__x86_64__` on x32 too, which I checked with `clang --target=x86_64-linux-gnux32 -dM -E`: it gives `__x86_64__=1`, `__ILP32__=1` and a 4-byte size_t. So Apple arm64, x86_64 and universal2 builds (both slices pass) take the vector path.

2. **Word loop on 8..15 bytes is vectorized but can never run.** Under the macro, the word loop only sees len <= 15. With `__builtin_memcpy`, clang 18 still auto-vectorizes it, and the vector body sits behind guards that can never pass:
   - x86-64: `add $-9; cmp $0x18; jb scalar`, so it needs len >= 33.
   - arm64-apple-macos: `subs x12,len,#9; cmp x12,#0x38; b.lo scalar`, so it needs len >= 65. This is an 8-word body (`ldp q4,q5 / ldp q6,q7`).
   - x32: `addl $-5; cmpl $0x1c`, so it needs len >= 33.

   In all three cases the body is unreachable.

3. **Plain memcpy under fortify.** The 16-byte vector path stays SIMD with no calls, and the word loop goes scalar. So in vector builds, the comment's reason for `__builtin_memcpy` (letting clang vectorize the word loop) no longer applies.

4. **GCC is unaffected.** `__builtin_memcpy` and plain memcpy give the same size and xmm counts at -O2 and -O3, macro on or off.

Two corrections to the evidence. Neither changes the conclusion.

- **The ~230 bytes is not all dead code on x86-64.** The 0xe7-byte gap between the two versions mixes three things:
  - about 0xcd bytes of unreachable vector word loop (0x441-0x50e);
  - a 2x unroll of the 16-byte vector loop, which is live for len >= 33. Clang does this unroll with `__builtin_memcpy` (fortify or not) but not with plain memcpy under fortify;
  - a 2x-unrolled scalar word loop in the plain version that is also dead (it needs len-9 >= 8).

  On arm64 the whole gap of 224 bytes (512 vs 288) is dead code, and the 16-byte loop is identical in both versions.

- **`__builtin_memcpy` still has one side effect in vector builds.** On x86-64 under fortify, it enables that 2x unroll of the 16-byte loop, whose speed effect is untested. The finding's second option, limiting `__builtin_memcpy` to builds without the vector path, would drop the unroll on x86-64 clang+fortify builds, Intel macOS included. The first option, two overlapping words with no loop for 8..15 bytes, avoids that. It also removes the dead code under either memcpy.

On severity: the dead code is never executed and lives in a function that is not inlined, so the cost is about 200 bytes of code size plus a misleading comment. Minor, close to info.

## 11. Windows (MSVC and clang-cl) never get the vector path, so a Windows PGO build that finds the loop cold is not fixed

**Claim.** The macro comes only from configure; PC/pyconfig.h does not define it. MSVC can't use GNU vectors anyway. clang-cl builds (PlatformToolset=ClangCL) also miss the path, although clang-cl defines __clang__ and __x86_64__/__aarch64__ and compiles varY's vector code fine. If the 'PGO training rarely runs the loop' motivation holds, it applies equally to the python.org Windows installers (MSVC PGO, where cold code is optimized for size), and varY leaves those unchanged.

**Evidence.** PC/pyconfig.h has no match for 'SHUFFLEVECTOR'. For x86_64-pc-windows-msvc clang predefines `_MSC_VER 1933`, `__clang__ 1`, `__x86_64__ 1`; for aarch64-pc-windows-msvc, `__aarch64__ 1` and `__ARM_NEON 1`. The varY kernel compiled with `clang --target=x86_64-pc-windows-msvc -fms-compatibility -fms-extensions -O2` gave rc=0 and 91 xmm instructions; aarch64-pc-windows-msvc gave rc=0 and 42 NEON v-register instructions.

**Suggestion.** Either say in the PR that the vector path is configure-only, or use a preprocessor gate that also covers clang-cl. MSVC itself stays on the count-by-one loop.

**Verifier (confirmed, info).** I checked every factual part of the finding and found no wrong premise.

1) The macro only comes from configure. In the checkout, _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR appears only in configure.ac:5522, configure, pyconfig.h.in and Python/pystrhex.c. PC/pyconfig.h, PCbuild/pyproject.props, pyproject-clangcl.props and pythoncore.vcxproj never define it, so no PCbuild build gets it, under either MSVC or ClangCL.

2) varY gates the vector path only on that macro (varY bytes_methods.c lines 278 and 307). The count-by-one loop is gated on `defined(_MSC_VER) && !defined(__clang__)` (line 318). So MSVC keeps the PR's count-by-one loop. clang-cl gets the generic word loop, with no 16-byte vector path.

3) clang-cl could use the path. I ran the real clang-cl 22.1.3 from VS 18 on varY's actual bytes_methods.c with PC/pyconfig.h. The macro dump shows `__clang__ 1`, `_MSC_VER 1951`, `__x86_64__ 1`, `__SSE2__ 1`, `MS_WINDOWS` and no SHUFFLEVECTOR macro. With -D_Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR added, the whole file still compiles with rc=0. ascii_case_words then contains a 16-byte SSE2 loop (movdqu/pand/paddq/pandn/psrlq/pxor, unrolled 2x). For --target=aarch64-pc-windows-msvc, clang-cl predefines `__aarch64__ 1`, `__ARM_NEON 1` and `__clang__ 1`, which matches the reviewer's evidence. The configure check's own architecture test (x86_64, aarch64, or arm with NEON) would pass on those targets.

4) The MSVC PGO point: the PR's own comment ("Dividing unsigned avoids an idiv in code optimized for size") and the session's measurement note (MSVC /O1 /Oi reproduced the real PGO-cold loops) support the claim that MSVC PGO compiles this loop for size when it is cold. The finding only says that if the PGO-cold motivation holds, varY doesn't help the python.org MSVC installers. That is true: varY leaves MSVC on the PR's loop.

Caveats:
- The MSVC half repeats something varY's own description already says ("every other build: MSVC ... keep the PR's word loop"). The new part is clang-cl.
- clang-cl is a secondary PCbuild toolset; the python.org installers use MSVC.
- At plain -O2 (no PGO), clang-cl already auto-vectorizes the PR's word loop: 42 xmm references in ascii_case_words even without the macro. So clang-cl loses something only in the PGO-cold case the finding names.
- pystrhex.c's SIMD hex has the same Windows gap, so varY is consistent with that precedent.

This is a scope note, not a defect, and 'info' is the right severity.

## 12. With -O3 and AVX2 (x86-64-v3/v4), the PR's auto-vectorized loop uses wider vectors than varY's fixed 16-byte vectors, so varY does about 2x the work per byte on long strings

**Claim.** When the PR's loop gets auto-vectorized for AVX2, it handles 32 bytes per ymm operation. With gcc that applies to len >= 33; with clang it is 4 ymm per iteration (128 B) for len >= 129. varY's vector type is fixed at 16 bytes (varY lines 282, 307-316), so it stays on xmm: 16 B per iteration with gcc, 2 xmm (32 B) with clang. That is exactly twice the vector ALU operations per byte. The same happens in the gcc PGO-hot case: -O2 plus the flags -fprofile-use turns on. With x86-64-v4, gcc gives the PR zmm at 64 B per iteration. varY wins below the crossover, which is about 64 B for gcc-v3 and about 128 B for clang-v3, and loses above it.

**Evidence.** gcc -O3 -march=x86-64-v3 PR hot loop (13 insns / 32 B): vmovdqu (%r8,%rax),%ymm1; vpand; vpaddq; vpaddq; vpandn; vpandn; vpsrlq; vpand; vpxor; vmovdqu %ymm0,(%rdi,%rax); addq $32,%rax. varY (13 insns / 16 B): the same sequence on %xmm with addq $16,%rax.
clang -O3 -march=x86-64-v3: the PR has 43 insns per 128 B (4x ymm) behind `cmpq $120,%rdx` (len >= 129) and `cmpq $128,%rbx` (alias check). varY has 23 insns per 32 B (2x xmm).
Vector ALU ops per byte: PR 0.25, varY 0.50.
llvm-mca, L1-resident, B/cycle (PR vs varY):
- gcc-v3: skylake 11.5 vs 5.3; znver3 14.7 vs 7.3
- clang-v3: skylake 12.0 vs 6.0; znver3 16.0 vs 8.0
- gcc-v4 (zmm): znver4 22.1 vs 7.9; icelake-server 25.1 vs 5.3
- clang-v4: znver4 21.3 vs 10.1
callgrind instruction counts for one _Py_bytes_lower call (PR vs varY):
- gv3: len 64 130 vs 90; 65 101 vs 103; 256 208 vs 246; 1024 520 vs 870; 4096 1768 vs 3366
- cv3: len 128 246 vs 126; 129 98 vs 139; 4096 1599 vs 2978
- gcc -O2 -march=x86-64-v3 with -ftree-loop-vectorize -fvect-cost-model=dynamic -funroll-loops -fpeel-loops (what -fprofile-use enables for hot code): 4096 1491 vs 2804; 256 201 vs 224
Rough end-to-end estimate for a 1 KB str.lower() on Zen3-class hardware: about 70 extra cycles (~15-20 ns), on the order of 10-25% of the call. Not measured.

**Suggestion.** Accept this as the trade-off, or close the gap under `#ifdef __AVX2__` with a 32-byte GNU vector main loop (vector_size(32), ge/gt passed as scalars). Keep vec16 for 16..31.
I tried this as variant Z2 in /tmp/rv/sa-Z2.c. Instruction counts at 4096 B: gv3 1702 (PR 1768, varY 3366); cv3 1508 (PR 1599). The output is a single ymm loop.
Do not use 32-byte vectors without AVX2. gcc -O2 SSE2 code for Z2 realigns the stack (`andq $-32,%rsp`) and spills the broadcast constants, so the loop reloads them (`movdqa -56(%rsp),%xmm7`). That costs 106 instructions for len 33..64, against 75 for varY.

**Verifier (confirmed, minor).** I couldn't refute the mechanism. It reproduces exactly. The severity is overstated, though, and the PGO-hot part of the claim is contradicted by evidence.

**What I confirmed**
- I checked that ~/abench/src-cf-PR and src-cf-varY match 9433a66 and the varY file.
- gcc 13 -O3 -march=x86-64-v3, PR: one ymm loop at 32 B per iteration, reached for len ≥ 33.
- Same flags, varY: one xmm loop at 16 B per iteration. Both loops have the same 8 vector ALU ops.
- clang 18 -O3 v3, PR: 4×ymm per iteration (128 B), behind `cmp $0x78` (len ≥ 129) and a 128-byte alias check.
- Same flags, varY: 2×xmm per iteration (32 B). clang also auto-vectorizes varY's 8..15 word loop into a ymm loop that can never run (bloat only).
- -march=x86-64-v4: gcc gives the PR zmm loops; varY stays on xmm.
- llvm-mca gives the same cycles per iteration for the ymm and xmm loops (znver3 2.18, skylake 2.8 vs 3.0). The PR therefore moves twice the bytes per cycle (znver3 14.7 vs 7.3 B/cycle), matching the finding.
- My own callgrind counts on a standalone extraction match the reviewer's numbers exactly (table in the reproduction field).

So in builds where the PR's loop is auto-vectorized with AVX2, varY loses above about 64 B with gcc and about 128 B with clang, and at 1-4 KB it runs about 1.7-1.9x the PR's instructions (callgrind).

**What is overstated**
1. **The PGO-hot case doesn't happen with CPython's training.** In the existing gcc PGO+LTO build (gp-PR), ascii_case_words.lto_priv.0 has 0 SIMD instructions: an un-rotated, size-optimized scalar loop. Yet the same gcc's -O3 release build (g-PR) vectorizes it. So the training leaves the loop cold. The profile doesn't depend on -march, so a gcc PGO build at x86-64-v3 also keeps the PR scalar. gp-varY keeps its SSE2 loop.
2. **Most AVX2 configurations leave the PR scalar, so varY is faster there at every length ≥ 16.** In those builds the PR is scalar:
   - gcc -O2 -march=x86-64-v3: 0 SIMD instructions in the PR.
   - gcc PGO: see point 1.
   - clang with -D_FORTIFY_SOURCE=2 and v3: 0 SIMD instructions in the PR.
   That covers how v3 distributions typically build python3 (RHEL 10 family: gcc, -O2, PGO+LTO).
   The loss only shows up in:
   - gcc -O3 without PGO plus an explicit AVX2 -march (custom or -march=native builds);
   - clang builds with AVX2, without fortify, where the loop is vectorized.
3. **Real call lengths are short.** The bench repo's realworld/summary.md shows 0% of calls at 64+ characters in every workload except doclower (whole-file lowercasing), including the PGO training task. Below the crossover varY wins even in the affected builds (gcc len 16/32/64: 43/64/90 vs PR 64/96/130 instructions).
4. **It is still a large win over main.** In the affected builds varY is the SSE2-width loop, which is the code the measured 3-4x-at-1 KB results already reflect.

The 10-25% estimate at 1 KB is plausible from the 2x loop throughput, but it was not measured. I didn't time anything, because timing is not allowed on this machine.

Net: this is a real but narrow trade-off, not a major regression. The fix suggested in the finding (a 32-byte vector type under `#ifdef __AVX2__`) is a reasonable follow-up, but I did not check it.

## 13. clang still vectorizes varY's 8..15 word loop, which can never reach the vector part; this adds dead code and an unconditional push/pop

**Claim.** In varY, the word loop at lines 327-329 only runs for 8 <= len <= 15, so it executes at most once. clang does not see that bound. It emits the full runtime-checked SIMD loop for that path: generic gets 2x xmm behind `cmpq $24,%rdx` (needs len >= 33), and v3 gets 4x ymm behind `cmpq $120`. Neither can ever execute. Because those dead loops use r14/rbx, clang moved `pushq %r14; pushq %rbx` to the function entry, so every call pays for them, including the 16+ vector path. gcc proves the bound and emits straight-line code.

**Evidence.** ascii_case_words code size, PR vs varY:
- clang -O3: 393 vs 719 B
- clang -O3 -march=x86-64-v3: 490 vs 803 B
- gcc -O3: 479 vs 386 B
callgrind at len 8, clang -O3: PR 28 vs varY 34 instructions. At len 12-15: 51 vs 53. cv3 at len 8: 28 vs 34.
The varY clang entry is `pushq %r14; pushq %rbx; ... cmpq $15,%rdx; jle .LBB8_1`. The dead vector loop .LBB8_5 is reachable only when `cmpq $24,%rdx` (that is, len-9 >= 24) fails to branch, which is impossible when len <= 15.

**Suggestion.** Inside the _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR block, handle 8..15 without a loop, for example: `if (len > SIZEOF_SIZE_T) ascii_case_word(result, cptr, 0, ge, gt); ascii_case_word(result, cptr, len - SIZEOF_SIZE_T, ge, gt); return;`.
Tried as variant Z1:
- clang code size: 461 B (cO3), 433 B (cv3)
- clang len 8: 31 instructions; len 12: 43, against PR 51 and varY 53
- gcc: unchanged at 386 B
Output was identical to the PR for lengths 1..1000.

**Verifier (confirmed, minor).** I couldn't refute this. The main claim reproduces, and under CPython's real CFLAGS the problem is wider than reported.

What holds:
- In varY the word loop (lines 327-329) runs only for 8 <= len <= 15, so it executes at most once.
- clang -O3 still emits the full runtime-checked SIMD loop for it:
  - generic: 2x xmm behind `cmpq $24` on len-9;
  - x86-64-v3: 4x ymm behind `cmpq $120`.
  - Neither can run when len <= 15.
- clang also puts `pushq %r14; pushq %rbx` at function entry, so the 16+ vector path pays for them on every call. The PR shrink-wraps its pushes behind `cmp $9; jl`.
- Sizes match the reviewer: clang -O3 393 vs 719 B, v3 490 vs 803 B.
- The same code is in the built ~/abench/cf-varY/python: ascii_case_words is 0x2e0 bytes, with `push rbp; mov rsp,rbp; push r14; push rbx` at entry and the dead loop at de440.
- On aarch64 (clang --target=aarch64) the dead NEON loop is also there (`cmp x12,#24`), but there is no push/pop.
- Z1 (two overlapping words for 8..15) matched the PR for every length from 8 to 600, random bytes, both cases, in every configuration.

Two corrections to the finding:

1. "gcc proves the bound and emits straight-line code" is true only for the reviewer's compile, which leaves out CPython's BASECFLAGS. CPython adds `-fno-strict-overflow` (plus frame pointers). With those flags gcc -O3 does not prove the bound either:
   - It emits the dead vectorized word loop: varY ascii_case_words is 721 B, the same size as in the built ~/abench/g-varY/python (0x2d1). The PR is 492 B and Z1 is 386 B.
   - The 8..15 path pushes rbp plus 4 registers. gcc does shrink-wrap, so the 16+ path doesn't pay.
   - So the dead code shows up under gcc too, and Z1 helps gcc more than clang.

2. The stated cause of the entry push is imprecise. The live scalar remainder loop (.LBB8_7, which runs once for len 9..15) also uses rbx and r14. Turning off vectorization for the word loop with `#pragma clang loop vectorize(disable) interleave(disable)` still leaves pushes at entry, now 4 registers because clang unrolls the loop. The real cause is having any loop on that path, which defeats shrink-wrapping. Z1 still pushes rbx at entry under clang, but only that one register.

Impact: a few instructions per call. 8..15 bytes costs 2-22 extra instructions, the most under gcc with CPython's flags. Under clang, len >= 16 costs about 3 extra (2 pushes, 2 pops). There are also about 150-330 B of dead code. This is small next to the cost of calling bytes.lower() from Python, so "minor" is right. Removing the loop (Z1) is still smaller, faster and simpler, so the suggestion stands.

## 14. On AArch64, clang does not unroll varY's vector loop; the PR's auto-vectorized loop does 32 B per iteration with ldp/stp

**Claim.** With generic aarch64 clang -O3, the PR's loop handles 32 B per iteration in 22 instructions (ldp q4,q5 / stp q4,q5). varY handles 16 B per iteration in 13 instructions and is not unrolled. Vector ALU ops per byte are the same, so wide cores (Apple M-series, Neoverse V1) are at parity. On narrower cores, the front end costs varY up to about 15%. With -mcpu=neoverse-v1, the PR uses SVE (ld1d z-regs, 256-bit on V1) while varY's main path stays 128-bit NEON. Generic distro builds do not enable SVE, so this only affects tuned builds.

**Evidence.** llvm-mca on aarch64 clang -O3 hot loops, B/cycle (PR vs varY): cortex-a72 3.2 vs 2.7; cortex-a76 3.2 vs 2.7; neoverse-n1 3.5 vs 3.2; neoverse-n2 3.6 vs 3.5; neoverse-v1 7.5 vs 7.0; apple-m1 6.0 vs 5.9.
I could not test gcc for aarch64 because no cross-compiler is installed.

**Suggestion.** Optional: process two vec16 per iteration (or use a 32-byte vector type, which clang lowers to ldp/stp q on NEON) so narrow ARM cores reach parity. This matters little next to the x86 finding.

**Verifier (confirmed, minor).** I could not refute it. Every factual claim reproduces. The impact is narrower than the finding implies, and one sub-point (SVE) does not matter.

What reproduces:
- **Loop shape.** I extracted the PR's ascii_case_words and varY's version into a standalone file. varY's block is byte-identical to src-cf-varY. With clang-18 `--target=aarch64-linux-gnu`, at -O2 and -O3:
  - PR hot loop: 22 instructions per 32 B, using `ldp q4,q5` / `stp q4,q5`.
  - varY: 13 instructions per 16 B, using `ldr q`/`str q`, with no unrolling.
  - This holds for -mcpu = generic, cortex-a53, a55, a72, a76, neoverse-n1. Vector ALU ops per byte are equal (16 per 32 B vs 8 per 16 B).
- **llvm-mca numbers match exactly** (PR vs varY, B/cycle): A72/A76/X1 3.19 vs 2.65, N1 3.54 vs 3.18, N2 3.55 vs 3.54, V1 7.49 vs 7.04, M1 5.97 vs 5.94. On A72 the limit is dispatch: 3 uops per cycle, and 28 uops per 32 B for the PR vs 16 uops per 16 B for varY. So "front end" is the right explanation there.
- **SVE.** `-mcpu=neoverse-v1` does give the PR an SVE loop (`ld1d z`, predicated with whilelo, 14 instructions). varY stays NEON.

Corrections and context:
1. **SVE makes no difference.** On V1-tuned code, llvm-mca gives PR (SVE) 7.08 vs varY 7.04 B/cycle. The SVE point has no throughput effect on V1.
2. **macOS default target (arm64-apple-macosx).** The PR's loop is 64 B per iteration (38 instructions, post-indexed ldp/stp), but llvm-mca shows parity on M1/M2: 5.81 vs 5.95 B/cycle.
3. **"Up to about 15%" understates the gap on in-order little cores**, if llvm-mca's crude in-order models are right. A55: 1.33 vs 0.94. A53 and A510: about 2x in the PR's favor, because varY's single dependency chain cannot hide latency. This would matter for generic builds running on phone little cores, for example clang-built Android/Termux.
4. **Only long strings are affected.** I counted dynamic instructions from the generic -O3 assembly:
   - 16–256 B: varY executes 0.68–0.96x as many instructions as the PR. The PR's vector loop only starts at len ≥ 33 and leaves up to 3 scalar 8-byte words plus extra loop exits.
   - The crossover is about 300 B. At 1000 B or more, varY executes 1.16x as many.
5. **PGO builds go the other way.** I used `__attribute__((cold))` as a proxy for a loop that PGO training finds cold (clang then optimizes for size). With it, clang leaves the PR's loop scalar (13 instructions per 8 B) while varY keeps NEON (13 per 16 B). In --enable-optimizations builds varY is ahead on aarch64. The finding's case is narrow: clang, no PGO, a non-Apple core, long strings.
6. **The suggested fix needs care.** Calling vec16 twice in a row does **not** give ldp/stp: the first store may alias the second load, so clang keeps them apart. Even so, it reaches parity on A72 (3.19) and M1 in llvm-mca. Loading both halves before either store does give ldp/stp: N1 3.55, but A72 drops to 2.90.

Not testable: gcc for aarch64 (no cross-compiler installed), and real ARM hardware. Every timing here is llvm-mca's model, not a measurement.

## 15. Gating on _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR leaves gcc 11 and older builds without the vector path, though varY only needs vector_size

**Claim.** The configure test (configure.ac 5496-5526) compiles a call to __builtin_shufflevector. GCC only added that in version 12 (from my knowledge; not verified here). With gcc <= 11 (for example the RHEL 9 or Ubuntu 22.04 toolchains), the macro is therefore undefined and varY falls back to the PR's word loop. That loop stays scalar at -O2 or in PGO-cold code, which is exactly the case varY is meant to fix. varY itself only uses GNU vector_size types, which much older gcc supports. PC/pyconfig.h does not define the macro either, so clang-cl gets the word loop; clang does auto-vectorize that loop.

**Evidence.** configure.ac:5505-5516 requires x86_64, aarch64, or arm+NEON and calls __builtin_shufflevector(a, b, ...). `grep SHUFFLEVECTOR PC/ Include/` finds nothing. I could only test gcc 13 locally, so the gcc <= 11 behaviour is inferred, not observed.

**Suggestion.** If broader coverage matters, gate on `(defined(__GNUC__) || defined(__clang__)) && (defined(__x86_64__) || defined(__aarch64__) || (defined(__arm__) && defined(__ARM_NEON)))`, or add a dedicated configure check. Otherwise, say in the comment or NEWS entry that the benefit needs gcc >= 12 or clang.

**Verifier (confirmed, minor).** I could not refute any of the finding's premises.

1. The gate depends on the builtin, not on what varY uses. In configure.ac:5496-5518, _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR is set only if a program calling __builtin_shufflevector(a, b, ...) compiles and links, on x86-64, aarch64, or ARM32 with NEON. varY's vector path (varY.patch lines 41-79) never calls __builtin_shufflevector. It uses only `vector_size(16)` of size_t, vector-scalar `&`, `+` and `>>`, `~`, and __builtin_memcpy.

2. GCC 11 and older lack the builtin. The GCC 12 changes page (gcc.gnu.org/gcc-12/changes.html) says, under C family: "Support for `__builtin_shufflevector` compatible with the clang language extension was added." The GCC 11.4 Vector Extensions manual documents only __builtin_shuffle. It does say "it is allowed to use a binary vector operation where one operand is a scalar", so varY's vector code is valid GNU C there. I simulated the configure program with gcc 13 and an absent builtin name. It fails to compile ("incompatible types when initializing type 'v16u8' ... using type 'int'"), so the macro would be undefined. No gcc older than 13 is installed in WSL, so this part is simulated, not observed.

3. Without the macro, varY is scalar at -O2. The same GCC 12 changes page says "Vectorization is enabled at -O2" as a new feature, so gcc 11 does not vectorize at -O2 at all. I compiled varY's real bytes_methods.c with gcc 13 -O2, with and without the macro. With it, ascii_case_words has 33 xmm and 4 paddq instructions. With it removed (the gcc ≤ 11 situation), it has 0 xmm and 0 paddq; the loop is plain 64-bit scalar. Adding -fno-tree-vectorize to mimic gcc 11 -O2 changed neither count. So on those toolchains varY behaves exactly like the PR, in the -O2 and PGO-cold cases varY targets.

4. Windows: PC/pyconfig.h does not define the macro, so clang-cl gets the PR word loop, which clang auto-vectorizes. This is correct and harmless.

Why only minor: CPython main is 3.16 (Include/patchlevel.h), due in late 2027. Most toolchains that build it (Debian 12+, Ubuntu 24.04+, Fedora, manylinux_2_28/2_34 with gcc-toolset-14, conda-forge, clang-based builds) are gcc ≥ 12 or clang. The gap is mainly self-builds with system gcc 11 on RHEL/Alma/Rocky 9, Amazon Linux 2023, or Ubuntu 22.04. Also, CPython's default non-PGO OPT is -O3, where gcc 11 can still vectorize the word loop. The impact is lost speed, not wrong results.

The suggested direct gate (GNUC/clang plus arch) is plausible but has trade-offs. It stops reusing an existing configure result, and it also turns the path on for clang-cl, which defines `__clang__` and `__x86_64__`. That needs separate checking. A NEWS or comment note is the cheaper fix.

## 16. In size-optimized or cold gcc code, varY's loop mixes floating-point-domain logic ops with integer SIMD adds

**Claim.** With -Os, or with __attribute__((cold)) as a stand-in for PGO-cold code, gcc emits andps/andnps/xorps/movaps interleaved with paddq. -O3 gives pand/pandn/pxor. On Intel cores this can add about one cycle of bypass latency per domain crossing. Iterations are independent and the loop is throughput-bound, so this is probably hidden. It is still SIMD and still about 2x the PR's scalar loop in the same mode.

**Evidence.** Op counts in ascii_case_words:
- sa-gcold-varY.s: 4 andnps, 4 andps, 6 movaps, 4 paddq, 2 xorps
- gO3-varY.s: 4 paddq, 4 pand, 4 pandn, 2 pxor
callgrind, gcc -Os, len 4096: PR 9246 vs varY 4378.

**Suggestion.** No change needed. Note it if PGO-cold timings look worse than the -O2 numbers.

**Verifier (confirmed, info).** I could not refute this. The codegen claim reproduces exactly, and the performance claim is hedged ("can add", "probably hidden") and consistent with the code.

1. -Os: I compiled varY's real Objects/bytes_methods.c with gcc 13.3 -Os. The 16-byte loop in ascii_case_words uses movups, movaps x3, andps, andnps, paddq x2, andps, andnps, psrlq, xorps, movups. At -O2 and -O3 the same loop uses movdqu/movdqa, pand, pandn, pxor. So the FP-domain logic ops are mixed with paddq at -Os, as claimed.

2. cold: In a standalone copy of the loop, __attribute__((cold)) at -O2 or -O3 and __attribute__((optimize("Os"))) both give 4 andnps, 4 andps, 6-7 movaps, 4 paddq and 2 xorps. That matches the reported counts.

3. Real gcc PGO, not just the cold stand-in: I used -fprofile-generate, then -fprofile-use.
   - With zero training calls, gcc puts the function in .text.unlikely and emits andps, andnps and xorps.
   - With 1000 training calls, it goes in .text.hot and uses pand, pandn and pxor.
   So the PGO-cold case is real. It is decided per function: it happens only when the PGO training never calls ascii_case_words. gcc picks the ps forms because optimize_function_for_size_p is true; they are one byte shorter, with no 66 prefix.

4. "About 2x the PR in the same mode": The PR's -Os word loop is 18 instructions per 8 bytes. varY's -Os loop is 17 instructions per 16 bytes. For len 4096 that gives about 9.2k vs 4.4k instructions, which matches the reported callgrind 9246 vs 4378.

5. Bypass latency: No iteration depends on the one before; only the index carries over. The dependency chain is load → andps → paddq → andps → andnps → psrlq → xorps → store, about 5 domain crossings. These add latency per iteration but not to loop throughput. That supports the reviewer's "probably hidden" for long strings. For 16-31 byte strings it could add a few cycles to a call that Python object overhead dominates. I could not measure the Intel bypass cost (no Intel hardware), and I did not run a timing test because of the benchmark on CPU 4. The "about one cycle on Intel" figure therefore stands as a plausible, documented characteristic, not something I verified.

Further notes:
- Only gcc does this. clang at -Os and -O2 emits pand, pandn and pxor.
- Builds with AVX2 enabled would use vpand regardless, but CPython builds for baseline SSE2.
- The -O2 build (Ubuntu/Debian) is not affected.

The suggestion of "no change needed" is reasonable.

## 17. Not necessary as written: a plain-C 16-byte block gets the same SIMD without GNU vectors, the configure macro, or __builtin_memcpy

**Claim.** varY targets three cases: gcc -O2, gcc PGO where the loop is cold, and clang with _FORTIFY_SOURCE. In all three, plain C11 that converts 16 bytes as an array of words (size_t x[16 / SIZEOF_SIZE_T], memcpy in, ascii_case_bits() on each element, memcpy out) is SLP-vectorized into the same SSE2/NEON sequence. That makes varY's GNU vector type, its second copy of the bit trick, the macro coupling and ASCII_CASE_MEMCPY avoidable. It would also give SIMD on targets the macro excludes (gcc 11, ppc64le, s390x, riscv64).

**Evidence.** I made a scratch copy of the PR file in which only ascii_case_words changes: a 16-byte array block for len >= 16 on non-MSVC builds, the MSVC count-by-one loop untouched, plain memcpy. Path: scratch/review_tmp\portable\Objects\bytes_methods.c. I compiled it with the real BASECFLAGS/OPT/NODIST flags read from ~/abench/*/Makefile and counted instructions in ascii_case_words (total / using SIMD registers):
- gcc -O2 (g2 flags): PR 65/0, varY 111/33, portable 115/37
- gcc -O3: PR 125/19, varY 176/52, portable 171/48
- clang -O3 -D_FORTIFY_SOURCE=2: PR 87/0, varY 173/83, portable 129/31
- clang --target=aarch64: portable 72 NEON instructions (add v.2d, bic, ushr)
- clang --target=armv7a -mfpu=neon: portable 72 NEON instructions
The gcc -O2 inner loop is movdqu/pand/paddq/paddq/pandn/pandn/psrlq/pand/pxor/movups, the same as varY's.
Standalone gcc -O3 -flto PGO with zero long-string calls in training ('long-calls=0'): portable16 96/28, varY 79/29, PR 53/0.
The portable form passed the ASan+UBSan harness: 'gcc portable: OK 1024237 checks', 'clang portable: OK 1024237 checks'.
Limits: at -Os the portable form is scalar (132/0) while varY stays SIMD (101/31). The cold-PGO result comes from a standalone program, not a real CPython PGO build, which I was not allowed to run.

**Suggestion.** Before proposing varY, build and benchmark the portable variant (call it varZ) in g2, gp and cf trees, and confirm the gp build disassembles to SIMD. If it holds, drop the vector_size typedef, ascii_case_vec16, the #ifdef _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR blocks and ASCII_CASE_MEMCPY. That answers the 'is it necessary / precedent for SIMD' objection with about 12 lines of plain C.

**Verifier (confirmed, major).** I could not refute the finding. I reproduced its numbers and also tested the case it could not: a real CPython PGO profile. In every case varY is aimed at, the plain-C 16-byte array block compiles to the same SSE2 or NEON sequence as varY's GNU vector type.

1. **Plain compiles.** I used the exact flags from `make -n` in g2-varY, g-varY and cf-varY. My counts match the reviewer's exactly. The gcc -O2 portable inner loop is movdqu/pand/paddq/paddq/pandn/pandn/psrlq/pand/pxor/movups, the same as varY's.

2. **Real PGO profile.** gp-varY kept Objects/bytes_methods.gcda. Its profile for `ascii_case_words` shows 9238 calls with 8..15 bytes, 935 calls with 16 or more, and 1373 iterations of the 16-byte loop. That is far below gcc's hot threshold (sum_max/10000 ≈ 46754), so the loop is not hot. This is why gp-PR's final binary is scalar (59/0) while gp-varY's is SIMD (98/31).
   - I made a portable copy of varY whose line numbers are unchanged, so every other function's profile still matches.
   - I wrote a gcda patcher and spliced in a record for `ascii_case_words` with the portable CFG checksum and the same training counts. Rewriting varY's own record gives a byte-identical file, and recompiling varY reproduces the real gp-varY object exactly.
   - Results (portable vs varY): gp flags at -O3, 97/31 vs 97/31, with only register allocation differing. Ubuntu-like -O2 PGO, 97/31 vs 97/31. 16-byte path never executed, 96/30 vs 96/30. Function never called, 171/48 vs 176/52.

3. **clang PGO (standalone, cold long path).** x86-64: portable 96/43 vs varY 94/41. arm64-macos13 reusing the same profile: 81/24 for both, all NEON. This held with and without a macro that mimics the macOS SDK's _FORTIFY_SOURCE memcpy.

4. **Correctness.** A standalone ASan+UBSan check passed for both forms (105280 checks each) under gcc and clang at -O2 and -O3.

**Where the finding overstates:**
- At -O1 and -Os the portable form is scalar (gcc) or mostly scalar (clang); varY stays SIMD there. The reviewer flagged -Os; -O1 behaves the same.
- Under clang with fortify, varY's 16-byte loop is unrolled 2x and the portable one is not. Each block is still one SSE2 sequence, so `ASCII_CASE_MEMCPY` still has a small effect.
- The claim of SIMD on gcc 11, s390x and riscv64 is overstated. gcc 11 does not vectorize at -O2 at all. Baseline rv64gc and Debian's z196 s390x have no vector unit.

**Not done:** an LTO-linked PGO interpreter for the portable form (for varY, the object compiled before the LTO link matched the final binary to within one instruction), and runtime benchmarks.

The core claim holds: varY's GNU vector type, its second copy of the bit trick, its dependence on the configure macro and its `ASCII_CASE_MEMCPY` are not needed for SIMD in gcc -O2, gcc or clang PGO, or clang with fortify.

## 18. No tests exercise the word or vector paths; the SIMD precedent shipped boundary tests

**Claim.** Neither the PR nor varY adds tests, and no existing CPython test calls lower()/upper() on ASCII input of 8 or more characters in a way that checks the result position by position. Lengths 16, 17, 31, 32 and 33, non-ASCII bytes at each position, and unaligned buffers are all untested. The precedent PR GH-143991 added test_hex_simd_boundaries (lengths 14, 15, 16, 17, 31, 32, 33, 64, 65), and AGENTS.md says to write tests that exercise the change.

**Evidence.** - Lib/test/string_tests.py:451-459 (BaseTest, so it runs for str, UserString, bytes and bytearray) only checks 'HeLLo' and 'hello', 5 characters.
- Lib/test/test_str.py:909-955 adds only non-ASCII cases, which take the Unicode path.
- Lib/test/test_bigmem.py:253/459 use 'A'*size and 'a'*size, one value at every position, and run only with -M.
- Lib/test/test_bytes.py:3090-3115 is a free-threading race test that only checks c[0] and c[-1] against 0xdd/0xcd.
- The PR's commit b4d59af adds only the NEWS file and Objects/bytes_methods.c.
I wrote the proposed tests to scratch/review_tmp\proposed_tests.py. They pass on g2-varY ('Ran 6 tests in 0.132s OK'), cf-varY (0.137s) and g-main (0.165s). A mutation check (mutation_check.py, same directory) swaps in implementations that skip the overlapping tail at lengths 33 and 17; both tests fail as intended ('failures: 2 (expected 2)').

**Suggestion.** Add two tests.
(1) In Lib/test/string_tests.py, BaseTest, after test_upper, add test_lower_upper_long. For n in [*range(1, 41), 63, 64, 65, 1000], and each position i (for n >= 100 only the first and last 20), put c in 'AZaz@[`{' at i inside '0'/'9' padding and checkequal lower and upper. Also check 'Hello, World! ' * 10. This covers str, UserString, bytes and bytearray.
(2) In Lib/test/test_bytes.py, BaseBytesTest, add test_lower_upper_every_byte. For n in (7, 8, 9, 15, 16, 17, 31, 32, 33), put every byte value 0..255 at every position over the background b'aZ@[`{zA\x80\xc1\xda\xe1\xfa\xff\x7f\x00' * 3 and compare with translate(bytes.maketrans(...)). Add unaligned bytearrays made with del b[:k] for k in range(16).
Both files are in the PGO training list (Lib/test/libregrtest/pgo.py), so re-check the PGO codegen after adding them.

**Verifier (confirmed, minor).** The core of the finding holds, but its headline and one piece of its evidence are wrong, so the real gap is narrower than claimed.

What is true:
- Neither the PR nor varY adds a test. The PR's own commits (b4d59af, a907379, 91c788f, 9433a66) touch only Objects/bytes_methods.c and the NEWS entry. varY.patch touches only Objects/bytes_methods.c.
- The dedicated tests are all short: string_tests.py test_lower/test_upper ('HeLLo', 5 chars), test_capitalize (at most 7 chars), test_casefold. A gdb hook on ascii_case_words in g2-varY counted zero calls with len >= 8 during all of test_str, test_bytes and test_userstring.
- Non-ASCII bytes are never tested on either path. I injected two mutations: for len >= 16 (vector path) and for 8..15 (word path), a byte >= 0x80 whose low 7 bits are a letter gets its case flipped, which is what you get if the "& ~x" guard is dropped. No test caught either one. That covers 12 modules: test_str, test_bytes, test_userstring, test_bigmem, test_email (1823 tests, about 66k calls), test_codecs, test_base64, test_configparser, test_urlparse, test_mimetypes, test_http_cookies and test_uuid. In fact the mutation never triggered: none of them passes such bytes in. Grep finds no test calling lower() or upper() on bytes with high bytes.
- The 'Z'/'z' boundary is covered only by accident. A mutation that leaves 'Z' unconverted on the vector path is caught only by test_codecs PunycodeTest.test_decode and test_base64 test_b32decode_ignorechars, never by a string test.
- The precedent test_hex_simd_boundaries exists in test_bytes.py:608, and AGENTS.md says to write tests that exercise the change.

What is wrong:
- The title "No tests exercise the word or vector paths" is false, and so is the claim that test_bigmem runs only with -M. bigmemtest has dry_run=True by default and calls the test with maxsize=5147 when -M is not given. test_bigmem has no resource gate, so it runs in normal CI.
  - Vector path: StrTest, BytesTest and BytearrayTest test_lower/test_upper run 'A'*5147 and 'a'*5147 through it (5147 % 16 = 11, so the overlapping tail runs too). They check every position with count() == size. Two mutations were each caught by all 6 of these tests: one leaves the last len % 16 bytes unconverted, the other leaves only the last byte unconverted.
  - Word path: _test_title builds its expected value with SUBSTR.lower(), where SUBSTR is 'SpaaHAaaAaham' (13 bytes). A mutation that leaves the last len % 8 bytes of an 8..15 string unconverted failed test_title for str, bytes and bytearray.

So existing default tests already catch gross loop and tail bugs on both paths. What is actually missing:
- non-ASCII bytes (the "& ~x" mask);
- systematic coverage of the 'Z'/'z' and '@'/'['/'`'/'{' edges;
- specific short lengths (16, 17, 31, 32, 33) and per-position placement.

The suggestion to add tests is still right. CI on aarch64 and ARM32 NEON would only catch a miscompile of the new vector code, or a broken high-byte guard, through such tests.

Why minor rather than major: the gap is narrower than claimed, it is cheap to close (about 20 lines in string_tests.py and test_bytes.py), and it applies equally to the PR and varY, so it does not bear on whether varY should replace the PR's loop. test_bytes and test_str are in the PGO training list (pgo.py lines 12 and 44), so the warning to re-check PGO codegen after adding the tests is valid.

## 19. Mixing scalars with GNU vector operands repeats the construct that broke pystrhex.c on older clang (gh-148474)

**Claim.** varY combines vector operands with scalar ones, which older clang rejects for vector_size types. The configure probe uses only vector-vector operations and __builtin_shufflevector, so it still defines the macro on such a compiler and the build then fails with a hard error.

**Evidence.** Scalar operands appear in four lines:
- Line 291: b = x & (0x7f * ones)
- Line 292: & (0x80 * ones) and >> 2
- Lines 309-310: (ascii_case_vec){0} + ge and (ascii_case_vec){0} + gt
In gh-148474 (reported by jmroot, fixed in PR #148475, merged 2026-04-16), pystrhex.c's 'v16u8 hi = (data >> 4) & mask_0f;' failed on older clang with "cannot convert between vector values of different size ('v16u8' ... and 'int')". The fix replaced the scalar 4 with an explicit splat, 'four'. A cfe-dev thread from May 2016 shows clang then rejected 'vec + 5' on GCC vectors. clang 18 and gcc 13 accept varY cleanly, even with -Weverything (only -Wunsafe-buffer-usage notes). I could not run an old clang, so this risk is plausible but not confirmed.

**Suggestion.** Follow pystrhex's post-fix style: no scalar operands. For example, use typedef uint64_t ascii_case_vec __attribute__((vector_size(16))) with explicit constants such as (ascii_case_vec){c, c} for ge, gt, 0x7f.., 0x80.. and a vector shift count {2, 2}. Two uint64 lanes work on 32-bit ARM NEON too (vadd.i64). This point disappears if the portable form is used instead.

**Verifier (confirmed, major).** I could not refute the finding. Its premise holds up when checked against clang's own source.

1. varY really does mix scalars with GNU vectors. In scratch/explore\varY\b\Objects\bytes_methods.c:
   - Line 291: `b = x & (0x7f * ones);` combines a vector with a size_t.
   - Line 292: `... & (0x80 * ones)) >> 2;` combines a vector with a size_t and shifts by an int.
   - Lines 309-310: `(ascii_case_vec){0} + ge` / `+ gt` combine a vector with a size_t.

2. Clang before 5.0 rejects a GCC `vector_size` vector combined with a scalar in `&`, `+`, `^` and similar operators. In clang 4.0.1, `Sema::CheckVectorOperands` splats a scalar only for ExtVectorType. Its own comment reads "FIXME: this should also work for regular vector types as supported in GCC." Its only other route is a lax conversion, which requires both operands to have the same total size: an 8-byte or 4-byte scalar never matches a 16-byte vector. It then emits `err_typecheck_vector_not_convertable` ("cannot convert between vector values of different size"). That is the exact error from gh-148474.

   Clang 5.0.0 added `tryGCCVectorConvertAndSplat` (D25866). From 5.0 on, `vec & size_t` is accepted, and so is `vec + size_t` when the element type is the same.

   In clang 4.0.1, a scalar shift is already splatted by `checkVectorShift`. gh-148474's `data >> 4` therefore failed on an even older clang. varY's `>> 2` fails on that range too, and its `&` and `+` operands also break clang 4.x. varY's breakage range is therefore a superset of the one CPython just fixed.

3. The configure probe does not protect these compilers. It only checks the architecture, a `vector_size(16)` typedef, a brace initializer and `__builtin_shufflevector`, all of which old clang supports. gh-148474 shows this directly: the macro was defined on the reporter's compiler, which is why pystrhex.c's SIMD block was compiled and failed. Issue page summary: macOS, "older than roughly Xcode 9"; fixed by PR #148475 on 2026-04-16 and backported. The checkout records it in Misc/NEWS.d/3.15.0b1.rst:2017 as "Fixed compilation of Python/pystrhex.c with older clang versions."

4. CPython's current pystrhex.c (lines 46-88) follows the fixed style, with no scalar operands: `four = v16u8_splat(4)` and `data >> four`. varY would bring back the pattern that was just removed.

Scope and severity: this is a hard compile error, but only with clang older than 5.0 (2017) or Apple clang from before about Xcode 9, on x86-64/aarch64/NEON. That is a narrow set of compilers, but CPython has just accepted a fix for exactly this case, so a reviewer would likely flag it. Rating: major as a review-readiness blocker, though the fix is trivial.

Note on the suggested fix: switching to uint64_t lanes changes the ARM32 lane width. Keeping size_t and using explicit splat vectors (lane count from SIZEOF_SIZE_T) or a vector shift count avoids that.

I did not compile with an actual pre-5.0 clang. WSL only has clang 18 and gcc 13, which accept varY.

## 20. Precedent shows maintainers resist SIMD in core on cost/benefit grounds; varY would be the second site

**Claim.** The only SIMD code in CPython core (Python/pystrhex.c, gh-144015 / PR GH-143991 by Gregory P. Smith, merged 2026-02-23) drew explicit objections from Serhiy Storchaka and Victor Stinner. A core developer merged it while taking personal ownership of it. varY adds a second GNU-vector site, in code those same reviewers maintain, on top of a PR that already vectorizes under MSVC, clang without fortify, and gcc -O3. PEP 7 also says not to use compiler-specific extensions, though guarded use has this one precedent.

**Evidence.** From the GH-143991 discussion:
- serhiy-storchaka: "How important the performance of this operation? What are precedences of using SIMD instructions in CPython?" and "To me, the cost/benefit ratio seems too high."
- vstinner: "I also have doubt that the speedup is worth it compared to the maintenance cost."
- gpshead at merge: "I know there were concerns about the maintenance burden from a couple of you, that's on me."
The precedent was also narrowed during review (the separator SIMD path was dropped) and broke once afterwards (gh-148474).
PEP 7: "Don't use compiler-specific extensions, such as those of GCC or MSVC."
Only Python/pystrhex.c uses vector_size in Objects/, Python/, Include/ and Modules/ (mimalloc's emmintrin.h aside).

**Suggestion.** Do not fold varY into the open PR. Land the portable word loop first. If more speed is wanted, open a follow-up issue with numbers for the builds that gain (gcc -O2, gcc PGO, clang+fortify), and prefer the plain-C block over GNU vectors. If GNU vectors remain, tag gpshead, who offered to be pinged about this code.

**Verifier (confirmed, major).** I couldn't refute this. I checked every piece of evidence against GitHub and the checkout, and it holds.

Verified:
- On GH-143991, serhiy-storchaka posted a COMMENTED review on 2026-01-19. It contains both quoted sentences word for word.
- vstinner's comment on 2026-01-26 matches the quote exactly.
- gpshead merged it himself on 2026-02-23T03:19Z. His closing comment includes "that's on me. Feel free to tag me in on anything that ever comes up regarding this code."
- gpshead offered to drop the sep= SIMD path. The merged pystrhex.c has no SIMD sep path.
- gh-148474 is a real build break: pystrhex.c failed to compile on older clang. gh-148475 fixed it by changing `data >> 4` to `data >> four` with a splatted constant.
- The PEP 7 sentence is quoted correctly.
- The configure.ac comment says the macro is "Used for SIMD-accelerated bytes.hex() in Python/pystrhex.c". varY would be its second user.

The live thread points the same way. On gh-161155, eendebakpt wrote "not convinced yet ... aim for a small diff and easy to review patch. 35 lines extra/diff might be ok". StanFromIreland asked for benchmarks without vectorization. No maintainer has reviewed PR 161201 yet. varY adds about 30 lines to that diff, plus a GNU vector type and a __builtin_memcpy macro. Nothing else in Objects/, Python/ or Include/ uses __builtin_memcpy.

Something the reviewer missed makes the finding stronger. varY's ascii_case_vec16 does `(...) >> 2`, a size_t vector shifted by an int scalar. That is the same kind of construct that broke pystrhex on older clang (gh-148474), where the error was "cannot convert between vector values of different size". So varY would likely bring back the one breakage this precedent has had, on the same old Xcode/MacPorts toolchains. Its other mixed operands (`x & (0x7f*ones)`, `{0} + ge`) are size_t scalars that match the element type, so they are probably fine. I can't test old clang here, so this part is inferred, not reproduced.

Small corrections that don't change the conclusion:
1. "Only Python/pystrhex.c uses vector_size" is wrong as worded. Modules/_hacl/libintvector.h, which is vendored, also uses vector_size(16). gpshead cited _hacl as SIMD precedent in that same thread. pystrhex.c is the only hand-written site.
2. "Guarded use has this one precedent" overstates things. Guarded GNU extensions are everywhere in core: 55 `__builtin_` uses in Objects/, Python/ and Include/, computed gotos in ceval, and `__attribute__` macros in pyport.h. So the PEP 7 argument is weak. The real precedent concern is specifically guarded GNU vector types.

Severity: this is not a correctness defect. varY compiles cleanly with gcc 13 and clang 18; the only warnings are existing -Wextra unused-parameter ones in fastsearch.h. It is a real review-readiness risk, though: folding varY in invites the same objections in a file those reviewers maintain, and probably repeats a known old-clang build break. Major for review-readiness is reasonable.

## 21. Reusing _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR: misleading name, gcc >= 12 requirement, stale configure documentation

**Claim.** varY never calls __builtin_shufflevector, but gates its code on a macro named for it. The macro's probe requires the builtin, so gcc 11 and older get no vector path even though vector_size works there. The macro's documentation would also go stale.

**Evidence.** - configure.ac:5493-5495 says 'Check for __builtin_shufflevector ... Used for SIMD-accelerated bytes.hex() in Python/pystrhex.c'.
- The AC_DEFINE description at 5522-5525 mentions only shufflevector.
- The gh-144015 NEWS entry (Misc/NEWS.d/3.15.0a7.rst:863-867) says 'gcc (version 12 or higher) or clang'.
- varY.patch changes only Objects/bytes_methods.c.
- PC/pyconfig.h has 0 occurrences of the macro, so MSVC and clang-cl never take the vector path.
So gcc 11 distro builds (e.g. RHEL 9, Ubuntu 22.04 default) keep the scalar PR loop at -O2. The claim 'explicit vectors stay SIMD everywhere' is overstated.

**Suggestion.** If the macro is reused, update the configure.ac comment and the AC_DEFINE text to mention Objects/bytes_methods.c, then regenerate configure and pyconfig.h.in (CI checks generated files), or use dnl comments. Better, avoid the coupling with the portable form.

**Verifier (confirmed, minor).** I couldn't refute any part of the finding.

1. **Misleading name.** varY never calls `__builtin_shufflevector`. The grep of the varY bytes_methods.c finds the macro only at lines 278 and 307, used as `#ifdef` gates. The code it gates uses only a `vector_size(16)` typedef with `+`, `&`, `~`, `>>` and `^`. The varY comment at 278-281 does not say why a shufflevector macro gates it.

2. **gcc 12 or newer required.** The probe in configure.ac at 5496-5518 is an AC_LINK_IFELSE that calls `__builtin_shufflevector`. gcc added that builtin in GCC 12, as the in-tree NEWS entry for gh-144015 says ("gcc (version 12 or higher) or clang", 3.15.0a7.rst:863-865). So gcc 11 and older fail the probe and never define the macro. varY's code doesn't need the builtin, only GNU vector extensions, which are much older. I could not run gcc 11 (WSL has only gcc-13 and clang-18), so the gcc 11 result rests on the probe source plus the NEWS text, not on a gcc 11 compile.
   - I showed the macro alone decides the codegen. With gcc 13 -O2, varY's bytes_methods.c with the macro defined gives an SSE2 16-byte loop in ascii_case_words (movdqu/paddq/pandn/psrlq/pxor/movups).
   - The same compile with only that macro removed from pyconfig.h gives a purely scalar 8-byte GPR loop, with no xmm instructions in ascii_case_words.
   - gcc 11 doesn't vectorize at -O2 at all (very-cheap vectorization at -O2 arrived in GCC 12). So gcc 11 -O2 builds keep the PR's scalar loop under varY, and "explicit vectors stay SIMD everywhere" overstates it.
   - This is not a regression against the PR; varY's gain just doesn't reach gcc 11 builds. clang is unaffected, since it has always had the builtin.

3. **Stale documentation.**
   - The configure.ac comment at 5493-5495 says "Used for SIMD-accelerated bytes.hex() in Python/pystrhex.c".
   - The AC_DEFINE text at 5522-5525 and pyconfig.h.in:2145 describe only shufflevector.
   - varY.patch has a single `diff --git` header, for Objects/bytes_methods.c, so none of these get updated.
   - PC/pyconfig.h* and Include/ have no occurrence of the macro, so MSVC and clang-cl never take the vector path. That part is already admitted in varY's description.
   - The suggestion's mechanics are right: `#` comments in configure.ac are copied into configure, and AC_DEFINE text goes into pyconfig.h.in, so editing either means regenerating those files.

All of this is cosmetic or a portability shortfall. Nothing is incorrect, so minor is the right severity.

## 22. ASCII_CASE_MEMCPY does nothing useful where varY's vector path exists, and its comment names macOS, where it does not apply

**Claim.** _FORTIFY_SOURCE does block clang from vectorizing the PR's word loop. But in varY, every platform that has the macro (including macOS: Apple clang on x86-64/arm64) handles 16 bytes and up in the explicit vector path, which stays SIMD with fortified plain memcpy. There __builtin_memcpy only lets clang vectorize the 8..15-byte word loop, which runs at most once, and that grows the code.

**Evidence.** - PR under clang -O2: 94/30 without fortify; 84/0 with -D_FORTIFY_SOURCE=2 and with =3. Fortify blocks vectorization on glibc too, not only macOS.
- gcc is unaffected: PR gcc -O3 with fortify 122/19.
- varY with ASCII_CASE_MEMCPY changed to plain memcpy, clang -O2 -D_FORTIFY_SOURCE=2: 124/29. The vector loop is intact: movdqu, pand, paddq, paddq, por, pandn, psrlq $0x2, pand, pxor, movdqu.
- varY as written: 168/83, which is the extra vectorized word loop.
- CPython has no other __builtin_memcpy use, and configure.ac:2822 puts _FORTIFY_SOURCE=3 under --enable-slower-safety.

**Suggestion.** Drop ASCII_CASE_MEMCPY from varY. If it is still wanted for clang+fortify builds on platforms without the macro, make it a separate change with its own measurement. Use the CPython idiom _Py__has_builtin(__builtin_memcpy) rather than __GNUC__ || __clang__, and avoid adding a function-like macro alias (PEP 7 prefers static inline in new code).

**Verifier (confirmed, minor).** I reproduced every number the reviewer gave, and their premises hold.

- **What the macro actually changes.** With the vector-path macro defined, ascii_case_words returns from the 16-byte path whenever len >= 16. The word loop only ever sees len 8..15 on 64-bit targets, where it runs at most once. On 32-bit ARM it sees len 4..15 and runs at most 3 times. So letting clang vectorize that loop, which is the only purpose the comment states, does nothing at runtime.
- **The vectorized copy is dead code.** In the vectorized word loop that __builtin_memcpy enables, the vector body only runs from len >= 33 on x86-64 and aarch64, and len >= 17 on ARM32 NEON. Those lengths never reach this loop.
- **Fortified plain memcpy keeps the vector path SIMD.** I checked clang 18 on aarch64-linux, arm64-apple-macos13 -mcpu=apple-m1, armv7a NEON and x86-64. No build leaves a call to __memcpy_chk anywhere.
- **macOS is covered by the vector path.** The configure check accepts __x86_64__ and __aarch64__, and Apple clang defines __aarch64__ for arm64. So macOS builds get the vector path, and the comment's rationale ("keeps clang from vectorizing the word loop") does not apply there.
- **gcc is unaffected.** At -O2 and -O3, with no fortify, =2 and =3, builtin and plain give the same instruction multiset and differ only in register allocation.
- **Precedent and idiom.** git grep finds no other __builtin_memcpy anywhere in the repo. Python/pystrhex.c already uses plain memcpy on vector types under this same macro. `_Py__has_builtin` exists in Include/pyport.h. configure.ac:2822 adds _FORTIFY_SOURCE=3 only with --enable-slower-safety.

**One nuance; it does not refute the finding.** The reviewer's word "only" is slightly too strong on x86-64. On x86-64 with clang and fortify, which includes Intel macOS, plain fortified memcpy also stops LLVM from unrolling the 16-byte loop 2x; with __builtin_memcpy (or no fortify) it is unrolled. On aarch64, Apple M1 and ARM32 the 16-byte loop is identical either way. llvm-mca puts that unroll at no throughput difference on Skylake and Alder Lake (680 vs 681 and 560 vs 560 cycles) and about 10% fewer cycles on its znver4 model (467 vs 517). That is an undocumented side effect with at most a small gain. The macro's stated justification still does not hold on platforms with the vector path. A separate, measured change, as the reviewer suggests, would be the right place for it.

## 23. Comments overstate or go stale: '-O2' applies to GCC only; the Apple-cores rationale is moot under varY

**Claim.** Three comments need correcting:
- Lines 279-281 say 'Compilers leave a loop over single words scalar at -O2'. clang vectorizes that loop at -O2 unless _FORTIFY_SOURCE is on; it is GCC's -O2 cost model that leaves it scalar.
- The PGO clause holds for gcc PGO+LTO with the current training set, but it depends on what the training runs and is untested for clang PGO.
- Lines 319-321 justify the non-MSVC loop shape with 'post-indexed accesses, slow on Apple cores'. Under varY, Apple builds (clang, x86-64/arm64) always take the vector path for 16 bytes and up, so that loop runs at most once there.

**Evidence.** - PR at clang -O2, no fortify: 94/30 SIMD.
- PR at gcc -O2 (g2 flags): 65/0.
- Built interpreters: gp-PR ascii_case_words.lto_priv.0 59/0 versus gp-varY 98/31, which confirms the gcc PGO claim.
- Standalone gcc PGO without LTO: the PR loop is scalar with 0 training calls (58/0) and SIMD with only 20 (117/19). test_bytes and test_str are in Lib/test/libregrtest/pgo.py.
- The '(SSE2 or NEON)' wording is accurate: x86-64 gives paddq/psrlq; aarch64 gives add v.2d/ushr; armv7 NEON gives vadd.i32/vshr.u32.

**Suggestion.** Say what the code does and keep the reason short and precise, e.g. '/* 16 bytes at a time with SSE2 or NEON.  GCC leaves the word loop scalar at -O2 and in cold PGO code. */'. Put the measurements in the commit message. Reword or drop the Apple-cores sentence if varY lands.

**Verifier (confirmed, minor).** I checked each of the three parts separately. Two hold up. The PGO part does not.

1) Lines 279-281 say "Compilers leave a loop over single words scalar at -O2". This is wrong for clang, so the finding holds. clang 18 at -O2 vectorizes the word loop: 94 instructions, 30 of them SIMD. Under varY that is true even with -D_FORTIFY_SOURCE=2, because ASCII_CASE_MEMCPY is __builtin_memcpy. I compiled varY with the macro removed so the word loop is the only path, and still got 94/30. Only gcc -O2 leaves it scalar (61/0, both for the PR and for varY's word-loop path). Its very-cheap cost model will not vectorize a loop whose trip count is unknown. gcc -O3 does vectorize it (122/19). So the -O2 claim is specific to GCC, not to "compilers". Also note that CPython's default OPT is -O3; -O2 is something distros choose.

2) The PGO clause does not overstate anything. The comment is already conditional ("in PGO builds whose training finds it cold"), so it already says the result depends on the training. The finding also called clang PGO untested, so I tested it with a standalone copy of the word loop, built with clang -O3 and instrumented PGO. With 0 training calls the loop is scalar (47/0). With 20 calls or more it is SIMD (84/18). Without PGO it is SIMD (96/30). gcc -O3 PGO with 0 or 20 calls is scalar (59/0). So the clause is accurate for both compilers. This part of the finding is refuted.

3) The Apple-cores sentence at lines 319-321 is moot under varY, so the finding holds. The configure check in configure.ac (around line 5493) defines _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR for any compiler with __builtin_shufflevector on x86-64, aarch64, or ARM32 with NEON. Apple clang on macOS (arm64, x86-64, or universal2) always has that builtin, so every Apple build takes the vector path when len >= 16. For len 8..15, the loop `for (i = 0; i < len - 8; i += 8)` runs at most once, so the stepping style no longer matters there. Commit 9433a66 explains its rationale as post-indexed accesses from clang on AArch64. That concern now applies only to builds that never reach Apple cores:
- clang-cl on Windows ARM64 (PC/pyconfig.h does not define the macro);
- gcc 11 or older on aarch64 (gcc added __builtin_shufflevector in GCC 12, so the macro is absent there; the commit was about clang anyway).
The sentence is still literally true, but it no longer justifies anything. It should be reworded or dropped if varY lands.

Overall: a real but small comment-accuracy issue. Parts 1 and 3 are confirmed and part 2 is refuted. The suggested wording, "GCC leaves the word loop scalar at -O2 and in cold PGO code", is accurate. Keeping the PGO clause general ("and in PGO builds whose training finds it cold") would also be correct, because it holds for clang too.

## 24. More #if paths, duplicated logic, and a generic 64-bit long-string path that GitHub CI no longer runs

**Claim.** Under varY, ascii_case_words has three compile-time paths (vector, byte-stepping word loop, MSVC count-by-one) behind four preprocessor conditionals in about 90 lines. The bit trick is written twice and 'ones' is defined three times. The PR's non-MSVC 64-bit word loop for 16 bytes and up would no longer run on any GitHub CI job: Ubuntu (gcc 12+) and macOS take the vector path, Windows takes the MSVC path. Only the 32-bit WASI job and buildbots would cover it. Meanwhile compilers still unroll or vectorize the word loop that the macro path leaves at one iteration or fewer.

**Evidence.** - Conditionals at lines 262, 278, 307 and 318.
- Bit trick at 254-257 and again at 291-292; 'ones' at 253, 288 and 304.
- CI runners: ubuntu-26.04 and ubuntu-26.04-arm (.github/workflows/build.yml), macos-26, Windows MSVC; reusable-wasi.yml runs 'make ... test' on wasm32.
- Code size of ascii_case_words: g-varY 176 versus g-PR 125; cf-varY 173 versus cf-PR 87.

**Suggestion.** If varY is kept, write the bit trick once (one static inline over a vector type, or a single shared expression). Make the mutually exclusive paths explicit with #if / #elif. Note in the PR which CI jobs cover which path.

**Verifier (confirmed, minor).** I checked each factual part of the finding and could not refute any of it. One detail about CI coverage is slightly wrong.

1. Structure (varY bytes_methods.c). The conditionals are at the lines cited: 262 (`#if __GNUC__||__clang__` for ASCII_CASE_MEMCPY), 278 (`#ifdef _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR`, the typedef and vec16), 307 (the same macro inside ascii_case_words) and 318 (`#if _MSC_VER && !__clang__`). The bit trick is written twice: once in ascii_case_bits (254-257) and again inline in ascii_case_vec16 (291-292). `ones` is defined three times (253, 288, 304); the PR already had two of these. The hunk adds 89 lines.

2. Dead loop that still gets optimized. Under the macro, the word loop is reached only for len 8..15, so `for (i=0;i<len-8;i+=8)` runs once or not at all. The disassembly of the built binaries shows the compilers still emit a SIMD body for that loop:
   - cf-varY (clang): a 2x-unrolled SSE2 loop guarded by len-9 >= 24, which cannot be true when len <= 15.
   - g-varY (gcc -O3): an SSE2 loop guarded by len-9 > 15, also impossible.

3. Code size. Instructions in ascii_case_words, counted with gdb disassemble:

   | Build | PR | varY |
   |---|---|---|
   | g (gcc -O3) | 124 | 174 |
   | cf (clang) | 86 | 173 |
   | g2 (gcc -O2) | 63 | 109 |

   In bytes (nm -S), cf is 297 vs 736 and g is 492 vs 721. These match the claimed 125/176 and 87/173.

4. CI coverage. The configure check defines the macro for x86-64, aarch64 and ARM32 with NEON, and the built pyconfig.h files confirm `#define _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR 1` under gcc 13 and clang. PC/pyconfig.h never defines it.
   - Ubuntu/BOLT/free-threading, sanitizers, CIFuzz, cross-build-linux, install and ro-srcdir all run on ubuntu-26.04 or ubuntu-26.04-arm, so they take the vector path.
   - macOS (macos-26, macos-26-intel), Android (aarch64, x86_64) and iOS (arm64) also take the vector path.
   - All Windows jobs, tail-call ones included, use MSVC: reusable-windows.yml calls build.bat with `--tail-call-interp`, and the matrix comment says msvc::musttail. So they take the count-by-one path. tail-call.yml is now Linux-only (clang on x86-64 and aarch64), so it is not a clang-cl job either.
   - So no GitHub Actions job runs the non-MSVC loop with 64-bit words for len >= 16. That source path is covered only by the 32-bit wasm builds and by buildbots.

   The slip: the finding names only WASI, but reusable-emscripten.yml also runs the full test suite (config.toml test-args are `-m test -uall`) on wasm32, so it covers the same 32-bit word loop.

The lost coverage is small. The bit trick still runs with 64-bit words on Windows x64/arm64 (MSVC path) and on Linux/macOS for len 8..15. What goes untested is only the multi-iteration loop control at stride 8, and the same source runs at stride 4 on WASI and Emscripten. "Minor" fits.

One weakness in the suggestion: the vector block is not exclusive of the generic word loop, because it falls through to that loop for len 8..15. Writing it as #if/#elif would therefore mean duplicating the generic loop.

## 25. NEWS entry and patch scope do not reflect the SIMD change

**Claim.** The PR's NEWS entry says the speed-up comes 'by converting a machine word at a time'. varY.patch touches only Objects/bytes_methods.c: no NEWS update, no tests, no configure.ac comment. The gh-144015 precedent documented the architectures and compilers in its NEWS entry.

**Evidence.** - Misc/NEWS.d/next/Core_and_Builtins/2026-11-02-05-27-54.gh-issue-161155.xXLPBV.rst.
- varY.patch applies cleanly to 4e0677ac and equals explore/varY/b/Objects/bytes_methods.c (checked with git apply and diff).
- Misc/NEWS.d/3.15.0a7.rst:863-867.

**Suggestion.** If varY is adopted, update the NEWS entry along the lines of '... 16 bytes at a time with SIMD on x86-64, ARM64 and ARM32 with NEON when built with gcc 12+ or clang'.

**Verifier (confirmed, info).** I checked every fact the finding cites, and each one holds:
- The PR's NEWS entry (Misc/NEWS.d/next/Core_and_Builtins/2026-11-02-05-27-54.gh-issue-161155.xXLPBV.rst) says the speed-up comes "by converting a machine word at a time".
- varY.patch touches only Objects/bytes_methods.c. Applied to 4e0677ac, it gives a file identical to explore/varY/b/Objects/bytes_methods.c.
- The configure.ac comment above the check (line 5495, copied into configure:20321) still reads "Used for SIMD-accelerated bytes.hex() in Python/pystrhex.c." If varY is adopted, that comment no longer lists every user of _Py_HAVE_EFFICIENT_BUILTIN_SHUFFLEVECTOR.
- The gh-144015 NEWS entry (3.15.0a7.rst, about lines 863-867) does name the architectures and the gcc 12+/clang requirement.

So there is a real, small doc gap if varY is adopted. I could not refute the claim as a whole, but parts of it overstate the problem:
1. "No NEWS update in varY.patch" comes from how the bench patches are made, not from varY. All 17 variant patches (varA through varY) are code-only diffs against main with zero NEWS hunks. The PR branch already has its NEWS file (commit b4d59af), and it would carry over unchanged. The only real question is whether the wording should change.
2. "No tests" is not specific to varY. The PR's own commits (b4d59af, a907379, 91c788f, 9433a66) touch only bytes_methods.c and the NEWS file. The existing tests use 5-character strings (string_tests.py:451-459), which never reach the word path or the vector path. The test gap is already there in the PR, so it is a PR-level gap, not something varY adds.
3. The NEWS wording is not false under varY:
   - The vector type is literally a vector of two size_t words.
   - Strings of 8-15 bytes and every build without the macro (MSVC, other architectures) still run the word loop.
   - The current PR's NEWS also leaves out that clang and MSVC auto-vectorize the word loop.
4. The gh-144015 precedent applies only weakly. That entry had to name architectures because its speed-up existed only on those platforms. Under varY, the speed-up applies on every platform, and SIMD only widens it.

What remains: if varY is adopted, the configure.ac/configure comment needs a one-line edit, which means regenerating configure. Changing the NEWS wording is optional. This has no effect on behaviour or correctness, so I rate it info rather than minor.

## 26. AI-tools policy points that matter for presenting varY

**Claim.** The devguide policy makes the submitter responsible for every line and requires them to 'be able to explain their proposed changes in their own words' and to describe how correctness was verified. It asks contributors to consider necessity, keep changes minimal and focused, follow existing patterns and write tests, and it singles out AI-generated testing advice for scrutiny. Maintainers can apply the AI-needs-explanation label or close a PR with AI-guidelines-not-met. Disclosing AI use is encouraged but not required. varY's overstated comments and the missing tests are the kind of thing that draws those labels. Adding a fifth loop design to an open PR that already has four commits of loop-shape churn reads as unfocused.

**Evidence.** - https://devguide.python.org/getting-started/ai-tools/ (fetched).
- AGENTS.md in the checkout repeats the core principles.
- The PR's commits are b4d59af, a907379, 91c788f and 9433a66; 91c788f and 9433a66 change the loop shape.

**Suggestion.** Keep varY, or the portable variant, out of the current PR. In any follow-up, state in the author's own words what was verified (sanitizer harness, the check_all.py exhaustive checker, codegen per compiler) and which builds gain. Disclose AI assistance, and make sure every claim in the code comments has been checked.

**Verifier (confirmed, info).** I could not refute the substance. Two details are wrong or loosely worded.

What checks out:
1. Policy text. I fetched the raw devguide page and it matches the finding:
   - "be able to explain their proposed changes in their own words".
   - The principles: necessity, "Make minimal, focused changes", existing style and patterns, "Write tests that exercise the change", backwards compatibility.
   - "Pay close attention to AI generated recommendations for testing changes."
   - Disclosure "is appreciated, while not required".
   - The page values "well scoped PRs without unneeded code churn".
   - Labels: AI-needs-explanation keeps the PR open, and the author must reply in their own words and "describe how you checked that it is correct". AI-guidelines-not-met closes it.
2. Overstated comments. varY's vector-block comment says "Compilers leave a loop over single words scalar at -O2". That is true only for gcc:
   - The PR's ascii_case_words built with clang -O2 contains 30 xmm instructions.
   - varY built without the macro under clang -O2, with or without -D_FORTIFY_SOURCE=2, also gets 30 xmm instructions, because its __builtin_memcpy change fixes the fortify block.
   - gcc -O2 gets 0. So the comment over-generalizes, and partly because of varY's own memcpy change.
   - The _FORTIFY_SOURCE comment holds for glibc: clang -O2 -D_FORTIFY_SOURCE=2 or 3 on the PR code gives 0 xmm instructions. I could not check the macOS SDK part here.
3. Missing tests. Neither the PR nor varY adds tests.
   - The shared lower/upper tests in Lib/test/string_tests.py use 'HeLLo' (5 bytes), below the 8-byte word threshold and the 16-byte vector threshold.
   - test_str adds only non-ASCII cases.
   - test_bigmem runs only with -M.
   - The free-threading test in test_bytes.py (around line 3215) runs lower() and upper() on 4 MiB bytearrays but checks only one byte.
   - Nothing targets lengths 7/8/15/16/17, the letter-range edge bytes (0x40/0x5B, 0x60/0x7B), or bytes ≥0x80. The exhaustive checkers live outside the repo.

Corrections:
- "Four commits of loop-shape churn" and "fifth loop design" are wrong by the finding's own evidence. b4d59af introduces the loop. a907379 changes comments only; I checked its diff and no code lines change. Only 91c788f and 9433a66 change the loop, and 9433a66 partly reverts 91c788f outside MSVC. varY would be the fourth loop design, not the fifth. The underlying point, that more loop churn on an open PR reads as unfocused, still holds.
- The "describe how correctness was verified" requirement is the reply the AI-needs-explanation label asks for, not a blanket rule. Outside the label, the page only requires authors to review AI output in detail and to write tests.
- Saying these issues would "draw those labels" is a judgment, not something I can verify. The policy also says AI use alone is not a reason to label a PR.

The advice itself (keep varY out of the current PR, say in your own words what was verified, check every claim in the comments) is consistent with the policy.
