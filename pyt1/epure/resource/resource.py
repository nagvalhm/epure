from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING, Any, List
if TYPE_CHECKING:
    from .savable import Savable
from inflection import underscore
from queue import Queue

# CREATE = 'CREATE'
# READ = 'READ'
# UPDATE = 'UPDATE'
# DELETE = 'DELETE'

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
        

    def create(self, savable:Savable, asynch:bool=False) -> object:
        raise NotImplementedError

    def serialize_for_create(self, savable:Savable, **kwargs) -> object:
        raise NotImplementedError

    def read(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def serialize_for_read(self, savable:Savable, **kwargs) -> object:
        raise NotImplementedError

    def update(self, savable:Savable, asynch:bool=False) -> object:
        raise NotImplementedError

    def serialize_for_update(self, savable:Savable,  **kwargs) -> object:
        raise NotImplementedError

    def delete(self, savable:Savable, asynch:bool=False):
        raise NotImplementedError

    def serialize_for_delete(self, savable:Savable,  **kwargs) -> object:
        raise NotImplementedError


    #all

    def create_all(self, savables:List[Savable]):
        raise NotImplementedError

    def update_all(self, savables:List[Savable], selector:object):
        raise NotImplementedError

    def delete_all(self, savables:List[Savable], selector:object):
        raise NotImplementedError



    def deserialize(self, savable:object, **kwargs) -> Savable:
        raise NotImplementedError

    def cache(self, script:str):
        raise NotImplementedError  

    def execute(self, script:str='') -> object:
        raise NotImplementedError

    def generate_id(self, savable:Savable=None):
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