"""Run replay.py with several interpreters in alternating rounds and keep the
best time per workload.

    python replay_drive.py HISTDIR OUTDIR ROUNDS base=PYTHON name=PYTHON [...]

Prints ns per call for each build and main/build ratios (base is main).
"""
import json, os, subprocess, sys

hdir, outdir, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
builds = {k: os.path.abspath(v) for k, v in (a.split("=", 1) for a in sys.argv[4:])}
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(outdir, exist_ok=True)
best = {b: {} for b in builds}
for r in range(rounds):
    order = list(builds)
    order = order[r % len(order):] + order[:r % len(order)]
    for b in order:
        out = os.path.join(outdir, f"{b}-{r}.json")
        subprocess.run([builds[b], "-I", os.path.join(here, "replay.py"), hdir, out, "5"],
                       check=True, capture_output=True)
        for w, v in json.load(open(out))["workloads"].items():
            best[b][w] = min(best[b].get(w, float("inf")), v["ns_per_call"])
json.dump(best, open(os.path.join(outdir, "best.json"), "w"), indent=1)
names = list(builds)
works = list(best[names[0]])
print("ns per call: | Workload | " + " | ".join(names) + " |")
for w in works:
    print(f"| {w} | " + " | ".join(f"{best[b][w]:.1f}" for b in names) + " |")
print("\nmain / build: | Workload | " + " | ".join(names[1:]) + " |")
for w in works:
    print(f"| {w} | " + " | ".join(f"{best['base'][w] / best[b][w]:.2f}x" for b in names[1:]) + " |")
