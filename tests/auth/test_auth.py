"""
tests.auth.test_auth
--------------------
Testing the Pixiv authentication API.
"""

import pytest
from pixivpy import auth
from pixivpy.common import exceptions
from tests.config import Config


def test_get_auth_token_sanity():
    """
    Ensure that the tuple response is not NULL.
    """
    result_tuple = auth.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    assert result_tuple is not None


def test_get_auth_token_tuple():
    """
    Ensure that the parsed response is type tuple.
    """
    result_tuple = auth.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    assert tuple == type(result_tuple)

def test_get_auth_token_subtypes():
    """
    Ensure that the authentication token response is a tuple of str, int
    """
    tkn, ttl = auth.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    assert str == type(tkn)
    assert int == type(ttl)

def test_get_auth_token_values():
    """
    Ensure that the value of the auth bearer token is non-empty and the value of the time-to-live
    is greater than 0.
    """
    tkn, ttl = auth.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    assert 0 < len(tkn)
    assert 0 < ttl

def test_get_auth_token_fails_bad_status():
    """
    Ensure that the auth.get_auth_token function fails due to an InvalidStatusCode exception
    for bad credentials.
    """
    with pytest.raises(exceptions.InvalidStatusCode):
        auth.get_auth_token('', '')