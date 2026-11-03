"""Fixed-length str.lower() timing over many builds, alternating rounds.

    python len_layout.py OUT.json ROUNDS name=PYTHON [...]

Meant for every layout shift of every tree (see layout_local.sh).  Each
build runs once per round, in an order that rotates each round and is
reversed on odd rounds; the best time per build and length is saved.  With
REPLAY_CPU=N on Linux, each run is pinned to logical CPU N.
"""
import json, os, subprocess, sys

out_path, rounds = sys.argv[1], int(sys.argv[2])
builds = dict(a.split("=", 1) for a in sys.argv[3:])
cpu = os.environ.get("REPLAY_CPU")
LENS = (8, 16, 24, 32, 64, 128, 256, 1024, 4096, 65536)
SNIP = r"""
import time
res = []
for n in %r:
    s = ('AbCdEfGhIjKlMnOp' * (n // 16 + 1))[:n]
    k = max(3000, 1_000_000 // n)
    best = 1e9
    for _ in range(5):
        t = time.perf_counter()
        for _ in range(k):
            s.lower()
        best = min(best, (time.perf_counter() - t) / k)
    res.append(best * 1e9)
print(*('%%.3f' %% x for x in res))
""" % (LENS,)

kw = {}
if cpu and hasattr(os, "sched_setaffinity"):
    kw["preexec_fn"] = lambda: os.sched_setaffinity(0, {int(cpu)})
best = {b: None for b in builds}
for r in range(rounds):
    order = list(builds)[r % len(builds):] + list(builds)[:r % len(builds)]
    if r % 2:
        order.reverse()
    for b in order:
        out = subprocess.run([builds[b], "-I", "-c", SNIP], capture_output=True, text=True,
                             check=True, **kw).stdout
        v = [float(x) for x in out.split()]
        best[b] = v if best[b] is None else [min(a, c) for a, c in zip(best[b], v)]
json.dump({"lens": LENS, "best": best}, open(out_path, "w"), indent=1)
