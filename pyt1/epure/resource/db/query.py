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


    def __lshift__(self, other:Term): #<<    
        return self.binary_operation(other, '<<')


    def __eq__(self, other): #==
        return self.binary_relation(other, '=')

    def binary_relation(self, other:Term, operator:str):
        if isinstance(self, PartialBinary):            
            if not isinstance(other, Binary):
                return Binary(self, other, operator)
            other.right = PartialBinary(other.left, other.right, other.operator)
            other.left = self
            other.operator = operator
            return other
        if isinstance(other, PartialBinary):            
            other.left = PartialBinary(self, other.left, operator)
            return other
        return Binary(self, other, operator)

    def binary_operation(self, other:Term, operator:str, right_self:bool = False):        
        left = self
        right = other
        if right_self:
            left = other
            right = self
        if isinstance(self, _PseudoColumn) or isinstance(other, _PseudoColumn) or not isinstance(other, Term):
            return PartialBinary(left, right, operator)
        return Binary(left, right, operator)
        

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

class _PseudoColumn(Pseudo):
    #overrided in pseudo.py
    pass

class _PseudoTable(Pseudo):
    #overrided in pseudo.py
    pass