from __future__ import annotations
from abc import abstractmethod, ABCMeta
from typing import *
import re


class MultipleInheritanceError(Exception):
    pass

class ProtoMeta(type):
    _proto_cls:ProtoMeta

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
        if '_proto_cls' in vars(cls).keys():
            return cls._proto_cls

        bases = cls.__bases__
        protos = list(filter(lambda base: issubclass(base, Proto), bases))
        if len(protos) > 1:
            raise MultipleInheritanceError(f'{cls.__name__} has more than one Proto ancestor: {protos}')
        
        if len(protos) == 0:
            raise
        res = protos[0]
        if not isinstance(res, ProtoMeta):
            raise TypeError

        cls._proto_cls = res
        return res



class Proto(metaclass=ProtoMeta):
    __proto__:Proto = None
    __abstractclass__ = 1
    

    def __new__(cls: ProtoMeta, *args: Any, **kwargs: Any) -> Proto:
        print(f'{cls.__name__} new called')
        res = super(type, cls).__new__(cls)
        if not isinstance(res, Proto):
            raise TypeError
        proto_cls = cls.proto_cls
        if '__abstractclass__' not in vars(proto_cls).keys():
            res.__proto__ = proto_cls(*args, **kwargs)

        return res
    
    def __setattr__(self, name: str, value: Any) -> None:
        self_cls = type(self)
        if not self_cls.is_special_attr(name):
            return super().__setattr__(name, value)

        if name in vars(self_cls).keys():
            print(f'{self_cls.__name__} set val for {name} = {value}')
            return super().__setattr__(name, value)


        self_proto = self.__proto__
        if self_proto:
            setattr(self_proto, name, value)
        else:
            raise AttributeError(f'{type(self)} object has no attribute {name}')



    def __getattribute__(self, name: str) -> Any:
        self_cls = type(self)
        if not self_cls.is_special_attr(name):            
            return super().__getattribute__(name)

        if name in vars(self_cls).keys():
            print(f'{self_cls.__name__} get val for {name}')
            return super().__getattribute__(name)


        self_proto = self.__proto__
        if self_proto:
            return getattr(self_proto, name)
        else:
            raise AttributeError(f'{type(self)} object has no attribute {name}')



    @classmethod
    def is_special_attr(cls, name: str) -> bool:
        pattern = re.compile(r"___.*___")
        res = bool(pattern.match(name))
        if not res:
            print(f'{name} is not special')
        
        return res