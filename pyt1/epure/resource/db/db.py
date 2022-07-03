from __future__ import annotations
from typing import *
import logging

from ..savable import Savable
if TYPE_CHECKING:
    from .table import Table
from ...resource.resource import Resource
from urllib.parse import urlparse
from ...errors import EpureError


class Db(Resource):

    database:str
    user:str
    password:str
    host:str
    port:str    
    params:Dict[str,str]

    log_level:int = logging.NOTSET
    logger:Optional[logging.Logger] = None
    connection:Any
    default_namespace:str
    py_db_types:Dict[type, str]
    db_py_types:Dict[str, type]
    tables:Dict[str,Table]
    
    def __init__(self, 
                connect_str:str='', 
                database:str='', 
                user:str='', 
                password:str='',
                host:str='', 
                port:str='', 
                default_namespace='', 
                log_level:int = logging.NOTSET,
                name:str='', res_id:object=None):

        connect_params = urlparse(connect_str)

        self.database = (database or connect_params.scheme)
        self.user = user or str(connect_params.username)
        self.password = password or str(connect_params.password)
        self.host = host or str(connect_params.hostname)
        self.port = port or str(connect_params.port)

        self.tables = {}
        self.default_namespace = default_namespace
        self.log_level = log_level

        self.set_logger()

        return super().__init__(name, res_id)



    def set_logger(self) -> Any:
        if self.log_level > logging.NOTSET:
            self.logger = logging.getLogger(__name__)
            logging.basicConfig()
            self.logger.setLevel(self.log_level)
            fileHandler = logging.FileHandler('epure_db.log', mode='a+')
            formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s:\n %(message)s')
            fileHandler.setFormatter(formater)

            self.logger.addHandler(fileHandler)


            

    def __contains__(self, object) -> bool:
        table_name = str(object)
        if table_name in self.tables:
            return True
        table = self.read(table_name=table_name)
        return bool(table)




    def execute(self, script: str = '') -> list:
        result = []
        
        if self.logger:
            self.logger.debug(script)
        try:
            result = self._execute(script)
        except Exception as ex:
            err = EpureError(f'unnable execute script {script}') \
                .with_traceback(ex.__traceback__)
            if self.logger:
                self.logger.error(err, exc_info=True)
                
            raise err
        return result

    def _execute(self, script: str = '') -> list:
        raise NotImplementedError()



    def get_db_type(self, py_type:type):
        return self.py_db_types[py_type]

    def get_py_type(self, db_type:str):
        return self.db_py_types[db_type]

    def get_table_scheme(self, resource:Savable) -> List[Dict[str, str]]:
        res: List[Dict[str, str]] = list()

        dict_items:ItemsView[str, Any]
        if isinstance(resource, Table):
            dict_items = dict(resource.header).items()
        else:
            dict_items = resource.__annotations__.items()
        

        for column_name, column_type in dict_items:
            if not resource.is_excluded(column_name):
                continue
            
            res.append({
                "column_name": column_name,
                "column_type": self.get_db_type(column_type)
            })

        return res