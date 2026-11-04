"""Pool the Windows runner jobs' real-world short-string mix (variants
workflow, one layout per job): per job, geometric mean over the short
workloads of main / build, then varB / PR pooled over jobs.
    python win_short.py JOBDIR..."""
import json, math, os, sys
def stats(r):
    lg = [math.log(x) for x in r]; m = sum(lg) / len(lg)
    se = (sum((x - m) ** 2 for x in lg) / (len(lg) - 1)) ** .5 / len(lg) ** .5
    return math.exp(m), math.exp(m - 2 * se), math.exp(m + 2 * se)
groups = {}
print("| Job | Build | CPU | PR (median) | varB (median) | PR (best) | varB (best) |")
print("|---|---|---|---|---|---|---|")
for job in sys.argv[1:]:
    r = os.path.join(job, "results")
    meta = json.load(open(os.path.join(r, "meta.json")))
    arch = "ARM64" if "arm" in meta["runner"] else "x64"
    vals = {}
    for kind in ("median", "best"):
        d = json.load(open(os.path.join(r, "replay", kind + ".json")))
        ws = [w for w in d["base"] if w != "doclower"]
        for t in ("varJ", "varB"):
            vals[kind, t] = math.exp(sum(math.log(d["base"][w] / d[t][w]) for w in ws) / len(ws))
        groups.setdefault((arch, meta["build"], kind), []).append(vals[kind, "varB"] / vals[kind, "varJ"])
    print("| %s | %s %s | %s | %.3f | %.3f | %.3f | %.3f |" % (os.path.basename(job), arch, meta["build"],
          meta["cpu"].replace(" Processor", ""), vals["median", "varJ"], vals["median", "varB"], vals["best", "varJ"], vals["best", "varB"]))
print()
print("| Build | Statistic | Jobs | varB / PR | 95% interval |")
print("|---|---|---|---|---|")
for k in sorted(groups):
    r = groups[k]
    if len(r) > 1:
        g, lo, hi = stats(r); print("| %s %s | %s | %d | %.3f | %.3f-%.3f |" % (k[0], k[1], k[2], len(r), g, lo, hi))
for kind in ("median", "best"):
    r = [x for k, v in groups.items() if k[2] == kind for x in v]
    g, lo, hi = stats(r); print("| all | %s | %d | %.3f | %.3f-%.3f |" % (kind, len(r), g, lo, hi))
