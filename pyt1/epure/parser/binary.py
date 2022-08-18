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

    def get_last_left_term(self, terms: List[Term]=None):
        if terms == None:
            terms = list(self.terms_graph.values())
        iterat = self.get_top(terms)

        res = iterat.go_until_hasattr(['left_parent', 'left'], terms)
        # return res
        while True:
            if hasattr(iterat, 'left_parent') and iterat.left_parent\
                 and iterat.left_parent.index_of(terms) != None:

                iterat = iterat.left_parent                
            elif hasattr(iterat, 'left') and iterat.left\
                and iterat.left.index_of(terms) != None:

                iterat = iterat.left                
            else:
                break

        return iterat

    def get_last_right_term(self, terms: List[Term] = None):        
        if terms == None:
            terms = list(self.terms_graph.values())
        iterat = self.get_top(terms)

        while True:
            if hasattr(iterat, 'right_parent') and iterat.right_parent\
                and iterat.right_parent.index_of(terms) != None:

                iterat = iterat.right_parent                
            elif hasattr(iterat, 'right') and iterat.right\
                and iterat.right.index_of(terms) != None:

                iterat = iterat.right                
            else:
                break

        return iterat

    def get_top(self, terms: List[Term]=None) -> Term:
        if terms == None:
            terms = list(self.terms_graph.values())
        iterat = terms[0]        
        while True:
            if hasattr(iterat, 'left_parent') and iterat.left_parent\
                and iterat.left_parent.index_of(terms) != None:

                iterat = iterat.left_parent
                
            elif hasattr(iterat, 'right_parent') and iterat.right_parent\
                and iterat.right_parent.index_of(terms) != None:

                iterat = iterat.right_parent
                
            else:
                break
        return iterat
        

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
        left_leaf = self.left
        if isinstance(self.left, Binary):
            left_leaf = self.left.get_last_left_term()
        left_leaf.left_parentheses_count += 1

        right_leaf = self.right
        if isinstance(self.right, Binary):
            right_leaf = self.right.get_last_right_term()
        right_leaf.right_parentheses_count += 1