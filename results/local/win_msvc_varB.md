# Windows (Ryzen 7 9800X3D), MSVC 19.51: varB next to main, the PR and varR

x64 PGO (`PCbuild/build.bat --pgo`, as python.org's 64-bit installers) and Win32 Release (`-p Win32 -c Release`, as python.org's 32-bit installer). `explore`-style timing: fixed lengths (`realworld/len_layout.py`, str.lower, 5 rounds) and the real-world replay (15 rounds), pinned to CPU 4 at high priority; one code layout per build. Every build passed edge_cases.py and check_all.py.

```
##### x64-pgo-B lengths (06:38:00)
main / build, geometric mean over shifts (range over shifts of ns / mean):
| Length | main ns | PR | varB | varR |
|---|---|---|---|---|
| 8 | 33.2 | 1.01x (1.00-1.00) | 1.00x (1.00-1.00) | 1.00x (1.00-1.00) |
| 16 | 34.9 | 1.06x (1.00-1.00) | 1.07x (1.00-1.00) | 1.05x (1.00-1.00) |
| 24 | 37.8 | 1.11x (1.00-1.00) | 1.13x (1.00-1.00) | 1.12x (1.00-1.00) |
| 32 | 39.0 | 1.17x (1.00-1.00) | 1.19x (1.00-1.00) | 1.17x (1.00-1.00) |
| 64 | 47.4 | 1.32x (1.00-1.00) | 1.41x (1.00-1.00) | 1.40x (1.00-1.00) |
| 128 | 60.0 | 1.50x (1.00-1.00) | 1.71x (1.00-1.00) | 1.69x (1.00-1.00) |
| 256 | 107.5 | 2.21x (1.00-1.00) | 2.82x (1.00-1.00) | 2.74x (1.00-1.00) |
| 1,024 | 269.8 | 2.28x (1.00-1.00) | 3.36x (1.00-1.00) | 3.34x (1.00-1.00) |
| 4,096 | 855.5 | 2.45x (1.00-1.00) | 4.33x (1.00-1.00) | 4.38x (1.00-1.00) |
| 65,536 | 12708.4 | 2.64x (1.00-1.00) | 5.72x (1.00-1.00) | 5.71x (1.00-1.00) |
##### x64-pgo-B replay (06:38:03)
best ns per call: | Workload | base | PR | varR | varB |
| config | 38.2 | 37.2 | 38.0 | 38.2 |
| doclower | 3234.0 | 1277.7 | 649.0 | 647.3 |
| email | 37.3 | 36.7 | 36.7 | 36.9 |
| html | 36.4 | 36.6 | 36.2 | 36.4 |
| http | 38.1 | 34.1 | 35.0 | 34.6 |
| paths | 35.5 | 35.6 | 36.0 | 35.3 |
| pgotask | 38.4 | 38.4 | 38.4 | 38.2 |
| urls | 36.7 | 35.2 | 35.9 | 36.0 |
| words | 37.6 | 37.9 | 38.7 | 38.2 |
main / build (best): | Workload | PR | varR | varB |
| config | 1.03x | 1.00x | 1.00x |
| doclower | 2.53x | 4.98x | 5.00x |
| email | 1.02x | 1.02x | 1.01x |
| html | 0.99x | 1.01x | 1.00x |
| http | 1.12x | 1.09x | 1.10x |
| paths | 1.00x | 0.98x | 1.00x |
| pgotask | 1.00x | 1.00x | 1.00x |
| urls | 1.04x | 1.02x | 1.02x |
| words | 0.99x | 0.97x | 0.98x |
median ns per call: | Workload | base | PR | varR | varB |
| config | 43.3 | 39.3 | 43.9 | 41.3 |
| doclower | 3245.9 | 1284.1 | 660.5 | 652.0 |
| email | 41.8 | 40.0 | 41.6 | 39.5 |
| html | 41.0 | 38.7 | 41.3 | 39.3 |
| http | 42.7 | 37.1 | 40.5 | 37.4 |
| paths | 40.3 | 38.2 | 40.6 | 37.8 |
| pgotask | 44.0 | 41.5 | 43.6 | 41.0 |
| urls | 42.0 | 37.3 | 40.7 | 38.7 |
| words | 42.9 | 40.8 | 43.3 | 41.0 |
main / build (median): | Workload | PR | varR | varB |
| config | 1.10x | 0.99x | 1.05x |
| doclower | 2.53x | 4.91x | 4.98x |
| email | 1.04x | 1.00x | 1.06x |
| html | 1.06x | 0.99x | 1.04x |
| http | 1.15x | 1.06x | 1.14x |
| paths | 1.06x | 0.99x | 1.07x |
| pgotask | 1.06x | 1.01x | 1.07x |
| urls | 1.13x | 1.03x | 1.09x |
| words | 1.05x | 0.99x | 1.05x |
##### win32-rel-B lengths (06:38:44)
main / build, geometric mean over shifts (range over shifts of ns / mean):
| Length | main ns | PR | varB | varR |
|---|---|---|---|---|
| 8 | 72.2 | 1.02x (1.00-1.00) | 1.07x (1.00-1.00) | 1.07x (1.00-1.00) |
| 16 | 66.6 | 0.92x (1.00-1.00) | 0.97x (1.00-1.00) | 0.98x (1.00-1.00) |
| 24 | 67.9 | 0.93x (1.00-1.00) | 0.96x (1.00-1.00) | 0.99x (1.00-1.00) |
| 32 | 73.1 | 1.00x (1.00-1.00) | 1.04x (1.00-1.00) | 1.07x (1.00-1.00) |
| 64 | 76.6 | 1.02x (1.00-1.00) | 1.06x (1.00-1.00) | 1.08x (1.00-1.00) |
| 128 | 90.3 | 1.16x (1.00-1.00) | 1.17x (1.00-1.00) | 1.26x (1.00-1.00) |
| 256 | 123.6 | 1.53x (1.00-1.00) | 1.56x (1.00-1.00) | 1.60x (1.00-1.00) |
| 1,024 | 314.3 | 2.14x (1.00-1.00) | 2.15x (1.00-1.00) | 2.09x (1.00-1.00) |
| 4,096 | 912.3 | 3.30x (1.00-1.00) | 3.31x (1.00-1.00) | 2.89x (1.00-1.00) |
| 65,536 | 13081.1 | 4.42x (1.00-1.00) | 4.44x (1.00-1.00) | 3.67x (1.00-1.00) |
##### win32-rel-B replay (06:38:49)
best ns per call: | Workload | base | PR | varR | varB |
| config | 74.3 | 75.8 | 73.7 | 74.3 |
| doclower | 3358.2 | 873.8 | 1019.0 | 865.2 |
| email | 77.2 | 78.6 | 76.6 | 77.2 |
| html | 75.1 | 77.9 | 75.0 | 74.4 |
| http | 79.4 | 79.9 | 78.1 | 78.2 |
| paths | 78.1 | 80.4 | 75.1 | 78.5 |
| pgotask | 73.4 | 74.9 | 74.0 | 73.6 |
| urls | 80.0 | 74.6 | 73.9 | 73.7 |
| words | 71.7 | 73.9 | 72.2 | 72.4 |
main / build (best): | Workload | PR | varR | varB |
| config | 0.98x | 1.01x | 1.00x |
| doclower | 3.84x | 3.30x | 3.88x |
| email | 0.98x | 1.01x | 1.00x |
| html | 0.96x | 1.00x | 1.01x |
| http | 0.99x | 1.02x | 1.02x |
| paths | 0.97x | 1.04x | 0.99x |
| pgotask | 0.98x | 0.99x | 1.00x |
| urls | 1.07x | 1.08x | 1.09x |
| words | 0.97x | 0.99x | 0.99x |
median ns per call: | Workload | base | PR | varR | varB |
| config | 76.4 | 77.5 | 76.6 | 76.9 |
| doclower | 3380.0 | 879.0 | 1026.2 | 872.4 |
| email | 79.6 | 81.0 | 79.3 | 79.8 |
| html | 76.3 | 79.6 | 77.3 | 78.1 |
| http | 81.2 | 81.7 | 81.0 | 80.8 |
| paths | 80.2 | 81.9 | 78.0 | 80.6 |
| pgotask | 75.1 | 76.6 | 76.5 | 75.7 |
| urls | 80.7 | 76.0 | 76.3 | 75.9 |
| words | 73.3 | 75.6 | 75.0 | 74.8 |
main / build (median): | Workload | PR | varR | varB |
| config | 0.99x | 1.00x | 0.99x |
| doclower | 3.85x | 3.29x | 3.87x |
| email | 0.98x | 1.00x | 1.00x |
| html | 0.96x | 0.99x | 0.98x |
| http | 0.99x | 1.00x | 1.01x |
| paths | 0.98x | 1.03x | 0.99x |
| pgotask | 0.98x | 0.98x | 0.99x |
| urls | 1.06x | 1.06x | 1.06x |
| words | 0.97x | 0.98x | 0.98x |
done 06:40:05
```

