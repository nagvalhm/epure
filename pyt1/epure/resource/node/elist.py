
from collections.abc import Iterable
from .node import TableNode
from typing import List, Any, Type, Generic
from uuid import UUID, uuid4
from ...epure import Epure, epure
from types import NoneType

class Generic(type):
    py_type:type = NoneType
    __origin__:type = NoneType

    def __getitem__(self:Type, param:Any):
        res = self.__class__(self.__name__, self.__bases__, dict(self.__dict__))
        res.__origin__ = self
        res.py_type = param


        # if issubclass(res.py_type, Constraint):
        #     # ( hasattr(res.py_type, '__origin__') and  issubclass(res.py_type.__origin__, Constraint)):
        #     raise EpureError('Constraint parameter cant be Constraint')
        return res

class Elist(TableNode, List, metaclass=Generic):
# class Elist(TableNode, List):
    values:List
    # py_type:type = NoneType
    list_epure:Epure = None
    node_id:UUID

    def __init__(self, _list:List) -> None:
        self.values = _list

        py_type = self.__class__.py_type
        name = f"{py_type.__name__}___list"
        self.list_epure = Epure.EDb.get_epure_by_table_name(name)
        if self.list_epure is None:
            obj = type(name, (object,), {})
            obj.__annotations__ = {"list_id":UUID, "value_order":int, "value":py_type}
            self.list_epure = epure()(obj)
        # super().__init__()
        # super(TableNode, self).__init__(_list)

    def save(self, asynch:bool = False) -> UUID:
        # Epure.EDb
        # if not f"{self.__class__.py_type.__name__}___list" in Epure.EDb:
            # pass
        uuid = uuid4()
        val_len = self.values.__len__()
        for i in range(val_len):
            inst = self.list_epure()
            inst.list_id = uuid
            inst.value_order = i
            inst.value = self.values[i]

            if i == val_len-1:
                inst.save()
            else:
                inst.save(asynch=True)
        self.node_id = uuid
        return self

    def __setitem__(self, index, item) -> None:
        self.values.__setitem__(index, item)

    def insert(self, index, item) -> None:
        self.values.insert(index, item)

    def append(self, item) -> None:
        self.values.append(item)

    def count(self) -> int:
        return self.values.count()
    
    def copy(self) -> list:
        return self.values.copy()
    
    def clear(self) -> None:
        self.values.clear()

    def index(self, value:Any, *args) -> int:
        return self.values.index(value, *args)

    def extend(self, __iterable: Iterable) -> None:
        self.values.extend(__iterable)
    
    def pop(self, __index = -1) -> Any:
        return self.values.pop(__index)
    
    def remove(self, __value: Any) -> None:
        self.values.remove(__value)
    
    def reverse(self) -> None:
        self.values.reverse()
    
    def sort(self) -> None:
        self.values.sort()