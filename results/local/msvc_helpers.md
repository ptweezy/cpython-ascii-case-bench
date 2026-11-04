# MSVC 19.51: each variant's helpers alone

`oldcc/make_test.py` output for each variant (the helpers copied from the patched `Objects/bytes_methods.c`, plus the exhaustive check), built with `cl /W3` for x64 and x86 at `/O2` and `/O1 /Oi` (a stand-in for code that PGO finds cold) on the Ryzen 7 9800X3D, and run. SIMD: instructions with an xmm operand in `ascii_case_words`, from the `/FAs` listing (`explore/msvcB/count.py`).

| Variant | Target | Flags | Check | SIMD instructions (with an xmm operand) in ascii_case_words | Warnings |
|---|---|---|---|---|---|
| PR | x64 | /O2 | 346327040 bytes checked, 0 wrong: ok | 45 | 0 |
| PR | x64 | /O1 /Oi | 346327040 bytes checked, 0 wrong: ok | 0 | 0 |
| varR | x64 | /O2 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| varR | x64 | /O1 /Oi | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| varN | x64 | /O2 | 346327040 bytes checked, 0 wrong: ok | 35 | 0 |
| varN | x64 | /O1 /Oi | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| varB | x64 | /O2 | 346327040 bytes checked, 0 wrong: ok | 70 | 0 |
| varB | x64 | /O1 /Oi | 346327040 bytes checked, 0 wrong: ok | 32 | 0 |
| PR | x86 | /O2 | 346456064 bytes checked, 0 wrong: ok | 46 | 0 |
| PR | x86 | /O1 /Oi | 346456064 bytes checked, 0 wrong: ok | 0 | 0 |
| varR | x86 | /O2 | 346456064 bytes checked, 0 wrong: ok | 43 | 0 |
| varR | x86 | /O1 /Oi | 346456064 bytes checked, 0 wrong: ok | 0 | 0 |
| varN | x86 | /O2 | 346456064 bytes checked, 0 wrong: ok | 43 | 0 |
| varN | x86 | /O1 /Oi | 346456064 bytes checked, 0 wrong: ok | 0 | 0 |
| varB | x86 | /O2 | 346456064 bytes checked, 0 wrong: ok | 46 | 0 |
| varB | x86 | /O1 /Oi | 346456064 bytes checked, 0 wrong: ok | 0 | 0 |