## Earlier: Win32 Release and PGO, main / PR / varR

```
##### Win32 MSVC rel lengths (05:51:15)
main / build, geometric mean over shifts (range over shifts of ns / mean):
| Length | main ns | PR | varR |
|---|---|---|---|
| 8 | 73.0 | 1.03x (1.00-1.00) | 1.04x (1.00-1.00) |
| 16 | 71.8 | 1.00x (1.00-1.00) | 1.00x (1.00-1.00) |
| 24 | 72.6 | 1.00x (1.00-1.00) | 1.00x (1.00-1.00) |
| 32 | 72.2 | 0.99x (1.00-1.00) | 0.99x (1.00-1.00) |
| 64 | 79.9 | 1.07x (1.00-1.00) | 1.06x (1.00-1.00) |
| 128 | 91.1 | 1.18x (1.00-1.00) | 1.22x (1.00-1.00) |
| 256 | 126.5 | 1.57x (1.00-1.00) | 1.58x (1.00-1.00) |
| 1,024 | 311.9 | 2.13x (1.00-1.00) | 2.06x (1.00-1.00) |
| 4,096 | 913.0 | 3.30x (1.00-1.00) | 2.81x (1.00-1.00) |
| 65,536 | 13128.2 | 4.44x (1.00-1.00) | 3.67x (1.00-1.00) |
##### Win32 MSVC rel replay (05:51:18)
best ns per call: | Workload | base | PR | varR |
| config | 72.1 | 74.4 | 74.2 |
| doclower | 3363.8 | 874.8 | 1040.5 |
| email | 72.0 | 73.7 | 73.1 |
| html | 75.3 | 78.4 | 79.5 |
| http | 72.3 | 73.5 | 74.2 |
| paths | 75.5 | 80.3 | 80.5 |
| pgotask | 73.2 | 75.0 | 75.0 |
| urls | 76.6 | 73.5 | 73.7 |
| words | 71.7 | 73.8 | 74.0 |
main / build (best): | Workload | PR | varR |
| config | 0.97x | 0.97x |
| doclower | 3.85x | 3.23x |
| email | 0.98x | 0.99x |
| html | 0.96x | 0.95x |
| http | 0.98x | 0.98x |
| paths | 0.94x | 0.94x |
| pgotask | 0.98x | 0.98x |
| urls | 1.04x | 1.04x |
| words | 0.97x | 0.97x |
median ns per call: | Workload | base | PR | varR |
| config | 74.2 | 75.4 | 74.5 |
| doclower | 3369.8 | 879.9 | 1045.9 |
| email | 73.7 | 74.6 | 73.6 |
| html | 76.3 | 79.3 | 79.9 |
| http | 74.2 | 74.9 | 74.6 |
| paths | 79.6 | 81.7 | 81.0 |
| pgotask | 74.4 | 76.0 | 75.2 |
| urls | 78.2 | 74.4 | 73.9 |
| words | 73.2 | 75.0 | 74.5 |
main / build (median): | Workload | PR | varR |
| config | 0.98x | 1.00x |
| doclower | 3.83x | 3.22x |
| email | 0.99x | 1.00x |
| html | 0.96x | 0.96x |
| http | 0.99x | 1.00x |
| paths | 0.98x | 0.98x |
| pgotask | 0.98x | 0.99x |
| urls | 1.05x | 1.06x |
| words | 0.98x | 0.98x |
##### Win32 MSVC pgo lengths (05:52:15)
main / build, geometric mean over shifts (range over shifts of ns / mean):
| Length | main ns | PR | varR |
|---|---|---|---|
| 8 | 40.8 | 0.97x (1.00-1.00) | 0.94x (1.00-1.00) |
| 16 | 43.1 | 1.00x (1.00-1.00) | 0.87x (1.00-1.00) |
| 24 | 44.7 | 1.00x (1.00-1.00) | 0.79x (1.00-1.00) |
| 32 | 46.2 | 1.01x (1.00-1.00) | 0.80x (1.00-1.00) |
| 64 | 53.2 | 1.06x (1.00-1.00) | 0.78x (1.00-1.00) |
| 128 | 65.6 | 1.08x (1.00-1.00) | 0.73x (1.00-1.00) |
| 256 | 114.6 | 1.40x (1.00-1.00) | 0.86x (1.00-1.00) |
| 1,024 | 300.9 | 1.10x (1.00-1.00) | 0.69x (1.00-1.00) |
| 4,096 | 884.8 | 1.03x (1.00-1.00) | 0.59x (1.00-1.00) |
| 65,536 | 12891.2 | 1.02x (1.00-1.00) | 0.56x (1.00-1.00) |
##### Win32 MSVC pgo replay (05:52:21)
best ns per call: | Workload | base | PR | varR |
| config | 44.6 | 44.5 | 49.0 |
| doclower | 3303.0 | 3232.0 | 5745.1 |
| email | 47.3 | 46.4 | 46.3 |
| html | 42.0 | 41.9 | 43.1 |
| http | 48.5 | 47.2 | 45.7 |
| paths | 43.8 | 43.9 | 44.9 |
| pgotask | 43.8 | 43.2 | 46.3 |
| urls | 42.5 | 42.5 | 47.7 |
| words | 42.7 | 42.8 | 45.2 |
main / build (best): | Workload | PR | varR |
| config | 1.00x | 0.91x |
| doclower | 1.02x | 0.57x |
| email | 1.02x | 1.02x |
| html | 1.00x | 0.98x |
| http | 1.03x | 1.06x |
| paths | 1.00x | 0.98x |
| pgotask | 1.02x | 0.95x |
| urls | 1.00x | 0.89x |
| words | 1.00x | 0.95x |
median ns per call: | Workload | base | PR | varR |
| config | 47.6 | 47.0 | 51.8 |
| doclower | 3313.0 | 3236.6 | 5758.6 |
| email | 50.3 | 49.0 | 49.0 |
| html | 44.6 | 44.4 | 45.5 |
| http | 51.4 | 49.8 | 48.2 |
| paths | 46.3 | 46.3 | 47.9 |
| pgotask | 46.6 | 45.9 | 49.1 |
| urls | 45.3 | 45.1 | 50.7 |
| words | 45.6 | 45.5 | 47.6 |
main / build (median): | Workload | PR | varR |
| config | 1.01x | 0.92x |
| doclower | 1.02x | 0.58x |
| email | 1.03x | 1.03x |
| html | 1.00x | 0.98x |
| http | 1.03x | 1.07x |
| paths | 1.00x | 0.97x |
| pgotask | 1.01x | 0.95x |
| urls | 1.00x | 0.89x |
| words | 1.00x | 0.96x |
done 05:52:58
```
