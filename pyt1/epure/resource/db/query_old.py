# from typing import Dict, Any
# from ...helpers.type_helper import check_type
# from .db_entity_resource import DbEntityResource
# from ...errors import DbError
# import inspect
# import sys


# class Pseudo:
#     pass


# class Query():

#     joins:list
#     condition:str
#     db:DbEntityResource
#     wrong_precedence:bool

#     def __init__(self, condition, joins = []):
#         self.condition = condition
#         self.joins = joins
#         # self.expr = f'{x}'

#     # def __rmatmul__(self, other:tuple):
#     def __xor__(self, other): #^
#         check_type('other', other, tuple)        
#         if isinstance(self, Query):
#             return SelectQuery(self.joins, self.condition, other)
#         raise NotImplementedError(f'''right join is cross-table relation, 
#                         its unkown for types: {type(self)}, {type(other)}''')

#     def get_brackets_term(self, other, operator:str, right:bool=False):
#         return '(' + self.get_term(other, operator, right) + ')'

#     def get_term(self, other, operator:str, right:bool=False):
#         if not isinstance(other, Query):
#             other = self.db.cast_py_db_val(type(other), other)
#         if right:
#             return str(other) + f' {operator} ' + str(self)
#         return str(self) + f' {operator} ' + str(other)


#     def logical_operation(self, other, operator:str, right:bool=False):

#         condition = self.get_condition(other, operator, right)

#         if hasattr(self, 'joins'):
#             joins = self.joins
#         else:
#             joins = []

#         if hasattr(other, 'joins'): 
#             joins = joins + other.joins

#         res = WhereClause(condition, joins)
#         if isinstance(self, Pseudo) or isinstance(other, Pseudo):            
#             res.wrong_precedence = True

#         return res
           
#     def __and__(self, other): #&
#         return self.logical_operation(other, 'AND')


#     def __or__(self, other): #|
#         return self.logical_operation(other, 'OR')

#     def __rand__(self, other): #&
#         return self.logical_operation(other, 'AND', True)


#     def __ror__(self, other): #|
#         return self.logical_operation(other, 'OR', True)


#     def __lshift__(self, other): #<<
#         raise NotImplementedError(f'''left join is cross-table relation, 
#                         its unkown for types: {type(self)}, {type(other)}''')

#     def __rshift__(self, other): #>>
#         raise NotImplementedError(f'''right join is cross-table relation, 
#                         its unkown for types: {type(self)}, {type(other)}''')

#     def get_condition(self, other, operator, right:bool=False):
#         if (hasattr(self, 'wrong_precedence') and self.wrong_precedence) or \
#             (hasattr(other, 'wrong_precedence') and other.wrong_precedence) or\
#                 isinstance(self, Pseudo) or isinstance(other, Pseudo):

#             return self.get_term(other, operator, right)
        
#         return self.get_brackets_term(other, operator, right)

#     def __eq__(self, other):
#         operator = '='
        
#         if other is None:
#             operator = 'is'

#         condition = self.get_condition(other, operator)

#         return WhereClause(condition, [])


#     def __ne__(self, other): #!=
#         if other is None:
#             return self.get_brackets_term(other, ' is not ')
#         return self.get_brackets_term(other, '!=')


#     def __lt__(self, other): #<
#         return self.get_brackets_term(other, '<')

#     def __le__(self, other): #<=
#         return self.get_brackets_term(other, '<=')
#     def __gt__(self, other): #>
#         return self.get_brackets_term(other, '>')
#     def __ge__(self, other): #>=
#         return self.get_brackets_term(other, '>=')


#     # def __invert__(self): #~
#     #     expr = '( invert ' + self.expr + ')'
#     #     return Query(expr)

#     def __str__(self) -> str:
#         return self.condition


# class SelectQuery(Query):
#     selected:Any

#     def __init__(self, condition, joins, selected):
#         self.selected = selected
#         return super().__init__(condition, joins)

# class JoinClause(Query):
#     direction:str
#     table:Any
#     operator:str

#     def __init__(self, condition, direction, table, operator:str=''):
#         if operator:
#             self.operator = operator
#         self.direction = direction
#         self.table = table
#         return super.__init__(condition)


#     def logical_operation(self, other, operator: str):
#         if isinstance(other, JoinClause):
#             other.operator = operator
#             return WhereClause('', [self, other])
#         if isinstance(other, WhereClause):
#             self.operator = operator
#             return WhereClause(other.condition, other.joins + [self])
#         raise NotImplementedError(f'''operation {operator} unkown for types: 
#             {type(self)}, {type(other)}''')
        

# class WhereClause(Query):

#     def logical_operation(self, other, operator: str):
#         if isinstance(other, JoinClause):
#             other.operator = operator
#             return WhereClause(self.condition, self.joins + [other])
#         if isinstance(other, WhereClause):
#             return super().logical_operation(other, operator)
#         raise NotImplementedError(f'''operation {operator} unkown for types: 
#             {type(self)}, {type(other)}''')