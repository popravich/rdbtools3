import unittest

from rdbtools3.intset import unpack_intset
from rdbtools3.exceptions import RDBValueError


class TestIntset(unittest.TestCase):

    def test_3x2bytes(self):
        val = (b'\x02\x00\x00\x00'  # int size
               b'\x03\x00\x00\x00'  # set length
               b'\x01\x00'          # item 1
               b'\x02\x00'          # item 2
               b'\x00\x01')         # item 3
        ret = list(unpack_intset(val))
        self.assertEqual([
            1, 2, 256
            ], ret)

    def test_2x4bytes(self):
        val = (b'\x04\x00\x00\x00'
               b'\x02\x00\x00\x00'
               b'\x01\x00\x00\x00'
               b'\x00\x00\x00\x80')
        ret = list(unpack_intset(val))
        self.assertEqual([
            1, 2**31
            ], ret)

    def test_2x8bytes(self):
        val = (b'\x08\x00\x00\x00'
               b'\x02\x00\x00\x00'
               b'\x01\x00\x00\x00\x00\x00\x00\x00'
               b'\x00\x00\x00\x00\x00\x00\x00\x80')
        ret = list(unpack_intset(val))
        self.assertEqual([
            1, 2**63
            ], ret)

    def test_bad_length(self):
        val = (b'\x02\x00\x00\x00'
               b'\x01\x00\x00\x00'
               b'\x01\x00'
               b'\x02\x00\x00')
        with self.assertRaisesRegex(RDBValueError,
                "Bad content size 5 \(expected 2\)"):
            list(unpack_intset(val))

    def test_bad_size_encoding(self):
        val = (b'\x03\x00\x00\x00'
               b'\x01\x00\x00\x00'
               b'\x00\x00\x00')
        with self.assertRaisesRegex(RDBValueError,
                "Unexpected size encoding 0x3"):
            list(unpack_intset(val))


    def test_zero_len(self):
        val = (b'\x02\x00\x00\x00'
               b'\x00\x00\x00\x00')
        ret = list(unpack_intset(val))
        self.assertEqual([], ret)


if __name__ == "__main__":
    unittest.main()
