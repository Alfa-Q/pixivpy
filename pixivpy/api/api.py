"""
pixivpy.api.api
--------------------
Layer above the models module for extracting particular data from the JSON response 
(i.e. a list of JSON data containing information of interest).
"""

import urllib.parse as urlparse
from . import models
from typing import Generator, Dict, List, Callable, Any
from pixivpy.common.exceptions import InvalidJsonResponse
from pixivpy.common.data import AuthToken


def _generator_api(api_model: Callable[[List[Any]], Dict], kwargs: Dict, valid_json: Callable[[Dict], bool], param_keys: [str], transform_json: Callable[[Dict], Any]):
    """ API helper generator function which continues to retrieve data via API calls until the 
    'next_url' key is mapped to an empty string, null value, or the key does not exist.

    Parameters:
        api_model: The API model used for retrieving the raw JSON response.
        kwargs: The api_model arguments, with the argument names mapped to its associated value.
        valid_json: Test before the JSON data received by the model is transformed and yielded.
        param_key: A parameter key within the 'next_url' query which is used to update the associated value in the api_model arguments. 
        transform_json: Function to transforms the JSON response before yielding it.

    Returns: A generator which returns some transformed JSON data.
    """
    try:
        json = {'next_url': 'first_run'}
        
        while json['next_url'] != None or json['next_url'] != "":
            
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
            if json['next_url'] != None and json['next_url'] !="" and json['next_url'] != 'first_run':
                parsed = urlparse.urlparse(json['next_url'])
                for param_key in param_keys:
                    print(parsed.query)
                    kwargs[param_key] = urlparse.parse_qs(parsed.query)[param_key][0]
                    print(kwargs)  # DEBUG
            
            # Yield the transformed results (list of particular fields, etc.)
            yield transform_json(json)
    except StopIteration:
        return
    except Exception as e:
        raise e


def get_bookmark_tags(auth_token: AuthToken, user_id: str, restrict: str='public', offset: str=None):
    """ Retrieves the bookmark tags for a specified user.

    Parameters:
        auth_token: The auth bearer token.
        user_id: The Pixiv user ID.
        restrict: Work restrictions, either 'public' or 'private.'
        offset: Optional parameter specifying the starting point within the complete list of user \
            bookmark tags.  If left empty, only one chunk of the user's bookmark tags is retrieved, \
            starting from the beginning the complete list of the user's bookmark tags.
    
    Returns: A chunk of bookmark tags from a particular user's bookmarks.
    """
    generator = _generator_api(
        api_model = models.get_bookmark_tags,
        kwargs = {
            'user_id': user_id,
            'restrict': restrict,
            'offset': offset,
            'auth_token': auth_token 
        },
        valid_json = lambda json: 'bookmark_tags' in json.keys(),
        param_keys = ['offset'],
        transform_json = lambda json: [ tag for tag in json['bookmark_tags'] ]
    )
    for data in generator:
        yield data


def get_bookmarks(auth_token: AuthToken, user_id: str, restrict: str='public', tag: str=None) -> Generator[List[Dict], None, None]:
    """ Retrieves the bookmarks for a specified user.

    Parameters:
        auth_token: The auth bearer token.
        user_id: The Pixiv user ID to retrieve bookmarks from.
        restrict: Specifies the work restrictions, either 'public' or 'private'
        tag: Optional parameter specifying a bookmark tag that is in the user's tag options, \
            dependent on the restrict mode.
    
    Returns: A chunk of JSON illustration information from a particular user's bookmarks.
    """
    yield from _generator_api(
        api_model = models.get_bookmarks,
        kwargs = {
            'user_id': user_id, 
            'restrict': restrict, 
            'max_bookmark_id': None,
            'tag': tag,
            'auth_token': auth_token
        },
        valid_json = lambda json: 'illusts' in json.keys(),
        param_keys  = ['max_bookmark_id'],
        transform_json = lambda json: [ illust for illust in json['illusts'] ]
    )


def get_illust_comments(auth_token: AuthToken, illust_id: str, offset: str=None) -> Generator[List[Dict], None, None]:
    """ Retrieves the comments for a specified user.

    Parameters:
        auth_token: The auth bearer token.
        illust_id: The illustration ID to identify which comments to retrieve.
        offset: Optional parameter specifying the starting point within the complete list of \
            comments (string integer).  If left empty, only one chunk of the comments is  \
            retrieved, starting from the beginning of the complete list of comments. 

    Returns: A chunk of JSON comment information for a particular illustration.
    """
    generator = _generator_api(
        api_model = models.get_illust_comments,
        kwargs = {
            'illust_id': illust_id,
            'offset': offset,
            'auth_token': auth_token
        },
        valid_json = lambda json: 'comments' in json.keys(),
        param_keys = ['offset'],
        transform_json = lambda json: [ comment for comment in json['comments'] ]
    )
    for data in generator:
        yield data


