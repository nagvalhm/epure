from .term import Term
from .model import Model
from ...errors import DbError

class Domain(Term):
    def __init__(self, db, default_namespace:str=None):
        self.__db__ = db
        self.default_namespace = default_namespace
        super().__init__()

    # def __getitem__(self, key:str):
    #     if key not in self.__db__:
    #         raise DbError(f'table {key} not in db {self.__db__.full_name}')
    #     res = Model(self.__db__, self.__db__[key])
    #     return res
    
    def __getattr__(self, key:str) -> Model:
        if self.default_namespace:
            key = f"{self.default_namespace}.{key}"

        if key not in self.__db__ and key not in self.__db__.namespaces:
            raise DbError(f'table {key} not in db {self.__db__.full_name}')
        elif key in self.__db__.namespaces:
            return Domain(self.__db__, default_namespace=key)
        res = Model(self.__db__, self.__db__[key])
        return res

    def __iter__(self):
        return self.__db__.__iter__()

    def __len__(self):
        return self.__db__.__len__()
    
    # def select(self, args)

    # def model(self, cls) -> Model:
    #     # if cls in Epure.epures:
    #     return Model(cls.resource.db, cls.resource)