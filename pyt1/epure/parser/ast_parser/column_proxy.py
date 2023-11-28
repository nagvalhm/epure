from .term import Term
from ..proxy_base_cls import ColumnProxyBase

class ColumnProxy(Term, ColumnProxyBase):
    def __init__(self, db, table, column, table_proxy=None):
        self.__db__ = db
        self.__table__ = table
        self.__column__ = column
        # self.__qp_name__ = self.serialize(parentheses=False, full_names=True)

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