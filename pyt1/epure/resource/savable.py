from types import NoneType
from .resource import Resource
from typing import Any, Dict, get_type_hints

class Savable(Resource):    
    
    resource: Resource
    is_saved:bool=False
    _annotations: Dict[str,Any]
    #append to it, if u want excude
    __exclude__:list = ['resource', 'is_saved', '_annotations', 'cache_queue']
    

    def __init__(self, name: str = '', namespace: str = '', resource:Resource=None) -> None:
        if resource:
            self.resource = resource
        super().__init__(name, namespace)

    @property
    def annotations(self) -> Dict[str,Any]:
        if not hasattr(self, '_annotations'):
            if isinstance(self, type):                
                self._annotations = get_type_hints(self)
            else:
                self.__class__._annotations = get_type_hints(self.__class__)
        return self._annotations

    def save(self, asynch:bool=False):
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