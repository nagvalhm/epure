from __future__ import annotations
from types import LambdaType, NoneType
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast
if TYPE_CHECKING:
    from .db import Db
from ..savable import Savable
from ...helpers.type_helper import check_type
from ..resource import Resource
from inflection import underscore


class TableColumn(Savable):
    column_type:str
    
    def __init__(self, name:str, column_type:str='') -> None:
        self.column_type = column_type
        super().__init__(name)

class TableHeader(Savable):
    columns:Dict[str,TableColumn]

    def __init__(self, 
            columns:Dict[str, Any]=None,
            name: str = '', res_id: object = None) -> None:
        check_type('columns', columns, [dict, NoneType])

        self.columns = {}
        super().__init__(name, res_id)
        if not columns:
            return

        for name, val in columns.items():
            if isinstance(val, str):
                val = TableColumn(name, val)
            val = cast(TableColumn, val)
            self.columns[name] = val

        

    def __setitem__(self, key:str, column:TableColumn):
        check_type('column', column, [TableColumn])
        self.columns[key] = column

    def __getitem__(self, key:str):
        return self.columns[key]

    def keys(self):
        return self.columns.keys()


class Table(Savable):
    header:TableHeader
    resource:Db

    def __init__(self, name: str = '', 
            header:Union[TableHeader, Dict[str, Any]]=None, res_id: object = None) -> None:        
        check_type('header', header, [TableHeader, dict, NoneType])

        if header == None:
            header = TableHeader()
        
        if isinstance(header, Dict):
            header = TableHeader(columns=header)


        self.header = header
        self.header.resource = self
        super().__init__(name, res_id)

    @property
    def db(self):
        return self.resource

    
    def get_scheme(self, db: Db) -> List[Dict[str, str]]:
        res: List[Dict[str, str]] = list()
        
        columns_items = self.header.columns.items()
        for column_name, column in columns_items:
            res.append({
                "column_name": underscore(column_name),
                "column_type": db.get_db_type(column.column_type)
            })

        return res



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