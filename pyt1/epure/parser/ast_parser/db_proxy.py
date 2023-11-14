from .term import Term
from .table_proxy import TableProxy
from ...errors import DbError

class DbProxy(Term):
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