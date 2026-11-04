"""main / build from the variants workflow's pyperf JSON, mean of all values.

    python win_pyperf.py JOBDIR... -> markdown rows
"""
import json, os, sys

NAMES = ["str.lower 16", "str.lower 64", "str.lower 256", "str.lower 1024", "str.lower 65536"]


def means(path):
    d = json.load(open(path))
    out = {}
    for b in d["benchmarks"]:
        vals = [v for r in b["runs"] for v in r.get("values", [])]
        out[b["metadata"]["name"]] = sum(vals) / len(vals)
    return out


def short(job, tree):
    p = os.path.join(job, "results", "replay", "median.json")
    if not os.path.exists(p):
        return None
    return json.load(open(p))


print("| Build | Job | CPU | " + " | ".join(n.split()[1] for n in NAMES) + " |")
for job in sys.argv[1:]:
    r = os.path.join(job, "results")
    meta = json.load(open(os.path.join(r, "meta.json")))
    trees = [t for t in ("varJ", "varB", "varR") if os.path.exists(os.path.join(r, t + ".json"))]
    base = means(os.path.join(r, "base.json"))
    for t in trees:
        m = means(os.path.join(r, t + ".json"))
        cells = ["%.2fx" % (base[n] / m[n]) for n in NAMES]
        name = "PR" if t == "varJ" else t
        print("| %s | %s | %s | %s | %s |" % (meta["build"], os.path.basename(job), meta["cpu"].replace(" Processor", ""), name, " | ".join(cells)))
