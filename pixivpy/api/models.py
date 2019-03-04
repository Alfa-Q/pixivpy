"""
pixivpy.api.models
--------------------
Pixiv application API request models for getting raw JSON response.
"""

from requests import Request
from pixivpy.common.data import AuthToken
from pixivpy.common.decors import request


@request(expected_code=200)
def get_bookmark_tags(user_id: str, restrict: str, offset: str, auth_token: AuthToken):
    """ Retrieves the user's bookmark tags for the particular bookmark type (private or public).

    Parameters:
        user_id: The Pixiv user ID.
        restrict: Work restrictions, specifying either 'public' or 'private.'
        offset: The offset from the start of the list of a user's bookmark tag list.
        auth_token: The auth bearer token.
    
    Returns: A JSON response containing the user's bookmark tags (public or private).
    """
    return Request(
        method = 'GET',
        url = 'https://app-api.pixiv.net/v1/user/bookmark-tags/illust',
        params = { 
            'user_id': user_id, 
            'restrict': restrict,
            'offset': offset
        },
        headers = { 'authorization': f'Bearer {auth_token.access_token}' }
    )


@request(expected_code=200)
def get_bookmarks(user_id: str, restrict: str, max_bookmark_id: str, tag: str, auth_token: AuthToken):
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
        url = 'https://app-api.pixiv.net/v1/user/bookmarks/illust',
        params = { 
            'user_id': user_id, 
            'restrict': restrict,
            'max_bookmark_id': max_bookmark_id,
            'tag':  tag
        },
        headers = { 'authorization': f'Bearer {auth_token.access_token}' }
    )


@request(expected_code=200)
def get_illust_comments(illust_id: str, offset: str, auth_token: AuthToken):
    """ Retrieves the comments on an illustration.

    Parameters:
        illust_id:  The illustration ID.
        offset: The offset from the start of a list containing all of the illustration comments.
        auth_token: The auth bearer token.
    
    Returns: A JSON response containing comments from a particular illustration.
    """
    return Request(
        method = 'GET',
        url = 'https://app-api.pixiv.net/v2/illust/comments',
        params = {
            'illust_id': illust_id,
            'offset': offset
        },
        headers = { 'authorization': f'Bearer {auth_token.access_token}' }
    )



@request(expected_code=200)
def get_recommended(filter: str, include_ranking_illusts: bool, include_privacy_policy: bool, 
                    min_bookmark_id_for_recent_illust: str, max_bookmark_id_for_recommend: str,
                    offset: str, auth_token: AuthToken):
    """ Retrieves the recommended illustrations for a user.

    Parameters:
        filter: A filter option (i.e. 'for_android')
        include_ranking_illusts: Whether or not the recommendations should include illusts 
            that are currently in the different Pixiv rankings (weekly, rookie, daily, etc.)
        include_privacy_policy:  Whether or not the privacy policy should be included (defaults to True).
        min_bookmark_id_for_recent_illust:  Most recent bookmark used for finding recommended 
            bookmarks between some range of IDs and filtering ones that are similar (on server side).
        max_bookmark_id_for_recommend:      Max bookmark ID for finding a recommendation.
        offset: The offset from the start of a list containing all of the recommended illustrations.
        auth_token: The auth bearer token.
    
    Returns: A JSON response containing recommended illustrations.
    """
    return Request(
        method = 'GET',
        url = 'https://app-api.pixiv.net/v1/illust/recommended',
        params = {
            'filter': filter,
            'include_ranking_illusts': include_ranking_illusts,
            'include_privacy_policy':  include_privacy_policy,
            'min_bookmark_id_for_recent_illust': min_bookmark_id_for_recent_illust,
            'max_bookmark_id_for_recommend': max_bookmark_id_for_recommend,
            'offset': offset
        },
        headers = { 'authorization': f'Bearer {auth_token.access_token}' }
    )


@request(expected_code=200)
def get_articles(filter: str, category: str, auth_token: AuthToken):
    """ Retrieves Pixiv articles from a particular category.

    Parameters:
        filter: A filter option (i.e. 'for_android')
        category: The article category to retrieve from (i.e. 'spotlight')
        auth_token: The auth bearer token.

    Returns: A JSON response containing articles for the particular category.
    """
    return Request(
        method = 'GET',
        url = 'https://app-api.pixiv.net/v1/spotlight/articles',
        params = {
            'filter': filter,
            'category': category
        },
        headers = { 'authorization': f'Bearer {auth_token.access_token}' }
    )


@request(expected_code=200)
def get_related(filter: str, illust_id: str, auth_token: AuthToken):
    """ Retrieves illustrations related to the one provided.

    Parameters:
        filter: A filter option (i.e. 'for_android')
        illust_id: The illustration which is used to find similar illustrations.
        auth_token: The auth bearer token.

    Returns: A JSON response containing related illustrations.
    """
    return Request(
        method = 'GET',
        url = 'https://app-api.pixiv.net/v2/illust/related',
        params = {
            'filter': filter,
            'illust_id': illust_id,
        },
        headers = { 'authorization': f'Bearer {auth_token.access_token}' }
    )


@request(expected_code=200)
def get_rankings(filter: str, mode: str, offset: str, auth_token: AuthToken):
    """ Retrieves the top ranked illustrations for some mode.

    Parameters:
        filter: A filter option (i.e. 'for_android')
        mode: Type of ranking (i.e. 'day', 'day_male', 'week', 'month', ...)  #TODO Create enums for modes and filters!!!
        offset: The offset from the start of a list containing all of the ranked illustrations for the mode + filter.

    Returns: A JSON response containing the ranked illustrations for the specified mode.
    """
    return Request(
        method = 'GET',
        url = 'https://app-api.pixiv.net/v1/illust/ranking',
        params = {
            'filter': filter,
            'mode': mode,
            'offset': offset
        },
        headers = { 'authorization': f'Bearer {auth_token.access_token}' }
    )
