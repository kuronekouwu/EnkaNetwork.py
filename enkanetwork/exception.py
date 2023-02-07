class VaildateUIDError(Exception):
    """ Raised when the UID is not valid. """

class ProfileNotFounded(Exception):
    """ Raised when the profile is not found. """

class BuildNotPublicData(Exception):
    """ Raised when the profile hoyos has public to hidden """

class HTTPException(Exception):
    """ Exception that's raised when an HTTP request operation fails. """

class EnkaValidateFailed(HTTPException):
    """ Exception that's raised for when status code 400 occurs."""

class EnkaPlayerNotFound(Exception):
    """ Raised when the UID is not found. """

class EnkaServerError(HTTPException):
    """ Exception that's raised for when status code 500 occurs."""

class EnkaServerMaintanance(HTTPException):
    """ Exception that's raised when status code 424 occurs. """

class EnkaServerRateLimit(HTTPException):
    """ Exception that's raised when status code 429 occurs."""

class EnkaServerUnknown(HTTPException):
    """ Exception that's raised when status code 503 occurs. """

ERROR_ENKA = {
    400: [VaildateUIDError, "Validate UID {uid} failed."],
    404: [EnkaPlayerNotFound, "Player ID {uid} not found. Please check your UID / Username"],
    429: [EnkaServerRateLimit, "Enka.network has been rate limit this path"],
    424: [EnkaServerMaintanance, "Enka.Network doing maintenance server. Please wait took 5-8 hours or 1 day"],
    500: [EnkaServerError, "Enka.network server has down or Genshin server broken."],
    503: [EnkaServerUnknown, "I screwed up massively"]
}