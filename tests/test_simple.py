import unittest
import mock

from .util import load_dump

from rdbtools3 import parse_rdb_stream


class TestSimple(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.rdb = load_dump('encodings.rdb')

    def tearDown(self):
        del self.rdb

    def test_parse(self):
        ret = list(parse_rdb_stream(self.rdb))
        self.assertEqual(len(ret), 13)
        return ret

    def testSimple(self):
        items = list(map(tuple, self.test_parse()))

        expected = [
        #    db, type, name, value, expire, extra info
            (0, 'zset', b'zset', mock.ANY, None, {}),
            (0, 'set', b'set_zipped_1', mock.ANY, None, {}),
            (0, 'list', b'list_zipped', mock.ANY, None, {}),
            (0, 'string', b'string', mock.ANY, None, {}),
            (0, 'string', b'compressible', mock.ANY, None, {}),
            (0, 'set', b'set_zipped_2', mock.ANY, None, {}),
            (0, 'string', b'number', mock.ANY, None, {}),
            (0, 'set', b'set_zipped_3', mock.ANY, None, {}),
            (0, 'set', b'set', mock.ANY, None, {}),
            (0, 'list', b'list', mock.ANY, None, {}),
            (0, 'hash', b'hash_zipped', mock.ANY, None, {}),
            (0, 'zset', b'zset_zipped', mock.ANY, None, {}),
            (0, 'hash', b'hash', mock.ANY, None, {}),
            ]
        self.assertEqual(expected, items)

    def testKeyValue_zset(self):
        # FIXME: must be int/float
        item = self.test_parse()[0]
        self.assertEqual([
            (b'bb', b'20'),
            (b'cc', b'30'),
            (b'bbb', b'200'),
            (b'bbbb', b'5000000000'),
            (b'ccc', b'300'),
            (b'cccc', b'123456789'),
            (b'a', b'1'),
            (b'aa', b'10'),
            (b'b', b'2'),
            (b'aaa', b'100'),
            (b'c', b'3'),
            (b'aaaa', b'1000'),
            ], item.value)
