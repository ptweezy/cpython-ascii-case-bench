"""Table from len_layout.py output.

    python len_layout_summary.py FILE.json

Build names are TREE.pSHIFT (main's trees named "main").  Per tree and
length: the geometric mean over shifts of ns per call; printed as main /
tree, with the range over shifts (ns / mean) in brackets.
"""
import json, math, sys
from collections import defaultdict


def geo(xs):
    xs = list(xs)
    return math.exp(sum(map(math.log, xs)) / len(xs))


def main():
    d = json.load(open(sys.argv[1]))
    lens, best = d["lens"], d["best"]
    trees = defaultdict(list)
    for name, v in best.items():
        trees[name.rsplit(".p", 1)[0]].append(v)
    order = ["main"] + sorted(t for t in trees if t != "main")
    mean = {t: [geo(v[i] for v in trees[t]) for i in range(len(lens))] for t in order}
    out = ["main / build, geometric mean over shifts (range over shifts of ns / mean):", "",
           "| Length | main ns | " + " | ".join(order[1:]) + " |", "|---|---|" + "---|" * (len(order) - 1)]
    for i, n in enumerate(lens):
        cells = []
        for t in order[1:]:
            xs = [v[i] for v in trees[t]]
            cells.append(f"{mean['main'][i] / mean[t][i]:.2f}x ({min(xs) / mean[t][i]:.2f}-{max(xs) / mean[t][i]:.2f})")
        out.append(f"| {n:,} | {mean['main'][i]:.1f} | " + " | ".join(cells) + " |")
    print("\n".join(out))


if __name__ == "__main__":
    main()
