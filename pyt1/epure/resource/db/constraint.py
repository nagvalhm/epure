from types import NoneType
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast
from ...helpers.type_helper import check_subclass
from ...errors import EpureError

__all__ = ['Constraint', 'Default', 'NotNull', 'Uniq', 'Prim', 'Foreign', 'Check']

class Constraint(type):
    py_type:type = NoneType
    __origin__:type = NoneType
    
    def __getitem__(self:Type, params:Any):
        res = self.__class__(self.__name__, self.__bases__, dict(self.__dict__))
        res.__origin__ = self
        if isinstance(params, type):
            res.py_type = params
        if isinstance(params, tuple):
            res.py_type = params[0]
            res.set_params(*params[1:])

        if issubclass(res.py_type, Constraint):
            # ( hasattr(res.py_type, '__origin__') and  issubclass(res.py_type.__origin__, Constraint)):
            raise EpureError('Constraint parameter cant be Constraint')
        return res

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.py_type != other.py_type:
            return False
        if self.__origin__ != other.__origin__:
            return False
        if self.__name__ != other.__name__:
            return False
        
        if self.__origin__ == Default:
            self = cast(Default, self)
            other = cast(Default, other)
            return self.default == other.default
        return True

class Default(metaclass=Constraint):
    py_type:type = NoneType
    default:Any = None

    @classmethod
    def set_params(cls, default:Any):
        cls.default = default



class NotNull(Default):
    pass
    # py_type:type
    # default:Any
    # def __class_getitem__(cls, py_type:type, default:Any=None):
    #     cls.py_type = py_type
    #     cls.default = default
    #     return cls

class Uniq(metaclass=Constraint):
    pass

class Prim(NotNull, Uniq):
    pass

class Foreign(metaclass=Constraint):
    table:str = ''
    column:str = ''
    
    @classmethod
    def set_params(cls, table:str, column:str):        
        cls.table = table
        cls.column = column


class Check(metaclass=Constraint):    
    condition:Any = None
    
    @classmethod
    def set_params(cls, condition:Any):
        cls.condition = condition
        return cls



# https://www.postgresql.org/docs/current/sql-createtable.html

# where column_constraint is:

# [ CONSTRAINT constraint_name ]
# { NOT NULL |
#   NULL |
#   CHECK ( expression ) [ NO INHERIT ] |
#   DEFAULT default_expr |
#   GENERATED ALWAYS AS ( generation_expr ) STORED |
#   GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ] |
#   UNIQUE index_parameters |
#   PRIMARY KEY index_parameters |
#   REFERENCES reftable [ ( refcolumn ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ]
#     [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
# [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]


#Default = DEFAULT
#NotNull = NOT NULL, need default
#Uniq = UNIQUE, can be nullable
#Foreign = REFERENCES, must refer to Prim or Uniq

#Prim = PRIMARY KEY = Uniq + NotNull need method @Prim, generated unique Prim by self
#Check = CHECK