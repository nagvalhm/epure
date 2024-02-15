from __future__ import annotations
import pytest
from _ast import BoolOp
from typing import Any
# from ..epure.parser.leaf import Domain
from ..epure.parser.inspect_parser.domain import Domain
from ..epure import epure
from ..epure import escript
# import inspect
# import typing
import jsonpickle
from ..epure.generics import NotNull
from typing import List

def foo1():
    return 1

def foo2():
    return 2

def test_simple_queries_inspect_parser_read_decorator():
    # dom = Domain(real_db)
    # tp = dom['oraculs_domain.competitions']
    # y = dom['oraculs_domain.oraculs']

    # class AstParser(ast.NodeTransformer):
    # class ReadHolderCls:
    #     def read(func):
    #         def inner(self, *args, **kwargs):
    #             dom = Domain(self.resource.db)
    #             self.tp = dom["public.inspect_parser_test_cls"]
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
    class InspectParserTestCls:
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


        #     res = self123.resource.read([self123.md.f1, self123.md.f2], query)

        @escript
        def test_default_vals_w_read(self, abc:str = "cats"):
            query = self.md.f2 == abc
            res = self.resource.read([self.md.f1, self.md.f2], query)
            return abc

        @escript
        def test_raw_str_like(self123):

            query = self123.md.f2.like("%a") and self123.md.f2.like("\%a")

            assert query == "public.inspect_parser_test_cls.f2 LIKE '%a' AND public.inspect_parser_test_cls.f2 LIKE '\\\\%a'"

            res = self123.resource.read([self123.md.f1, self123.md.f2], query)
                
        @escript
        def test_diff_cases(self123):
            var = self123.md.f1
            var.pole = self123.md.f1            
            tup = ("dr","dgb")
            lst = ["br","zcv"]

            tptst = self123.md

            query = self123.md.f2.like('%percent0')

            query = self123.md.f2.like(r'%percent01R')

            query = self123.md.f2.like(r"%percent02R")

            query = self123.md.f2.like(r"""%percent03R""")

            query = self123.md.f2.like('\\%percent1')

            query = self123.md.f2.like(r'\\%percent1R')
            
            query = self123.md.f2.like('%\\%percent\\%2')
            
            query = self123.md.f2.like(r'%\\%percent\\%2R')

            query = self123.md.f2.like('%\\%percent\\%%3')

            query = self123.md.f2.like(r'%\\%percent\\%%3R')

            query = self123.md.f2.like('percent4')

            query = self123.md.f2.like(r'percent4R')

            query = self123.md.f2.like('_undscore5')

            query = self123.md.f2.like(r'_undscore5R')

            query = self123.md.f2.like('\\_undscore6')

            query = self123.md.f2.like(r'\\_undscore6R')
            
            query = self123.md.f2.like('_\\_undscore\\_7')

            query = self123.md.f2.like(r'_\\_undscore\\_7R')

            query = self123.md.f2.like('_\\_undscore\\__8')

            query = self123.md.f2.like(r'_\\_undscore\\__8R')

            query = tptst.f2.like('_\\_undscore\\__8') and tptst.f2.like(r'_\\_undscore\\__8R')

            # unterminated string literal case
            # query = self123.md.f2 == 'undscore9\\'

            query = self123.md.f2.like(r'undscore9\\R')

            query = f"{var}"

            query = "abc" == self123.md.f2

            query = True == True and True == False

            query = 4 == var and 45 == var.pole

            query = 5 == self123.md.f2 and False == 82

            query = self123.md.f1 == 5 and True == 5

            query = self123.md.f1 == 5 or True == 5

            query = True == 5 or self123.md.f1 == 5

            query = self123.md.f1 == 5 or "basc" == self123.md.f1 

            query = 5 == self123.md.f2 and self123.md.f1 == 234

            query = self123.md.f1 == 234 and 5 == self123.md.f2
            
            query = self123.md.f1 == "234" and "abc" == self123.md.f2

            query = self123.md.f4 in ("abc","def") and self123.md.f8 in lst

            query = self123.md.f4 in ["abc","def"] and self123.md.f8 in lst

            query = "abc" in ["abc","def"] and "abc" in lst

            query = "abc" == self123.md.f2 or "def" == self123.md.f2 and self123.md.f1 == "cor" and self123.md.f1 == "vet"

            tptst = self123.md

            res = self123.resource.read([tptst.f1, tptst.f2], query)

            return res

        @escript
        def test_wrong_columns_attr_error(self):
            query = 5 == self.md.col_4 or 5 == self.md.col_4 and self.md.col_5 == 234 and self.md.col_8 == 234
            res = self.resource.read([self.md.col_4, self.md.col_5, self.md.col_8], query)

            return res
        
        @escript
        def test_in_sql_func(self342):
            lst = ["br","zcv"]
            query = self342.md.f4 in ("abc","def") and self342.md.f8 in lst
            res = self342.resource.read([self342.md.f4, self342.md.f8], query)
            return res
        
        @escript
        def test_like_sql_func(self342):
            query = self342.md.f4.like("%def")
            res = self342.resource.read([self342.md.f4, self342.md.f8], query)
            return query
        
        @escript
        def test_no_sql_operator(self342):
            query = self342.md.f4 > 3 and not self342.md.f4 < 20
            assert query == "public.inspect_parser_test_cls.f4 > 3 AND NOT public.inspect_parser_test_cls.f4 < 20"
            # res = self342.resource.read([self342.md.f4, self342.md.f8], query)
            return query
        
    InspectParserTestCls().test_default_vals_w_read()
    InspectParserTestCls().test_default_vals_w_read("brain")
        
    res = InspectParserTestCls().test_raw_str_like()
        
    res = InspectParserTestCls().test_diff_cases()
    try:
        res = InspectParserTestCls().test_wrong_columns_attr_error()
        assert False
    except(AttributeError):
        assert True

    res = InspectParserTestCls().test_in_sql_func()

    res = InspectParserTestCls().test_like_sql_func()

    res = InspectParserTestCls().test_no_sql_operator()

