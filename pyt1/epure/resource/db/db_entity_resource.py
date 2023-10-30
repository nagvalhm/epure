from ..resource import Resource
from typing import Dict, List, Any, Callable
from .constraint import Constraint
from ...errors import DbError
from ..savable import Savable
from uuid import UUID


class DbEntityResource(Resource):

    py_db_types:Dict[type, str]
    db_py_types:Dict[str, type]
    default_namespace:str
    py_db_operators:Dict[str, str] = {
        '==': '=',
    }
    json_serializer:Savable
    # py_db_key_words:Dict[str, str] = {
    #     'where': 'where'
    # }
    

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

    def same_db_type(self, first:type, second:type) -> bool:
        if first == second:
            return True
        res = self.get_db_type(first) == self.get_db_type(second)
        return res

    def cast_py_db_val(self, val:Any, py_type:type) -> str:
        raise NotImplementedError


    def cast_db_py_val(self, val:Any, py_type:type) -> Any:
        # if type(val) == Decimal:
        if val is None:
            return val
        if py_type in (int, float, bool, UUID):
            return py_type(val)
        if self.same_db_type(py_type, Any):
            return self.json_serializer.deserialize(val)
        if py_type in (bytearray, bytes) and isinstance(val, memoryview):
            return py_type(val.tobytes())
        # if py_type == UUID:
            # return str(val)
        if py_type is complex:
            complex_tuple = eval(val)
            return py_type(f"{complex_tuple[0]}+{complex_tuple[1]}j")
        return val
        # return py_type(val) instead of 54,55.