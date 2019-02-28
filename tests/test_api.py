"""
tests.test_api
--------------
Pixiv API tests.
"""    

import os, copy, json
import pytest                                               # testcase parametrization and exception testing support
from typing import Callable, Dict                           # typing support for function signature
from unittest.mock import MagicMock, patch                  # mocking support
from pixivpy.common.exceptions import InvalidJsonResponse   # expected exceptions
from pixivpy import api                                     # api functions that are being tested


# Test case paths
testcase_dir = os.path.dirname(__file__) + '/api_testcases'
api_test_info = {
    'get_bookmarks': {
        'fn': api.get_bookmarks,
        'invalid_json': f'{testcase_dir}/get_bookmarks_invalid.json',
        'valid_json':   f'{testcase_dir}/get_bookmarks_valid.json'
    },
    'get_bookmark_tags': {
        'fn': api.get_bookmark_tags,
        'invalid_json': f'{testcase_dir}/get_bookmark_tags_invalid.json',
        'valid_json':   f'{testcase_dir}/get_bookmark_tags_valid.json'
    }
}


@pytest.mark.parametrize("api_gen_fn, args, invalid_json",
    # Use list comprehension to load the testcases for each API call from their associated file.
    [   # api_gen_fn                                # args                                      # invalid_json
        (api_test_info['get_bookmarks']['fn'],      ['12345','public',None,'some-valid-token'], json.loads(json_testcase)) \
            for json_testcase in open(api_test_info['get_bookmarks']['invalid_json'], encoding='utf-8').readlines() 
    ]+
    [
        (api_test_info['get_bookmark_tags']['fn'],  ['12345','public',None,'some-valid-token'], json.loads(json_testcase)) \
            for json_testcase in open(api_test_info['get_bookmark_tags']['invalid_json'], encoding='utf-8').readlines()
    ]
)
def test_api_gen_invalid_json(api_gen_fn: Callable, args, invalid_json: Dict):
    """ Test cases for API (generator fn) calls when the associated model returns a JSON response 
    that does not contain the keys required to extract the information of interest.
    
    Parameters:
        api_gen_fn: An API function which returns a generator.
        args: Some valid function arguments for the API function.
        invalid_json: Invalid JSON response received by the model.
        
    """
    # Setup the associated mocked model function with an invalid JSON return value
    api_model_patch = patch(f'pixivpy.api.models.{api_gen_fn.__name__}')
    api_model_mock = api_model_patch.start()
    api_model_mock.return_value = invalid_json

    # Run with the mocked model function with returned invalid JSON
    counter = 0
    with pytest.raises(InvalidJsonResponse) as e:
        for chunk in api_gen_fn(*args):
            counter += 1
            if counter == 2:
                break
    assert counter <= 1, 'Api generator function ran too many times!  Should have failed immediately.'


@pytest.mark.parametrize("api_gen_fn, args, valid_json, stop_json",
    # Use list comprehension to load the testcases for each API call from their associated file.
    [   # api_gen_fn                                # args                                      # valid_json
        (api_test_info['get_bookmarks']['fn'],      ['12345','public',None,'some-valid-token'], json.loads(json_testcase), stop_json) \
            for stop_json in [{'illusts':[], 'next_url': None}, {'illusts':[]}] \
            for json_testcase in open(api_test_info['get_bookmarks']['valid_json'], encoding='utf-8').readlines() 
    ]+
    [
        (api_test_info['get_bookmark_tags']['fn'],  ['12345','public',None,'some-valid-token'], json.loads(json_testcase), stop_json) \
            for stop_json in [{'bookmark_tags':[], 'next_url': None}, {'bookmark_tags':[]}] \
            for json_testcase in open(api_test_info['get_bookmark_tags']['valid_json'], encoding='utf-8').readlines()
    ]
)
@pytest.mark.parametrize("repeat", range(1, 5))
def test_api_gen_valid_json(api_gen_fn: Callable, args, valid_json: Dict, repeat: int, stop_json: Dict):
    """ Test cases for API (generator fn) calls when the associated model returns a JSON response 
    that contains the keys required to extract the information of interest.  
    
    All of the tests are under the assumption that each API generator terminates once the key 
    'next_url' is set to None OR it is missing from the JSON response.

    Parameters:
        api_gen_fn: An API function which returns a generator.
        args: Some valid function arguments for the API function.
        valid_json: Valid JSON response received by the model.
        repeat: The number of times to call the generator function.
        stop_json: The JSON response which denotes that no more items can be retrieved.

    """
    # Setup the associated mocked model function
    api_model_patch = patch(f'pixivpy.api.models.{api_gen_fn.__name__}')
    api_model_mock = api_model_patch.start()

    # Set up the number of times to repeat the call to the generator function by modifying the
    # return values for the model function on each iteration of the generator function call.
    api_model_mock.side_effect = [copy.deepcopy(valid_json)]*(repeat-1) + [stop_json]

    # Run with mocked model function with returned valid JSON
    counter = 0
    for chunk in api_gen_fn(*args):
        if counter == repeat:
            assert None == chunk
        else:
            counter += 1
    assert counter == repeat

