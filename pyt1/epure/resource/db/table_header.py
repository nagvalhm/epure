from __future__ import annotations
from types import LambdaType, NoneType
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast
from .constraints import NotNull

from tomlkit import table
if TYPE_CHECKING:
    from .table import Table
    from .db import Db
from ..savable import Savable
from ...helpers.type_helper import check_type
from ...errors import EpureError
from ..resource import UPDATE, CREATE
from inflection import underscore

class TableColumn(Savable):
    column_type:str
    
    def __init__(self, name:str, column_type:str='') -> None:
        self.column_type = column_type
        super().__init__(name)

    def __eq__(self, other:TableColumn) -> bool:
        return self.name == other.name and\
            self.column_type == other.column_type

class TableHeader(Savable):
    columns:Dict[str,TableColumn]
    table:Table

    def __sub__(self, other: TableHeader) -> List[TableColumn]:
        res = []
        for column_name in self:
            in_other = (column_name in other) and self[column_name] == other[column_name]
            if not in_other:
                res.append(self[column_name])
        return res

    def update(self, new_column: Savable) -> Any:
        check_type('new_column', new_column, TableColumn)

        new_column = cast(TableColumn, new_column)
        old_column = self.columns[new_column.name]

        if new_column.column_type == old_column.column_type:
            return old_column

        script = self.serialize(new_column, method=UPDATE)
        self.execute(script)

        return old_column

    def create(self, column: Savable) -> Any:
        check_type('column', column, TableColumn)

        script = self.serialize(column, method=CREATE)
        self.execute(script)

        return column




    def deserialize(self, column_dict: object, **kwargs) -> Savable:
        check_type('column_dict', column_dict, dict)
        column_dict = cast(dict, column_dict)

        column_dict = self._deserialize(column_dict)

        column_name = column_dict['column_name']
        is_nullable = column_dict['is_nullable']
        db_type = column_dict['db_type']

        db = self._get_db(**kwargs)
        try:
            column_type = db.get_py_type(db_type)
        except KeyError as ex:
            raise TypeError(f'{db_type} is unknown for {db.name} '
                            'set db_py_types attribute properly') from ex
        # colum_type = TypeVar('colum_type', bound=colum_type)
        if not is_nullable:
            column_type = NotNull[column_type]
        
        return TableColumn(column_name, column_type)

    def _deserialize(self, column_dict:dict) -> dict:
        return column_dict

    def _get_db(self, **kwargs) -> Db:
        db = kwargs['db']

        if not db:
            db = self.table.db
        if not db:
            raise EpureError('undefined db for column serialization')
        return db



    def __init__(self, 
            columns:Dict[str, Any]=None, table:Table=None,
            name: str = '', res_id: object = None) -> None:
        check_type('columns', columns, [dict, NoneType])

        self.table = table
        self.columns = {}
        super().__init__(name, res_id)
        if not columns:
            return

        for name, val in columns.items():
            if isinstance(val, str):
                val = TableColumn(name, val)
            val = cast(TableColumn, val)
            self.columns[name] = val


    def __getitem__(self, key:str):
        return self.columns[key]

    def keys(self):
        return self.columns.keys()

    def _set_column(self, column:TableColumn):
        check_type('column', column, TableColumn)
        self.columns[column.name] = column



    # def serialize(self, column: Savable, **kwargs) -> object:
    #     check_type('column', column, TableColumn)
    #     column = cast(TableColumn, column)

    #     db = self._get_db(**kwargs)
    #     res = {
    #         "column_name": underscore(column.name),
    #         "column_type": db.get_db_type(column.column_type)
    #     }

    #     return res