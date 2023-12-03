from _ast import BoolOp
from typing import Any
# from ..epure.parser.leaf import DbProxy
from ..epure.parser.ast_parser.db_proxy import DbProxy
from ..epure.parser.term_parser import TermParser
from .epure_classes import db as real_db
# import networkx as nx
# import matplotlib.pyplot as plt
# from ..epure.parser.term_debugger import MatplotTermDebugger
from ..epure import epure, Epure
import inspect
import ast
import textwrap
import types
import pdb
from ..epure.parser.ast_parser.ast_parser import AstParser
from ..epure.epure import escript, select

import pytest

def foo1():
    return 1

def foo2():
    return 2

def test_simple_queries_ast_parser_read_decorator():
    # dbp = DbProxy(real_db)
    # tp = dbp['oraculs_domain.competitions']
    # y = dbp['oraculs_domain.oraculs']

    # class AstParser(ast.NodeTransformer):
    # class ReadHolderCls:
    #     def read(func):
    #         def inner(self, *args, **kwargs):
    #             dbp = DbProxy(self.resource.db)
    #             self.tp = dbp["public.ast_parser_test_cls"]
    #             func_source = inspect.getsource(func)
    #             dedent_src = textwrap.dedent(func_source)

    #             func_parsed = AstParser().parse(dedent_src)
                
    #             # ast.fix_missing_locations(changed_tree)

    #             co = compile(func_parsed, "debug_parser.py", "exec")

    #             fn = types.FunctionType(co.co_consts[0], globals())

    #             res = fn(self,*args)

    #             # exec(co, globals())
    #             res = self.resource.read(res)
                
    #             return res
    #             # return self.resource.read(res)
    #         return inner
        
        # def visit_BoolOp(self, node: BoolOp) -> Any:

        #     return ast.Constant("Hello, Monkeys!!!")
        

    @epure()
    # class AstParserTestCls(ReadHolderCls):
    class AstParserTestCls:
        int_field:int
        f2:str
        f1:str
        f8:str
        f4:str
        # @ReadHolderCls.read
        # def foo(self, param):
        #     print(param)
        #     # var = foo2()
        #     # query = tp.f1 == 1 and tp.f2 == var
        #     query = tp.f1.abc == 1 and tp.f2 == 4
        #     return query + param

        # @read
        # def test_raw_str_like_diff_variants(self123):

        #     query = self123.tp.f2.like(r'%percent01R')

        #     query = self123.tp.f2.like(r"%percent02R")

        #     query = not self123.tp.f2.like(r"""%percent03R""")

        #     query = self123.tp.f2.Not_Like(r"""%percent03R""")

        #     like = self123.tp.like

        #     query = self123.tp.f2 != like(r"""%percent03R""")

        #     query = self123.tp.f2 == self123.tp.like(r"""%percent03R""")

        #     import Like

        #     query = self123.tp.f2 != Like(r"""%percent03R""")


        #     res = self123.resource.read([self123.tp.f1, self123.tp.f2], query)

        @escript
        def test_default_vals_w_read(self, abc:str = "cats"):
            query = self.tp.f2 == abc
            res = self.resource.read([self.tp.f1, self.tp.f2], query)
            return abc

        @escript
        def test_raw_str_like(self123):

            query = self123.tp.f2 == "%a" and self123.tp.f2 == "\%a"

            assert query == "public.ast_parser_test_cls.f2 LIKE '%a' AND public.ast_parser_test_cls.f2 = '\\\\%a'"

            res = self123.resource.read([self123.tp.f1, self123.tp.f2], query)
                
        @escript
        def test_diff_cases(self123):
            var = self123.tp.f1
            var.pole = self123.tp.f1
            var = True
            tup = ("dr","dgb")
            lst = ["br","zcv"]

            tptst = self123.tp

            query = self123.tp.f2 == '%percent0'

            query = self123.tp.f2 == r'%percent01R'

            query = self123.tp.f2 == r"%percent02R"

            query = self123.tp.f2 == r"""%percent03R"""

            query = self123.tp.f2 == '\\%percent1'

            query = self123.tp.f2 == r'\\%percent1R'
            
            query = self123.tp.f2 == '%\\%percent\\%2'
            
            query = self123.tp.f2 == r'%\\%percent\\%2R'

            query = self123.tp.f2 == '%\\%percent\\%%3'

            query = self123.tp.f2 == r'%\\%percent\\%%3R'

            query = self123.tp.f2 == 'percent4'

            query = self123.tp.f2 == r'percent4R'

            query = self123.tp.f2 == '_undscore5'

            query = self123.tp.f2 == r'_undscore5R'

            query = self123.tp.f2 == '\\_undscore6'

            query = self123.tp.f2 == r'\\_undscore6R'
            
            query = self123.tp.f2 == '_\\_undscore\\_7'

            query = self123.tp.f2 == r'_\\_undscore\\_7R'

            query = self123.tp.f2 == '_\\_undscore\\__8'

            query = self123.tp.f2 == r'_\\_undscore\\__8R'

            query = tptst.f2 == '_\\_undscore\\__8' and tptst.f2 == r'_\\_undscore\\__8R'

            # unterminated string literal case
            # query = self123.tp.f2 == 'undscore9\\'

            query = self123.tp.f2 == r'undscore9\\R'

            query = f"{var}"

            query = "abc" == self123.tp.f2

            query = True == True and True == False

            query = 4 == var and 45 == var.pole

            query = 5 == self123.tp.f2 and False == 82

            query = self123.tp.f1 == 5 and True == 5

            query = self123.tp.f1 == 5 or True == 5

            query = True == 5 or self123.tp.f1 == 5

            query = self123.tp.f1 == 5 or "basc" == self123.tp.f1 

            query = 5 == self123.tp.f2 and self123.tp.f1 == 234

            query = self123.tp.f1 == 234 and 5 == self123.tp.f2
            
            query = self123.tp.f1 == "234" and "abc" == self123.tp.f2

            query = self123.tp.f4 in ("abc","def") and self123.tp.f8 in lst

            query = self123.tp.f4 in ["abc","def"] and self123.tp.f8 in lst

            query = "abc" in ["abc","def"] and "abc" in lst

            query = "abc" == self123.tp.f2 or "def" == self123.tp.f2 and self123.tp.f1 == "cor" and self123.tp.f1 == "vet"

            tptst = self123.tp

            res = self123.resource.read([tptst.f1, tptst.f2], query)

            return res

        @escript
        def test_wrong_columns_attr_error(self):
            query = 5 == self.tp.col_4 or 5 == self.tp.col_4 and self.tp.col_5 == 234 and self.tp.col_8 == 234
            res = self.resource.read([self.tp.col_4, self.tp.col_5, self.tp.col_8], query)

            return res
        
        @escript
        def test_in_sql_func(self342):
            lst = ["br","zcv"]
            query = self342.tp.f4 in ("abc","def") and self342.tp.f8 in lst
            res = self342.resource.read([self342.tp.f4, self342.tp.f8], query)
            return res
        
        @escript
        def test_like_sql_func(self342):
            query = self342.tp.f4 == "%def"
            res = self342.resource.read([self342.tp.f4, self342.tp.f8], query)
            return query
        
    AstParserTestCls().test_default_vals_w_read()
    AstParserTestCls().test_default_vals_w_read("brain")
        
    res = AstParserTestCls().test_raw_str_like()
        
    res = AstParserTestCls().test_diff_cases()
    try:
        res = AstParserTestCls().test_wrong_columns()
        assert False
    except(AttributeError):
        assert True

    res = AstParserTestCls().test_in_sql_func()

    res = AstParserTestCls().test_like_sql_func()

    @epure()
    class AstParserTestCls2:
        name:str
        last_name:str
        age:int

        def __init__(self, name, last_name, age) -> None:
            self.name = name
            self.last_name = last_name
            self.age = age

        @escript
        def find_sql_in_mike_ermantraut_or_wazowsky(self):
            tp = self.tp
            query = tp.name == "Mike" and tp.last_name in ('Wazowsky', 'Ermantraut')
            assert query == "public.ast_parser_test_cls2.name = 'Mike' AND public.ast_parser_test_cls2.last_name IN ('Wazowsky', 'Ermantraut')"
            res = self.resource.read([self.tp.name, self.tp.last_name, self.tp.age], query)
            return res
        
        @escript
        def find_sql_like_m(self33):
            tp = self33.tp
            query = tp.name == "M%" or 84 == tp.age
            assert query == "public.ast_parser_test_cls2.name LIKE 'M%' OR public.ast_parser_test_cls2.age = 84"
            res = self33.resource.read([self33.tp.name, self33.tp.last_name, self33.tp.age], query)
            return res

        @escript
        def find_sql_like_V_backshash(self33):
            def test():
                return 3
            tp = self33.tp
            query = tp.name == r"\%Victor"
            # assert query == r"public.ast_parser_test_cls2.name = '\\%Victor'"
            res = self33.resource.read([self33.tp.name, self33.tp.last_name, self33.tp.age], query)
            return res
        
        @escript
        def find_sql_no_header(self33):
            tp = self33.tp
            query = tp.name == "Mike"
            # assert query == r"public.ast_parser_test_cls2.name = '\\%Victor'"
            res = self33.resource.read(query)
            return res
        
        @escript
        def find_sql_empty_read(self33):
            res = self33.resource.read()
            return res
        
        @escript
        def sql_subquery_select_func(self):
            tp = self.tp
            res = tp.last_name in select([tp], tp.name == "Mike")
            return res
        
    erman = AstParserTestCls2("Mike", "Ermantraut", 60)
    erman.save()
    wazow = AstParserTestCls2("Mike", "Wazowsky", 20)
    wazow.save()
    killof = AstParserTestCls2("Mike", "Killof", 42)
    killof.save()
    erm = AstParserTestCls2("Viktor", "Ermantraut", 84)
    erm.save()
    golden = AstParserTestCls2("Mark", "Golden", 30)
    golden.save()
    mona = AstParserTestCls2("Mona", "Traumb", 50)
    mona.save()
    matthew = AstParserTestCls2("Matthew", "Crysler", 50)
    matthew.save()
    maten = AstParserTestCls2("Maten", "Dragov", 50)
    maten.save()
    vic = AstParserTestCls2("\%Victor", "Volben", 50)
    vic.save()


    res1 = erman.find_sql_in_mike_ermantraut_or_wazowsky()
    assert res1
    
    res2 = erman.find_sql_like_m()
    assert res2

    res3 = erman.find_sql_like_V_backshash()
    assert res3

    res4 = erman.find_sql_no_header()
    assert res4

    res5 = erman.find_sql_empty_read()
    assert res5

    res6 = erman.sql_subquery_select_func()
    assert res6

# def lambda db, tp: tp.