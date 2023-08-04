from typing import List, Dict, Union
from .term import Term, TermHeader
from .leaf import QueryingProxy
from ast import Constant, Name, BinOp, Eq, NotEq, LShift, RShift, BitXor, parse, dump, NodeVisitor, NodeTransformer, unparse, walk, iter_child_nodes, AST, Mod, And, GtE, Tuple
import re
# import astor
from ..helpers.string_helper import find_parentheses
from ..helpers.dict_helper import reverse_dict
from ..resource.db.table import Table
from ..helpers.type_helper import check_type
from uuid import uuid4
from ..errors import EpureParseError
from .leaf import Leaf

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

    
    def parse(self, *args) -> str:
        #args
        header:Union[List[QueryingProxy], TermHeader] = None
        body:object = None
        full_names=True

        first = args[0]
        if isinstance(first, list) or isinstance(first, tuple):
            header = list(args[0])
            body = args[1]
            if len(args) > 2:
                full_names = args[2]
        else:
            header = []
            body = args[0]
            if len(args) > 1:
                full_names = args[1]

        check_type('body', body, [Term, str])
        if isinstance(header, TermHeader):
            header = header.val

        if isinstance(body, Term):
        # if isinstance(body, Term) and header:
            header = body.merge_headers(header, body.__header__)

        # if not header:
        #     raise EpureParseError('header not defined')

        body = body.str(True, full_names, self.resource.db.cast_py_db_val)
        self.joins.clear()
        # self.collect_joins(body)
        body = self.collect_joins(body)
        where_clause = self.remove_join_ids(body)

        if '@' in body:
            res = body.split(' @ ', 1)
            where_clause = res[1]
            header = res[0]
            if header[0] == '(':
                # header = eval(header)
                # header = header[1:-1]
                header = header.replace('(','')
                header = header.replace(')','')
                header = tuple(header.split(', '))
            else:
                header = (header,)
        
        if not header:
            header = (self.resource.querying_proxy,)
            # header = self.parse_for_headers(where_clause)
            # if header:
                

        res = self.resource.serialize_read(header, self.joins, where_clause, full_names)
        self.joins = []
        return res

    def parse_for_headers(self, body):
        res = []
        # if '@' in body:
        #    res = (body.split(' @ '))
        
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
        # match = re.search(pattern, repl)
        body = body.replace(' ^ ', '')
        body = body.replace('^ ', '')
        body = body.replace(' ^', '')
        body = body.replace('^', '')

        while '()' in body:
            body = body.replace('()', '')

        body = self.clear_parentheses(body, '( and')
        body = self.clear_parentheses(body, '(and')
        body = self.clear_parentheses(body, '( or')
        body = self.clear_parentheses(body, '(or')

        body = self.clear_parentheses(body, 'and )', 4)
        body = self.clear_parentheses(body, 'and)', 3)
        body = self.clear_parentheses(body, 'or )', 3)
        body = self.clear_parentheses(body, 'or)', 2)
        #needed?

        # body = body.replace('^', '')

        return body

    def clear_parentheses(self, body:str, pattern:str, offset:int=0):
        if pattern not in body:
            return body

            
        while pattern in body:
            first = body.index(pattern) + offset
            open_close_parentheses = find_parentheses(body)
            
            second = None
            if first in open_close_parentheses:
                second = open_close_parentheses[first]
            else:
                close_open_parentheses = reverse_dict(open_close_parentheses)
                second = close_open_parentheses[first]

            if second == None:
                raise EpureParseError()

            list_body = list(body)
            list_body[first] = ''
            list_body[second] = ''
            body = ''.join(list_body)

        return body


    def visit_BinOp(self, node:BinOp):
        self.generic_visit(node)
        op = node.op

        if isinstance(op,Mod) and isinstance(node.right.value, str):
            return Name(f"{unparse(node.left)} like {unparse(node.right)}")

        # if isinstance(op, And) and (isinstance() or )
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
    
    # def serialize_tuple(self, ast_tuple:Tuple):
    #         res = []
    #         for const in ast_tuple.elts:
    #             res.append(const.value)
            
    #         return str(tuple(res))

    def visit_Compare(self, node:GtE):
        self.generic_visit(node)
        op = node.ops[0]

        if isinstance(op, GtE) and (isinstance(node.comparators[0], Tuple) or isinstance(node.comparators[0], BinOp)):
            # Ast_tuple_str = self.serialize_tuple(node.comparators[0])
            # return Name(f"{node.left.id} in {self.serialize_tuple(node.comparators[0])}")
            return Name(f"{unparse(node.left)} in {unparse(node.comparators[0])}")
        else:
            return node

    

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