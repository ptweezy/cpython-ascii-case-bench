# MSVC 19.51 on GitHub runners: `varB` next to the PR (pyperf and the replay)

The `variants` workflow with `variants="varJ varB"`: runs 41839922874 (PGO, x64 and ARM64) and 41839935849 (Release), then 41856413089 (x64 PGO, 6 jobs), 41856431217 (x64 Release, 4 jobs) and 41856451197 (ARM64 PGO, 2 jobs). Each job builds `main`, the PR (`varJ`) and `varB` once, so each tree is one build at one code layout; the replay is pinned to one CPU at high priority, the pyperf lengths aren't. Lengths: `bench.py` with pyperf, `str.lower` on inputs that cycle through all 128 ASCII characters, main / build from the mean of all values (`analysis/win_pyperf.py`). Short mix: the real-world replay, geometric mean over the eight short workloads of main / build, by median and by best time (`analysis/win_short.py`).

## Lengths

| Build | Job | CPU | Tree | 16 | 64 | 256 | 1024 | 65536 |
|---|---|---|---|---|---|---|---|---|
| pgo | variants-windows-11-arm-pgo-1 | Cobalt 100 | PR | 1.09x | 1.30x | 1.87x | 2.39x | 3.00x |
| pgo | variants-windows-11-arm-pgo-1 | Cobalt 100 | varB | 1.10x | 1.44x | 2.18x | 2.76x | 3.86x |
| pgo | variants-windows-11-arm-pgo-2 | Cobalt 100 | PR | 1.11x | 1.29x | 1.87x | 2.36x | 3.00x |
| pgo | variants-windows-11-arm-pgo-2 | Cobalt 100 | varB | 1.11x | 1.43x | 2.20x | 2.77x | 3.84x |
| pgo | variants-windows-2025-pgo-1 | AMD EPYC 9V74 80-Core | PR | 1.11x | 1.06x | 1.75x | 2.06x | 2.11x |
| pgo | variants-windows-2025-pgo-1 | AMD EPYC 9V74 80-Core | varB | 1.09x | 1.20x | 2.16x | 3.08x | 4.86x |
| pgo | variants-windows-2025-pgo-2 | INTEL(R) XEON(R) PLATINUM 8573C | PR | 1.03x | 1.30x | 1.87x | 2.35x | 3.18x |
| pgo | variants-windows-2025-pgo-2 | INTEL(R) XEON(R) PLATINUM 8573C | varB | 1.05x | 1.41x | 2.51x | 2.72x | 5.08x |
| pgo | variants-windows-2025-pgo-1 | AMD EPYC 9V45 96-Core | PR | 1.09x | 1.28x | 2.04x | 2.28x | 2.38x |
| pgo | variants-windows-2025-pgo-1 | AMD EPYC 9V45 96-Core | varB | 1.10x | 1.49x | 2.89x | 3.85x | 5.36x |
| pgo | variants-windows-2025-pgo-2 | AMD EPYC 7763 64-Core | PR | 1.10x | 1.39x | 1.88x | 2.14x | 2.26x |
| pgo | variants-windows-2025-pgo-2 | AMD EPYC 7763 64-Core | varB | 1.07x | 1.48x | 2.35x | 3.16x | 4.99x |
| pgo | variants-windows-2025-pgo-3 | AMD EPYC 7763 64-Core | PR | 1.21x | 1.62x | 2.73x | 3.31x | 3.97x |
| pgo | variants-windows-2025-pgo-3 | AMD EPYC 7763 64-Core | varB | 1.22x | 1.77x | 3.55x | 4.79x | 8.85x |
| pgo | variants-windows-2025-pgo-4 | AMD EPYC 7763 64-Core | PR | 1.09x | 1.63x | 1.94x | 1.85x | 2.38x |
| pgo | variants-windows-2025-pgo-4 | AMD EPYC 7763 64-Core | varB | 1.12x | 1.75x | 2.46x | 3.11x | 5.29x |
| pgo | variants-windows-2025-pgo-5 | AMD EPYC 9V74 80-Core | PR | 1.08x | 1.32x | 1.70x | 2.06x | 2.08x |
| pgo | variants-windows-2025-pgo-5 | AMD EPYC 9V74 80-Core | varB | 1.11x | 1.33x | 2.04x | 3.18x | 5.34x |
| pgo | variants-windows-2025-pgo-6 | INTEL(R) XEON(R) PLATINUM 8573C | PR | 1.06x | 1.29x | 1.95x | 2.29x | 2.99x |
| pgo | variants-windows-2025-pgo-6 | INTEL(R) XEON(R) PLATINUM 8573C | varB | 1.08x | 1.40x | 2.56x | 3.07x | 5.06x |
| release | variants-windows-11-arm-release-1 | Cobalt 100 | PR | 1.06x | 1.22x | 1.66x | 2.16x | 3.01x |
| release | variants-windows-11-arm-release-1 | Cobalt 100 | varB | 1.06x | 1.27x | 1.81x | 2.47x | 3.92x |
| release | variants-windows-2025-release-1 | INTEL(R) XEON(R) PLATINUM 8573C | PR | 1.06x | 1.20x | 2.05x | 2.86x | 5.02x |
| release | variants-windows-2025-release-1 | INTEL(R) XEON(R) PLATINUM 8573C | varB | 1.06x | 1.22x | 2.08x | 3.03x | 5.34x |
| release | variants-windows-2025-release-1 | AMD EPYC 7763 64-Core | PR | 1.01x | 1.25x | 2.02x | 2.92x | 5.39x |
| release | variants-windows-2025-release-1 | AMD EPYC 7763 64-Core | varB | 0.99x | 1.20x | 2.00x | 3.10x | 5.76x |
| release | variants-windows-2025-release-2 | INTEL(R) XEON(R) PLATINUM 8573C | PR | 1.08x | 1.19x | 2.03x | 2.46x | 5.06x |
| release | variants-windows-2025-release-2 | INTEL(R) XEON(R) PLATINUM 8573C | varB | 1.06x | 1.20x | 2.05x | 2.98x | 5.38x |
| release | variants-windows-2025-release-3 | AMD EPYC 9V74 80-Core | PR | 1.01x | 1.22x | 1.91x | 2.96x | 5.41x |
| release | variants-windows-2025-release-3 | AMD EPYC 9V74 80-Core | varB | 1.00x | 1.21x | 1.89x | 3.10x | 5.87x |
| release | variants-windows-2025-release-4 | AMD EPYC 9V45 96-Core | PR | 1.03x | 1.25x | 2.30x | 3.04x | 5.68x |
| release | variants-windows-2025-release-4 | AMD EPYC 9V45 96-Core | varB | 1.00x | 1.23x | 2.34x | 3.76x | 6.03x |
| pgo | variants-windows-11-arm-pgo-1 | Cobalt 100 | PR | 1.10x | 1.27x | 1.86x | 2.37x | 2.97x |
| pgo | variants-windows-11-arm-pgo-1 | Cobalt 100 | varB | 1.10x | 1.44x | 2.16x | 2.75x | 3.91x |
| pgo | variants-windows-11-arm-pgo-2 | Cobalt 100 | PR | 1.09x | 1.27x | 1.86x | 2.33x | 3.01x |
| pgo | variants-windows-11-arm-pgo-2 | Cobalt 100 | varB | 1.10x | 1.41x | 2.12x | 2.77x | 3.93x |

