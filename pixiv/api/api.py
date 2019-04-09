"""Pixiv API functions for retrieving data.

Layer above the models module for repeatedly making an API call to retrieve the next chunk of data
and extracts the data of interest from the JSON response.

"""

import urllib.parse as urlparse
from typing import Optional, Iterator, Dict, List, Callable, Any

from pixiv.api import models
from pixiv.api.decors import generate_data
from pixiv.api.data import (
    RESTRICT,
    ARTICLE_CATEGORY,
    FILTER,
    RANK_MODE
)
from pixiv.common.data import AuthToken


def _call_api(
        api_model: Callable[[Any], Dict[str, Any]],
        kwargs: Dict[str, Any],
        param_keys: List[str],
    ) -> Iterator[List[Dict[str, Any]]]:
    """Retrieve next JSON response.

    All Pixiv API responses contain a JSON key called "next_url" which is used to retrieve the
    next chunk of data like so:
    {
        'list_key': [{JSON DATA},{JSON DATA},{JSON DATA}]
        'next_url': https://pixiv-apicall.com/getdata?offset=#
    }

    Each item in the list of the JSON response contains information on the data requested.
        i.e. requesting bookmarks, each {JSON DATA} contains info about some illustration
            that is in your bookmarks.

    The JSON response is returned so the API function may perform validation, raise API specific
    errors if a key is missing, and yield each item in the list.

    Using the 'next_url' key in the JSON response, the query parameters in the URL are parsed and
    makes another API request. The function continues this loop until the 'next_url' key is
    mapped to an empty string, null value, or the key does not exist which indicates that no more
    data can be retrieved.

    Args:
        api_model: API model function used for retrieving the raw JSON response.
        kwargs: api_model arguments, with each argument name mapped to its associated value.
        param_keys: Keys within the 'next_url' query to be extracted and used as arguments for the
            next API request.

    Yields:
        The next JSON response.

    Raises:
        InvalidStatusCode: The API model function failed to make the API call.

    """
    try:
        json = {'next_url': 'first_run'}

        while json['next_url'] is not None or json['next_url'] != "":

            # Get raw JSON response
            json = api_model(**kwargs)

            # If next_url key not in the response, set to None to stop next iteration.
            # Makes the fn more flexible in case the json schema changes in the future.
            if 'next_url' not in json.keys():
                json['next_url'] = None

            # If requires any parameter from the JSON response, set it to the kwargs
            if json['next_url'] is not None and json['next_url'] != "" and json['next_url'] != 'first_run':
                parsed = urlparse.urlparse(json['next_url'])
                for param_key in param_keys:
                    kwargs[param_key] = urlparse.parse_qs(parsed.query)[param_key][0]
            yield json
    except StopIteration:
        return
    except Exception as ex:
        raise ex


@generate_data(list_key='bookmark_tags')
def get_bookmark_tags(
        auth_token: AuthToken,
        user_id: str,
        restrict: str = RESTRICT.PUBLIC,
        offset: Optional[str] = None
    ) -> Iterator[Dict[str, Any]]:
    """Retrieve the bookmark tags for a specified user.

    Args:
        auth_token: OAuth bearer token.
        user_id: Pixiv user ID.
        restrict: Work restriction option.
        offset: Optional parameter specifying the offset into a user's complete list of bookmark
            tags.

    Yields:
        The next bookmark tag from a user's list of bookmark tags in JSON format.

    Raises:
        ApiError: An exception occurred while making the API request.

    """
    return _call_api(
        api_model=models.get_bookmark_tags,
        kwargs={
            'user_id': user_id,
            'restrict': restrict,
            'offset': offset,
            'auth_token': auth_token
        },
        param_keys=['offset']
    )


@generate_data(list_key='illusts')
def get_bookmarks(
        auth_token: AuthToken,
        user_id: str,
        restrict: str = RESTRICT.PUBLIC,
        tag: Optional[str] = None
    ) -> Iterator[Dict[str, Any]]:
    """Retrieve the bookmarks for a specified user.

    Args:
        auth_token: OAuth bearer token.
        user_id: Pixiv user ID.
        restrict: Work restriction option.
        tag: Optional parameter that specifies a bookmark tag that is in the user's tag options,
            dependent on the restrict option.

    Yields:
        The next illustration from a user's list of bookmarks in JSON format.

    Raises:
        ApiError: An exception occurred while making the API request.

    """
    return _call_api(
        api_model=models.get_bookmarks,
        kwargs={
            'user_id': user_id,
            'restrict': restrict,
            'max_bookmark_id': None,
            'tag': tag,
            'auth_token': auth_token
        },
        param_keys=['max_bookmark_id'],
    )


