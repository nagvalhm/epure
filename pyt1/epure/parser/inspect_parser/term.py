from __future__ import annotations
import types
from typing import Any
from uuid import UUID
import collections.abc

class Term:

    def is_str_or_uuid(self, other:Any) -> bool:
        if isinstance(other,str) and "SELECT" not in other\
            or isinstance(other, UUID):
            return True

        return False
    
    def convert_tuple_for_in(self, other):
        other_types_set = {type(it) for it in other}
        if other_types_set.issubset({UUID, str}):
            other = [str(it) for it in other]
        other = tuple(other)
        return other

    #bool_ops
    def _and(self, left, right): #and
        return self.__db__.serialize_op('and', str(left), str(right))
    
    def _or(self, left, right): #or
        return self.__db__.serialize_op('or', str(left), str(right))
    
    #compare_ops
    def _not(self, other): #not
        return self.__db__.serialize_op('not', str(other))

    def not_in(self, other): #not in
        if type(other) in (set, list, tuple):
            other = self.convert_tuple_for_in(other)
        
        if isinstance(other, str) and not "(SELECT" in other\
            or not isinstance(other, tuple):
            raise TypeError(f"'{other}' is of type '{type(other)}' and not of type List, Tuple, Set or select method, so it cannot be right operand for SQL 'NOT IN' operator")
        
        return self.__db__.serialize_op('not in', str(self), str(other))
    
    def _in(self, other): #in
        if type(other) in (set, list, tuple):
            other = self.convert_tuple_for_in(other)
        
        if isinstance(other, str) and not "(SELECT" in other\
            or type(other) not in (tuple, str):
            raise TypeError(f"'{other}' is of type '{type(other)}' and not of type List, Tuple, Set or Model.select() method, so it cannot be right operand for SQL 'IN' operator")
            
        return self.__db__.serialize_op('in', str(self), str(other))

    def __eq__(self, other): # ==
        if self.is_str_or_uuid(other):
            other = repr(str(other))
        return self.__db__.serialize_op('==', str(self), str(other))
    
    def __lt__(self, other): #<
        if self.is_str_or_uuid(other):
            other = repr(str(other))
        return self.__db__.serialize_op('<', str(self), str(other))

    def __le__(self, other): #<=
        if self.is_str_or_uuid(other):
            other = repr(str(other))
        return self.__db__.serialize_op('<=', str(self), str(other))

    def __ne__(self, other): #!=
        if self.is_str_or_uuid(other):
            other = repr(str(other))
        return self.__db__.serialize_op('!=', str(self), str(other))

    def __gt__(self, other): #>
        if self.is_str_or_uuid(other):
            other = repr(str(other))
        return self.__db__.serialize_op('>', str(self), str(other))

    def __ge__(self, other): #>=
        if self.is_str_or_uuid(other):
            other = repr(str(other))
        return self.__db__.serialize_op('>=', str(self), str(other))
    
    def _is(self, other): # is
        if other != None:
            raise TypeError(f"operator IS can be used only with NULL value, but not with {other}")
        return self.__db__.serialize_op('is', str(self), "NULL")
        
    def is_not(self, other): # is not
        if other != None:
            raise TypeError(f"operator IS NOT can be used only with NULL value, but not with {other}")
        return self.__db__.serialize_op('is not', str(self), "NULL")
    
    #non-existent in python
    def like(self, other):
        if type(other) in (UUID, str):
            other = repr(str(other))
        return self.__db__.serialize_op('like', str(self), str(other))
    
    #all

    #any

    #between

    #some
    
    def __str__(self):
        return self.serialize(True)