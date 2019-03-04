"""
tests.test_auth
----------------------
Test cases for pixivpy authentication functions.
"""

import os, pytest, json                                     # testcase parametrization and exception testing support
from typing import Callable, Dict                           # typing support for function signature
from unittest.mock import patch, MagicMock                  # mocking support
from pixivpy.common.exceptions import InvalidJsonResponse   # expected exceptions
from pixivpy.common.data import AuthToken                   # auth token used to renew access token
from pixivpy import auth                                    # auth functions that are being tested


""" -------------------------------------- Test Mapping --------------------------------------- """
#   To setup testcases for authentication, it must contain the following fields:
#       fn:             The API generator function to test.
#       invalid_json:   Text file containing bad responses that should produce an exception, each testcase separated by newline in JSON format.
#       valid_json:     Text file containing good responses, each testcase separated by newline in JSON format.
#       valid_args:     List of valid function arguments. Ensures that only the extraction is being tested.
testcase_dir = os.path.dirname(__file__) + '/auth_testcases'
auth_test_info = {
    'get_auth_token': {
        'fn': auth.get_auth_token,
        'invalid_json': f'{testcase_dir}/get_auth_token_invalid.json',
        'valid_json':   f'{testcase_dir}/get_auth_token_valid.json',
        'valid_args':    ['email','password'],
    },
    'renew_auth_token': {
        'fn': auth.renew_auth_token,
        'invalid_json': f'{testcase_dir}/renew_auth_token_invalid.json',
        'valid_json':   f'{testcase_dir}/renew_auth_token_valid.json',
        'valid_args':    [AuthToken('access','refresh',3600)]
    }
}


""" --------------------------------------- Test Cases ---------------------------------------- """
@pytest.mark.parametrize("auth_fn, args, invalid_json",
    # Use list comprehension to load the testcases for each auth call from their associated file.
    [
    #   auth fn             list of valid api fn args   invalid json to test 
        (test_info['fn'],   test_info['valid_args'],    json.loads(json_testcase))
        for test_info in auth_test_info.values()
        for json_testcase in open(test_info['invalid_json'], encoding='utf-8').readlines()
    ]
)
def test_auth_invalid_json(auth_fn: Callable, args, invalid_json: Dict):
    """ Test cases for auth API calls when the model returns a JSON response that does not contain
    the keys required to extract the information of interest.
    
    Parameters:
        auth_fn: The authentication function to test.
        args: Some valid function arguments for the authentication function.
        invalid_json: Invalid JSON response.
        
    """
    # Setup the mocked auth function with the returned json
    auth_func_patch = patch(f'pixivpy.auth.models.{auth_fn.__name__}')
    auth_func_mock = auth_func_patch.start()
    auth_func_mock.return_value = invalid_json

    # Run with the mocked model function with returned invalid json
    with pytest.raises(InvalidJsonResponse) as e:
        auth_fn(*args) 


@pytest.mark.parametrize("auth_fn, args, valid_json",
    # Use list comprehension to load the testcases for each auth call from their associated file.
    [
    #   auth fn             list of valid api fn args   valid json to test 
        (test_info['fn'],   test_info['valid_args'],    json.loads(json_testcase))
        for test_info in auth_test_info.values()
        for json_testcase in open(test_info['valid_json'], encoding='utf-8').readlines()
    ]
)
def test_auth_valid_json(auth_fn: Callable, args, valid_json: Dict):
    """ Test cases for auth API calls when the model returns a JSON response that contains the keys
    required to extract the information of interest.
    
    Parameters:
        auth_fn: The authentication function to test.
        args: Some valid function arguments for the authentication function.
        valid_json: Valid JSON response.
        
    """
    # Setup the mocked auth function with the returned json
    auth_func_patch = patch(f'pixivpy.auth.models.{auth_fn.__name__}')
    auth_func_mock = auth_func_patch.start()
    auth_func_mock.return_value = valid_json

    # Run with the mocked model function with returned json
    auth_token = auth_fn(*args) 
    assert valid_json['response']['access_token']  == auth_token.access_token,  'Access token did not match'
    assert valid_json['response']['refresh_token'] == auth_token.refresh_token, 'Refresh token did not match expected'
    assert valid_json['response']['expires_in'] == auth_token.ttl, 'Token expiration time did not match expected'
