"""Time two CPython builds (main and main + gh-161155) with pyperf.

    python bench.py --which TREE            print the built interpreter's path
    python bench.py BASE_TREE PATCHED_TREE OUTDIR PYPERF_DIR

The builds take turns, one benchmark at a time (and which goes first
alternates), so slow drift on a shared machine hits both equally.
"""
import json
import os
import platform
import subprocess
import sys

CANDIDATES = ("python.exe", "python", "PCbuild/amd64/python.exe",
              "PCbuild/arm64/python.exe")


def which(tree):
    for c in CANDIDATES:
        p = f"{tree}/{c}"
        if os.path.isfile(p):
            return p
    sys.exit(f"no built python in {tree}")


PHRASE = "Hello World, The Quick Brown Fox Jumps Over 13 Lazy Dogs! "
SETUP = (
    f"t = {PHRASE!r} * 2000\n"
    f"words = ({PHRASE!r} * 2).split() * 50\n"
    "hdrs = ['Host', 'Accept', 'User-Agent', 'Connection', 'Content-Type',"
    " 'Cache-Control', 'Content-Length', 'Accept-Encoding'] * 50"
)

BENCHES = [(f"str.lower {n}", f"s = t[:{n}]", "s.lower()")
           for n in (1, 3, 5, 7, 8, 11, 15, 16, 32, 64, 1024, 65536)]
for n in (1, 7, 8, 16, 1024):
    BENCHES.append((f"str.upper {n}", f"s = t[:{n}]", "s.upper()"))
    BENCHES.append((f"bytes.lower {n}", f"s = t[:{n}].encode()", "s.lower()"))
BENCHES.append(("words (1100, 2-6 chars)", "", "[w.lower() for w in words]"))
BENCHES.append(("headers (400, 4-15 chars)", "", "[h.lower() for h in hdrs]"))


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw).stdout.strip()


def cpu_model():
    system = platform.system()
    try:
        if system == "Linux":
            for line in run(["lscpu"]).splitlines():
                if line.startswith("Model name"):
                    return line.split(":", 1)[1].strip()
        elif system == "Darwin":
            return (run(["sysctl", "-n", "machdep.cpu.brand_string"])
                    or run(["sysctl", "-n", "hw.model"]))
        elif system == "Windows":
            return run(["powershell", "-NoProfile", "-Command",
                        "(Get-CimInstance Win32_Processor).Name"])
    except OSError as e:
        return f"unknown ({e})"
    return "unknown"


def main():
    if sys.argv[1] == "--which":
        print(which(sys.argv[2]))
        return
    base_tree, patched_tree, out, pyperf_dir = sys.argv[1:5]
    os.makedirs(out, exist_ok=True)
    builds = [("base", os.path.abspath(which(base_tree))),
              ("patched", os.path.abspath(which(patched_tree)))]
    env = dict(os.environ, PYTHONPATH=os.path.abspath(pyperf_dir))
    procs = os.environ.get("BENCH_PROCS", "10")

    meta = {
        "runner": os.environ.get("BENCH_RUNNER", ""),
        "image": f"{os.environ.get('ImageOS', '')} {os.environ.get('ImageVersion', '')}".strip(),
        "build": os.environ.get("BENCH_BUILD", ""),
        "rep": os.environ.get("BENCH_REP", ""),
        "machine": platform.machine(),
        "cpu": cpu_model(),
        "cpus": os.cpu_count(),
        "procs": procs,
    }
    for name, py in builds:
        meta[f"{name}_version"] = run([py, "-c", "import sys; print(sys.version)"])
    print(json.dumps(meta, indent=2), flush=True)
    with open(os.path.join(out, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    for name, _ in builds:
        path = os.path.join(out, f"{name}.json")
        if os.path.exists(path):
            os.remove(path)
    for i, (bench, setup, stmt) in enumerate(BENCHES):
        order = builds if i % 2 == 0 else builds[::-1]
        for name, py in order:
            cmd = [py, "-m", "pyperf", "timeit", "-q", "-p", procs,
                   "--name", bench, "-s", SETUP + "\n" + setup, stmt,
                   "--append", os.path.join(out, f"{name}.json")]
            r = subprocess.run(cmd, env=env, capture_output=True, text=True)
            line = (r.stdout.strip().splitlines() or [""])[-1]
            print(f"{name:8} {bench:28} {line}", flush=True)
            if r.returncode:
                print(r.stderr, file=sys.stderr)
                sys.exit(r.returncode)

    table = run([builds[1][1], "-m", "pyperf", "compare_to",
                 os.path.join(out, "base.json"),
                 os.path.join(out, "patched.json"), "--table"], env=env)
    print(table)
    with open(os.path.join(out, "compare.txt"), "w") as f:
        f.write(table + "\n")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"### {meta['runner']} / {meta['build']} / run {meta['rep']}\n\n")
            f.write(f"CPU: {meta['cpu']} ({meta['cpus']} CPUs), {meta['machine']}\n\n")
            f.write(f"`{meta['patched_version']}`\n\n```\n{table}\n```\n")


if __name__ == "__main__":
    main()
