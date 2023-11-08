from ....epure.epure import Epure, epure
# from ...test_epure import epure_class1, epure_class2
from uuid import UUID
import pytest
from ...test_epure import EpureClass1
# from epure import Elist
from ....epure import Elist
from types import LambdaType, NoneType

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
        epure_cls:EpureClass1 = "1a35b818-81fe-45f5-9c60-3706b290cd68"
        name:str = "John"
        last_name:str = "Dow"
        age:int = 35

    # _dict = {key:value for key, value in Human.__dict__.items() if not key.startswith('__') 
    # and not callable(key) and key!='is_saved' and key!='prepared_resource'}
    # _dict = {key:value for key, value in Human.__dict__.items() if not Human.is_excluded(key)}
    # _dict['height'] = 6
    # _dict['name'] = 8
    # _dict['node_id'] = '312'
    # _dict['node_id'] = '1a35b818-81fe-45f5-9c60-3706b290cd68'
    _dict['age'] = None
    # _dict = dict(name = "John", last_name = "Dow", Age = 35, grandma = epure_class1, grandpa = epure_class2)
    res = Human.from_dict(_dict)

    assert compare_dict_to_obj(_dict, res)

def test_node_not_recursive_to_dict_default_depth_no_save():
    
    @epure()
    class EpureClsToDict1:
        nametag:str = "Plain"
        num:int = 86
    
    @epure()
    class EpureClsToDictPlain1:
        epure_cls:EpureClsToDict1
        text:str = "Text"
        age:int = 80

    inst = EpureClsToDictPlain1()
    inst.epure_cls = EpureClsToDict1()
    res = inst.to_dict()

    assert res == {'epure_cls': {'nametag': 'Plain', 'num': 86}, 'text': 'Text', 'age': 80}

def test_node_to_dict_custom_lambda_func_nested_vals_recursive_with_save():

    @epure()
    class EpureClsSimple:
        str0:str = "Texxxt"
        num0:int = 2

    epure_cls_simple1 = EpureClsSimple()
    epure_cls_simple2 = EpureClsSimple()

    @epure()
    class EpureClsToDict2:
        nametag:str = "Plain"
        num:int = 86
        elist_str_to_exclude:Elist[str] = Elist[str](["abc", "def"])
        elist_epure_to_exclude:Elist[EpureClsSimple] = Elist[EpureClsSimple]([epure_cls_simple1, epure_cls_simple2])
        elist_str_no_def_val:Elist[str]
        elist_str_def_val:Elist[str] = Elist[str](["abc", "def"])
        elist_epure:Elist[EpureClsSimple] = Elist[EpureClsSimple]([epure_cls_simple1, epure_cls_simple2])

    @epure()
    class ExcludedEpure:
        another_epure:EpureClsToDict2 = EpureClsToDict2()

    @epure()
    class EpureClsToDictPlain2:
        epure_cls:EpureClsToDict2
        excluded_epure:ExcludedEpure = ExcludedEpure()
        text:str = "Text"
        age:int = 80
        random_none_attr:NoneType = 3

    inst = EpureClsToDictPlain2()
    inst.epure_cls = EpureClsToDict2()
    inst.epure_cls.elist_str_no_def_val = Elist[str](["no", "definitions"])
    id1 = inst.save().node_id

    res = inst.to_dict(lambda_func= lambda field_name, field_value, parent_value, depth_level, args: 
                depth_level < 2 and (field_name != "excluded_epure" and field_name != "elist_str_to_exclude") and field_name != "elist_epure_to_exclude")
    
    
    assert res['epure_cls']['elist_str_no_def_val'] == ['no', 'definitions'] 
    assert res['epure_cls']['elist_epure'][0]['num0'] == 2

    res_json = inst.to_json()

    # expected_res_from_to_dict = {'node_id': 'bf35bd03-7bbf-42ef-a1f4-ab28dac9334f', 'epure_cls': {'node_id': 'b4b7ff10-47f0-40e8-bf26-8f1d86e12b27', 'nametag': 'Plain', 'num': 86, 'elist_str_to_exclude': '7b1aad0c-c3e8-4163-bfa0-b545584271f0', 'elist_epure_to_exclude': 'dcf26df7-5f9d-4453-8979-4ccf3d96f4a2', 'elist_str_no_def_val': ['no', 'definitions'], 'elist_str_def_val': ['abc', 'def'], 'elist_epure': [{'node_id': '486c198a-f421-4313-8a00-e402b3f977fe', 'str0': 'Texxxt', 'num0': 2}, {'node_id': '11570fa7-5206-4dcd-89bf-beed2faca04e', 'str0': 'Texxxt', 'num0': 2}]}, 'excluded_epure': 'bedaa95f-f6bf-4166-9327-9bae52b4c177', 'text': 'Text', 'age': 80}

    epure_from_db = inst.table.read(node_id=id1)[0]

    res_to_dict_from_epure_db = epure_from_db.to_dict(lambda_func= lambda field_name, field_value, parent_value, depth_level, args: 
                depth_level < 2 and (field_name != "excluded_epure" and field_name != "elist_str_to_exclude") and field_name != "elist_epure_to_exclude")

    assert res == res_to_dict_from_epure_db

    assert "random_none_attr" not in inst.__dict__ and res['random_none_attr'] == 3
    assert "random_none_attr" not in epure_from_db.__dict__ and res_to_dict_from_epure_db['random_none_attr'] == 3


    

def test_node_recursive_to_dict_with_collections_of_epure():

    @epure()
    class AnotherEpure:
        str3:str = "Str"
    
    @epure()
    class EpureClsSimple1:
        str0:str = "Texxxt"
        num0:int = 2

    epure_cls_simple1 = EpureClsSimple1()
    epure_cls_simple1.another_epure = AnotherEpure()

    epure_cls_simple2 = EpureClsSimple1()

    @epure()
    class EpureClsToDict3:
        nametag:str = "Plain"
        num:int = 86
        elist_str:Elist[str] = Elist[str](["abc", "def"])
        elist_epure:Elist[EpureClsSimple1] = Elist[EpureClsSimple1]([epure_cls_simple1, epure_cls_simple2])

    @epure()
    class EpureClsToDictPlain3:
        epure_cls:EpureClsToDict3
        text:str = "Text"
        age:int = 80
        # epure_dict:NoneType = {"abc":AnotherEpure(), "gvd":AnotherEpure()}
        epure_list:NoneType = [AnotherEpure(), AnotherEpure(), AnotherEpure()]
        # epure_set:NoneType = (AnotherEpure(), AnotherEpure())

    inst = EpureClsToDictPlain3()
    inst.epure_cls = EpureClsToDict3()

    id1 = inst.save().node_id

    epure_from_db = inst.table.read(node_id=id1)[0]

    res = epure_from_db.to_dict()

    assert res["epure_list"] == [{'str3': 'Str'}, {'str3': 'Str'}, {'str3': 'Str'}]