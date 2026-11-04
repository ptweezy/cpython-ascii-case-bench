"""Time string operations that never reach the case-conversion code, next to
short lower() calls, over many builds: a control for whole-build effects.

    python control.py OUT.json ROUNDS name=PYTHON [...]
    python control.py --summary OUT.json

PGO builds of identical code can differ by several percent (the training
and the compiler's hot/cold choices vary), and that moves every operation,
not only lower() and upper().  If a tree is slower on the control
operations by about as much as on short lower() calls, the cause is the
build as a whole, not the variant's code.  Run like len_layout.py: rounds
rotate the build order; REPLAY_CPU=N pins each run to logical CPU N.
"""
import json, math, os, subprocess, sys
from collections import defaultdict

# (label, setup, statement, group).  "control" never calls _Py_bytes_lower
# or _Py_bytes_upper; "case" does.
OPS = [
    ("str.strip, 6 chars", "s = ' abcd '", "s.strip()", "control"),
    ("str.swapcase, 6 chars", "s = 'AbCdEf'", "s.swapcase()", "control"),
    ("str.casefold, 6 chars", "s = 'AbCdEf'", "s.casefold()", "control"),
    ("str.replace, 12 chars", "s = 'abcdefabcdef'", "s.replace('a', 'b')", "control"),
    ("str.startswith", "s = 'abcdefgh'", "s.startswith('abc')", "control"),
    ("str slice, 12 chars", "s = 'abcdefghijkl'", "s[1:9]", "control"),
    ("str concat", "s = 'abcd'; t = 'efgh'", "s + t", "control"),
    ("bytes.decode, 12 bytes", "b = b'abcdefghijkl'", "b.decode()", "control"),
    ("str.lower, 5 chars", "s = 'AbCdE'", "s.lower()", "case"),
    ("str.lower, 12 chars", "s = 'AbCdEfGhIjKl'", "s.lower()", "case"),
    ("str.upper, 12 chars", "s = 'AbCdEfGhIjKl'", "s.upper()", "case"),
    ("bytes.lower, 12 bytes", "b = b'AbCdEfGhIjKl'", "b.lower()", "case"),
]

SNIP = r"""
import time
res = []
for setup, stmt in %r:
    ns = {}
    exec(setup, ns)
    code = compile('for _ in range(k):\n    ' + stmt, '<op>', 'exec')
    ns['k'] = 200_000
    best = 1e9
    for _ in range(5):
        t = time.perf_counter()
        exec(code, ns)
        best = min(best, (time.perf_counter() - t) / 200_000)
    res.append(best * 1e9)
print(*('%%.3f' %% x for x in res))
""" % ([(s, st) for _, s, st, _ in OPS],)


def geo(xs):
    xs = list(xs)
    return math.exp(sum(map(math.log, xs)) / len(xs))


def measure(out_path, rounds, builds):
    cpu = os.environ.get("REPLAY_CPU")
    kw = {}
    if cpu and hasattr(os, "sched_setaffinity"):
        kw["preexec_fn"] = lambda: os.sched_setaffinity(0, {int(cpu)})
    best = {b: None for b in builds}
    for r in range(rounds):
        order = list(builds)[r % len(builds):] + list(builds)[:r % len(builds)]
        if r % 2:
            order.reverse()
        for b in order:
            p = subprocess.run([builds[b], "-I", "-c", SNIP], capture_output=True, text=True, **kw)
            if p.returncode:
                sys.exit(f"{builds[b]} failed: {p.stderr}")
            v = [float(x) for x in p.stdout.split()]
            best[b] = v if best[b] is None else [min(a, c) for a, c in zip(best[b], v)]
    json.dump({"ops": [o[0] for o in OPS], "groups": [o[3] for o in OPS], "best": best},
              open(out_path, "w"), indent=1)


def summary(path):
    d = json.load(open(path))
    ops, groups, best = d["ops"], d["groups"], d["best"]
    trees = defaultdict(list)
    for name, v in best.items():
        tree = "main" if name == "base" else name.rsplit(".p", 1)[0]
        trees[tree].append(v)
    order = ["main"] + sorted(t for t in trees if t != "main")
    mean = {t: [geo(v[i] for v in trees[t]) for i in range(len(ops))] for t in order}
    out = ["main / build, geometric mean over shifts (above 1.00x: faster than main):", "",
           "| Operation | main ns | " + " | ".join(order[1:]) + " |", "|---|---|" + "---|" * (len(order) - 1)]
    for i, op in enumerate(ops):
        out.append(f"| {op} | {mean['main'][i]:.1f} | "
                   + " | ".join(f"{mean['main'][i] / mean[t][i]:.3f}x" for t in order[1:]) + " |")
    for g in ("control", "case"):
        idx = [i for i, x in enumerate(groups) if x == g]
        out.append(f"| **geometric mean, {g}** | | "
                   + " | ".join(f"**{geo(mean['main'][i] / mean[t][i] for i in idx):.3f}x**" for t in order[1:]) + " |")
    print("\n".join(out))


if __name__ == "__main__":
    if sys.argv[1] == "--summary":
        summary(sys.argv[2])
    else:
        measure(sys.argv[1], int(sys.argv[2]), dict(a.split("=", 1) for a in sys.argv[3:]))
