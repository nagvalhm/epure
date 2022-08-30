# from __future__ import annotations
# from ...errors import DbError

# class Term:

#     def __and__(self, other): #&
#         return self.binary_operation(other, 'and')

#     def __rand__(self, other): #&
#         return self.binary_operation(other, 'and', True)

#     def __or__(self, other:Term): #|
#         return self.binary_operation(other, 'or')

#     def __ror__(self, other:Term): #|
#         return self.binary_operation(other, 'or', True)

#     def __xor__(self, other:Term): #^
#         return self.binary_operation(other, '^')

#     def __rxor__(self, other:Term): #^
#         return self.binary_operation(other, '^', True)


#     def __lshift__(self, other:Term): #<<
#         return self.binary_operation(other, '<<')
#         # return self.join_operation(other, 'left')

#     def __matmul__(self, other:Term): #@
#         return self.binary_operation(other, '@')

#     def __rmatmul__(self, other:Term): #@
#         return self.binary_operation(other, '@', True)

#     def __eq__(self, other): #==
#         return self.binary_relation(other, '==')

#     def binary_relation(self, other:Term, operator:str):
#         if isinstance(self, PartialBinary):            
#             if not isinstance(other, Binary):
#                 return Binary(self, other, operator)
#             other.right = PartialBinary(other.left, other.right, other.operator)
#             other.left = self
#             other.operator = operator
#             return other
#         if isinstance(other, PartialBinary):            
#             other.left = PartialBinary(self, other.left, operator)
#             return other
#         return Binary(self, other, operator)

#     def binary_operation(self, other:Term, operator:str, right_self:bool = False):        
#         left = self
#         right = other
#         if right_self:
#             left = other
#             right = self
#         if isinstance(self, _PseudoColumn) or isinstance(other, _PseudoColumn) or not isinstance(other, Term):
#             return PartialBinary(left, right, operator)
#         if (isinstance(self, PartialBinary) and not isinstance(other, PartialBinary)) or\
#             isinstance(other, PartialBinary) and not isinstance(self, PartialBinary):
#             return PartialBinary(left, right, operator)
#         return Binary(left, right, operator)
        
#     # def join_operation(self, other:Term, join_type:str=''):
#     #     if not isinstance(self, _PseudoTable):
#     #         raise NotImplementedError(f'''join is cross-table relation, 
#     #                         its unkown for types: {type(self)}, {type(other)}''')
#     #     if isinstance(other, _PseudoColumn) or not isinstance(other, Term):
#     #         return PartialJoinBinary(self, other, join_type)
#     #     return JoinBinary(self, other, join_type)


# class Binary(Term):
#     left:Term
#     right:Term
#     operator:str    

#     def __init__(self, left, right, operator='') -> None:
#         self.left = left
#         self.right = right
#         self.operator = operator

#     def __str__(self) -> str:
#         return f'({self.left} {self.operator} {self.right})'


# class JoinBinary(Binary):    
#     table:str
#     on_clause:str
#     join_type:str
#     unparsed:str

#     LEFT_TYPE='LEFT'
#     RIGHT_TYPE='RIGHT'

#     def __init__(self, table, on_clause, join_type='', unparsed='') -> None:
#         self.table = table
#         self.on_clause = on_clause
#         self.join_type = join_type
#         self.unparsed = unparsed
        

# #     def __str__(self) -> str:
# #         return f'[{self.join_type} join on {self.left.__table__.full_name}:{self.right}]'

# # class PartialJoinBinary(JoinBinary):
# #     def __str__(self) -> str:
# #         return f'{self.join_type} join on {self.left.__table__.full_name}:{self.right}'

# class PartialBinary(Binary):
#     def __str__(self) -> str:
#         return f'{self.left} {self.operator} {self.right}'

# class Pseudo(Term):
#     pass
        


# class _PseudoColumn(Pseudo):
#     #overrided in pseudo.py
#     pass

# class _PseudoTable(Pseudo):
#     #overrided in pseudo.py
#     pass