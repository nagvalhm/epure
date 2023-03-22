from __future__ import annotations
from typing import TYPE_CHECKING, Any, List
if TYPE_CHECKING:
    from .savable import Savable
from queue import Queue

# CREATE = 'CREATE'
# READ = 'READ'
# UPDATE = 'UPDATE'
# DELETE = 'DELETE'

class Resource():

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