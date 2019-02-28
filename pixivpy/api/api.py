"""
pixivpy.api.api
--------------------
Layer above the models module for extracting particular data from the JSON response.
"""

import urllib.parse as urlparse
from . import models
from typing import Generator, Dict, List, Callable, Any
from pixivpy.common.exceptions import InvalidJsonResponse


def _generator_api(api_model: Callable[[List[Any]], Dict], kwargs: Dict, valid_json: Callable[[Dict], bool], param_key: str, transform_json: Callable[[Dict], Any]):
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
                kwargs[param_key] = urlparse.parse_qs(parsed.query)[param_key][0]
            
            # Yield the transformed results (list of particular fields, etc.)
            yield transform_json(json)
    except StopIteration:
        return
    except Exception as e:
        raise e


def get_bookmark_tags(user_id: str, restrict: str, offset: str, auth_token: str):
    """ Retrieves the bookmark tags for a specified user.

    Parameters:
        user_id: The Pixiv user ID.
        restrict: Work restrictions, either 'public' or 'private.'
        offset: Optional parameter specifying the ending point of the bookmark tags to retrieve.
            If left empty, only one chunk of bookmark tags is retrieved, starting from the 
            beginning the list which contains all of the user's bookmark tags.
        auth_token: The auth bearer token.
    
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
        param_key = 'offset',
        transform_json = lambda json: [ tag for tag in json['bookmark_tags'] ]
    )
    for data in generator:
        yield data


def get_bookmarks(user_id: str, restrict: str, tag: str, auth_token: str) -> Generator[List[Dict], None, None]:
    """ Retrieves the bookmarks for a specified user.

    Parameters:
        user_id: The Pixiv user ID.
        restrict: Work restrictions, either 'public' or 'private.'
        max_bookmark_id: Optional parameter specifying the ending point of the bookmarks to retrieve.
            If left empty, only one chunk of bookmarks is retrieved, starting from the beginning of 
            the most recent bookmarks for that user.
        tag: A bookmark tag that is in the user's tag options, dependent on the restrict mode.
        auth_token: The auth bearer token.
    
    Returns: A chunk of JSON illustration information from a particular user's bookmarks.
    """
    generator = _generator_api(
        api_model = models.get_bookmarks,
        kwargs = {
            'user_id': user_id, 
            'restrict': restrict, 
            'max_bookmark_id': None,
            'tag': tag,
            'auth_token': auth_token
        },
        valid_json = lambda json: 'illusts' in json.keys(),
        param_key  = 'max_bookmark_id',
        transform_json = lambda json: [ illust for illust in json['illusts'] ]
    )
    for data in generator:
        yield data
