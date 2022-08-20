from typing import List, Dict
from .term import Term
from .leaf import QueryingProxy
from ast import Constant, Name, BinOp, Eq, NotEq, LShift, RShift, parse, dump, NodeVisitor, NodeTransformer, unparse, walk, iter_child_nodes, AST
import re
# import astor
from ..helpers.string_helper import find_parentheses
from ..resource.db.table import Table
from ..helpers.type_helper import check_type
from uuid import uuid4

class JoinOperation:    
    table:str
    on_clause:str
    join_type:str
    join_id:str

    LEFT_TYPE='LEFT'
    RIGHT_TYPE='RIGHT'

    def __init__(self, table, on_clause, join_type='', join_id='') -> None:
        self.table = table
        self.on_clause = on_clause
        self.join_type = join_type
        self.join_id = join_id



class TermParser(NodeTransformer):
    header:List[QueryingProxy]
    joins:List[JoinOperation]
    parent = None
    resource:Table

    def __init__(self, resource:Table) -> None:
        self.resource = resource
        self.joins = []

    
    def parse(self, header:List[QueryingProxy], body:object) -> str:
        check_type('body', body, [Term, str])
        body = str(body)

        self.joins = []        
        body = self.collect_joins(body)
        where_clause = self.remove_join_ids(body)
        
        res = self.resource.serialize_read(header, self.joins, where_clause)
        self.joins = []
        return res


    def collect_joins(self, body:str):
        tree = parse(body)
        self.visit(tree)
        res = unparse(tree)
        return res


    def remove_join_ids(self, body:str):

        for join in self.joins:
            body = body.replace(join.join_id, '')

        #needed?
        while '()' in body:
            body = body.replace('()', '')

        body = self.clear_parentheses(body, '( and')
        body = self.clear_parentheses(body, '(and')
        body = self.clear_parentheses(body, '( or')
        body = self.clear_parentheses(body, '(or')
        body = self.clear_parentheses(body, 'and )')
        body = self.clear_parentheses(body, 'and)')
        body = self.clear_parentheses(body, 'or )')
        body = self.clear_parentheses(body, 'or)')
        #needed?

        body = body.replace('^', '')

        return body

    def clear_parentheses(self, body:str, pattern:str):
        if pattern not in body:
            return body

            
        while pattern in body:
            first = body.index(pattern)
            parentheses = find_parentheses(body)
            second = parentheses[first]

            list_body = list(body)
            list_body[first] = ''
            list_body[second] = ''
            body = ''.join(list_body)

        return body


    def visit_BinOp(self, node:BinOp):
        self.generic_visit(node)
        op = node.op
        if not (isinstance(op, LShift) or isinstance(op, RShift)):
            return node

        join_type = JoinOperation.LEFT_TYPE if isinstance(op, LShift)\
            else JoinOperation.RIGHT_TYPE
        left = unparse(node.left)
        right = unparse(node.right)
        join_id = 'join_' + str(uuid4()).replace('-', '')

        join = JoinOperation(left, right, join_type, join_id)
        self.joins.append(join)
        return Name(join_id)


    # def visit_LShift(self, node: LShift):        
    #     left = unparse(node.parent.left)
    #     right = unparse(node.parent.right)
    #     unparsed = unparse(node.parent)
    #     # unparsed = astor.to_source(node.parent)
    #     # unparsed = unparsed.replace('\n', '')
    #     # if unparsed[0] == '(' and unparsed[-1] == ')':
    #     #     unparsed = unparsed[1:-1]
    #     join = JoinOperation(left, right, JoinOperation.LEFT_TYPE, unparsed)
    #     self.joins.append(join)
    #     return node
    

    # def visit(self, node):
    #     node.parent = self.parent
    #     self.parent = node
    #     self.generic_visit(node)
    #     if isinstance(node, LShift):
    #         node = self.visit_LShift(node)
    #     if isinstance(node, AST):
    #         self.parent = node.parent
    #     return node