def test_inspect_parser_like_comp_etc():

    @epure()
    class InspectParserTestCls2:
        name:str
        last_name:str
        age:int

        def __init__(self, name, last_name, age) -> None:
            self.name = name
            self.last_name = last_name
            self.age = age

        @escript
        def test_self_cls_inst_creation(self):
            ins = InspectParserTestCls2("Mike", "Ermantraut", 60)
            ins

        @escript
        def find_sql_in_mike_ermantraut_or_wazowsky(self):
            md = self.md
            query = md.name == "Mike" and md.last_name in ('Wazowsky', 'Ermantraut')
            assert query == "public.inspect_parser_test_cls2.name = 'Mike' AND public.inspect_parser_test_cls2.last_name IN ('Wazowsky', 'Ermantraut')"
            res = self.resource.read([self.md.name, self.md.last_name, self.md.age], query)
            return res
        
        @escript
        def find_sql_like_m(self33):
            md = self33.md
            query = md.name.like("M%") or 84 == md.age
            assert query == "public.inspect_parser_test_cls2.name LIKE 'M%' OR public.inspect_parser_test_cls2.age = 84"
            res = self33.resource.read([self33.md.name, self33.md.last_name, self33.md.age], query)
            return res

        @escript
        def find_sql_like_V_backshash(self33):
            def test():
                return 3
            md = self33.md
            query = md.name.like(r"%Victor")
            # assert query == r"public.inspect_parser_test_cls2.name = '\\%Victor'"
            res = self33.resource.read([self33.md.name, self33.md.last_name, self33.md.age], query)
            return res
        
        @escript
        def find_sql_no_header(self33):
            md = self33.md
            query = md.name == "Mike"
            # assert query == r"public.inspect_parser_test_cls2.name = '\\%Victor'"
            res = self33.resource.read(query)
            return res
        
        @escript
        def find_sql_empty_read(self33):
            res = self33.resource.read()
            return res
        
        @escript
        def sql_subquery_select_func(self):
            md = self.md
            res = md.last_name in md.select([md], md.name == "Mike")
            return res
        
        @escript
        def sql_subquery_wrong_func(self):
            md = self.md
            res = md.last_name in foo1()
            return res
        
        @escript
        def sql_subquery_select_real_ex(self):
            md = self.md
            tp_oraculs_dom_tasks = self.dom.oraculs_domain.tasks
            query = md.name in md.select([md.name], md.age == 50)
            assert query == 'public.inspect_parser_test_cls2.name IN (SELECT public.inspect_parser_test_cls2.name as public___inspect_parser_test_cls2___name FROM public.inspect_parser_test_cls2 \n  WHERE \n public.inspect_parser_test_cls2.age = 50)'
            res = self.resource.read(query)
            # self.resource.read([md.first_name, md.last_name], md.node_id in select([self.dom['tp2'].node_id]))
            return res
        
        @escript
        def test_not_eq(self):
            md = self.md

            query1 = md.name != "Mike" and md.last_name not in ("Ermantraut", "Traumb")
            assert query1 == "public.inspect_parser_test_cls2.name <> 'Mike' AND public.inspect_parser_test_cls2.last_name NOT IN ('Ermantraut', 'Traumb')"
            res1 = self.resource.read(query1)

            query2 = md.last_name not in ("Ermantraut", "Traumb") and not md.name != "Mike"
            assert query2 == "public.inspect_parser_test_cls2.last_name NOT IN ('Ermantraut', 'Traumb') AND NOT public.inspect_parser_test_cls2.name <> 'Mike'"
            res2 = self.resource.read(query2)

            query3 = not md.age >= 30 or md.name > "Mike"
            assert query3 == "NOT public.inspect_parser_test_cls2.age >= 30 OR public.inspect_parser_test_cls2.name > 'Mike'"
            res3 = self.resource.read(query3)

            query4 = md.name < "Mike" and not md.age <= 30
            assert query4 == "public.inspect_parser_test_cls2.name < 'Mike' AND NOT public.inspect_parser_test_cls2.age <= 30"
            res4 = self.resource.read(query4)

            # expect error bc column returns more than one val

            # query5 = md.name > md.select([md.name], md.age <= 30)
            # assert query5 == 'public.inspect_parser_test_cls2.name > (SELECT public.inspect_parser_test_cls2.name as public___inspect_parser_test_cls2___name FROM public.inspect_parser_test_cls2 \n  WHERE \n public.inspect_parser_test_cls2.age <= 30)'
            # res5 = self.resource.read(query5)

            query6 = md.name in md.select([md.name], md.age <= 30)
            assert query6 == "public.inspect_parser_test_cls2.name IN (SELECT public.inspect_parser_test_cls2.name as public___inspect_parser_test_cls2___name FROM public.inspect_parser_test_cls2 \n  WHERE \n public.inspect_parser_test_cls2.age <= 30)"
            res6 = self.resource.read(query6)

            # expect Value error bc header is not passed into select
            
            # try:
            #     query8 = md.name > md.select(md.age <= 30)
            #     assert False
            # except ValueError:
            #     assert True

            # expect error raise with wrong type
            # try:
            #     query7 = md.last_name > ('bf', 'gena')
            #     assert False
            # except TypeError:
            #     assert True 

            return res4
        
        @escript
        def test_is_and_is_not(self, val):
            jsonpickle.encode(val)
            inst = InspectParserTestCls2("Mike", "Ermantraut", 60)
            # inst
            md = self.md

            query1 = md.name != "Mike" and md.last_name is not None
            assert query1 == "public.inspect_parser_test_cls2.name <> 'Mike' AND public.inspect_parser_test_cls2.last_name IS NOT NULL"
            res1 = self.resource.read(query1)

            query2 = not md.name != "Mike" or not md.last_name is None
            assert query2 == "NOT public.inspect_parser_test_cls2.name <> 'Mike' OR NOT public.inspect_parser_test_cls2.last_name IS NULL"
            res2 = self.resource.read(query2)

            try:
                query4 = md.last_name is "None"
                assert False
            except TypeError:
                assert True

            query2 = not md.name != "Mike" or not md.last_name is not val
            assert query2 == "NOT public.inspect_parser_test_cls2.name <> 'Mike' OR NOT public.inspect_parser_test_cls2.last_name IS NOT NULL"

        @classmethod
        @escript
        def cls_method_escript(cls):
            inst = InspectParserTestCls2("Mike", "Ermantraut", 60)
            cls_mod = cls.model(InspectParserTestCls2)
            query1 = cls.md.name != "Mike" and cls.md.last_name is not None
            assert query1 == "public.inspect_parser_test_cls2.name <> 'Mike' AND public.inspect_parser_test_cls2.last_name IS NOT NULL"
            return query1

    # sig = inspect.signature(InspectParserTestCls2.__init__)
    # type_hints = typing.get_type_hints(InspectParserTestCls2)

    erman = InspectParserTestCls2("Mike", "Ermantraut", 60)
    erman.save()
    wazow = InspectParserTestCls2("Mike", "Wazowsky", 20)
    wazow.save()
    killof = InspectParserTestCls2("Mike", "Killof", 42)
    killof.save()
    erm = InspectParserTestCls2("Viktor", "Ermantraut", 84)
    erm.save()
    golden = InspectParserTestCls2("Mark", "Golden", 30)
    golden.save()
    mona = InspectParserTestCls2("Mona", "Traumb", 50)
    mona.save()
    matthew = InspectParserTestCls2("Matthew", "Crysler", 50)
    matthew.save()
    maten = InspectParserTestCls2("Maten", "Dragov", 50)
    maten.save()
    vic = InspectParserTestCls2("\%Victor", "Volben", 50)
    vic.save()

    erman.test_self_cls_inst_creation()

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

    try:
        res7 = erman.sql_subquery_wrong_func()
        assert False
    except(TypeError):
        assert True

    res8 = erman.sql_subquery_select_real_ex()
    assert res8

    res9 = erman.test_not_eq()
    assert res9

    res10 = erman.test_is_and_is_not(None)
    # assert res10

    res11 = InspectParserTestCls2.cls_method_escript()

