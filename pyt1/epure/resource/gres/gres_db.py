from uuid import UUID
from ..db.db import Db
import psycopg2
import psycopg2.extras
from typing import cast, Type, Dict, Any, Callable, List, Tuple
from types import NoneType, LambdaType
from itertools import groupby
from .gres_table import GresTable
from ..db.table import Table
from datetime import timedelta, datetime
from ipaddress import _IPAddressBase
from ..resource import Resource, FullName, SnakeCaseNamed
from ..savable import Savable
import logging
from inflection import underscore
from ...helpers.type_helper import check_type
from ..db.constraint import Constraint, Default, Foreign, Prim, NotNull, Uniq
from ...errors import DbError
from ..file.json_file import JsonFile
from .jsonb_table import JsonbTable
from decimal import Decimal

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

        self._set_namespaces()
        
        self._set_tables()

        self.json_serializer = JsonFile('')


    def read(self, selector:object=None, **kwargs) -> Any:
        
        table_name = str(selector)
        full_table_name = self._get_full_table_name(table_name)


        collumns = self.execute(f'''SELECT cols.table_schema, cols.table_name, 
                    cols.column_name, cols.is_nullable, cols.data_type, cols.column_default,
                    cols_constr.table_schema AS foreign_schema,
				    cols_constr.table_name AS foreign_table,
				    cols_constr.column_name AS foreign_column,
                    constr.constraint_type
                    FROM information_schema.columns cols
                    left join information_schema.constraint_column_usage cols_constr
                    	on cols.table_schema = cols_constr.table_schema and cols.table_name = cols_constr.table_name
                    	and cols.column_name = cols_constr.column_name
                    left join information_schema.table_constraints constr
                    	on cols_constr.constraint_name = constr.constraint_name WHERE
                    cols.table_schema = \'{full_table_name.namespace}\' AND
                    cols.table_name = \'{full_table_name.name}\' ''')

        if len(collumns) > 0:
            table = self.deserialize_table(collumns)
            self._set_table(table)
            return table
        return []
    

    def serialize_namespace_for_create(self, namespace) -> object:
        return f'''CREATE SCHEMA {namespace};'''


    def serialize_for_create(self, table: Savable, **kwargs) -> object:
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
                    try:
                        result = cursor.fetchall()
                    except psycopg2.ProgrammingError as err:
                        self.logger.info(err)

        return result




    def _deserialize_table_name(self, table_columns:list) -> FullName:
        first_columns = table_columns[0]

        table_name = first_columns['table_name']
        namespace = first_columns['table_schema']
        return SnakeCaseNamed(name=table_name, namespace=namespace)

    def get_default_namespace(self):
        return underscore(self.default_namespace)
      
    def _set_namespaces(self):
        script = '''
          SELECT schema_name
                    FROM information_schema.schemata
        '''
        all_namespaces = self.execute(script)

        # for namespace in all_namespaces:
        #     self.namespaces.append(namespace[0])

        self.namespaces = [row[0] for row in all_namespaces]

    def _set_tables(self):
        script = '''
          SELECT cols.table_schema, cols.table_name, 
                    cols.column_name, cols.is_nullable, cols.data_type, cols.column_default,
                    cols_constr.table_schema AS foreign_schema,
				    cols_constr.table_name AS foreign_table,
				    cols_constr.column_name AS foreign_column,
                    constr.constraint_type
                    FROM information_schema.columns cols
                    left join information_schema.constraint_column_usage cols_constr
                    	on cols.table_schema = cols_constr.table_schema and cols.table_name = cols_constr.table_name
                    	and cols.column_name = cols_constr.column_name
                    left join information_schema.table_constraints constr
                    	on cols_constr.constraint_name = constr.constraint_name
                    ORDER BY cols.table_schema, cols.table_name
        '''
        all_collumns = self.execute(script)    
        
        for key, group in groupby(all_collumns,  lambda row: row['table_schema'] + '.' + row['table_name']):
            group = list(group)
            # if group[0]['table_name'] == 'default_epure':
            #     breakpoint()
            table = self.deserialize_table(group)
            self._set_table(table)

    def _get_table_type(self, table_columns:list):
        if len(table_columns) > 2:
            return self.default_table_type
        jsonb_cols = list(filter(lambda c: c['data_type'] == 'jsonb', table_columns))
        if len(jsonb_cols) != 1:
            return self.default_table_type
        return JsonbTable

    def serialize_constraint(self, constraint:Constraint) -> str:
        
        db_type = self.get_db_type(constraint.py_type)
        _default = getattr(constraint, 'default', '')
        default = ''
        if _default:
            default = self.cast_py_db_val(_default, constraint.py_type)
        
        origin = constraint.__origin__
        
        if origin == Default:
            return f"{db_type} DEFAULT {default}"
        elif origin == NotNull:
            return f"{db_type} NOT NULL DEFAULT {default}"
        elif origin == Uniq:
            return f"{db_type} UNIQUE"
        elif origin == Prim:
            return f"{db_type} PRIMARY KEY DEFAULT {default}"
        elif origin == Foreign:
            return f"{db_type}" #Foreign not realy implemented yet, because of ciclyc cases
                
        raise DbError('unknown constraint')
        
    def cast_py_db_val(self, val:Any, py_type:type) -> str:
        if val == None:
            return 'NULL'
        if py_type in (int, float, bool):
            return str(val)            
        if py_type in (str, UUID):
            res = f"'{str(val)}'"
            return res
        if py_type in (bytes, bytearray):            
            val = val.decode()
            val = val.replace("\x00","")
            res = f"'{val}'"
            return res
        if py_type == complex:            
            return f"point({val.real}, {val.imag})"

        json = self.json_serializer.serialize_for_update(val)
        return f"'{json}'"

        
    py_db_types:Dict[type, str] = {
        str: 'text',
        int: 'bigint',
        float: 'numeric',        
        complex: 'point',
        UUID: 'uuid',
        bool: 'boolean',

        #bytea siblings
        bytes: 'bytea',
        bytearray: 'bytea',

        #json siblings
        range: 'json',
        list: 'json',
        List: 'json',
        tuple: 'json',
        Tuple: 'json',
        object: 'json',
        Any: 'json',
        dict: 'json',
        Dict: 'json',
        Dict[int,str]: 'json',
        set: 'json',
        frozenset: 'json',
        memoryview: 'json',
        LambdaType: 'json',
        Callable: 'json'
    }

    db_py_types:Dict[str, type] = {
        'bigint': int, #-9223372036854775808 to +9223372036854775807
        'text': str,
        # 'json': object,
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
        'point' : complex,
        'json': Any,
        'jsonb': Any,
        'uuid' : UUID,
        'bytea': bytes,

        'pg_ndistinct': int,
        'pg_mcv_list': int,
        'pg_dependencies': int,        
        'xid': int,        
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
        'polygon' : int,
        'tsquery' : int,
        'tsvector' : int,
        'txid_snapshot' : int,        
        'xml' : int
    }