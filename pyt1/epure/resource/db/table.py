from __future__ import annotations
from types import LambdaType, NoneType
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast
from ..savable import Savable
import inspect
from .pseudo_table import PresudoTable, PseudoDb
from .select_query import SelectQuery
from .constraint import Constraint
from ..resource import Resource
from ..node.node import Node

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

    @property
    def db(self):
        return self.resource

    def __init__(self, name: str,
            header:Union[TableHeader, Dict[str, Any]]=None, resource:Resource=None, namespace:str = '') -> None:        
        check_type('header', header, [TableHeader, dict, NoneType])
        

        self._set_header(header)

        super().__init__(name, namespace, resource)


    def _serialize(self, node: Savable) -> Dict[str, str]:
        res = {}
        for field_name, field_type in node.annotations.items():
            if isinstance(field_type, Constraint):
                field_type = field_type.py_type
                
            if node.is_excluded(field_name, field_type):
                continue
            if field_name not in self.header:
                continue

            field_val = getattr(node, field_name, None)
            #working for db:
            if isinstance(field_val, Savable):
                field_type = field_val.annotations['node_id']
                field_val = field_val.save(True).node_id
                
            field_val = self.db.cast_py_db_val(field_type, field_val)

            res[field_name] = field_val
        
        return res



    def create(self, node: Node, asynch:bool=False) -> object:
        node.node_id = self.generate_id()
        script = self.serialize_for_create(node)
        if asynch:
            self.cache(script)
        else:
            self.execute(script)
        return node


    def read(self, selector: object = None, **kwargs) -> Any: #Union[Resource, Sequence[Resource]]:
        if selector == None:
            return self.read_by_fields(**kwargs)
        if isinstance(selector, str):
            return self.execute(selector)
        if not callable(selector):
            raise NotImplementedError(f'couldn read by object of type {type(selector)}')


        if inspect.ismethod(selector):
            def reader(self:Table, *args, **kwargs):
                pseudo_self = PresudoTable(self)
                pseudo_db = PseudoDb(self.db)
                script = selector(pseudo_self, pseudo_db, *args, **kwargs)
                return self.execute(selector)
            setattr(self, selector.__name__, reader)

        pseudo_self = PresudoTable(self)
        pseudo_db = PseudoDb(self.db)
        script = selector(pseudo_self, pseudo_db)
        res = self.execute(script)
        return res


    def update(self, node: Savable, asynch:bool=False) -> object:
        script = self.serialize_for_update(node)
        if asynch:
            self.cache(script)
        else:
            self.execute(script)
        return node


    def cache(self, script: str):        
        self.db.cache_queue.append(script)


    def _set_header(self, header):
        if header == None:
            header = TableHeader(table=self)
        
        if isinstance(header, Dict):
            header = TableHeader(columns=header, table=self)
        
        self.header = header
        self.header.resource = self
       
    def serialize_for_create(self, node: Savable, **kwargs) -> object:
        raise NotImplementedError

    def serialize_for_read(self, node: Savable, **kwargs) -> object:
        raise NotImplementedError

    def serialize_for_update(self, node: Savable, **kwargs) -> object:
        raise NotImplementedError

    def serialize_for_delete(self, node: Savable, **kwargs) -> object:
        raise NotImplementedError

    
    def serialize_header(self, db: TableStorage=None, **kwargs) -> List[Dict[str, str]]:
        res: List[Dict[str, str]] = list()

        if db == None:
            db = self.db

        if db == None:
            raise EpureError('undefined db for header serialization')
        
        header = self.header
        for column_name in header:
            column = header[column_name]
           
            serialized = {
                "column_name": column.name,
                "column_type": column.serialize_type(db) #db.get_db_type(column.column_type)
            }
            res.append(serialized)
        return res