from __future__ import annotations
from abc import abstractmethod
from typing import *
if TYPE_CHECKING:
    from .savable import Savable



class Resource():

    res_id:object
    name:str
    
    @abstractmethod
    def __init__(self, name:str='', res_id:object=None) -> None:
        self.name = name if name else self.__class__.__name__
        self.res_id = res_id if res_id else self.name

    def create(self, resource:Savable, res_id:object=None) -> Any:
        raise NotImplementedError

    def read(self, selector:object=None, **kwargs) -> Union[Resource, Sequence[Resource]]:
        raise NotImplementedError

    def update(self, resource:Savable, res_id:object=None) -> Any:
        raise NotImplementedError

    # def delete(resource:Savable, res_id=None ? Object):
    #     pass

    def create_all(self, savables:List[Savable]):
        pass
    def update_all(self, savables:List[Savable]):
        pass

    # def delete_all(?):
    #     pass

    def execute(self, script:str='') -> object:
        pass