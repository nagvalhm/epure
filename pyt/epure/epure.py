
from typing import Any
from .query import Query
from .node import Node


class Epure(type):


    def __new__(mcls, cls, protocol_cls=None, *, storage=None):

        if type(cls) is Epure:
            return cls


        methods = ('save', 'find', 'put', 'search')
        for foo_name in methods:
            if not (hasattr(cls, foo_name) and callable(getattr(cls, foo_name))):
                if not protocol_cls:
                    raise NodeException(f'{foo_name} must be implemented')
                else:
                    val = getattr(protocol_cls, foo_name)
                    setattr(cls, foo_name, val)
                    

        for atr_name in dir(cls):
            value = getattr(cls, atr_name, None)
            mcls.on_setattr(cls.__name__, atr_name, value)


        res = super().__new__(mcls, cls.__name__, cls.__bases__, dict(cls.__dict__))
        if storage:
            res._storage = storage

        del cls

        return res



    def __init__(*args, **kwargs):
        pass
        # cls, cls_name, bases, attrs
        # execute = getattr(cls, 'exec')
        # setattr(cls, 'exec', staticmethod(execute))
        # for foo_name in ('save', 'take'):
        #     foo = getattr(cls, foo_name)            
        #     setattr(cls, foo_name, Query(foo, execute))

        # return super().__init__(*args, **kwargs)



    def __setattr__(cls, atr_name: str, value: Any) -> None:
        mcls = type(cls)
        mcls.on_setattr(cls.__name__, atr_name, value)
        return super().__setattr__(atr_name, value)


    @staticmethod
    def on_setattr(epure_name: str, atr_name: str, value: Any):
        if atr_name[:3] != "___" or atr_name[-3:] != "___":
            return

        print(f'on_setattr {epure_name}, {atr_name}, {value}')
        

class NodeException(Exception):
    pass

def epure(storage_=None) -> Any:
    def epure_creator(cls):
        return Epure(cls, Node, storage=storage_)
    return epure_creator

# Epure = Epure(Epure, Node)