"""
pixivpy.auth.auth
--------------------
Layer above the models module for extracting data from the JSON response.
"""

import requests
from typing import Tuple
from pixivpy.auth import models
from pixivpy.common import validate, exceptions


def get_auth_token(email: str, password: str) -> Tuple[str, int]:
    """ For initial auth bearer token retrieval.

    Once logged in with username and password, you may continue to use the API calls with it, only
    needing to renew it once the time-to-live expires.

    Parameters:
        username: The username or email address of the pixiv user.
        password: Associated password used to login.

    Returns: An auth bearer token and the associated time-to-live (in seconds).
    """
    try:
        json = models.get_auth_token(email, password)
        validate.json(json)
        return json['response']['refresh_token'], json['response']['expires_in']
    except exceptions.InvalidStatusCode as e:
        raise e
    except exceptions.InvalidJSONResponse as e:
        raise e


def renew_auth_token(auth_token: str) -> Tuple[str, int]:
    """ Renews an auth bearer token.

    After an auth bearer token expires, either a new auth bearer token will be returned or the
    same token with the time-to-live refreshed.

    Parameters:
        auth_token: The auth bearer token to be renewed.
    
    Returns: A renewed auth bearer token and the associated time-to-live (in seconds).
    """
    try:
        json = models.renew_auth_token(auth_token)
        validate.json(json)
        return json['response']['refresh_token'], json['response']['expires_in']
    except exceptions.InvalidStatusCode as e:
        raise e
    except exceptions.InvalidJSONResponse as e:
        raise e