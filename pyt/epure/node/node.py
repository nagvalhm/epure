from __future__ import annotations
from abc import abstractmethod
from typing import *
import inflection
import json
import jsonpickle
import uuid
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


class ScriptType:
    sql = 'postgress'

class StorageNotFound(Exception):
    pass


class Node(Searchable, Storable):
    _storage = None
    parent = None
    __proto__ = None
    dict:Dict[object, object] = {}
    heap:Node = None
    _name:str = None
    node_id:str = None
    script_type:str = None
    __exclude__:Sequence[Any]
    # _storage = None
    


    def __init__(self, name:str=None, storage:Node = None) -> None:
        if storage:
            self._storage = storage
        if name:
            self._name = name        



    def save(self, storage:Node=None) -> Any:
        storage = self.get_storage(storage)
        return storage.put(self)



    def find(self, storage:Node=None) -> Any:
        storage = self.get_storage(storage)
        return storage.search([])



    def put(self, node:Node=None) -> Any:
        raise AttributeError('storage not defined')
        # self.dict[id(node)] = node
        # return id(node)



    def search(self, keys:list[str]) -> Any:        
        return self.dict[keys]



    def delete(self, node:Node = None) -> bool:
        pass



    def contains(self, node:Node, deep:bool=True) -> bool:
        pass



    @property
    def path(self) -> str:
        return ''



    def get_storage(self, storage:Node=None) -> Node:
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
    def storage(self) -> Node:
        return self._storage 



    @storage.setter
    def storage(self, storage:Node) -> None:
        self._storage = storage



    def link(self) -> Node:        
        node_type = type(self)
        link = object.__new__(node_type)
        if not isinstance(link, Node):
            raise TypeError
            
        vars(link)['___id___'] = self.get_id()

        return link


    def get_id(self) -> str:
        if not self.node_id:
            self.node_id = str(uuid.uuid4())
        return self.node_id


    # def is_savable(self, atr_name: str, node_fields: dict[str, Any]) -> bool:
        


Node.heap = Node()