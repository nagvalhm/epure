from .term import Term
from ast import BinOp, Compare
from .leaf import Primitive, QueryingProxy
from typing import Dict, List, TYPE_CHECKING

class Binary(Term):
    left:Term
    right:Term
    operator:str
    parentheses = False
    debugger = None
    val = None


    def __init__(self, left, right, operator='') -> None:

        if not (isinstance(left, Term) or isinstance(right, Term)):
            raise NotImplementedError('please fuck urself')

        if not isinstance(left, Term):
            left = Primitive(left)
        elif isinstance(left, QueryingProxy) and not left.is_copy:
            left = left._copy()

        if not isinstance(right, Term):
            right = Primitive(right)
        elif isinstance(right, QueryingProxy) and not right.is_copy:
            right = right._copy()

        left.right_parent = self
        right.left_parent = self

        self.left = left
        self.right = right
        self.operator = operator
        self.positions = {}
        super().__init__()


    def serialize(self, for_debug=False) -> str:        
        # res = f'{self.left.serialize()} {self.operator} {self.right.serialize()}'
        # if self.parentheses:
        #     return f'({res})'
        # return res
        return self.operator

    def __str__(self):
        res = ''
        sorted_graph = self.sort_graph()
        for term in sorted_graph:
            res += term.serialize() + " "
        return res[:-1]

    def sort_graph(self):
        res = []
        terms = list(self.terms_graph.values())

        #copy terms
        copies = []
        for term in terms:
            term_copy = term._simple_copy()
            copies.append(term_copy)

        for copy in copies:
            copy._restore_links(terms, copies)

        if self.debugger:
            self.debugger.show(copies)
        
        # terms = sorted(terms, key=cmp_to_key(self.compare_terms))
        
        while len(copies):
            shifted = self.shift_graph(copies)
            if self.debugger and self.debugger.each_step:
                self.debugger.show(copies)
            term = self.terms_graph[shifted.id]
            res.append(term)
            del shifted

        return res



    def shift_graph(self, terms: List[Term]) -> Term:

        iterat = self.get_top(terms)

        while True:
            if hasattr(iterat, 'left_parent') and iterat.left_parent:
                iterat = iterat.left_parent
                continue
            elif hasattr(iterat, 'left') and iterat.left:
                iterat = iterat.left
                continue
            else:
                break

        if hasattr(iterat, 'right_parent') and iterat.right_parent\
            and hasattr(iterat, 'right') and iterat.right:
            iterat.right_parent.left = iterat.right
            iterat.right.right_parent = iterat.right_parent
            iterat.right.left_parent = None

        elif hasattr(iterat, 'right_parent') and iterat.right_parent:
            iterat.right_parent.left = None            

        elif hasattr(iterat, 'right') and iterat.right:
            iterat.right.left_parent = None            

        iterat_index = iterat.index_of(terms)
        del terms[iterat_index]
        return iterat

    def get_top(self, terms: List[Term]) -> Term:
        top = terms[0]
        while True:
            if hasattr(top, 'left_parent') and top.left_parent:
                top = top.left_parent
                continue
            elif hasattr(top, 'right_parent') and top.right_parent:
                top = top.right_parent
                continue
            else:
                break
        return top
        

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
    def __init__(self, left, right, operator='') -> None:
        if isinstance(left, Comparison) and isinstance(right, Comparison):
            self.parentheses = True
        return super().__init__(left, right, operator)

    def is_correct(self):
        not_correct = (self.right_open() or self.left_open())
        return not not_correct

    def right_open(self):
        right_leaf = self.go_until_hasattr('right')
        right_closed = isinstance(right_leaf.left_parent, Comparison)
        right_open = not right_closed
        return right_open

    def left_open(self):
        left_leaf = self.go_until_hasattr('left')
        left_closed = isinstance(left_leaf.right_parent, Comparison)
        left_open = not left_closed
        return left_open

class Comparison(Binary, Compare):
    def __init__(self, left, right, operator='') -> None:
        from .leaf import ColumnProxy
        from .leaf import Primitive

        if isinstance(left, ColumnProxy) and isinstance(right, ColumnProxy):
            self.parentheses = True
        elif isinstance(left, ColumnProxy) and isinstance(right, Primitive):
            self.parentheses = True
        elif isinstance(left, Primitive) and isinstance(right, ColumnProxy):
            self.parentheses = True #raize Error?
        elif isinstance(left, Primitive) and isinstance(right, Primitive):
            self.parentheses = True

        if isinstance(left, BinOperation) and isinstance(right, BinOperation):
            if left.is_correct() and right.is_correct():
                self.parentheses = True
            elif left.right_open() and right.left_open():
                self.parentheses = True


        return super().__init__(left, right, operator)