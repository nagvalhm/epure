from __future__ import annotations
from .edata import EData, TableData
from typing import Any, Dict, get_type_hints, Tuple
from ..savable import Savable
from ...errors import MultipleInheritanceError

class ProtoMeta(type):
    # def proto_cls(cls):
    #     if '_proto_cls' in vars(cls).keys():
    #         return cls._proto_cls

    @classmethod
    def savable_classes(mcl, bases):
        res = list(filter(lambda base: issubclass(base, Savable), bases))
        return res

    def __new__(mcl, name:str, bases:Tuple[type], namespace: dict[str, Any]) -> ProtoMeta:
        savable_classes = mcl.savable_classes(bases)
        if len(savable_classes) > 1:
            raise MultipleInheritanceError(f'{name} has more than one Savable parent: {str(savable_classes)}')
        res = super().__new__(mcl, name, bases, namespace)
        if len(savable_classes) == 1:
            res.__proto_cls__ = savable_classes[0]
        return res

class Proto(ProtoMeta, TableData):
    @property
    def annotations(self) -> Dict[str,Any]:
        if not hasattr(self, '_annotations'):
            if isinstance(self, type):
                self._annotations = self.get_self_annotations()
            else:
                self.__class__._annotations = self.get_self_annotations()
        return self._annotations

    @property
    def all_annotations(self) -> Dict[str,Any]:
        if not hasattr(self, 'all_annotations'):
            if isinstance(self, type):                
                self._all_annotations = get_type_hints(self)
            else:
                self.__class__._all_annotations = get_type_hints(self.__class__)
        return self._all_annotations

    @classmethod
    def get_self_annotations(cls):
        res = []
        all_annotations = get_type_hints(cls)
        self_annotations  = cls.__annotations__
        for annot_name in self_annotations:
            res[annot_name] = all_annotations[annot_name]
        res['__proto__'] = cls.__bases__[0]
        return res


    @property
    def __proto__(self) -> EData:
        proto_obj = self.__proto_cls__.__new__(proto_obj)
        for key in proto_obj.annotations:
            if key in vars(self):
                val = getattr(self, key)
                setattr(proto_obj, val)
        return proto_obj


    def set_proto_fields(self, proto:Savable):
        for attr_name in vars(proto):
            if attr_name in self.all_annotations:
                val = getattr(proto, attr_name)
                setattr(self, val)

    @classmethod
    def is_excluded(cls, atr_name:str, type_hint:Any='') -> bool:
        if atr_name == '__proto__':
            return False
        return super().is_excluded(atr_name, type_hint)