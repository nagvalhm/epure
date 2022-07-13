from __future__ import annotations
from types import LambdaType, NoneType
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast
from ..savable import Savable
from ..resource import UPDATE, CREATE

if TYPE_CHECKING:
    from .table_storage import TableStorage
from .db_entity import DbEntity
from ...helpers.type_helper import check_type
from ...errors import EpureError, DbError
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



    def serialize(self, node: Savable, method: str = '', **kwargs) -> str:
        res = {}
        for field_name, field_type in node.annotations.items():
            if node.is_excluded(field_name, field_type):
                continue
            if field_name not in self.header:
                continue

            field_val = getattr(node, field_name, None)
            if isinstance(field_val, Savable):
                field_val = field_val.save(True)
            field_val = self.db.cast_py_db_val(field_type, field_val)

            res[field_name] = field_val
            
        if method == UPDATE:
            return self.serialize_update(res)
        elif method == CREATE:
            return self.serialize_create(res)
        raise DbError(f'Couldnt serialize node for method {method}')


    def create(self, node: Savable) -> object:
        script = self.serialize(node, CREATE)
        self.execute(script)

    def update(self, node: Savable) -> object:
        script = self.serialize(node, UPDATE)
        self.execute(script)

    def cache(self, node: Savable, method: str = ''):
        script = self.serialize(node, method)
        self.cache_queue.append(script)

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

    def serialize_update(self, node: Dict[str, str]) -> str:
        raise NotImplementedError

    def serialize_create(self, node: Dict[str, str]) -> str:
        raise NotImplementedError
    
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
                "column_type": column.serialize_type(db) #db.get_db_type(column.column_type)
            }
            res.append(serialized)
        return res