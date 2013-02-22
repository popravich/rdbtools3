import unittest
import mock

from .util import load_dump

from rdbtools3 import parse_rdb_stream


class TestSimple(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.rdb = load_dump('misc.rdb')

    def tearDown(self):
        del self.rdb

    def test_parse(self):
        ret = list(parse_rdb_stream(self.rdb))
        self.assertEqual(len(ret), 9)
        return ret

    def testSimple(self):
        items = list(map(tuple, self.test_parse()))

        expected = [
        #    db, type, name, value, expire, extra info
            (1, 'string', b'str2', mock.ANY, None, mock.ANY),
            (1, 'hash', b'hset1', mock.ANY, None, mock.ANY),
            (1, 'set', b'set1', mock.ANY, None, mock.ANY),
            (1, 'hash', b'some_long_hash_key_name', mock.ANY, None, mock.ANY),
            (1, 'zset', b'zset1', mock.ANY, None, mock.ANY),
            (1, 'string', 1, mock.ANY, None, mock.ANY),
            (1, 'string', b'str1', mock.ANY, None, mock.ANY),
            (2, 'string', b'str3_exp', mock.ANY, mock.ANY, mock.ANY),
            (2, 'list', b'list1', mock.ANY, None, mock.ANY),
            ]
        self.assertEqual(expected, items)

    def testKeyValue_str2(self):
        item = self.test_parse()[0]
        self.assertEqual(b'str2', item.key)
        self.assertEqual(123456789, item.value)
        self.assertEqual({
            'encoding': 'raw',
            }, item.info)
        self.assertIsNone(item.expire)

    def testKeyValue_hset1(self):
        item = self.test_parse()[1]
        self.assertEqual(b'hset1', item.key)
        self.assertEqual([
            (b'aa', b'10'),
            ], item.value)
        self.assertEqual({
            'encoding': 'zipmap',
            }, item.info)

    def testKeyValue_zset(self):
        # FIXME: must be int/float
        item = self.test_parse()[4]
        self.assertEqual(b'zset1', item.key)
        self.assertEqual([
            (b'one', 1),
            (b'two', 2),
            ], item.value)
        self.assertEqual({
            'encoding': 'ziplist',
            }, item.info)
        self.assertIsNone(item.expire)
