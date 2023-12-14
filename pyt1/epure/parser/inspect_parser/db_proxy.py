from .term import Term
from .table_proxy import TableProxy
from ...errors import DbError

class DbProxy(Term):
    def __init__(self, db, default_namespace:str=None):
        self.__db__ = db
        self.default_namespace = default_namespace
        super().__init__()

    # def __getitem__(self, key:str):
    #     if key not in self.__db__:
    #         raise DbError(f'table {key} not in db {self.__db__.full_name}')
    #     res = TableProxy(self.__db__, self.__db__[key])
    #     return res
    
    def __getattr__(self, key:str) -> TableProxy:
        if self.default_namespace:
            key = f"{self.default_namespace}.{key}"

        if key not in self.__db__ and key not in self.__db__.namespaces:
            raise DbError(f'table {key} not in db {self.__db__.full_name}')
        elif key in self.__db__.namespaces:
            return DbProxy(self.__db__, default_namespace=key)
        res = TableProxy(self.__db__, self.__db__[key])
        return res

    def __iter__(self):
        return self.__db__.__iter__()

    def __len__(self):
        return self.__db__.__len__()
    
    # def select(self, args)