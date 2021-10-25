
from typing import Any


def foo(self):
    return 2

class Epure(type):

    def __new__(mcls, epure_name, bases, attrs):
        for atr_name, value in attrs.items():
            mcls.on_setattr(epure_name, atr_name, value)
        
        for foo_name in ('add', 'get', 'exec'):
            if foo_name not in attrs.keys():
                attrs[foo_name] = getattr(mcls, foo_name)
        
        return super().__new__(mcls, epure_name, bases, attrs)

    def __init__(cls, cls_name, bases, attrs):

        for foo_name in ('add', 'get', 'exec'):
            foo = getattr(cls, foo_name)            
            setattr(cls, foo_name, classmethod(foo))

        return super().__init__(cls_name, bases, attrs)

    def __setattr__(cls, atr_name: str, value: Any) -> None:
        mcls = type(cls)
        mcls.on_setattr(cls.__name__, atr_name, value)
        return super().__setattr__(atr_name, value)

    def on_setattr(epure_name: str, atr_name: str, value: Any):
        print('on_setattr', epure_name, atr_name, value)
        pass

    def add(cls, make):
        print('add is called')

    def get(cls):
        print('get is called')

    def exec(cls, query):
        print('exec is called')

class Query:
    __exec__
    __query__
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

def epure(storage, execute: callable=None) -> Any:

    def epure_creator(cls):
        if type(cls) is Epure:
            return cls

        attrs = dict(cls.__dict__)        
        attrs['_storage'] = storage
        if execute:
            #type check
            if not callable(execute):
                raise Exception('execute must be callable')
            attrs['exec'] = execute

        res = Epure(cls.__name__, cls.__bases__, attrs)
        del cls
        # try:
        #     res = Epure(cls.__name__, cls.__bases__, cls.__dict__)
        # except Exception:
        #     raise Exception

        return res
    return epure_creator