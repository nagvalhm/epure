from __future__ import annotations
from abc import abstractmethod
from typing import Dict, Any, Type, cast
import logging

from .db_entity import DbEntity

from ..savable import Savable
from .table import Table
from .table_storage import TableStorage
from urllib.parse import urlparse
from ...errors import EpureError
from ...helpers.type_helper import check_type



class Db(TableStorage):

    database:str
    user:str
    password:str
    host:str
    port:str    
    params:Dict[str,str]

    log_level:int = logging.NOTSET
    logger:logging.Logger
    connection:Any
    
    


    @abstractmethod
    def __init__(self, 
                connect_str:str='', 
                database:str='', 
                user:str='', 
                password:str='',
                host:str='', 
                port:str='', 
                default_namespace='', 
                log_level:int = logging.NOTSET,
                name:str='', res_id:object=None,
                default_table_type:Type[Table]=None,
                migrate_on_delete:bool=False):
        


        connect_params = urlparse(connect_str)

        self.database = (database or connect_params.scheme)
        self.user = user or str(connect_params.username)
        self.password = password or str(connect_params.password)
        self.host = host or str(connect_params.hostname)
        self.port = port or str(connect_params.port)        

        if default_namespace:
            self.default_namespace = default_namespace

        if log_level:
            self.log_level = log_level


        self.tables = {}
        self.set_logger()

        return super().__init__(name, default_table_type, res_id, migrate_on_delete)



    def create(self, db_entity: Savable) -> DbEntity:
        check_type('db_entity', db_entity, DbEntity)
        if isinstance(db_entity, Table):
            return self.create_table(db_entity)
        raise NotImplementedError(f'createion not implemented for type {type(db_entity)}')


    def update(self, db_entity: Savable) -> DbEntity:
        check_type('db_entity', db_entity, DbEntity)
        if isinstance(db_entity, Table):
            return self.update_table(db_entity)
        raise NotImplementedError(f'update not implemented for type {type(db_entity)}')


    def execute(self, script: str = '') -> list:
        result = []
        
        if hasattr(self, 'logger') and self.logger:
            self.logger.debug(script)
        try:
            script = self.get_cache() + script
            script = script.replace("\n", "")
            result = self._execute(script)
        except Exception as ex:
            err = EpureError(f'unnable execute script {script}: {ex}') \
                .with_traceback(ex.__traceback__)
            if self.logger:
                self.logger.error(err, exc_info=True)
                
            raise err
        return result

    def _execute(self, script: str = '') -> list:
        raise NotImplementedError()

    def get_cache(self) -> str:
        res = self.cache_queue
        if not res:
            return ''
        res = '\n'.join(res)
        res = res + '\n'
        self.cache_queue = []
        return res

    def set_logger(self) -> Any:
        if self.log_level > logging.NOTSET:
            self.logger = logging.getLogger(__name__)
            
            self.logger.setLevel(self.log_level)
            fileHandler = logging.FileHandler('epure_db.log', mode='a+')
            fileHandler.setLevel(self.log_level)
            formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s:\n %(message)s')
            fileHandler.setFormatter(formater)

            self.logger.addHandler(fileHandler)