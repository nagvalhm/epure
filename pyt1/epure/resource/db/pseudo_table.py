from .term import  Pseudo, _PseudoColumn, _PseudoTable, Term
from .select_query import SelectQuery
# Query, JoinClause, ,
from ...errors import DbError
from typing import Any, TYPE_CHECKING, cast
from ...helpers.type_helper import check_type
if TYPE_CHECKING:
    from .table_column import TableColumn
    from .table import Table
    from .db import Db



class PseudoColumn(_PseudoColumn):
    if TYPE_CHECKING:
        table:Table
        column:TableColumn
        db:Db
    def __init__(self, db, table, column):
        self.db = db
        self.table = table
        self.column = column

    def __str__(self) -> str:
        return f'{self.column.full_name}'
        # return f'{self.table.full_name}.{self.column.full_name}'

class PresudoTable(_PseudoTable):
    if TYPE_CHECKING:
        __table__:Table
        __db__:Db
    def __init__(self, db, table):
        self.__db__ = db
        self.__table__ = table
        

    def __getattr__(self, attr_name: str) -> Any:
        if attr_name not in self.__table__.header:
            raise DbError(f'column {attr_name} not in header of table {self.__table__.full_name}')
        column = self.__table__.header[attr_name]
        res = PseudoColumn(self.__db__, self.__table__, column)
        return res

    def __str__(self) -> str:
        return f'{self.__table__.full_name}'



class PseudoDb(Pseudo):
    if TYPE_CHECKING:
        db:Db
    def __init__(self, db):
        self.db = db

    def __getitem__(self, key:str):
        if key not in self.db:
            raise DbError(f'table {key} not in db {self.db.full_name}')
        res = PresudoTable(self.db, self.db[key])
        return res

    def __iter__(self):
        return self.db.__iter__()

    def __len__(self):
        return self.db.__len__()

    def __call__(self, *args: list) -> Term:
        select_header = args[0:-1]
        select_body = args[-1]
        check_type('select_body', select_body, Term)

        res = SelectQuery(select_header, select_body)
        
        table = list(self.db.tables.values())[0]
        return table.serialize_read(res)