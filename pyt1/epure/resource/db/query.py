from __future__ import annotations

class Term:

    def __and__(self, other): #&
        return self.binary_operation(other, 'AND')

    def __rand__(self, other): #&
        return self.binary_operation(other, 'AND', True)

    def __or__(self, other:Term): #|
        return self.binary_operation(other, 'OR')

    def __ror__(self, other:Term): #|
        return self.binary_operation(other, 'OR', True)

    def __eq__(self, other):
        if isinstance(self, PartialBinary):
            # self.right = Binary(other, self.right, '=')
            if not isinstance(other, Binary):
                return Binary(self, other, '=')
            other.right = PartialBinary(other.left, other.right, other.operator)
            other.left = self
            other.operator = '='
            return other
        if isinstance(other, PartialBinary):            
            other.left = PartialBinary(self, other.left, '=')
            return other
        return Binary(self, other, '=')# self.binary_relation(other, '=')

    def binary_relation(self, other:Term, operator:str):
        return Binary(other, self, operator)

    def binary_operation(self, other:Term, operator:str, right_self:bool = False):
        if isinstance(self, Pseudo) or isinstance(other, Pseudo) or not isinstance(other, Term):
            if not right_self:
                return PartialBinary(self, other, operator)
            return PartialBinary(other, self, operator)
        if not right_self:
            return Binary(self, other, operator)
        return Binary(other, self, operator)
        

class Binary(Term):
    left:Term
    right:Term
    operator:str    

    def __init__(self, left, right, operator) -> None:
        self.left = left
        self.right = right
        self.operator = operator

    def __str__(self) -> str:
        return f'({self.left} {self.operator} {self.right})'

class PartialBinary(Binary):
    def __str__(self) -> str:
        return f'{self.left} {self.operator} {self.right}'

class Pseudo(Term):
    pass