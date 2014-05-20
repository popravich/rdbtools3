Redis dump.rdb parser tool implemented in Python 3
==================================================

.. image:: https://travis-ci.org/popravich/rdbtools3.png
   :target: https://travis-ci.org/popravich/rdbtools3
   :alt: Build status

Inspired by `redis-rdb-tools <https://github.com/sripathikrishnan/redis-rdb-tools>`_

Documentation
^^^^^^^^^^^^^

See http://rdbtools3.readthedocs.org/

Usage example
^^^^^^^^^^^^^

.. code:: python

    from rdbtools3 import parse_rdb_stream

    with open('/path/to/redis/dump.rdb', 'rb') as f:
        for item in parse_rdb_stream(f):
            print(item.key, item.value)
