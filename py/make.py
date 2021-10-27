from abc import abstractmethod

class Savable():

    @abstractmethod
    def save(self=None):
        pass

    @abstractmethod
    def take(self=None):
        pass

class Finable():

    @abstractmethod
    def put(self=None):
        pass

    @abstractmethod
    def find(self=None):
        pass

class Make(Savable, Finable):

    @abstractmethod
    def __new__(cls):
        return super().__new__(cls)

    def save(self=None):
        return 'save is called'

    def take(self=None):
        return 'take is called'
    
    def put(self=None):
        return 'put is called'

    def find(self=None):
        return 'find is called'

