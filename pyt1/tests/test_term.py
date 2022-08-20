from ..epure.parser.leaf import DbProxy
from ..epure.parser.term_parser import TermParser
from .epure_classes import db as real_db
import networkx as nx
import matplotlib.pyplot as plt
from ..epure.parser.term_debugger import MatplotTermDebugger


# def test_show_graph():
#     G = nx.Graph()
#     G.add_edges_from([('hello' ,'but') , (2 ,3) , (1 ,3) , (1 ,4), (1, 5) ])
#     # pos = { 1: (20, 30), 2: (40, 30), 3: (30, 10),4: (0, 40)} 

#     # nx.draw_networkx(G, pos=pos)
#     nx.draw_networkx(G)
#     plt.show()

def test_simple_queries():
    db = DbProxy(real_db)
    x = db['oraculs_domain.competitions']
    y = db['oraculs_domain.oraculs']

    debugger = MatplotTermDebugger()

    query = x.f1 == y.f2 | x.f3 == x.f4 & 4 == x.f5 | (x.f6 == y.f7)
    # query.debugger = debugger
    str_query = str(query)
    assert str_query == '(f1 == f2 or f3 == f4 and 4 == f5 or (f6 == f7))'

    query = x.f1 == y.f2 | x.f3 == y.f4 & 5 == x.f5 | (x.f6 == y.f7)
    # query.debugger = debugger
    str_query = str(query)
    assert str_query == '(f1 == f2 or f3 == f4 and 5 == f5 or (f6 == f7))'
    
    query = x.f1 == y.f2 ^ y << x.f3 == y.f4 & 5 == x.f5 | x.f6 == y.f7
    # query.debugger = debugger
    str_query = str(query)
    assert str_query == '(f1 == f2 ^ oraculs_domain.oraculs << (f3 == f4) and 5 == f5 or f6 == f7)'

    query = x.f1 == y.f2 ^ y << (x.f3 == y.f4) & 5 == x.f5 | x.f6 == y.f7
    # query.debugger = debugger
    str_query = str(query)
    assert str_query == '(f1 == f2 ^ oraculs_domain.oraculs << (f3 == f4) and 5 == f5 or f6 == f7)'

    query = x.f1 == y.f2 ^ y << (x.f3 == y.f4 & 5 == x.f5) | x.f6 == y.f7
    # query.debugger = debugger
    str_query = str(query)
    assert str_query == '(f1 == f2 ^ oraculs_domain.oraculs << (f3 == f4 and 5 == f5) or f6 == f7)'

    query = x.f1 == y.f2 & y << x.f3 == y.f4 ^ 5 == x.f5 | x.f6 == y.f7
    # query.debugger = debugger
    str_query = str(query)
    assert str_query == '(f1 == f2 and oraculs_domain.oraculs << (f3 == f4) ^ 5 == f5 or f6 == f7)'

    query = y << x.f3 == y.f4 ^ x.f1 == y.f2 & 5 == x.f5 | x.f6 == y.f7
    # query.debugger = debugger
    str_query = str(query)
    assert str_query == '(oraculs_domain.oraculs << (f3 == f4) ^ f1 == f2 and 5 == f5 or f6 == f7)'

    query = x.f1 == y.f2 & 5 == x.f5 | x.f6 == y.f7 ^ y << x.f3 == y.f4
    # query.debugger = debugger
    str_query = str(query)
    assert str_query == '(f1 == f2 and 5 == f5 or f6 == f7 ^ oraculs_domain.oraculs << (f3 == f4))'

    query = x.str0 == y.test_field1 | (x.int0 == y.test_field2 & 5 == x.float0) | x.complex0 == y.test_field3
    # query.debugger = debugger
    str_query = str(query)
    assert str_query == '(str0 == test_field1 or (int0 == test_field2 and 5 == float0) or complex0 == test_field3)'
    
    query = (x.str0 == y.test_field1) | x.int0 == y.test_field2 & 5 == x.float0 | x.complex0 == y.test_field3
    str_query = str(query)
    assert str_query == '((str0 == test_field1) or int0 == test_field2 and 5 == float0 or complex0 == test_field3)'

    query = (x.str0 == y.test_field1 | x.int0 == y.test_field2)
    str_query = str(query)
    assert str_query == '(str0 == test_field1 or int0 == test_field2)'

    query = (x.str0 == y.test_field1 | x.int0 == y.test_field2) & 5 == x.float0 | x.complex0 == y.test_field3
    str_query = str(query)
    assert str_query == '((str0 == test_field1 or int0 == test_field2) and 5 == float0 or complex0 == test_field3)'

    query = (x.str0 == y.test_field1 | (x.int0 == y.test_field2 & 5 == x.float0)) | x.complex0 == y.test_field3
    str_query = str(query)
    assert str_query == '((str0 == test_field1 or (int0 == test_field2 and 5 == float0)) or complex0 == test_field3)'
 
    query = (x.str0 == y.test_field1) | (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3)
    str_query = str(query)
    assert str_query == '(((str0 == test_field1) or ((int0 == test_field2) and (float0 == 5))) or (complex0 == test_field3))'


