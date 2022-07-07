from __future__ import annotations
from abc import abstractmethod
from typing import *
if TYPE_CHECKING:
    from .savable import Savable
from inflection import underscore

CREATE = 'CREATE'
READ = 'READ'
UPDATE = 'UPDATE'
DELETE = 'DELETE'

class Resource():

    res_id:object
    name:str
    namespace:str
    
    @abstractmethod
    def __init__(self, name:str='', res_id:object=None, namespace:str='') -> None:
        self.name = name if name else self.__class__.__name__
        self.namespace = namespace
        self.res_id = res_id if res_id else self.full_name
        

    @property
    def full_name(self):
        if self.namespace:
            return self.namespace + '.' + self.name
        return self.name

    def create(self, resource:Savable) -> Any:
        raise NotImplementedError

    def read(self, selector:object=None, **kwargs) -> Union[Resource, Sequence[Resource]]:
        raise NotImplementedError

    def update(self, resource:Savable) -> Any:
        raise NotImplementedError

    # def delete(resource:Savable, res_id=None ? Object):
    #     pass

    def create_all(self, savables:List[Savable]):
        pass
    def update_all(self, savables:List[Savable]):
        pass

    def serialize(self, resource:Savable, method:str='', **kwargs) -> object:
        pass

    def deserialize(self, resource:object, **kwargs) -> Savable:
        pass

    # def delete_all(?):
    #     pass

    def execute(self, script:str='') -> object:
        pass



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