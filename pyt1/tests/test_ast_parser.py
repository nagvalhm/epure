from _ast import BoolOp
from typing import Any
# from ..epure.parser.leaf import DbProxy
from ..epure.parser.ast_parser.db_proxy import DbProxy
from ..epure.parser.term_parser import TermParser
from .epure_classes import db as real_db
import networkx as nx
import matplotlib.pyplot as plt
from ..epure.parser.term_debugger import MatplotTermDebugger
from ..epure import epure, Epure
import inspect
import ast
import textwrap
import types
import pdb
from ..epure.parser.ast_parser.ast_parser import AstParser

def foo1():
    return 1

def foo2():
    return 2

def test_simple_queries_ast_parser_read_decorator():
    dbp = DbProxy(real_db)
    tp = dbp['oraculs_domain.competitions']
    # y = dbp['oraculs_domain.oraculs']

    # class AstParser(ast.NodeTransformer):
    class ReadHolderCls:
        def read(func):
            def inner(self, *args, **kwargs):
                # func_source = inspect.getsource(func)
                # dedent_src = textwrap.dedent(func_source)

                # func_tree = ast.parse(dedent_src)
                func_parsed = AstParser().parse(func, *args, **kwargs)
                # res = func_str.exec()
                # changed_tree = visitor.visit(func_tree)
                # res = ast.unparse(changed_tree)
                # ast.fix_missing_locations(changed_tree)

                co = compile(func_parsed, "codeod.py", "exec")

                fn = types.FunctionType(co.co_consts[0], globals())

                res = fn(self,*args)

                # exec(co, globals())
                
                return res
                # return self.resource.read(res)
            return inner
        
        def visit_BoolOp(self, node: BoolOp) -> Any:

            return ast.Constant("Hello, Monkeys!!!")
        

    @epure()
    class AstParserTestCls(ReadHolderCls):
        @ReadHolderCls.read
        def foo(self, param):
            print(param)
            var = foo2()
            query = tp.f1 == 1 and tp.f2 == var
            return query + param
        
        @ReadHolderCls.read
        def foo2(self,tp,dbp):
            var = tp.f1

            query = True == True and True == False

            query = tp.f1 == 5

        @ReadHolderCls.read
        def foo3(self,tp,dbp):
            var = True
        
    AstParserTestCls().foo(" and some bongos-bongos")
    AstParserTestCls().foo2(tp,dbp)