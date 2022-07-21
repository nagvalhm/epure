from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Union, Sequence, List
if TYPE_CHECKING:
    from .savable import Savable
from inflection import underscore
from queue import Queue

CREATE = 'CREATE'
READ = 'READ'
UPDATE = 'UPDATE'
DELETE = 'DELETE'

class Resource():
    
    
    name = ''
    namespace = ''

    
    @abstractmethod
    def __init__(self, name:str='', namespace:str='') -> None:
        self.name = name if name else self.__class__.__name__
        self.namespace = namespace
        

    @property
    def full_name(self):
        if hasattr(self, 'namespace') and self.namespace:
            return self.namespace + '.' + self.name
        if not (hasattr(self, 'name') and self.name):
            if isinstance(self, type):
                self.name = self.__name__
            else:
                self.name = self.__class__.__name__
        return self.name
        

    def create(self, resource:Savable) -> object:
        raise NotImplementedError

    def read(self, selector:object=None, **kwargs) -> Any: #Union[Resource, Sequence[Resource]]:
        raise NotImplementedError

    def update(self, resource:Savable) -> object:
        raise NotImplementedError

    def delete(resource:Savable):
        raise NotImplementedError

    def delete_all(resource:Savable, selector:object):
        raise NotImplementedError

    def create_all(self, savables:List[Savable]):
        raise NotImplementedError

    def update_all(self, savables:List[Savable], selector:object):
        raise NotImplementedError


    def serialize(self, resource:Savable, method:str='', **kwargs) -> object:
        raise NotImplementedError

    def deserialize(self, resource:object, **kwargs) -> Savable:
        raise NotImplementedError

    def cache(self, resource:Savable, method:str=''):
        raise NotImplementedError

  

    def execute(self, script:str='') -> object:
        raise NotImplementedError


    def generate_id(self, resource:Savable=None):
        raise NotImplementedError



class FullName(Resource):
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