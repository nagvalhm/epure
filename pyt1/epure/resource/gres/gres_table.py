from ..db.table import Table
from .gres_header import GresHeader
from .gres_entity import GresEntity
from typing import Dict, Any
from ..savable import Savable
from ...errors import  DbError

class GresTable(Table, GresEntity):
    def _set_header(self, header):
        if header == None:
            header = GresHeader(table=self)
        
        if isinstance(header, Dict):
            header = GresHeader(columns=header, table=self)
        
        self.header = header
        self.header.resource = self

    def serialize_create(self, node_dict: Dict[str, str]) -> str:

        columns = ""
        values = ""

        for name, val in node_dict.items():
            columns = columns + name + ', '
            values = values + val + ', '
        columns = columns[:-2]
        values = values[:-2]

        res = f'INSERT INTO {self.full_name}({columns}) VALUES ({values});'
        return res


    def serialize_update(self, node_dict: Dict[str, str]) -> str:

        if not ('res_id' in node_dict and node_dict['res_id']):
            raise DbError('unable update node without res_id')

        res_id = node_dict['res_id']
        pairs = ''

        for name, val in node_dict.items():
            pairs = pairs + name + ' = ' + val + ', '

        pairs = pairs[:-2]
        res = f'''UPDATE {self.full_name}
                SET {pairs}
                WHERE res_id = {res_id};'''
        return res