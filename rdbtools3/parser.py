import struct
import datetime
from collections import namedtuple

from rdbtools3 import consts as C
from rdbtools3.exceptions import FileFormatError


RDBKey = namedtuple('RDBKey', 'dbnum key_type key value expire info')


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

    _skip_db = False

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
            data_type = read_byte(f)
        except TypeError:
            # assume thats the end of a file
            # TODO: find a better way to handle this;
            break

        if data_type == C.SELECTDB:
            dbnum = read_length(f)
            _skip_db = skip_db(dbnum)
            continue
        if data_type == C.RDB_EOF:
            # TODO: maybe check crc
            break

        if dbnum is None:
            raise FileFormatError('Select DB code expected but none found')

        expire = parse_expire(data_type, f)
        if expire is not None:
            data_type = read_byte(f)
        key_type, key = parse_key(data_type, f)

        if _skip_db:
            pass    # TODO: skip object

        # TODO: read object
        #yield RDBKey(dbnum, key_type, key, value, expire, {})


def parse_expire(data_type, f):
    if data_type == C.EXPIRE_SEC:
        exp = unpack('I', f.read(4))
        return datetime.datetime.utcfromtimestamp(exp)
    elif data_type == C.EXPIRE_MSEC:
        exp = unpack('Q', f.read(8))
        return datetime.datetime.utcfromtimestamp(exp / 1000)


def parse_key(data_type, f):
    if data_type not in C.TYPE_NAMES:
        raise NotImplementedError('Got unknown data type {}'
                                  .format(hex(data_type)))
    key_type = C.TYPE_NAMES[data_type]
    key = read_string(f)
    return key_type, key


### few util functions ###


def read_byte(f):
    return ord(f.read(1))


def skip_bytes(f, num):
    f.seek(num, 1)


def unpack(spec, bytes_):
    return struct.unpack(spec, bytes_)[0]


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


def read_string(f):
    pass
