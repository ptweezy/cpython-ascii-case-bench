"""Fixed-length str/bytes lower()/upper() timing over many builds, alternating rounds.

    python len_layout_win.py OUT.json ROUNDS name=PYTHON [...]

Adapted from benchrepo/realworld/len_layout.py: each build runs once per
round, in an order that rotates each round and is reversed on odd rounds.
Within a run, every (op, length) is timed as the best of BATCHES batches of
K calls of `s.<method>()` (s a str or bytes of that length, a local of a
function, as in pyperf timeit).  All rounds are
saved ("rounds": build -> list of per-round vectors) as well as the best
over rounds ("best").  With REPLAY_CPU=N each run is pinned to logical CPU N
at high priority.  LENS="0 1 2 ..." replaces the default lengths;
OPS="str.lower bytes.upper ..." the default ops; K and BATCHES env vars too.
"""
import json
import os
import subprocess
import sys

out_path, rounds = sys.argv[1], int(sys.argv[2])
builds = dict(a.split("=", 1) for a in sys.argv[3:])
cpu = os.environ.get("REPLAY_CPU")
LENS = (tuple(int(x) for x in os.environ.get("LENS", "").split())
        or tuple(range(18)) + (20, 24, 32, 64))
OPS = tuple(os.environ.get("OPS", "").split()
            or ("str.lower", "str.upper", "bytes.lower", "bytes.upper"))
K = int(os.environ.get("K", "20000"))
BATCHES = int(os.environ.get("BATCHES", "20"))

# Like pyperf timeit, the statement runs in a function with s and the loop
# variable as locals.
BLOCK = r"""
def bench_%(i)d(s, k):
    for _ in range(k):
        s.%(meth)s()
for n in %(lens)r:
    s = %(mk)s('AbCdEfGhIjKlMnOp' * (n // 16 + 1))[:n]
    best = 1e9
    for _ in range(%(batches)d):
        t = perf_counter()
        bench_%(i)d(s, %(k)d)
        t = perf_counter() - t
        if t < best:
            best = t
    res.append(best / %(k)d * 1e9)
"""
parts = []
for i, op in enumerate(OPS):
    typ, meth = op.split(".")
    mk = {"str": "", "bytes": "bytes", "bytearray": "bytearray"}[typ]
    if mk:
        mk = "(lambda x: %s(x, 'ascii'))" % mk
    parts.append(BLOCK % dict(i=i, lens=LENS, mk=mk, batches=BATCHES, k=K, meth=meth))
SNIP = ("\nfrom time import perf_counter\nres = []\n" + "".join(parts)
        + "print(*('%.3f' % x for x in res))\n")

kw = {}
if cpu and sys.platform == "win32":
    kw["creationflags"] = subprocess.HIGH_PRIORITY_CLASS
elif cpu and hasattr(os, "sched_setaffinity"):
    kw["preexec_fn"] = lambda: os.sched_setaffinity(0, {int(cpu)})


def run(exe):
    p = subprocess.Popen([exe, "-I", "-S", "-c", SNIP], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, **kw)
    if cpu and sys.platform == "win32":
        import ctypes
        ctypes.windll.kernel32.SetProcessAffinityMask(int(p._handle), 1 << int(cpu))
    out, err = p.communicate()
    if p.returncode:
        sys.exit(f"{exe} failed: {err}")
    return [float(x) for x in out.split()]


allr = {b: [] for b in builds}
for r in range(rounds):
    order = list(builds)[r % len(builds):] + list(builds)[:r % len(builds)]
    if r % 2:
        order.reverse()
    for b in order:
        allr[b].append(run(builds[b]))
    print("round", r + 1, "done", flush=True)
    best = {b: [min(c) for c in zip(*v)] for b, v in allr.items()}
    json.dump({"lens": LENS, "ops": OPS, "k": K, "batches": BATCHES, "cpu": cpu,
               "best": best, "rounds": allr}, open(out_path, "w"), indent=0)
