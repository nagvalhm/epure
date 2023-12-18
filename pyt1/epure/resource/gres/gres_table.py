from ..db.table import Table
from .gres_header import GresHeader
from .gres_entity import GresEntity
from typing import Dict, Any, List
from ..savable import Savable
from ...errors import  DbError, EpureParseError
# from ..db.select_query import SelectQuery
# from ..db.term import JoinBinary, Pseudo, _PseudoColumn, _PseudoTable
from ...parser.leaf import QueryingProxy, ColumnProxy, Model
from ...parser.proxy_base_cls import ColumnProxyBase, ModelBase
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



    def serialize_for_create(self, edata: Savable, **kwargs) -> object:

        data_dict = self._serialize(edata, self._serialize_field_val_to_sql)

        columns = ""
        values = ""

        for name, val in data_dict.items():
            columns = columns + name + ', '
            values = values + val + ', '
        columns = columns[:-2]
        values = values[:-2]

        res = f'INSERT INTO {self.full_name}({columns}) VALUES ({values}) returning data_id;'
        return res

    # def serialize_read(self, header, joins, where_clause, full_names) -> str:
    #     header = self._add_node_id_fields(header)
    #     res_header = self.serialize_read_header(header, full_names)
    #     res_joins = self.serialize_joins(joins)        

    #     if where_clause:
    #         res = f'{res_header} \n {res_joins} WHERE \n {where_clause}'
    #     else:
    #         res = f'{res_header} \n {res_joins}'
    #     res = self.replace_operators(res)
    #     return res

    def serialize_read(self, header, joins, where_clause, full_names, include_data_id:bool=True) -> str:
        if include_data_id:
            header = self._add_data_id_fields(header)
        res_header = self.serialize_read_header(header, full_names)
        res_joins = self.serialize_joins(joins)        

        if where_clause:
            res = f'{res_header} \n {res_joins} WHERE \n {where_clause}'
        else:
            res = f'{res_header} \n {res_joins}'
        # res = self.replace_operators(res)
        return res
    
    def serialize_for_delete(self, data_id) -> str:
        #here
        return f"DELETE FROM {self.full_name} WHERE data_id = '{str(data_id)}'"



    def serialize_read_header(self, header:List[QueryingProxy], full_names:bool):
        res = 'SELECT'
        for item in header:
            if isinstance(item, ColumnProxyBase):
            # if isinstance(item, self.db.parser.column_proxy_cls):
                res += f' {item.serialize(False, full_names, True)},'
            elif isinstance(item, ModelBase):
            # elif isinstance(item, self.db.parser.model_cls):
                res += f' {item.serialize(False, full_names, True)},'
            elif isinstance(item, str):
                sp = item.split('.')
                if len(sp) == 2:
                    proxy = self.db[item].querying_proxy
                    res += f' {proxy.serialize(False, full_names, True)},'
                else:
                    res += f' {self.header.serialize_read_column(item, full_names)},'
            else:
                raise EpureParseError('select header item must be ColumnProxy or Model')
        res = res[:-1]

        # first_item = header[0]
        # table_name = ''
        # # if isinstance(first_item, ColumnProxy):
        # if isinstance(first_item, ColumnProxyBase):
        #     table_name = first_item.__table__.full_name
        # # elif isinstance(first_item, Model):
        # elif isinstance(first_item, ModelBase):
        #     table_name = str(first_item)
        # elif isinstance(first_item, str):
        #     first_item = first_item.split('.')
        #     table_name = f'{first_item[0]}.{first_item[1]}'
        # res = res + f' FROM {table_name}'
        res = res + f' FROM {self.full_name}'
        return res



    # def replace_operators(self, where_clause:str):
    #     if not (self.db and self.db.py_db_operators):
    #         return where_clause
    #     for py_op, db_op in self.db.py_db_operators.items():
    #         where_clause = where_clause.replace(f' {py_op} ', f' {db_op} ')
    #     return where_clause



    def serialize_joins(self, joins:List[JoinOperation]):
        res = ''
        for join in joins:
            ser_join = self.serialize_join(join)
            res += ser_join        
        return res

    def serialize_join(self, join:JoinOperation):
        return f'{join.join_type} JOIN {join.model.__table__.full_name} on {join.on_clause} \n'

        

    def serialize_for_update(self, edata: Savable, **kwargs) -> object:

        data_dict = self._serialize(edata, self._serialize_field_val_to_sql)
        if not ('data_id' in data_dict and data_dict['data_id']):
            raise DbError('unable update edata without data_id')

        data_id = data_dict['data_id']
        pairs = ''

        for name, val in data_dict.items():
            pairs = pairs + name + ' = ' + val + ', '

        pairs = pairs[:-2]
        res = f'''UPDATE {self.full_name}
                SET {pairs}
                WHERE data_id = {data_id};'''
        return res


    def generate_id(self, resource: Savable = None):
        return uuid4()

    # def get_column_header_name(self, column_name:str):
    #     table_name = self.full_name
    #     res = f'{table_name}.{column_name}'
    #     alias = res.replace('.', '___')
    #     res = f'{res} as {alias}'
    #     return res