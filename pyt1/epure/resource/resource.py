from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from .savable import Savable



class Resource():

    res_id:object
    name:str
    
    def __init__(self) -> None:
        pass

    def create(self, resource:Savable, res_id=None):
        pass
    def read(self, selector:object, **kwargs):
        pass
    def update(self, resource:Savable, res_id=None):
        pass

    # def delete(resource:Savable, res_id=None ? Object):
    #     pass

    def create_all(self, savables:List[Savable]):
        pass
    def update_all(self, savables:List[Savable]):
        pass

    # def delete_all(?):
    #     pass

    def execute(self, script:str=''):
        pass