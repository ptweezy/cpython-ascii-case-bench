"""Insert the two proposed tests (tests/proposed_tests.py) into a CPython
tree, where a PR would put them: test_lower_upper_long into
Lib/test/string_tests.py (BaseTest, after test_upper), and
test_lower_upper_every_byte into Lib/test/test_bytes.py (end of
BaseBytesTest).  test_str and test_bytes are in CPython's PGO training
(Lib/test/libregrtest/pgo.py), so the tests also change what PGO sees.

    python add_tests.py CPYTHON_TREE
"""
import os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
prop = open(os.path.join(here, "proposed_tests.py"), encoding="utf-8").read()


def method(name):
    m = re.search(r"(    def %s\(self\):\n.*?)(?=\n\n\S|\nclass )" % name, prop, re.S)
    return m.group(1).rstrip() + "\n"


tree = sys.argv[1]
p = os.path.join(tree, "Lib/test/string_tests.py")
s = open(p, encoding="utf-8").read()
anchor = "    def test_upper(self):\n"
i = s.index(anchor)
j = s.index("\n\n", i) + 2  # end of test_upper
s = s[:j] + method("test_lower_upper_long") + "\n" + s[j:]
open(p, "w", encoding="utf-8").write(s)

p = os.path.join(tree, "Lib/test/test_bytes.py")
s = open(p, encoding="utf-8").read()
anchor = "\n\n\nclass BytesTest(BaseBytesTest, unittest.TestCase):"
assert s.count(anchor) == 1
s = s.replace(anchor, "\n\n" + method("test_lower_upper_every_byte") + anchor[1:], 1)
open(p, "w", encoding="utf-8").write(s)
print("inserted")
