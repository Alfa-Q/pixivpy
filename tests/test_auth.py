"""Test cases for pixivpy authentication functions.

Testcases check that the auth functions are able to extract data properly and raise the correct
exceptions in cases where the JSON is invalid. The testcases run under the assumption that the
status code of the response is valid and that the arguments provided to the function are valid.

TODO: Create tests with StatusCodeError

Each new Auth function is registered in the _AUTH_TEST_INFO dictionary as a sub-dictionary with
the function name mapped to a dictionary containing the following fields:
    fn: The authentication function to test.
    valid_args: Valid arguments for the auth function.
    valid_json: Filepath to a file containing good responses, each testcase separated by newline
        in JSON format.
    invalid_json: Filepath to a file containing bad responses, each testcase separated by newline
        in JSON format.

The @pytest.mark.parametrize wrapper on each testcase function builds the testcases for each auth
function using list comprehension. It loads the testcases from the filepath by going line-by-line
and converting the string into into a dictionary using json.

"""

import os
import json
from typing import Callable, Dict, Any
from unittest.mock import patch

import pytest

from pixivpy.common.exceptions import InvalidJsonResponse
from pixivpy.common.data import AuthToken
from pixivpy import auth


# -------------------------------------- Test Mapping ---------------------------------------
_TESTCASE_DIR = os.path.dirname(__file__) + '/auth_testcases'
_AUTH_TEST_INFO = {
    'get_auth_token': {
        'fn': auth.get_auth_token,
        'valid_args':   ['email', 'password'],
        'valid_json':   f'{_TESTCASE_DIR}/get_auth_token_valid.json',
        'invalid_json': f'{_TESTCASE_DIR}/get_auth_token_invalid.json'
    },
    'renew_auth_token': {
        'fn': auth.renew_auth_token,
        'valid_args':    [AuthToken('access', 'refresh', 3600)],
        'valid_json':   f'{_TESTCASE_DIR}/renew_auth_token_valid.json',
        'invalid_json': f'{_TESTCASE_DIR}/renew_auth_token_invalid.json'
    }
}


# --------------------------------------- Test Cases ----------------------------------------
@pytest.mark.parametrize(
    "auth_fn, args, invalid_json",
    [
        (test_info['fn'], test_info['valid_args'], json.loads(json_testcase))
        for test_info in _AUTH_TEST_INFO.values()
        for json_testcase in open(test_info['invalid_json'], encoding='utf-8').readlines()
    ]
)
def test_auth_invalid_json(auth_fn: Callable, args: Any, invalid_json: Dict[Any, Any]):
    """Test auth calls when the the JSON response is invalid.

    Ensures that the auth call raises an InvalidJsonResponse exception is thrown when the JSON
    received from the model is in an unexpected, imparsable format under conditions where the
    arguments and response status code are valid.

    Args:
        auth_fn: The auth function to test.
        args: Valid function arguments for the auth function.
        invalid_json: Invalid JSON response received by the model.

    """
    # Setup the mocked auth function with the returned json
    auth_func_patch = patch(f'pixivpy.auth.models.{auth_fn.__name__}')
    auth_func_mock = auth_func_patch.start()
    auth_func_mock.return_value = invalid_json

    # Run with the mocked model function with returned invalid json
    with pytest.raises(InvalidJsonResponse):
        auth_fn(*args)


@pytest.mark.parametrize(
    "auth_fn, args, valid_json",
    [
        (test_info['fn'], test_info['valid_args'], json.loads(json_testcase))
        for test_info in _AUTH_TEST_INFO.values()
        for json_testcase in open(test_info['valid_json'], encoding='utf-8').readlines()
    ]
)
def test_auth_valid_json(auth_fn: Callable, args: Any, valid_json: Dict[str, Any]):
    """Test auth calls when the JSON response is valid.

    Ensures that the auth call is able to extract information from the JSON to create an AuthToken
    object without any issues and checks that the fields of the token are set to the expected
    value.

    Args:
        auth_fn: The auth function to test.
        args: Valid function arguments for the auth function.
        valid_json: Valid JSON response received by the model.

    """
    # Setup the mocked auth function with the returned json
    auth_func_patch = patch(f'pixivpy.auth.models.{auth_fn.__name__}')
    auth_func_mock = auth_func_patch.start()
    auth_func_mock.return_value = valid_json

    # Run with the mocked model function with returned json
    auth_token = auth_fn(*args)
    assert valid_json['response']['access_token'] == auth_token.access_token, (
        'Access token did not match')
    assert valid_json['response']['refresh_token'] == auth_token.refresh_token, (
        'Refresh token did not match expected')
    assert valid_json['response']['expires_in'] == auth_token.ttl, (
        'Token expiration time did not match expected')
