from __future__ import annotations
from abc import abstractmethod
from typing import *
import inflection
import json

class Storable():

    @abstractmethod
    def save(self) -> Any:
        pass

    @abstractmethod
    def find(self) -> Any:
        pass

class Searchable():

    @abstractmethod
    def put(self, node:Node=None, **kwargs:Any) -> Any:
        pass

    @abstractmethod
    def search(self, key:object) -> Any:
        pass

class StorageNotFound(Exception):
    pass


class Node(Searchable, Storable):
    storage = None
    parent = None
    __proto__ = None
    dict:Dict[object, object] = {}
    heap:Node
    _name:str

    def __init__(self, storage:Any = None, name:str=None) -> None:
        if storage:
            self.storage = storage
        self._name = name



    def save(self, storage:Any=None) -> Any:
        storage = self.get_storage(storage)
        return storage.put(self)



    def find(self, storage:Any=None) -> Any:
        storage = self.get_storage(storage)
        return storage.search()



    def put(self, node:Node=None, **kwargs:Any) -> Any:
        self.dict[id(node)] = node
        return id(node)



    def search(self, key:object) -> Any:        
        return self.dict[key]



    def delete(self, node:Node = None, **kwargs:Any) -> bool:
        pass



    def contains(self, node:Node=None, **kwargs:Any) -> bool:
        pass



    def get_storage(self, storage:Any=None) -> Any:
        storage = storage or self.storage or type(self).heap
        if not storage:
            raise StorageNotFound
        return storage

    
    
    @property
    def name(self) -> str:
        if not self._name:
            self._name = inflection.underscore(type(self).__name__)
        return self._name



    @name.setter
    def name(self, name:str) -> None:
        self._name = name
    


    def to_json(self) -> str:
        json_dict = {}
        for key, val in vars(self).items():
            if hasattr(val, 'to_json') and callable(val.to_json):
                json_dict[key] = val.to_json()
            else:
                json_dict[key] = json.dumps(val)
        return json.dumps(json_dict)

Node.heap = Node()