def test_join_queries():
    db = DbProxy(real_db)
    x = db['default_epure']
    y = db['oraculs_domain.test_clssasdas']


    query = y << (x.str0 == y.test_field1) | (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3)
    str_query = str(query)
    assert str_query == '(oraculs_domain.test_clssasdas << (str0 == test_field1) or ((int0 == test_field2) and (float0 == 5)) or (complex0 == test_field3))'
                        
    query = y << x.str0 == y.test_field1 | (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3)
    str_query = str(query)
    assert str_query == '(oraculs_domain.test_clssasdas << (str0 == test_field1) or ((int0 == test_field2) and (float0 == 5)) or (complex0 == test_field3))'

    query =  (x.int0 == y.test_field2) & y << x.str0 == y.test_field1 & (5 == x.float0) | (x.complex0 == y.test_field3)
    str_query = str(query)
    assert str_query == '((int0 == test_field2) and oraculs_domain.test_clssasdas << (str0 == test_field1) and (float0 == 5) or (complex0 == test_field3))'


def test_term_parser():
    db = DbProxy(real_db)
    x = db['default_epure']
    real_x = real_db['default_epure']
    y = db['oraculs_domain.test_clssasdas']
    # z = db['no_table']
    z = db['oraculs_domain.oraculs']
    parser = TermParser(real_x)


    # term = (x.str0 == y.test_field1 
    #     | x.int0 == y.test_field2 & 5 == x.float0 
    #     | (x.complex0 == y.test_field3))
    # query = parser.parse([x, y], term)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n str0 = test_field1 or (int0 = test_field2 and 5 = float0) or complex0 = test_field3'
                         
    # query = parser.parse([x, y], x.str0 == y.test_field1 | (x.int0 == y.test_field2 & 5 == x.float0) | x.complex0 == y.test_field3)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n (str0 = test_field1 or (int0 = test_field2 and 5 = float0) or complex0 = test_field3)'
    
    # query = parser.parse([x.str0, x.int0, y.test_field2, y], (x.str0 == y.test_field1) | x.int0 == y.test_field2 & 5 == x.float0 | x.complex0 == y.test_field3)
    # assert query == 'SELECT str0, int0, test_field2, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n ((str0 = test_field1) or int0 = test_field2 and 5 = float0 or complex0 = test_field3)'

    # query = parser.parse([x, y], x.str0 == y.test_field1 | x.int0 == y.test_field2)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n (str0 = test_field1 or int0 = test_field2)'

    # query = parser.parse([x, y], (x.str0 == y.test_field1 | x.int0 == y.test_field2) & 5 == x.float0 | x.complex0 == y.test_field3)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n ((str0 = test_field1 or int0 = test_field2) and 5 = float0 or complex0 = test_field3)'

    # query = parser.parse([x, y], (x.str0 == y.test_field1 | (x.int0 == y.test_field2 & 5 == x.float0)) | x.complex0 == y.test_field3)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n ((str0 = test_field1 or (int0 = test_field2 and 5 = float0)) or complex0 = test_field3)'
    
    # term = (x.str0 == y.test_field1) | (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3)
    # term_str = str(term)
    # assert term_str == '(((str0 == test_field1) or ((int0 == test_field2) and (float0 == 5))) or (complex0 == test_field3))'
    # query = parser.parse([x, y], term_str)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n (((str0 = test_field1) or ((int0 = test_field2) and (float0 = 5))) or (complex0 = test_field3))'
    
    
    term = (x.int0 == y.test_field2) ^ y << (x.str0 == y.test_field1) & (5 == x.float0) | (x.complex0 == y.test_field3)
    term_str = str(term)
    assert term_str == '(((int0 == test_field2) ^ oraculs_domain.test_clssasdas << (str0 == test_field1) and (float0 == 5)) or (complex0 == test_field3))'
    query = parser.parse([x, y], term_str)
    assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1\n WHERE \n (int0 = test_field2)   and float0 = 5 or complex0 = test_field3'

    term = y << x.str0 == y.test_field1 ^ (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3)
    term_str = str(term)
    assert term_str == '(oraculs_domain.test_clssasdas << (str0 == test_field1) ^ ((int0 == test_field2) and (float0 == 5)) or (complex0 == test_field3))'
    query = parser.parse([x, y], term_str)
    assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1\n WHERE \n   (int0 = test_field2 and float0 = 5) or complex0 = test_field3'


    term = (x.int0 == y.test_field2) ^ y << (x.str0 == y.test_field1 & (x.float0 == 5 | x.int0 == 4)) | (x.complex0 == y.test_field3)
    term_str = str(term)
    assert term_str == '((int0 == test_field2) ^ oraculs_domain.test_clssasdas << (str0 == test_field1 and (float0 == 5 or int0 == 4)) or (complex0 == test_field3))'
    query =  parser.parse([x, y], term_str)
    assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 and (float0 = 5 or int0 = 4)\n WHERE \n (int0 = test_field2)   or complex0 = test_field3'
    
    # wrong serialize
    term = (x.int0 == y.test_field2) & y << (x.str0 == y.test_field1 & (5 == x.float0)) ^ (x.complex0 == y.test_field3)
    term_str = str(term)
    assert term_str == '((int0 == test_field2) and oraculs_domain.test_clssasdas << (str0 == test_field1 and (float0 == 5)) ^ (complex0 == test_field3))'
    query =  parser.parse([x, y], term_str)
    assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 and float0 = 5\n WHERE \n int0 = test_field2 and   (complex0 = test_field3)'

    term = (x.int0 == y.test_field2) &  (x.complex0 == y.test_field3) ^ y << (x.str0 == y.test_field1 & (5 == x.float0))
    term_str = str(term)
    assert term_str == '((int0 == test_field2) and (complex0 == test_field3)) ^ oraculs_domain.test_clssasdas << (str0 == test_field1 and (float0 == 5))'
    query =  parser.parse([x, y], term_str)
    assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 and float0 = 5\n WHERE \n (int0 = test_field2 and complex0 = test_field3)  '
    

    term = (y << (x.str0 == y.test_field1 | x.int0 == y.test_field2\
    & x.float0 ==  5 | x.complex0 == y.test_field3)) ^\
        z >> y.test_field1 == z.test_field\
        & x.complex0 == 'vse'\
        | y << (x.int3 == y.test_field3)\
        ^ (x.list0 > 100500 | x.tuple0 < False)\
        & x.float3 < y.test_field3\
        & x.complex3 == 4\
        & x >> z
    term_str = str(term)
    assert term_str == "(oraculs_domain.test_clssasdas << (str0 == test_field1 or int0 == test_field2 and float0 == 5 or complex0 == test_field3) ^ oraculs_domain.oraculs >> (test_field1 == test_field) and complex0 == 'vse' or oraculs_domain.test_clssasdas << (int3 == test_field3) ^ (list0 > 100500 or tuple0 < False) and float3 < test_field3 and complex3 == 4 and public.default_epure >> oraculs_domain.oraculs)"
    query = parser.parse([x.complex0, y.test_field3], term)

    assert(query) == ''