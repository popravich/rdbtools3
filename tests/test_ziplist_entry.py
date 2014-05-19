import unittest
from io import BytesIO

from rdbtools3.ziplist import unpack_ziplist_entry
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

    def test_str_32bit(self):
        data = b'\x00'
        data += b'\x80\x08\x00\00\x00'
        data += b'A' * 8
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(b'AAAAAAAA', ret)

    def test_int_16bit(self):
        data = b'\x00'
        data += b'\xC0'
        data += b'\x01\x00'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(1, ret)

        data = b'\x00\xC0\x00\x80'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(-32768, ret)

    def test_int_32bit(self):
        data = b'\x00\xD0\x01\x00\x00\x00'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(1, ret)

        data = b'\x00\xD0\x00\x00\x00\x80'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(-(2**31), ret)

    def test_int_64bit(self):
        data = b'\x00\xE0\x01\x00\x00\x00\x00\x00\x00\x00'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(1, ret)

        data = b'\x00\xE0\x00\x00\x00\x00\x00\x00\x00\x80'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(-(2**63), ret)

    def test_int_24bit(self):
        data = b'\x00\xF0\x01\x00\x00'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(1, ret)

        data = b'\x00\xF0\x00\x00\x80'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(-(2**23), ret)

    def test_int_8bit(self):
        data = b'\x00\xFE\x01'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(1, ret)

        data = b'\x00\xFE\x80'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(-128, ret)

    def test_uint_4bit(self):
        data = b'\x00\xF1'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(0, ret)

        data = b'\x00\xF2'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(1, ret)

        data = b'\x00\xFF'
        ret = unpack_ziplist_entry(BytesIO(data))
        self.assertEqual(14, ret)


if __name__ == "__main__":
    unittest.main()
