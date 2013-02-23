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
        self.assertEqual(1, item.dbnum)
        self.assertEqual(b'str2', item.key)
        self.assertEqual(123456789, item.value)
        self.assertEqual({
            'encoding': 'raw',
            }, item.info)
        self.assertIsNone(item.expire)

    def testKeyValue_hset1(self):
        item = self.test_parse()[1]
        self.assertEqual(1, item.dbnum)
        self.assertEqual(b'hset1', item.key)
        self.assertEqual([
            (b'aa', b'10'),
            ], item.value)
        self.assertEqual({
            'encoding': 'zipmap',
            }, item.info)
        self.assertIsNone(item.expire)

    def testKeyValue_set1(self):
        item = self.test_parse()[2]
        self.assertEqual(1, item.dbnum)
        self.assertEqual(b'set1', item.key)
        self.assertEqual([
            1, 2,
            ], item.value)
        self.assertEqual({
            'encoding': 'intset',
            }, item.info)
        self.assertIsNone(item.expire)

    def testKeyValue_long_hash(self):
        item = self.test_parse()[3]
        self.assertEqual(1, item.dbnum)
        self.assertEqual(b'some_long_hash_key_name', item.key)
        self.assertEqual([
            (b'even_more_longer_hash_key_field_name',
             b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
            ], item.value)
        self.assertEqual({
            'encoding': 'zipmap',
            }, item.info)
        self.assertIsNone(item.expire)

    def testKeyValue_zset(self):
        # FIXME: must be int/float
        item = self.test_parse()[4]
        self.assertEqual(1, item.dbnum)
        self.assertEqual(b'zset1', item.key)
        self.assertEqual([
            (b'one', 1),
            (b'two', 2),
            ], item.value)
        self.assertEqual({
            'encoding': 'ziplist',
            }, item.info)
        self.assertIsNone(item.expire)

    def testKeyValue_str(self):
        item = self.test_parse()[5]
        self.assertEqual(1, item.dbnum)
        self.assertEqual(1, item.key)
        self.assertEqual(b'aa', item.value)
        self.assertEqual({
            'encoding': 'raw',
            }, item.info)
        self.assertIsNone(item.expire)

    def testKeyValue_list(self):
        item = self.test_parse()[8]
        self.assertEqual(2, item.dbnum)
        self.assertEqual(b'list1', item.key)
        self.assertEqual([
            1234567890, b'aaaaaaaaaaaaaaaaaaaaaa', 2, 1
            ], item.value)
        self.assertEqual({
            'encoding': 'ziplist',
            }, item.info)
        self.assertIsNone(item.expire)

    def testKeyValue_str_w_expire(self):
        from datetime import datetime

        item = self.test_parse()[7]
        self.assertEqual(2, item.dbnum)
        self.assertEqual(b'str3_exp', item.key)
        self.assertEqual({
            'encoding': 'raw',
            }, item.info)
        self.assertEqual(datetime(2013, 2, 22, 23, 22, 31),
                         item.expire)