## Short mix

| Job | Build | CPU | PR (median) | varB (median) | PR (best) | varB (best) |
|---|---|---|---|---|---|---|
| variants-windows-11-arm-pgo-1 | ARM64 pgo | Cobalt 100 | 1.018 | 1.078 | 1.018 | 1.020 |
| variants-windows-11-arm-pgo-2 | ARM64 pgo | Cobalt 100 | 1.046 | 0.945 | 0.983 | 0.992 |
| variants-windows-2025-pgo-1 | x64 pgo | AMD EPYC 9V74 80-Core | 1.064 | 1.019 | 1.078 | 1.021 |
| variants-windows-2025-pgo-2 | x64 pgo | INTEL(R) XEON(R) PLATINUM 8573C | 1.056 | 0.989 | 1.070 | 1.018 |
| variants-windows-2025-pgo-1 | x64 pgo | AMD EPYC 9V45 96-Core | 0.979 | 1.013 | 1.022 | 1.034 |
| variants-windows-2025-pgo-2 | x64 pgo | AMD EPYC 7763 64-Core | 0.924 | 0.839 | 0.982 | 0.941 |
| variants-windows-2025-pgo-3 | x64 pgo | AMD EPYC 7763 64-Core | 1.018 | 0.923 | 1.006 | 0.913 |
| variants-windows-2025-pgo-4 | x64 pgo | AMD EPYC 7763 64-Core | 0.966 | 0.930 | 1.004 | 0.970 |
| variants-windows-2025-pgo-5 | x64 pgo | AMD EPYC 9V74 80-Core | 1.021 | 1.094 | 1.023 | 1.036 |
| variants-windows-2025-pgo-6 | x64 pgo | INTEL(R) XEON(R) PLATINUM 8573C | 1.078 | 1.170 | 1.084 | 1.102 |
| variants-windows-11-arm-release-1 | ARM64 release | Cobalt 100 | 1.024 | 1.006 | 1.023 | 1.005 |
| variants-windows-2025-release-1 | x64 release | INTEL(R) XEON(R) PLATINUM 8573C | 0.982 | 0.969 | 0.969 | 0.973 |
| variants-windows-2025-release-1 | x64 release | AMD EPYC 7763 64-Core | 0.965 | 0.979 | 0.968 | 0.982 |
| variants-windows-2025-release-2 | x64 release | INTEL(R) XEON(R) PLATINUM 8573C | 1.021 | 0.989 | 1.000 | 0.982 |
| variants-windows-2025-release-3 | x64 release | AMD EPYC 9V74 80-Core | 0.969 | 0.977 | 0.972 | 0.991 |
| variants-windows-2025-release-4 | x64 release | AMD EPYC 9V45 96-Core | 0.983 | 0.987 | 0.987 | 1.002 |
| variants-windows-11-arm-pgo-1 | ARM64 pgo | Cobalt 100 | 1.115 | 1.050 | 1.057 | 1.046 |
| variants-windows-11-arm-pgo-2 | ARM64 pgo | Cobalt 100 | 1.087 | 0.958 | 1.038 | 1.014 |

| Build | Statistic | Jobs | varB / PR | 95% interval |
|---|---|---|---|---|
| ARM64 pgo | best | 4 | 0.994 | 0.980-1.008 |
| ARM64 pgo | median | 4 | 0.944 | 0.870-1.023 |
| x64 pgo | best | 8 | 0.971 | 0.943-0.999 |
| x64 pgo | median | 8 | 0.981 | 0.932-1.032 |
| x64 release | best | 5 | 1.007 | 0.993-1.021 |
| x64 release | median | 5 | 0.996 | 0.979-1.013 |
| all | median | 18 | 0.977 | 0.949-1.005 |
| all | best | 18 | 0.986 | 0.972-1.001 |
