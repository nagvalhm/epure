from abc import abstractmethod

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
    heap = dict()

    def save(self, storage=None):
        storage = self.get_storage(self, storage)        
        return storage.put(self)

    def find(self, storage=None):
        storage = self.get_storage(self, storage)
        return storage.search()

    def put(self, node):
        heap: dict = type(self).heap
        heap[id(node)] = node
        return id(node)

    def search(self, key):
        heap: dict = type(self).heap        
        return heap[key]

    def get_storage(self, storage=None):
        storage = storage or self.storage or type(self).heap
        if not storage:
            raise StorageNotFound
        return storage
    




