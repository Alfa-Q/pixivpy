"""
tests.test_auth
----------------------
Test cases for pixivpy authentication functions.
"""

import pytest                                               # testcase parametrization and exception testing support
from typing import Callable, Dict                           # typing support for function signature
from unittest.mock import patch, MagicMock                  # mocking support
from pixivpy.common.exceptions import InvalidJsonResponse   # expected exceptions
from pixivpy import auth                                    # auth functions that are being tested


@pytest.mark.parametrize("auth_fn, args, json", [
    (auth.get_auth_token,   ['email','password'], {'has_error':True,'errors':{'system':{'message':'Invalid grant_type parameter or parameter missing'}}}),
    (auth.get_auth_token,   ['email','password'], {'response':{'refresh_token': 'valid-token'}}),
    (auth.get_auth_token,   ['email','password'], {'response':{'expires_in': 1000}}),
    (auth.get_auth_token,   ['email','password'], {'response':{'random_key': 'some-value'}}),
    (auth.get_auth_token,   ['email','password'], {'response':'string-not-a-dictionary'}),
    (auth.renew_auth_token, ['some-valid-token'], {'has_error':True,'errors':{'system':{'message':'Invalid grant_type parameter or parameter missing'}}}),
    (auth.renew_auth_token, ['some-valid-token'], {'response':{'refresh_token': 'valid-token'}}),
    (auth.renew_auth_token, ['some-valid-token'], {'response':{'expires_in': 1000}}),
    (auth.renew_auth_token, ['some-valid-token'], {'response':{'random_key': 'some-value'}}),
    (auth.renew_auth_token, ['some-valid-token'], {'response':'string-not-a-dictionary'}),
])
def test_auth_invalid_json(auth_fn: Callable, args, json: Dict):
    """ Test cases for auth API calls when the model returns a JSON response that does not contain
    the keys required to extract the information of interest.
    
    Parameters:
        auth_fn: The authentication function to test.
        args: Some valid function arguments for the authentication function.
        json: Invalid JSON response.
        
    """
    # Setup the mocked auth function with the returned json
    auth_func_patch = patch(f'pixivpy.auth.models.{auth_fn.__name__}')
    auth_func_mock = auth_func_patch.start()
    auth_func_mock.return_value = json

    # Run with the mocked model function with returned invalid json
    with pytest.raises(InvalidJsonResponse) as e:
        auth_fn(*args) 


@pytest.mark.parametrize("auth_fn, args, json", [
    (auth.get_auth_token,   ['email','password'], {'response':{'refresh_token': 'valid-token', 'expires_in': 3600}}),
    (auth.renew_auth_token, ['some-valid-token'], {'response':{'refresh_token': 'valid-token', 'expires_in': 3600}})
])
def test_auth_valid_json(auth_fn: Callable, args, json: Dict):
    """ Test cases for auth API calls when the model returns a JSON response that contains the keys
    required to extract the information of interest.
    
    Parameters:
        auth_fn: The authentication function to test.
        args: Some valid function arguments for the authentication function.
        json: Valid JSON response.
        
    """
    # Setup the mocked auth function with the returned json
    auth_func_patch = patch(f'pixivpy.auth.models.{auth_fn.__name__}')
    auth_func_mock = auth_func_patch.start()
    auth_func_mock.return_value = json

    # Run with the mocked model function with returned json
    token, ttl = auth_fn(*args) 
    assert json['response']['refresh_token'] == token, 'Token did not match expected'
    assert json['response']['expires_in'] == ttl, 'Token expiration time did not match expected'
