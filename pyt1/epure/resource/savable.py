from .resource import Resource
from typing import *

class Savable(Resource):
    
    __exclude__:list
    resource: Resource


    def save(self, level:int=0, resource:Optional[Resource]=None):
        pass

    def serialize(self):
        pass

    def deserialize(self):
        pass

    def is_excluded(self, atr_name:str) -> bool:
        if hasattr(self, '__exclude__') and atr_name in self.__exclude__:
            return False
        if atr_name[:2] == "__" and atr_name[-2:] == "__":
            return False
        return True