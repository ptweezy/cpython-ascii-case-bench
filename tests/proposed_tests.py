"""Proposed additions for gh-161155 (run standalone against a built python).

A) string_tests.BaseTest (runs for str, UserString, bytes, bytearray):
   test_lower_upper_long
B) test_bytes.BaseBytesTest (bytes, bytearray): test_lower_upper_every_byte
"""
import sys
import time
import unittest
from collections import UserString
from test import string_tests


class LongCaseMixin:
    # --- would go in Lib/test/string_tests.py, class BaseTest, after test_upper
    def test_lower_upper_long(self):
        # gh-161155: lower() and upper() convert ASCII strings several
        # characters at a time.  Put a letter or a character next to the
        # letter ranges at every position of strings around those sizes.
        lengths = [*range(1, 41), 63, 64, 65, 1000]
        for n in lengths:
            positions = range(n) if n < 100 else [*range(20), *range(n - 20, n)]
            for i in positions:
                for c in 'AZaz@[`{':
                    s = '0' * i + c + '9' * (n - i - 1)
                    self.checkequal(s[:i] + c.lower() + s[i+1:], s, 'lower')
                    self.checkequal(s[:i] + c.upper() + s[i+1:], s, 'upper')
        s = 'Hello, World! ' * 10
        self.checkequal('hello, world! ' * 10, s, 'lower')
        self.checkequal('HELLO, WORLD! ' * 10, s, 'upper')


class EveryByteMixin:
    # --- would go in Lib/test/test_bytes.py, class BaseBytesTest
    def test_lower_upper_every_byte(self):
        # gh-161155: every byte value at every position of lengths around
        # the 8 and 16 bytes that lower() and upper() convert at once,
        # including unaligned bytearrays.
        lo = b'abcdefghijklmnopqrstuvwxyz'
        up = lo.upper()
        to_lower = bytes.maketrans(up, lo)
        to_upper = bytes.maketrans(lo, up)
        bg = b'aZ@[`{zA\x80\xc1\xda\xe1\xfa\xff\x7f\x00' * 3
        for n in (7, 8, 9, 15, 16, 17, 31, 32, 33):
            for i in range(n):
                for v in range(256):
                    b = self.type2test(bg[:i] + bytes([v]) + bg[i+1:n])
                    self.assertEqual(b.lower(), b.translate(to_lower))
                    self.assertEqual(b.upper(), b.translate(to_upper))
        data = bytes(range(256)) * 2
        for k in range(16):
            b = bytearray(k) + data
            del b[:k]  # moves the start of the buffer
            self.assertEqual(b.lower(), data.translate(to_lower))
            self.assertEqual(b.upper(), data.translate(to_upper))


class StrT(LongCaseMixin, string_tests.BaseTest, unittest.TestCase):
    type2test = str
class UserStrT(LongCaseMixin, string_tests.BaseTest, unittest.TestCase):
    type2test = UserString
class FixedB(string_tests.BaseTest):
    def fixtype(self, obj):
        if isinstance(obj, str):
            return self.type2test(obj.encode("utf-8"))
        return super().fixtype(obj)
class BytesStrT(LongCaseMixin, FixedB, unittest.TestCase):
    type2test = bytes
class ByteArrayStrT(LongCaseMixin, FixedB, unittest.TestCase):
    type2test = bytearray
class BytesT(EveryByteMixin, unittest.TestCase):
    type2test = bytes
class ByteArrayT(EveryByteMixin, unittest.TestCase):
    type2test = bytearray

if __name__ == '__main__':
    t0 = time.perf_counter()
    # Only the proposed tests: the classes inherit all of string_tests, and
    # some of those don't apply to bytes in this standalone setup.
    r = unittest.main(exit=False, verbosity=2,
                      argv=[sys.argv[0], '-k', 'test_lower_upper', *sys.argv[1:]]).result
    print(f"elapsed {time.perf_counter() - t0:.2f}s on {sys.version.split()[0]}")
