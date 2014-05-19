import unittest
from io import BytesIO

from rdbtools3.lzf import unpack_lzf
from rdbtools3.exceptions import RDBValueError


class TestLZF(unittest.TestCase):

    def test_simple(self):
        data = BytesIO(b'\x04ABCDE')

        ret = unpack_lzf(data, 6, 5)
        self.assertEqual(b'ABCDE', ret)

    def test_empty(self):
        data = BytesIO(b'\x00')
        ret = unpack_lzf(data, 0, 0)
        self.assertEqual(b'', ret)

    def test_bad_lenghts(self):
        with self.assertRaises(RDBValueError):
            unpack_lzf(BytesIO(b'\x00'), 1, 1)
        with self.assertRaises(RDBValueError):
            unpack_lzf(BytesIO(b'\x00'), 0, 1)
        with self.assertRaises(ValueError):
            unpack_lzf(BytesIO(b'\x01'), 1, 1)

    def test_simple_backref(self):
        data = (b'\x01AB'       # simple
                b'\x60\x01')    # backref: len 3+2; back 2-1-1
        ret = unpack_lzf(BytesIO(data), 5, 7)
        self.assertEqual(b'ABABABA', ret)

    def test_longer_backref(self):
        data = (b'\x01AB'
                b'\xE0\x01\x00')    # backref: len 7+1+2; back 2-0-1
        ret = unpack_lzf(BytesIO(data), 6, 12)
        self.assertEqual(b'ABBBBBBBBBBB', ret)


if __name__ == "__main__":
    unittest.main()
