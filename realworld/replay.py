"""Replay the lower()/upper() length mix recorded for each workload.

    python replay.py HISTDIR OUT.json [REPEATS]

For each hist_<name>.txt, build a shuffled list of ASCII strings whose
lengths follow the recorded counts (scaled to about TARGET calls; strings
of 4096+ characters get the bucket's average length), then time
`for s in L: s.lower()` and keep the fastest of REPEATS runs.
"""
import glob, json, os, random, sys, time

hdir, out = sys.argv[1], sys.argv[2]
repeats = int(sys.argv[3]) if len(sys.argv) > 3 else 15
TARGET = 200_000
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_./:;= "


def load(path):
    counts, big = {}, {}
    for line in open(path):
        if line.startswith("#"):
            continue
        k, a, b = line.split()
        if a == "bigbytes":
            big[k] = big.get(k, 0) + int(b)
        else:
            counts[int(a)] = counts.get(int(a), 0) + int(b)
    nbig = counts.pop(4096, 0)
    if nbig:
        avg = sum(big.values()) // nbig
        counts[avg] = counts.get(avg, 0) + nbig
    return counts


rng = random.Random(161155)
res = {"version": sys.version, "workloads": {}}
for path in sorted(glob.glob(os.path.join(hdir, "hist_*.txt"))):
    name = os.path.basename(path)[5:-4]
    if name == "startup":
        continue
    counts = load(path)
    calls = sum(counts.values())
    nbytes = sum(n * c for n, c in counts.items())
    # Scale to about TARGET calls, but cap the total characters at 64 MB.
    scale = min(TARGET / calls, 64e6 / max(nbytes, 1))
    pool = {n: ["".join(rng.choice(ALPHA) for _ in range(min(n, 64))) * (n // 64 + 1) for _ in range(4)]
            for n in counts}
    pool = {n: [s[:n] for s in v] for n, v in pool.items()}
    L = []
    for n, c in counts.items():
        k = max(1, round(c * scale))
        L += [pool[n][i % 4] for i in range(k)]
    rng.shuffle(L)
    best = float("inf")
    for _ in range(repeats):
        t = time.perf_counter()
        for s in L:
            s.lower()
        best = min(best, time.perf_counter() - t)
    res["workloads"][name] = {"calls": calls, "chars": nbytes, "replayed": len(L),
                              "best_s": best, "ns_per_call": best / len(L) * 1e9}
json.dump(res, open(out, "w"), indent=1)
for k, v in res["workloads"].items():
    print(f"{k:<10} {v['replayed']:>8} calls  {v['ns_per_call']:8.1f} ns/call")
