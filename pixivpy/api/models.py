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


@request(expected_code=200)
def get_bookmarks(user_id: str, restrict: str, max_bookmark_id: str, tag: str, auth_token: str) -> Dict:
    """ Retrieves the bookmarks for a specified user.

    Parameters:
        user_id: The Pixiv user ID.
        restrict: Work restrictions, either 'public' or 'private.'
        max_bookmark_id: Optional parameter specifying the ending point of the bookmarks to retrieve.   // IF LEFT EMPTY, DEFAULTS TO JUST FIRST X NUMBER OF ILLUST BOOKMARKS
        tag: A bookmark tag that is in the user's tag options, dependent on the restrict mode.  // MAY NEED TO BE IN JAPANESE?
        auth_token: The auth bearer token.
    
    Returns: A JSON response containing bookmarks information.
    """
    return Request(
        method = 'GET',
        url = f'https://app-api.pixiv.net/v1/user/bookmarks/illust',
        params = { 
            'user_id': user_id, 
            'restrict': restrict,
            'max_bookmark_id': max_bookmark_id,
            'tag':  tag
        },
        headers = { 'authorization': f'Bearer {auth_token}' }
    )
