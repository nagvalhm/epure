from ..savable import Savable
from ...named import NamedByClass
from abc import abstractmethod
from ..resource import Resource

class DbEntity(Savable, NamedByClass):
    name = ''
    namespace = ''

    @abstractmethod
    def __init__(self, name:str='', namespace:str='', resource:Resource=None) -> None:
        self.name = name if name else self.__class__.__name__
        self.namespace = namespace
        super().__init__(resource)

    # @property
    # def full_name(self):
    #     if hasattr(self, 'namespace') and self.namespace:
    #         return self.namespace + '.' + self.name
    #     if not (hasattr(self, 'name') and self.name):
    #         if isinstance(self, type):
    #             self.name = self.__name__
    #         else:
    #             self.name = self.__class__.__name__
    #     return self.name