from __future__ import annotations
from types import NoneType
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast, Optional
from ..savable import Savable
from .constraint import Constraint
from .db_entity_resource import DbEntityResource


class TableColumn(Savable):
    column_type:type
    
    def __init__(self, name:str, column_type:type=NoneType) -> None:
        self.column_type = column_type
        super().__init__(name)

    
    def __eq__(self, other:TableColumn) -> bool:
        if self.name != other.name:
            return False            
        return self.column_type == other.column_type

    def serialize_type(self, db:DbEntityResource):
        column_type = self.column_type
        if isinstance(column_type, Constraint):
            return db.serialize_constraint(column_type)
        return db.get_db_type(column_type)