from ..resource import Resource
from typing import Dict

class DbEntityResource(Resource):

    py_db_types:Dict[str, str]
    db_py_types:Dict[str, str]
    default_namespace:str

    def get_default_namespace(self):
        return self.default_namespace

    def get_db_type(self, py_type:str):
        return self.py_db_types[py_type]

    def get_py_type(self, db_type:str):
        return self.db_py_types[db_type]

    @property
    def any_types(self):
        if hasattr(self, '_any_types'):
            return self._any_types
        res = []
        any_db_type = self.get_db_type('Any')
        for py_type, db_type in self.py_db_types.items():
            if db_type == any_db_type:
                res.append(py_type)
        self._any_types = res
        return res