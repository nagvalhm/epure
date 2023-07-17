from typing import TYPE_CHECKING, Any, Union
if TYPE_CHECKING:
    from ..resource.db.table_column import TableColumn
    from ..resource.db.table import Table
    from ..resource.db.db import Db
from ..errors import DbError
from .term import Term, TermHeader
from ast import Name
from ast import Name, Constant
from ..errors import EpureParseError
from ..helpers.type_helper import check_type
from uuid import UUID

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
        return self.serialize(False, True)


class Primitive(Leaf, Constant):
    def __init__(self, val) -> None:
        self.val = val
        super().__init__()

    def serialize(self, parentheses=True, full_names=True, for_header=False) -> str:
        res = ""
        if isinstance(self.val, list) or isinstance(self.val, tuple):
            res = "("
            for item in self.val:
                if isinstance(item, Leaf):
                    res += f'{item.serialize(parentheses, full_names, for_header)}, '
                    # temp.append(str(item))
                elif isinstance(item,str):
                    res += f"'{item}', "
                else:
                    # temp.append(item.serialize(parentheses, full_names, for_header))
                    res += f'{str(item)}, '
                    # res += f'{cast_py_db_val(item)}, '
            res = res[:-2] + ")"
            # res += ")"
            # res = str(tuple(temp))
        else:
            res = str(self.val)
            # res = self(self.val)

        if isinstance(self.val, str) or isinstance(self.val, UUID):
            res = f"'{res}'"

        if not parentheses:
            return res
        res = self.append_parentheses(res)
        return res



class QueryingProxy(Leaf):
    if TYPE_CHECKING:
        __db__:Db
    __is_copy__ = False
    __qp_name__:str
    

    def _copy(self):
        raise NotImplementedError

    def in_header(self, header:Union[list,tuple]):
        raise NotImplementedError


class ColumnProxy(QueryingProxy, Name):
    if TYPE_CHECKING:
        __table__:Table
        __column__:TableColumn
        __table_proxy__ = None

    def __init__(self, db, table, column, table_proxy=None):
        self.__db__ = db
        self.__table__ = table
        self.__column__ = column
        self.__qp_name__ = self.serialize(parentheses=False, full_names=True)

        if table_proxy is None:
            table_proxy = TableProxy(db, table)
        self.__table_proxy__ = table_proxy
        super().__init__()



    def serialize(self, parentheses=True, full_names=True, for_header=False) -> str:
        res = ''
        # if not full_names:
        #     res = self.__column__.name
        # el
        if for_header:
            res = self.__table__.header.serialize_read_column(self.__column__, full_names)
        elif not full_names:
            res = self.__column__.name
        else:
            table = self.__table__.full_name
            res = f'{table}.{self.__column__.name}'

        if not for_header and parentheses:
            res = self.append_parentheses(res)
        
        return res


    def _copy(self):
        res = ColumnProxy(self.__db__, self.__table__, self.__column__, self.__table_proxy__)
        res.__header__ = self.__header__
        res.__is_copy__ = True
        return res

    def in_header(self, header:Union[list,tuple]) -> bool:
        table_name = self.__table__.full_name
        for qp in header:
            check_type('qp', qp, [TableProxy, ColumnProxy])
            if isinstance(qp, ColumnProxy):
                if self.__qp_name__ == qp.__qp_name__:
                    return True
            if isinstance(qp, TableProxy):
                if qp.__qp_name__ == table_name:
                    return True
        return False


class TableProxy(QueryingProxy, Name):
    if TYPE_CHECKING:
        __table__:Table

    def __init__(self, db, table):
        self.__db__ = db
        self.__table__ = table
        self.__qp_name__ = self.serialize(parentheses=False, full_names=True)
        super().__init__()

    def __getattr__(self, attr_name: str) -> Any:
        if self.__is_copy__:
            raise AttributeError
        if attr_name not in self.__table__.header:
            raise AttributeError(f'column {attr_name} not in header of table {self.__table__.full_name}')
        column = self.__table__.header[attr_name]
        res = ColumnProxy(self.__db__, self.__table__, column, self)
        return res

    def __getitem__(self, *args) -> Any:
        res = TermHeader(list(*args))
        return res

    # def __call__(self, *args) -> Any:
    #     res = TermHeader(list(*args))
    #     return res

    def serialize(self, parentheses=True, full_names=True, for_header=False) -> str:
        res = ''
        # if not full_names:
        #     res = self.__table__.name      
        # el
        if for_header:
            header = self.__table__.header
            for col in header:
                res += header.serialize_read_column(header[col], full_names) + ', '
            res = res[0:-2]
        else:
            res = f'{self.__table__.full_name}'

        if not for_header and parentheses:
            res = self.append_parentheses(res)
        
        return res

    def _copy(self):
        res = TableProxy(self.__db__, self.__table__)
        res.__header__ = self.__header__
        res.__is_copy__ = True
        return res

    def in_header(self, header:Union[list,tuple]) -> bool:
        for qp in header:
            check_type('qp', qp, [TableProxy, ColumnProxy])
            if isinstance(qp, TableProxy) and self.__qp_name__ == qp.__qp_name__:
                return True
        return False

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