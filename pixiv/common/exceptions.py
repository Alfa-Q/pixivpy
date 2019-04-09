"""python-pixiv common exception classes."""

class PixivError(Exception):
    """Generic exception when an error occurs."""


class InvalidStatusCode(PixivError):
    """Indicates that the status code in the response did not match the expected code."""


class RetryError(PixivError):
    """Indicates that the retry decorator was unable to continue due to an unexpected exception."""


class DataNotFound(PixivError):
    """Indicates that data could not be found in the JSON response."""
