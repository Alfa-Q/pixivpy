"""pixivpy common exception classes."""

class InvalidStatusCode(Exception):
    """Indicates that the status code in the response did not match the expected code."""


class InvalidJsonResponse(Exception):
    """Indicates that the JSON response received by the request call was invalid."""
