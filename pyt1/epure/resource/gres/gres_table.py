from ..db.table import Table
from .gres_header import GresHeader
from .gres_entity import GresEntity
from typing import Dict, Any, List
from ..savable import Savable
from ...errors import  DbError
from ..db.select_query import SelectQuery
from ..db.term import JoinBinary, Pseudo, _PseudoColumn, _PseudoTable
from uuid import uuid4

class GresTable(Table, GresEntity):
    def _set_header(self, header):
        if header == None:
            header = GresHeader(table=self)
        
        if isinstance(header, Dict):
            header = GresHeader(columns=header, table=self)
        
        self.header = header
        self.header.resource = self



    def serialize_for_create(self, node: Savable, **kwargs) -> object:

        node_dict = self._serialize(node)

        columns = ""
        values = ""

        for name, val in node_dict.items():
            columns = columns + name + ', '
            values = values + val + ', '
        columns = columns[:-2]
        values = values[:-2]

        res = f'INSERT INTO {self.full_name}({columns}) VALUES ({values}) returning node_id;'
        return res



    def serialize_read(self, selector:SelectQuery) -> str:
        header = self.serialize_select_header(selector.header)
        joins = self.serialize_joins(selector.joins)        

        res = f'{header} \n {joins} WHERE \n {selector.where_clause}'
        res = self.replace_operators(res)
        return res



    def serialize_select_header(self, header:List[Pseudo]):
        res = 'SELECT'
        for item in header:
            if isinstance(item, _PseudoColumn):
                res += f' {str(item)},'
            elif isinstance(item, _PseudoTable):
                res += f' {str(item)}.*,'
        res = res[:-1]

        first_item = header[0]
        table_name = ''
        if isinstance(first_item, _PseudoColumn):
            table_name = first_item.table.full_name
        elif isinstance(first_item, _PseudoTable):
            table_name = str(first_item)
        res = res + f' FROM {table_name}'
        return res


    def replace_operators(self, where_clause:str):
        if not (self.db and self.db.py_db_operators):
            return where_clause
        for py_op, db_op in self.db.py_db_operators.items():
            where_clause = where_clause.replace(f' {py_op} ', f' {db_op} ')
        return where_clause



    def serialize_joins(self, joins:List[JoinBinary]):
        res = ''
        for join in joins:
            ser_join = self.serialize_join(join)
            res += ser_join        
        return res

    def serialize_join(self, join:JoinBinary):
        return f'{join.join_type} JOIN {join.table} on {join.on_clause}\n'

        

    def serialize_for_update(self, node: Savable, **kwargs) -> object:

        node_dict = self._serialize(node)

        if not ('node_id' in node_dict and node_dict['node_id']):
            raise DbError('unable update node without node_id')

        node_id = node_dict['node_id']
        pairs = ''

        for name, val in node_dict.items():
            pairs = pairs + name + ' = ' + val + ', '

        pairs = pairs[:-2]
        res = f'''UPDATE {self.full_name}
                SET {pairs}
                WHERE node_id = {node_id};'''
        return res


    def generate_id(self, resource: Savable = None):
        return uuid4()