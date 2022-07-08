from __future__ import annotations
from types import LambdaType, NoneType
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast, Optional

from .table_storage import TableStorage
from .constraints import NotNull

from tomlkit import table
if TYPE_CHECKING:
    from .table import Table
    from .db import Db
from ..savable import Savable
from ...helpers.type_helper import check_type
from ...errors import EpureError
from ..resource import UPDATE, CREATE
from uuid import uuid4


class TableColumn(Savable):
    column_type:str
    
    def __init__(self, name:str, column_type:str='') -> None:
        self.column_type = column_type
        super().__init__(name)

    
    def __eq__(self, other:TableColumn) -> bool:
        if self.name != other.name:
            return False            
        return self.column_type == other.column_type