"""
pixivpy.api.models
--------------------
Pixiv application API request models for getting raw JSON response.
"""

from requests import Request
from pixivpy.common.decors import request, validate
from pixivpy.common.exceptions import InvalidJsonResponse


@validate([
    (lambda json: 'error' not in json.keys(),     InvalidJsonResponse),
    (lambda json: 'bookmark_tags' in json.keys(), InvalidJsonResponse),
    (lambda json: 'next_url' in json.keys(),      InvalidJsonResponse),
    (lambda json: list == type(json['bookmark_tags']), InvalidJsonResponse)
])
@request(expected_code=200)
def get_bookmark_tags(user_id: str, restrict: str, auth_token: str):
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


@validate([
    (lambda json: 'error' not in json.keys(),    InvalidJsonResponse),
    (lambda json: 'illusts' in json.keys(),      InvalidJsonResponse),
    (lambda json: 'next_url' in json.keys(),     InvalidJsonResponse),
    (lambda json: list == type(json['illusts']), InvalidJsonResponse)
])
@request(expected_code=200)
def get_bookmarks(user_id: str, restrict: str, max_bookmark_id: str, tag: str, auth_token: str):
    """ Retrieves the bookmarks for a specified user.

    Parameters:
        user_id: The Pixiv user ID.
        restrict: Work restrictions, either 'public' or 'private.'
        max_bookmark_id: Optional parameter specifying the ending point of the bookmarks to retrieve.
            If left empty, only one chunk of bookmarks is retrieved, starting from the beginning of 
            the most recent bookmarks for that user.
        tag: A bookmark tag that is in the user's tag options, dependent on the restrict mode.
        auth_token: The auth bearer token.
    
    Returns: A JSON response containing illustrations from a particular users bookmarks.
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


@validate([
    (lambda json: 'error' not in json.keys(),     InvalidJsonResponse),
    (lambda json: 'comments' in json.keys(),      InvalidJsonResponse),
    (lambda json: 'next_url' in json.keys(),      InvalidJsonResponse),
    (lambda json: list == type(json['comments']), InvalidJsonResponse),
])
@request(expected_code=200)
def get_illust_comments(illust_id: str, auth_token: str):
    """ Retrieves the comments on an illustration.

    Parameters:
        illust_id:  The illustration ID.
        auth_token: The auth bearer token.
    
    Returns: A JSON response containing comments from a particular illustration.
    """
    return Request(
        method = 'GET',
        url = f'https://app-api.pixiv.net/v2/illust/comments',
        params = {
            'illust_id': illust_id
        },
        headers = { 'authorization': f'Bearer {auth_token}' }
    )
