import struct


_SIZE_2_SPEC = {
    1: 'b',
    2: 'h',
    4: 'i',
    8: 'q',
}


def read_byte(f):
    return ord(f.read(1))


def skip_bytes(f, num):
    f.seek(num, 1)


def unpack(spec, bytes_):
    return struct.unpack(spec, bytes_)[0]


def read_int(f, size):
    spec = _SIZE_2_SPEC[size]
    return struct.unpack(spec, f.read(size))[0]


def read_uint(f, size):
    spec = _SIZE_2_SPEC[size]
    return struct.unpack(spec.upper(), f.read(size))[0]
