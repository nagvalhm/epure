from ..epure.parser.leaf import DbProxy
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

    # query = x.f1 == y.f2 | x.f3 == x.f4 & 4 == x.f5 | (x.f6 == y.f7)
    # # query.debugger = debugger
    # str_query = str(query)
    # assert str_query == '(f1 == f2 or f3 == f4 and 4 == f5 or (f6 == f7))'

    # query = x.f1 == y.f2 | x.f3 == y.f4 & 5 == x.f5 | (x.f6 == y.f7)
    # # query.debugger = debugger
    # str_query = str(query)
    # assert str_query == '(f1 == f2 or f3 == f4 and 5 == f5 or (f6 == f7))'
    
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


# def test_select_queries():
#     db = DbProxy(real_db)
#     x = db['default_epure']
#     y = db['oraculs_domain.test_clssasdas']
#     # z = db['no_table']
#     z = db['oraculs_domain.oraculs']


#     query = db(x, y, x.str0 == y.test_field1 
#         | x.int0 == y.test_field2 & 5 == x.float0 
#         | (x.complex0 == y.test_field3))
#     assert str(query) == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n str0 = test_field1 or int0 = test_field2 and 5 = float0 or (complex0 = test_field3)'
                         
#     query = db(x, y, x.str0 == y.test_field1 | (x.int0 == y.test_field2 & 5 == x.float0) | x.complex0 == y.test_field3)
#     assert str(query) == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n (str0 = test_field1 or (int0 = test_field2 and 5 = float0) or complex0 = test_field3)'
    
#     query = db(x.str0, x.int0, y.test_field2, y, (x.str0 == y.test_field1) | x.int0 == y.test_field2 & 5 == x.float0 | x.complex0 == y.test_field3)
#     assert str(query) == 'SELECT str0, int0, test_field2, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n ((str0 = test_field1) or int0 = test_field2 and 5 = float0 or complex0 = test_field3)'

#     query = db(x, y, x.str0 == y.test_field1 | x.int0 == y.test_field2)
#     assert str(query) == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n (str0 = test_field1 or int0 = test_field2)'

#     query = db(x, y, (x.str0 == y.test_field1 | x.int0 == y.test_field2) & 5 == x.float0 | x.complex0 == y.test_field3)
#     assert str(query) == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n ((str0 = test_field1 or int0 = test_field2) and 5 = float0 or complex0 = test_field3)'

#     query = db(x, y, (x.str0 == y.test_field1 | (x.int0 == y.test_field2 & 5 == x.float0)) | x.complex0 == y.test_field3)
#     assert str(query) == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n (str0 = test_field1 or (int0 = test_field2 and 5 = float0) or complex0 = test_field3)'
 
#     query = db(x, y, (x.str0 == y.test_field1) | (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3))
#     assert str(query) == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n (((str0 = test_field1) or ((int0 = test_field2) and (float0 = 5))) or (complex0 = test_field3))'
    
    #wrong serialize
    # query = db(x, y, (x.int0 == y.test_field2) ^ y << (x.str0 == y.test_field1) & (5 == x.float0) | (x.complex0 == y.test_field3))
    # assert str(query) == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1\n WHERE \n (((int0 = test_field2)   and (float0 = 5)) or (complex0 = test_field3))'


    # query = db(x, y, y << x.str0 == y.test_field1 | (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3))
    # assert str(query) == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0\n WHERE \n oraculs_domain.test_clssasdas << str0 = test_field1 or ((int0 = test_field2) and (float0 = 5)) or (complex0 = test_field3)'

    # query =  db(x, y, (x.int0 == y.test_field2) & y << (x.str0 == y.test_field1 & (5 == x.float0)) | (x.complex0 == y.test_field3))
    # assert str(query) == '(int0 = test_field2) AND oraculs_domain.test_clssasdas << str0 = test_field1 AND (float0 = 5) OR (complex0 = test_field3)'
    
    
    # query = db(x, y, (y << (x.str0 == y.test_field1 | x.int0 == y.test_field2 \
    # & x.float0 ==  5 | x.complex0 == y.test_field3))\
    #     & x.complex0 == 'vse' \
    #     | y << (x.str0 == y.test_field3)\
    #     & (x.list0 > 100500 | x.tuple0 < False) \
    #     & x.str0 < y.test_field3\
    #     & x.no_field == 4\
    #     & x >> z)

    # assert(query) == ''