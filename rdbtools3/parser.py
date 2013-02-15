import struct
import datetime
from collections import namedtuple

from rdbtools3 import consts as C
from rdbtools3.exceptions import FileFormatError


RDBItem = namedtuple('RDBItem', 'dbnum key_type key value expire info')


def parse_rdb_stream(f, skip_db=lambda dbnum: False,
                        skip_key_type=lambda dbnum, key_type: False,
                        skip_key=lambda dbnum, key_type, key: False,
                        skip_expired=False):
    """
    Parses RDB file
    """
    dbnum = None
    key_type = None
    key = None
    value = None

    _skip_db = _skip_key_type = _skip_key = False

    # read signature and version
    bsign = f.read(5)
    if bsign != C.MAGIC_STRING:
        raise FileFormatError('Invalid file format')
    bversion = f.read(4)
    try:
        version = int(bversion)
    except ValueError:
        raise FileFormatError('Invalid RDB version number')
    if version < 1:
        raise FileFormatError('Invalid RDB version number')
    elif version > 6:
        raise NotImplementedError("Version {} is not supported"
                                  .format(version))
    while True:
        try:
            ctl_code = read_byte(f)
        except TypeError:
            # assume thats the end of a file
            # TODO: find a better way to handle this;
            break

        if ctl_code == C.SELECTDB:
            dbnum = read_length(f)
            _skip_db = skip_db(dbnum)
            continue
        if ctl_code == C.RDB_EOF:
            # TODO: maybe check crc
            break

        if dbnum is None:
            raise FileFormatError('Select DB code expected but none found')

        expire, ctl_code = read_expire(ctl_code, f)

        if ctl_code not in C.VALUE_ENC_TYPES:
            raise NotImplementedError("Got unknown data type {}"
                                      .format(hex(ctl_code)))
        key_type = C.TYPE_NAMES[ctl_code]

        if _skip_db or skip_key_type(dbnum, key_type):
            read_skip_key(f)
            read_skip_value(ctl_code, f)
            continue

        key = read_key(f)
        if skip_key(dbnum, key_type, key):
            read_skip_value(ctl_code, f)
            continue

        value = read_value(ctl_code, f)
        yield RDBItem(dbnum, key_type, key, value, expire, {})


def read_expire(ctl_code, f):
    if ctl_code == C.EXPIRE_SEC:
        exp = unpack('I', f.read(4))
        return datetime.datetime.utcfromtimestamp(exp), read_byte(f)
    elif ctl_code == C.EXPIRE_MSEC:
        exp = unpack('Q', f.read(8))
        return datetime.datetime.utcfromtimestamp(exp / 1000), read_byte(f)
    return None, ctl_code


def read_skip_expire(ctl_code, f):
    if ctl_code == C.EXPIRE_SEC:
        skip_bytes(f, 4)
        return None, read_byte(f)
    elif ctl_code == C.EXPIRE_MSEC:
        skip_bytes(f, 8)
        return None, read_byte(f)
    return None, ctl_code


def read_string(f):
    str_enc_type, len_ = read_string_length(f)
    if str_enc_type == C.STR_RAW:
        return f.read(len_)
    elif str_enc_type == C.STR_INTEGER:
        return read_int(f, len_)
    elif str_enc_type == C.STR_COMPRESSED:
        clen, explen = len_
        return f.read(clen)
    raise NotImplementedError('Got unknown string encoding type {}'
                              .format(hex(str_enc_type)))


def read_skip_string(f):
    str_enc_type, len_ = read_string_length(f)
    if str_enc_type == C.STR_COMPRESSED:
        len_, explen = len_
    skip_bytes(f, len_)
    #if str_enc_type == C.STR_RAW:
    #    skip_bytes(f, len_)
    #elif str_enc_type == C.STR_INTEGER:
    #    skip_bytes(f, len_)
    #elif str_enc_type == C.STR_COMPRESSED:
    #    clen, explen = len_
    #    skip_bytes(f, clen)

read_key = read_string
read_skip_key = read_skip_string


