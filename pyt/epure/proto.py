from __future__ import annotations
from typing import Any
import re



class Proto:
    __proto__:Proto

    def __setattr__(self, name: str, value: Any) -> None:
        self_cls = type(self)
        if not self_cls.is_special_attr(name):
            return super().__setattr__(name, value)

        if not hasattr(self_cls, name):
            raise AttributeError(f'{type(self)} object has no attribute {name}')

    def __getattribute__(self, name: str) -> Any:
        self_cls = type(self)
        if not self_cls.is_special_attr(name):            
            return super().__getattribute__(name)

        if not hasattr(self_cls, name):
            raise AttributeError(f'{type(self)} object has no attribute {name}')

    @staticmethod
    def is_special_attr(name: str) -> bool:
        pattern = re.compile(r"___.*___")
        res = bool(pattern.match(name))
        if not res:
            print(f'{name} is not special')
        
        return res