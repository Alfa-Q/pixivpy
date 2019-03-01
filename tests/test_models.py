"""
tests.test_models
----------------------
Test cases for pixivpy authentication and api models.
"""

import pytest                                               # testcase parametrization support
from typing import Callable, Dict, List                     # typing support for function arguments
from unittest.mock import patch, MagicMock                  # mocking support
from pixivpy.api  import models as apimodels                # api models to test
from pixivpy.auth import models as authmodels               # authentication models to test
from pixivpy.common.exceptions import InvalidStatusCode     # exceptions to catch


""" -------------------------------------- Test Mapping --------------------------------------- """
model_test_info = {
    'get_auth_token': {
        'fn': authmodels.get_auth_token,
        'valid_args':    ['email','password'],
        'valid_codes':   [200],
        'invalid_codes': [-200,302,400,403,404]
    },
    'renew_auth_token': {
        'fn': authmodels.renew_auth_token,
        'valid_args':    ['some-valid-token'], 
        'valid_codes':   [200],
        'invalid_codes': [-200,302,400,403,404]
    },
    'get_bookmark_tags': {
        'fn': apimodels.get_bookmark_tags,
        'valid_args':    ['12345','public',None,'some-valid-token'], 
        'valid_codes':   [200],
        'invalid_codes': [-200,302,400,403,404]
    },
    'get_bookmarks': {
        'fn': apimodels.get_bookmarks,
        'valid_args':    ['12345','public',None,None,'some-valid-token'],
        'valid_codes':   [200],
        'invalid_codes': [-200,302,400,403,404]
    },
    'get_illust_comments': {
        'fn': apimodels.get_illust_comments,
        'valid_args':    ['12345',None,'some-valid-token'],
        'valid_codes':   [200],
        'invalid_codes': [-200,302,400,403,404]
    },
    'get_recommended': {
        'fn': apimodels.get_recommended,
        'valid_args':    ['for_android',True,True,'min-id','max-id',None,'some-valid-token'],
        'valid_codes':   [200],
        'invalid_codes': [-200,302,400,403,404]
    }
}


""" ------------------------------------ Helper Functions ------------------------------------- """
def create_mock_response(status_code: int, json: Dict=None):
    """ Creates a mock object which mimics the behavior of the requests.Response object.
    Used to fake the response from API calls that are made using the requests library.

    Parameters:
        status_code: The status code to mimic.
        json: The json function return value to mimic.

    Returns: The mocked object, which should be set to a requests.get / requests.post 
    / requests.Session().send return_value.
    """
    # Add the 'json' function for the mocked response, and set return value to the provided
    # json parameter value
    response_mock = MagicMock(
        json = MagicMock(            
            # json function returns the json value
            return_value = json
        )
    )
    # Create the status code attribute for the mocked response
    response_mock.status_code = status_code
    return response_mock


""" --------------------------------------- Test Cases ---------------------------------------- """
@pytest.mark.parametrize("model, m_args, status_code", 
    # Use list comprehension to create the testcases for each model from the model_test_info dict.
    [
        (test_info['fn'],   test_info['valid_args'],   status_code)
        for test_info in model_test_info.values()
        for status_code in test_info['invalid_codes']
    ]
)
@patch('requests.Session')
def test_model_invalid_status_code(session_mock: MagicMock, model: Callable, m_args: List, status_code: int):
    """ Test cases for a model when the status code is invalid.  Ensures that the InvalidStatusCode
    exception is thrown when the status code does not match the expected.  This exception thrown by
    the model indicates that a problem is with the model, meaning that the model's request likely 
    needs to be updated.
    
    Parameters:
        session_mock: The mock object for 'requests.Session' which is created by patch decorator.
        model: The model function to test.
        m_args: Some valid function arguments for the model function.
        status_code: An invalid status code.

    """
    # Setup the mocked session and session response.
    response_mock = create_mock_response(status_code=status_code)
    session_mock.return_value = MagicMock(
        # Mock object contains function 'send' and returns the mocked response
        send = MagicMock(return_value=response_mock)
    )
    # Run with the mocked session and mock response
    with pytest.raises(InvalidStatusCode) as e:
        model(*m_args)


@pytest.mark.parametrize("model, m_args, status_code",
    # Use list comprehension to create the testcases for each model from the model_test_info dict.
    [
        (test_info['fn'],   test_info['valid_args'],   status_code)
        for test_info in model_test_info.values()
        for status_code in test_info['valid_codes']
    ]
)
@patch('requests.Session')
def test_model_valid_status_code(session_mock: MagicMock, model: Callable, m_args: List, status_code: int):
    """ Test cases for a model when the status code is valid.  If the status code is valid, the
    model should not raise any exceptions, and just return a JSON response.
    
    Parameters:
        session_mock: The mock object for 'requests.Session' which is created by patch decorator.
        model: The model function to test.
        m_args: Some valid function arguments for the model function.
        status_code: A valid status code.

    """
    # Setup the mocked session and session response.  JSON response is just a dictionary,
    # and is set to an empty dictionary since JSON validation is performed in 
    # (auth or api module) and will be tested in a different test module.
    response_mock = create_mock_response(status_code=status_code, json=dict())
    session_mock.return_value = MagicMock(
        # Mock object contains function 'send' and returns the mocked response
        send = MagicMock(return_value=response_mock)
    )
    # Run with the mocked session and mock response
    response = model(*m_args)
    assert dict == type(response)
