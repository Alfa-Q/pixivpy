"""Validation for API JSON response data."""

from typing import Dict, Any

from pixivpy.common.exceptions import DataNotFound


def response_contains_key(res_json: Dict[str, Any], key: str):
    """Ensure the JSON response contains a specific key.

    Args:
        res_json: JSON response retrieved by the model function.
        key: Required key.

    Raises:
        DataNotFound: Required key was not in the JSON response.

    """
    if key not in res_json.keys():
        raise DataNotFound(
            f"Could not find key '{key}' in the JSON response.\n"+
            f"Got Keys: {res_json.keys()}"
        )


def response_key_mapping(res_json: Dict[str, Any], key: str, _type: type):
    """Ensure the key in a JSON response is mapped to a particular type.

    Assumes that the key already exists in the JSON response.  The 'key' is used for producing a
    more descriptive exception message (it's not useless).

    Args:
        res_json: JSON response retrieved by the model function.
        key: Required key.
        _type: Expected type of the key's associated value.

    Raises:
        DataNotFound: Type was invalid.

    """
    if _type != type(res_json[key]):
        raise DataNotFound(
            f"Failed to find the expected type for key '{key}.'\n"+
            f"Expected type: {_type} | Got type: {type(res_json[key])}.\n"+
            f"Full response: {res_json}"
        )
