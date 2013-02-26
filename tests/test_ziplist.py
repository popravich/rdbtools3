import unittest
from io import BytesIO

from rdbtools3.ziplist import unpack_ziplist, unpack_ziplist_entry
from rdbtools3.exceptions import RDBValueError


class TestZiplist(unittest.TestCase):

    def test_empty(self):
        data = b'\x00' * 4
        data += b'\x00' * 4
        data += b'\x00' * 2
        data += b'\xFF'
        ret = list(unpack_ziplist(data))
        self.assertEqual([], ret)

    def test_bad_end(self):
        data = b'\x00' * 4
        data += b'\x00' * 4
        data += b'\x00' * 2
        with self.assertRaises(TypeError):
            list(unpack_ziplist(data))

        data += b'\xFE'
        with self.assertRaises(RDBValueError):
            list(unpack_ziplist(data))

    def test_simple(self):
        data = b'\x00' * 4
        data += b'\x00' * 4
        data += b'\x02\x00'
        data += b'\x00\x03key'
        data += b'\x00\xF2'
        data += b'\xFF'
        ret = list(unpack_ziplist(data))
        self.assertEqual([b'key', 1], ret)

if __name__ == "__main__":
    unittest.main()
