

class ParserError(Exception):
    " Base RDB parser error type "


class FileFormatError(ParserError):
    " Raised if magic string is invalid "
