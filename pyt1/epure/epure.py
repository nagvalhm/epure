from __future__ import annotations
from typing import *
from .resource.resource import Resource

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
    
    def save_epure(cls, level:int=0, resource:Resource=None):

        if not (isinstance(resource, str) or isinstance(resource, Savable)):
            raise TypeError('epure resource type must be table name (str) or Savable')

        if type(resource) == Savable:
            resource = cast(Savable, resource)
            grandpa = resource.resource
            grandpa.update(cls, resource.res_id)
        else:
            table_name = resource if resource else cls.__name__
            resource = cls._create_or_update(str(table_name))

        cls.resource = resource

    def _create_or_update(cls, table_name:str) -> Table:
        if table_name in cls.EDb:
            return cls.EDb.update(cls, table_name)
        else:
            return cls.EDb.create(cls, table_name)


def epure(resource:object='', saver:type=TableNode, epure_metaclass:type=Epure) -> Callable:
    
    def epure_creator(cls:type) -> Epure:
        epure_cls = _create_epure(cls, saver, epure_metaclass)
        epure_cls.save_epure(0, resource)
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

