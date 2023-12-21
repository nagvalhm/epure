from typing import Any, List, Callable, Union
from uuid import UUID


def check_type(var_name:str, value:Any, must_be:Union[type,List[type]]):
    err_text = f'{var_name} must be '
    check_all(err_text, value, must_be, isinstance)
    # for typ in must_be:
    #     if isinstance(value, typ):
    #         return
    #     else:
    #         err_text += f'{must_be} or'
    
    # raise TypeError(err_text[:-3])

def check_subclass(var_name:str, value:type, must_be:Union[type,List[type]]):
    err_text = f'{var_name} must subclass '
    check_all(err_text, value, must_be, issubclass)
    # for typ in must_be:
    #     if issubclass(value, typ):
    #         return
    #     else:
    #         err_text += f'{must_be} or'
    
    # raise TypeError(err_text[:-3])

def check_all(err_text:str, value:type, must_satisfy:Union[type,List[type]], check_func: Callable):
    if not isinstance(must_satisfy, list):
        must_satisfy = [must_satisfy]

    for must in must_satisfy:
        if check_func(value, must):
            return
        else:
            err_text += f'{must_satisfy} or'
    
    raise TypeError(err_text[:-3])

def is_uuid(obj:Any) -> bool:
    try:
        UUID(obj)
    except Exception:
        return False
    return True