from typing import Any
from types import MethodType

class Query:
    __exec__ = None
    __query_taker__ = None

    def __init__(self, query_taker, exec) -> None:
        self.__exec__ = exec
        self.__query_taker__ = query_taker

    def __call__(self, ins=None, exec=None) -> Any:
        res = (exec(self.__query_taker__) if exec
            else self.__exec__(self.__query_taker__()))
        return res

    def __str__(self) -> str:
        res = self.__query_taker__() or super().__str__()
        return res

    def __get__(self, ins, instype):
        res = (MethodType(self, ins) if ins
            else self)
        return res