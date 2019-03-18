"""API related exceptions."""

from pixivpy.common.exceptions import PixivpyError


class ApiError(PixivpyError):
    """Generic exception which is thrown when an expected error occurs during an API call."""
