from __future__ import annotations
from types import NoneType
from typing import cast, Callable, List, Any, get_type_hints, Dict
from .resource.resource import Resource
from .helpers.type_helper import check_type
from .errors import EpureError, DefaultConstraintError
from .resource.db.constraint import Foreign, Default, Constraint

from .resource.db.table import Table
# from types import FunctionType
from ..epure.resource.node.node import TableNode
from .resource.savable import Savable
from .resource.db.db import Db
from .resource.db.db_entity import DbEntity
import functools



def connect(edb:Db) -> None:
    Epure.EDb = edb

class Epure(type, Savable):
    
    EDb:Db
    epures:List[Epure] = []
    # annotations:Dict[str,Any]
    resource:Savable
    prepared_resource:object
    
    # def __new__(mcls, name: str, cls_bases: Tuple[type, ...], namespace: dict[str, Any]) -> Epure:
    #     return super().__new__(mcls, name, cls_bases, namespace)    
    
    def __call__(self, *args, **kwargs):
        if not self.is_saved:
            self.save_epure()
            self.is_saved = True
            
        return super(Epure, self).__call__(*args, **kwargs)

    #decorator
    @classmethod
    def read(cls, method):
        querying_proxy = None
        resource_proxy = None
        if getattr(cls, 'resource', None):
            querying_proxy = getattr(cls.resource, 'querying_proxy', None)
            resource_proxy = getattr(cls.resource, 'resource_proxy', None)
        @functools.wraps(method)
        def wrap(self, *args, **kwargs):
            if querying_proxy and resource_proxy:
                return method(self, querying_proxy, resource_proxy, *args, **kwargs)
            if querying_proxy:
                return method(self, querying_proxy, *args, **kwargs)
            if resource_proxy:
                return method(self, resource_proxy, *args, **kwargs)
            return method(self, *args, **kwargs)
        return wrap
        # def reader(self:Table, *args, **kwargs):
        #     pseudo_self = PresudoTable(self)
        #     pseudo_db = PseudoDb(self.db)
        #     script = selector(pseudo_self, pseudo_db, *args, **kwargs)
        #     return self.execute(selector)
        # setattr(self, selector.__name__, reader)

    def prepare_save(self, resource:object):        
        self.__class__.epures.append(self)
        self.prepared_resource = resource


    def save_epure(self):

        resource = self.prepared_resource
        check_type('resource', resource, [str, Savable, NoneType])

        if type(resource) == Savable:
            resource = cast(Savable, resource)
            if not hasattr(resource, 'resource'):
                raise EpureError('For using savable as resource for epure, savable must have own resource')
            grandpa = resource.resource
            grandpa.update(self)
        else:
            table_name = self._get_table_name(self, resource)
            resource = self._create_or_update(table_name)

        self.resource = resource
        
        

    def _create_or_update(self, table_name:str) -> Table:
        table:Table = self._get_table(table_name)
        res:DbEntity
        if table_name in self.EDb:
            res = self.EDb.update(table)
        else:
            res = self.EDb.create(table)
        res = cast(Table, res)
        return res

    def _get_table_name(self, cls, resource: object) -> str:
        
        if not isinstance(resource, str):
            resource = cast(Savable, resource)
            return resource.full_name

        if resource:
            return resource
        
        return self.EDb._get_full_table_name(cls.__name__).full_name

        

    def _get_table(self, table_name: str = '') -> Table:
        table:Table
        
        full_name = self.EDb._get_full_table_name(table_name)        
        columns = {}

        for field_name, py_type in self.annotations.items():
            py_type = cast(type, py_type)
            if self.is_excluded(field_name, py_type):
                continue
            py_type = self.get_py_type(field_name, py_type)
            
            columns[field_name] = py_type

        TableCls = self.EDb.default_table_type
        table = TableCls(full_name.name, columns, self.EDb, full_name.namespace)
        return table

    def get_py_type(self, field_name:str, py_type:type) -> type:
       
        if py_type in self.epures:
            py_type = cast(Epure, py_type)
            return self.get_py_type(field_name, py_type.annotations['node_id'])
            
        if isinstance(py_type, Constraint) and issubclass(py_type.__origin__, Default):
            return self.get_default_type(field_name, py_type)

        return py_type

    def get_default_type(self, field_name:str, py_type:Default) -> Any:
        default = getattr(self, field_name, None)
        if not (default or py_type.default):
            raise DefaultConstraintError(self.full_name, field_name)
        if not py_type.default:
            py_type.default = default

        if not isinstance(py_type.default, py_type.py_type):
            raise DefaultConstraintError(message=f'''field {field_name} of class {self.full_name} 
                    has wrong defaul value {py_type.default} not corresponding to {py_type.py_type} type''')

        return py_type


    def get_foreign_type(self, foreign:Epure) -> Any:
        foreign_id_type = foreign.annotations['node_id']

        foreign_table = self._get_table_name(foreign, foreign.prepared_resource)

        foreign_column = 'node_id'
        column_type = Foreign[foreign_id_type, foreign_table, foreign_column]
        return column_type


        

def epure(resource:object='', saver:type=TableNode, epure_metaclass:type=Epure) -> Callable:
    check_type('resource', resource, [str, Savable, NoneType])

    def epure_creator(cls:type) -> Epure:
        epure_cls = _create_epure(cls, saver, epure_metaclass)
        epure_cls.prepare_save(resource)

        del cls
        return epure_cls

    return epure_creator


def _create_epure(cls, saver, _Epure):
    cls_dict = dict(cls.__dict__)
    if issubclass(cls, Savable):
        return _Epure(cls.__name__, cls.__bases__, cls_dict)

    bases = list(cls.__bases__)
    if object in bases:
        bases.remove(object)
    bases.append(saver)
    return _Epure(cls.__name__, tuple(bases), cls_dict)

