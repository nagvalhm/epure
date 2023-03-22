from __future__ import annotations
from types import NoneType
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast, Optional
from ..savable import Savable
from .constraint import Constraint
from .db_entity_resource import DbEntityResource
import re
from ...named import Named


class TableColumn(Savable, Named):
    py_type:type
    
    @property
    def is_deleted(self):
        # res = re.match(r'.*deleted_[a-f0-9]{32}', self.name)
        res = self.name[-10:-4] == '___del'
        if res:
            return res
        return res

    def __init__(self, name:str, py_type:type=NoneType) -> None:
        self.py_type = py_type
        self.name = name
        super().__init__()

    
    def __eq__(self, other:TableColumn) -> bool:
        if self.name != other.name:
            return False            
        return self.py_type == other.py_type

    def serialize_type(self, db:DbEntityResource):
        py_type = self.py_type
        if isinstance(py_type, Constraint):
            return db.serialize_constraint(py_type)
        return db.get_db_type(py_type)