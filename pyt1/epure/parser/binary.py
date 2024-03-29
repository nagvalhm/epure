from ..errors import EpureParseError
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
            raise EpureParseError('expression is incorrect')

        if not isinstance(left, Term):
            left = Primitive(left)
        elif isinstance(left, QueryingProxy) and not left.__is_copy__:
            left = left._copy()

        if not isinstance(right, Term):
            right = Primitive(right)
        elif isinstance(right, QueryingProxy) and not right.__is_copy__:
            right = right._copy()

        left.right_parent = self
        right.left_parent = self

        self.left = left
        self.right = right
        self.operator = operator
        self.positions = {}
        super().__init__()


    def serialize(self, parentheses=True, full_names=True, for_header=False, translator=None) -> str:
        return self.operator

    def __str__(self):
        #not debug mode
        return self.str(parentheses=True, full_names=True)


    def str(self, parentheses=False, full_names=False, translator=None):
        res = ''        
        sorted_graph = self.sort_graph(translator)
        for term in sorted_graph:
            res += term.serialize(parentheses, full_names, translator=translator) + " "
        return res[:-1]



    def sort_graph(self, translator=None):
        res = []
        
        copies = self._simple_copy_terms(translator=translator)

        if self.debugger:
            self.debugger.show(copies)

        
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

    def get_last_left_term(self, terms: List[Term]=None):
        if terms is None:
            terms = list(self.terms_graph.values())
        top = self.get_top(terms)

        res = top.go_until_hasattr('left_parent', 'left', terms)
        return res


    def get_last_right_term(self, terms: List[Term] = None):        
        if terms is None:
            terms = list(self.terms_graph.values())
        iterat = self.get_top(terms)

        res = iterat.go_until_hasattr('right_parent', 'right', terms)
        return res

    def get_top(self, terms: List[Term]=None) -> Term:
        if terms is None:
            terms = list(self.terms_graph.values())
        iterat = terms[0]

        res = iterat.go_until_hasattr('left_parent', 'right_parent', terms)
        return res
        

    def merge_graphs(self):
        terms_graph = {}
        left = self.left
        right = self.right

        # if left.__header__ or right.__header__:
        #     header = self.merge_headers(left.__header__, right.__header__)
        #     left.__header__ = header
        #     right.__header__ = header
        #     self.__header__ = header
            
        terms_graph.update(self.terms_graph)        
        terms_graph.update(left.terms_graph)        
        terms_graph.update(right.terms_graph)
        
        left.terms_graph = terms_graph
        right.terms_graph = terms_graph
        self.terms_graph = terms_graph

        return terms_graph

    def set_parentheses(self):
        self.parentheses = True
        left_leaf = self.left
        if isinstance(self.left, Binary):
            left_leaf = self.left.get_last_left_term()
        left_leaf.left_parentheses_count += 1

        right_leaf = self.right
        if isinstance(self.right, Binary):
            right_leaf = self.right.get_last_right_term()
        right_leaf.right_parentheses_count += 1