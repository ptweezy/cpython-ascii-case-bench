"""Add a length histogram to _Py_bytes_lower/_Py_bytes_upper (scratch builds only).

At exit, if CASE_HIST names a file, append "l|u LEN COUNT" lines to it.
Lengths >= 4096 share one bucket; their total length is kept separately.
"""
import sys
p = sys.argv[1]
src = open(p).read()
helper = r'''
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
static unsigned long long case_hist[2][4097], case_big_bytes[2];
__attribute__((destructor)) static void
case_hist_dump(void)
{
    const char *path = getenv("CASE_HIST");
    FILE *f;
    if (path == NULL || (f = fopen(path, "a")) == NULL) {
        return;
    }
    fprintf(f, "# pid %d\n", (int)getpid());
    for (int k = 0; k < 2; k++) {
        for (int i = 0; i <= 4096; i++) {
            if (case_hist[k][i]) {
                fprintf(f, "%c %d %llu\n", "lu"[k], i, case_hist[k][i]);
            }
        }
        if (case_big_bytes[k]) {
            fprintf(f, "%c bigbytes %llu\n", "lu"[k], case_big_bytes[k]);
        }
    }
    fclose(f);
}
#define CASE_HIST(k, len) do { \
        if ((len) >= 4096) { case_hist[k][4096]++; case_big_bytes[k] += (len); } \
        else { case_hist[k][(len)]++; } \
    } while (0)
'''
anchor = "/* Return 0x20 in each byte"
assert src.count(anchor) == 1
src = src.replace(anchor, helper + "\n" + anchor)
for k, name in ((0, "_Py_bytes_lower"), (1, "_Py_bytes_upper")):
    sig = f"\n{name}(char *result, const char *cptr, Py_ssize_t len)\n{{\n"
    assert src.count(sig) == 1, name
    i = src.index(sig) + len(sig)
    j = src.index("\n\n", i) + 1      # after the local declarations
    src = src[:j] + f"    CASE_HIST({k}, len);\n" + src[j:]
open(p, "w").write(src)
print("patched", p)
