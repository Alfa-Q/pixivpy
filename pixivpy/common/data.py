"""Common dataclasses used by the API and auth packages."""

import time
from typing import Optional


class AuthToken:
    """Represent an auth bearer token received from OAuth.

    Attributes:
        access_token: A string representing a token used to access content.
        refresh_token: A string representing a token used to renew the access token.
        ttl: An integer of the time until the access token expires.
        expires_at: An integer of the epoch time when the token expires.

    """

    __slots__ = ['access_token', 'refresh_token', 'ttl', 'expires_at']
    def __init__(self, access_token: str, refresh_token: str, ttl: int,
                 expires_at: Optional[int] = None):
        """Init AuthToken with an access token, refresh token and expiration info."""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.ttl = ttl
        self.expires_at = (expires_at, int(time.time()) + ttl)[expires_at is None]
