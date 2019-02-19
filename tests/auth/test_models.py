"""
tests.auth.test_models
-------------------
Testing the Pixiv authentication API model.
"""

import pytest
from pixivpy.common import exceptions
from pixivpy.auth import models
from tests.config import Config


def test_model_get_auth_token_sanity():
    """
    Ensure that the json response is not NULL
    """
    json = models.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    assert json is not None


def test_model_get_auth_token_json():
    """
    Ensure that the json response is type Dict
    """
    json = models.get_auth_token(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    assert dict == type(json)


def test_model_get_auth_token_fails_bad_status():
    """
    Ensure that the models.get_auth_token function fails due to an InvalidStatusCode exception
    for bad credentials.
    """
    with pytest.raises(exceptions.InvalidStatusCode):
        models.get_auth_token('', '')