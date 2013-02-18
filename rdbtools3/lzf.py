from io import BytesIO
from .util import read_byte


def unpack_lzf(f, clen, explen):
    out = bytearray()
    idx = out_idx = 0
    while idx < clen:
        ctrl = read_byte(f)
        idx += 1
        if ctrl < 32:
            out.extend(f.read(ctrl + 1))
            idx += ctrl + 1
            out_idx = len(out)
        else:
            len_ = ctrl >> 5
            if len_ == 7:
                len_ += read_byte(f)
                idx += 1
            ref = out_idx - ((ctrl & 0x1F) << 8) - read_byte(f) - 1
            idx += 1
            for i in range(ref, ref + len_ + 2):
                out.append(out[i])
            out_idx = len(out)
    if len(out) != explen:
        raise ValueError('Invalid length {}, expected {}'
                         .format(len(out), explen))
    return out
