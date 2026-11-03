"""Summarize a layout run (times.json from replay_drive.py; see layout.yml).

    python layout_summary.py TIMES.json

Build names are TREE.pSHIFT, with "base" standing for main.p0.  Per build:
the median ns per call over rounds for each workload, and the geometric
mean over the short-string workloads (all but doclower).  Per tree: the
geometric mean over shifts, the range over shifts, and main / tree with a
95% bootstrap interval (shifts resampled independently for both).  A
meta.json next to the times.json directory, if present, names the CPU.
"""
import json, math, os, random, statistics, sys
from collections import defaultdict

SHORT = ["config", "email", "html", "http", "paths", "pgotask", "urls", "words"]


def geo(xs):
    xs = list(xs)
    return math.exp(sum(map(math.log, xs)) / len(xs))


def summarize(path):
    times = json.load(open(path))
    trees = defaultdict(dict)  # tree -> shift -> (short ns, doclower ns)
    for n, w in times.items():
        tree, shift = ("main", "0") if n == "base" else n.rsplit(".p", 1)
        med = {k: statistics.median(v) for k, v in w.items()}
        trees[tree][int(shift)] = (geo(med[k] for k in SHORT), med["doclower"])
    return trees


def main():
    path = sys.argv[1]
    trees = summarize(path)
    meta_p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(path))), "meta.json")
    meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
    shifts = sorted(trees["main"])
    order = ["main"] + sorted(t for t in trees if t != "main")
    rng = random.Random(1)

    def boot(a, b, n=4000):
        rs = sorted(geo(rng.choice(a) for _ in a) / geo(rng.choice(b) for _ in b) for _ in range(n))
        return rs[int(0.025 * n)], rs[int(0.975 * n)]

    out = [f"### {meta.get('runner', '')} {meta.get('build', '')} run {meta.get('rep', '')}: {meta.get('cpu', '')}", "",
           "Short mix, ns per call (geometric mean of the short workloads), per shift:", "",
           "| Build | " + " | ".join(f"+{s}" for s in shifts) + " | range |",
           "|---|" + "---|" * (len(shifts) + 1)]
    for t in order:
        xs = [trees[t][s][0] for s in shifts]
        out.append(f"| {t} | " + " | ".join(f"{x:.1f}" for x in xs) + f" | {100 * (max(xs) / min(xs) - 1):.0f}% |")
    out += ["", "| Build | short ns (mean over shifts) | main / build | 95% interval | doclower main / build |",
            "|---|---|---|---|---|"]
    m_short = [trees["main"][s][0] for s in shifts]
    m_doc = geo(trees["main"][s][1] for s in shifts)
    for t in order:
        xs = [trees[t][s][0] for s in shifts]
        lo, hi = boot(m_short, xs)
        out.append(f"| {t} | {geo(xs):.2f} | {geo(m_short) / geo(xs):.3f}x | {lo:.3f}-{hi:.3f} | "
                   f"{m_doc / geo(trees[t][s][1] for s in shifts):.2f}x |")
    print("\n".join(out))


if __name__ == "__main__":
    main()
