from __future__ import annotations
from types import LambdaType, NoneType
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast

if TYPE_CHECKING:
    from .table_storage import TableStorage
from .db_entity import DbEntity
from ...helpers.type_helper import check_type
from ...errors import EpureError
from .table_header import TableHeader


class Table(DbEntity):
    header:TableHeader
    if TYPE_CHECKING:
        resource:TableStorage

    def __init__(self, name: str,
            header:Union[TableHeader, Dict[str, Any]]=None, namespace:str = '') -> None:        
        check_type('header', header, [TableHeader, dict, NoneType])
        

        self._set_header(header)

        super().__init__(name, namespace=namespace)



    def _set_header(self, header):
        if header == None:
            header = TableHeader(table=self)
        
        if isinstance(header, Dict):
            header = TableHeader(columns=header, table=self)
        
        self.header = header
        self.header.resource = self
       

    @property
    def db(self):
        return self.resource

    
    def serialize_header(self, db: TableStorage=None, **kwargs) -> List[Dict[str, str]]:
        res: List[Dict[str, str]] = list()

        if not db:
            db = self.db

        if not db:
            raise EpureError('undefined db for header serialization')
        
        header = self.header
        for column_name in header:
            column = header[column_name]
            # serialized = header.serialize(column, db=db)
            serialized = {
                "column_name": column.name,
                "column_type": db.get_db_type(column.column_type)
            }
            res.append(serialized)
        return res