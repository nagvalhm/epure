from __future__ import annotations
from collections.abc import Iterable
from .node import TableNode
from typing import List, Any, Type, Generic, Set, Dict
from uuid import UUID, uuid4
from ...epure import Epure, epure, escript
from types import NoneType
# from .elist_metacls import ElistMetacls
from .elist_metacls import ECollectionMetacls

class Elist(TableNode, List, metaclass=ECollectionMetacls):
# class Elist(TableNode, List):
    entries:List
    deleted_entries:List
    py_type:type = NoneType
    collection_epure:Epure = None
    node_id:UUID

    def __init__(self, _list:List) -> None:
        self.entries = []
        self.deleted_entries = []
        if isinstance(_list[0], self.collection_epure):
            self.node_id = _list[0].collection_node_id
            _list.sort(key= lambda x: x.value_order)
            self.entries = _list
        else:
            for val in _list:
                self.append(val)

    def save(self, asynch:bool=False) -> UUID:
            
        if not hasattr(self,"node_id") or not self.node_id:
            self.node_id = uuid4()

        val_len = self.entries.__len__()
        for i in range(val_len):
            item = self.entries[i]
            if not isinstance(item.value, self.py_type):
                raise TypeError(f"value '{item.value}' of type '{type(item.value)}' is not same " 
                                f"type as Elist '{self.collection_epure.resource.full_name}' type of '{self.py_type}'")
            
            item.collection_node_id = self.node_id
            item.value_order = i

            # if hasattr(val, "__deleted__") and val.__deleted__:
            #     self.resource.delete(val)
            if i != val_len-1:
                item.save(asynch=True)
            else:
                item.save(asynch=asynch)

        for i in range(self.deleted_entries.__len__()):
            item = self.deleted_entries[i]
            self.collection_epure.resource.delete(item.node_id)
        
        self.deleted_entries = []

        return self

    def __setitem__(self, index, item) -> None:
        if not isinstance(item, self.py_type):
                raise TypeError(f"value '{item}' of type '{type(item)}' is not same " 
                                f"type as Elist '{self.collection_epure.resource.full_name}' type of '{self.py_type}'")
        self.entries[index].value = item
        # res = self.collection_epure()
        # res.value_order = index
        # res.value = item
        # self.entries.__setitem__(index, res)

    # def __delitem__(self, key)

    def insert(self, index, item) -> None:
        if not isinstance(item, self.py_type):
                raise TypeError(f"value '{item}' of type '{type(item)}' is not same " 
                                f"type as Elist '{self.collection_epure.resource.full_name}' type of '{self.py_type}'")
        res = self.collection_epure()
        res.value_order = index
        res.value = item
        self.entries.insert(index, res)

    def append(self, item) -> None:
        if not isinstance(item, self.py_type):
                raise TypeError(f"value '{item}' of type '{type(item)}' is not same " 
                                f"type as Elist '{self.collection_epure.resource.full_name}' type of '{self.py_type}'")
        res = self.collection_epure()
        res.value_order = len(self.entries)
        res.value = item
        self.entries.append(res)

    def count(self) -> int:
        return self.entries.count()
    
    def copy(self) -> list:
        return self.entries.copy()
    
    def clear(self) -> None:
        entries = self.entries.copy()
        self.entries.clear()
        self.deleted_entries.extend(entries)

    def index(self, value:Any, *args) -> int:
        return self.entries.index(value, *args)

    def extend(self, __iterable: Iterable) -> None:
        self.entries.extend(__iterable)
    
    def pop(self, index = -1) -> Any:
        res = self.entries.pop(index)
        self.deleted_entries.append(res)
        return res
    
    def remove(self, __value: Any) -> None:
        for x in self.entries:
            if x.value == __value:
                __value = x
                break
        self.entries.remove(__value)
        self.deleted_entries.append(__value)
    
    def reverse(self) -> None:
        self.entries.reverse()
    
    def sort(self, *, key=None, reverse=False) -> None:
        self.entries.sort(key=key, reverse=reverse)

    def __getitem__(self: Type, _param: Any):
        return self.entries[_param].value
    
    def __repr__(self):
        return str(self.entries)
    
    # def __eq__(self, __value: Elist|object) -> bool:
    #     if issubclass(__value,Elist):
    #         return self.entries.__eq__(__value.entries)
    #     return self.entries.__eq__(__value)

    @escript
    def read(self, *args, **kwargs):
        if not isinstance(self.py_type, Epure):
            return

        node_id_dict:dict = {}
        
        for val in self.entries:
            if hasattr(val, '__promises_dict__') and 'value' in val.__promises_dict__:
                node_id_dict[val.__promises_dict__['value'].node_id] = val

        if len(node_id_dict) == 0:
            return

        # res = self.py_type.resource.read(lambda tp, dp: tp.node_id >= list(node_id_dict.keys()))
        res = self.py_type.resource.read(self.tp.node_id in list(node_id_dict.keys()))

        for val in res:
            node_id_dict[val.node_id].value = val

    def __len__(self) -> int:
        return self.entries.__len__()
    
    @property
    def ids(self):
        res = []
        for item in self.entries:
            # if hasattr(item, "__promises_dict__") and\
            # "value" in item.__promises_dict__:
            #     id = item.__promises_dict__['value'].node_id
            # else:
            id = item.node_id

            res.append(str(id))

        return res

