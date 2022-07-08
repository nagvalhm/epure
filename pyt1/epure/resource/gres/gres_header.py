from ..db.table_header import TableHeader
from ..db.table_column import TableColumn




class GresHeader(TableHeader):
    
    def _deserialize(self, column_dict: dict) -> dict:
        res = {'column_name': column_dict['column_name'],
                'is_nullable': (column_dict['is_nullable'] == 'YES'),
                'db_type': column_dict['data_type']}
        return res

    
    def _rename_column_script(self, table_name:str, old_name:str, new_name:str) -> str:
        return f'''
            ALTER TABLE {table_name} RENAME {old_name} TO {new_name};
        '''
        
    
    def _set_not_null_script(self, table_name:str, column_name:str) -> str:
        return f'''
            ALTER TABLE {table_name} ALTER COLUMN {column_name} SET NOT NULL;
        '''

    def _create_column_script(self, table_name:str, column:TableColumn) -> str:
        db = self.table.db
        db_type = db.get_db_type(column.column_type)
        
        create_script = f'ALTER TABLE {table_name} ADD COLUMN {column.name} {db_type};'
        return create_script

    def _migrate_columns_script(self, table_name:str, from_column:str, to_column:str) -> str:
        return f'''
            UPDATE TABLE {table_name} SET {to_column} = {from_column};
        '''