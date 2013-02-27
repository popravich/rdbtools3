from io import BytesIO
import unittest

from rdbtools3.zipmap import unpack_zipmap, read_next_len
from rdbtools3.exceptions import RDBValueError


class TestZipmap(unittest.TestCase):

    def testReadLen_single_byte(self):
        s = BytesIO(b'\x01\x02')
        ret = read_next_len(s)
        self.assertEqual(1, ret)

        s = BytesIO(b'\xFD')
        ret = read_next_len(s)
        self.assertEqual(253, ret)

    def testReadLen_254(self):
        s = BytesIO(b'\xFE\x02\x00\x00\x00')
        ret = read_next_len(s)
        self.assertEqual(2, ret)

    def testReadLen_255(self):
        s = BytesIO(b'\xFF\x00')
        ret = read_next_len(s)
        self.assertIsNone(ret)

    def testUnpack_simple(self):
        data = (b'\x02'     # items
                b'\x03'     # item1 len
                b'Key'      # key
                b'\x05'     # value len
                b'\x00'     # free bytes
                b'Value'    # value
                b'\x04Key1\x06\x01Value2\x00'
                b'\xFF')    # end of zipmap
        ret = list(unpack_zipmap(data))
        self.assertEqual([
            (b'Key', b'Value'),
            (b'Key1', b'Value2'),
            ], ret)

    def testUnpack_long_key(self):
        data = b'\x01\xFE\x00\x01\x00\x00'
        data += b'a' * 256
        data += b'\x03\x00val\xFF'
        ret = list(unpack_zipmap(data))
        self.assertEqual([
            (b'a' * 256, b'val'),
            ], ret)

    def testUnpack_bad_value_len(self):
        data = (b'\x02\x02k1\x02\x00v1'
                b'\x02k2\xFF\x00v2\xFF')
        with self.assertRaises(RDBValueError):
            list(unpack_zipmap(data))

    def testUnpack_empty(self):
        data = b'\x00\xFFspam'
        ret = list(unpack_zipmap(data))
        self.assertEqual([], ret)

        data = b'\x01\xFFspam'
        with self.assertRaises(RDBValueError):
            list(unpack_zipmap(data))

    def testUnpack_no_entries_count(self):
        data = b'\xFF\xFF'
        ret = list(unpack_zipmap(data))
        self.assertEqual([], ret)


if __name__ == "__main__":
    unittest.main()
