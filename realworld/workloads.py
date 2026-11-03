"""Everyday stdlib tasks, run one per process, to see which string lengths
reach str/bytes lower() and upper() (counted inside the C code by a
scratch build; see hist_patch.py).

    python workloads.py NAME SRC      # SRC: a CPython source tree (Lib/, Doc/)
"""
import glob, os, re, sys, threading
from collections import Counter

name, SRC = sys.argv[1], sys.argv[2]
rst = sorted(glob.glob(os.path.join(SRC, "Doc", "**", "*.rst"), recursive=True))


def email_():
    import email, email.policy
    for p in sorted(glob.glob(os.path.join(SRC, "Lib", "test", "test_email", "data", "msg_*.txt"))):
        with open(p, "rb") as f:
            msg = email.message_from_binary_file(f, policy=email.policy.default)
        for part in msg.walk():
            for k, v in part.items():
                str(v)
            part.get_content_type(); part.get_content_charset(); part.get_filename()
            part["subject"]; part["from"]; part["to"]; part["date"]; part["message-id"]
            if part.get_content_maintype() == "text":
                try:
                    part.get_content()
                except Exception:
                    pass


def http():
    import http.client, http.server, functools
    root = os.path.join(SRC, "Lib")
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
    http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    files = sorted(f for f in os.listdir(root) if f.endswith(".py"))[:150]
    conn = http.client.HTTPConnection("127.0.0.1", srv.server_address[1])
    for f in files:
        conn.request("GET", "/" + f, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Example/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "no-cache", "Connection": "keep-alive"})
        r = conn.getresponse()
        r.read()
        r.getheader("Content-Type"); r.getheader("Content-Length"); r.getheader("Last-Modified")
        r.getheader("Connection")
    srv.shutdown()


def html_gen():
    import pydoc, importlib
    out = "/tmp/pydoc_html"
    os.makedirs(out, exist_ok=True)
    for m in ("os", "re", "json", "email.message", "http.client", "collections", "pathlib",
              "argparse", "logging", "subprocess", "typing", "datetime", "functools", "itertools",
              "string", "textwrap", "urllib.parse", "html.parser", "csv", "configparser"):
        mod = importlib.import_module(m)
        with open(os.path.join(out, m + ".html"), "w", encoding="utf-8") as f:
            f.write(pydoc.html.page(pydoc.describe(mod), pydoc.html.document(mod, m)))


def html():
    from html.parser import HTMLParser
    class P(HTMLParser):
        def handle_starttag(self, tag, attrs):
            self.n = getattr(self, "n", 0) + 1
    for p in sorted(glob.glob("/tmp/pydoc_html/*.html")):
        P().feed(open(p, encoding="utf-8").read())


def words():
    c = Counter()
    for p in rst:
        for w in re.findall(r"[A-Za-z']+", open(p, encoding="utf-8").read()):
            c[w.lower()] += 1


def doclower():
    c = Counter()
    for p in rst:
        c.update(re.findall(r"[a-z']+", open(p, encoding="utf-8").read().lower()))


def paths():
    import mimetypes
    mimetypes.init()
    for d, _, fs in os.walk(SRC):
        for f in fs:
            p = os.path.join(d, f)
            os.path.splitext(f)[1].lower()
            mimetypes.guess_type(p)


def urls():
    import urllib.parse
    pat = re.compile(r"https?://[^\s<>`'\")]+")
    for p in rst:
        for u in pat.findall(open(p, encoding="utf-8").read()):
            s = urllib.parse.urlsplit(u)
            s.hostname
            try:
                s.port
            except ValueError:
                pass
            urllib.parse.urlparse(u).scheme
            urllib.parse.parse_qs(s.query)


def config():
    import configparser
    paths = [p for p in glob.glob(os.path.join(SRC, "**", "*.*"), recursive=True)
             if p.endswith((".cfg", ".ini", ".toml.cfg"))]
    text = "".join(f"[section{i}]\nServerAliveInterval = {i}\nCompression = yes\n"
                   f"ForwardX11 = no\nUser = hg\nPort = 50022\nlog_level = INFO\n"
                   f"Enable_Feature_X = true\n\n" for i in range(300))
    for src in [text] + [open(p, encoding="utf-8", errors="replace").read() for p in paths]:
        cp = configparser.ConfigParser(interpolation=None, strict=False)
        try:
            cp.read_string(src)
        except configparser.Error:
            continue
        for s in cp.sections():
            for k in cp[s]:
                v = cp[s][k]
                if v.lower() in ("yes", "no", "true", "false", "on", "off", "1", "0"):
                    cp.getboolean(s, k)


{"email": email_, "http": http, "html-gen": html_gen, "html": html, "words": words,
 "doclower": doclower, "paths": paths, "urls": urls, "config": config}[name]()
