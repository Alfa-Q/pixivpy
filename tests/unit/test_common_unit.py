"""Test cases for Pixiv common modules."""

from typing import Dict, Any, Optional

import pytest

from pixiv.common import validate
from pixiv.common.exceptions import DataNotFound, PixivError


@pytest.mark.parametrize(
    "fn_kwargs, error",
    [
        (   # Does not contain the target key
            {'res_json': {}, 'key': 'the_key'},
            DataNotFound
        ),
        (   # Contains some other key that is not the target
            {'res_json': {'not_the_key': []}, 'key': 'the_key'},
            DataNotFound
        ),
        (   # Contains the target key, no exception
            {'res_json': {'the_key': []}, 'key': 'the_key'},
            None
        )
    ]
)
def test_validate_response_contains_key(fn_kwargs: Dict[str, Any], error: Optional[PixivError]):
    """Test validation functions for responses.

    Sanity test to ensure that basic validation is functioning properly, raising the appropriate
    errors for a responses that is missing a required key.

    Args:
        fn_kwargs: Arguments for validation fn being tested.
        error: The error expected from the function call.

    """
    if error is None:
        validate.response_contains_key(**fn_kwargs)
    else:
        with pytest.raises(DataNotFound):
            validate.response_contains_key(**fn_kwargs)


@pytest.mark.parametrize(
    "fn_kwargs, error",
    [
        (   # Type does not match expected
            {'res_json': {'the_key': 10}, 'key': 'the_key', '_type': list},
            DataNotFound
        ),
        (   # Type matches expected
            {'res_json': {'the_key': []}, 'key': 'the_key', '_type': list},
            None
        )
    ]
)
def test_validate_response_typing(fn_kwargs: Dict[str, Any], error: Optional[PixivError]):
    """Test validation functions for responses.

    Sanity test to ensure that basic validation is functioning properly, raising the appropriate
    errors when the value type does not match the expected type.

    Args:
        fn_kwargs: Arguments for validation fn being tested.
        error: The error expected from the function call.

    """
    if error is None:
        validate.response_key_mapping(**fn_kwargs)
    else:
        with pytest.raises(DataNotFound):
            validate.response_key_mapping(**fn_kwargs)
