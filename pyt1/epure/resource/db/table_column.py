from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast, Optional
from ..savable import Savable



class TableColumn(Savable):
    column_type:str
    
    def __init__(self, name:str, column_type:str='') -> None:
        self.column_type = column_type
        super().__init__(name)

    
    def __eq__(self, other:TableColumn) -> bool:
        if self.name != other.name:
            return False            
        return self.column_type == other.column_type