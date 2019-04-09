"""Pixiv Authentication functions for retrieving and renewing OAuth tokens to make API calls.

Layer above the models module for extracting particular data from the JSON response.

"""

import time

from pixiv.auth import models
from pixiv.auth.exceptions import AuthError
from pixiv.common.exceptions import PixivError
from pixiv.common.data import AuthToken
from pixiv.common import validate


def _validate_auth_response(res_json):
    """Validate raw JSON response of auth function.

    Args:
        res_json: The raw response JSON.

    Raises:
        DataNotFound: Validation failed due to missing data or unexpected data.

    """

    # Ensure sub-dictionary exists
    validate.response_contains_key(res_json, 'response')
    validate.response_key_mapping(res_json, 'response', dict)
    # Ensure the sub-dictionary contains the required keys
    validate.response_contains_key(res_json['response'], 'access_token')
    validate.response_contains_key(res_json['response'], 'refresh_token')
    validate.response_contains_key(res_json['response'], 'expires_in')
    # Ensure the type of those keys is correct
    validate.response_key_mapping(res_json['response'], 'access_token', str)
    validate.response_key_mapping(res_json['response'], 'refresh_token', str)
    validate.response_key_mapping(res_json['response'], 'expires_in', int)


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
        _validate_auth_response(json)
        return AuthToken(
            access_token=json['response']['access_token'],      # pylint: disable=unsubscriptable-object
            refresh_token=json['response']['refresh_token'],    # pylint: disable=unsubscriptable-object
            ttl=json['response']['expires_in']                  # pylint: disable=unsubscriptable-object
        )
    except PixivError as ex:
        raise AuthError(
            "An error occured while trying to make the Auth call 'get_auth_token.'"
        ) from ex


def renew_auth_token(auth_token: AuthToken) -> AuthToken:
    """Renews an auth bearer token if it has expired.

    After an auth bearer token expires, the refresh token is used to update the access token within
    the AuthToken object. A request to update the token is only made if the 'expires_at' value
    is less than the current time. This function is never meant to be called directly, the API
    functions will make a call to this function before each request.

    This function does not account for the potential case where the 'expires_at' value is greater
    than the current time but doesn't have enough time to make a request, before the token expires.

    Args:
        auth_token: The auth bearer token to be updated.

    Returns:
        A valid auth bearer token.

    Raises:
        InvalidJsonResponse: A key within the JSON response could not be found.

    """
    try:
        # Check if the token has expired.
        if time.time() >= auth_token.expires_at:
            json = models.renew_auth_token(auth_token)
            _validate_auth_response(json)
            return AuthToken(
                access_token=json['response']['access_token'],      # pylint: disable=unsubscriptable-object
                refresh_token=json['response']['refresh_token'],    # pylint: disable=unsubscriptable-object
                ttl=json['response']['expires_in']                  # pylint: disable=unsubscriptable-object
            )
        return auth_token
    except PixivError as ex:
        raise AuthError(
            "An error occured while trying to make the Auth call 'renew_auth_token.'"
        ) from ex
