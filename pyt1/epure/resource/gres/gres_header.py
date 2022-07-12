from ..db.table_header import TableHeader
from ..db.table_column import TableColumn
from ..db.db_entity_resource import DbEntityResource
import re
from ...helpers.string_helper import is_float


class GresHeader(TableHeader):
    
    def _deserialize(self, column_dict: dict) -> dict:
        column_name = column_dict['column_name']
        db_type = column_dict['data_type']
        not_null = (column_dict['is_nullable'] == 'NO')
        default = column_dict['column_default']
        uniq = (column_dict['constraint_type'] == 'UNIQUE')
        prim = (column_dict['constraint_type'] == 'PRIMARY KEY')
        foreign = (column_dict['constraint_type'] == 'FOREIGN KEY')

        if default:
            default = self.parse_column_default(default, db_type)

        res = {'column_name': column_name,
                'not_null': not_null,
                'db_type': db_type,
                'default':default,
                'uniq':uniq,
                'prim':prim,
                'foreign':foreign}

        if foreign:
            foreign_schema = column_dict['foreign_schema']
            foreign_table = column_dict['foreign_table']
            foreign_table = foreign_schema + '.' + foreign_table
            foreign_column = column_dict['foreign_column']

            res.update({'foreign_schema':foreign_schema,
                        'foreign_table':foreign_table,
                        'foreign_column':foreign_column})
                                
        return res
        

    def parse_column_default(self, default:str, db_type:str):
        res = re.sub('::[a-z]*', '', default)
        if res[0] == "'" and res[-1] == "'":
            res = res[1:-1]

        elif is_float(res):
            res = float(res)
        elif res[:5] == 'point':
            pattern = re.compile(r"point\(\((.*)\).*\((.*)\).*\)")
            res = pattern.findall(res)[0]
            res = complex(float(res[0]), float(res[1]))

        return res

    def _rename_column_script(self, table_name:str, old_name:str, new_name:str) -> str:
        return f'''
            ALTER TABLE {table_name} RENAME {old_name} TO {new_name};
        '''
        
    
    def _set_not_null_script(self, table_name:str, column_name:str) -> str:
        return f'''
            ALTER TABLE {table_name} ALTER COLUMN {column_name} SET NOT NULL;
        '''

    def _create_column_script(self, table_name:str, column:TableColumn, db:DbEntityResource) -> str:        
        db_type = column.serialize_type(db) #db.get_db_type(column.column_type)
        
        create_script = f'ALTER TABLE {table_name} ADD COLUMN {column.name} {db_type};'
        return create_script

    def _migrate_columns_script(self, table_name:str, from_column:str, to_column:str) -> str:
        return f'''
            UPDATE TABLE {table_name} SET {to_column} = {from_column};
        '''