class VaildateUIDError(Exception):
    """ Raised when the UID is not valid. """
    pass

class UIDNotFounded(Exception):
    """ Raised when the UID is not found. """
    pass

class HTTPException(Exception):
    """ Exception that's raised when an HTTP request operation fails. """
    pass

class Forbidden(HTTPException):
    """ Exception that's raised for when status code 403 occurs."""
    pass

class EnkaServerError(HTTPException):
    """ Exception that's raised for when status code 500 occurs."""
    pass
