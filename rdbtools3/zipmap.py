from io import BytesIO

from .exceptions import RDBValueError
from .util import read_byte, read_uint, skip_bytes


def unpack_zipmap(bytes_):
    s = BytesIO(bytes_)
    zmlen = read_byte(s)
    if zmlen < 254:
        num_entries = zmlen
    else:
        num_entries = None
    while True:
        key_len = read_next_len(s)
        if key_len is None:
            break   # end of zipmap encountered
        key = s.read(key_len)
        val_len = read_next_len(s)
        if val_len is None:
            raise RDBValueError("Unexpected end of zipmap")
        free = read_byte(s)
        value = s.read(val_len)
        skip_bytes(s, free)
        yield key, value
        if num_entries is not None:
            num_entries -= 1
    if num_entries is not None and num_entries != 0:
        raise RDBValueError("Invalid number of entries in zipmap")


def read_next_len(s):
    len_ = read_byte(s)
    if len_ < 254:
        return len_
    elif len_ == 254:
        return read_uint(s, 4)
