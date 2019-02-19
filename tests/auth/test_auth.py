"""
tests.auth.test_auth
--------------------
Testing the Pixiv authentication API.
"""

import pytest
from pixivpy import auth
from pixivpy.common import exceptions
from tests.config import Config


""" ------------------------------------- get_auth_token -------------------------------------- """
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
    Ensure that the parsed response is a tuple of str, int
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
    

""" ------------------------------------ renew_auth_token ------------------------------------- """
def test_renew_auth_token_sanity():
    """
    Ensure that the tuple response is not NULL.
    """
    tkn, ttl = auth.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    result_tuple = auth.renew_auth_token(tkn)
    assert result_tuple is not None


def test_renew_auth_token_tuple():
    """
    Ensure that the parsed response is type tuple.
    """
    tkn, ttl = auth.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    result_tuple = auth.renew_auth_token(tkn)
    assert tuple == type(result_tuple)


def test_renew_auth_token_subtypes():
    """
    Ensure that the parsed response is a tuple of str, int
    """
    tkn_1, ttl_1 = auth.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    tkn_2, ttl_2 = auth.renew_auth_token(tkn_1)
    assert str == type(tkn_2)
    assert int == type(ttl_2)


def test_renew_auth_token_values():
    """
    Ensure that the value of the auth bearer token is non-empty and the value of the time-to-live
    is greater than 0.
    """
    tkn_1, ttl_1 = auth.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    tkn_2, ttl_2 = auth.renew_auth_token(tkn_1)
    assert 0 < len(tkn_2)
    assert 0 < ttl_2


def test_renew_auth_token_fails_bad_status():
    """
    Ensure that the auth.renew_auth_token function fails due to an InvalidStatusCode exception
    for bad credentials.
    """
    with pytest.raises(exceptions.InvalidStatusCode):
        auth.renew_auth_token('')