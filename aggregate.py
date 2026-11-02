"""Merge pyperf results from many machines into one markdown report.

    python aggregate.py OUT.md DIR [DIR ...]

Each DIR holds base.json and patched.json (or word.json), and optionally
meta.json from bench.py.  Ratios are base time / patched time, so 1.25 means
the patch is 1.25x faster.  A ratio is marked "~" when a Welch t-test can't
tell the two builds apart (|t| < 2).
"""
import glob
import json
import math
import os
import sys
from collections import defaultdict


def load(path):
    with open(path) as f:
        data = json.load(f)
    out = {}
    for b in data["benchmarks"]:
        name = b["metadata"].get("name") or data["metadata"].get("name")
        vals = [v for r in b["runs"] for v in r.get("values", [])]
        if vals:
            out[name] = vals
    return out


def stats(v):
    n = len(v)
    m = sum(v) / n
    var = sum((x - m) ** 2 for x in v) / (n - 1) if n > 1 else 0.0
    return m, var, n


def compare(a, b):
    ma, va, na = stats(a)
    mb, vb, nb = stats(b)
    se = math.sqrt(va / na + vb / nb)
    t = (ma - mb) / se if se else float("inf")
    return ma / mb, abs(t) >= 2.0, ma, mb


def find_dirs(args):
    """Yield (dir, other result file) for each non-base result next to a base.json."""
    for a in args:
        for base in glob.glob(os.path.join(a, "**", "base.json"), recursive=True):
            d = os.path.dirname(base)
            for p in sorted(os.listdir(d)):
                if p.endswith(".json") and p not in ("base.json", "meta.json"):
                    yield d, p


def fmt_time(s):
    for unit, k in (("ns", 1e9), ("us", 1e6), ("ms", 1e3)):
        if s * k < 1000:
            return f"{s * k:.3g} {unit}"
    return f"{s:.3g} s"


def main():
    out_md, args = sys.argv[1], sys.argv[2:]
    cols = []
    for d, pname in sorted(find_dirs(args)):
        meta = {}
        if os.path.exists(os.path.join(d, "meta.json")):
            with open(os.path.join(d, "meta.json")) as f:
                meta = json.load(f)
        label = meta.get("runner") or os.path.basename(os.path.dirname(d)) or d
        if meta.get("build"):
            label += f" {meta['build']}"
        if meta.get("rep"):
            label += f" #{meta['rep']}"
        variant = pname[:-5]
        if variant not in ("patched", "word"):
            label += f" [{variant}]"
        base, patched = load(os.path.join(d, "base.json")), load(os.path.join(d, pname))
        res = {k: compare(base[k], patched[k]) for k in base if k in patched}
        cols.append((label, dict(meta, variant=variant), res))

    order = []
    for _, _, res in cols:
        for k in res:
            if k not in order:
                order.append(k)

    lines = ["# gh-161155 benchmark results", "",
             "Ratio = time on main / time with the patch (above 1 = patch faster). "
             "`~` = not significant (Welch |t| < 2).", "", "## Machines", "",
             "| # | Job | CPU | CPUs | Compiler |", "|---|---|---|---|---|"]
    for i, (label, meta, _) in enumerate(cols, 1):
        comp = meta.get("patched_version", "")
        comp = comp[comp.rfind("[") + 1:comp.rfind("]")] if "[" in comp else ""
        lines.append(f"| {i} | {label} | {meta.get('cpu', '')} | {meta.get('cpus', '')} | {comp} |")

    # Per-benchmark summary across all columns, split by build type.
    groups = defaultdict(list)
    for i, (label, meta, _) in enumerate(cols):
        key = meta.get("build") or "local"
        if meta["variant"] not in ("patched", "word"):
            key += f" / {meta['variant']}"
        groups[key].append(i)
    lines += ["", "## Summary by build type", "",
              "Geometric mean of the ratios across machines, with the range, and how many "
              "machines were significantly faster / slower / unchanged.", ""]
    for g, idx in groups.items():
        lines += [f"### {g} ({len(idx)} jobs)", "",
                  "| Benchmark | geomean | min | max | faster / slower / ~ |", "|---|---|---|---|---|"]
        for k in order:
            rs = [cols[i][2][k] for i in idx if k in cols[i][2]]
            if not rs:
                continue
            ratios = [r[0] for r in rs]
            gm = math.exp(sum(math.log(r) for r in ratios) / len(ratios))
            fast = sum(1 for r in rs if r[1] and r[0] > 1)
            slow = sum(1 for r in rs if r[1] and r[0] < 1)
            lines.append(f"| {k} | {gm:.3f} | {min(ratios):.3f} | {max(ratios):.3f} | "
                         f"{fast} / {slow} / {len(rs) - fast - slow} |")
        lines.append("")

    lines += ["## Every job", "", "| Benchmark | " + " | ".join(str(i) for i in range(1, len(cols) + 1)) + " |",
              "|---|" + "---|" * len(cols)]
    for k in order:
        cells = []
        for _, _, res in cols:
            if k in res:
                r, sig, _, _ = res[k]
                cells.append(f"{r:.2f}" + ("" if sig else "~"))
            else:
                cells.append("")
        lines.append(f"| {k} | " + " | ".join(cells) + " |")
    lines += ["", "## Absolute times (main → patched)", "",
              "| Benchmark | " + " | ".join(str(i) for i in range(1, len(cols) + 1)) + " |",
              "|---|" + "---|" * len(cols)]
    for k in order:
        cells = [f"{fmt_time(res[k][2])} → {fmt_time(res[k][3])}" if k in res else ""
                 for _, _, res in cols]
        lines.append(f"| {k} | " + " | ".join(cells) + " |")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{len(cols)} result sets -> {out_md}")


if __name__ == "__main__":
    main()
