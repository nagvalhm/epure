from __future__ import annotations
from abc import abstractmethod
from typing import *

class Storable():

    @abstractmethod
    def save(self=None):
        pass

    @abstractmethod
    def find(self=None):
        pass

class Storage():

    @abstractmethod
    def put(self=None):
        pass

    @abstractmethod
    def search(self=None):
        pass

class StorageNotFound(Exception):
    pass


class Node(Storage, Storable):

    storage = None
    parent = None
    __proto__ = None
    universe:Dict[object, object] = {}
    heap:Node

    def __init__(self:Any, storage:Any = None) -> None:
        if storage:
            self.storage = storage

    def save(self, storage=None):
        storage = self.get_storage(storage)
        return storage.put(self)

    def find(self, storage=None):
        storage = self.get_storage(storage)
        return storage.search()

    def put(self, node):
        self.universe[id(node)] = node
        return id(node)

    def search(self, key):
        heap: dict = type(self).heap        
        return heap[key]

    def delete(self, node):
        pass

    def contains(self, node) -> bool:
        pass

    def get_storage(self, storage=None):
        storage = storage or self.storage or type(self).heap
        if not storage:
            raise StorageNotFound
        return storage
    
Node.heap = Node()
    




