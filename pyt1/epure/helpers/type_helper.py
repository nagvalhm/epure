from typing import Any


def check_type(var_name:str, value:Any, must_be:type):
    if not isinstance(value, must_be):
        raise TypeError(f'{var_name} must be {must_be}')