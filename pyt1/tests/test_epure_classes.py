from __future__ import annotations
from ..epure.epure import epure, connect
from ..epure.resource.db.table import NotNull
from typing import List, Dict
from datetime import datetime
import pytest
import types

#parent
class ParentClass1:
    str:NotNull[str]
    int:int = 5
    float:float
    complex:complex
    list:list
    tuple:tuple


class ParentClass2(ParentClass1):
    range:range
    dict:dict
    set:set
    frozenset:frozenset
    bool:bool
    bytes:bytes

class ParentClass3(ParentClass1):
    bytearray:bytearray
    memoryview:memoryview
    NoneType:types.NoneType
    none:None
    generic_dict:Dict[int, str]
    generic_list:List[int]
    lambda_field:types.LambdaType



#regular fields
@epure()
class SeparatedEpure1:
    str1:str
    int1:int
    float1:float
    complex1:complex
    list1:list
    tuple1:tuple

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
    str2:str
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
    regular_class:RegularClass3
    epure_class:EpureClass3

    str3:str
    int3:int
    float3:float
    complex3:complex
    list3:list
    tuple3:tuple

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