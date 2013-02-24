from io import BytesIO
from .exceptions import RDBValueError
from .util import read_uint


def unpack_intset(bytes_):
    s = BytesIO(bytes_)
    int_size = read_uint(s, 4)
    len_ = read_uint(s, 4)
    if int_size not in (2, 4, 8):
        raise RDBValueError("Unexpected size encoding {}"
                            .format(hex(int_size)))
    if len(bytes_) - 8 != len_ * int_size:
        raise RDBValueError("Bad content size {} (expected {})"
                            .format(len(bytes_) - 8, len_ * int_size))
    for _ in range(len_):
        yield read_uint(s, int_size)
