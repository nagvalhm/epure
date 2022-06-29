from __future__ import annotations
from typing import Any, Dict
from .dbnode import DBNode
from .node import Node
import psycopg2
from .postgress_table_node import PostgressTableNode

class PostgressNode(DBNode):

    dbtypes:Dict[type, str] = {
        int: 'bigint',
        str: 'text',
        type(None): 'json'
    }

    # def __init__(self, name:str=None, storage:Node = None) -> None:
    def __init__(self, host:str="127.0.0.1", port:str="5432", database:str=None, 
                user:str=None, password:str=None) -> None:

        self.connection = psycopg2.connect(database=database, 
            user = user, 
            password = password, 
            host = host, 
            port = port)

        super().__init__(database, user, password, host, port)

    def put_script(self, node:Node) -> str:
        scheme = self.get_table_scheme(node)
        column_defenitions = []
        for column in scheme[:-1]:
            column_defenitions.append(
                column['name'] + " " + column['column_type'] + ","
            )
        last_column = scheme[len(scheme)-1]
        column_defenitions.append(
            last_column['name'] + " " + last_column['column_type']
        )

        scheme_script = " \n ".join(column_defenitions)

        script = f'''
        CREATE TABLE IF NOT EXISTS {node.name} (
            {scheme_script}
        );'''

        return script


    def put(self, node:Node=None) -> PostgressTableNode:
        if isinstance(node, PostgressTableNode) and self.contains(node):
            return node      

        script = self.put_script(node)

        print(script)
        print(script.replace("\n", ""))
        self.execute(script.replace("\n", ""))

        res = PostgressTableNode()

        return res

    def execute(self, script: str) -> Any:
        cursor = self.connection.cursor()
        cursor.execute(script)
        self.connection.commit()
        return cursor
