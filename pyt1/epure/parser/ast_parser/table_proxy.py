from .term import Term
from typing import Any
from .column_proxy import ColumnProxy

class TableProxy(Term):

    def __init__(self, db, table):
        self.__db__ = db
        self.__table__ = table
        # self.__qp_name__ = self.serialize(parentheses=False, full_names=True)
        super().__init__()

    def __getattr__(self, attr_name: str) -> Any:
        # if self.__is_copy__:
            # raise AttributeError
        if attr_name not in self.__table__.header:
            raise AttributeError(f'column {attr_name} not in header of table {self.__table__.full_name}')
        column = self.__table__.header[attr_name]
        res = ColumnProxy(self.__db__, self.__table__, column, self)
        return res

    # def __getitem__(self, *args) -> Any:
    #     res = TermHeader(list(*args))
    #     return res