def get_recommended(auth_token: AuthToken, filter: str='for_android', include_ranking_illusts: bool=True, 
                    include_privacy_policy: bool=True, min_bookmark_id_for_recent_illust: str=None, 
                    max_bookmark_id_for_recommend: str=None, offset: str=None) -> Generator[List[Dict], None, None]:
    """ Retrieves the recommended illustrations for a user.

    Parameters:
        auth_token: The auth bearer token.
        filter: Parameter which is used by Pixiv backend to filter the results somehow.
        include_ranking_illusts: Whether or not the recommendations should include illusts \
            that are currently in the different Pixiv rankings (weekly, rookie, daily, etc.)
        include_privacy_policy:  Whether or not the privacy policy should be included (defaults to True). \
        min_bookmark_id_for_recent_illust:  Optional parameter which specifies the most recent \
            illustration ID. Used by Pixiv backend for finding recommended bookmarks between \
            some range of IDs and filtering ones out similar ones between this range.
        max_bookmark_id_for_recommend: Optional parameter specifying the max bookmark ID for \
            finding a recommendation.
        offset: Optional parameter specifying the offset from the start of a list containing \
            all of the recommended illustrations.
    
    Returns: A chunk of JSON recommended illustrations based on the last on a range of bookmark IDs.
    """
    generator = _generator_api(
        api_model = models.get_recommended,
        kwargs = {
            'filter': filter,
            'include_ranking_illusts': include_ranking_illusts,
            'include_privacy_policy':  include_privacy_policy,
            'min_bookmark_id_for_recent_illust': min_bookmark_id_for_recent_illust,
            'max_bookmark_id_for_recommend':     max_bookmark_id_for_recommend,
            'offset': offset,
            'auth_token': auth_token
        },
        valid_json = lambda json: 'illusts' in json.keys(),
        param_keys = ['min_bookmark_id_for_recent_illust', 'max_bookmark_id_for_recommend', 'offset'],
        transform_json = lambda json: [ illust for illust in json['illusts'] ]
    )
    for data in generator:
        yield data


def get_articles(auth_token: AuthToken, filter: str='for_android', category: str='all') -> Generator[List[Dict], None, None]:
    """ Retrieves Pixiv articles for a particular category.

    Parameters:
        auth_token: The auth bearer token.
        filter: Parameter which is used by Pixiv backend to filter the results somehow.
        category: Parameter which specifies which category to grab articles from (defaults to all). 

    Returns: A chunk of JSON articles based on the category and platform.
    """
    generator = _generator_api(
        api_model = models.get_articles,
        kwargs = {
            'filter': filter,
            'category': category,
            'auth_token': auth_token
        },
        valid_json = lambda json: 'spotlight_articles' in json.keys(),
        param_keys = ['offset'],
        transform_json = lambda json: [ article for article in json['spotlight_articles'] ]
    )
    for data in generator:
        yield data


def get_related(auth_token: AuthToken, illust_id: str, filter: str='for_android') -> Generator[List[Dict], None, None]:
    """ Retrieves illustrations related to the one provided.

    Parameters:
        auth_token: The auth bearer token.
        illust_id: The illustration which is used to find similar illustrations.
        filter: A filter option (i.e. 'for_android')

    Returns: A JSON response containing related illustrations.
    """
    generator = _generator_api(
        api_model = models.get_related,
        kwargs = {
            'filter': filter,
            'illust_id': illust_id,
            'auth_token': auth_token
        },
        valid_json = lambda json: 'illusts' in json.keys(),
        param_keys = [ f'seed_illust_ids[{i}]' for i in range(0,20) ],
        transform_json = lambda json: [ illust for illust in json['illusts'] ]
    )
    for data in generator:
        yield data


def get_rankings(auth_token: AuthToken, filter: str='for_android', mode: str='day', offset: str=None) -> Generator[List[Dict], None, None]:
    """ Retrieves the top ranked illustrations for some mode.

    Parameters:
        auth_token: The auth bearer token.
        filter: A filter option (i.e. 'for_android')
        mode: Type of ranking (i.e. 'day', 'day_male', 'week', 'month', ...)  #TODO Create enums for modes and filters!!!
        offset: The offset from the start of a list containing all of the ranked illustrations for the mode + filter.

    Returns: A JSON response containing the ranked illustrations for the specified mode.
    """
    generator = _generator_api(
        api_model = models.get_rankings,
        kwargs = {
            'filter': filter,
            'mode': mode,
            'offset': offset,
            'auth_token': auth_token
        },
        valid_json = lambda json: 'illusts' in json.keys(),
        param_keys = ['mode', 'offset', 'filter'],
        transform_json = lambda json: [ illust for illust in json['illusts'] ]
    )
    for data in generator:
        yield data
