from __future__ import annotations
from abc import abstractmethod
from typing import Dict, Any, Type, cast
from .table_column import TableColumn

from ..resource import FullName, SnakeCaseNamed
from ..savable import Savable
from .table import Table
from .db_entity_resource import DbEntityResource
from ...helpers.type_helper import check_subclass, check_type

class TableStorage(DbEntityResource):

    tables:Dict[str,Table]
    default_table_type:Type[Table] = Table
    migrate_on_delete:bool = False

    @abstractmethod
    def __init__(self, name:str='', default_table_type:Type[Table]=None, 
    res_id:object=None, migrate_on_delete:bool=False):

        if default_table_type:
            self.default_table_type = default_table_type

        self.migrate_on_delete = migrate_on_delete

        super().__init__(name, res_id) 


        
    def __getitem__(self, key:str):
        return self.tables[key]

    def __iter__(self):
        return self.tables.__iter__()

    def __len__(self):
        return self.tables.__len__()

    def __contains__(self, table_name:str) -> bool:
        full_name = self._get_full_table_name(table_name)
        if full_name.full_name in self.tables:
            return True
        table = self.read(table_name)
        return bool(table)
        



    def create_table(self, table: Savable):
        check_type('table', table, self.default_table_type)
        table = cast(Table, table)

        script = self.serialize(table)
        script = str(script)
        self.execute(script)

        self._set_table(table)
        return table

    def update_table(self, new_table: Savable) -> Any:
        check_type('new_table', new_table, Table)

        new_table = cast(Table, new_table)        
        old_table = self.tables[new_table.full_name]

        new_header = new_table.header
        old_header = old_table.header

        diff = new_header - old_header
        if not diff:
            return old_table

        for column in diff:
            if column.name in old_header:
                old_header.update(column)
            else:
                old_header.create(column)

        self._set_table(new_table)
        return new_table


    def deserialize_table(self, table_columns: object) -> Table:
        check_type('table_columns', table_columns, list)
        table_columns = cast(list, table_columns)

        full_name = self._deserialize_table_name(table_columns)

        TableCls = self.default_table_type
        table = TableCls(name=full_name.name, namespace=full_name.namespace)
        table.resource = self
        
        for column_dict in table_columns:
            column = table.header.deserialize(column_dict, db=self)
            column = cast(TableColumn, column)
            table.header._set_column(column)
        
        return table

        
    def _deserialize_table_name(self, table_columns:list) -> FullName:
        raise NotImplementedError

    def _set_table(self, table:Table):
        self.tables[table.full_name] = table
        if table.namespace == self.get_default_namespace():
            self.tables[table.name] = table
        table.resource = self


    def get_table_for_resource(self, resource: Savable, table_name: str = '') -> Table:
        table:Table

        full_name = self._get_full_table_name(table_name)        
        columns = resource.__annotations__
        columns = {name: val
            for name, val in columns.items() if
            not resource.is_excluded(name)}

        TableCls = self.default_table_type
        table = TableCls(full_name.name, columns, full_name.namespace)
        return table

    def _get_full_table_name(self, table_name:str) -> FullName:
        table_name = table_name
        full_name = table_name.split('.')
        if len(full_name) > 2:
            raise NameError('table_name name must have no more then one dot')
        if len(full_name) == 1:
            default_namespace = self.get_default_namespace()
            full_name.insert(0, default_namespace)

        res = SnakeCaseNamed(namespace=full_name[0], name=full_name[1])
        return res