from __future__ import annotations
from collections.abc import Iterable
from .node import TableNode
from typing import List, Any, Type, Generic
from uuid import UUID, uuid4
from ...epure import Epure, epure
from types import NoneType
from .elist_metacls import ElistMetacls

class Elist(TableNode, List, metaclass=ElistMetacls):
# class Elist(TableNode, List):
    values:List
    # py_type:type = NoneType
    list_epure:Epure = None
    node_id:UUID

    def __init__(self, _list:List) -> None:
        self.values = []
        if isinstance(_list[0], self.list_epure):
            self.node_id = _list[0].node_id
            _list.sort(key= lambda x: x.value_order)
            self.values = _list
        else:
            for val in _list:
                self.append(val)

    def save(self, asynch:bool=False) -> UUID:
            
        if not hasattr(self,"node_id") or not self.node_id:
            self.node_id = uuid4()

        val_len = self.values.__len__()
        for i in range(val_len):
            val = self.values[i]
            val.elist_node_id = self.node_id

            if i != val_len-1:
                val.save(asynch=True)
            else:
                val.save(asynch=asynch)

        return self

    def __setitem__(self, index, item) -> None:
        self.values.__setitem__(index, item)

    def insert(self, index, item) -> None:
        self.values.insert(index, item)

    def append(self, item) -> None:
        res = self.list_epure()
        res.value_order = len(self.values)
        res.value = item
        self.values.append(res)

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
    
    def sort(self, *, key=None, reverse=False) -> None:
        self.values.sort(key=key, reverse=reverse)

    def __getitem__(self: Type, _param: Any):
        return self.values[_param]
    
    def __repr__(self):
        return str(self.values)
    
    # def __eq__(self, __value: Elist|object) -> bool:
    #     if issubclass(__value,Elist):
    #         return self.values.__eq__(__value.values)
    #     return self.values.__eq__(__value)