"""Pixivpy common decorator functions."""

from functools import wraps
from typing import Dict, Callable, List

import requests

from pixivpy.common.exceptions import InvalidStatusCode, RetryError


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
                    f'Expect Code: {expected_code} | Got: {response.status_code} | '+
                    f'Function Call: {function.__name__}\n'+
                    f'Response Body: {response.content}'
                )
            return response.json()
        return wrapper
    return decorator


def retry(times: int, on_exceptions: List[Exception]):
    """Retry the wrapped function when specific exceptions are raised.

    Args:
        times: The number of times to retry. Must be greater than or equal to 1.
        on_exceptions: Exceptions that make the wrapped function retry-able.

    Returns:
        The return value of the wrapped function.

    Raises:
        Exception: The last exception raised after exceeding the number of retry times.
        RetryError: An unexpected exception occurred while making the function call.

    Example:
        >>> @retry(times = 2, on_exceptions = [InvalidStatusCode, InvalidJsonResponse])
        >>> def some_function(...)...

        Makes the function retry-able up to 2 times if and only if the wrapped function raises an
        InvalidStatusCode exception OR a InvalidJsonResponse exception.

    """
    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            raised = []
            for _ in range(times):
                try:
                    return function(*args, **kwargs)
                except Exception as ex:
                    raised.append(ex)
                    if type(ex) not in on_exceptions:
                        raise RetryError(
                            'An unexpected error occurred while calling the function '+
                            f'{function.__name__}.'
                        ) from ex
            raise raised.pop()
        return wrapper
    return decorator
