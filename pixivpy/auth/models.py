"""
pixivpy.auth.models
--------------------
Authentication request models for getting raw JSON response.
"""

from requests import Request
from pixivpy.common.decors import request, validate
from pixivpy.common.exceptions import InvalidJsonResponse


@validate([
    (lambda json: 'has_error' not in json.keys(), InvalidJsonResponse),
    (lambda json: 'response'  in json.keys(),     InvalidJsonResponse),
    (lambda json: dict == type(json['response']), InvalidJsonResponse),
    (lambda json: 'refresh_token' in json['response'].keys(), InvalidJsonResponse),
    (lambda json: 'expires_in'    in json['response'].keys(), InvalidJsonResponse)
])
@request(expected_code=200)
def get_auth_token(username: str, password: str):
    """ Retrieves the auth bearer token used for making API requests.

    Parameters:
        username: The username or email address of the pixiv user.
        password: Associated password used to login.

    Returns: The JSON response.
    """
    return Request(
        method = 'POST',
        url = 'https://oauth.secure.pixiv.net/auth/token',
        headers = { 
            'Authority':    'oauth.secure.pixiv.net',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data = {
            'client_id':     'MOBrBDS8blbauoSck0ZfDbtuzpyT',                
            'client_secret': 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj',
            'grant_type': 'password',
            'username': username,
            'password': password,
            'device_token': 'pixiv',
            'get_secure_url': True,
            'include_policy': True
        }
    )


@validate([
    (lambda json: 'has_error' not in json.keys(),    InvalidJsonResponse),
    (lambda json: 'response'  in json.keys(), InvalidJsonResponse),
    (lambda json: dict == type(json['response']), InvalidJsonResponse),
    (lambda json: 'refresh_token' in json['response'].keys(), InvalidJsonResponse),
    (lambda json: 'expires_in'    in json['response'].keys(), InvalidJsonResponse)
])
@request(expected_code=200)
def renew_auth_token(auth_token: str):
    """ Renews an auth bearer token for making API requests.

    Parameters:
        auth_token: The auth bearer token to be renewed.
    
    Returns: The JSON response.
    """
    return Request(
        method = 'POST',
        url = 'https://oauth.secure.pixiv.net/auth/token',
        headers = { 
            'Authority':    'oauth.secure.pixiv.net',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data = {
            'client_id':     'MOBrBDS8blbauoSck0ZfDbtuzpyT',               
            'client_secret': 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj', 
            'device_token':  'pixiv',
            'grant_type': 'refresh_token',
            'refresh_token': auth_token,
            'get_secure_url': True,
            'include_policy': True
        }
    )