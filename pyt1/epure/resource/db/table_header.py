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
from .table_column import TableColumn


class TableHeader(Savable):
    columns:Dict[str,TableColumn]
    table:Table

    def __init__(self, 
            columns:Dict[str, Any]=None, table:Table=None,
            name: str = '', res_id: object = None) -> None:
        check_type('columns', columns, [dict, NoneType])

        if table:
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

    @property
    def db(self):
        return self.table.db

    def __getitem__(self, key:str):
        return self.columns[key]

    def __iter__(self):
        res = self.columns.__iter__()
        return res

    def __len__(self):
        return self.columns.__len__()


    def __sub__(self, other: TableHeader) -> List[TableColumn]:
        res = []
        for column_name in self:
            self_column = self[column_name]

            if self_column not in other:
                res.append(self_column)
        return res

    def __contains__(self, other:Any) -> bool:
        if not isinstance(other, TableColumn):
            return other in self.columns
        column = cast(TableColumn, other)

        if column.name not in self:
            return False

        self_column = self[column.name]
        if self_column.column_type == 'Any' and \
            column.column_type in self.db.any_types:
            return True
        
        return column == self_column


    def create(self, column: Savable) -> Any:
        check_type('column', column, TableColumn)

        script = self.serialize(column, method=CREATE)
        script = str(script)
        self.execute(script)

        return column


    def update(self, new_column: Savable) -> Any:
        check_type('new_column', new_column, TableColumn)

        new_column = cast(TableColumn, new_column)
        old_column = self.columns[new_column.name]

        if new_column in self:
            return old_column

        script = self.serialize(new_column, method=UPDATE)
        script = str(script)
        self.execute(script)

        return old_column




    def serialize(self, column: Savable, method:str='', **kwargs) -> object:
        check_type('column', column, TableColumn)
        column = cast(TableColumn, column)
        script = ''

        table_name = self.table.full_name
        random_id = str(uuid4()).replace('-', '')
        del_column_name = f'{column.name}_deleted_{random_id}'

        if method == UPDATE:
            script = script + self._serialize_pre_delete(table_name, column, del_column_name)

        script = script + self._create_column_script(table_name, column)

        if self.table.db.migrate_on_delete:
            script = script + self._migrate_columns_script(table_name, del_column_name, column.name)

        return script


    def _serialize_pre_delete(self, table_name:str, column:TableColumn, del_column_name:str) -> str:
        script = self._rename_column_script(table_name, column.name, del_column_name)\
                + self._set_not_null_script(table_name, del_column_name)
        return script


    def deserialize(self, column_dict: object, **kwargs) -> Savable:
        check_type('column_dict', column_dict, [dict, list])
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

    def _get_db(self, **kwargs) -> TableStorage:

        db = None
        if 'db' in kwargs:
            db = kwargs['db']
            return db
        
        if hasattr(self, 'table') and hasattr(self.table, 'db'):
            db = self.table.db

        if db is None:
            raise EpureError('undefined db for column serialization')
        return db


    def _rename_column_script(self, table_name:str, old_name:str, new_name:str) -> str:
        raise NotImplementedError
        
    
    def _set_not_null_script(self, table_name:str, column_name:str) -> str:
        raise NotImplementedError

    def _create_column_script(self, table_name:str, column:TableColumn) -> str:
        raise NotImplementedError

    def _migrate_columns_script(self, table_name:str, from_column:str, to_column:str) -> str:
        raise NotImplementedError


    def _set_column(self, column:TableColumn):
        check_type('column', column, TableColumn)
        self.columns[column.name] = column