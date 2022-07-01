from .db import Db
import psycopg2
from typing import Any, Dict
from itertools import groupby
from .gres_table import GresTable
from ...helpers.type_helper import check_type

class GresDb(Db):



    def __init__(self, connect_str:str='', database:str='', user:str='', password:str='',
             host:str='', port:str=''):

        super().__init__(connect_str, 
            database=database, 
            user=user, 
            password=password, 
            host=host, 
            port=port)

        
        need_set_tables = True
        if hasattr(self, 'tables') and self.tables:
            need_set_tables = False

            for key in self.params:
                if self.params[key] != getattr(self, key, ''):
                    need_set_tables = True


        self.params = {
            'database': self.database, 
            'user': self.user, 
            'password': self.password, 
            'host': self.host, 
            'port': self.port
        }

        print(self.execute("select 'test request'"))

        if need_set_tables:
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
            if first_row[0] == 'public' \
            else first_row[0] + '.' + first_row[1]
        table = GresTable(table_name)
        table.resource = self
        
        for column_info in table_info:
            column = table.create_column(column_info)
            table.header[column.name] = column

        
    py_db_types:Dict[type, str] = {
        int: 'bigint',
        str: 'text',
        type(None): 'json'
    }

    db_py_types:Dict[str, type] = {
        'bigint': int,
        'text': str,
        'json': type(None),
        'name': str,
        'ARRAY': list,
        'oid': int
    }


        # for row in rows:
        #     table_name = row[0] + '.' + row[1] if \
        #                  row[0] != 'public' \
        #                  else row[1]
        #     pass


    def execute(self, script: str = '') -> list:
        result = []
        with psycopg2.connect(**self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(script)
                if cursor.rowcount != 0:
                    result = cursor.fetchall()
        return result


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
