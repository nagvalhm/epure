from __future__ import annotations
from typing import Any

from .node.filenode import FileNode
from .query import Query
from .node import Node # type: ignore


class Epure(type):


    def __new__(mcls, cls:type, node_cls:type=Node, *, storage:Any=None) -> Epure:

        if type(cls) is Epure:
            return cls

        cls_bases = cls.__bases__
        if not issubclass(cls, node_cls):
            bases = list(cls_bases)
            bases.append(node_cls)
            cls_bases = tuple(bases)

        for atr_name in dir(cls):
            value = getattr(cls, atr_name, None)
            mcls.on_setattr(cls.__name__, atr_name, value)


        res = super().__new__(mcls, cls.__name__, cls_bases, dict(cls.__dict__))
        if storage:
            res._storage = storage

        del cls

        return res



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

def epure(node_cls:Any=Node, storage_:Any=None) -> Any:
    def epure_creator(cls:type) -> type:
        return Epure(cls, node_cls, storage=storage_)
    return epure_creator

# def file_epure(storage_:Any=None) -> Any:
#     def epure_creator(cls:type) -> type:
#         return Epure(cls, FileNode, storage=storage_)
#     return epure_creator

# Epure = Epure(Epure, Node)