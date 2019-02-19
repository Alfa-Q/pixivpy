"""
tests.config
--------------
Configuration for setting up tests, using environmental variables.
"""

import os


class Config:
    TEST_EMAIL = os.environ['TEST_EMAIL']
    TEST_PASSWORD = os.environ['TEST_PASSWORD']