from ..db.table import Table
from .gres_header import GresHeader
from .gres_entity import GresEntity
from typing import Dict, Any, List
from ..savable import Savable
from ...errors import  DbError, EpureParseError
# from ..db.select_query import SelectQuery
# from ..db.term import JoinBinary, Pseudo, _PseudoColumn, _PseudoTable
from ...parser.leaf import QueryingProxy, ColumnProxy, TableProxy
from ...parser.term_parser import JoinOperation
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



    def serialize_read(self, header, joins, where_clause, full_names) -> str:
        header = list(header) + self._get_extra_node_id_fields(header)
        res_header = self.serialize_select_header(header, full_names)
        res_joins = self.serialize_joins(joins)        

        res = f'{res_header} \n {res_joins} WHERE \n {where_clause}'
        res = self.replace_operators(res)
        return res



    def serialize_select_header(self, header:List[QueryingProxy], full_names:bool):
        res = 'SELECT'
        for item in header:
            if isinstance(item, ColumnProxy):
                res += f' {item.str(False, full_names)},'
            elif isinstance(item, TableProxy):
                res += f' {item.str(False, full_names)}.*,'
            else:
                raise EpureParseError('select header item must be ColumnProxy or TableProxy')
        res = res[:-1]

        first_item = header[0]
        table_name = ''
        if isinstance(first_item, ColumnProxy):
            table_name = first_item.__table__.full_name
        elif isinstance(first_item, TableProxy):
            table_name = str(first_item)
        res = res + f' FROM {table_name}'
        return res



    def replace_operators(self, where_clause:str):
        if not (self.db and self.db.py_db_operators):
            return where_clause
        for py_op, db_op in self.db.py_db_operators.items():
            where_clause = where_clause.replace(f' {py_op} ', f' {db_op} ')
        return where_clause



    def serialize_joins(self, joins:List[JoinOperation]):
        res = ''
        for join in joins:
            ser_join = self.serialize_join(join)
            res += ser_join        
        return res

    def serialize_join(self, join:JoinOperation):
        return f'{join.join_type} JOIN {join.table} on {join.on_clause} \n'

        

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