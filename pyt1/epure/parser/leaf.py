from msilib.schema import Error
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from ..resource.db.table_column import TableColumn
    from ..resource.db.table import Table
    from ..resource.db.db import Db
from ..errors import DbError
from .term import Term
from ast import Name
from ast import Name, Constant
from ..errors import EpureParseError

class Leaf(Term):
    left_parentheses_count = 0
    right_parentheses_count = 0

    def __init__(self) -> None:
        self.left_parentheses_count = 0
        self.right_parentheses_count = 0
        super().__init__()

    def append_parentheses(self, val):
        return '(' * self.left_parentheses_count + val + ')' * self.right_parentheses_count

    def __str__(self):
        return self.serialize(False)


class Primitive(Leaf, Constant):
    def __init__(self, val) -> None:
        self.val = val
        super().__init__()

    def serialize(self, parentheses=True) -> str:
        res = str(self.val)
        if isinstance(self.val, str):
            res = f"'{res}'"
        if not parentheses:
            return res
        res = self.append_parentheses(res)
        return res


class QueryingProxy(Leaf):
    if TYPE_CHECKING:
        __db__:Db
    is_copy = False

    def _copy(self):
        raise NotImplementedError

class ColumnProxy(QueryingProxy, Name):
    if TYPE_CHECKING:
        __table__:Table
        __column__:TableColumn        

    def __init__(self, db, table, column):
        self.__db__ = db
        self.__table__ = table
        self.__column__ = column
        super().__init__()


    def serialize(self, parentheses=True) -> str:
        res = f'{self.__column__.full_name}'
        if not parentheses:
            return res
        res = self.append_parentheses(res)
        return res


    def _copy(self):
        res = ColumnProxy(self.__db__, self.__table__, self.__column__)
        res.is_copy = True
        return res


class TableProxy(QueryingProxy, Name):
    if TYPE_CHECKING:
        __table__:Table

    def __init__(self, db, table):
        self.__db__ = db
        self.__table__ = table
        super().__init__()

    def __getattr__(self, attr_name: str) -> Any:
        if self.is_copy:
            raise AttributeError
        if attr_name not in self.__table__.header:
            raise DbError(f'column {attr_name} not in header of table {self.__table__.full_name}')
        column = self.__table__.header[attr_name]
        res = ColumnProxy(self.__db__, self.__table__, column)
        return res

    def serialize(self, parentheses=True) -> str:
        res = f'{self.__table__.full_name}'
        if not parentheses:
            return res
        res = self.append_parentheses(res)
        return res

    def _copy(self):
        res = TableProxy(self.__db__, self.__table__)
        res.is_copy = True
        return res

class DbProxy(QueryingProxy):

    def __init__(self, db):
        self.__db__ = db
        super().__init__()

    def __getitem__(self, key:str):
        if key not in self.__db__:
            raise DbError(f'table {key} not in db {self.__db__.full_name}')
        res = TableProxy(self.__db__, self.__db__[key])
        return res

    def __iter__(self):
        return self.__db__.__iter__()

    def __len__(self):
        return self.__db__.__len__()