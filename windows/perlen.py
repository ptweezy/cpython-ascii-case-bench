"""Per length: geomean over placements of BASE_N/VAR_N (each pooled as the
geomean over runs of best-of-rounds), and [min-max] over placements.
usage: perlen.py BASE VAR RUN.json [...]"""
import json, math, sys
base, var = sys.argv[1:3]
runs = [json.load(open(p)) for p in sys.argv[3:]]
lens, ops = runs[0]["lens"], runs[0]["ops"]
pl = sorted({int(b.split("_")[1]) for b in runs[0]["rounds"] if b.startswith(var + "_")})
gm = lambda xs: math.exp(sum(map(math.log, xs)) / len(xs))
best = [{b: [min(c) for c in zip(*r["rounds"][b])] for b in r["rounds"]} for r in runs]
print("%s/%s per length: gm over placements %s [min-max]; %d runs" % (base, var, pl, len(runs)))
for oi, op in enumerate(ops):
    cells = []
    for li, L in enumerate(lens):
        i = oi * len(lens) + li
        per = [gm([b["%s_%d" % (base, n)][i] / b["%s_%d" % (var, n)][i] for b in best]) for n in pl]
        cells.append("%d:%.3f[%.3f-%.3f]" % (L, gm(per), min(per), max(per)))
    print(op + "  " + " ".join(cells))
