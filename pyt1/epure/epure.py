from __future__ import annotations
from types import NoneType
from typing import cast, Callable
from .resource.resource import Resource
from .helpers.type_helper import check_type
from .errors import EpureError

from .resource.db.table import Table
# from types import FunctionType
from ..epure.resource.node.node import TableNode
from .resource.savable import Savable
from .resource.db.db import Db



def connect(edb:Db) -> None:
    Epure.EDb = edb

class Epure(type, Savable):

    EDb:Db
    
    # def __new__(mcls, name: str, cls_bases: Tuple[type, ...], namespace: dict[str, Any]) -> Epure:
    #     return super().__new__(mcls, name, cls_bases, namespace)    
    
    def save_epure(cls, level:int=0, resource:object=None):

        check_type('resource', resource, [str, Savable, NoneType])

        if type(resource) == Savable:
            resource = cast(Savable, resource)
            if not hasattr(resource, 'resource'):
                raise EpureError('For using savable as resource for epure, savable must have own resource')
            grandpa = resource.resource
            grandpa.update(cls, resource.res_id)
        else:
            table_name = resource if resource else cls.__name__            
            resource = cls._create_or_update(str(table_name))

        cls.resource = resource

    def _create_or_update(cls, table_name:str) -> Table:
        table = cls.EDb.get_table_for_resource(cls, table_name)
        if table_name in cls.EDb:
            return cls.EDb.update(table)
        else:
            return cls.EDb.create(table)


def epure(resource:object='', saver:type=TableNode, epure_metaclass:type=Epure) -> Callable:
    
    def epure_creator(cls:type) -> Epure:
        epure_cls = _create_epure(cls, saver, epure_metaclass)
        epure_cls.save_epure(resource=resource)

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

