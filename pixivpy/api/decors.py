"""API decorator functions."""

from functools import wraps
from typing import Iterator, Dict, Any, Callable

from pixivpy.api.exceptions import ApiError
from pixivpy.common import validate


def generate_data(list_key: str) -> Iterator[Dict[str, Any]]:
    """Generate individual pieces of data from the wrapped function.

    Takes the generator api call object returned by the wrapped function to continuously generate
    the next JSON response.  Each response is validated to contain a list_key and if the key
    exists, each item in the list is yielded.  This process repeats until the api call object
    can no longer retrieve data from the model API function (likely due to yielding all data).

    Args:
        list_key: Key that is mapped to some list of data to be yielded.

    Yields:
        Each element in the the list.

    Raises:
        ApiError: An exception occurred while making the API call.
    
    """
    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Generator object used to repeatedly make API calls.
            api_call = function(*args, **kwargs)
            try:
                for response in api_call:
                    validate.response_contains_key(response, list_key)
                    validate.response_key_mapping(response, list_key, list)
                    for json_data in response[list_key]:
                        yield json_data
            except Exception as e:
                raise ApiError(
                    "An error occured while trying to make the API call '{function.__name__}.'"
                ) from e
        return wrapper
    return decorator