# def lambda db, tp: tp.
    
def test_docs_cats_example():

    @epure()
    class Cat:
        paws_cntr:int
        name:str
        tail_cntr:int
        likes_catnip:bool

        def __init__(self, paws_cntr, name, tail_cntr, likes_catnip):
            self.paws_cntr = paws_cntr
            self.name = name
            self.tail_cntr = tail_cntr
            self.likes_catnip = likes_catnip

        @classmethod
        @escript
        def get_all_cats_with_two_tails(cat):
            
            my_query = cat.md.tail_cntr > 1 and cat.md.likes_catnip == False
            
            res = cat.resource.read(my_query)

            return res

    Cat(4, "boogie", "1", True).save()
    Cat(5, "gzoragh the great", "3", False).save()
    Cat(4, "Willie", "1", False).save()
    Cat(7, "Krzferf-13", "5", False).save()

    Cat.get_all_cats_with_two_tails()

@epure()
class Publication:
    text_style: str = "scientific"

@epure()
class Reporter:
    full_name: str = "Victor Bennet"

@epure() # (1)!
class Article:
    text_style: str = "scientific" # inherits
    reporter: Reporter # error appears
    title: str
    times_published: NotNull[int] = 3 # error appears
    authors: List[str] = ["Charles Dickens", "Frank Herbert"]

    def __init__(self, reporter, title):
        self.reporter = reporter
        self.title = title

    def get_articles_using_kwargs(self):

        articles = self.resource.read(times_published=5) # -> [<Article object at 0x0...>, <Article object at 0x2...>]

        return articles[0]
    
    @escript 
    def get_articles_docs_example(self):

        model = self.md 

        title_names = ["Why Epure is the best ORM?", "Why Elist is so powerfull?", "What is magic method?"] 

        query = False

        for name in title_names:
            query = query or model.title == name

        query = model.title in title_names 

        articles = self.resource.read(query) 

        return articles
    
    @escript
    def test_diff_cases(self):
        model = self.md 

        title_names = ["Why Epure is the best ORM?", "Why Elist is so powerfull?", "What is magic method?"] 

        query1 = model and True == True

        query2 = 9 == 9 or False

        for name in title_names:
            query2 = query2 or model.title == name

        query3 = False

        for name in title_names:
            query3 = 1 == 1 or False or query3 or model.title == name

        assert query3 == "True OR public.article.title = 'What is magic method?'"

        query9 = 14 == 14 or False or query3 or model.title == name

        assert query9 == "True OR True OR public.article.title = 'What is magic method?' OR public.article.title = 'What is magic method?'"

        query10 = 13 == 13 and False or query3 or model.title == name

        assert query10 == "False OR True OR public.article.title = 'What is magic method?' OR public.article.title = 'What is magic method?'"

        query11 = 11 == 11 and False and query3 or model.title == name

        assert query11 == "False AND True OR public.article.title = 'What is magic method?' OR public.article.title = 'What is magic method?'"

        query11 = 11 == 11 and False and query3 and model.title == name

        assert query11 == "False AND True OR public.article.title = 'What is magic method?' AND public.article.title = 'What is magic method?'"

        #should fail?
            
        query4 = model and 5

        query5 = model and model

        pass

def test_docs_for_in_example():
        
    my_reporter = Reporter()

    article_one = Article(my_reporter, "Why Epure is the best ORM?")
    # article_one = Article()
    article_one.save()

    article_two = Article(my_reporter, "Why Eset is so magnificent?")
    article_two.save()

    article_one.get_articles_docs_example()

    article_one.test_diff_cases()