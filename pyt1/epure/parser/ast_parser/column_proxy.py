from .term import Term
class ColumnProxy(Term):
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