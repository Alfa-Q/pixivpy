"""
pixivpy.auth.auth
--------------------
Layer above the models module for extracting particular data from the JSON response.
"""

import requests
from typing import Tuple
from . import models
from pixivpy.common.data import AuthToken
from pixivpy.common.exceptions import InvalidJsonResponse


def get_auth_token(email: str, password: str) -> AuthToken:
    """ For initial auth bearer token retrieval.

    Once logged in with username and password, you may continue to use the API calls with it, only
    needing to renew it once the time-to-live expires.

    Parameters:
        username: The username or email address of the pixiv user.
        password: Associated password used to login.

    Returns: An auth bearer token.

    Raises a InvalidJsonResponse if a key within the JSON response which contains the information
    could not be found.
    """
    try:
        json = models.get_auth_token(email, password)
        return AuthToken(
            access_token  = json['response']['access_token'], 
            refresh_token = json['response']['refresh_token'], 
            ttl = json['response']['expires_in']
        )
    except Exception as e:
        raise InvalidJsonResponse(e)


def renew_auth_token(auth_token: AuthToken) -> AuthToken:
    """ Renews an auth bearer token.

    After an auth bearer token expires, the refresh token is used to update the access token within
    the AuthToken object, with the updated time-to-live value.

    Parameters:
        auth_token: The auth bearer token to be renewed.
    
    Returns: A renewed auth bearer token.

    Raises a InvalidJsonResponse if a key within the JSON response which contains the information
    could not be found.
    """
    try:
        json = models.renew_auth_token(auth_token)
        return AuthToken(
            access_token  = json['response']['access_token'], 
            refresh_token = json['response']['refresh_token'], 
            ttl = json['response']['expires_in']
        )
    except Exception as e:
        raise InvalidJsonResponse(e)
