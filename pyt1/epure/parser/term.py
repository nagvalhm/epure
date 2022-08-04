from __future__ import annotations
from ast import Name, BinOp, Compare, Constant
from typing import Dict, List
from uuid import UUID, uuid4
from functools import cmp_to_key

class Term:
    id:UUID
    terms_graph: Dict[UUID, Term]
    left_parent:Term
    right_parent:Term

    #primitive operators:
    def __and__(self, other): #&
        return self.operation(self, other, 'and')

    def __rand__(self, other): #&
        return self.operation(other, self, 'and')

    def __or__(self, other:Term): #|
        return self.operation(self, other, 'or')

    def __ror__(self, other:Term): #|
        return self.operation(other, self, 'or')


    #non primitive operators:
    def __xor__(self, other:Term): #^
        return self.operation(self, other, '^')


    def __lshift__(self, other:Term): #<<
        return self.operation(self, other, '<<')
        # return self.join_operation(other, 'left')

    def __rshift__(self, other:Term): #<<
        return self.operation(self, other, '>>')

    #comparators:
    def __eq__(self, other): #==
        return self.comparison(self, other, '==')

    def __lt__(self, other): #<
        return self.comparison(self, other, '<')

    def __le__(self, other): #<=
        return self.comparison(self, other, '<=')

    def __ne__(self, other): #!=
        return self.comparison(self, other, '!=')

    def __gt__(self, other): #>
        return self.comparison(self, other, '>')

    def __ge__(self, other): #>=
        return self.comparison(self, other, '>=')


    def __init__(self) -> None:
        self.id = str(uuid4())
        self.terms_graph = {self.id: self}



    def operation(self, left:Term, right:Term, operator:str):
        res = BinOperation(left, right, operator)
        res.merge_graphs()
        return res


    def comparison(self, left:Term, right:Term, operator:str):
        res = Comparison(left, right, operator)
        res.merge_graphs()
        return res


    def serialize(self) -> str:
        raise NotImplementedError

class Binary(Term):
    left:Term
    bottom_right:Term
    operator:str
    parentheses = False

    def __init__(self, left, right, operator='') -> None:

        if not (isinstance(left, Term) or isinstance(right, Term)):
            raise NotImplementedError('please fuck urself')

        if not isinstance(left, Term):
            left = Primitive(left)
        if not isinstance(right, Term):
            right = Primitive(right)

        left.right_parent = self
        right.left_parent = self

        self.left = left
        self.right = right
        self.operator = operator
        super().__init__()

    def serialize(self) -> str:        
        # res = f'{self.left.serialize()} {self.operator} {self.right.serialize()}'
        # if self.parentheses:
        #     return f'({res})'
        # return res
        return self.operator

    def __str__(self):
        res = ''
        sorted_graph = self.sort_graph()
        for term in sorted_graph:
            res += term.serialize()
        return res

    def sort_graph(self):
        res = []
        terms = list(self.terms_graph.values())
        # terms = sorted(terms, key=cmp_to_key(self.compare_terms))
        
        while len(terms):
            shifted = self.shift_graph(terms)
            res.append(shifted)

        return res

    def shift_graph(self, terms: List[Term]):

        iterat = self.get_tops(terms)[0]

        while True:
            if hasattr(iterat, 'left_parent') and iterat.left_parent:
                iterat = iterat.left_parent
                continue
            elif hasattr(iterat, 'left') and iterat.left:
                iterat = iterat.left
            else:
                break

        if hasattr(iterat, 'right_parent') and iterat.right_parent\
            and hasattr(iterat, 'right') and iterat.right:
            iterat.right_parent.left = iterat.right
            iterat.right.left_parent = iterat.right_parent
            return iterat

        if hasattr(iterat, 'right_parent') and iterat.right_parent:
            iterat.right_parent.left = None
            return iterat

        if hasattr(iterat, 'right') and iterat.right:
            iterat.right.left_parent = None
            return iterat


    def get_tops(self, terms: List[Term]):
        not_tops = set()
        for term in terms:
            if not isinstance(term, Binary):
                continue
            not_tops.add(term.left)
            not_tops.add(term.right)
        tops = []
        for term in terms:
            if term not in not_tops:
                tops.append(term)
        return tops
        

    # def compare_terms(self, x, y):
    #     pass

    def merge_graphs(self):
        terms_graph = {}
        terms_graph.update(self.terms_graph)        
        terms_graph.update(self.left.terms_graph)        
        terms_graph.update(self.right.terms_graph)

        
        self.left.terms_graph = terms_graph        
        self.right.terms_graph = terms_graph
        self.terms_graph = terms_graph

        return terms_graph

class BinOperation(Binary, BinOp):
    pass

class Comparison(Binary, Compare):
    pass

class Primitive(Term, Constant):
    val = None
    def __init__(self, val) -> None:
        self.val = val
        super().__init__()

    def serialize(self) -> str:
        return str(self.val)