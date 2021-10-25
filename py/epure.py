
from typing import Any


def foo(self):
    return 2

class Epure(type):
    def __new__(mcls, cls_name, bases, attrs):
        for atr_name, value in attrs:
            mcls.on_setattr(atr_name, value)
        return super().__new__(mcls, cls_name, bases, attrs)

    def __init__(cls, cls_name, bases, attrs):

        return super().__new__(cls, cls_name, bases, attrs)

    def __setattr__(mcls, atr_name: str, value: Any) -> None:
        mcls.on_setattr(atr_name, value)
        return super().__setattr__(atr_name, value)

    def on_setattr(mcls, atr_name: str, value: Any):
        print('on_setattr', atr_name, value)
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

@epure('stror', 'as')
class A():
    a_filed = 1

    def __setattr__(self, name: str, value: Any) -> None:
        print('hi5')
        return super().__setattr__(name, value)

A.a_filed
print(A._storage)
