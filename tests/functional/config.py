"""Configuration settings for functional tests.

Functional tests are not run in Travis CI due to the slow nature of requests in Travis CI.
As a result, it is preferable to run the functional tests locally before committing. Install dotenv
in your virtual environment and create a .env file with the following information to run the
functional tests:

TEST_ACCT_USERNAME=<pixiv username of test account>
TEST_ACCT_PASSWORD=<pixiv password of test account>

"""

import os

from dotenv import load_dotenv

from pixiv.auth import get_auth_token


# Use the local .env file
load_dotenv()

# A cached OAuth token which is used for functional tests on all the API calls except for the
# get_auth_token API call which requires a username and password.
CACHED_TOKEN = get_auth_token(os.environ['TEST_ACCT_USERNAME'], os.environ['TEST_ACCT_PASSWORD'])

# User ID of the test account which is used as an argument for the user ID of certain API calls.
USER_ID = 38225203

# Illust ID used for testing (retrieving comments, etc.)
ILLUST_ID = 71519097
