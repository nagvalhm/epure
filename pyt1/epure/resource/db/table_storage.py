from __future__ import annotations
from abc import abstractmethod
from typing import Dict, Any, Type, cast

from epure.errors import DbError
from .table_column import TableColumn

from ..resource import FullName, SnakeCaseNamed
from ..savable import Savable
from .table import Table
from .db_entity_resource import DbEntityResource
from ...helpers.type_helper import check_subclass, check_type
from ...epure import Epure

class TableStorage(DbEntityResource):

    tables:Dict[str,Table]
    default_table_type:Type[Table] = Table
    migrate_on_delete:bool = False
    _epures: Dict[str, type] = None

    @abstractmethod
    def __init__(self, name:str='', default_table_type:Type[Table]=None, 
    migrate_on_delete:bool=False):

        if default_table_type:
            self.default_table_type = default_table_type

        self.migrate_on_delete = migrate_on_delete

        super().__init__(name) 


        
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

        script = self.serialize_for_create(table)
        script = str(script)
        self.execute(script)

        self._set_table(table)
        return table

    def update_table(self, py_table: Savable) -> Any:
        check_type('py_table', py_table, Table)

        py_table = cast(Table, py_table)        
        db_table = self.tables[py_table.full_name]

        py_header = py_table.header
        db_header = db_table.header

        diff = py_header - db_header

        for column in diff:
            if column.name in db_header:
                db_header.update(column)
            else:
                db_header.create(column)
        
        diff = db_header - py_header
        for column in diff:
            db_header.delete(column)

        self._set_table(py_table)
        return py_table


    def deserialize_table(self, table_columns: object) -> Table:
        check_type('table_columns', table_columns, list)
        table_columns = cast(list, table_columns)

        full_name = self._deserialize_table_name(table_columns)

        TableCls = self._get_table_type(table_columns)
        table = TableCls(name=full_name.name, namespace=full_name.namespace, resource=self)
        
        
        for column_dict in table_columns:
            column = table.header.deserialize(column_dict, db=self)
            column = cast(TableColumn, column)
            table.header._set_column(column)
        
        return table


    def get_epure_by_table_name(self, table_name: str):
        if self._epures == None:            
            self._epures = self._get_epures_dict()
        if table_name not in self._epures:
            from ...epure import Epure
            self._epures[table_name] = self._get_epure_by_table_name()
        if table_name not in self._epures:
            return None
            # raise DbError('no one epure has this table as resource')
        return self._epures[table_name]
    
    def _get_epures_dict(self):        
        res = {}
        for ep in Epure.epures:
            table_name = ep.resource.full_name
            if table_name in self:
                res[table_name] = ep
        # if not res:
        #     raise DbError('no one epure has table as resource')
        return res
    
    def _get_epure_by_table_name(self, table_name: str):
        for ep in Epure.epures:
            if ep.resource.full_name in self:
                return ep
        return None
        
    def _get_table_type(self, table_columns:list):
        return self.default_table_type

    def _deserialize_table_name(self, table_columns:list) -> FullName:
        raise NotImplementedError

    def _set_table(self, table:Table):
        self.tables[table.full_name] = table
        if table.namespace == self.get_default_namespace():
            self.tables[table.name] = table
        table.resource = self


    # def get_table_for_resource(self, resource: Savable, table_name: str = '') -> Table:
    #     table:Table

    #     full_name = self._get_full_table_name(table_name)
    #     columns = self.get_annotations(resource)
    #     columns = {name: val
    #         for name, val in columns.items() if
    #         not resource.is_excluded(name)}

    #     TableCls = self.default_table_type
    #     table = TableCls(full_name.name, columns, full_name.namespace)
    #     return table

    # def get_annotations(self, resource: Savable):
        
    #     res = {}
    #     resource_cls:type
    #     if isinstance(resource, type):
    #         resource_cls = resource
    #     resource_cls = resource.__class__

    #     res = resource.__annotations__
        
    #     for cls in resource_cls.mro():
    #         res.update(cls.__annotations__)


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