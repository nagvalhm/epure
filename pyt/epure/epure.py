from __future__ import annotations
from typing import Any, Dict, Tuple

from .node.filenode import FileNode
from .query import Query
from .node import Node # type: ignore


class Epure(type):

    def __new__(mcls, name: str, cls_bases: Tuple[type, ...], 
        namespace: dict[str, Any], **kwds: Any) -> Epure:
       
        cls = kwds.get('cls', None)
        node_cls = kwds.get('node_cls', None)
        storage = kwds.get('storage', None)

        if type(cls) is Epure:
            raise TypeError(f'{cls} is Epure')

        if node_cls:
            cls_bases = mcls._add_node_cls(node_cls, cls, cls_bases)
        
        res = super().__new__(mcls, name, cls_bases, dict(namespace))
        if storage:
            res._storage = storage

        for atr_name in dir(res):
            value = getattr(res, atr_name, None)
            mcls.on_setattr(name, atr_name, value)

        if cls:
            del cls

        return res

    def _add_node_cls(node_cls:type, cls:type, cls_bases:Tuple[type, ...]) -> Tuple[type, ...]:
        if not node_cls:
            return cls_bases
            
        is_node_child = True
        if cls:
            is_node_child = issubclass(cls, node_cls)
        else:
            mro = set(cls_bases).copy()
            for base in cls_bases:
                mro.union(base.mro())
            is_node_child = node_cls in mro

        if not is_node_child:
            bases = list(cls_bases)
            if object in bases:
                bases.remove(object)
            bases.append(node_cls)
            cls_bases = tuple(bases)

        return cls_bases
    


    def __init__(*args:Any, **kwargs:Any):
        pass



    def __setattr__(cls, atr_name: str, value: Any) -> None:
        mcls = type(cls)
        mcls.on_setattr(cls.__name__, atr_name, value)
        return super().__setattr__(atr_name, value)


    @staticmethod
    def on_setattr(epure_name: str, atr_name: str, value: Any) -> None:
        if atr_name[:3] != "___" or atr_name[-3:] != "___":
            return

        print(f'on_setattr {epure_name}, {atr_name}, {value}')
        

class NodeException(Exception):
    pass

def epure(_node_cls:Any=Node, _storage:Any=None) -> Any:
    def epure_creator(_cls:type) -> type:
        return Epure(_cls.__name__, _cls.__bases__, _cls.__dict__, cls=_cls, node_cls=_node_cls, storage=_storage)
    return epure_creator

# def file_epure(storage_:Any=None) -> Any:
#     def epure_creator(cls:type) -> type:
#         return Epure(cls, FileNode, storage=storage_)
#     return epure_creator

# Epure = Epure(Epure, Node)