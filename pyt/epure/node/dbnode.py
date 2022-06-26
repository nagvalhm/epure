from __future__ import annotations
from typing import Any, Dict, List
from .node import Node

# class SchemeRow: ColumnMeta


class DBNode(Node):

    database:str
    user:str
    password:str
    host:str
    port:str
    connection:Any
    dbtypes:Dict[type, str]

    def __init__(self, host:str="127.0.0.1", port:str="5432", database:str=None, 
                user:str=None, password:str=None) -> None:

        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_table_scheme(self, node:Node) -> List[Dict[str, str]]:
        res: List[Dict[str, str]] = list()

        for name, val in vars(node).items():
            if not self.is_savable(name):
                continue
            column_type = val if isinstance(val, type) else type(val)
            res.append({
                "name": name,
                "column_type": self.dbtypes.get(column_type, 'bytea')
            })

        return res

    def is_savable(self, atr_name: str) -> bool:
        if hasattr(self, '__exclude__') and atr_name in self.__exclude__:
            return False
        if atr_name[:2] == "__" and atr_name[-2:] == "__":
            return False
        return True