@generate_data(list_key='comments')
def get_illust_comments(
        auth_token: AuthToken,
        illust_id: str,
        offset: Optional[int] = None
    ) -> Iterator[Dict[str, Any]]:
    """Retrieve the comments on an illustration.

    Args:
        auth_token: OAuth bearer token.
        illust_id: Pixiv illustration ID.
        offset: Specifies the offset into an illustration's complete list of comments.

    Yields:
        The next comment on a particular illustration in JSON format.

    Raises:
        ApiError: An exception occurred while making the API request.

    """
    return _call_api(
        api_model=models.get_illust_comments,
        kwargs={
            'illust_id': illust_id,
            'offset': str(offset),
            'auth_token': auth_token
        },
        param_keys=['offset']
    )


@generate_data(list_key='illusts')
def get_recommended(
        auth_token: AuthToken,
        filter: str = FILTER.FOR_ANDROID,
        include_ranking_illusts: bool = True,
        include_privacy_policy: bool = True,
        offset: Optional[str] = None
    ) -> Iterator[Dict[str, Any]]:
    """Retrieve the recommended illustrations for a user.

    Args:
        auth_token: OAuth bearer token.
        filter: Filter option.
        include_ranking_illusts: Determines if the recommendations should include illusts
            that are currently in the different Pixiv ranking categories.
        include_privacy_policy:  Determines if the privacy policy should be included.
        offset: Optional parameter specifying the offset into a user's complete list containing
            all of the recommended illustrations.

    Notes: #TODO: Clean up this shit
        These two fields are also in the params of the request.
        Under no circumstance will a sane user ever modify them.  If you wish to modify these
        parameters, please use the models function.
        min_bookmark_id_for_recent_illust:  Optional parameter which specifies the most recent
            illustration ID. Used by Pixiv backend for finding recommended bookmarks between
            some range of IDs and filtering ones out similar ones between this range.
        max_bookmark_id_for_recommend: Optional parameter specifying the max bookmark ID for
            finding a recommendation.

    Yields:
        The next recommended illustration in JSON format.

    Raises:
        ApiError: An exception occurred while making the API request.

    """
    return _call_api(
        api_model=models.get_recommended,
        kwargs={
            'filter': filter,
            'include_ranked': ('false', 'true')[include_ranking_illusts],
            'include_privacy': ('false', 'true')[include_privacy_policy],
            'min_bookmark_id_for_recent_illust': None,
            'max_bookmark_id_for_recommend': None,
            'offset': offset,
            'auth_token': auth_token
        },
        param_keys=['min_bookmark_id_for_recent_illust', 'max_bookmark_id_for_recommend', 'offset']
    )


@generate_data(list_key='spotlight_articles')
def get_articles(
        auth_token: AuthToken,
        filter: str = FILTER.FOR_ANDROID,
        category: str = ARTICLE_CATEGORY.ALL
    ) -> Iterator[Dict[str, Any]]:
    """Retrieve Pixiv articles for a particular category.

    Args:
        auth_token: OAuth bearer token.
        filter: Filter option.
        category: Option which specifies the category to retrieve articles from.

    Yields:
        The next article in JSON format.

    Raises:
        ApiError: An exception occurred while making the API request.

    """
    return _call_api(
        api_model=models.get_articles,
        kwargs={
            'filter': filter,
            'category': category,
            'auth_token': auth_token
        },
        param_keys=['offset']
    )


@generate_data(list_key='illusts')
def get_related(
        auth_token: AuthToken,
        illust_id: str,
        filter: str = FILTER.FOR_ANDROID
    ) -> Iterator[Dict[str, Any]]:
    """Retrieve illustrations related to the one provided.

    Args:
        auth_token: OAuth bearer token.
        illust_id: Pixiv illustration ID.
        filter: A filter option.

    Yields:
        The next chunk of JSON illustrations related to the one requested.

    Raises:
        ApiError: An exception occurred while making the API request.

    """
    return _call_api(
        api_model=models.get_related,
        kwargs={
            'filter': filter,
            'illust_id': illust_id,
            'auth_token': auth_token
        },
        #HACK: params in URL contains on key for each seed instead of a single array of seeds.
        #   This is a unreliable, temporary solution.
        param_keys=[f'seed_illust_ids[{i}]' for i in range(0, 20)]
    )


@generate_data(list_key='illusts')
def get_rankings(
        auth_token: AuthToken,
        filter: str = FILTER.FOR_ANDROID,
        mode: str = RANK_MODE.DAY,
        offset: Optional[str] = None
    ) -> Iterator[Dict[str, Any]]:
    """Retrieve the top ranked illustrations for some mode.

    Args:
        auth_token: OAuth bearer token.
        filter: Filter option.
        mode: Ranking mode option.
        offset: Offset from the start of a list containing all of the ranked illustrations.

    Yields:
        The next chunk of JSON illustrations for the specified ranking mode.

    Raises:
        ApiError: An exception occurred while making the API request.

    """
    return _call_api(
        api_model=models.get_rankings,
        kwargs={
            'filter': filter,
            'mode': mode,
            'offset': offset,
            'auth_token': auth_token
        },
        param_keys=['mode', 'offset', 'filter']
    )
