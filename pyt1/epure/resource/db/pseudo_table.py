from .query import Query, JoinClause, Pseudo
from ...errors import DbError
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from .table_column import TableColumn
    from .table import Table
    from .db import Db



class PseudoColumn(Query, Pseudo):
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

class PresudoTable(Pseudo):
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

    def __lshift__(self, other:Query): #<<
        if hasattr(other, 'joins') and other.joins:
            raise DbError('do not use joins inside where clause')
        return JoinClause(other.condition, 'LEFT', self)

    def __rshift__(self, other): #>>
        if hasattr(other, 'joins') and other.joins:
            raise DbError('do not use joins inside where clause')
        return JoinClause(other.condition, 'RIGHT', self)


class PseudoDb(Query, Pseudo):
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

