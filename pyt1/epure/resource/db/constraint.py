from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast

class Constraint(type):
    def __getitem__(cls:Type, param:Any):
        cls.__param__ = param
        return cls

    def is_constraint():
        pass

class Default(metaclass=Constraint):
    pass

class NotNull(Default):
    __param__:type
    __default__:Callable
    def __class_getitem__(cls, param:Any, default:Any):
        cls.__param__ = param
        cls.__default__ = default
        return cls

class Id(metaclass=Constraint):
    __param__:type

class Uniq(metaclass=Constraint):
    __param__:type


class Check(metaclass=Constraint):
    __param__:type
    __condition__:Callable
    def __class_getitem__(cls, param:Any, condition:Callable):
        cls.__param__ = param
        cls.__condition__ = condition
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

#Id = PRIMARY KEY = Uniq + NotNull need method @Id, generated unique Id by self
#Check = CHECK