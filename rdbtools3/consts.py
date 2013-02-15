MAGIC_STRING = b'REDIS'


SELECTDB = 254  # FE -- next db selector
RDB_EOF = 255   # FF -- EOF

EXPIRE_SEC = 253    # FD -- expire timestamp in seconds
EXPIRE_MSEC = 252   # FC -- expire timestamp in milliseconds


### Length encodings ###
LEN_ENC_6BIT = 0
LEN_ENC_14BIT = 1
LEN_ENC_32BIT = 2
LEN_ENC_SPECIAL = 3
LEN_ENC_SPECIAL_8BIT = 0
LEN_ENC_SPECIAL_16BIT = 1
LEN_ENC_SPECIAL_32BIT = 2


### Value Type encodings ###
VALUE_ENC_STRING = 0
VALUE_ENC_LIST = 1
VALUE_ENC_SET = 2
VALUE_ENC_SORTET_SET = 3
VALUE_ENC_HASH = 4

VALUE_ENC_ZIPMAP = 9
VALUE_ENC_ZIPLIST = 10
VALUE_ENC_INTSET = 11
VALUE_ENC_ZSET_IN_ZIPLIST = 12
VALUE_ENC_HASH_IN_ZIPLIST = 13


### Value types to readable names mapping ###
TYPE_NAMES = {
    VALUE_ENC_STRING: 'string',
    VALUE_ENC_LIST: 'list',
    VALUE_ENC_SET: 'set',
    VALUE_ENC_SORTET_SET: 'zset',
    VALUE_ENC_HASH: 'hash',
    VALUE_ENC_ZIPMAP: 'hash',
    VALUE_ENC_ZIPLIST: 'list',
    VALUE_ENC_INTSET: 'set',
    VALUE_ENC_ZSET_IN_ZIPLIST: 'zset',
    VALUE_ENC_HASH_IN_ZIPLIST: 'hash',
}
