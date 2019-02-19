"""
pixivpy.auth.models
--------------------
Authentication request models for getting raw JSON response.
"""

import requests
from pixivpy.common.decors import request


@request(expected_code=200)
def get_auth_token(username: str, password: str):
    """ Retrieves the auth bearer token used for making API requests.

    Parameters:
        username: The username or email address of the pixiv user.
        password: Associated password used to login.

    Returns: The JSON response.
    """
    return requests.Request(
        method = 'POST',
        url = 'https://oauth.secure.pixiv.net/auth/token',
        headers = { 
            'Authority':    'oauth.secure.pixiv.net',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data = {
            'client_id':     'MOBrBDS8blbauoSck0ZfDbtuzpyT',                # TEMPORARILY HARD CODED (NOT MINE)
            'client_secret': 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj',    # TEMPORARILY HARD CODED (NOT MINE)
            'grant_type': 'password',
            'username': username,
            'password': password,
            'device_token': 'pixiv',
            'get_secure_url': True,
            'include_policy': True
        }
    )


