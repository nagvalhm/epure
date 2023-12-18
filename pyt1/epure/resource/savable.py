from __future__ import annotations
from types import NoneType
from .resource import Resource
from typing import Any, Dict, get_type_hints, Callable
from .db.constraint import Constraint

class Savable(Resource):    
    
    resource: Resource
    is_saved:bool=False
    _annotations: Dict[str,Any]
    #append to it, if u want exclude
    __exclude__:list = ['resource', 'is_saved', '_annotations', 'cache_queue']
    

    def __init__(self, resource:Resource=None) -> None:
        if resource != None:
            self.resource = resource
        super().__init__()

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

    # def to_json(self) -> str:
    #     raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def is_excluded(self, edata, atr_name:str, type_hint:Any='') -> bool:
        cls = type(edata)
        if isinstance(edata, type):
            cls = edata

        if hasattr(cls, '__exclude__') and atr_name in cls.__exclude__:
            return True
        if atr_name[:2] == "__" and atr_name[-2:] == "__":
            return True
        if atr_name in ("prepared_resource"):
            return True
        # if type_hint in (NoneType, None):
        #     return True
        return False

    def execute(self, script: str = '') -> object:
        return self.resource.execute(script)
    
    def _serialize(self, edata: Savable, serializer:Callable, rec_depth:int=None, *args) -> Dict[str, str]:
        res = {}
        for field_name, field_type in edata.annotations.items():
            if isinstance(field_type, Constraint):
                field_type = field_type.py_type
                
            # if edata.is_excluded(field_name, field_type):
            #     continue
            if self.is_excluded(edata, field_name, field_type):
                continue
            # if field_name not in self.header:
            #     continue
            if not hasattr(edata, field_name):
                continue

            field_val = getattr(edata, field_name, None)

            field_val = serializer(field_val, field_type, field_name, rec_depth, args)
            
            # field_val = self._serialize_field_val(field_val, field_type)

            res[field_name] = field_val
        
        return res
    
    # def _serialize_field_val(field_val, field_type=None):
    #     raise NotImplementedError