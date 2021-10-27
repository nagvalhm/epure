
from typing import Any
from query import Query
from make import Make

# import tests
# print(tests.test_foo)
# print(tests.__dict__)

class Epure(type):

    def __new__(mcls, cls):

        
        
        return super().__new__(mcls, cls.__name__, cls.__bases__, cls.__dict__)

    # def __new__(mcls, epure_name, bases, attrs):
    #     for atr_name, value in attrs.items():
    #         mcls.on_setattr(epure_name, atr_name, value)
        
    #     for foo_name in ('save', 'take', 'put', 'find'):
    #         if foo_name not in attrs.keys():
    #             raise EpureProtocolException(f'{foo_name} must be implemented')                
        
    #     return super().__new__(mcls, epure_name, bases, attrs)



    def __init__(cls, cls_name, bases, attrs):

        execute = getattr(cls, 'exec')
        setattr(cls, 'exec', staticmethod(execute))
        for foo_name in ('save', 'take'):
            foo = getattr(cls, foo_name)            
            setattr(cls, foo_name, Query(foo, execute))

        return super().__init__(cls_name, bases, attrs)



    def __setattr__(cls, atr_name: str, value: Any) -> None:
        mcls = type(cls)
        mcls.on_setattr(cls.__name__, atr_name, value)
        return super().__setattr__(atr_name, value)



    def on_setattr(epure_name: str, atr_name: str, value: Any):
        print('on_setattr', epure_name, atr_name, value)
        pass

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