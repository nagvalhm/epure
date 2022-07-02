from types import NoneType
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

    def __init__(self, columns:Dict[str,TableColumn]=None, name: str = '', res_id: object = None) -> None:
        self.columns = columns if columns else {}
        super().__init__(name, res_id)

    def __setitem__(self, key:str, column:TableColumn):
        if type(column) != TableColumn:
            raise TypeError('only TableColumn can be added to table header')
        self.columns[key] = column

    def __getitem__(self, key:str):
        return self.columns[key]


class Table(Savable):
    header:TableHeader
    resource:Db

    def __init__(self, name: str = '', header:TableHeader=None, res_id: object = None) -> None:
        self.header = header if header else TableHeader()
        self.header.resource = self
        super().__init__(name, res_id)


T = TypeVar('T')
class NotNullMeta(type, Generic[T]):
    def __getitem__(cls, param:Any):
        cls.__param__ = param
        return cls

class NotNull(metaclass=NotNullMeta):
    __param__:type

    # def __class_getitem__(cls, param:Any):
    #     cls.__param__ = param
    #     return cls