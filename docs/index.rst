.. rdbtools3 documentation master file, created by
   sphinx-quickstart on Tue May 20 20:51:10 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rdbtools3
=========

Redis dumps parser and cli tool.


Installation
------------

The easiest way to install rdbtools3 is by using the package on PyPi::

   pip install rdbtools3


Source code
-----------


The project is hosted on `GitHub`_ and can be installed running following
commands::

   git clone https://github.com/popravich/rdbtools3.git
   cd rdbtools3
   python3 setup.py install

   # optionally, run tests with
   make test

Fill free to `fork`_ it and/or to report any found issues/ideas on `bug tracker`_

.. _GitHub: https://github.com/popravich/rdbtools3
.. _fork: GitHub_
.. _bug tracker: https://github.com/popravich/rdbtools3/issues


Getting started
---------------

The simpliest way to start using tool::

   from rdbtools3 import parse_rdb_stream

   with open('/path/to/redis/dump.rdb', 'rb') as f:
      for item in parse_rdb_stream(f):
         print(item.key, item.value)

And on command line::

   python3 -m rdbtools3 /path/to/redis/dump.rdb


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::

   parser
   cli
