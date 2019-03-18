"""pixivpy common exception classes."""


class PixivpyError(Exception):
    """Generic exception when an error occurs."""


class InvalidStatusCode(PixivpyError):
    """Indicates that the status code in the response did not match the expected code."""


class InvalidJsonResponse(PixivpyError):
    """Indicates that the JSON response received by the request call was invalid."""


class RetryError(PixivpyError):
    """Indicates that the retry decorator was unable to continue due to an unexpected exception."""


class DataNotFound(PixivpyError):
    """Indicates that data could not be found in the JSON response."""
