# from typing import List, Dict
# from .term import  Pseudo, JoinBinary, Term
# from .db_entity_resource import DbEntityResource
# from ast import Eq, NotEq, LShift, parse, dump, NodeVisitor, NodeTransformer, unparse, walk, iter_child_nodes, AST
# import re
# import astor
# from ...helpers.string_helper import find_parentheses


# class SelectQuery(NodeVisitor):
#     header:List[Pseudo]
#     joins:List[JoinBinary]
#     where_clause:str
#     parent = None

#     def __init__(self, header:List[Pseudo], body:Term) -> None:
#         self.header = header
#         self.joins = []
        
#         self.set_where_clause(str(body))


#     def set_where_clause(self, body:str):
#         tree = parse(body)
#         self.visit(tree)
#         body = self.remove_py_joins(body)        

#         self.where_clause = body


#     def remove_py_joins(self, body:str):

#         for join in self.joins:
#             body = body.replace(join.unparsed, '')

#         while '()' in body:
#             body = body.replace('()', '')

#         body = self.clear_parentheses(body, '( and')
#         body = self.clear_parentheses(body, '(and')
#         body = self.clear_parentheses(body, '( or')
#         body = self.clear_parentheses(body, '(or')
#         body = self.clear_parentheses(body, 'and )')
#         body = self.clear_parentheses(body, 'and)')
#         body = self.clear_parentheses(body, 'or )')
#         body = self.clear_parentheses(body, 'or)')

#         body = body.replace('^', '')

#         return body

#     def clear_parentheses(self, body:str, pattern:str):
#         if pattern not in body:
#             return body

            
#         while pattern in body:
#             first = body.index(pattern)
#             parentheses = find_parentheses(body)
#             second = parentheses[first]

#             list_body = list(body)
#             list_body[first] = ''
#             list_body[second] = ''
#             body = ''.join(list_body)

#         return body





#     def visit_LShift(self, node: LShift):        
#         left = unparse(node.parent.left)
#         right = unparse(node.parent.right)
#         unparsed = astor.to_source(node.parent)
#         unparsed = unparsed.replace('\n', '')
#         join = JoinBinary(left, right, JoinBinary.LEFT_TYPE, unparsed)
#         self.joins.append(join)
#         return node
    

#     def visit(self, node):
#         node.parent = self.parent
#         self.parent = node
#         self.generic_visit(node)
#         if isinstance(node, LShift):
#             node = self.visit_LShift(node)
#         if isinstance(node, AST):
#             self.parent = node.parent
#         return node