"""Test cases for pixiv authentication and api models.

The testscases check that the @request decorator throws an InvalidStatusCode for cases where the
response contains a code which does not match the expected response code. It only tests the
behavior of the @request decorator for each model, without being dependent on making actual
requests to a server. As a result, mocking is used to fake requests and responses to test this
behavior.

Each new API or Auth model is registered in the _MODEL_TEST_INFO dictionary as a sub-dictionary
with the function name as the key mapped to a dictionary containing the following fields:
    fn: The callable model function to test.
    valid_args: Valid arguments for the model.
    valid_codes: A list of valid status codes.
    invalid_codes: A list of invalid status codes.

The @pytest.mark.parametrize wrapper on each testcase function builds the testcases for each model
during runtime using list comprehension.

TODO: Add support for when a timeout occurs while sending the request and waiting for a response.

"""

from typing import Callable, Dict, List, Optional, Any
from unittest.mock import patch, MagicMock

import pytest

from pixiv.api  import models as apimodels
from pixiv.auth import models as authmodels
from pixiv.common.exceptions import InvalidStatusCode
from pixiv.common.data import AuthToken


# -------------------------------------- Test Mapping ---------------------------------------
_MODEL_TEST_INFO = {
    'get_auth_token': {
        'fn': authmodels.get_auth_token,
        'valid_args':    ['email', 'password'],
        'valid_codes':   [200],
        'invalid_codes': [-200, 302, 400, 403, 404]
    },
    'renew_auth_token': {
        'fn': authmodels.renew_auth_token,
        'valid_args':    [AuthToken('access', 'refresh', 3600)],
        'valid_codes':   [200],
        'invalid_codes': [-200, 302, 400, 403, 404]
    },
    'get_bookmark_tags': {
        'fn': apimodels.get_bookmark_tags,
        'valid_args':    ['12345', 'public', None, AuthToken('access', 'refresh', 3600)],
        'valid_codes':   [200],
        'invalid_codes': [-200, 302, 400, 403, 404]
    },
    'get_bookmarks': {
        'fn': apimodels.get_bookmarks,
        'valid_args':    ['12345', 'public', None, None, AuthToken('access', 'refresh', 3600)],
        'valid_codes':   [200],
        'invalid_codes': [-200, 302, 400, 403, 404]
    },
    'get_illust_comments': {
        'fn': apimodels.get_illust_comments,
        'valid_args':    ['12345', None, AuthToken('access', 'refresh', 3600)],
        'valid_codes':   [200],
        'invalid_codes': [-200, 302, 400, 403, 404]
    },
    'get_recommended': {
        'fn': apimodels.get_recommended,
        'valid_args':    ['for_android', True, True, 'min-id', 'max-id', None,
                          AuthToken('refresh', 'access', 3600)],
        'valid_codes':   [200],
        'invalid_codes': [-200, 302, 400, 403, 404]
    },
    'get_articles': {
        'fn': apimodels.get_articles,
        'valid_args':    ['for_android', 'all', AuthToken('access', 'refresh', 3600)],
        'valid_codes':   [200],
        'invalid_codes': [-200, 302, 400, 403, 404]
    },
    'get_related': {
        'fn': apimodels.get_related,
        'valid_args':    ['for_android', '12345', AuthToken('access', 'refresh', 3600)],
        'valid_codes':   [200],
        'invalid_codes': [-200, 302, 400, 403, 404]
    },
    'get_rankings': {
        'fn': apimodels.get_rankings,
        'valid_args':    ['for_android', 'day', None, AuthToken('access', 'refresh', 3600)],
        'valid_codes':   [200],
        'invalid_codes': [-200, 302, 400, 403, 404]
    }
}


# ------------------------------------ Helper Functions -------------------------------------
def create_mock_response(status_code: int, json: Optional[Dict[str, Any]] = None) -> MagicMock:
    """Create a mock object for the request.Response object.

    The mocked response object helps mimic a requests.Session object so the response from API calls
    (made using the requests library) can be faked. This helps test the behavior of the @request
    decorator when the status code does not match the expected code.

    Args:
        status_code: The status code to mimic.
        json: The json function return value to mimic.

    Returns:
        The mocked object, which mocks a requests.Response object.

    """
    # Add the 'json' function for the mocked response, and set return value to the provided
    # json parameter value
    response_mock = MagicMock(
        json=MagicMock(
            # json member function returns the json value
            return_value=json
        )
    )
    # Create the status code attribute for the mocked response
    response_mock.status_code = status_code
    return response_mock


# --------------------------------------- Test Cases ----------------------------------------
@pytest.mark.parametrize(
    "model, m_args, status_code",
    [
        (test_info['fn'], test_info['valid_args'], status_code)
        for test_info in _MODEL_TEST_INFO.values()
        for status_code in test_info['invalid_codes']
    ]
)
@patch('requests.Session')
def test_model_invalid_status_code(session_mock: MagicMock, model: Callable, m_args: List,
                                   status_code: int):
    """Test a model when the status code is invalid.

    Ensures that the InvalidStatusCode exception is thrown when the status code does not match the
    expected code.

    Args:
        session_mock: Mock object for 'requests.Session.'
        model: The model function to test.
        m_args: Valid function arguments for the model function.
        status_code: An invalid status code.

    """
    # Setup the mocked session and session response.
    response_mock = create_mock_response(status_code=status_code)
    session_mock.return_value = MagicMock(
        # Mock object contains function 'send' and returns the mocked response
        send=MagicMock(return_value=response_mock)
    )
    # Run with the mocked session and mock response
    with pytest.raises(InvalidStatusCode):
        model(*m_args)


@pytest.mark.parametrize(
    "model, m_args, status_code",
    [
        (test_info['fn'], test_info['valid_args'], status_code)
        for test_info in _MODEL_TEST_INFO.values()
        for status_code in test_info['valid_codes']
    ]
)
@patch('requests.Session')
def test_model_valid_status_code(session_mock: MagicMock, model: Callable, m_args: List,
                                 status_code: int):
    """Test a model when the status code is valid.

    If the status code is valid, the model should not raise any exceptions, and just return a JSON
    dictionary response.

    Args:
        session_mock: Mock object for 'requests.Session.'
        model: The model function to test.
        m_args: Valid function arguments for the model function.
        status_code: A valid status code.

    """
    # Setup the mocked session, mocked response, and session response.
    response_mock = create_mock_response(status_code=status_code, json=dict())
    session_mock.return_value = MagicMock(
        # Mock object contains function 'send' and returns the mocked response
        send=MagicMock(return_value=response_mock)
    )
    # Run with the mocked session and mock response
    response = model(*m_args)
    assert dict == type(response)
