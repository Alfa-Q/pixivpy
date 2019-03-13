"""Pixiv API request models.

Pixiv application API request models for getting raw JSON responses.
Each function returns a Request object which defines the Pixiv app API call which is then executed
by the 'request' wrapper, converted into JSON, and returned to the callee.
"""

from typing import Dict, Any

from requests import Request

from pixivpy.auth import renew_auth_token
from pixivpy.common.data import AuthToken
from pixivpy.common.decors import request


@request(expected_code=200)
def get_bookmark_tags(user_id: str, restrict: str, offset: str,
                      auth_token: AuthToken) -> Dict[str, Any]:
    """Retrieve the user's bookmark tags for the particular bookmark type.

    Args:
        user_id: Pixiv user ID.
        restrict: Work restriction option.
        offset: Optional parameter specifying the offset into a user's complete list of bookmark
            tags.
        auth_token: OAuth bearer token.

    Returns:
        A JSON response containing the user's bookmark tags.

    """
    auth_token = renew_auth_token(auth_token)
    return Request(
        method='GET',
        url='https://app-api.pixiv.net/v1/user/bookmark-tags/illust',
        params={
            'user_id': user_id,
            'restrict': restrict,
            'offset': offset
        },
        headers={
            'authorization': f'Bearer {auth_token.access_token}'
        }
    )


@request(expected_code=200)
def get_bookmarks(user_id: str, restrict: str, max_bookmark_id: str, tag: str,
                  auth_token: AuthToken) -> Dict[str, Any]:
    """Retrieve the bookmarks for a specified user.

    Args:
        user_id: Pixiv user ID.
        restrict: Work restriction option.
        max_bookmark_id: Optional parameter specifying the end point of the bookmarks to retrieve.
        tag: Optional parameter that specifies a bookmark tag that is in the user's tag options,
            dependent on the restrict option.
        auth_token: OAuth bearer token.

    Returns:
        A JSON response containing illustrations from a particular users bookmarks.

    """
    auth_token = renew_auth_token(auth_token)
    return Request(
        method='GET',
        url='https://app-api.pixiv.net/v1/user/bookmarks/illust',
        params={
            'user_id': user_id,
            'restrict': restrict,
            'max_bookmark_id': max_bookmark_id,
            'tag':  tag
        },
        headers={
            'authorization': f'Bearer {auth_token.access_token}'
        }
    )


@request(expected_code=200)
def get_illust_comments(illust_id: str, offset: str, auth_token: AuthToken) -> Dict[str, Any]:
    """Retrieve the comments on a specified illustration.

    Args:
        illust_id: Pixiv illustration ID.
        offset: Optional parameter specifying the offset into an illustration's complete list of
            comments.
        auth_token: OAuth bearer token.

    Returns:
        A JSON response containing comments from a particular illustration.

    """
    auth_token = renew_auth_token(auth_token)
    return Request(
        method='GET',
        url='https://app-api.pixiv.net/v2/illust/comments',
        params={
            'illust_id': illust_id,
            'offset': offset
        },
        headers={
            'authorization': f'Bearer {auth_token.access_token}'
        }
    )


@request(expected_code=200)
def get_recommended(filter: str, include_ranked: bool, include_privacy: bool,
                    min_bookmark_id_for_recent_illust: str, max_bookmark_id_for_recommend: str,
                    offset: str, auth_token: AuthToken) -> Dict[str, Any]:
    """Retrieve the recommended illustrations for a user.

    The recommendation is based on a the bookmark with the smallest ID within a list containing
    some amount of the user's most recent bookmarks. It then looks for similar bookmarks between
    this min ID bookmark and some maximum bookmark ID. Both of these values are retrieved encoded
    in the query of the 'next_url' URL value.

    Args:
        filter: A filterable option.
        include_ranked: Recommended should include illusts that are in the ranked list (i.e. daily)
        include_privacy: Whether or not the privacy policy should be included.
        min_bookmark_id_for_recent_illust: Bookmark ID used for finding recommended bookmarks.
        max_bookmark_id_for_recommend: Max bookmark ID for finding a recommendation.
        offset: Offset from the start of a list containing all of the recommended illustrations.
        auth_token: OAuth bearer token.

    Returns:
        A JSON response containing recommended illustrations.

    """
    auth_token = renew_auth_token(auth_token)
    return Request(
        method='GET',
        url='https://app-api.pixiv.net/v1/illust/recommended',
        params={
            'filter': filter,
            'include_ranking_illusts': include_ranked,
            'include_privacy_policy':  include_privacy,
            'min_bookmark_id_for_recent_illust': min_bookmark_id_for_recent_illust,
            'max_bookmark_id_for_recommend': max_bookmark_id_for_recommend,
            'offset': offset
        },
        headers={
            'authorization': f'Bearer {auth_token.access_token}'
        }
    )


@request(expected_code=200)
def get_articles(filter: str, category: str, auth_token: AuthToken) -> Dict[str, Any]:
    """Retrieve Pixiv articles from a particular category.

    Args:
        filter: A filter option.
        category: The article category to retrieve from.
        auth_token: OAuth bearer token.

    Returns:
        A JSON response containing articles for the particular category.

    """
    auth_token = renew_auth_token(auth_token)
    return Request(
        method='GET',
        url='https://app-api.pixiv.net/v1/spotlight/articles',
        params={
            'filter': filter,
            'category': category
        },
        headers={
            'authorization': f'Bearer {auth_token.access_token}'
        }
    )


@request(expected_code=200)
def get_related(filter: str, illust_id: str, auth_token: AuthToken) -> Dict[str, Any]:
    """Retrieve illustrations related to the one provided.

    Args:
        filter: A filter option.
        illust_id: The illustration that is used to find other similar illustrations.
        auth_token: OAuth bearer token.

    Returns:
        A JSON response containing related illustrations.

    """
    auth_token = renew_auth_token(auth_token)
    return Request(
        method='GET',
        url='https://app-api.pixiv.net/v2/illust/related',
        params={
            'filter': filter,
            'illust_id': illust_id,
        },
        headers={
            'authorization': f'Bearer {auth_token.access_token}'
        }
    )


@request(expected_code=200)
def get_rankings(filter: str, mode: str, offset: str, auth_token: AuthToken) -> Dict[str, Any]:
    """Retrieve the top ranked illustrations for some mode.

    Args:
        filter: A filter option.
        mode: Type of ranking.
        offset: Offset from the start of a list containing all of the filtered ranked illustrations
        auth_token: OAuth bearer token.

    Returns:
        A JSON response containing the ranked illustrations for the specified mode.

    """
    auth_token = renew_auth_token(auth_token)
    return Request(
        method='GET',
        url='https://app-api.pixiv.net/v1/illust/ranking',
        params={
            'filter': filter,
            'mode': mode,
            'offset': offset
        },
        headers={
            'authorization': f'Bearer {auth_token.access_token}'
        }
    )
