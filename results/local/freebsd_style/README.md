# FreeBSD-style build: clang 18.1 `-O2` + ThinLTO, no PGO (Ryzen 7 9800X3D, WSL2)

FreeBSD's `lang/python313` and `lang/python314` ports set `OPT=""`, build with the ports' default CFLAGS and turn LTO on by default (no PGO option). Reproduced with:

    PATH=/usr/lib/llvm-18/bin:$PATH REPLAY_CPU=4 realworld/layout_local.sh WORK "varJ varR varT varN" \
      CC=clang OPT= "CFLAGS=-O2 -pipe -fstack-protector-strong -fno-strict-aliasing" --with-lto

Configure picked `-flto=thin`. SIMD (xmm) instructions in `ascii_case_words`: varJ 30, varR 99, varT 83, varN 83. Every build passed edge_cases.py (253,814 cases) and check_all.py (1,495,930 cases). `lengths.md`: fixed lengths; `layout.md`: the short-string replay; 8 shifts each.
