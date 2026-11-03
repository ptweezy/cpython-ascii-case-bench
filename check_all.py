"""Check lower() and upper() of bytes, bytearray and ASCII str against a
reference built on translate(), which doesn't share their code.

- every byte value (0..255 for bytes and bytearray, 0..127 for str) at every
  position, for every length 0..80, on a random background;
- the same at the first, middle and last 9 positions of lengths around
  multiples of the word size up to 4,096;
- random content at every length 0..1,100;
- unaligned buffers: a bytearray whose first k bytes were deleted starts k
  bytes into its allocation, for every k in 0..15;
- bytes/bytearray capitalize() and str casefold(), which share the code.
"""
import random
import sys

UP, LO = bytes(range(65, 91)), bytes(range(97, 123))
TO_LOWER, TO_UPPER = bytes.maketrans(UP, LO), bytes.maketrans(LO, UP)
rng = random.Random(161155)
cases = 0


def check_bytes(b):
    global cases
    lo, up = b.translate(TO_LOWER), b.translate(TO_UPPER)
    assert b.lower() == lo and b.upper() == up, b
    cap = b[:1].translate(TO_UPPER) + b[1:].translate(TO_LOWER)
    assert b.capitalize() == cap, b
    ba = bytearray(b)
    assert ba.lower() == lo and ba.upper() == up and ba.capitalize() == cap, b
    assert ba == b  # unchanged
    cases += 1


def check_str(s):
    global cases
    e = s.encode("ascii")
    lo, up = e.translate(TO_LOWER).decode(), e.translate(TO_UPPER).decode()
    assert s.lower() == lo and s.upper() == up and s.casefold() == lo, s
    assert s.lower().isascii() and s.upper().isascii()
    cases += 1


def check_unaligned(b):
    global cases
    lo, up = b.translate(TO_LOWER), b.translate(TO_UPPER)
    for k in range(16):
        ba = bytearray(rng.randbytes(k)) + b
        del ba[:k]  # moves the start, not the data
        assert ba.lower() == lo and ba.upper() == up, (k, b)
        cases += 1


def every_value_at(n, positions):
    for pos in positions:
        bg = rng.randbytes(n)
        sbg = bytes(c & 0x7F for c in bg)
        for v in range(256):
            b = bg[:pos] + bytes([v]) + bg[pos + 1:]
            check_bytes(b)
            if v < 128:
                check_str((sbg[:pos] + bytes([v]) + sbg[pos + 1:]).decode())


for n in range(81):
    every_value_at(n, range(n))
    if n:
        check_unaligned(rng.randbytes(n))

W = 8
for n in sorted({m * W + d for m in (3, 4, 8, 16, 32, 64, 128, 512) for d in (-1, 0, 1)}):
    mid = n // 2 - 4
    every_value_at(n, sorted(set(range(9)) | set(range(mid, mid + 9)) | set(range(n - 9, n))))
    check_unaligned(rng.randbytes(n))

for n in range(1101):
    b = rng.randbytes(n)
    check_bytes(b)
    check_str(bytes(c & 0x7F for c in b).decode())
    if n % 7 == 0:
        check_unaligned(b)

print(f"ok {cases} cases ({sys.version.split()[0]}, {sys.version.split('[')[-1][:-1]})")
