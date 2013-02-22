import io
import os.path


_DUMPS = os.path.join(os.path.dirname(__file__), 'dumps')


def load_dump(fname):
    with open(os.path.join(_DUMPS, fname), 'rb') as f:
        return io.BytesIO(f.read())
