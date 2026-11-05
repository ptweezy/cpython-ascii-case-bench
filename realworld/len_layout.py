"""Fixed-length str.lower() and str.upper() timing over many builds,
alternating rounds.

    python len_layout.py OUT.json ROUNDS name=PYTHON [...]

Meant for every layout shift of every tree (see layout_local.sh).  Each
build runs once per round, in an order that rotates each round and is
reversed on odd rounds; the best time per build, method and length is
saved: "best" holds every length for lower(), then every length for
upper(), in the order of "ops".  With REPLAY_CPU=N, each run is pinned to
logical CPU N (Linux; on Windows also at high priority).
"""
import json, os, subprocess, sys

out_path, rounds = sys.argv[1], int(sys.argv[2])
builds = dict(a.split("=", 1) for a in sys.argv[3:])
cpu = os.environ.get("REPLAY_CPU")
LENS = (8, 16, 24, 32, 64, 128, 256, 1024, 4096, 65536)
OPS = ("lower", "upper")
# The loop for each method, the same as when only lower() was timed.
BLOCK = r"""
for n in %r:
    s = ('AbCdEfGhIjKlMnOp' * (n // 16 + 1))[:n]
    k = max(3000, 1_000_000 // n)
    best = 1e9
    for _ in range(5):
        t = time.perf_counter()
        for _ in range(k):
            s.%s()
        best = min(best, (time.perf_counter() - t) / k)
    res.append(best * 1e9)
"""
SNIP = ("\nimport time\nres = []\n" + "".join(BLOCK % (LENS, op) for op in OPS)
        + "print(*('%.3f' % x for x in res))\n")

kw = {}
if cpu and sys.platform == "win32":
    kw["creationflags"] = subprocess.HIGH_PRIORITY_CLASS
elif cpu and hasattr(os, "sched_setaffinity"):
    kw["preexec_fn"] = lambda: os.sched_setaffinity(0, {int(cpu)})


def run(exe):
    p = subprocess.Popen([exe, "-I", "-c", SNIP], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, **kw)
    if cpu and sys.platform == "win32":
        import ctypes
        ctypes.windll.kernel32.SetProcessAffinityMask(int(p._handle), 1 << int(cpu))
    out, err = p.communicate()
    if p.returncode:
        sys.exit(f"{exe} failed: {err}")
    return out


best = {b: None for b in builds}
for r in range(rounds):
    order = list(builds)[r % len(builds):] + list(builds)[:r % len(builds)]
    if r % 2:
        order.reverse()
    for b in order:
        out = run(builds[b])
        v = [float(x) for x in out.split()]
        best[b] = v if best[b] is None else [min(a, c) for a, c in zip(best[b], v)]
json.dump({"lens": LENS, "ops": OPS, "best": best}, open(out_path, "w"), indent=1)
