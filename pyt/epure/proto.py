from __future__ import annotations
from abc import abstractmethod, ABCMeta
from typing import *
import re


class MultipleInheritanceError(Exception):
    pass

class ProtoMeta(type):

    def __new__(mcl, name:str, bases:Tuple[type], namespace: dict[str, Any]) -> ProtoMeta:
        res_cls = super().__new__(mcl, name, bases, namespace)

        if name == 'Proto':
            return res_cls

        try:
            res_cls.proto_cls
        except MultipleInheritanceError:
            del res_cls
            raise

        return res_cls

    @property
    def proto_cls(cls) -> ProtoMeta:
        bases = cls.__bases__
        protos = list(filter(lambda base: issubclass(base, Proto), bases))
        if len(protos) > 1:
            raise MultipleInheritanceError(f'{cls.__name__} has more than one Proto ancestor: {protos}')
        
        if len(protos) == 0:
            raise Exception()
        res = protos[0]
        if not isinstance(res, ProtoMeta):
            raise Exception('res must be Proto')

        return res



class Proto(metaclass=ProtoMeta):
    __proto__:Proto
    __abstractclass__ = 1
    

    def __new__(cls: ProtoMeta, *args: Any, **kwargs: Any) -> Proto:
        print(f'{cls.__name__} new called')
        res = super(type, cls).__new__(cls)
        if not isinstance(res, Proto):
            raise
        # proto = res.proto()

        return res

    # @property
    def proto(self, *args: Any, **kwargs: Any) -> Proto:
        self_cls = type(self)
        if not hasattr(self, '__proto__'):
            proto_cls = self_cls.proto_cls
            if '__abstractclass__' in vars(proto_cls).keys():
                return None
            self.__proto__ = proto_cls(*args, **kwargs)
        return self.__proto__

    
    def __setattr__(self, name: str, value: Any) -> None:
        self_cls = type(self)
        if not self_cls.is_special_attr(name):
            return super().__setattr__(name, value)

        if name in vars(self_cls).keys():
            print(f'{self_cls.__name__} set val for {name} = {value}')
            return super().__setattr__(name, value)


        self_proto = self.proto()
        if self_proto:
            setattr(self_proto, name, value)
        else:
            raise AttributeError(f'{type(self)} object has no attribute {name}')



    def __getattribute__(self, name: str) -> Any:
        self_cls = type(self)
        if not self_cls.is_special_attr(name):            
            return super().__getattribute__(name)

        if not hasattr(self_cls, name):
            raise AttributeError(f'{type(self)} object has no attribute {name}')



    @classmethod
    def is_special_attr(cls, name: str) -> bool:
        pattern = re.compile(r"___.*___")
        res = bool(pattern.match(name))
        if not res:
            print(f'{name} is not special')
        
        return res