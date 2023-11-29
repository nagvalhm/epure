from .term import Term
from ..proxy_base_cls import ColumnProxyBase
from typing import Union

class ColumnProxy(Term, ColumnProxyBase):
    def __init__(self, db, table, column, table_proxy=None):
        self.__db__ = db
        self.__table__ = table
        self.__column__ = column
        self.__qp_name__ = self.serialize(parentheses=False, full_names=True)

        if table_proxy is None:
            from .table_proxy import TableProxy
            table_proxy = TableProxy(db, table)
        self.__table_proxy__ = table_proxy
        super().__init__()

    def serialize(self, parentheses=True, full_names=True, for_header=False) -> str:
        if for_header:
            res = self.__table__.header.serialize_read_column(self.__column__, full_names)
        elif not full_names:
            res = self.__column__.name
        else:
            table = self.__table__.full_name
            res = f'{table}.{self.__column__.name}'

        # if not for_header and parentheses:
        #     res = self.append_parentheses(res)

        return res
    
    def in_header(self, header:Union[list,tuple]) -> bool:
        table_name = self.__table__.full_name
        from .table_proxy import TableProxy
        for qp in header:
            # check_type('qp', qp, [TableProxy, ColumnProxy])
            if isinstance(qp, ColumnProxy):
                if self.__qp_name__ == qp.__qp_name__:
                    return True
            if isinstance(qp, TableProxy):
                if qp.__qp_name__ == table_name:
                    return True
        return False