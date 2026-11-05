"""Collect every layout-workflow job under the given artifact directories into
one JSON and one Markdown table: per job, the build description, and per
tree main / tree at each fixed length, on the short mix and on doclower
(means over shifts), the control-operation geomeans and the SIMD count.

    python collect.py OUT_PREFIX DIR [DIR ...]

Writes OUT_PREFIX.json and OUT_PREFIX.md.
"""
import glob, json, math, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "realworld"))
from layout_summary import summarize, geo

ALIAS = {"base": "main", "varJ": "PR"}


def compiler(meta):
    v = meta.get("base_version", "")
    m = re.search(r"\[(GCC [\d.]+|Clang [\d.]+)", v)
    return m.group(1) if m else ""


def lengths(res):
    p = os.path.join(res, "lengths.json")
    if not os.path.exists(p):
        return {}
    d = json.load(open(p))
    trees = {}
    for name, v in d["best"].items():
        tree = name.rsplit(".p", 1)[0]
        trees.setdefault(tree, []).append(v)
    mean = {t: [geo(v[i] for v in vs) for i in range(len(d["lens"]))] for t, vs in trees.items()}
    out = {}
    for t in mean:
        if t == "main":
            continue
        out[ALIAS.get(t, t)] = {str(n): mean["main"][i] / mean[t][i] for i, n in enumerate(d["lens"])}
    return out


def control(res):
    p = os.path.join(res, "control.json")
    if not os.path.exists(p):
        return {}
    d = json.load(open(p))
    trees = {}
    for name, v in d["best"].items():
        tree = "main" if name == "base" else name.rsplit(".p", 1)[0]
        trees.setdefault(tree, []).append(v)
    mean = {t: [geo(v[i] for v in vs) for i in range(len(d["ops"]))] for t, vs in trees.items()}
    out = {}
    for t in mean:
        if t == "main":
            continue
        g = {}
        for grp in ("control", "case"):
            idx = [i for i, x in enumerate(d["groups"]) if x == grp]
            g[grp] = geo(mean["main"][i] / mean[t][i] for i in idx)
        out[ALIAS.get(t, t)] = g
    return out


def simd(res):
    p = os.path.join(res, "simd.txt")
    out = {}
    if os.path.exists(p):
        for line in open(p):
            t, f, n = line.split()
            if f == "ascii_case_words":
                out[ALIAS.get(t, t)] = int(n) if n.isdigit() else n
    return out


def main():
    prefix, dirs = sys.argv[1], sys.argv[2:]
    jobs = []
    for d in dirs:
        for meta_p in sorted(glob.glob(os.path.join(d, "**", "results", "meta.json"), recursive=True)):
            res = os.path.dirname(meta_p)
            meta = json.load(open(meta_p))
            job = {"dir": os.path.relpath(res, os.path.dirname(os.path.abspath(d))).replace("\\", "/"),
                   "runner": meta.get("runner", ""), "rep": meta.get("rep", ""), "cpu": meta.get("cpu", ""),
                   "build": meta.get("build", ""), "compiler": compiler(meta),
                   "cflags_extra": meta.get("cflags", ""), "container": meta.get("container", ""),
                   "training": "custom" if meta.get("profile_task") else "default",
                   "cflags": meta.get("varJ_cflags", "")}
            tp = os.path.join(res, "layout", "times.json")
            short = {}
            if os.path.exists(tp):
                trees = summarize(tp)
                shifts = sorted(trees["main"])
                ms = geo(trees["main"][s][0] for s in shifts)
                md = geo(trees["main"][s][1] for s in shifts)
                for t in trees:
                    if t != "main":
                        short[ALIAS.get(t, t)] = {"short": ms / geo(trees[t][s][0] for s in shifts),
                                                  "doclower": md / geo(trees[t][s][1] for s in shifts)}
            job.update(short=short, lengths=lengths(res), control=control(res), simd=simd(res))
            jobs.append(job)
    json.dump(jobs, open(prefix + ".json", "w"), indent=1)
    trees = ["PR", "varP", "varR", "varT", "varN", "varO", "varB", "varB5", "cmpA", "cmpB", "cmpC", "cmpM", "varQ", "varS", "varU"]
    lines = ["| Job | Build | CPU | Tree | SIMD | 64K | 4,096 | 1,024 | 256 | 128 | 64 | 32 | 16 | short mix | control | doclower |",
             "|" + "---|" * 16]
    for j in jobs:
        desc = " ".join(x for x in (j["container"], j["compiler"], j["build"], j["cflags_extra"],
                                    "Debian training" if j["training"] == "custom" else "") if x)
        for t in trees:
            if t not in j["lengths"] and t not in j["short"]:
                continue
            L = j["lengths"].get(t, {})
            S = j["short"].get(t, {})
            C = j["control"].get(t, {})
            f = lambda d, k, p=2: f"{d[k]:.{p}f}" if k in d else "—"
            lines.append(f"| {j['dir']} | {desc} | {j['cpu'].replace(' Processor', '')} | {t} | {j['simd'].get(t, '—')} | "
                         f"{f(L, '65536')} | {f(L, '4096')} | {f(L, '1024')} | {f(L, '256')} | {f(L, '128')} | {f(L, '64')} | {f(L, '32')} | {f(L, '16')} | "
                         f"{f(S, 'short', 3)} | {f(C, 'control', 3)} | {f(S, 'doclower')} |")
    open(prefix + ".md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"{len(jobs)} jobs")


if __name__ == "__main__":
    main()
