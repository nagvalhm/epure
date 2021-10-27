
from typing import Any
from .query import Query
from .make import Make


class Epure(type):


    def __new__(mcls, cls, make=None):    

        name, bases, attrs = cls.__name__, cls.__bases__, cls.__dict__

        methods = ('save', 'take', 'put', 'find')
        if any(not hasattr(cls, foo_name) for foo_name in methods):
            if not make:
                not_implemented = set(methods).difference(dir(cls))
                raise EpureProtocolException(f'{not_implemented} must be implemented')
            else:
                bases = [*bases, make]


        for atr_name in dir(cls):
            value = getattr(cls, atr_name, None)
            mcls.on_setattr(cls.__name__, atr_name, value)  

        res = super().__new__(mcls, name, tuple(bases), dict(attrs))
        del cls

        return res



    def __init__(*args, **kwargs):
        print(1)
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

def epure(storage) -> Any:

    def epure_creator(cls):
        if type(cls) is Epure:
            return cls      
        

        # attrs = dict(cls.__dict__)        
        # attrs['_storage'] = storage
        res = None
        try:
            res = Epure(cls)
            # res = Epure(cls.__name__, cls.__bases__, cls.__dict__)
        except EpureProtocolException:
            # cls.__bases__ = cls.__bases__ + (Make,)
            res = Epure(cls.__name__, [*cls.__bases__, Make], cls.__dict__)

        del cls
        # try:
        #     res = Epure(cls.__name__, cls.__bases__, cls.__dict__)
        # except Exception:
        #     raise Exception

        return res
    return epure_creator