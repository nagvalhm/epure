from ....epure.epure import Epure, epure
# from ...test_epure import epure_class1, epure_class2
import pytest

def compare_dict_to_obj(dict, obj):
    for item in dict:
        if item in obj.annotations.keys() and obj.annotations[item]==type(dict[item]):
            continue
        else:
            return False
    return True

def test_node_from_dict():
    
    @epure()
    class Human:
        name:str = "John"
        last_name:str = "Dow"
        age:int = 35

    # _dict = {key:value for key, value in Human.__dict__.items() if not key.startswith('__') 
    # and not callable(key) and key!='is_saved' and key!='prepared_resource'}
    _dict = {key:value for key, value in Human.__dict__.items() if not Human.is_excluded(key)}
    _dict['height'] = 6
    # _dict['name'] = 8
    # _dict = dict(name = "John", last_name = "Dow", Age = 35, grandma = epure_class1, grandpa = epure_class2)
    res = Human.from_dict(_dict)

    assert compare_dict_to_obj(_dict, res)