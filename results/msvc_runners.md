# MSVC 19.51 on GitHub runners: main / build (pyperf)

The `variants` workflow (runs 41760501953 for release and 41760498215 for PGO): `bench.py` with pyperf, one code layout per job, not pinned. `str.lower` on inputs that cycle through all 128 ASCII characters; mean of all values. PR = `varJ` (the PR's code).

| Build | Runner | CPU | Length | PR | varR |
|---|---|---|---|---|---|
| PGO | windows-11-arm-pgo-1 | Cobalt 100 | 1024 | 2.40x | 2.75x |
| PGO | windows-11-arm-pgo-1 | Cobalt 100 | 65536 | 3.03x | 3.83x |
| PGO | windows-11-arm-pgo-2 | Cobalt 100 | 1024 | 2.36x | 2.79x |
| PGO | windows-11-arm-pgo-2 | Cobalt 100 | 65536 | 3.02x | 3.88x |
| PGO | windows-2025-pgo-1 | AMD EPYC 7763 64-Core | 1024 | 2.08x | 3.28x |
| PGO | windows-2025-pgo-1 | AMD EPYC 7763 64-Core | 65536 | 2.40x | 5.28x |
| PGO | windows-2025-pgo-2 | AMD EPYC 9V74 80-Core | 1024 | 2.05x | 3.21x |
| PGO | windows-2025-pgo-2 | AMD EPYC 9V74 80-Core | 65536 | 2.14x | 5.34x |
| Release | windows-11-arm-release-1 | Cobalt 100 | 1024 | 2.16x | 2.47x |
| Release | windows-11-arm-release-1 | Cobalt 100 | 65536 | 2.96x | 3.83x |
| Release | windows-11-arm-release-2 | Cobalt 100 | 1024 | 2.15x | 2.46x |
| Release | windows-11-arm-release-2 | Cobalt 100 | 65536 | 3.00x | 3.84x |
| Release | windows-2025-release-1 | AMD EPYC 7763 64-Core | 1024 | 2.97x | 3.05x |
| Release | windows-2025-release-1 | AMD EPYC 7763 64-Core | 65536 | 5.49x | 5.86x |
| Release | windows-2025-release-2 | AMD EPYC 9V45 96-Core | 1024 | 3.53x | 3.84x |
| Release | windows-2025-release-2 | AMD EPYC 9V45 96-Core | 65536 | 5.61x | 6.17x |
