from .resource import Resource
from typing import *

class Savable(Resource):
    
    __exclude__:list
    resource: Resource


    def save(self, level:int=0, resource:Optional[Resource]=None):
        pass

    def to_json(self):
        pass

    @classmethod
    def is_excluded(cls, atr_name:str) -> bool:
        if hasattr(cls, '__exclude__') and atr_name in cls.__exclude__:
            return True
        if atr_name[:2] == "__" and atr_name[-2:] == "__":
            return True
        return False

    def execute(self, script: str = '') -> object:
        return self.resource.execute(script)