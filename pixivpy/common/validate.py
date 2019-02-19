"""
pixivpy.common.validate
-----------------------
Pixiv JSON response validation.
"""

from pixiv.common.exceptions import InvalidJSONResponse
from typing import Dict


def json(json: Dict):
    """ Ensures that the JSON response received is in valid format.

    Parameters:
        json: The JSON response received from the pixiv API call.

    Raises an InvalidJSONResponse exception if the JSON response was found to be invalid.
    """
    if json['error'] == True:
        raise InvalidJSONResponse(
            "'error' flag was set in the json response.\n"+
            '\tJSON: {json}'
        )