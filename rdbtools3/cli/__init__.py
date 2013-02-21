import argparse
import sys
from collections import defaultdict

from rdbtools3.parser import read_signature, read_version, parse_rdb_stream
from rdbtools3.exceptions import FileFormatError


def get_options():
    ap = argparse.ArgumentParser(
            prog='python3 -m rdbtools3.cli',
            description="Redis RDB parser tool")
    ap.add_argument('dumpfile', metavar="FILE",
            help="path to Redis dump.rdb file",
            type=argparse.FileType('rb'))
    # attach common options
    # db filtering
    gr = ap.add_mutually_exclusive_group()
    gr.add_argument('-d', '--include-db', metavar="N",
            help="include DB number",
            dest="include_dbs", default=None,
            action="append", type=int)
    gr.add_argument('-D', '--exclude-db', metavar="N",
            help="exclude DB number",
            dest="exlude_dbs", default=None,
            action="append", type=int)
    # type filtering
    types = ['str', 'list', 'set', 'hash', 'zset']
    gr = ap.add_mutually_exclusive_group()
    gr.add_argument('-k', '--include-type', metavar="TYPE",
            help="include key type in result"
                 " (choices are: %(choices)s)",
            dest="include_types", default=None,
            action="append", choices=types)
    gr.add_argument('-K', '--exclude-type', metavar="TYPE",
            help="exclude key type in result"
                 " (choices are: %(choices)s)",
            dest="exclude_types", default=None,
            action="append", choices=types)
    # keys filtering
    gr = ap.add_mutually_exclusive_group()
    gr.add_argument('-e', '--include-regex', metavar="REGEX",
            help="include keys matched by regex",
            dest="include_key", default=None)
    gr.add_argument('-E', '--exclude-regex', metavar="REGEX",
            help="exclude keys matched by regex",
            dest="exclude_key", default=None)

    ap.add_argument('-i', '--info',
            help="Show dump info and exit",
            dest="show_info_only", default=False, action="store_true")
    return ap


def print_info(options):
    f = options.dumpfile
    try:
        read_signature(f)
        version = read_version(f)
    except FileFormatError:
        sys.stderr.write("Invalid file format\n")
        sys.exit(1)
    else:
        sys.stdout.write('version: {}\n'.format(version))
    f.seek(0)

    dbs = {}

    def skip_db(dbnum):
        dbs.setdefault(dbnum, defaultdict(int))
        return False

    def skip_key_type(dbnum, key_type):
        dbs[dbnum][key_type] += 1
        return True

    for item in parse_rdb_stream(f, skip_db=skip_db,
                                    skip_key_type=skip_key_type):
        pass

    headline = 'db: {{:>{0}}}; keys: {{}}\n'.format(len(str(max(dbs))))
    for db, keys in sorted(dbs.items()):
        total = sum(keys.values())
        sys.stdout.write(headline.format(db, total))
        for key, count in sorted(keys.items()):
            sys.stdout.write('  {:<10}: {}\n'.format(key, count))


def print_keys(options):
    for item in parse_rdb_stream(options.dumpfile):
        sys.stdout.write('db: {item.dbnum}; type: {item.key_type};'
                         ' key: {item.key}'.format(item=item))
        sys.stdout.write('\n')


def main():
    ap = get_options()
    options = ap.parse_args()

    if options.show_info_only:
        print_info(options)
    else:
        print_keys(options)
