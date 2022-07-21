from __future__ import annotations
from ..epure.epure import epure, connect
from ..epure.resource.gres.gres_db import GresDb
from ..epure.resource.db.constraint import NotNull, Check, Prim, Uniq, Default
from typing import List, Dict, Tuple, Callable
from datetime import datetime
import pytest
import types

try:
    connect(GresDb('postgres://user_name:pass@host:5432'))
except Exception as ex:
    print(ex)

connect(GresDb('postgres://postgres:postgres@localhost:5432'))

db = GresDb('postgres://postgres:postgres@localhost:32', 
    # host="localhost", 
    port="5432", 
    # database="postgres", 
    # user="postgres", 
    password="postgres",
    log_level=3)
connect(db)

#parent
class ParentClass1:
    str0:Default[str] = 'str0_value'
    int0:Default[int] = 11
    float0:Default[float] = 1.4
    complex0:Default[complex] = 5 + 7j
    list0:list
    tuple0:tuple


class ParentClass2(ParentClass1):
    range0:range
    dict0:dict
    set0:set
    frozenset0:frozenset
    bool0:bool
    bytes0:bytes
    int0:Uniq[str] = 'uniq_str'

class ParentClass3(ParentClass2, ParentClass1):
    bytearray0:bytearray
    memoryview0:memoryview
    NoneType0:types.NoneType
    none0:None
    generic_dict0:Dict[int, str]
    generic_list0:List[int]
    generic_tuple0:Tuple[int]
    lambda_field0:types.LambdaType
    str3:NotNull[int] = 6



#regular fields
@epure()
class SeparatedEpure1:
    str1:str = None
    int1:Default[int] = 7
    float1:NotNull[float] = 3.14
    complex1:Uniq[complex]
    list1:list
    tuple1:tuple
    no_type = None
    

class RegularClass2:
    separated_epure1:SeparatedEpure1

    range1:range
    dict1:dict
    set1:set
    frozenset1:frozenset
    bool1:bool
    bytes1:bytes

class RegularClass3:
    regular_class:RegularClass2

    bytearray1:bytearray
    memoryview1:memoryview
    NoneType1:types.NoneType
    none1:None
    generic_dict1:Dict[int, str]
    generic_list1:List[int]
    lambda_field1:types.LambdaType

#epure fields
@epure()
class EpureClass1:
    str2:str = 'EpureClass1.str2'
    int2:int
    float2:float
    complex2:complex
    list2:list
    tuple2:tuple

@epure()
class EpureClass2:
    epure_class:EpureClass1

    range2:range
    dict2:dict
    set2:set
    frozenset2:frozenset
    bool2:bool
    bytes2:bytes

@epure()
class EpureClass3:
    epure_class:EpureClass2

    bytearray2:bytearray
    memoryview2:memoryview
    NoneType2:types.NoneType
    none2:None
    generic_dict2:Dict[int, str]
    generic_list2:List[int]
    lambda_field2:types.LambdaType



#epures
@epure()
class DefaultEpure(ParentClass3):
    str3:Default[str] = 'str3_value'
    int3:NotNull[int] = 6
    float3:Uniq[float]
    complex3:complex = None
    list3:list
    tuple3:tuple

    regular_class:RegularClass3
    epure_class:EpureClass3

    def __init__(self):
        pass

@epure('prefix.AliasedTable')
class AliasedEpure:
    regular_class:RegularClass3
    epure_class:EpureClass3

    range3:range
    dict3:dict
    set3:set
    frozenset3:frozenset
    bool3:bool
    bytes3:bytes

    def __init__(self):
        pass

@epure()
class CustomSaveEpure:
    regular_class:RegularClass3
    epure_class:EpureClass3

    bytearray3:bytearray
    memoryview3:memoryview
    NoneType3:types.NoneType
    none3:None
    generic_dict3:Dict[int, str]
    generic_list3:List[int]
    lambda_field3:types.LambdaType

    def save(self):
        id = self.db.execute('select 65')
        self.db.execute('insert into ... (...65...)')
        return id

    def __init__(self):
        pass


def test_test():
    pass