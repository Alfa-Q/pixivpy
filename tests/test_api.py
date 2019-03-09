"""Test cases for pixivpy API functions.

#TODO: Convert tests to function _generator_api() tests.
#TODO: Add tests for each API function yielding a single JSON item at a time (non-list).

Each new Auth function is registered in the _API_TEST_INFO dictionary as a sub-dictionary with
the function name mapped to a dictionary containing the following fields:
    fn: The API function to test.
    valid_args: Valid arguments for the API function.
    valid_json: Filepath to a file containing good responses, each testcase separated by newline
        in JSON format.
    invalid_json: Filepath to a file containing bad responses, each testcase separated by newline
        in JSON format.
    list_key: The key in the JSON response which contains a list of information to be extracted.

The @pytest.mark.parametrize wrapper on each testcase function builds the testcases for each API
function using list comprehension. It loads the testcases from the filepath by going line-by-line
and converting the string into into a dictionary using json.

"""

import os
import copy
import json
from typing import Callable, Dict, Any
from unittest.mock import patch

import pytest

from pixivpy.common.exceptions import InvalidJsonResponse
from pixivpy.common.data import AuthToken
from pixivpy import api


# -------------------------------------- Test Mapping ---------------------------------------
_TESTCASE_DIR = os.path.dirname(__file__) + '/api_testcases'
_API_TEST_INFO = {
    'get_bookmark_tags': {
        'fn': api.get_bookmark_tags,
        'invalid_json': f'{_TESTCASE_DIR}/get_bookmark_tags_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_bookmark_tags_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600), '12345'],
        'list_key':     'bookmark_tags'
    },
    'get_bookmarks': {
        'fn': api.get_bookmarks,
        'invalid_json': f'{_TESTCASE_DIR}/get_bookmarks_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_bookmarks_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600), '12345'],
        'list_key':     'illusts'
    },
    'get_illust_comments': {
        'fn': api.get_illust_comments,
        'invalid_json': f'{_TESTCASE_DIR}/get_illust_comments_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_illust_comments_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600), '12345'],
        'list_key':     'comments'
    },
    'get_recommended': {
        'fn': api.get_recommended,
        'invalid_json': f'{_TESTCASE_DIR}/get_recommended_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_recommended_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600)],
        'list_key':     'illusts'
    },
    'get_articles': {
        'fn': api.get_articles,
        'invalid_json': f'{_TESTCASE_DIR}/get_articles_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_articles_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600)],
        'list_key':     'spotlight_articles'
    },
    'get_related': {
        'fn': api.get_related,
        'invalid_json': f'{_TESTCASE_DIR}/get_related_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_related_valid.json',
        'valid_args':   [AuthToken('access', 'access', 3600), '12345'],
        'list_key':     'illusts'
    },
    'get_rankings': {
        'fn': api.get_rankings,
        'invalid_json': f'{_TESTCASE_DIR}/get_rankings_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_rankings_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600)],
        'list_key':     'illusts'
    }
}


# --------------------------------------- Test Cases ----------------------------------------
@pytest.mark.parametrize(
    "api_gen_fn, args, invalid_json",
    [
        (test_info['fn'], test_info['valid_args'], json.loads(json_testcase))
        for test_info in _API_TEST_INFO.values()
        for json_testcase in open(test_info['invalid_json'], encoding='utf-8').readlines()
    ]
)
def test_api_gen_invalid_json(api_gen_fn: Callable, args: Any, invalid_json: Dict[Any, Any]):
    """Test API generator fn when the JSON response is invalid.

    Ensures that the API generator function raises an Exception when the the JSON received from the
    model is in an unexpected, imparsable format under conditions where the arguments and response
    status are valid.

    Args:
        api_gen_fn: The API generator function to test.
        args: Valid function arguments for the API generator function.
        invalid_json: Invalid JSON response received by the model.

    """
    # Setup the associated mocked model function with an invalid JSON return value
    api_model_patch = patch(f'pixivpy.api.models.{api_gen_fn.__name__}')
    api_model_mock = api_model_patch.start()
    api_model_mock.return_value = invalid_json

    # Run with the mocked model function with returned invalid JSON
    counter = 0
    with pytest.raises(InvalidJsonResponse):
        for _ in api_gen_fn(*args):
            counter += 1
            if counter == 2:
                break
    assert counter <= 1, (
        'Api generator function ran too many times!  Should have failed immediately.')


@pytest.mark.parametrize(
    "api_gen_fn, args, valid_json, stop_json",
    [
        (test_info['fn'], test_info['valid_args'], json.loads(json_testcase), stop_json)
        for test_info in _API_TEST_INFO.values()
        for json_testcase in open(test_info['valid_json'], encoding='utf-8').readlines()
        for stop_json in [{test_info['list_key']:[], 'next_url': None}, {test_info['list_key']:[]}]
    ]
)
@pytest.mark.parametrize("repeat", range(1, 5))
def test_api_gen_valid_json(api_gen_fn: Callable, args: Any, valid_json: Dict[str, Any],
                            repeat: int, stop_json: Dict[str, Any]):
    """Test API generator fn when the JSON response is valid.

    Ensures that the API generator function raises an Exception when the the JSON received from the
    model is in an unexpected, imparsable format under conditions where the arguments and response
    status are valid.

    Note:
        Pixiv's API returns only a portion of data from a complete list on each API call. Because of
        this limitation, the _generator_api() function in pixivpy.api repeatedly makes a request as
        long as the 'next_url' key (which containing parameters that are used to retrieve the next
        batch of items in this complete list) is set. If the 'next_url' key is missing or not set to
        anything, this indicates that no more data can be fetched, so the _generator_api() function
        will stop making requests.

    Args:
        api_gen_fn: The API generator function to test.
        args: Valid function arguments for the API generator function.
        valid_json: Valid JSON response received by the model.
        repeat: Number of times to call the generator before stopping.
        stop_json: JSON response which denotes that no more items can be retrieved due to the
            a missing 'next_url' key.

    """
    # Setup the associated mocked model function
    api_model_patch = patch(f'pixivpy.api.models.{api_gen_fn.__name__}')
    api_model_mock = api_model_patch.start()

    # Set up the number of times to repeat the call to the generator function by modifying the
    # return values for the model function on each iteration of the generator function call.
    api_model_mock.side_effect = [copy.deepcopy(valid_json)]*(repeat-1) + [stop_json]

    # Run with mocked model function with returned valid JSON
    counter = 0
    generator = api_gen_fn(*args)
    for chunk in generator:
        if counter == repeat:
            assert chunk is None
        else:
            counter += 1
    assert counter == repeat
