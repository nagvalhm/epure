from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict
if TYPE_CHECKING:
    from .table import Table
from ...resource.resource import Resource
from urllib.parse import urlparse


class Db(Resource):

    database:str
    user:str
    password:str
    host:str
    port:str
    
    params:Dict[str,str]

    connection:Any

    py_db_types:Dict[type, str]
    db_py_types:Dict[str, type]
    tables:Dict[str,Table]
    
    def __init__(self, connect_str:str='', database:str='', user:str='', password:str='',
             host:str='', port:str=''):

        connect_params = urlparse(connect_str)

        self.database = (database or connect_params.scheme)
        self.user = user or str(connect_params.username)
        self.password = password or str(connect_params.password)
        self.host = host or str(connect_params.hostname)
        self.port = port or str(connect_params.port)

    def __contains__(self, object):
        table_name = str(object)
        if table_name in self.tables:
            return True
        self.read(table_name=table_name)

    def get_db_type(self, py_type:type):
        return self.py_db_types[py_type]

    def get_py_type(self, db_type:str):
        return self.db_py_types[db_type]

    # def get_table_scheme(self, node:Node) -> List[Dict[str, str]]:
    #     res: List[Dict[str, str]] = list()

    #     for name, val in vars(node).items():
    #         if not self.is_savable(name):
    #             continue
    #         column_type = val if isinstance(val, type) else type(val)
    #         res.append({
    #             "name": name,
    #             "column_type": self.dbtypes.get(column_type, 'bytea')
    #         })

    #     return res