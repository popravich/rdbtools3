import unittest
from io import BytesIO

from rdbtools3.ziplist import unpack_ziplist, unpack_ziplist_entry
from rdbtools3.exceptions import RDBValueError


class TestZiplistEntry(unittest.TestCase):

    def test_bad_prev_length(self):
        data = b'\xFFabc'
        with self.assertRaises(RDBValueError):
            unpack_ziplist_entry(BytesIO(data))

    def test_str_6bit(self):
        data1 = b'\x00'
        data1 += b'\x01'
        data1 += b'A'
        ret = unpack_ziplist_entry(BytesIO(data1))
        self.assertEqual(b'A', ret)

        data2 = b'\x00'
        data2 += b'\x3F'
        data2 += b'a' * 63
        ret = unpack_ziplist_entry(BytesIO(data2))
        self.assertEqual(b'a' * 63, ret)

    def test_str_14bit(self):
        data1 = b'\x00'
        data1 += b'\x40\x01'
        data1 += b'A'
        ret = unpack_ziplist_entry(BytesIO(data1))
        self.assertEqual(b'A', ret)

        data2 = b'\x00'
        data2 += b'\x60\x00'
        data2 += b'a' * (2 ** 13)
        ret = unpack_ziplist_entry(BytesIO(data2))
        self.assertEqual(b'a' * (2 ** 13), ret)
        self.assertEqual(8192, len(ret))


if __name__ == "__main__":
    unittest.main()
