class VaildateUIDError(Exception):
    """ Raised when the UID is not valid. """

class UIDNotFounded(Exception):
    """ Raised when the UID is not found. """

class HTTPException(Exception):
    """ Exception that's raised when an HTTP request operation fails. """

class Forbidden(HTTPException):
    """ Exception that's raised for when status code 403 occurs."""

class EnkaServerError(HTTPException):
    """ Exception that's raised for when status code 500 occurs."""

class EnkaServerMaintanance(HTTPException):
    """ Exception that's raised when status code 424 occurs. """