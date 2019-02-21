"""
pixivpy.api.models
--------------------
Pixiv application API request models for getting raw JSON response.
"""

from requests import Request
from pixivpy.common.decors import request
from typing import Dict


@request(expected_code=200)
def get_bookmark_tags(user_id: str, restrict: str, auth_token: str) -> Dict:
    """ Retrieves the user's bookmark tags for the particular bookmark type (private or public).

    Parameters:
        user_id: The Pixiv user ID.
        restrict: Work restrictions, specifying either 'public' or 'private.'
        auth_token: The auth bearer token.
    
    Returns: A JSON response containing the user's bookmark tags (public or private).
    """
    return Request(
        method = 'GET',
        url = f'https://app-api.pixiv.net/v1/user/bookmark-tags/illust',
        params = { 'user_id': user_id, 'restrict': restrict },
        headers = { 'authorization': f'Bearer {auth_token}' }
    )


