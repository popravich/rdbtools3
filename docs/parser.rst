:mod:`rdbtools3` --- Parser API
===============================

.. module:: rdbtools3


.. _parse_rdb_stream:

Parser
------

.. function:: parse_rdb_stream(f, skip_db=lambda dbnum: False, \
                               skip_key_type=lambda dbnum, key_type: False, \
                               skip_key=lambda dbnum, key_type, key: False)

   :param file f: File stream
   :param skip_db: callback to check if db should be skipped.
   :type skip_db: function
   :param skip_key_type: callback to check if key type should be skipped.
   :type skip_key_type: function
   :param skip_key: callback to check if key should be skipped.
   :type skip_key: function

   :returns: generator that yields :class:`RDBItem`'s
   :rtype: generator

   :raise rdbtools3.FileFormatError: if read invalid magic string,
      unsupported RDB version or no "select db" code found.
   :raises rdbtools3.RDBValueError: if parser encounters unexpected data value.

   Parses Redis dump file stream.


.. _RDBItem:

RDBItem
-------

.. class:: RDBItem(dbnum, key_type, key, value, expire, info)

   :param int dbnum: database number
   :param str key_type: key type; possible values `string`, `list`, `set`, \
                        `zset`, `hash`
   :param bytes key: Key name
   :param bytes value: Value itself
   :param expire: TTL if set
   :type expire: int or None
   :param dict info: additional key info

   Named tuple representing Redis DB item.


Exceptions
----------

.. exception:: ParserError

   Base parser exception type.

   Subclass of :exc:`ValueError`.


.. exception:: FileFormatError(msg)

   Raised if magic string is invalid,
   RDB version number invalid or not supported or
   no "select db" control code found.


.. exception:: RDBValueError(msg)

   Raised if unexpected value received.
