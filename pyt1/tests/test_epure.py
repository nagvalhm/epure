from __future__ import annotations

# from ..epure.epure import Epure, epure
# from epure import connect

# from ..epure.epure import Epure, epure, connect
from typing import List, Dict
from datetime import datetime
import pytest
import types
from .epure_classes import *
import psycopg2
import psycopg2.extras
import random
from uuid import uuid4

def get_epure(cls):
    epure = cls()
    id = epure.save().node_id
    res = epure.table.read(node_id=id)

    # initial_epure_json = epure.table._serialize(epure)
    # res_json = epure.table._serialize(res[0][0])

    # assert res[0][0] == epure
    # assert initial_epure_json == res_json
    
    assert res[0][0].annotations == epure.annotations
    return res

def table_exists(table_name):
    result = []
    with psycopg2.connect(dbname="postgres", user="postgres", 
            password="postgres", host="localhost", port=5432) as connection:
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(f'select * from {table_name}')
            if cursor.rowcount > 0:
                result = cursor.fetchall()
    return result

@pytest.fixture
def epure_class1():
    res = EpureClass1()
    # res.str2 = 'str2'
    res.int2 = 1111
    res.float2 = 3.14
    res.complex2 = 3.14 + 2.7j
    res.list2 = [1, 2, 3]
    res.tuple2:tuple = (1, 2, 3)

    return res

@pytest.fixture
def epure_class2(epure_class1):
    res = EpureClass2()
    res.epure_class = epure_class1
    res.range2 = range(0, 10)
    res.dict2 = {'val1': 'val1', 4:5}
    res.set2 = {1, 3, 6}
    res.frozenset2 = {1, 3, 6}
    res.bool2 = True
    res.bytes2 = bytes('epure_class2.bytes', 'utf8')

    return res

@pytest.fixture
def epure_class3(epure_class2):
    res = EpureClass3()
    res.epure_class = epure_class2

    res.bytearray2 = bytearray('epure_class3.bytearray' , 'utf8')
    # memoryview2:memoryview
    res.NoneType2 = 'NoneType2'
    res.none2 = 'none2'
    res.generic_dict2 = {4:'val1', 'val2':5}
    res.generic_list2 = [1, '2', 3.14]
    res.lambda_field2 = lambda y: y

    return res

@pytest.fixture
def regular_class3():
    res = RegularClass3()
    # res.regular_class:RegularClass2

    res.bytearray1 = bytearray('regular_class3.bytearray', 'utf8')
    # res.memoryview1 = memoryview()
    res.NoneType1 = 'NoneType1'
    res.none1 = 'none1'
    res.generic_dict1 = {4:'5d', 'sdf':7}
    res.generic_list1 = [4, 'dff']
    res.lambda_field1 = lambda x: x

    return res

@pytest.fixture
def default_epure(regular_class3, epure_class3, epure_class1):
    epure = DefaultEpure()
    epure.float3 = random.uniform(0.0, 1000000.0)
    epure.range0 = range(1, 10)
    epure.dict0 = {'field1': 'val1', 'field2': 3}
    epure.set0 = {'set_val1', 3, 13.4}
    epure.frozenset0 = frozenset([1, '2', 3.14])
    epure.bool0 = True
    epure.bytes0 = bytes(10)
    epure.epure_class2 = uuid4()

    epure.regular_class = regular_class3
    epure.epure_class = epure_class3
    epure.epure_class1 = epure_class1

    epure.with_out_hint = True

    id = epure.save().node_id
    res = epure.table.read(node_id=id)

    # orig_json = epure.to_json()
    # res_json = res[0][0].to_json()

    orig_json = epure.to_dict()
    res_json = res[0][0].to_dict()
    
    # assert orig_json == res_json

    # res = epure.table.read(int3=6, str3="str3_value")

    assert not hasattr(res[0][0], "with_out_hint")
    assert res[0][0].node_id == epure.node_id
    return res

def test_default_epure_table(default_epure):
    assert default_epure[0][0].table.name == 'default_epure'
    assert default_epure[0][0].table.db.__class__.__name__ == 'GresDb'
    assert table_exists('default_epure')

def test_default_epure_fields(default_epure):
    pass


def test_default_epure_fields_in_correct_tables():
    pass

@pytest.fixture
def aliased_epure():
    return get_epure(AliasedEpure)

# @pytest.fixture
# def aliased_epure():
#     return get_epure(EpureClass4)

def test_aliased_epure_fields(aliased_epure):
    pass

def test_aliased_epure_table(aliased_epure):
    assert aliased_epure[0][0].table.full_name == 'public.aliased_table'
    assert aliased_epure[0][0].table.db.database == 'postgres'
    assert table_exists('public.aliased_table')

def test_aliased_epure_fields_in_correct_tables():
    pass

# @pytest.fixture
# def custom_save_epure():
#     epure = CustomSaveEpure()
#     id = epure.save()
#     assert id == 65
#     res = epure.table.read(id=id)   
#     return res

# def test_custom_save_fields(custom_save_epure):
#     pass

# def test_custom_save_table(custom_save_epure):
#     assert custom_save_epure.table.name == 'prefix.aliasedtable'
#     assert default_epure.db.name == 'GresDb'
#     assert table_exists('prefix.aliasedtable')

# def test_custom_save_fields_in_correct_tables():
#     pass



# #test exceptions
# def test_not_null_column_not_accept_null():
#     pass

# def test_not_null_column_must_have_default():
#     pass

# def test_not_typed_fields_not_saved():
#     pass

# def test_excluded_fields_not_saved():
#     pass