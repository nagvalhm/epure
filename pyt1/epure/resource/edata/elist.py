from __future__ import annotations
from collections.abc import Iterable, Iterator
from .edata import TableData
from typing import List, Any, Type, Generic, Set, Dict
from uuid import UUID, uuid4
from ...epure import Epure, epure, escript
from types import NoneType
from .ecollection_metacls import ECollectionMetacls
from ..db.table import Table
from ...resource.savable import Savable
from typing import get_origin

class Elist(TableData, List, metaclass=ECollectionMetacls):
# class Elist(TableNode, List):
    entries:List
    deleted_entries:List
    py_type:type = NoneType
    collection_epure:Epure = None
    data_id:UUID

    def __init__(self, _list:List=None) -> None:
        self.entries = []
        self.deleted_entries = []

        if _list == None:
            _list = []

        # if len(_list) and isinstance(_list[0], self.collection_epure):
        if len(_list) and hasattr(_list[0], "resource") and\
        _list[0].resource.full_name == self.collection_epure.resource.full_name:
            self.data_id = _list[0].eset_id
            _list.sort(key= lambda x: x.value_order)
            self.entries = _list
        else:
            for val in _list:
                self.append(val)
    
    @classmethod
    def get_collection_epure(cls, table=None, parent_obj=None, field_name=None) -> Epure:  
        return cls.collection_epure

    def save(self, asynch:bool=False) -> Elist:
        """
        Save all items stored in Elist, if asynch=True is passed - Elist will be saved asynchronously
        """
        if not hasattr(self,"data_id") or not self.data_id:
            self.data_id = uuid4()

        val_len = self.entries.__len__()
        for i in range(val_len):
            item = self.entries[i]

            if get_origin(self.py_type) != None: # check if class is Generic
                self.py_type = get_origin(self.py_type)

            if not isinstance(item.value, self.py_type):
                raise TypeError(f"value '{item.value}' of type '{type(item.value)}' is not same " 
                                f"type as Elist '{self.collection_epure.resource.full_name}' type of '{self.py_type}'")
            
            item.eset_id = self.data_id
            item.value_order = i

            # if hasattr(val, "__deleted__") and val.__deleted__:
            #     self.resource.delete(val)
            if i != val_len-1:
                item.save(asynch=True)
            else:
                item.save(asynch=asynch)

        for i in range(self.deleted_entries.__len__()):
            item = self.deleted_entries[i]
            self.collection_epure.resource.delete(item.data_id)
        
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
        # if not isinstance(item, self.py_type):
        if hasattr(item, "resource") and item.resource.full_name != self.py_type.resource.full_name:
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
        item = next(iter(__iterable), False)
        if not ((hasattr(__iterable, "py_type") and item.py_type == self.py_type)\
                or type(item) == self.py_type):
            raise TypeError(f"value '{item}' of type '{type(item)}' is not same "
                                f"type as Elist '{self.collection_epure.resource.full_name}' type of '{self.py_type}'")
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
    def load(self, *args, **kwargs) -> None:
        """
        Loads all items of Elist contents like Epure, Elist, Eset values from DataPromises
        """
        if not isinstance(self.py_type, Epure):
            return

        data_id_dict:dict = {}
        
        for val in self.entries:
            if hasattr(val, '__promises_dict__') and 'value' in val.__promises_dict__:
                data_id_dict[val.__promises_dict__['value'].data_id] = val

        if len(data_id_dict) == 0:
            return

        # res = self.py_type.resource.read(lambda tp, dp: tp.node_id >= list(node_id_dict.keys()))
        # res = self.py_type.resource.read(self.tp.node_id in list(node_id_dict.keys()))
        py_type_tp = getattr(self.dom, self.py_type.resource.full_name)
        res = self.py_type.resource.read(py_type_tp.data_id in list(data_id_dict.keys()))


        for val in res:
            data_id_dict[val.data_id].value = val

    def __len__(self) -> int:
        return self.entries.__len__()
    
    @property
    def ids(self) -> List[str]:
        """
        Returns data_id's from all items of Elist
        """

        res = []
        for item in self.entries:
            # if hasattr(item, "__promises_dict__") and\
            # "value" in item.__promises_dict__:
            #     id = item.__promises_dict__['value'].node_id
            # else:
            id = item.data_id

            res.append(str(id))

        return res
    
    def __iter__(self) -> Iterator:
        return iter([i.value for i in self.entries])

