from abc import abstractmethod

class Savable():

    @abstractmethod
    def save(self=None):
        pass

    @abstractmethod
    def find(self=None):
        pass

class Outable():

    @abstractmethod
    def search(self=None):
        pass

    @abstractmethod
    def out(self=None):
        pass

class StoreNotFound(Exception):
    pass

class Node(Savable, Outable):

    store = None
    parent = None
    __proto__ = None
    heap = dict()

    def save(self, store=None):
        store = self.get_store(self, store)        
        return store.search(self)

    def find(self, store=None):
        store = self.get_store(self, store)
        return store.out()

    def search(self, node):
        heap: dict = type(self).heap
        heap[id(node)] = node
        return id(node)

    def out(self, key):
        heap: dict = type(self).heap        
        return heap[key]

    def get_store(self, store=None):
        store = store or self.store or type(self).heap
        if not store:
            raise StoreNotFound
        return store
    




