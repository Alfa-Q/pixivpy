"""
tests.auth.test_auth
--------------------
Testing the Pixiv authentication API.
"""

from pixivpy import auth
from tests.config import Config


def test_get_auth_token_sanity():
    """
    Ensure that the json response is valid, assuming credentials are valid.
    """
    json = auth.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    assert json is not None


def test_get_auth_token_json():
    """
    Ensure that the json response is type Dict
    """
    json = auth.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    assert dict == type(json)

