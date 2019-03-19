"""Auth related exceptions."""

from pixivpy.common.exceptions import PixivpyError


class AuthError(PixivpyError):
    """Generic exception which is thrown when an error occurs during an Auth call."""
