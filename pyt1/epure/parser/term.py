from __future__ import annotations
from ast import Name, BinOp, Compare, Constant
from msilib.schema import Error
from turtle import left, right
from typing import Dict, List
from uuid import UUID, uuid4
import networkx as nx
import matplotlib.pyplot as plt
# from functools import cmp_to_key

class Term:
    id:UUID
    terms_graph: Dict[UUID, Term]
    left_parent:Term
    right_parent:Term
    val:str
    debug = False

    def __init__(self) -> None:
        self.id = str(uuid4())
        self.terms_graph = {self.id: self}

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

    def _copy(self) -> Term:
        res = Term()
        if hasattr(self, 'id') and self.id:
            res.id = self.id

        res.val = ''
        if isinstance(self, Binary):
            res.val = self.operator
        else:
            res.val = self.serialize()
        return res


    def _restore_links(self, origin_terms, copies):
        self_orig_index = self.index_of(origin_terms)
        orig = origin_terms[self_orig_index]

        if hasattr(orig, 'left') and orig.left:
            left_copy_index = orig.left.index_of(copies)
            left_copy = copies[left_copy_index]
            self.left = left_copy
        if hasattr(orig, 'right') and orig.right:
            right_copy_index = orig.right.index_of(copies)
            right_copy = copies[right_copy_index]
            self.right = right_copy
        if hasattr(orig, 'left_parent') and orig.left_parent:
            left_parent_copy_index = orig.left_parent.index_of(copies)
            left_parent_copy = copies[left_parent_copy_index]
            self.left_parent = left_parent_copy
        if hasattr(orig, 'right_parent') and orig.right_parent:
            right_parent_copy_index = orig.right_parent.index_of(copies)
            right_parent_copy = copies[right_parent_copy_index]
            self.right_parent = right_parent_copy



    def index_of(self, terms: List[Term]):
        indexes = [index for (index, item) in enumerate(terms) if item.id == self.id]
        if len(indexes) > 1:
            raise Error('term occurred in a list more then once')
        if len(indexes) == 0:
            return -1
        return indexes[0]

class Binary(Term):
    left:Term
    right:Term
    operator:str
    parentheses = False

    @property
    def val(self):
        return self.operator

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
            res += " " + str(term.val)
        return res

    def sort_graph(self):
        res = []
        terms = list(self.terms_graph.values())

        #copy terms
        copies = []
        for term in terms:
            term_copy = term._copy()
            copies.append(term_copy)

        for copy in copies:
            copy._restore_links(terms, copies)

        if self.debug:
            self.show_graph_structure(copies)
        
        # terms = sorted(terms, key=cmp_to_key(self.compare_terms))
        
        while len(copies):
            shifted = self.shift_graph(copies)
            if self.debug:
                self.show_graph_structure(copies)
            term = self.terms_graph[shifted.id]
            res.append(term)
            del shifted

        return res



    def show_graph_structure(self, terms: List[Term]):
        # res = ''

        nx_edges = []
        for term in terms:
            term_name = str(term.id)[0:4]
            term_name = f'{term.val}_{term_name}'

            # self_index = term.index_of(terms)

            # res += "{"
            # res += f'{term_name}, '

            # res += f"{self_index}_id_{term.id},"
            if hasattr(term, 'left') and term.left:
                # left_index = term.left.index_of(terms)
                # res += f"{self_index}_left_{left_index},"

                left_name = str(term.left.id)[0:4]
                left_name = f'{term.left.val}_{left_name}'
                nx_edges.append((term_name, left_name))

            if hasattr(term, 'right') and term.right:
                # right_index = term.right.index_of(terms)
                # res += f"{self_index}_right_{right_index},"

                right_name = str(term.right.id)[0:4]
                right_name = f'{term.right.val}_{right_name}'
                nx_edges.append((term_name, right_name))

            # res += '}:'

        nx_graph = nx.Graph()
        nx_graph.add_edges_from(nx_edges)
        plt.figure(str(uuid4()))
        nx.draw_networkx(nx_graph, label='legend')
        plt.show()

        # return res

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

        del terms[iterat.index_of(terms)]
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