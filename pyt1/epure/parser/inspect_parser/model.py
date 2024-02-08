from __future__ import annotations
from .term import Term
from typing import Any
from .column_proxy import ColumnProxy
from ..proxy_base_cls import ModelBase
from inflection import underscore
from ...resource.join_resource.join_resource import JoinResource

class Model(Term, ModelBase):

    def __init__(self, db, table):
        self.__db__ = db
        self.__table__ = table
        self.__resource__ = table
        self.__qp_name__ = self.serialize(parentheses=False, full_names=True)
        super().__init__()

    def __getattr__(self, attr_name: str) -> ColumnProxy:
        # if self.__is_copy__:
            # raise AttributeError
        
        # case_name = underscore(attr_name)
        case_name = attr_name.lower()
        
        if case_name not in self.__table__.header:
            raise AttributeError(f'column {attr_name} not in header of table {self.__table__.full_name}')
        column = self.__table__.header[case_name]
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
    
    
    def select(self, *args, joins=[], include_data_id=False, **kwargs):
        if type(args[0]) not in (tuple,list,set):
            raise ValueError(f"first arg must be tuple, list or set, not {args[0]}")
        return "(" + self.__table__.select(*args, joins=joins, include_data_id=include_data_id, **kwargs) + ")"
    
    def join(self, joined_model:Model, on_clause:str, join_type:str="LEFT", alias:str="") -> JoinResource:
        join_resource =  JoinResource(self)
        new_join_resource = join_resource.join(joined_model, on_clause, join_type, alias)
        return new_join_resource