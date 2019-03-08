"""Common dataclasses used by the API and auth packages."""


class AuthToken:
    """Represent an auth bearer token received from OAuth.

    Attributes:
        access_token: A string representing a token used to access content.
        refresh_token: A string representing a token used to renew the access token.
        ttl: An integer of the time until the access token expires.

    """

    __slots__ = ['access_token', 'refresh_token', 'ttl']
    def __init__(self, access_token: str, refresh_token: str, ttl: int):
        """Init AuthToken with an access token, refresh token and time to live value."""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.ttl = ttl
