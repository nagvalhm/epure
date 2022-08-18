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
        return self.str(False)
        # res = ''
        # sorted_graph = self.sort_graph()
        # for term in sorted_graph:
        #     res += term.serialize() + " "
        # return res[:-1]

    def str(self, debug=True):
        res = ''
        sorted_graph = self.sort_graph()
        for term in sorted_graph:
            res += term.serialize(debug) + " "
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
        left_leaf = self.get_last_left_term(terms)

        if hasattr(left_leaf, 'right_parent') and left_leaf.right_parent\
            and hasattr(left_leaf, 'right') and left_leaf.right:
            left_leaf.right_parent.left = left_leaf.right
            left_leaf.right.right_parent = left_leaf.right_parent
            left_leaf.right.left_parent = None

        elif hasattr(left_leaf, 'right_parent') and left_leaf.right_parent:
            left_leaf.right_parent.left = None            

        elif hasattr(left_leaf, 'right') and left_leaf.right:
            left_leaf.right.left_parent = None            

        left_leaf_index = left_leaf.index_of(terms)
        del terms[left_leaf_index]
        return left_leaf

    def get_last_left_term(self, terms: List[Term]):
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
        return iterat

    def get_last_right_term(self, terms: List[Term]):
        iterat = self.get_top(terms)

        while True:
            if hasattr(iterat, 'right_parent') and iterat.right_parent:
                iterat = iterat.right_parent
                continue
            elif hasattr(iterat, 'right') and iterat.right:
                iterat = iterat.right
                continue
            else:
                break
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

    def set_parentheses(self):
        self.parentheses = True
        terms = list(self.terms_graph.values())
        left_leaf = self.get_last_left_term(terms)
        left_leaf.left_parentheses_count += 1
        right_leaf = self.get_last_right_term(terms)
        right_leaf.right_parentheses_count += 1


class BinOperation(Binary, BinOp):
    def __init__(self, left, right, operator='') -> None:
        super().__init__(left, right, operator)
        if isinstance(left, Comparison) and isinstance(right, Comparison):
            self.set_parentheses()


    def is_correct(self):
        res = self.left_closed() and self.right_closed()
        return res

    def left_open(self):
        left_open = not self.left_closed()
        return left_open

    def right_open(self):
        right_open = not self.right_closed()
        return right_open

    def left_closed(self):
        terms = list(self.terms_graph.values())
        left_leaf = self.get_last_left_term(terms)
        left_closed = isinstance(left_leaf.right_parent, Comparison)
        return left_closed

    def right_closed(self):
        terms = list(self.terms_graph.values())
        right_leaf = self.get_last_right_term(terms)
        right_closed = isinstance(right_leaf.left_parent, Comparison)
        return right_closed

class Comparison(Binary, Compare):
    def __init__(self, left, right, operator='') -> None:
        from .leaf import ColumnProxy
        from .leaf import Primitive

        super().__init__(left, right, operator)

        if isinstance(left, ColumnProxy) and isinstance(right, ColumnProxy):
            self.set_parentheses()
        elif isinstance(left, ColumnProxy) and isinstance(right, Primitive):
            self.set_parentheses()
        elif isinstance(left, Primitive) and isinstance(right, ColumnProxy):
            self.set_parentheses() #raize Error?
        elif isinstance(left, Primitive) and isinstance(right, Primitive):
            self.set_parentheses()

        if isinstance(left, BinOperation) and isinstance(right, BinOperation):
            if left.is_correct() and right.is_correct():
                self.set_parentheses()
            elif left.left_closed() and left.right_open() \
                and right.left_open() and right.right_closed():
                self.set_parentheses()