def read_value(ctl_code, f):
    if ctl_code == C.VALUE_ENC_STRING:
        return read_string(f)
    elif ctl_code == C.VALUE_ENC_LIST:
        lsize = read_length(f)
        return [read_string(f)
                for _ in range(lsize)]
    elif ctl_code == C.VALUE_ENC_SET:
        ssize = read_length(f)
        # TODO: set values are ordered
        return {read_string(f)
                for _ in range(ssize)}
    elif ctl_code == C.VALUE_ENC_SORTET_SET:
        zs_size = read_length(f)
        ret = []
        for _ in range(zs_size):
            val = read_string(f)
            len_ = read_byte(f)
            score = f.read(len_)
            ret.append((val, score))
        return ret
    elif ctl_code == C.VALUE_ENC_HASH:
        hsize = read_length(f)
        ret = []
        for _ in range(hsize):
            field = read_string(f)
            value = read_string(f)
            ret.append((field, value))
        return ret
    elif ctl_code == C.VALUE_ENC_ZIPMAP:
        return read_string(f)
    elif ctl_code == C.VALUE_ENC_ZIPLIST:
        return read_string(f)
    elif ctl_code == C.VALUE_ENC_INTSET:
        return read_string(f)
    elif ctl_code == C.VALUE_ENC_ZSET_IN_ZIPLIST:
        return read_string(f)
    elif ctl_code == C.VALUE_ENC_HASH_IN_ZIPLIST:
        return read_string(f)
    raise NotImplementedError("Got unknown data type {}".format(hex(ctl_code)))


def read_skip_value(ctl_code, f):
    if ctl_code == C.VALUE_ENC_STRING:
        read_skip_string(f)
    elif ctl_code == C.VALUE_ENC_LIST or ctl_code == C.VALUE_ENC_SET:
        lsize = read_length(f)
        for _ in range(lsize):
            read_skip_string(f)
    elif ctl_code == C.VALUE_ENC_SORTET_SET:
        zs_size = read_length(f)
        for _ in range(zs_size):
            read_skip_string(f)
            skip_bytes(f, read_byte(f))
    elif ctl_code == C.VALUE_ENC_HASH:
        hsize = read_length(f)
        for _ in range(hsize):
            read_skip_string(f)
            read_skip_string(f)
    elif ctl_code == C.VALUE_ENC_ZIPMAP:
        read_skip_string(f)
    elif ctl_code == C.VALUE_ENC_ZIPLIST:
        read_skip_string(f)
    elif ctl_code == C.VALUE_ENC_INTSET:
        read_skip_string(f)
    elif ctl_code == C.VALUE_ENC_ZSET_IN_ZIPLIST:
        read_skip_string(f)
    elif ctl_code == C.VALUE_ENC_HASH_IN_ZIPLIST:
        read_skip_string(f)


### few util functions ###


def read_byte(f):
    return ord(f.read(1))


def skip_bytes(f, num):
    f.seek(num, 1)


def unpack(spec, bytes_):
    return struct.unpack(spec, bytes_)[0]


def read_int(f, size, _specs={1: 'b', 2: 'h', 4: 'i'}):
    spec = _specs[size]
    return unpack(spec, f.read(size))


def read_length(f):
    byte = read_byte(f)
    enc_type = byte >> 6
    val = byte & 0x3F
    if enc_type == C.LEN_ENC_6BIT:
        return val
    elif enc_type == C.LEN_ENC_14BIT:
        next_val = read_byte(f)
        return (val << 8) | next_val
    elif enc_type == C.LEN_ENC_32BIT:
        val = unpack('>I', f.read(4))
        return val
    # else: LEN_ENC_SPECIAL
    elif val == C.LEN_ENC_SPECIAL_8BIT:
        return read_byte(f)
    elif val == C.LEN_ENC_SPECIAL_16BIT:
        return unpack('H', f.read(2))
    elif val == C.LEN_ENC_SPECIAL_32BIT:
        return unpack('I', f.read(4))
    raise NotImplementedError('Got unknown length encoding type {}'
                              .format(hex(byte)))


def read_string_length(f):
    """
    parses string length and returns
    string encoding type and string length;

    Note: if string is compressed string length is returned as
        a tuple consisting of compressed length and
        expected uncompressed length
    """
    byte = read_byte(f)
    enc_type = byte >> 6
    val = byte & 0x3F
    # no encoding; raw string follows
    if enc_type == C.LEN_ENC_6BIT:
        return C.STR_RAW, val
    elif enc_type == C.LEN_ENC_14BIT:
        next_val = read_byte(f)
        return C.STR_RAW, ((val << 8) | next_val)
    elif enc_type == C.LEN_ENC_32BIT:
        val = unpack('>I', f.read(4))
        return C.STR_RAW, val
    # string encoded integer;
    elif val == C.LEN_ENC_SPECIAL_8BIT:
        return C.STR_INTEGER, 1
    elif val == C.LEN_ENC_SPECIAL_16BIT:
        return C.STR_INTEGER, 2
    elif val == C.LEN_ENC_SPECIAL_32BIT:
        return C.STR_INTEGER, 4
    elif val == C.LEN_ENC_SPECIAL_LZF:
        clen = read_length(f)
        explen = read_length(f)
        return C.STR_COMPRESSED, (clen, explen)
    raise NotImplementedError('Got unknown length encoding type {}'
                              .format(hex(byte)))
