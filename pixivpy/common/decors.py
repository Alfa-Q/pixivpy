"""
pixivpy.common.decors
-------------
pixivpy common decorator functions.
"""

import requests
from functools import wraps
from typing import Dict, Callable, Any, List, Tuple
from .exceptions import InvalidStatusCode


def validate(validators: List[Tuple[Callable[[Any],bool], Exception]]):
    """ Decorator for validating the return value of a wrapped function.

    Parameters:
        validators: A list of tuples containing a validation (test) function and the exception to throw 
            if the validation is false.

    Returns: The validated result of the wrapped function or an exception if any of the tests failed.
    """
    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            value = function(*args, **kwargs)
            for test, exception in validators:
                if not test(value):
                    raise exception(value)
            return value
        return wrapper
    return decorator


def request(expected_code: int) -> Dict:
    """ Decorator for making requests using a Request object model returned by the decorated 
    function with support for status code validation.

    Parameters:
        expected_code: The expected response status code.

    Returns: The JSON response, if the API call was successful.

    Raises a InvalidStatusCode exception if the expected_code does not match the response status 
    code.
    """
    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            request = function(*args, **kwargs)
            prepared = request.prepare()
            response = requests.Session().send(prepared)

            if response.status_code != expected_code:
                raise InvalidStatusCode(
                    f'Expected Code: {expected_code} | Got: {response.status_code}\n'+
                    f'\tFunction Call: {function.__name__}\n'
                    f'\tResponse Content: {response.content}'
                )
            return response.json()
        return wrapper
    return decorator