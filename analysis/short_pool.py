"""Pool the short-string mix (main / build, mean over shifts) across layout
runs, for the varT/varU comparison.

    python short_pool.py OUT.md [DIR ...] [--times LABEL=times.json ...]
                         [--row "LABEL|PR|varP|varT|varQ|varU" ...]

DIRs are downloaded layout-workflow artifacts (searched for times.json);
--times adds a local layout run; --row adds a row measured elsewhere (use
"-" for a variant that wasn't measured).  Prints one row per job and the
geometric mean over rows that have every variant in a column set.
"""
import glob, json, math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "realworld"))
from layout_summary import summarize, geo

TREES = [("varJ", "PR"), ("varP", "varR (varP)"), ("varT", "varT"), ("varN", "varN"), ("varO", "varO"),
         ("varB", "varB"), ("varQ", "varS (varQ)"), ("varU", "varU")]
ROW_ORDER = ["varJ", "varP", "varT", "varQ", "varU"]  # --row values
# varR and varP compile to the same code under gcc and clang.
ALIASES = {"PR": "varJ", "varR": "varP"}


def row_from_times(path):
    trees = summarize(path)
    trees = {ALIASES.get(k, k): v for k, v in trees.items()}
    shifts = sorted(trees["main"])
    ms = geo(trees["main"][s][0] for s in shifts)
    return {t: ms / geo(trees[t][s][0] for s in shifts) for t, _ in TREES if t in trees}


def main():
    args = sys.argv[1:]
    out, rest = args[0], args[1:]
    rows = []
    i = 0
    while i < len(rest):
        a = rest[i]
        if a == "--times":
            label, path = rest[i + 1].split("=", 1)
            rows.append((label, row_from_times(path)))
            i += 2
        elif a == "--row":
            parts = rest[i + 1].split("|")
            vals = {t: float(v) for t, v in zip(ROW_ORDER, parts[1:]) if v != "-"}
            rows.append((parts[0], vals))
            i += 2
        else:
            for tp in sorted(glob.glob(os.path.join(a, "**", "layout", "times.json"), recursive=True)):
                res = os.path.dirname(os.path.dirname(tp))
                meta = json.load(open(os.path.join(res, "meta.json")))
                cpu = meta.get("cpu", "").replace(" Processor", "").replace("(R)", "").replace("(TM)", "")
                build = meta.get("build", "")
                extra = " ".join(x for x in (meta.get("container", ""), meta.get("cc", ""), meta.get("cflags", ""),
                                             "Debian training" if meta.get("profile_task") else "") if x)
                label = f"{meta.get('runner', '')} {build}{' ' + extra if extra else ''}, {cpu}"
                rows.append((label, row_from_times(tp)))
            i += 1
    lines = ["| Run | " + " | ".join(n for _, n in TREES) + " |", "|---|" + "---|" * len(TREES)]
    for label, vals in rows:
        lines.append(f"| {label} | " + " | ".join(f"{vals[t]:.3f}" if t in vals else "—" for t, _ in TREES) + " |")
    for cols in (["varJ", "varP", "varT", "varQ", "varU"], ["varJ", "varP", "varT"],
                 ["varJ", "varN"], ["varJ", "varO"], ["varJ", "varB"]):
        sel = [v for _, v in rows if all(c in v for c in cols)]
        if not sel:
            continue
        g = {c: geo(v[c] for v in sel) for c in cols}
        wins = {c: sum(v[c] > v["varJ"] for v in sel) for c in cols if c != "varJ"}
        lines.append(f"| **Geometric mean of {len(sel)} rows ({', '.join(cols)})** | "
                     + " | ".join(f"**{g[t]:.3f}**" if t in g else "" for t, _ in TREES) + " |")
        lines.append(f"| rows ahead of the PR | " + " | ".join(
            f"{wins[t]}/{len(sel)}" if t in wins else "" for t, _ in TREES) + " |")
        def ci(c):  # 95% interval of the geometric-mean ratio to the PR
            r = [math.log(v[c] / v["varJ"]) for v in sel]
            if len(r) < 2:
                return ""
            m = sum(r) / len(r)
            se = (sum((x - m) ** 2 for x in r) / (len(r) - 1)) ** .5 / len(r) ** .5
            return f"{math.exp(m):.3f} ({math.exp(m - 2 * se):.3f}-{math.exp(m + 2 * se):.3f})"
        lines.append(f"| ratio to the PR (95% interval) | " + " | ".join(
            ci(t) if t in wins else "" for t, _ in TREES) + " |")
    # varB's code, from whichever tree in each job compiles to it
    # (results/varB_equiv.md): varB itself, else varN on x86-64, varT on
    # x86-64 without AVX2, varO on arm64 or with AVX2.
    def target(label):
        runner = label.split(" ")[0]
        if runner.endswith("-arm") or runner == "macos-15":
            return "arm64"
        if any(x in label for x in ("x86-64-v3", "x86-64-v4", "avx2")):
            return "x86-64 with AVX2"
        return "x86-64 without AVX2"
    pick = {"arm64": ["varB", "varO"], "x86-64 with AVX2": ["varB", "varN", "varO"],
            "x86-64 without AVX2": ["varB", "varN", "varT"]}
    by = {}
    for label, v in rows:
        t = target(label)
        src = next((c for c in pick[t] if c in v), None)
        if src and "varJ" in v:
            by.setdefault(t, []).append(v[src] / v["varJ"])
    lines += ["", "varB's code (varB, or the tree with the same machine code in that job), ratio to the PR:", "",
              "| Target | Rows | Geometric mean | 95% interval | Rows ahead of the PR | Lowest |", "|---|---|---|---|---|---|"]
    for t in ("x86-64 without AVX2", "x86-64 with AVX2", "arm64", "all"):
        r = [x for k, xs in by.items() for x in xs] if t == "all" else by.get(t, [])
        if len(r) < 2:
            continue
        lg = [math.log(x) for x in r]
        m = sum(lg) / len(lg)
        se = (sum((x - m) ** 2 for x in lg) / (len(lg) - 1)) ** .5 / len(lg) ** .5
        lines.append(f"| {t} | {len(r)} | {math.exp(m):.3f} | {math.exp(m - 2 * se):.3f}-{math.exp(m + 2 * se):.3f} "
                     f"| {sum(x > 1 for x in r)}/{len(r)} | {min(r):.3f} |")
    text = "\n".join(lines) + "\n"
    open(out, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
