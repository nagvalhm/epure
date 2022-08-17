from __future__ import annotations
from msilib.schema import Error
from turtle import left, right
from typing import Dict, List, TYPE_CHECKING
from uuid import UUID, uuid4
if TYPE_CHECKING:
    from ..resource.db.db import Db


class Term:
    id:UUID
    terms_graph: Dict[UUID, Term]
    left_parent:Term = None
    right_parent:Term = None
    val:str

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
        from .binary import BinOperation
        res = BinOperation(left, right, operator)
        res.merge_graphs()
        return res


    def comparison(self, left:Term, right:Term, operator:str):
        from .binary import Comparison
        res = Comparison(left, right, operator)
        res.merge_graphs()
        return res

    def __str__(self):
        return self.serialize(True)

    def serialize(self, for_debug=False) -> str:
        raise NotImplementedError

    def _simple_copy(self) -> Term:
        res = Term()
        if hasattr(self, 'id') and self.id:
            res.id = self.id

        res.val = self.serialize(True)

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
            raise Error('term occurred in a list more then once')
        if len(indexes) == 0:
            return None
        return indexes[0]


    def go_until_hasattr(self, attr_name) -> Term:
        next = None
        if hasattr(self, attr_name):
            next = getattr(self, attr_name)

        if not next:
            return self
        return next.go_until_hasattr(attr_name)