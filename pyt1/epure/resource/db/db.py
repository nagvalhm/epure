from __future__ import annotations
from abc import abstractmethod
from typing import Dict, Any, Type, cast
import logging

from ..savable import Savable
from .table import Table
from ...resource.resource import Resource, FullName, SnakeCaseNamed
from urllib.parse import urlparse
from ...errors import EpureError
from ...helpers.type_helper import check_subclass, check_type
from inflection import underscore


class Db(Resource):

    database:str
    user:str
    password:str
    host:str
    port:str    
    params:Dict[str,str]

    log_level:int = logging.NOTSET
    logger:logging.Logger = None
    connection:Any
    default_namespace:str
    py_db_types:Dict[str, str]
    db_py_types:Dict[str, str]
    tables:Dict[str,Table]
    default_table_type:Type[Table] = Table
    migrate_on_delete:bool = False


    def __getitem__(self, key:str):
        return self.tables[key]

    def __iter__(self):
        return self.tables.__iter__()

    def __len__(self):
        return self.tables.__len__()

    @property
    def any_types(self):
        if hasattr(self, '_any_types'):
            return self._any_types
        res = []
        any_db_type = self.get_db_type('Any')
        for py_type, db_type in self.py_db_types.items():
            if db_type == any_db_type:
                res.append(py_type)
        self._any_types = res
        return res


    def _set_table(self, table:Table):
        self.tables[table.full_name] = table
        if table.namespace == self.get_default_namespace():
            self.tables[table.name] = table
        table.resource = self



    def create(self, table: Savable):
        check_type('table', table, self.default_table_type)
        table = cast(Table, table)

        script = self.serialize(table)
        self.execute(script)

        self._set_table(table)
        return table


    def update(self, new_table: Savable) -> Any:
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

    
    @abstractmethod
    def __init__(self, 
                connect_str:str='', 
                database:str='', 
                user:str='', 
                password:str='',
                host:str='', 
                port:str='', 
                default_namespace='', 
                log_level:int = logging.NOTSET,
                name:str='', res_id:object=None,
                default_table_type:type=None,
                migrate_on_delete:bool=False):
        


        connect_params = urlparse(connect_str)

        self.database = (database or connect_params.scheme)
        self.user = user or str(connect_params.username)
        self.password = password or str(connect_params.password)
        self.host = host or str(connect_params.hostname)
        self.port = port or str(connect_params.port)        

        if default_namespace:
            self.default_namespace = default_namespace

        if log_level:
            self.log_level = log_level
        if default_table_type:
            self.default_table_type = default_table_type

        self.tables = {}
        self.set_logger()

        return super().__init__(name, res_id)



    def set_logger(self) -> Any:
        if self.log_level > logging.NOTSET:
            self.logger = logging.getLogger(__name__)
            
            self.logger.setLevel(self.log_level)
            fileHandler = logging.FileHandler('epure_db.log', mode='a+')
            fileHandler.setLevel(self.log_level)
            formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s:\n %(message)s')
            fileHandler.setFormatter(formater)

            self.logger.addHandler(fileHandler)
            

    def __contains__(self, table_name:str) -> bool:
        full_name = self._get_full_table_name(table_name)
        if full_name.full_name in self.tables:
            return True
        table = self.read(table_name)
        return bool(table)




    def execute(self, script: str = '') -> list:
        result = []
        
        if self.logger:
            self.logger.debug(script)
        try:
            script = script.replace("\n", "")
            result = self._execute(script)
        except Exception as ex:
            err = EpureError(f'unnable execute script {script}: {ex}') \
                .with_traceback(ex.__traceback__)
            if self.logger:
                self.logger.error(err, exc_info=True)
                
            raise err
        return result

    def _execute(self, script: str = '') -> list:
        raise NotImplementedError()


    
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

    def get_default_namespace(self):
        return underscore(self.default_namespace)


    def deserialize(self, table_columns: object) -> Savable:
        check_type('table_columns', table_columns, list)
        table_columns = cast(list, table_columns)

        full_name = self._deserialize_table_name(table_columns)

        TableCls = self.default_table_type
        table = TableCls(name=full_name.name, namespace=full_name.namespace)
        table.resource = self
        
        for column_dict in table_columns:
            column = table.header.deserialize(column_dict, db=self)
            table.header._set_column(column)
        
        return table





    def get_db_type(self, py_type:str):
        return self.py_db_types[py_type]

    def get_py_type(self, db_type:str):
        return self.db_py_types[db_type]