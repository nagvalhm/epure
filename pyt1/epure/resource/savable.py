from types import NoneType
from .resource import Resource
from typing import Any

class Savable(Resource):    
    
    resource: Resource
    is_saved:bool=False
    #append to it, if u want excude
    __exclude__:list = ['resource', 'is_saved']


    def save(self, level:int=0, resource:Resource=None):
        pass

    def to_json(self):
        pass

    @classmethod
    def is_excluded(cls, atr_name:str, type_hint:Any='') -> bool:
        if hasattr(cls, '__exclude__') and atr_name in cls.__exclude__:
            return True
        if atr_name[:2] == "__" and atr_name[-2:] == "__":
            return True
        if type_hint in (NoneType, None):
            return True
        return False

    def execute(self, script: str = '') -> object:
        return self.resource.execute(script)