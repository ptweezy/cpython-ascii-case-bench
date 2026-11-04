# MSVC 19.51: SIMD instructions in ascii_case_words of each Python build

Local Windows builds (Ryzen 7 9800X3D, `PCbuild/<arch>-<tree>-<build>`): the function's address and size from `python316.pdb` (`llvm-pdbutil dump --symbols`), disassembled with `llvm-objdump`; instructions with an xmm/ymm operand counted. `blkR` is `varR`.

| Build | PR (`varJ`) | `varR` | `varB` |
|---|---|---|---|
| x64 PGO (`PCbuild/build.bat --pgo`) | 0 (194 bytes) | 32 (383 bytes) | 32 (386 bytes) |
| x64 Release (`/O2`) | 45 (521 bytes) | 35 (436 bytes) | 70 (691 bytes) |
| x86 (32-bit) PGO | 0 (156 bytes) | 0 (358 bytes) | not built (the PR's code) |
| x86 (32-bit) Release | 46 (460 bytes) | 43 (596 bytes) | 46 (460 bytes) |
| x64 PGO with the proposed tests in `Lib/test` (the training runs them) | 0 (194 bytes) | not built | 32 (386 bytes) |

In the 32-bit Release build `varR`'s block is vectorized behind a run-time CPU check (`___isa_available`) and copies each block through the stack; in the 32-bit PGO build it is scalar. `varB`'s 32-bit function has the PR's size and instruction count.

With the proposed tests in the PGO training (`PCbuild/amd64-PRt-pgo`, `PCbuild/amd64-varBt-pgo`; both passed `test_bytes` and `test_str` during training), MSVC still leaves the PR's loop scalar: its `ascii_case_words` has the same instructions as without the tests (addresses aside). `varB`'s has the same size and SIMD count, with small differences elsewhere in the function.
