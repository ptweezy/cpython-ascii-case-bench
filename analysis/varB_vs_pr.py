"""For each layout job in runner_jobs.md, varB's code (varB, or the tree with
the same machine code in that job; results/varB_equiv.md) against the PR at
256, 1,024, 4,096 and 64K, and the lowest ratios.

    python varB_vs_pr.py runner_jobs.md"""
import sys, collections

LENGTHS = ("256", "1,024", "4,096", "64K")
rows = collections.OrderedDict()
hdr = None
for line in open(sys.argv[1], encoding="utf-8"):
    if not line.startswith("| "):
        continue
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if c[0] == "Job":
        hdr = c
        continue
    d = dict(zip(hdr, c))
    rows.setdefault((d["Job"], d["Build"], d["CPU"]), {})[d["Tree"]] = d


def target(build, cpu):
    if any(x in cpu for x in ("Neoverse", "Apple", "Cobalt")):
        return "arm64"
    if any(x in build for x in ("x86-64-v3", "x86-64-v4")):
        return "avx2"
    return "x86"


pick = {"arm64": ["varB", "varO"], "avx2": ["varB", "varN", "varO"], "x86": ["varB", "varN", "varT"]}
n = 0
ratios = []
for (job, build, cpu), t in rows.items():
    src = next((p for p in pick[target(build, cpu)] if p in t), None)
    if not src or "PR" not in t:
        continue
    n += 1
    for L in LENGTHS:
        try:
            ratios.append((float(t[src][L]) / float(t["PR"][L]), L, job, build, cpu, src))
        except (KeyError, ValueError):
            pass
ratios.sort()
low = sorted({r[2] for r in ratios if r[0] < 0.985})
rest = [r for r in ratios if r[2] not in low]
print("jobs with varB's code:", n, "of", len(rows))
print("below 0.985x (0.98x or less when rounded) at some length from 256 up:", len(low))
print("lowest in the other %d jobs: %.3f" % (n - len(low), rest[0][0]))
for r in ratios[:10]:
    print("%.3f at %s: %s | %s | %s (%s)" % r)
