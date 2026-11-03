# Which lengths reach lower() and upper() in practice

`hist_patch.py` adds a length count to `_Py_bytes_lower()` and `_Py_bytes_upper()`
in a scratch build (everything that reaches the PR's code: `str.lower`/`upper`/`casefold`
on ASCII strings, `bytes` and `bytearray`, including C callers such as
`sorted(key=str.lower)`). With `CASE_HIST=FILE` set, each process appends its counts at exit.

`workloads.py` runs everyday stdlib tasks, one per process, over a CPython source tree
(gcc 13.3 build of the PR on Linux):

- `email`: parse `Lib/test/test_email/data/msg_*.txt` and read their headers and text parts
- `http`: `http.server` serving `Lib/` to `http.client` (150 GETs with browser-like headers)
- `html`: `html.parser` over pydoc's HTML for 20 stdlib modules
- `words`: `w.lower()` for every word of `Doc/**/*.rst`
- `doclower`: `.lower()` on each whole `Doc/**/*.rst` file
- `paths`: `os.walk` the tree, lowercase each extension and call `mimetypes.guess_type`
- `urls`: `urllib.parse` on every URL in `Doc/**/*.rst`
- `config`: `configparser` on the tree's `.cfg`/`.ini` files and a generated one
- `pgotask`: CPython's own PGO training run, `python -m test --pgo`

`hist/hist_<workload>.txt` has lines `l|u LENGTH COUNT` (lower/upper); 4096 means 4096 or
more, and `bigbytes` is their total length.

`replay.py HISTDIR OUT.json` times `for s in L: s.lower()` over shuffled ASCII strings with
each workload's length mix, so two builds can be compared on it.
