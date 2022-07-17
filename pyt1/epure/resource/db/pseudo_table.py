from .query import Query, JoinClause, Pseudo
from ...errors import DbError
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from .table_column import TableColumn
    from .table import Table
    from .db import Db



class PseudoColumn(Pseudo):
    if TYPE_CHECKING:
        table:Table
        column:TableColumn
    def __init__(self, table, column):
        self.table = table
        self.column = column

    def __str__(self) -> str:
        return f'{self.table.full_name}.{self.column.full_name}'

class PresudoTable(Query, Pseudo):
    if TYPE_CHECKING:
        table:Table
    def __init__(self, table):
        self.table = table

    def __getattr__(self, attr_name: str) -> Any:
        if attr_name not in self.table.header:
            raise DbError(f'column {attr_name} not in header of table {self.table.full_name}')
        column = self.table.header[attr_name]
        res = PseudoColumn(column, self.table)
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
        res = PresudoTable(self.db[key])
        return res

    def __iter__(self):
        return self.db.__iter__()

    def __len__(self):
        return self.db.__len__()

