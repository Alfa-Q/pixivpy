"""Functional tests for models using an actual account token.

Ensures that each of the models are able to make a request to the server and receive some JSON
response.

"""

from typing import Dict, Any

import pytest

import config
from pixiv.api import (
    RESTRICT,
    FILTER,
    ARTICLE_CATEGORY,
    RANK_MODE
)
import pixiv.auth.models as authmodels
import pixiv.api.models as apimodels


# -------------------------------------- Test Mapping ---------------------------------------
_MODEL_TEST_INFO = [
    {
        'fn': authmodels.renew_auth_token,
        'valid_kwargs': {
            'auth_token': config.CACHED_TOKEN
        }
    },
    {
        'fn': apimodels.get_bookmark_tags,
        'valid_kwargs': {
            'user_id': config.USER_ID,
            'restrict': RESTRICT.PUBLIC,
            'offset': None,
            'auth_token': config.CACHED_TOKEN
        }
    },
    {
        'fn': apimodels.get_bookmarks,
        'valid_kwargs': {
            'user_id': config.USER_ID,
            'restrict': RESTRICT.PUBLIC,
            'max_bookmark_id': None,
            'tag': None,
            'auth_token': config.CACHED_TOKEN
        }
    },
    {
        'fn': apimodels.get_illust_comments,
        'valid_kwargs': {
            'illust_id': config.ILLUST_ID,
            'offset': None,
            'auth_token': config.CACHED_TOKEN
        }
    },
    {
        'fn': apimodels.get_recommended,
        'valid_kwargs': {
            'filter': FILTER.FOR_ANDROID,
            'include_ranked': 'true',
            'include_privacy': 'true',
            'min_bookmark_id_for_recent_illust': None,
            'max_bookmark_id_for_recommend': None,
            'offset': None,
            'auth_token': config.CACHED_TOKEN
        }
    },
    {
        'fn': apimodels.get_articles,
        'valid_kwargs': {
            'filter': FILTER.FOR_ANDROID,
            'category': ARTICLE_CATEGORY.ALL,
            'auth_token': config.CACHED_TOKEN
        }
    },
    {
        'fn': apimodels.get_related,
        'valid_kwargs': {
            'filter': FILTER.FOR_ANDROID,
            'illust_id': config.ILLUST_ID,
            'auth_token': config.CACHED_TOKEN
        }
    },
    {
        'fn': apimodels.get_rankings,
        'valid_kwargs': {
            'filter': FILTER.FOR_ANDROID,
            'mode': RANK_MODE.DAY,
            'offset': None,
            'auth_token': config.CACHED_TOKEN
        }
    }
]


# --------------------------------------- Test Cases ----------------------------------------
@pytest.mark.parametrize("test_info", [test_info for test_info in _MODEL_TEST_INFO])
def test_no_errors(test_info: Dict[str, Any]):
    """Ensure that no errors occur when making a call to the model.

    Basic sanity test to ensure that something is retrieved and ensure that the API call is most
    likely functioning as expected.

    Args:
        test_info: Model test information.

    """
    json = test_info['fn'](**test_info['valid_kwargs'])
    assert dict == type(json)
