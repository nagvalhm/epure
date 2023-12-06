from __future__ import annotations
from .term import Term
from typing import Any
from .column_proxy import ColumnProxy
from ..proxy_base_cls import TableProxyBase
from ...resource.join_resource.join_resource import JoinResource

class TableProxy(Term, TableProxyBase):

    def __init__(self, db, table):
        self.__db__ = db
        self.__table__ = table
        self.__qp_name__ = self.serialize(parentheses=False, full_names=True)
        super().__init__()

    def __getattr__(self, attr_name: str) -> ColumnProxy:
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

        # if not for_header and parentheses:
        #     res = self.append_parentheses(res)

        return res
    
    def join(self, table_proxy:TableProxy, on_clause:str, join_type:str="LEFT", alias:str="") -> JoinResource:
        join_resource =  JoinResource(self)
        join_resource.join(table_proxy, on_clause, join_type, alias)
        return join_resource
    
    def select(self, *args, joins=[], include_node_id=False, **kwargs):
        self.__table__.select(*args, joins=joins, include_node_id=include_node_id, **kwargs)