from .table import Table, TableColumn, TableHeader, NotNull
from typing import TypeVar
from collections.abc import Sequence
from ...helpers.type_helper import check_type

class GresTable(Table):
    def create_column(self, column_info: Sequence) -> TableColumn:
        check_type('column_info', column_info, Sequence)

        column_name = column_info[2]
        is_nullable = column_info[3] == 'YES'
        db_type = column_info[4]
        try:
            colum_type = self.resource.get_py_type(db_type)
        except KeyError as ex:
            raise TypeError(f'{db_type} is unknown for {self.resource.name} '
                            'set db_py_types attribute properly') from ex
        # colum_type = TypeVar('colum_type', bound=colum_type)
        if not is_nullable:
            colum_type = NotNull[colum_type]
        
        return TableColumn(column_name, colum_type)

class JsonbTable(GresTable):
    pass