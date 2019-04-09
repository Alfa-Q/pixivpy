"""API related exceptions."""

from pixiv.common.exceptions import PixivError


class ApiError(PixivError):
    """Generic exception which is thrown when an expected error occurs during an API call."""
