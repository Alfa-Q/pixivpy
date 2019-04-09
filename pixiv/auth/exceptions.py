"""Auth related exceptions."""

from pixiv.common.exceptions import PixivError


class AuthError(PixivError):
    """Generic exception which is thrown when an error occurs during an Auth call."""
