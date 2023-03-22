from inflection import underscore
from abc import abstractmethod

class Named:
    name:str
    namespace:str

    @abstractmethod
    def __init__(self, name:str=None, namespace:str=None) -> None:
        if name is not None:
            self.name = name
        if namespace is not None:
            self.namespace = namespace

    @property
    def full_name(self):
        res = None
        if hasattr(self, 'name'):
            res = self.name
        if hasattr(self, 'namespace') and self.namespace and res:
            res = self.namespace + '.' + res

        return res
    
class NamedByClass(Named):

    @property
    def full_name(self):
        res = super().full_name
        if res is not None:
            return res
        if isinstance(self, type):
            return self.__name__
        else:
            return self.__class__.__name__

    
    
class FullName(Named):
    pass

class SnakeCaseNamed(FullName):
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = underscore(val)

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, val):
        self._namespace = underscore(val)