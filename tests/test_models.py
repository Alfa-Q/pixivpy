"""
tests.test_models
----------------------
Test cases for pixivpy authentication and api models.
"""

import pytest
from typing import Callable, Dict               # typing support for function arguments
from unittest.mock import patch, MagicMock      # mocking support
from pixivpy.api  import models as apimodels    # api models to test
from pixivpy.auth import models as authmodels   # authentication models to test
from pixivpy.common import exceptions           # exceptions to catch


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
@pytest.mark.parametrize("model, m_args, status_code", [
    (authmodels.get_auth_token,     ['email','password'], 201),
    (authmodels.renew_auth_token,   ['some-valid-token'], 201),
    (apimodels.get_bookmark_tags,   ['12345','public','some-valid-token'], 201),
    (apimodels.get_bookmarks,       ['12345','public',None,None,'some-valid-token'], 201),
    (apimodels.get_illust_comments, ['12345','some-valid-token'], 201)
])
@patch('requests.Session')
def test_model_invalid_status_code(session_mock, model: Callable, m_args, status_code: int):
    """ Test cases for a model when the status code is invalid.
    
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
    with pytest.raises(exceptions.InvalidStatusCode) as e:
        model(*m_args)
    

@pytest.mark.parametrize("model, m_args, status_code, json", [
    (authmodels.get_auth_token,   ['email','password'], 200, {'has_error':True,'errors':{'system':{'message':'Invalid grant_type parameter or parameter missing'}}}),
    (authmodels.get_auth_token,   ['email','password'], 200, {'response':{'refresh_token': 'valid-token'}}),
    (authmodels.get_auth_token,   ['email','password'], 200, {'response':{'expires_in': 1000}}),
    (authmodels.get_auth_token,   ['email','password'], 200, {'response':{'random_key': 'some-value'}}),
    (authmodels.get_auth_token,   ['email','password'], 200, {'response':'string-not-a-dictionary'}),

    (authmodels.renew_auth_token, ['some-valid-token'], 200, {'has_error':True,'errors':{'system':{'message':'Invalid grant_type parameter or parameter missing'}}}),
    (authmodels.renew_auth_token, ['some-valid-token'], 200, {'response':{'refresh_token': 'valid-token'}}),
    (authmodels.renew_auth_token, ['some-valid-token'], 200, {'response':{'expires_in': 1000}}),
    (authmodels.renew_auth_token, ['some-valid-token'], 200, {'response':{'random_key': 'some-value'}}),
    (authmodels.renew_auth_token, ['some-valid-token'], 200, {'response':'string-not-a-dictionary'}),

    (apimodels.get_bookmark_tags, ['12345','prevet','some-valid-token'], 200,  {'error':{'user_message':'','message':'{\u0022restrict\u0022:[\u0022Restrict contains invalid value\u0022]}','reason':'','user_message_details':{}}}),
    (apimodels.get_bookmark_tags, ['12345','public','some-valid-token'], 200,  {'bookmark_tags':[]}),
    (apimodels.get_bookmark_tags, ['12345','private','some-valid-token'], 200, {'next_url':None}),
    
    (apimodels.get_bookmarks, ['12345','public',None,None,'some-valid-token'], 200, {'error':{'user_message':'','message':'{\u0022restrict\u0022:[\u0022Restrict contains invalid value\u0022]}','reason':'','user_message_details':{}}}),
    (apimodels.get_bookmarks, ['12345','public',None,None,'some-valid-token'], 200, {'illusts':[]}),        # NEED BOTH
    (apimodels.get_bookmarks, ['12345','public',None,None,'some-valid-token'], 200, {'next_url':None}),

    (apimodels.get_illust_comments, ['12345','some-valid-token'], 200, {'error':{'user_message':'','message':'Error occurred at the OAuth process. Please check your Access Token to fix this. Error Message: invalid_request','reason':'','user_message_details':{}}}),
    (apimodels.get_illust_comments, ['12345','some-valid-token'], 200, {'comments':[]}),                    # NEED BOTH
    (apimodels.get_illust_comments, ['12345','some-valid-token'], 200, {'next_url':None})
])
@patch('requests.Session')
def test_model_valid_status_code_invalid_json(session_mock, model: Callable, m_args, status_code: int, json: Dict):
    """ Test cases for a model when the status code is valid, but the json response is invalid due 
    to missing keys.
    
    Parameters:
        session_mock: The mock object for 'requests.Session' which is created by patch decorator.
        model: The model function to test.
        m_args: Some valid function arguments for the model function.
        status_code: A valid status code.
        json: Invalid JSON response.
    """
    # Setup the mocked session and session response.
    response_mock = create_mock_response(status_code=status_code, json=json)
    session_mock.return_value = MagicMock(
        # Mock object contains function 'send' and returns the mocked response
        send = MagicMock(return_value=response_mock)
    )
    # Run with the mocked session and mock response
    with pytest.raises(exceptions.InvalidJsonResponse) as e:
        model(*m_args)


@pytest.mark.parametrize("model, m_args, status_code, json", [
    (authmodels.get_auth_token,     ['email','password'], 200, {'response':{'refresh_token': 'valid-token', 'expires_in': 3600}}),
    (authmodels.renew_auth_token,   ['some-valid-token'], 200, {'response':{'refresh_token': 'valid-token', 'expires_in': 3600}}),
    (apimodels.get_bookmark_tags,   ['12345','public','some-valid-token'], 200, {'bookmark_tags':[],'next_url':None}),
    (apimodels.get_bookmarks,       ['12345','public',None,None,'some-valid-token'], 200, {'illusts':[],'next_url':None}),
    (apimodels.get_illust_comments, ['12345','some-valid-token'], 200, {'comments':[],'next_url':None})
])
@patch('requests.Session')
def test_model_valid_status_code_valid_json(session_mock, model: Callable, m_args, status_code: int, json: Dict):
    """ Test cases for a model when the status code is valid and the json response is valid.
    
    Parameters:
        session_mock: The mock object for 'requests.Session' which is created by patch decorator.
        model: The model function to test.
        m_args: Some valid function arguments for the model function.
        status_code: A valid status code.
        json: Valid JSON response.
    """
    # Setup the mocked session and session response.
    response_mock = create_mock_response(status_code=status_code, json=json)
    session_mock.return_value = MagicMock(
        # Mock object contains function 'send' and returns the mocked response
        send = MagicMock(return_value=response_mock)
    )
    # Run with the mocked session and mock response
    model(*m_args)
