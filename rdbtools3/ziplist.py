from io import BytesIO

from .exceptions import RDBValueError
from .util import read_uint, read_int, read_byte, unpack
from .zipmap import read_next_len


# length masks
STR_6BIT = 0
STR_14BIT = 1
STR_32BIT = 2
INT_16BIT = 12
INT_32BIT = 13
INT_64BIT = 14
INT_24BIT = 240
INT_8BIT = 254
UINT_4BIT = 15


def unpack_ziplist(bytes_):
    s = BytesIO(bytes_)
    read_uint(s, 8)     # zlist size and tail offset; not used when unpacking
    # zlsize = read_uint(s, 4)
    # tail_offset = read_uint(s, 4)
    num_entries = read_uint(s, 2)
    for _ in range(num_entries):
        yield unpack_ziplist_entry(s)
    zend = read_byte(s)
    if zend != 255:
        raise RDBValueError("Invalid ziplist end {}".format(hex(zend)))


def unpack_ziplist_entry(s):
    prev_len = read_next_len(s)     # used for next check only
    if prev_len is None:
        raise RDBValueError("Unexpected end of ziplist")
    entry_type = read_byte(s)
    enc = entry_type >> 6
    if enc == STR_6BIT:
        len_ = entry_type & 0x3F
        return s.read(len_)
    elif enc == STR_14BIT:
        len_ = ((entry_type & 0x3F) << 8) | read_byte(s)
        return s.read(len_)
    elif enc == STR_32BIT:
        len_ = read_uint(s, 4)
        return s.read(len_)
    enc = entry_type >> 4
    if enc == INT_16BIT:
        return read_int(s, 2)
    elif enc == INT_32BIT:
        return read_int(s, 4)
    elif enc == INT_64BIT:
        return read_int(s, 8)
    enc = entry_type
    if enc == INT_24BIT:
        val = unpack('i', b'\x00' + s.read(3))
        return val >> 8
    elif enc == INT_8BIT:
        return read_int(s, 1)
    else:   # UINT_4BIT
        return (entry_type & 0x0F) - 1
