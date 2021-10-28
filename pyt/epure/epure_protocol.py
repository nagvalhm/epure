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
    def put(self=None):
        pass

    @abstractmethod
    def out(self=None):
        pass


class EpureProtocol(Savable, Outable):

    @abstractmethod
    def __new__(cls):
        return super().__new__(cls)

    def save(self=None):
        return 'save is called'

    def out(self=None):
        return 'EpureProtocol out'
    
    def put(self=None):
        return 'put is called'

    def find(self=None):
        return 'find is called'

