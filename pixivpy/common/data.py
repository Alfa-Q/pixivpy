"""
pixivpy.common.data
-------------------
Common dataclasses used by the API and authentication.
"""


class AuthToken:
    __slots__ = ['access_token','refresh_token','ttl']
    def __init__(self, access_token: str, refresh_token: str, ttl: int):
        """ 
        Represents a token received from OAuth.
        
        Parameters:
            access_token: The auth bearer token used to access content.
            refresh_token: The token used for renewing the access token.
            ttl: The amount of time until the access token expires.
    
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.ttl = ttl

    def __repr__(self):
        return "AuthToken(access_token={access_token}, refresh_token={refresh_token}, ttl={ttl})".format(
            access_token = self.access_token,
            refresh_token = self.refresh_token,
            ttl = self.ttl
        )