"""Relink a built CPython tree's python3XX.dll at several code placements.

    python win_relink.py TREE N [N ...] [--plat x64|Win32|ARM64] [--config Release]

For each N (a multiple of 16, 0 <= N <= 4080) this makes
TREE\\PCbuild\\<arch>-padN\\, a copy of TREE\\PCbuild\\<arch>\\ (without
.pdb/.lib/.exp files) whose python3XX.dll is relinked from the tree's own
object files with a padding object of N bytes ahead of all code: every
function of the DLL moves by exactly N bytes and no instruction changes.
python.exe in that directory runs like the one in <arch>\\ (pybuilddir.txt
and the ..\\..\\Lib lookup are the same).

How: msbuild records the DLL's link command in
PCbuild\\obj\\<ver><arch>_<config>\\pythoncore\\pythoncore.tlog\\link.command.1.tlog.
The command is replayed with link.exe (from the newest Visual Studio, found
with vswhere) with its outputs redirected, and with the environment variable
_LINK_ set to padN.obj, which link.exe appends to its command line.  The pad
object has a code section named ".text$a"; the linker sorts sections of a
group by the name after "$" and MSVC's code is in ".text$mn" and later, so the
pad lands first in .text whatever its place on the command line.  A tail
section ".text$~~" of 4096 - N bytes (sorted after every other group,
including the ".text$zs/zy/zz" groups of a PGO build) keeps .text the same
size, so data addresses are the same at every placement.  The LTCG code generation is
rerun but is deterministic (a relink without the pad reproduces the
original DLL's code byte for byte).

Do not use /LTCG:INCREMENTAL to speed this up: it generates different code.
The same _LINK_ trick also works for a full build (set _LINK_ before
PCbuild\\build.bat); the pad object has machine type "any" and a @feat.00
symbol, so it also links into the Win32 _freeze_module.exe build.bat makes.
"""
import argparse
import os
import re
import shutil
import struct
import subprocess
import sys

ARCH = {"x64": ("amd64", "x64"), "Win32": ("win32", "x64_x86"), "ARM64": ("arm64", "x64_arm64")}


def make_pad(n, path, total=4096):
    # IMAGE_SCN_CNT_CODE | IMAGE_SCN_ALIGN_16BYTES | MEM_EXECUTE | MEM_READ
    chars = 0x00000020 | 0x00500000 | 0x20000000 | 0x40000000
    sections = [(b".text$a", b"\xcc" * n), (b".text$~~", b"\xcc" * (total - n))]
    hdr = 20 + 40 * len(sections)
    raw = shdrs = b""
    for name, data in sections:
        shdrs += struct.pack("<8sIIIIIIHHI", name.ljust(8, b"\0"), 0, 0, len(data),
                             hdr + len(raw) if data else 0, 0, 0, 0, 0, chars)
        raw += data
    syms = struct.pack("<8sIhHBB", b"@feat.00", 1, -1, 0, 3, 0)   # SafeSEH-compatible
    fhdr = struct.pack("<HHIIIHH", 0, len(sections), 0, hdr + len(raw), 1, 0, 0)
    with open(path, "wb") as f:
        f.write(fhdr + shdrs + raw + syms + struct.pack("<I", 4))


def vcvarsall():
    vswhere = os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                           "Microsoft Visual Studio", "Installer", "vswhere.exe")
    out = subprocess.run([vswhere, "-latest", "-products", "*", "-requires",
                          "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                          "-property", "installationPath"],
                         capture_output=True, text=True, check=True).stdout.strip()
    return os.path.join(out.splitlines()[0], r"VC\Auxiliary\Build\vcvarsall.bat")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tree")
    ap.add_argument("pads", type=int, nargs="+")
    ap.add_argument("--plat", default="x64", choices=ARCH)
    ap.add_argument("--config", default="Release")
    a = ap.parse_args()
    tree = os.path.abspath(a.tree)
    arch, vcarch = ARCH[a.plat]
    pcb = os.path.join(tree, "PCbuild")
    src = os.path.join(pcb, arch)
    objroot = os.path.join(pcb, "obj")
    cand = [d for d in os.listdir(objroot) if d.endswith("%s_%s" % (arch, a.config))]
    if len(cand) != 1:
        sys.exit("no unique obj dir for %s_%s in %s: %s" % (arch, a.config, objroot, cand))
    tlog = os.path.join(objroot, cand[0], "pythoncore", "pythoncore.tlog", "link.command.1.tlog")
    with open(tlog, encoding="utf-16") as f:
        lines = f.read().splitlines()
    cmd = "\n".join(l for l in lines[1:] if l.strip())   # line 0 lists the inputs
    dllname = os.path.basename(re.search(r'/OUT:"([^"]+)"', cmd).group(1)).lower()
    vcv = vcvarsall()
    for n in a.pads:
        if n % 16 or not 0 <= n <= 4080:
            sys.exit("pad must be a multiple of 16 in 0..4080: %d" % n)
        out = os.path.join(pcb, "%s-pad%d" % (arch, n))
        if os.path.isdir(out):
            shutil.rmtree(out)
        # A PGO (--config PGUpdate) relink reads the merged .pgd next to /OUT;
        # leave the .pgc files behind or link.exe would merge them again.
        shutil.copytree(src, out, ignore=shutil.ignore_patterns(
            "*.pdb", "*.lib", "*.exp", "*.ilk", "*.iobj", "*.ipdb", "*.pgc", "instrumented"))
        pad = os.path.join(out, "pad%d.obj" % n)
        make_pad(n, pad)
        text = cmd
        for opt, name in (("OUT", dllname), ("PDB", dllname[:-4] + ".pdb"),
                          ("IMPLIB", dllname[:-4] + ".lib"), ("LTCGOUT", dllname[:-4] + ".iobj")):
            new = '/%s:"%s"' % (opt, os.path.join(out, name))
            text, k = re.subn(r'/%s:"[^"]*"' % opt, lambda m: new, text)
            if opt != "LTCGOUT" and k != 1:
                sys.exit("cannot redirect /%s in %s" % (opt, tlog))
        rsp = os.path.join(out, "relink.rsp")
        with open(rsp, "w") as f:
            f.write(text + "\n/MAP\n")
        env = dict(os.environ, _LINK_=pad)
        p = subprocess.run('call "%s" %s >nul && link.exe @"%s"' % (vcv, vcarch, rsp),
                           shell=True, env=env, capture_output=True, text=True)
        if p.returncode:
            sys.exit("link failed for pad %d:\n%s%s" % (n, p.stdout, p.stderr))
        # check: the map file lists .text$a with N bytes at the start of .text
        mp = open(os.path.join(out, dllname[:-4] + ".map"), errors="replace").read()
        m = re.search(r"0001:([0-9a-f]{8}) ([0-9a-f]{8})H \.text\$a ", mp)
        m2 = re.search(r"0001:([0-9a-f]{8}) [0-9a-f]{8}H \.text\$mn ", mp)
        if not m or int(m.group(1), 16) != 0 or int(m.group(2), 16) != n or int(m2.group(1), 16) != n:
            sys.exit("pad %d: .text$a/.text$mn not where expected in the map" % n)
        print("%s: %s relinked, code starts at .text+%#x" % (out, dllname, n), flush=True)


if __name__ == "__main__":
    main()
