"""
pixivpy.common.exceptions
-------------------------
pixivpy common exception classes.
"""

class InvalidStatusCode(Exception):
    """
    Exception which indicates that the status code returned by the request call did not match the
    expected value.
    """
    pass


class InvalidJsonResponse(Exception):
    """
    Exception which indicates that the JSON response received by the request call was invalid.
    """
    pass