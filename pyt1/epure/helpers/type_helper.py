from typing import Any, List, Callable


def check_type(var_name:str, value:Any, must_be:List[type]):
    err_text = f'{var_name} must be '
    check_all(err_text, value, must_be, isinstance)
    # for typ in must_be:
    #     if isinstance(value, typ):
    #         return
    #     else:
    #         err_text += f'{must_be} or'
    
    # raise TypeError(err_text[:-3])

def check_subclass(var_name:str, value:type, must_be:List[type]):
    err_text = f'{var_name} must subclass '
    check_all(err_text, value, must_be, issubclass)
    # for typ in must_be:
    #     if issubclass(value, typ):
    #         return
    #     else:
    #         err_text += f'{must_be} or'
    
    # raise TypeError(err_text[:-3])

def check_all(err_text:str, value:type, must_satisfy:List[Any], check_func: Callable):    
    for must in must_satisfy:
        if check_func(value, must):
            return
        else:
            err_text += f'{must_satisfy} or'
    
    raise TypeError(err_text[:-3])