class Eset(set, TableData, metaclass=ECollectionMetacls):
    # entries:Set
    deleted_entries:Set
    py_type:type = NoneType
    collection_epure:Epure = None
    data_id:UUID

    def __init__(self, _set:Set=None, collection_resourse=None, **kwargs:dict[UUID:UUID]) -> None:
        super(set, self).__init__()
        if collection_resourse != None:
            self.collection_epure = self.get_collection_epure(collection_resourse)

        if _set == None:
            _set = []

        self.deleted_entries = []
        # if len(_set) and isinstance(_set[0], self.collection_epure):
        if len(_set) and hasattr(_set[0], "resource") and\
        _set[0].resource.full_name == self.collection_epure.resource.full_name:
                # self.data_id = _set[0].eset_id
                self.update(_set, ids_dict=kwargs)
        else:
            for index, item in enumerate(_set):
                if kwargs and kwargs["ids_dict"]:
                    self.add(item, ids_dict=list(kwargs["ids_dict"].items())[index])
                else:
                    self.add(item)


    def add(self, item: Any, **kwargs) -> None:

        if not isinstance(item, (self.py_type, Savable)):
                raise TypeError(f"value '{item}' of type '{type(item)}' is not same " 
                                f"type as Elist '{self.collection_epure.resource.full_name}' type of '{self.py_type}'")
        
        elif isinstance(self.py_type, Savable) and isinstance(item, Savable)\
        and not self.py_type.resource.full_name == item.resource.full_name:
            raise TypeError(f"value '{item}' of type '{type(item)}' is not same " 
                                f"type as Elist '{self.collection_epure.resource.full_name}' type of '{self.py_type}'")
        
        # super(Eset, self).add(item)
        # self.add(item)
        res = self.collection_epure()
        res.value = item

        if isinstance(self.py_type, Savable):
            self_iter_obj = super(self.__class__, self).__iter__()
            # for val in self:
            for val in self_iter_obj:
                if item is val:
                    raise ValueError(f"value {item} is already present in Eset")
                
        if kwargs and kwargs['ids_dict']:
            res.data_id = kwargs['ids_dict'][0]
            res.eset_id = kwargs['ids_dict'][1]
            
        super(self.__class__, self).add(res)

    def save(self, asynch:bool=False) -> Elist:
        """
        Save all items stored in Eset, if asynch=True is passed - Eset will be saved asynchronously
        """
        if not hasattr(self, "data_id") or not self.data_id:
            self.data_id = uuid4()

        val_len = self.__len__()
        self_iter_obj = super(self.__class__, self).__iter__()
        # self_list = list(self)
        self_list = list(self_iter_obj)
        for i in range(val_len):
            item = self_list[i]
            if not isinstance(item.value, self.py_type):
                raise TypeError(f"value '{item.value}' of type '{type(item.value)}' is not same " 
                                f"type as Elist '{self.collection_epure.resource.full_name}' type of '{self.py_type}'")
            
            item.eset_id = self.data_id

            # if hasattr(val, "__deleted__") and val.__deleted__:
            #     self.resource.delete(val)
            if i != val_len-1:
                item.save(asynch=True)
            else:
                item.save(asynch=asynch)

        for i in range(self.deleted_entries.__len__()):
            item = self.deleted_entries[i]
            if hasattr(item, "data_id") and item.data_id:
                self.collection_epure.resource.delete(item.data_id)
        
        self.deleted_entries = []

        return self
    
    def remove(self, ___element: Any) -> None:
        self_iter_obj = super(self.__class__, self).__iter__()
        # for x in self:
        for x in self_iter_obj:
            if x.value == ___element:
                ___element = x
                break
        self.deleted_entries.append(___element)
        return super(self.__class__, self).remove(___element)
    
    def discard(self, el: Any) -> None:
        self_iter_obj = super(self.__class__, self).__iter__()
        for x in self_iter_obj:
        # for x in self:
            if x.value == el:
                el = x
                break
        self.deleted_entries.append(el)
        return super(self.__class__, self).discard(el)
    
    def clear(self) -> None:
        """
        Clear Eset from elements
        """
        entries = self.copy()
        self.deleted_entries.extend(entries)
        return super(self.__class__, self).clear()
    
    @property
    def ids(self) -> List[str]:
        """
        Returns data_id's from all items of Elist
        """
        # if not self.is_saved:
        #     raise Exception("Your Eset is not saved, try .save()")
        self_iter_obj = super(self.__class__, self).__iter__()
        res = []
        # for item in list(self):
        for item in self_iter_obj:
            # if hasattr(item, "__promises_dict__") and\
            # "value" in item.__promises_dict__:
            #     id = item.__promises_dict__['value'].node_id
            # else:
            id = item.data_id

            res.append(str(id))

        return res
    
    def __contains__(self, __o: object) -> bool:
        self_iter_obj = super(self.__class__, self).__iter__()
        # for x in self:
        for x in self_iter_obj:
            if x.value == __o:
                return True

        # return super().__contains__(__o)


    @classmethod
    def get_collection_epure(cls, table=None, parent_obj=None, field_name=None):
        """Get Epure class from Eset"""        
        from .edata import EsetTableData

        if table != None:
            name = table.full_name
        else:
            from ...named import SnakeCaseNamed
            name = f'{parent_obj.__class__.__name__}__{field_name}'
            name = SnakeCaseNamed(name).full_name


        if name in Epure.EDb:
            res = Epure.EDb.get_epure_by_table_name(name)
            return res
        
        # if name in ECollectionMetacls.ecollections:
        #     res = ECollectionMetacls.ecollections[name]
        #     cls.collection_epure = res
        #     return res
    
        obj = type(name, (object,), {})
        obj.__annotations__ = {"eset_id":UUID, "value":cls.py_type}
        res = epure(resource=f'ecollections.{name}', saver=EsetTableData)(obj)
        cls.collection_epure = res
        # ECollectionMetacls.ecollections[name] = res

        return res
    

    def _redefine_collection_epure(self, collection_epure:Epure) -> None:
        vals_list = []
        ids_dict = {}
        self_iter_obj = super(self.__class__, self).__iter__()
        # for item in self:
        for item in self_iter_obj:
            vals_list.append(item.value)
            if hasattr(item, "eset_id") and hasattr(item, "data_id"):
                ids_dict[item.data_id] = item.eset_id
            
        self.clear()
        self.collection_epure = collection_epure

        # for item in vals_list:
        #     self.add(item)

        self.__init__(vals_list, ids_dict=ids_dict)
    
    def load(self) -> None:
        """
        Load Eset instance's items
        """
        list_values = self.collection_epure.resource.read(eset_id=self.data_id)
        self.__init__(list_values)

        if not isinstance(self.py_type, Epure):
            return

        data_id_dict:dict = {}
        
        for val in self:
            if hasattr(val, '__promises_dict__') and 'value' in val.__promises_dict__:
                data_id_dict[val.__promises_dict__['value'].data_id] = val

        if len(data_id_dict) == 0:
            return

        # res = self.py_type.resource.read(lambda tp, dp: tp.node_id >= list(node_id_dict.keys()))
        # res = self.py_type.resource.read(self.tp.node_id in list(node_id_dict.keys()))
        py_type_tp = getattr(self.dom, self.py_type.resource.full_name)
        res = self.py_type.resource.read(py_type_tp.data_id in list(data_id_dict.keys()))


        for val in res:
            data_id_dict[val.data_id].value = val

    def __iter__(self) -> Iterator:
        it_obj = super(self.__class__, self).__iter__()
        return iter([item.value for item in it_obj])
    
    def update(self, *s: Iterable, **kwargs:[UUID, UUID]) -> None:
        """
        Add items to Eset instance from an iterable
        """
        fin_res = []
        if kwargs["ids_dict"]:
            for ind, _iterable in enumerate(s):
                # if not isinstance(list(item)[0], self.collection_epure):
                    # raise TypeError("Eset cannot be updated with Eset of different type")
                res = []
                for item, ids in zip(list(_iterable)[ind], kwargs["ids_dict"].items()):
                    item.data_id = ids[0]
                    item.eset_id = ids[1]
                    res.append(item)
                
                fin_res.append(res)

        super(self.__class__, self).update(*s)