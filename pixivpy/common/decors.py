"""Pixivpy common decorator functions."""

from functools import wraps
from typing import Dict, Callable

import requests

from pixivpy.common.exceptions import InvalidStatusCode


def request(expected_code: int) -> Dict:
    """Make a request and validate the status code of a wrapped function.

    Takes the Request object returned by a wrapped function and uses it to make an API call
    via the requests module. After making the request, it checks the status code of the
    response and ensures that it matches the expected code.

    Args:
        expected_code: The expected response status code.

    Returns:
        The raw JSON response, if the API call was successful.

    Raises:
        InvalidStatusCode: The expected_code value does not match the response status code.

    """
    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            request_model = function(*args, **kwargs)
            prepared_request = request_model.prepare()
            response = requests.Session().send(prepared_request)

            if response.status_code != expected_code:
                raise InvalidStatusCode(
                    f'Expect Code: {expected_code} | Got: {response.status_code}\n'+
                    f'\tFunction Call: {function.__name__}\n'
                    f'\tResponse Content: {response.content}'
                )
            return response.json()
        return wrapper
    return decorator
