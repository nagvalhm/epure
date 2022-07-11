from ..resource import Resource
from typing import Dict, List, Any, Callable
from .constraint import Constraint
from ...errors import DbError

class DbEntityResource(Resource):

    py_db_types:Dict[type, str]
    db_py_types:Dict[str, type]
    default_namespace:str

    def serialize_constraint(self, constraint:Constraint) -> str:
        raise NotImplementedError

    def get_default_namespace(self):
        return self.default_namespace

    def get_db_type(self, py_type:type):
        if py_type in self.py_db_types:
            return self.py_db_types[py_type]
        if Any not in self.py_db_types:
            raise DbError(f'''type {py_type} unknown for 
                {self.full_name} specify Any db type for using unknown types''')
        return self.py_db_types[Any]

    def get_py_type(self, db_type:str):
        return self.db_py_types[db_type]

    # @property
    # def any_types(self):
    #     if hasattr(self, '_any_types'):
    #         return self._any_types
    #     res = []
    #     any_db_type = self.get_db_type(Any)
    #     for py_type, db_type in self.py_db_types.items():
    #         if db_type == any_db_type:
    #             res.append(py_type)
    #     self._any_types = res
    #     return res

    def same_db_type(self, first:type, second:type) -> bool:
        if first == second:
            return True

        first_siblings = self.get_sibling_py_types(first)
        return second in first_siblings


    def get_sibling_py_types(self, py_type:type) -> List[type]:
        sib_db_type = self.get_db_type(py_type)
        siblings = getattr(self, f'_{sib_db_type}_py_types', None)
        if siblings:
            return siblings
        
        res = []
        for py_type, db_type in self.py_db_types.items():
            if db_type == sib_db_type:
                res.append(py_type)
        setattr(self, f'_{sib_db_type}_py_types', res)
        return res