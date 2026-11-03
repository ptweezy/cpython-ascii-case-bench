"""Run replay.py with several interpreters in alternating rounds.

    python replay_drive.py HISTDIR OUTDIR ROUNDS base=PYTHON name=PYTHON [...]

The build order rotates each round and is reversed on odd rounds.  With
REPLAY_CPU=N set, each timed interpreter runs pinned to logical CPU N (and
at high priority on Windows).  Writes times.json (every round), best.json
and median.json, and prints ns per call and main/build ratios for both
(base is main).
"""
import json, os, statistics, subprocess, sys

hdir, outdir, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
builds = {k: os.path.abspath(v) for k, v in (a.split("=", 1) for a in sys.argv[4:])}
here = os.path.dirname(os.path.abspath(__file__))
cpu = os.environ.get("REPLAY_CPU")
os.makedirs(outdir, exist_ok=True)


def run(cmd):
    kw = {}
    if cpu and sys.platform == "win32":
        kw["creationflags"] = subprocess.HIGH_PRIORITY_CLASS
    elif cpu and hasattr(os, "sched_setaffinity"):
        kw["preexec_fn"] = lambda: os.sched_setaffinity(0, {int(cpu)})
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, **kw)
    if cpu and sys.platform == "win32":
        import ctypes
        ctypes.windll.kernel32.SetProcessAffinityMask(int(p._handle), 1 << int(cpu))
    _, err = p.communicate()
    if p.returncode:
        sys.exit(f"{cmd[0]} failed: {err.decode(errors='replace')}")


times = {b: {} for b in builds}
for r in range(rounds):
    order = list(builds)
    order = order[r % len(order):] + order[:r % len(order)]
    if r % 2:
        order.reverse()
    for b in order:
        out = os.path.join(outdir, f"{b}-{r}.json")
        run([builds[b], "-I", os.path.join(here, "replay.py"), hdir, out, "5"])
        for w, v in json.load(open(out))["workloads"].items():
            times[b].setdefault(w, []).append(v["ns_per_call"])
json.dump(times, open(os.path.join(outdir, "times.json"), "w"), indent=1)
names = list(builds)
works = list(times[names[0]])
for label, f in (("best", min), ("median", statistics.median)):
    summary = {b: {w: f(times[b][w]) for w in works} for b in names}
    json.dump(summary, open(os.path.join(outdir, f"{label}.json"), "w"), indent=1)
    print(f"\n{label} ns per call: | Workload | " + " | ".join(names) + " |")
    for w in works:
        print(f"| {w} | " + " | ".join(f"{summary[b][w]:.1f}" for b in names) + " |")
    print(f"\nmain / build ({label}): | Workload | " + " | ".join(names[1:]) + " |")
    for w in works:
        print(f"| {w} | " + " | ".join(f"{summary['base'][w] / summary[b][w]:.2f}x" for b in names[1:]) + " |")
