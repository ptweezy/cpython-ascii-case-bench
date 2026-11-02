"""Check str/bytes/bytearray lower()/upper() (and friends that share the
code) against a plain per-character reference.

Covers lengths 0..40 at every start offset 0..15 inside a larger buffer
(so the 8-byte loads start unaligned), every byte value 0..255 in every
position of the word, mixed ASCII/non-ASCII str, and a few long strings.
"""
import random

def ref_lower_b(b):
    return bytes(c + 32 if 65 <= c <= 90 else c for c in b)

def ref_upper_b(b):
    return bytes(c - 32 if 97 <= c <= 122 else c for c in b)

def check_bytes(b):
    lo, up = ref_lower_b(b), ref_upper_b(b)
    assert b.lower() == lo, (b, b.lower(), lo)
    assert b.upper() == up, (b, b.upper(), up)
    ba = bytearray(b)
    assert ba.lower() == lo and ba.upper() == up, b
    assert memoryview(b).tobytes().lower() == lo
    # bytes.capitalize() reuses _Py_bytes_lower for the tail
    if b:
        cap = ref_upper_b(b[:1]) + lo[1:]
        assert b.capitalize() == cap, (b, b.capitalize(), cap)

def check_str_ascii(s):
    assert s.isascii()
    lo = ''.join(chr(ord(c) + 32) if 'A' <= c <= 'Z' else c for c in s)
    up = ''.join(chr(ord(c) - 32) if 'a' <= c <= 'z' else c for c in s)
    assert s.lower() == lo, (s, s.lower(), lo)
    assert s.upper() == up, (s, s.upper(), up)
    assert s.casefold() == lo
    assert s.lower().isascii() and s.upper().isascii()

rng = random.Random(12345)
n = 0

# 1. every length 0..40 at every offset 0..15, random bytes and random ASCII
for trial in range(40):
    big = bytes(rng.randrange(256) for _ in range(80))
    bigs = ''.join(chr(rng.randrange(128)) for _ in range(80))
    for off in range(16):
        for length in range(41):
            check_bytes(big[off:off + length])
            # slicing makes a new object, so also go through memoryview
            check_bytes(bytes(memoryview(big)[off:off + length]))
            check_str_ascii(bigs[off:off + length])
            n += 3

# 2. every byte value in every position of a 16-byte buffer, on several fills
for fill in (0x00, 0x40, 0x41, 0x5A, 0x5B, 0x60, 0x61, 0x7A, 0x7B, 0x7F, 0x80, 0xC1, 0xDA, 0xFF):
    for pos in range(16):
        for v in range(256):
            buf = bytearray([fill]) * 16
            buf[pos] = v
            check_bytes(bytes(buf))
            check_bytes(bytes(buf[:pos + 1]))
            if v < 128 and fill < 128:
                check_str_ascii(buf.decode('ascii'))
            n += 3

# 3. the boundaries around the letter ranges, packed into one word
edge = bytes([0x40, 0x41, 0x5A, 0x5B, 0x60, 0x61, 0x7A, 0x7B,
              0xC0, 0xC1, 0xDA, 0xDB, 0xE0, 0xE1, 0xFA, 0xFB])
for length in range(len(edge) + 1):
    check_bytes(edge[:length])
    n += 1

# 4. mixed ASCII/non-ASCII str: non-ASCII strings take the Unicode path,
#    so only check that results still equal a per-character reference.
alphabet = 'abcXYZ09 _@[`{\x7f' + '\xe9\xc9\xdf\u0130\u03a3\u1e9e\ufb01\U0001d400'
for trial in range(3000):
    length = rng.randrange(41)
    s = ''.join(rng.choice(alphabet) for _ in range(length))
    assert s.lower() == ''.join(c.lower() for c in s) or '\u03a3' in s
    assert s.upper() == ''.join(c.upper() for c in s)
    n += 1
# an ASCII prefix longer than 8 followed by non-ASCII
for k in range(0, 33):
    s = 'HeLLo-WoRLD-' * 3
    s = s[:k] + '\xc9' + s[k:]
    assert s.lower() == ''.join(c.lower() for c in s)
    assert s.upper() == ''.join(c.upper() for c in s)
    n += 1

# 5. long strings
for length in (1000, 1023, 1024, 1025, 4096 + 3, 1 << 20):
    b = bytes(rng.randrange(256) for _ in range(length)) if length < 5000 else \
        rng.randbytes(length)
    check_bytes(b)
    s = b.decode('latin-1').encode('ascii', 'ignore').decode()
    s = ''.join(chr(c & 0x7f) for c in b[:length]) if length < 5000 else \
        bytes(c & 0x7f for c in b).decode()
    check_str_ascii(s)
    n += 2

print(f"OK: {n} cases")
