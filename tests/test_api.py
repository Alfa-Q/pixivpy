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


""" -------------------------------------- Test Mapping --------------------------------------- """
#   To setup testcases for an API generator function, it must contain the following fields:
#       fn:             The API generator function to test.
#       invalid_json:   Text file containing bad responses that should produce an exception, each testcase separated by newline in JSON format.
#       valid_json:     Text file containing good responses, each testcase separated by newline in JSON format.
#       valid_args:     List of valid function arguments. Ensures that only the extraction is being tested.
#       list_key:       The key in the JSON response which contains a list of information to be extracted.
testcase_dir = os.path.dirname(__file__) + '/api_testcases'
api_test_info = {
    'get_bookmarks': {
        'fn': api.get_bookmarks,
        'invalid_json': f'{testcase_dir}/get_bookmarks_invalid.json',
        'valid_json':   f'{testcase_dir}/get_bookmarks_valid.json',
        'valid_args':   ['12345','public',None,'some-valid-token'],
        'list_key':     'illusts'
    },
    'get_bookmark_tags': {
        'fn': api.get_bookmark_tags,
        'invalid_json': f'{testcase_dir}/get_bookmark_tags_invalid.json',
        'valid_json':   f'{testcase_dir}/get_bookmark_tags_valid.json',
        'valid_args':   ['12345','public',None,'some-valid-token'],
        'list_key':     'bookmark_tags'
    },
    'get_illust_comments': {
        'fn': api.get_illust_comments,
        'invalid_json': f'{testcase_dir}/get_illust_comments_invalid.json',
        'valid_json':   f'{testcase_dir}/get_illust_comments_valid.json',
        'valid_args':   ['12345',None,'some-valid-token'],
        'list_key':     'comments'
    },
    'get_recommended': {
        'fn': api.get_recommended,
        'invalid_json': f'{testcase_dir}/get_recommended_invalid.json',
        'valid_json':   f'{testcase_dir}/get_recommended_valid.json',
        'valid_args':   ['for_android',True,True,'min-id','max-id',None,'some-valid-token'],
        'list_key':     'illusts'
    }
}


""" --------------------------------------- Test Cases ---------------------------------------- """
@pytest.mark.parametrize("api_gen_fn, args, invalid_json",
    # Use list comprehension to load the testcases for each API call from their associated file.
    [
    #   api generator fn    list of valid api fn args   invalid json to test 
        (test_info['fn'],   test_info['valid_args'],    json.loads(json_testcase))
        for test_info in api_test_info.values()
        for json_testcase in open(test_info['invalid_json'], encoding='utf-8').readlines()
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
    [
    #   api generator fn    list of valid api fn args   valid json to test          stop json
        (test_info['fn'],   test_info['valid_args'],    json.loads(json_testcase),  stop_json)
        for test_info in api_test_info.values()
        for json_testcase in open(test_info['valid_json'], encoding='utf-8').readlines()
        for stop_json in [{test_info['list_key']:[], 'next_url': None}, {test_info['list_key']:[]}]
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

