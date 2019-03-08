"""Pixiv API functions for retrieving data.

Layer above the models module for repeatedly making an API call to retrieve the next chunk of data
and extracts the data of interest from the JSON response.

Example of an API Function Usage:
    >>> from pixivpy import api
    >>> for each bookmark_chunk in api.get_bookmarks(...):
    >>>     for bookmark in bookmark_chunk:
    >>>         print(bookmark)
    {json data}
    {json data}
    ...

#TODO: Iterate in the _generator_api function so a single item is returned instead of a list of
       items.
"""

import urllib.parse as urlparse
from typing import Iterator, Dict, List, Callable, Any

from pixivpy.api import models
from pixivpy.api.data import (
    RESTRICT,
    ARTICLE_CATEGORY,
    FILTER,
    RANK_MODE
)
from pixivpy.common.exceptions import InvalidJsonResponse
from pixivpy.common.data import AuthToken


#TODO: Remove transform JSON and valid_json arguments
def _generator_api(api_model: Callable[[Any], Dict], kwargs: Dict,
                   valid_json: Callable[[Dict], bool], param_keys: [str],
                   transform_json) -> Iterator[List[Dict]]:
    """AI helper generator function for repeatedly retrieving data via API calls.

    All Pixiv API responses contain a JSON key called "next_url" which is used to retrieve the
    next chunk of data like so:
    {
        'target_key': [{JSON DATA},{JSON DATA},{JSON DATA}]
        'next_url': https://pixiv-apicall.com/getdata?offset=#
    }
    Using the 'next_url' key in the JSON response, the query parameters in the URL are parsed and
    the api_model is called again. The function continues this loop until the 'next_url' key is
    mapped to an empty string, null value, or the key does not exist which indicates that no more
    data can be retrieved.

    Args:
        api_model: API model function used for retrieving the raw JSON response.
        kwargs: api_model arguments, with each argument name mapped to its associated value.
        valid_json: Test before the JSON data received by the model is transformed and yielded
        param_keys: Parameter keys within the 'next_url' query to be extracted.
        transform_json: Function to transforms the JSON response before yielding it.

    Yields:
        The next chunk of JSON data; a list of JSON data.

    Raises:
        InvalidJsonResponse

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

            # Check contains certain keys or values
            if not valid_json(json):
                raise InvalidJsonResponse(json)

            # If requires any parameter from the JSON response, set it to the kwargs
            if json['next_url'] is not None and json['next_url'] != "" and json['next_url'] != 'first_run':
                parsed = urlparse.urlparse(json['next_url'])
                for param_key in param_keys:
                    kwargs[param_key] = urlparse.parse_qs(parsed.query)[param_key][0]

            # Yield the transformed results (list of particular fields, etc.)
            yield transform_json(json)
    except StopIteration:
        return
    except InvalidJsonResponse as e:  # pylint: disable=invalid-name
        raise e


def get_bookmark_tags(auth_token: AuthToken, user_id: str, restrict: str = RESTRICT.PUBLIC,
                      offset: str = None) -> Iterator[List[Dict]]:
    """Retrieve the bookmark tags for a specified user.

    Args:
        auth_token: OAuth bearer token.
        user_id: Pixiv user ID.
        restrict: Work restriction option.
        offset: Optional parameter specifying the offset into a user's complete list of bookmark
            tags.

    Yields:
        The next chunk of JSON bookmark tags from a particular user's list of bookmark tags.

    Additional Info:
        If the offset parameter is left empty the first chunk of bookmark tags retrieved starts
        from the beginning of the user's complete bookmark tag list.

    """
    generator = _generator_api(
        api_model=models.get_bookmark_tags,
        kwargs={
            'user_id': user_id,
            'restrict': restrict,
            'offset': offset,
            'auth_token': auth_token
        },
        valid_json=lambda json: 'bookmark_tags' in json.keys(),
        param_keys=['offset'],
        transform_json=lambda json: [tag for tag in json['bookmark_tags']]
    )
    for data in generator:
        yield data


def get_bookmarks(auth_token: AuthToken, user_id: str, restrict: str = RESTRICT.PUBLIC,
                  tag: str = None) -> Iterator[List[Dict]]:
    """Retrieve the bookmarks for a specified user.

    Args:
        auth_token: OAuth bearer token.
        user_id: Pixiv user ID.
        restrict: Work restriction option.
        tag: Optional parameter that specifies a bookmark tag that is in the user's tag options,
            dependent on the restrict option.

    Yields:
        The next chunk of JSON illustrations from a particular user's list of bookmarks.

    Examples:
        Pixiv User
        - ID: 12345
        - Public Bookmark Tags:  ['sicc']
        - Private Bookmark Tags: ['boob', 'boobs', 'boobies']

        >>> [for x in get_bookmarks(tkn, 12345)]
        [{public bookmark}, {public bookmark}, ...]
        >>> [for x in get_bookmarks(tkn, 12345, RESTRICT.PUBLIC, 'sicc')]
        [{public bookmark you tagged 'sicc'}, ...]
        >>> [for x in get_bookmarks(tkn, 12345, RESTRICT.PRIVATE, 'boobies')]
        [{private bookmark you tagged 'boobies'}, ...]

    """
    generator = _generator_api(
        api_model=models.get_bookmarks,
        kwargs={
            'user_id': user_id,
            'restrict': restrict,
            'max_bookmark_id': None,
            'tag': tag,
            'auth_token': auth_token
        },
        valid_json=lambda json: 'illusts' in json.keys(),
        param_keys=['max_bookmark_id'],
        transform_json=lambda json: [illust for illust in json['illusts']]
    )
    for data in generator:
        yield data


def get_illust_comments(auth_token: AuthToken, illust_id: str,
                        offset: str = None) -> Iterator[List[Dict]]:
    """Retrieve the comments on a specified illustration.

    Args:
        auth_token: OAuth bearer token.
        illust_id: Pixiv illustration ID.
        offset: Optional parameter specifying the offset into an illustration's complete list of
            comments.

    Yields:
        The next chunk of JSON comments from a particular illustration.

    """
    generator = _generator_api(
        api_model=models.get_illust_comments,
        kwargs={
            'illust_id': illust_id,
            'offset': offset,
            'auth_token': auth_token
        },
        valid_json=lambda json: 'comments' in json.keys(),
        param_keys=['offset'],
        transform_json=lambda json: [comment for comment in json['comments']]
    )
    for data in generator:
        yield data


def get_recommended(auth_token: AuthToken, filter: str = FILTER.FOR_ANDROID,
                    include_ranking_illusts: bool = True, include_privacy_policy: bool = True,
                    offset: str = None) -> Iterator[List[Dict]]:
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
        parameters, please use the models.
        min_bookmark_id_for_recent_illust:  Optional parameter which specifies the most recent
            illustration ID. Used by Pixiv backend for finding recommended bookmarks between
            some range of IDs and filtering ones out similar ones between this range.
        max_bookmark_id_for_recommend: Optional parameter specifying the max bookmark ID for
            finding a recommendation.

    Yields:
        The next chunk of JSON recommended illustrations.

    """
    generator = _generator_api(
        api_model=models.get_recommended,
        kwargs={
            'filter': filter,
            'include_ranking_illusts': include_ranking_illusts,
            'include_privacy_policy':  include_privacy_policy,
            'min_bookmark_id_for_recent_illust': None,
            'max_bookmark_id_for_recommend':     None,
            'offset': offset,
            'auth_token': auth_token
        },
        valid_json=lambda json: 'illusts' in json.keys(),
        param_keys=['min_bookmark_id_for_recent_illust', 'max_bookmark_id_for_recommend', 'offset'],
        transform_json=lambda json: [illust for illust in json['illusts']]
    )
    for data in generator:
        yield data


