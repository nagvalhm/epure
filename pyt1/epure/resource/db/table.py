from types import LambdaType, NoneType
from typing import *
from .db import Db
from ..savable import Savable
from ...helpers.type_helper import check_type


class TableColumn(Savable):
    column_type:type
    
    def __init__(self, name:str, column_type:type=NoneType) -> None:
        self.column_type = column_type
        super().__init__(name)

class TableHeader(Savable):
    columns:Dict[str,TableColumn]

    def __init__(self, 
            columns:Dict[str,TableColumn]=None, 
            name: str = '', res_id: object = None) -> None:

        self.columns = columns if columns else {}
        super().__init__(name, res_id)

    def __setitem__(self, key:str, column:TableColumn):
        if type(column) != TableColumn:
            raise TypeError('only TableColumn can be added to table header')
        self.columns[key] = column

    def __getitem__(self, key:str):
        return self.columns[key]

    def keys(self):
        return self.columns.keys()


class Table(Savable):
    header:TableHeader
    resource:Db    

    def __init__(self, name: str = '', header:TableHeader=None, res_id: object = None) -> None:
        self.header = header if header else TableHeader()
        self.header.resource = self
        super().__init__(name, res_id)



class IndexedTypeMeta(type):
    def __getitem__(cls:Type, param:Any):
        cls.__param__ = param
        return cls

class NotNull(metaclass=IndexedTypeMeta):
    __param__:type

class Id(metaclass=IndexedTypeMeta):
    __param__:type

class Uniq(metaclass=IndexedTypeMeta):
    __param__:type

class Check(metaclass=IndexedTypeMeta):
    __param__:type
    __condition__:Callable
    def __class_getitem__(cls, param:Any, condition:Callable):
        cls.__param__ = param
        cls.__condition__ = condition
        return cls