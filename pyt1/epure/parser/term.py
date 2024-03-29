from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING
from uuid import UUID, uuid4
from ..errors import EpureParseError
if TYPE_CHECKING:
    from ..resource.db.db import Db


class Term:
    id:UUID
    terms_graph: Dict[UUID, Term]
    left_parent:Term = None
    right_parent:Term = None
    val:str
    __header__:list

    def __init__(self) -> None:
        self.id = str(uuid4())
        self.terms_graph = {self.id: self}
        self.__header__ = []

    #primitive operators:
    def __and__(self, other): #&
        return self.operation(self, other, 'and')

    def __rand__(self, other): #&
        return self.operation(other, self, 'and')

    def __or__(self, other:Term): #|
        return self.operation(self, other, 'or')

    def __ror__(self, other:Term): #|
        return self.operation(other, self, 'or')
    
    def __mod__(self, other): #%
        return self.operation(self, other, '%')

    #non primitive operators:
    def __xor__(self, other:Term): #^
        return self.operation(self, other, '^')

    def __rxor__(self, other:Term): #^
        return self.operation(other, self, '^')
    
    def __matmul__(self, other): #@
        return self.operation(self, other, '@')
    
    def __rmatmul__(self, other): #@
        return self.operation(other, self, '@')

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
    
    # def __contains__(self, other): #in
    #     return self.comparison(self, other, 'in')



    def operation(self, left:Term, right:Term, operator:str):
        from .bin_operation import BinOperation
        if isinstance(right, TermHeader):
            right = right.val
        # if isinstance(right, list):
        #     if not isinstance(left, Term):
        #         from .leaf import Primitive
        #         left = Primitive(left)
        #     left.__header__ = self.merge_headers(left.__header__, right)
        #     return left
            
        # if isinstance(left, TermHeader):
        #     left = left.val
        # if isinstance(left, list):
        #     if not isinstance(right, Term):
        #         from .leaf import Primitive
        #         right = Primitive(right)
        #     right.__header__ = self.merge_headers(left, right.__header__)
        #     return right
        res = BinOperation(left, right, operator)
        res.merge_graphs()
        return res


    def comparison(self, left:Term, right:Term, operator:str):
        from .bin_operation import Comparison
        res = Comparison(left, right, operator)
        res.merge_graphs()
        return res

    def str(self, parentheses=False, full_names=False, translator:function=None):
        return self.serialize(parentheses, full_names, translator)

    def serialize(self, parentheses=True, full_names=True, for_header=False, translator=None) -> str:
        raise NotImplementedError
        

    def _simple_copy_terms(self, terms: List[Term]=None, translator=None):
        if terms is None:
            terms = list(self.terms_graph.values())

        copies = []
        for term in terms:
            term_copy = term._simple_copy(translator)
            copies.append(term_copy)

        for copy in copies:
            copy._restore_links(terms, copies)

        return copies



    def _simple_copy(self, translator=None) -> Term:
        res = Term()
        if hasattr(self, 'id') and self.id:
            res.id = self.id

        res.val = self.serialize(False, False, translator=translator)

        if hasattr(self, 'parentheses'):
            res.parentheses = self.parentheses
        else:
            res.parentheses = False
        return res


    def _restore_links(self, origin_terms, copies):
        self_orig_index = self.index_of(origin_terms)
        orig = origin_terms[self_orig_index]

        if hasattr(orig, 'left') and orig.left:
            left_copy_index = orig.left.index_of(copies)
            if left_copy_index != None:
                left_copy = copies[left_copy_index]
                self.left = left_copy
        if hasattr(orig, 'right') and orig.right:
            right_copy_index = orig.right.index_of(copies)
            if right_copy_index != None:
                right_copy = copies[right_copy_index]
                self.right = right_copy
        if hasattr(orig, 'left_parent') and orig.left_parent:
            left_parent_copy_index = orig.left_parent.index_of(copies)
            if left_parent_copy_index != None:
                left_parent_copy = copies[left_parent_copy_index]
                self.left_parent = left_parent_copy
        if hasattr(orig, 'right_parent') and orig.right_parent:
            right_parent_copy_index = orig.right_parent.index_of(copies)
            if right_parent_copy_index != None:
                right_parent_copy = copies[right_parent_copy_index]
                self.right_parent = right_parent_copy



    def index_of(self, terms: List[Term]):
        indexes = [index for (index, item) in enumerate(terms) if item.id == self.id]
        if len(indexes) > 1:
            raise EpureParseError('term occurred in a list more then once')
        if len(indexes) == 0:
            return None
        return indexes[0]


    def in_list(self, terms: List[Term]=None) -> bool:
        return self.index_of(terms) != None


    def go_until_hasattr(self, first_attr: str, second_attr: str, terms: List[Term]=None) -> Term:
        if terms is None:
            terms = list(self.terms_graph.values())

        iterat = self
        while True:
            first_attr_val: Term = getattr(iterat, first_attr, None)
            second_attr_val: Term = getattr(iterat, second_attr, None)

            if first_attr_val and first_attr_val.in_list(terms):
                iterat = first_attr_val

            elif second_attr_val and second_attr_val.in_list(terms):
                iterat = second_attr_val

            else:
                break

        return iterat


    def merge_headers(self, left_header, right_header):
        left_header = list(left_header)
        right_header = list(right_header)
        res = []
        for qp in right_header:
            if not qp.in_header(left_header):
                res.append(qp)
        res = left_header + res
        return res


class TermHeader(Term):
    def __init__(self, val:list) -> None:
        self.val = val


    # def go_until_hasattr(self, attr_names: List[str], terms: List[Term]=None) -> Term:
    #     next = self
    #     while True:
    #         has_attr = False
    #         for attr in attr_names:                
    #             if hasattr(next, attr):
    #                 tmp = getattr(next, attr) 
    #                 if tmp and tmp.index_of(terms) != None:
    #                     next = tmp
    #                     has_attr = True
    #                     break
    #         if not has_attr:
    #             return next

    #     # for attr_name in attr_names:
    #     #     if hasattr(self, attr_name):
    #     #         next = getattr(self, attr_name)
    #     #         break

    #     # if not next:
    #     #     return self
    #     # return next.go_until_hasattr(terms, attr_names)