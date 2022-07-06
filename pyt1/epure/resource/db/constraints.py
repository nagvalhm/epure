from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast

class IndexedTypeMeta(type):
    def __getitem__(cls:Type, param:Any):
        cls.__param__ = param
        return cls

class NotNull(metaclass=IndexedTypeMeta):
    __param__:type

class Id(metaclass=IndexedTypeMeta):
    __param__:type

class Uniq(metaclass=IndexedTypeMeta):
    __param__:type

class Check(metaclass=IndexedTypeMeta):
    __param__:type
    __condition__:Callable
    def __class_getitem__(cls, param:Any, condition:Callable):
        cls.__param__ = param
        cls.__condition__ = condition
        return cls