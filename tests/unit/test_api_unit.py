"""Test cases for pixivpy API functions.

Each new Auth function is registered in the _API_TEST_INFO dictionary as a sub-dictionary with
the function name mapped to a dictionary containing the following fields:
    name: The API and model function name.
    api_fn: The API function.
    valid_args: Valid arguments for the API function.
    valid_json: Filepath to a file containing good responses, each testcase separated by newline
        in JSON format.
    invalid_json: Filepath to a file containing bad responses, each testcase separated by newline
        in JSON format.
    list_key: The key in the JSON response which contains a list of information to be extracted.

The @pytest.mark.parametrize wrapper builds the testcases. It loads the textfile and goes
line-by-line, converting the string into a dictionary using json.

Testcases do not directly test the _call_api generator function which is called by each of the
API functions.

"""

import os
import copy
import json
from typing import Dict, Any
from unittest.mock import patch

import pytest

from pixivpy.api.exceptions import ApiError
from pixivpy.common.data import AuthToken
from pixivpy import api


# -------------------------------------- Test Mapping ---------------------------------------
_TESTCASE_DIR = os.path.dirname(__file__) + '/api_testcases'
_API_TEST_INFO = [
    {
        'name': 'get_bookmark_tags',
        'api_fn': api.get_bookmark_tags,
        'invalid_json': f'{_TESTCASE_DIR}/get_bookmark_tags_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_bookmark_tags_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600), '12345'],
        'list_key':     'bookmark_tags'
    },
    {
        'name': 'get_bookmarks',
        'api_fn': api.get_bookmarks,
        'invalid_json': f'{_TESTCASE_DIR}/get_bookmarks_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_bookmarks_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600), '12345'],
        'list_key':     'illusts'
    },
    {
        'name': 'get_illust_comments',
        'api_fn': api.get_illust_comments,
        'invalid_json': f'{_TESTCASE_DIR}/get_illust_comments_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_illust_comments_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600), '12345'],
        'list_key':     'comments'
    },
    {
        'name': 'get_recommended',
        'api_fn': api.get_recommended,
        'invalid_json': f'{_TESTCASE_DIR}/get_recommended_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_recommended_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600)],
        'list_key':     'illusts'
    },
    {
        'name': 'get_articles',
        'api_fn': api.get_articles,
        'invalid_json': f'{_TESTCASE_DIR}/get_articles_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_articles_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600)],
        'list_key':     'spotlight_articles'
    },
    {
        'name': 'get_related',
        'api_fn': api.get_related,
        'invalid_json': f'{_TESTCASE_DIR}/get_related_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_related_valid.json',
        'valid_args':   [AuthToken('access', 'access', 3600), '12345'],
        'list_key':     'illusts'
    },
    {
        'name': 'get_rankings',
        'api_fn': api.get_rankings,
        'invalid_json': f'{_TESTCASE_DIR}/get_rankings_invalid.json',
        'valid_json':   f'{_TESTCASE_DIR}/get_rankings_valid.json',
        'valid_args':   [AuthToken('access', 'refresh', 3600)],
        'list_key':     'illusts'
    }
]


# --------------------------------------- Test Cases ----------------------------------------
@pytest.mark.parametrize(
    "test_info, invalid_json",
    [
        (test_info, json.loads(json_testcase))
        for test_info in _API_TEST_INFO
        for json_testcase in open(test_info['invalid_json'], encoding='utf-8').readlines()
    ]
)
def test_api_gen_invalid_json(test_info: Dict[str, Any], invalid_json: Dict[Any, Any]):
    """Test API when the JSON response is invalid.

    Ensures that the API call function raises an Exception when the the JSON received from the
    model is in an unexpected, imparsable format under conditions where the arguments and response
    status are valid.

    Args:
        test_info: Test information for a specific API function.
        invalid_json: Invalid JSON response received by the model.

    """
    # Setup the associated mocked model function with an invalid JSON return value
    api_model = patch(f"pixivpy.api.models.{test_info['name']}").start()
    api_model.return_value = invalid_json

    # Run with the mocked model function with returned invalid JSON
    counter = 0
    with pytest.raises(Exception) as ex:
        for _ in test_info['api_fn'](*test_info['valid_args']):
            counter += 1
            if counter == 2:
                break
    #TODO: Assert the cause of the ApiError is DataNotFound (inner-exception)
    assert ex.type == ApiError, "Incorrect exception thrown."
    assert counter <= 1, (
        "Api generator function ran too many times!  Should have failed immediately.")


@pytest.mark.parametrize(
    "test_info, valid_json",
    [
        (test_info, json.loads(json_testcase))
        for test_info in _API_TEST_INFO
        for json_testcase in open(test_info['valid_json'], encoding='utf-8').readlines()
    ]
)
def test_api_gen_valid_json(test_info: Dict[str, Any], valid_json: Dict[str, Any]):
    """Test API when the JSON response is valid.

    Ensures that the API call function is yielding the correct data within a single JSON
    response under conditions where the arguments and response status are valid.

    Args:
        test_info: Test information for a specific API function.
        valid_json: Valid JSON response received by the model.

    """
    # Setup the associated mocked model function with a valid JSON return value
    api_model_mock = patch(f"pixivpy.api.models.{test_info['name']}").start()
    api_model_mock.return_value = copy.deepcopy(valid_json)

    # Total expected items in the valid json
    valid_data_items = valid_json[test_info['list_key']]

    # Run with mocked model function and check that it gets the same data items that are in the
    # valid_json
    generator = test_info['api_fn'](*test_info['valid_args'])

    for expected_data_item in valid_data_items:
        data_item = next(generator)
        assert expected_data_item == data_item, 'Mismatching data items!'
