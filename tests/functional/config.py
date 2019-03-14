"""Configuration settings for functional tests."""

import os

from pixivpy.auth import get_auth_token


# A cached OAuth token which is used for functional tests on all the API calls except for the
# get_auth_token API call which requires a username and password.
CACHED_TOKEN = get_auth_token(os.environ['TEST_ACCT_USERNAME'], os.environ['TEST_ACCT_PASSWORD'])

# User ID of the test account which is used as an argument for the user ID of certain API calls.
USER_ID = 38225203

# Illust ID used for testing (retrieving comments, etc.)
ILLUST_ID = 71519097
