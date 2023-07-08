from __future__ import annotations
from types import LambdaType, NoneType
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast, Optional


from .constraint import NotNull

if TYPE_CHECKING:
    from .table import Table
    from .table_storage import TableStorage
from ..savable import Savable
from ...helpers.type_helper import check_type
from ...errors import EpureError
# from uuid import uuid4
from .table_column import TableColumn
from ..db.db_entity_resource import DbEntityResource
from .constraint import Constraint, NotNull, Default, Prim, Foreign, Uniq, Check
import uuid


class TableHeader(Savable):
    columns:Dict[str,TableColumn]
    deleted_columns:Dict[str, TableColumn]

    if TYPE_CHECKING:
        table:Table

    def __init__(self, 
            columns:Dict[str, type]=None, table:Table=None,
            name: str = '') -> None:
        check_type('columns', columns, [dict, NoneType])

        if table:
            self.table = table
        self.columns = {}
        self.deleted_columns = {}
        super().__init__(name)
        if not columns:
            return

        for name, py_type in columns.items():            
            column = TableColumn(name, py_type)
            column = cast(TableColumn, column)
            self.columns[name] = column

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

            if self_column.is_deleted:
                continue

            if self_column not in other:
                    res.append(self_column)
        return res

    def __contains__(self, other:Any) -> bool:
        if not isinstance(other, TableColumn):
            return other in self.columns
        column = cast(TableColumn, other)

        if column.is_deleted:
            return False

        if column.name not in self:
            return False

        self_column = self[column.name]

        if column == self_column:
            return True

        if isinstance(self_column.py_type, Constraint) or isinstance(column.py_type, Constraint):
            return False

        return self.db.same_db_type(self_column.py_type, column.py_type)

    def create(self, column: Savable) -> Any:
        check_type('column', column, TableColumn)

        script = ''
        restored_col_name = ''
        column_is_for_restore = False

        for restored_col_name, restored_column in self.deleted_columns:
            if restored_col_name[:-4] == f'{column.name}___del' and restored_column.py_type == column.py_type:
                script = self.serialize_for_restore(column)
                column_is_for_restore = True
                break

        if script == '':
            script = self.serialize_for_create(column)

        script = str(script)
        self.execute(script)

        if column_is_for_restore:
            self.deleted_columns.pop(restored_col_name)

        self.columns[column.name] = column

        return column

    def delete(self, column: Savable) -> Any:
        check_type('column', column, TableColumn)

        random_id = str(uuid.uuid4())[0:4]
        del_column_name = f'{column.name}___del{random_id}'

        script = self.serialize_for_delete(column, del_column_name)
        script = str(script)
        self.execute(script)

        self.columns.pop(column.name)
        self.deleted_columns[del_column_name] = column
        column.name = del_column_name

        return column

    def update(self, py_column: Savable) -> Any:
        check_type('py_column', py_column, TableColumn)

        py_column = cast(TableColumn, py_column)
        db_column = self.columns[py_column.name]

        if py_column in self:
            return db_column

        random_id = str(uuid.uuid4())[0:4]
        del_column_name = f'{py_column.name}___del{random_id}'

        script = ''
        restored_col_name = ''
        column_is_for_restore = False

        for restored_col_name, restored_column in self.deleted_columns.items():
            if restored_col_name[:-4] == f'{py_column.name}___del' and restored_column.py_type == py_column.py_type:

                script = self.serialize_for_restore(py_column, restored_col_name, del_column_name)
                column_is_for_restore = True
                break
        
        if script == '':
            script = self.serialize_for_update(py_column, del_column_name)
        script = str(script)
        self.execute(script)

        db_column.name = del_column_name
        self.deleted_columns[del_column_name] = db_column

        if column_is_for_restore:
            self.deleted_columns.pop(restored_col_name)
            
        self.columns[py_column.name] = py_column

        return db_column

    def serialize_for_create(self, column: Savable, **kwargs) -> object:
        check_type('column', column, TableColumn)
        column = cast(TableColumn, column)
        table_name = self.table.full_name

        db:DbEntityResource
        if 'db' in kwargs:
            db = kwargs['db']
        else:
            db = self.table.db        

        create_script = self._create_column_script(table_name, column, db)
        return create_script

    def serialize_for_update(self, column: Savable, del_column_name:str, **kwargs) -> object:
        check_type('column', column, TableColumn)
        column = cast(TableColumn, column)
        table_name = self.table.full_name

        pre_delete_script = self._serialize_pre_delete(table_name, column, del_column_name)

        db:DbEntityResource
        if 'db' in kwargs:
            db = kwargs['db']
        else:
            db = self.table.db

        create_script = self._create_column_script(table_name, column, db)

        migrate_script = ''
        if self.table.db.migrate_on_delete:
            migrate_script = self._migrate_columns_script(table_name, del_column_name, column.name)

        return pre_delete_script + create_script + migrate_script

    def serialize_for_delete(self, column: Savable, del_column_name:str, **kwargs) -> object:
        check_type('column', column, TableColumn)
        column = cast(TableColumn, column)
        table_name = self.table.full_name

        pre_delete_script = self._serialize_pre_delete(table_name, column, del_column_name)
        return pre_delete_script
    
    def serialize_for_restore(self, column:Savable, restore_col_name:str, del_column_name:str=None):
        check_type('column', column, TableColumn)
        restore_script = ''
        script = ''
        pre_delete_script = ''

        table_name = self.table.full_name
        column = cast(TableColumn, column)
        restore_script = self._serialize_for_restore(table_name, column, restore_col_name)
        if del_column_name:
            pre_delete_script = self._serialize_pre_delete(table_name, column, del_column_name)
        script = pre_delete_script + restore_script

        return script

    def _serialize_for_restore(self, table_name:str, column:TableColumn, restore_name) -> object:
        script = self._rename_column_script(table_name, restore_name, column.name)
        return script

    def _serialize_pre_delete(self, table_name:str, column:TableColumn, del_column_name:str) -> str:
        script = self._rename_column_script(table_name, column.name, del_column_name)\
                + self._set_nullable_script(table_name, del_column_name)
        return script

    def deserialize(self, column_dict: object, **kwargs) -> Savable:
        check_type('column_dict', column_dict, [dict, list])
        column_dict = cast(dict, column_dict)

        column_dict = self._deserialize(column_dict)

        column_name = column_dict['column_name']
        db_type = column_dict['db_type']

        not_null = column_dict['not_null']
        default = column_dict['default']
        uniq = column_dict['uniq']
        prim = column_dict['prim']
        foreign = column_dict['foreign']
        

        db = self._get_db(**kwargs)
        try:
            column_type = db.get_py_type(db_type)
            if prim:
                column_type = Prim[column_type]
            elif uniq:
                column_type = Uniq[column_type]
            elif not_null:
                column_type = NotNull[column_type, default]
            elif default:
                column_type = Default[column_type, default]
            elif foreign:                
                foreign_table = column_dict['foreign_table']
                foreign_column = column_dict['foreign_column']
                column_type = Foreign[column_type, foreign_table, foreign_column]
            

        except KeyError as ex:
            raise TypeError(f'{db_type} is unknown for {db.name} '
                            'set db_py_types attribute properly') from ex       
        
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

    def _set_nullable_script(self, table_name:str, column_name:str) -> str:
        raise NotImplementedError

    def _create_column_script(self, table_name:str, column:TableColumn, db:DbEntityResource) -> str:
        raise NotImplementedError

    def _migrate_columns_script(self, table_name:str, from_column:str, to_column:str) -> str:
        raise NotImplementedError

    def _set_column(self, column:TableColumn):
        check_type('column', column, TableColumn)
        if column.is_deleted:
            self.deleted_columns[column.name] = column
        else:
            self.columns[column.name] = column
    
    def serialize_read_column(self, column_name:str):
        raise NotImplementedError