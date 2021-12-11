from __future__ import annotations
from abc import abstractmethod
from typing import *
import inflection
import json
import jsonpickle
# from deepdiff import DeepDiff


class Storable():

    @abstractmethod
    def save(self) -> Any:
        pass

    @abstractmethod
    def find(self) -> Any:
        pass

class Searchable():

    @abstractmethod
    def put(self, node:Node=None) -> Any:
        pass

    @abstractmethod
    def search(self, keys:list[str]) -> Any:
        pass

class StorageNotFound(Exception):
    pass


class Node(Searchable, Storable):
    _storage = None
    parent = None
    __proto__ = None
    dict:Dict[object, object] = {}
    heap:Node = None
    _name:str = None
    # _storage = None
    


    def __init__(self, storage:Any = None, name:str=None) -> None:
        if storage:
            self._storage = storage
        self._name = name



    def save(self, storage:Any=None) -> Any:
        storage = self.get_storage(storage)
        return storage.put(self)



    def find(self, storage:Any=None) -> Any:
        storage = self.get_storage(storage)
        return storage.search()



    def put(self, node:Node=None) -> Any:
        self.dict[id(node)] = node
        return id(node)



    def search(self, keys:list[str]) -> Any:        
        return self.dict[keys]



    def delete(self, node:Node = None) -> bool:
        pass



    def contains(self, node:Node=None, deep:bool=True) -> bool:
        pass



    @property
    def path(self) -> str:
        return ''



    def get_storage(self, storage:Any=None) -> Any:
        storage = storage or self.storage or type(self).heap
        if not storage:
            raise StorageNotFound
        return storage



    @classmethod
    def class_name(cls) -> str:
        return inflection.underscore(cls.__name__)
    


    @property
    def name(self) -> str:
        if not self._name:
            self._name = type(self).class_name()
        return self._name



    @name.setter
    def name(self, name:str) -> None:
        self._name = name
    


    def to_json(self) -> str:
        return str(jsonpickle.encode(self))



    @staticmethod
    def from_json(json_str:str) -> Node:
        res = jsonpickle.decode(json_str)
        if not isinstance(res, Node):
            raise TypeError('res must be Node')
        return res



    def __eq__(self, o: object) -> bool:
        if self is o:
            return True
        self_json = self.to_json()
        if not isinstance(o, Node):
            raise TypeError(f'{o} must be Node')
        o_json = o.to_json()
        return bool(json.loads(self_json) == json.loads(o_json))

        # return bool(DeepDiff(self, o) == {})
    


    @property
    def storage(self) -> Any:
        return self._storage 



    @storage.setter
    def storage(self, storage:Any) -> None:
        self._storage = storage



Node.heap = Node()