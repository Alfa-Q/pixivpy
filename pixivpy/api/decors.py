"""
"""


def api_generator(api_model: Callable[Dict], kwargs: Dict, extract_param: str, transform_json: Callable):
    """ API generator function which continues to 
    """
    try:
        json = {'next_url': 'first_run'}
        param_value = None
        
        while json['next_url'] != None or json['next_url'] != "":
            
            json = api_model(**kwargs)

            # If next_url key not in the response, set to None to stop next iteration.
            # Makes the fn more flexible in case the json schema changes in the future.
            if 'next_url' not in json.keys():
                json['next_url'] = None
            
            # Check contains certain keys or values
            if not valid_json(json):
                raise InvalidJsonResponse(json) 
            
            # Yield the transformed results (list of particular fields, etc.)
            yield transform_json(json)
    except StopIteration:
        return
    except Exception as e:
        raise e