"""Pixiv Authentication functions for retrieving and renewing OAuth tokens to make API calls.

Layer above the models module for extracting particular data from the JSON response.

An unfortunate side-effect of the request decorator is that Python get confused on which
type the wrapped function returns. As a result, this causes Pylint to incorrectly think
that the json returned is not a dictionary object (hence the pylint disable comments).
Plans to fix this in the future.

#TODO: Add AuthError on InvalidStatusCode exception and parse 'error' key
#TODO: Parse more specific Exceptions, KeyError
"""

from pixivpy.auth import models
from pixivpy.common.data import AuthToken
from pixivpy.common.exceptions import InvalidJsonResponse


def get_auth_token(email: str, password: str) -> AuthToken:
    """For initial auth bearer token retrieval.

    Once logged in with username and password, you may continue to use the API calls with it, only
    needing to renew it once the time-to-live expires.

    Args:
        username: The username or email address of the pixiv user.
        password: Associated password used to login.

    Returns:
        An auth bearer token.

    Raises:
        InvalidJsonResponse: A key within the JSON response could not be found.
        AuthError: The request was unsuccessful (invalid status code).

    """
    try:
        json = models.get_auth_token(email, password)
        return AuthToken(
            access_token=json['response']['access_token'],      # pylint: disable=unsubscriptable-object
            refresh_token=json['response']['refresh_token'],    # pylint: disable=unsubscriptable-object
            ttl=json['response']['expires_in']                  # pylint: disable=unsubscriptable-object
        )
    except Exception as ex:
        raise InvalidJsonResponse(ex)


def renew_auth_token(auth_token: AuthToken) -> AuthToken:
    """Renews an auth bearer token.

    After an auth bearer token expires, the refresh token is used to update the access token within
    the AuthToken object, with the updated time-to-live value.

    Args:
        auth_token: The auth bearer token to be renewed.

    Returns:
        A renewed auth bearer token.

    Raises:
        InvalidJsonResponse: A key within the JSON response could not be found.

    """
    try:
        json = models.renew_auth_token(auth_token)
        return AuthToken(
            access_token=json['response']['access_token'],      # pylint: disable=unsubscriptable-object
            refresh_token=json['response']['refresh_token'],    # pylint: disable=unsubscriptable-object
            ttl=json['response']['expires_in']                  # pylint: disable=unsubscriptable-object
        )
    except Exception as ex:
        raise InvalidJsonResponse(ex)
