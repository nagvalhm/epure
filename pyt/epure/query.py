from __future__ import annotations
from typing import Any
from types import *

class Query:
    __exec__:MethodType
    __query_taker__:MethodType

    def __init__(self:Query, query_taker:MethodType, exec:MethodType) -> None:
        self.__exec__ = exec
        self.__query_taker__ = query_taker

    def __call__(self:Query, ins:object=None, exec:Any=None) -> Any:
        res = (exec(self.__query_taker__) if exec
            else self.__exec__(self.__query_taker__()))
        return res

    def __str__(self:Query) -> str:
        res = self.__query_taker__() or super().__str__()
        return res

    def __get__(self:Query, ins:object, instype:type) -> Any:
        res = (MethodType(self, ins) if ins
            else self)
        return res