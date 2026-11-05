"""Compact summary over runs: base/variant ratios by length band and placement.

usage: summary.py BASE VARIANT RUN.json [RUN.json ...]
For each op: geomean over lengths in a band (0, 1-4, 5-8, 9-15, 16-17, 20-64)
of BASE_N/VARIANT_N per placement N, then the geomean over placements, and
the same for each run separately; plus BASE_i/BASE_j extremes (main-only
swing) per band.
"""
import json
import math
import sys

base, var = sys.argv[1], sys.argv[2]
runs = [json.load(open(p)) for p in sys.argv[3:]]
lens, ops = runs[0]["lens"], runs[0]["ops"]
pl = sorted({int(b.split("_")[1]) for b in runs[0]["rounds"] if b.startswith(base + "_")})
BANDS = [("0", [0]), ("1-4", [1, 2, 3, 4]), ("5-8", [5, 6, 7, 8]), ("9-15", list(range(9, 16))),
         ("1-15", list(range(1, 16))), ("16-17", [16, 17]), ("20-64", [20, 24, 32, 64])]


def gm(xs):
    xs = list(xs)
    return math.exp(sum(math.log(x) for x in xs) / len(xs))


def best(run, b):
    return [min(c) for c in zip(*run["rounds"][b])]


B = [{b: best(r, b) for b in r["rounds"]} for r in runs]
print("%s/%s, %d runs, placements %s" % (base, var, len(runs), pl))
for oi, op in enumerate(ops):
    print("\n== %s" % op)
    print("band    " + " ".join("%6d" % n for n in pl) + "  | gm-all  per-run gm         | %s swing (max/min over N)" % base)
    for name, ls in BANDS:
        idx = [oi * len(lens) + lens.index(L) for L in ls if L in lens]
        per = []
        for n in pl:
            per.append(gm(B[k]["%s_%d" % (base, n)][i] / B[k]["%s_%d" % (var, n)][i]
                          for k in range(len(runs)) for i in idx))
        runsgm = [gm(B[k]["%s_%d" % (base, n)][i] / B[k]["%s_%d" % (var, n)][i]
                     for n in pl for i in idx) for k in range(len(runs))]
        # main swing: per length, max/min over placements of base time (gm over runs), then gm over band
        sw = gm(max(gm(B[k]["%s_%d" % (base, n)][i] for k in range(len(runs))) for n in pl)
                / min(gm(B[k]["%s_%d" % (base, n)][i] for k in range(len(runs))) for n in pl)
                for i in idx)
        print("%-6s  " % name + " ".join("%6.3f" % x for x in per)
              + "  | %6.3f  " % gm(per) + " ".join("%6.3f" % x for x in runsgm)
              + "  | %6.3f" % sw)
