from rdbtools3.parser import parse_rdb_stream


class RdbParser:

    def __init__(self, callback, filters=None):
        self._callback = callback
        self._filters = filters

    def parse(self, dumpfile):
        with open(dumpfile, 'rb') as f:
            for rdbkey in parse_rdb_stream(f):
                pass
