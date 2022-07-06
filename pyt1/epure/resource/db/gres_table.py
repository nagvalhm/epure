from .table import Table, NotNull
from .table_header import TableHeader, TableColumn
from typing import Dict
from collections.abc import Sequence
from ...helpers.type_helper import check_type
from ..savable import Savable
from ..resource import UPDATE


class GresHeader(TableHeader):
    
    def _deserialize(self, column_dict: dict) -> dict:
        res = {'column_name': column_dict['column_name'],
                'is_nullable': (column_dict['is_nullable'] == 'YES'),
                'db_type': column_dict['data_type']}
        return res

    def serialize(self, column: Savable, method:str='', **kwargs) -> object:
        check_type('column', column, TableColumn)
        script = ''

        table_name = self.table.full_name
        if method == UPDATE:
            script = script + f'''
                ALTER TABLE {table_name} rename column str1 to str2;
            '''

class GresTable(Table):
    def _set_header(self, header):
        if header == None:
            header = GresHeader(table=self)
        
        if isinstance(header, Dict):
            header = GresHeader(columns=header, table=self)
        
        self.header = header
        self.header.resource = self

class JsonbTable(GresTable):
    pass