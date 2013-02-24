

class ParserError(ValueError):
    " Base RDB parser error type "


class FileFormatError(ParserError):
    " Raised if magic string is invalid "


class RDBValueError(ParserError):
    " Raised when unexpected value received "
