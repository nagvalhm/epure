from .db import Db
import psycopg2
from typing import *
from itertools import groupby
from .gres_table import GresTable
from .table import *
from ...helpers.type_helper import check_type
from datetime import timedelta, datetime
from ipaddress import _IPAddressBase
from ..resource import Resource
from ..savable import Savable
import logging

class GresDb(Db):

    def _execute(self, script: str = '') -> list:
        result = []
        with psycopg2.connect(**self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(script)
                if cursor.rowcount != 0:
                    result = cursor.fetchall()

        return result

    def create(self, resource: Savable, res_id: object = None):
        pass
    #     scheme = self.get_table_scheme(resource)
    #     column_defenitions = []
    #     for column in scheme[:-1]:
    #         column_defenitions.append(
    #             column['name'] + " " + column['column_type'] + ","
    #         )
    #     last_column = scheme[len(scheme)-1]
    #     column_defenitions.append(
    #         last_column['name'] + " " + last_column['column_type']
    #     )

    #     scheme_script = " \n ".join(column_defenitions)

    #     script = f'''
    #     CREATE TABLE IF NOT EXISTS {resource.name} (
    #         {scheme_script}
    #     );'''

    #     return script

    def read(self, selector:object=None, **kwargs) -> Union[Resource, Sequence[Resource]]:
    
        table_id = self._get_table_id(selector, **kwargs)

        collumns = self.execute(f'''select table_schema, table_name,
                    column_name, is_nullable, data_type
                    from information_schema.columns where
                    table_schema = \'{table_id[0]}\' and table_name = \'{table_id[1]}\' ''')
        if len(collumns) > 0:
            return self._add_table(collumns)
        return []

        
    def _get_table_id(self, selector:object=None, **kwargs) -> List[str]:
        table_name = ''
        if  selector:    
            table_name = str(selector)

        if not table_name:
            table_name = kwargs.get('table_name', '')    

        if not table_name:
            raise ValueError('method read of bd need table_name as argument')

        table_id = table_name.split('.')
        if len(table_id) > 2:
            raise NameError('table name must have no more then one dot')
        if len(table_id) == 1:
            table_id.insert(0, self.default_namespace)
        return table_id



    def __init__(self, connect_str:str='', database:str='', user:str='', password:str='',
             host:str='', port:str='', default_namespace='public', log_level:int = logging.NOTSET):

        super().__init__(connect_str, 
            database=database, 
            user=user, 
            password=password, 
            host=host, 
            port=port,
            default_namespace=default_namespace,
            log_level=log_level)

        self.params = {
            'database': self.database, 
            'user': self.user, 
            'password': self.password, 
            'host': self.host, 
            'port': self.port
        }

        print(self.execute("select 'test request'"))

        
        self.set_tables()        


    def set_tables(self):
        script = '''SELECT table_schema, table_name, 
                    column_name, is_nullable, data_type 
                    FROM information_schema.columns 
                    order by table_schema, table_name'''
        all_collumns = self.execute(script)

        
        for key, group in groupby(all_collumns,  lambda row: row[0] + '.' + row[1]):
            self._add_table(list(group))
    
    def _add_table(self, table_info):
        first_row = table_info[0]
        table_name = first_row[1] \
            if first_row[0] == self.default_namespace \
            else first_row[0] + '.' + first_row[1]
        table = GresTable(table_name)
        table.resource = self
        
        for column_info in table_info:
            column = table.create_column(column_info)
            table.header[column.name] = column

        self.tables[table_name] = table
        return table
        
    py_db_types:Dict[type, str] = {
        int: 'bigint',
        str: 'text',
        type(None): 'json'
    }

    db_py_types:Dict[str, type] = {
        'bigint': int, #-9223372036854775808 to +9223372036854775807
        'text': str,
        'json': object,
        'name': str,
        'ARRAY': list,
        'oid': int, #0 to 4294967295
        'interval': timedelta,
        'smallint': int, #-32768 to +32767
        'inet': _IPAddressBase, #IPv4Address or IPv6Address ipaddress.ip_address        
        'pg_node_tree': str, #representation of parsed sql query
        'boolean': bool,
        'numeric': float, #up to 131072 digits before the decimal point; up to 16383 digits after the decimal point
        'decimal': float, #up to 131072 digits before the decimal point; up to 16383 digits after the decimal point        
        'anyarray': list,
        'regproc': str, #sql procidure name
        'regtype': str, #sql type name
        'timestamp' : datetime,
        'timestamp with time zone': datetime,
        'time' : datetime,
        'time with time zone' : datetime,
        'double precision': float,
        'real': float,
        '"char"': str,
        'character varying': str,
        'character': str,

        'pg_ndistinct': int,
        'pg_mcv_list': int,
        'pg_dependencies': int,
        'jsonb': int,
        'xid': int,
        'bytea': int,
        'integer': int,
        'pg_lsn': int,        
        'date': int,
        'smallserial':int,
        'serial': int,
        'bigserial': int,
        'bit': int,
        'bit varying': int,
        'box': int,
        'cidr': int,
        'circle': int,
        'line' : int,
        'lseg' : int,
        'macaddr' : int,
        'macaddr8' : int,
        'money' : int,
        'path' : int,
        'pg_snapshot' : int,
        'point' : int,
        'polygon' : int,
        'tsquery' : int,
        'tsvector' : int,
        'txid_snapshot' : int,
        'uuid' : int,
        'xml' : int
    }








# from __future__ import annotations
# from typing import Any, Dict
# from .dbnode import DBNode
# from .node import Node
# import psycopg2
# from .postgress_table_node import PostgressTableNode

# class PostgressNode(DBNode):

#     dbtypes:Dict[type, str] = {
#         int: 'bigint',
#         str: 'text',
#         type(None): 'json'
#     }

#     # def __init__(self, name:str=None, storage:Node = None) -> None:
#     def __init__(self, host:str="127.0.0.1", port:str="5432", database:str=None, 
#                 user:str=None, password:str=None) -> None:

#         self.connection = psycopg2.connect(database=database, 
#             user = user, 
#             password = password, 
#             host = host, 
#             port = port)

#         super().__init__(database, user, password, host, port)

#     def put_script(self, node:Node) -> str:
#         scheme = self.get_table_scheme(node)
#         column_defenitions = []
#         for column in scheme[:-1]:
#             column_defenitions.append(
#                 column['name'] + " " + column['column_type'] + ","
#             )
#         last_column = scheme[len(scheme)-1]
#         column_defenitions.append(
#             last_column['name'] + " " + last_column['column_type']
#         )

#         scheme_script = " \n ".join(column_defenitions)

#         script = f'''
#         CREATE TABLE IF NOT EXISTS {node.name} (
#             {scheme_script}
#         );'''

#         return script


#     def put(self, node:Node=None) -> PostgressTableNode:
#         if isinstance(node, PostgressTableNode) and self.contains(node):
#             return node      

#         script = self.put_script(node)

#         print(script)
#         print(script.replace("\n", ""))
#         self.execute(script.replace("\n", ""))

#         res = PostgressTableNode()

#         return res

#     def execute(self, script: str) -> Any:
#         cursor = self.connection.cursor()
#         cursor.execute(script)
#         self.connection.commit()
#         return cursor
