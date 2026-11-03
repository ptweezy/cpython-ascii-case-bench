"""Share of lower()/upper() calls and characters by length, per workload."""
import glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
BUCKETS = [("0", 0, 0), ("1-7", 1, 7), ("8-15", 8, 15), ("16-63", 16, 63), ("64-1023", 64, 1023), ("1024+", 1024, 10**12)]
hdir = sys.argv[1]
sys.stdout.reconfigure(encoding="utf-8")
print(f"| Workload | Calls | Median length | " + " | ".join(b[0] for b in BUCKETS) + " | Characters in 64+ |")
print("|---|---|---|" + "---|" * len(BUCKETS) + "---|")
for path in sorted(glob.glob(os.path.join(hdir, "hist_*.txt"))):
    name = os.path.basename(path)[5:-4]
    if name == "startup":
        continue
    counts, big = {}, 0
    for line in open(path):
        if line.startswith("#"):
            continue
        k, a, b = line.split()
        if a == "bigbytes":
            big += int(b)
        else:
            counts[int(a)] = counts.get(int(a), 0) + int(b)
    nbig = counts.pop(4096, 0)
    calls = sum(counts.values()) + nbig
    chars = sum(n * c for n, c in counts.items()) + big
    acc, med = 0, None
    for n in sorted(counts):
        acc += counts[n]
        if med is None and acc >= calls / 2:
            med = n
    if med is None:
        med = "4096+"
    cells = []
    for _, lo, hi in BUCKETS:
        c = sum(v for n, v in counts.items() if lo <= n <= hi) + (nbig if hi > 4096 else 0)
        cells.append(f"{c / calls:.0%}" if c else "–")
    long_chars = sum(n * v for n, v in counts.items() if n >= 64) + big
    print(f"| {name} | {calls:,} | {med} | " + " | ".join(cells) + f" | {long_chars / chars:.0%} |")