def get_articles(auth_token: AuthToken, filter: str = FILTER.FOR_ANDROID,
                 category: str = ARTICLE_CATEGORY.ALL) -> Iterator[List[Dict]]:
    """Retrieve Pixiv articles for a particular category.

    Args:
        auth_token: OAuth bearer token.
        filter: Filter option.
        category: Option which specifies the category to retrieve articles from.

    Yields:
        The next chunk of JSON articles.

    """
    generator = _generator_api(
        api_model=models.get_articles,
        kwargs={
            'filter': filter,
            'category': category,
            'auth_token': auth_token
        },
        valid_json=lambda json: 'spotlight_articles' in json.keys(),
        param_keys=['offset'],
        transform_json=lambda json: [article for article in json['spotlight_articles']]
    )
    for data in generator:
        yield data


def get_related(auth_token: AuthToken, illust_id: str,
                filter: str = FILTER.FOR_ANDROID) -> Iterator[List[Dict]]:
    """Retrieve illustrations related to the one provided.

    Args:
        auth_token: OAuth bearer token.
        illust_id: Pixiv illustration ID.
        filter: A filter option.

    Yields:
        The next chunk of JSON illustrations related to the one requested.

    """
    generator = _generator_api(
        api_model=models.get_related,
        kwargs={
            'filter': filter,
            'illust_id': illust_id,
            'auth_token': auth_token
        },
        valid_json=lambda json: 'illusts' in json.keys(),
        #HACK: params in URL contains on key for each seed instead of a single array of seeds.
        param_keys=[f'seed_illust_ids[{i}]' for i in range(0, 20)],
        transform_json=lambda json: [illust for illust in json['illusts']]
    )
    for data in generator:
        yield data


def get_rankings(auth_token: AuthToken, filter: str = FILTER.FOR_ANDROID,
                 mode: str = RANK_MODE.DAY, offset: str = None) -> Iterator[List[Dict]]:
    """Retrieve the top ranked illustrations for some mode.

    Args:
        auth_token: OAuth bearer token.
        filter: Filter option.
        mode: Ranking mode option.
        offset: Offset from the start of a list containing all of the ranked illustrations.

    Yields:
        The next chunk of JSON illustrations for the specified ranking mode.

    """
    generator = _generator_api(
        api_model=models.get_rankings,
        kwargs={
            'filter': filter,
            'mode': mode,
            'offset': offset,
            'auth_token': auth_token
        },
        valid_json=lambda json: 'illusts' in json.keys(),
        param_keys=['mode', 'offset', 'filter'],
        transform_json=lambda json: [illust for illust in json['illusts']]
    )
    for data in generator:
        yield data