class Eset(set, TableNode, metaclass=ECollectionMetacls):
    # entries:Set
    deleted_entries:Set
    py_type:type = NoneType
    collection_epure:Epure = None
    node_id:UUID

    def __init__(self, _set:Set) -> None:
        super(set, self).__init__()
        self.deleted_entries = []
        if isinstance(_set[0], self.collection_epure):
                self.node_id = _set[0].collection_node_id
                super(self.__class__, self).update(_set)
        else:
            for item in _set:
                self.add(item)

    def add(self, item: Any) -> None:

        if not isinstance(item, self.py_type):
                raise TypeError(f"value '{item}' of type '{type(item)}' is not same " 
                                f"type as Elist '{self.collection_epure.resource.full_name}' type of '{self.py_type}'")
        
        # super(Eset, self).add(item)
        # self.add(item)
        res = self.collection_epure()
        res.value = item
        for val in self:
            if item is val.value:
                raise ValueError(f"value {item} is already present in Eset")
        super(self.__class__, self).add(res)

    def save(self, asynch:bool=False) -> UUID:
            
        if not hasattr(self, "node_id") or not self.node_id:
            self.node_id = uuid4()

        val_len = self.__len__()
        self_list = list(self)
        for i in range(val_len):
            item = self_list[i]
            if not isinstance(item.value, self.py_type):
                raise TypeError(f"value '{item.value}' of type '{type(item.value)}' is not same " 
                                f"type as Elist '{self.collection_epure.resource.full_name}' type of '{self.py_type}'")
            
            item.collection_node_id = self.node_id

            # if hasattr(val, "__deleted__") and val.__deleted__:
            #     self.resource.delete(val)
            if i != val_len-1:
                item.save(asynch=True)
            else:
                item.save(asynch=asynch)

        for i in range(self.deleted_entries.__len__()):
            item = self.deleted_entries[i]
            self.collection_epure.resource.delete(item.node_id)
        
        self.deleted_entries = []

        return self
    
    def remove(self, ___element: Any) -> None:
        for x in self:
            if x.value == ___element:
                ___element = x
                break
        self.deleted_entries.append(___element)
        return super(self.__class__, self).remove(___element)
    
    def discard(self, el: Any) -> None:
        for x in self:
            if x.value == el:
                el = x
                break
        self.deleted_entries.append(el)
        return super(self.__class__, self).discard(el)
    
    def clear(self) -> None:
        entries = self.copy()
        self.deleted_entries.extend(entries)
        return super(self.__class__, self).clear()
    
    @property
    def ids(self):
        res = []
        for item in list(self):
            # if hasattr(item, "__promises_dict__") and\
            # "value" in item.__promises_dict__:
            #     id = item.__promises_dict__['value'].node_id
            # else:
            id = item.node_id

            res.append(str(id))

        return res
    
    def __contains__(self, __o: object) -> bool:
        
        for x in self:
            if x.value == __o:
                return True

        # return super().__contains__(__o)