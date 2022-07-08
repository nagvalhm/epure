from ..db.db import Db
import psycopg2
import psycopg2.extras
from typing import Sequence
from itertools import groupby
from .gres_table import GresTable
from ..db.table import *
from datetime import timedelta, datetime
from ipaddress import _IPAddressBase
from ..resource import Resource, FullName, SnakeCaseNamed
from ..savable import Savable
import logging
from inflection import underscore

class GresDb(Db):

    default_table_type: Type[Table] = GresTable
    default_namespace:str='Public'
    log_level:int = logging.NOTSET

    def __init__(self, connect_str:str='', database:str='', user:str='', password:str='',
             host:str='', port:str='', default_namespace='', log_level:int = logging.NOTSET,
             migrate_on_delete:bool=False):

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

        print(self.execute("SELECT 'test request'"))

        
        self._set_tables()


    def read(self, selector:object=None, **kwargs) -> Union[Resource, Sequence[Resource]]:
        
        table_name = str(selector)
        full_table_name = self._get_full_table_name(table_name)

        collumns = self.execute(f'''SELECT table_schema, table_name,
                    column_name, is_nullable, data_type
                    FROM information_schema.columns WHERE
                    table_schema = \'{full_table_name.namespace}\' AND
                    table_name = \'{full_table_name.name}\' ''')
        if len(collumns) > 0:
            table = self.deserialize_table(collumns)
            self._set_table(table)
            return table
        return []



    def serialize(self, table: Savable, method:str='', **kwargs) -> object:
        check_type('table', table, self.default_table_type)
        table = cast(Table, table)

        header = table.serialize_header(self)
        column_defenitions = []
        for column in header[:-1]:
            column_defenitions.append(
                column['column_name'] + " " + column['column_type'] + ","
            )

        last_column = header[len(header)-1]
        column_defenitions.append(
            last_column['column_name'] + " " + last_column['column_type']
        )

        script = " \n ".join(column_defenitions)
        
        script = f'''
        CREATE TABLE {table.full_name} (
            {script}
        );'''

        return script



    def _execute(self, script: str = '') -> list:
        result = []
        with psycopg2.connect(**self.params) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(script)
                if cursor.rowcount > 0:
                    result = cursor.fetchall()

        return result




    def _deserialize_table_name(self, table_columns:list) -> FullName:
        first_columns = table_columns[0]

        table_name = first_columns['table_name']
        namespace = first_columns['table_schema']
        return SnakeCaseNamed(name=table_name, namespace=namespace)

    def get_default_namespace(self):
        return underscore(self.default_namespace)
      


    def _set_tables(self):
        script = '''SELECT table_schema, table_name, 
                    column_name, is_nullable, data_type 
                    FROM information_schema.columns 
                    ORDER BY table_schema, table_name'''
        all_collumns = self.execute(script)    
        
        for key, group in groupby(all_collumns,  lambda row: row['table_schema'] + '.' + row['table_name']):
            group = list(group)
            table = self.deserialize_table(group)
            self._set_table(table)
    

        
    py_db_types:Dict[str, str] = {
        'int': 'bigint',
        'float': 'numeric',
        'str': 'text',
        'complex': 'point',

        'list': 'jsonb',
        'tuple': 'jsonb',
        'object': 'jsonb',
        'NoneType': 'jsonb',
        'Any': 'jsonb'
    }

    db_py_types:Dict[str, str] = {
        'bigint': 'int', #-9223372036854775808 to +9223372036854775807
        'text': 'str',
        'json': 'object',
        'name': 'str',
        'ARRAY': 'list',
        'oid': 'int', #0 to 4294967295
        'interval': 'timedelta',
        'smallint': 'int', #-32768 to +32767
        'inet': '_IPAddressBase', #IPv4Address or IPv6Address ipaddress.ip_address        
        'pg_node_tree': 'str', #representation of parsed sql query
        'boolean': 'bool',
        'numeric': 'float', #up to 131072 digits before the decimal point; up to 16383 digits after the decimal point
        'decimal': 'float', #up to 131072 digits before the decimal point; up to 16383 digits after the decimal point        
        'anyarray': 'list',
        'regproc': 'str', #sql procidure name
        'regtype': 'str', #sql type name
        'timestamp' : 'datetime',
        'timestamp with time zone': 'datetime',
        'time' : 'datetime',
        'time with time zone' : 'datetime',
        'double precision': 'float',
        'real': 'float',
        '"char"': 'str',
        'character varying': 'str',
        'character': 'str',
        'point' : 'complex',
        'jsonb': 'Any',

        'pg_ndistinct': 'int',
        'pg_mcv_list': 'int',
        'pg_dependencies': 'int',        
        'xid': 'int',
        'bytea': 'int',
        'integer': 'int',
        'pg_lsn': 'int',        
        'date': 'int',
        'smallserial':'int',
        'serial': 'int',
        'bigserial': 'int',
        'bit': 'int',
        'bit varying': 'int',
        'box': 'int',
        'cidr': 'int',
        'circle': 'int',
        'line' : 'int',
        'lseg' : 'int',
        'macaddr' : 'int',
        'macaddr8' : 'int',
        'money' : 'int',
        'path' : 'int',
        'pg_snapshot' : 'int',        
        'polygon' : 'int',
        'tsquery' : 'int',
        'tsvector' : 'int',
        'txid_snapshot' : 'int',
        'uuid' : 'int',
        'xml' : 'int'
    }