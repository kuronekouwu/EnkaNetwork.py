"""
    System exception
"""


class VaildateUIDError(Exception):
    """ Raised when the UID is not valid. """


"""
    EnkaNetwork network exception
"""


class EnkaNetworError(Exception):
    """Base class for EnkaNetwork errors."""


class NetworkError(EnkaNetworError):
    """Base class for exceptions due to networking errors."""


class TimedOut(NetworkError):
    """Raised when a request took too long to finish."""


class EnkaServerError(EnkaNetworError):
    """ Exception that's raised for when status code 500 occurs."""


class EnkaServerMaintanance(EnkaNetworError):
    """ Exception that's raised when status code 424 occurs. """


class EnkaServerRateLimit(EnkaNetworError):
    """ Exception that's raised when status code 429 occurs."""


class EnkaServerUnknown(EnkaNetworError):
    """ Exception that's raised when status code 503 occurs. """


"""
    Github
"""


class HTTPException(Exception):
    """Base class for EnkaNetwork errors."""


"""
    EnkaNetwork response error
"""


class ProfileNotFounded(Exception):
    """ Raised when the profile is not found. """


class BuildNotPublicData(Exception):
    """ Raised when the profile hoyos has public to hidden """


class EnkaValidateFailed(EnkaNetworError):
    """ Exception that's raised for when status code 400 occurs."""


class EnkaPlayerNotFound(Exception):
    """ Raised when the UID is not found. """


ERROR_ENKA = {
    400: [VaildateUIDError, "Validate UID {uid} failed."],
    404: [EnkaPlayerNotFound, "Player ID {uid} not found. Please check your UID / Username"],  # noqa
    429: [EnkaServerRateLimit, "Enka.network has been rate limit this path"],
    424: [EnkaServerMaintanance, "Enka.Network doing maintenance server. Please wait took 5-8 hours or 1 day"],  # noqa
    500: [EnkaServerError, "Enka.network server has down or Genshin server broken."],  # noqa
    503: [EnkaServerUnknown, "I screwed up massively"]
}
