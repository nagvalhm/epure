from __future__ import annotations
from typing import Any
from configparser import SectionProxy, RawConfigParser
from ...helpers.string_helper import is_float, is_int, is_bool

class NoneIniSection:

    parser:RawConfigParser
    path:str

    def __init__(self, parser:RawConfigParser, path:str) -> None:
        self.parser = parser
        self.path = path

    def __getattr__(self, attr_name: str) -> Any:
        return self.get_next(attr_name)

    def get_next(self, attr_name: str) -> NoneIniSection:
        next_path = self.next_path(attr_name)
        if next_path in self.parser:
            return IniSection(self.parser, next_path)
        else:
            return NoneIniSection(self.parser, next_path)

    def next_path(self, attr_name: str) -> str:
        return '.'.join([self.path, attr_name])


class IniSection(NoneIniSection):

    section:SectionProxy


    def __init__(self, parser:RawConfigParser, path:str):
        if path not in parser:
            raise Exception('path not in parser')
        self.section = parser[path]
        super().__init__(parser, path)

    def __contains__(self, key: str) -> bool:
        return key in self.section


    def __getattr__(self, attr_name: str) -> Any:
        if attr_name not in self:
            return self.get_next(attr_name)

        attr_val = self.section[attr_name]
        return self._cast_val(attr_val)

        



    def _cast_val(self, attr_val: Any) -> Any:
        attr_is_float = is_float(attr_val)
        attr_is_int = is_int(attr_val, attr_is_float)

        if attr_is_int:
            return int(attr_val)
        elif attr_is_float:
            return float(attr_val)
        elif is_bool(attr_val):
            return attr_val.lower() == 'true'
        else:
            return attr_val



