
from typing import Any
from .query import Query
from .make import Make


class Epure(type):


    def __new__(mcls, cls, cls_with_methods=None, *, store=None):

        if type(cls) is Epure:
            return cls

        name, bases, attrs = cls.__name__, cls.__bases__, cls.__dict__

        methods = ('save', 'find', 'put', 'out')
        if not all(hasattr(cls, foo_name)
        and callable(getattr(cls, foo_name)) for foo_name in methods):
            if not cls_with_methods:
                not_implemented = set(methods).difference(dir(cls))
                raise EpureProtocolException(f'{not_implemented} must be implemented')
            else:
                bases = [*bases, cls_with_methods]


        for atr_name in dir(cls):
            value = getattr(cls, atr_name, None)
            mcls.on_setattr(cls.__name__, atr_name, value)

        res = super().__new__(mcls, name, tuple(bases), dict(attrs))
        if store:
            res._store = store

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



    def on_setattr(epure_name: str, atr_name: str, value: Any):
        if atr_name[:3] != "___" or atr_name[-3:] != "___":
            return

        print(f'on_setattr {epure_name}, {atr_name}, {value}')
        

class EpureProtocolException(Exception):
    pass

def epure(store_=None) -> Any:
    def epure_creator(cls):
        return Epure(cls, Make, store=store_)
    return epure_creator