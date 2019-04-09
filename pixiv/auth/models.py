"""Pixiv Authorization request models.

Authentication request models for getting raw JSON response.
Each function returns a Request object which defines the OAuth call which is then executed
by the 'request' wrapper, converted into JSON, and returned back to the callee.  It is then
the callee's responsibility for converted the JSON into the Authentication token based on
the keys within the JSON response.
"""

from typing import Dict, Any

from requests import Request

from pixiv.common.decors import request
from pixiv.common.data import AuthToken


@request(expected_code=200)
def get_auth_token(username: str, password: str)  -> Dict[str, Any]:
    """Retrieve the auth bearer token used for making API requests.

    Parameters:
        username: The username or email address of the pixiv account.
        password: Associated account password.

    Returns:
        The raw OAuth JSON response.

    Raises:
        InvalidStatusCode: Expected status code did not match the response status code.

    """
    return Request(
        method='POST',
        url='https://oauth.secure.pixiv.net/auth/token',
        headers={
            'Authority': 'oauth.secure.pixiv.net',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'client_id': 'MOBrBDS8blbauoSck0ZfDbtuzpyT',
            'client_secret': 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj',
            'grant_type': 'password',
            'username': username,
            'password': password,
            'device_token': 'pixiv',
            'get_secure_url': True,
            'include_policy': True
        }
    )


@request(expected_code=200)
def renew_auth_token(auth_token: AuthToken) -> Dict[str, Any]:
    """Renew an auth bearer token for making API requests.

    Parameters:
        auth_token: The auth bearer token to be renewed.

    Returns:
        The raw OAuth JSON response.

    Raises:
        InvalidStatusCode: Expected status code did not match the response status code.

    """
    return Request(
        method='POST',
        url='https://oauth.secure.pixiv.net/auth/token',
        headers={
            'Authority': 'oauth.secure.pixiv.net',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'client_id': 'MOBrBDS8blbauoSck0ZfDbtuzpyT',
            'client_secret': 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj',
            'device_token': 'pixiv',
            'grant_type': 'refresh_token',
            'refresh_token': auth_token.refresh_token,
            'get_secure_url': True,
            'include_policy': True
        }
    )
