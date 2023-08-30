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

    query = x.f1 == y.f2 | x.f3 == y.f4 & 5 == x.f5 | (x.f6 == y.f7)
    # query.debugger = debugger
    str_query = query.str(True)
    assert str_query == '(f1 == f2 or f3 == f4 and 5 == f5 or (f6 == f7))'

    # query = y.test_field1 @ x.f1 == x.f2 | x.f4 == x.f3 % 3 & 5 == x.f5 | (x.f6 == x.f7) | x.f1 >= (x.f4,x.f2)
    # # a @ a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= ((a.f4,a.f2)@(x.str0 == y.test_field1))
    # # query.debugger = debugger
    # str_query = query.str(True)
    # assert str_query == '(f1 == f2 or f3 == f4 and 5 == f5 or (f6 == f7))'

    # query = [x.str5] @ ((x.str3 == y.test_field2))
    # str_query = query.str(True,True)
    # assert str_query == ""

    query = [x.str5, x.int4, y.test_field3, y] @ (x.str3 == y.test_field2) | x.int0 == y.test_field2 & 5 == x.float0 | x.complex0 == y.test_field3 | x.f1 >= ((x.f4, y.f2) @ (x.str1 == y.test_field1)) | x.f1 >= ('val3', 'val4')
    # query = [x.str0, x.int0, y.test_field2, y] @ (x.str0 == y.test_field1) | x.int0 == y.test_field2 & 5 == x.float0 | x.complex0 == y.test_field3 | x.f1 >= ((x.f4, y.f2) @ (x.str0 == y.test_field1))
    # query.debugger = debugger
    # query.debugger.each_step = True
    str_query = query.str(True, True)
    assert str_query == "[oraculs_domain.competitions.str5, oraculs_domain.competitions.int4, oraculs_domain.oraculs.test_field3, oraculs_domain.oraculs] @ (oraculs_domain.competitions.str3 == oraculs_domain.oraculs.test_field2) or oraculs_domain.competitions.int0 == oraculs_domain.oraculs.test_field2 and 5 == oraculs_domain.competitions.float0 or oraculs_domain.competitions.complex0 == oraculs_domain.oraculs.test_field3 or oraculs_domain.competitions.f1 >= [oraculs_domain.competitions.f4, oraculs_domain.oraculs.f2] @ (oraculs_domain.competitions.str1 == oraculs_domain.oraculs.test_field1) or oraculs_domain.competitions.f1 >= ['val3', 'val4']"


    query = [x.str0, x.int0, y.test_field2, y] @ (x.str0 == y.test_field1) | x.int0 == y.test_field2 & 5 == x.float0 | x.complex0 == y.test_field3 | x.f1 >= ((x.f4,y.f2)@(x.str0 == y.test_field1))
    str_query = query.str(True, True)
    assert str_query == '[oraculs_domain.competitions.str0, oraculs_domain.competitions.int0, oraculs_domain.oraculs.test_field2, oraculs_domain.oraculs] @ (oraculs_domain.competitions.str0 == oraculs_domain.oraculs.test_field1) or oraculs_domain.competitions.int0 == oraculs_domain.oraculs.test_field2 and 5 == oraculs_domain.competitions.float0 or oraculs_domain.competitions.complex0 == oraculs_domain.oraculs.test_field3 or oraculs_domain.competitions.f1 >= [oraculs_domain.competitions.f4, oraculs_domain.oraculs.f2] @ (oraculs_domain.competitions.str0 == oraculs_domain.oraculs.test_field1)'


    query = x.f1 == y.f2 | x.f3 % '%test_like%' & 5 == x.f5 | (x.f6 == y.f7)
    # query.debugger = debugger
    str_query = query.str(True)
    assert str_query == "(f1 == f2 or f3 % '%test_like%' and 5 == f5 or (f6 == f7))"

    # query = ('val1', 'val2') in x.f8
    # query = x.f8 % '%krysa%'
    # query = x.f8 >= ('val1', 'val2')
    # query = x.f8 >> ('val1', 'val2')
    query = x.f8 >= ('val1', 'val2') | x.f1 == y.f2 | x.f9 > ('val3', 'val4') | x.f3 == x.f4 & 4 == x.f5 | (x.f6 == y.f7)
    # query.debugger = debugger
    # query.debugger.each_step = True
    str_query = query.str(True)
    assert str_query == "(f8 >= ['val1', 'val2'] or f1 == f2 or f9 > ['val3', 'val4'] or f3 == f4 and 4 == f5 or (f6 == f7))"

    query = x.f8 >= ['val1', 'val2'] | x.f1 == y.f2 | x.f9 > ('val3', 'val4') | x.f3 == x.f4 & 4 == x.f5 | (x.f6 == y.f7)
    # query.debugger = debugger
    # query.debugger.each_step = True
    str_query = query.str(True)
    assert str_query == "(f8 >= ['val1', 'val2'] or f1 == f2 or f9 > ['val3', 'val4'] or f3 == f4 and 4 == f5 or (f6 == f7))"

    # query = x.f8 in (y.f2, y.f7) | x.f1 == y.f2 | x.f3 == x.f4 & 4 == x.f5 | (x.f6 == y.f7)
    # # query.debugger = debugger
    # str_query = query.str(True)
    # assert str_query == '(f8 in (f2, f7) or f1 == f2 or f3 == f4 and 4 == f5 or (f6 == f7))'
    
    # old precise tests 

    query = x.f1 == y.f2 | x.f3 == x.f4 & 4 == x.f5 | (x.f6 == y.f7)
    # query.debugger = debugger
    # query.debugger.each_step = True
    str_query = query.str(True)
    assert str_query == '(f1 == f2 or f3 == f4 and 4 == f5 or (f6 == f7))'

    query = x.f1 == y.f2 | x.f3 == y.f4 & 5 == x.f5 | (x.f6 == y.f7)
    # query.debugger = debugger
    str_query = query.str(True)
    assert str_query == '(f1 == f2 or f3 == f4 and 5 == f5 or (f6 == f7))'
    
    query = x.f1 == y.f2 ^ y << x.f3 == y.f4 & 5 == x.f5 | x.f6 == y.f7
    # query.debugger = debugger
    str_query = query.str(True)
    assert str_query == '(f1 == f2 ^ oraculs_domain.oraculs << (f3 == f4) and 5 == f5 or f6 == f7)'

    query = x.f1 == y.f2 ^ y << (x.f3 == y.f4) & 5 == x.f5 | x.f6 == y.f7
    # query.debugger = debugger
    str_query = query.str(True)
    assert str_query == '(f1 == f2 ^ oraculs_domain.oraculs << (f3 == f4) and 5 == f5 or f6 == f7)'

    query = x.f1 == y.f2 ^ y << (x.f3 == y.f4 & 5 == x.f5) | x.f6 == y.f7
    # query.debugger = debugger
    str_query = query.str(True)
    assert str_query == '(f1 == f2 ^ oraculs_domain.oraculs << (f3 == f4 and 5 == f5) or f6 == f7)'

    query = x.f1 == y.f2 & y << x.f3 == y.f4 ^ 5 == x.f5 | x.f6 == y.f7
    # query.debugger = debugger
    str_query = query.str(True)
    assert str_query == '(f1 == f2 and oraculs_domain.oraculs << (f3 == f4) ^ 5 == f5 or f6 == f7)'

    query = y << x.f3 == y.f4 ^ x.f1 == y.f2 & 5 == x.f5 | x.f6 == y.f7
    # query.debugger = debugger
    str_query = query.str(True)
    assert str_query == '(oraculs_domain.oraculs << (f3 == f4) ^ f1 == f2 and 5 == f5 or f6 == f7)'

    query = x.f1 == y.f2 & 5 == x.f5 | x.f6 == y.f7 ^ y << x.f3 == y.f4
    # query.debugger = debugger
    str_query = query.str(True)
    assert str_query == '(f1 == f2 and 5 == f5 or f6 == f7 ^ oraculs_domain.oraculs << (f3 == f4))'

    query = x.str0 == y.test_field1 | (x.int0 == y.test_field2 & 5 == x.float0) | x.complex0 == y.test_field3
    # query.debugger = debugger
    str_query = query.str(True)
    assert str_query == '(str0 == test_field1 or (int0 == test_field2 and 5 == float0) or complex0 == test_field3)'
    
    query = (x.str0 == y.test_field1) | x.int0 == y.test_field2 & 5 == x.float0 | x.complex0 == y.test_field3
    str_query = query.str(True)
    assert str_query == '((str0 == test_field1) or int0 == test_field2 and 5 == float0 or complex0 == test_field3)'

    query = (x.str0 == y.test_field1 | x.int0 == y.test_field2)
    str_query = query.str(True)
    assert str_query == '(str0 == test_field1 or int0 == test_field2)'

    query = (x.str0 == y.test_field1 | x.int0 == y.test_field2) & 5 == x.float0 | x.complex0 == y.test_field3
    str_query = query.str(True)
    assert str_query == '((str0 == test_field1 or int0 == test_field2) and 5 == float0 or complex0 == test_field3)'

    query = (x.str0 == y.test_field1 | (x.int0 == y.test_field2 & 5 == x.float0)) | x.complex0 == y.test_field3
    str_query = query.str(True)
    assert str_query == '((str0 == test_field1 or (int0 == test_field2 and 5 == float0)) or complex0 == test_field3)'
    
    query = (x.str0 == y.test_field1) | (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3)
    str_query = query.str(True)
    assert str_query == '(((str0 == test_field1) or ((int0 == test_field2) and (float0 == 5))) or (complex0 == test_field3))'

    #old test end

    query = (x.str0 == y.test_field1) | (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3)
    str_query = query.str(True, True)
    assert str_query == '(((oraculs_domain.competitions.str0 == oraculs_domain.oraculs.test_field1) or ((oraculs_domain.competitions.int0 == oraculs_domain.oraculs.test_field2) and (oraculs_domain.competitions.float0 == 5))) or (oraculs_domain.competitions.complex0 == oraculs_domain.oraculs.test_field3))'

    query = [x.str0, x.int0, y.test_field2, y] @ (x.str0 == y.test_field1) | x.int0 == y.test_field2 & 5 == x.float0 | x.complex0 == y.test_field3
    # query.debugger = debugger
    # query.debugger.each_step = True
    str_query = query.str(True)
    assert str_query == "[str0, int0, test_field2, oraculs_domain.oraculs] @ (str0 == test_field1) or int0 == test_field2 and 5 == float0 or complex0 == test_field3"

    query = [x.str0, x.int0, y.test_field2, y] @ (x.str0 == y.test_field1) | x.int0 == y.test_field2 & 5 == x.float0 | x.complex0 == y.test_field3
    # query.debugger = debugger
    # query.debugger.each_step = True
    str_query = query.str(True, True)
    assert str_query == "[oraculs_domain.competitions.str0, oraculs_domain.competitions.int0, oraculs_domain.oraculs.test_field2, oraculs_domain.oraculs] @ (oraculs_domain.competitions.str0 == oraculs_domain.oraculs.test_field1) or oraculs_domain.competitions.int0 == oraculs_domain.oraculs.test_field2 and 5 == oraculs_domain.competitions.float0 or oraculs_domain.competitions.complex0 == oraculs_domain.oraculs.test_field3"

    # query = [a.f1, z.f2] @ a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= ((a.f4,a.f2)@(x.str0 == y.test_field1))
    

def test_join_queries():
    db = DbProxy(real_db)
    x = db['default_epure']
    y = db['oraculs_domain.test_clssasdas']


    query = y << (x.str0 == y.test_field1) | (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3)
    str_query = query.str(True)
    assert str_query == '(oraculs_domain.test_clssasdas << (str0 == test_field1) or ((int0 == test_field2) and (float0 == 5)) or (complex0 == test_field3))'
                        
    query = y << x.str0 == y.test_field1 | (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3)
    str_query = query.str(True)
    assert str_query == '(oraculs_domain.test_clssasdas << (str0 == test_field1) or ((int0 == test_field2) and (float0 == 5)) or (complex0 == test_field3))'

    query =  (x.int0 == y.test_field2) & y << x.str0 == y.test_field1 & (5 == x.float0) | (x.complex0 == y.test_field3)
    str_query = query.str(True)
    assert str_query == '((int0 == test_field2) and oraculs_domain.test_clssasdas << (str0 == test_field1) and (float0 == 5) or (complex0 == test_field3))'


def test_term_parser():
    db = DbProxy(real_db)
    x = db['default_epure']
    real_x = real_db['default_epure']
    y = db['oraculs_domain.test_clssasdas']
    # z = db['no_table']
    z = db['oraculs_domain.oraculs']
    a = db['oraculs_domain.competitions']
    b = db['oraculs_domain.tasks']
    parser = TermParser(real_x)

    term = a.f1 == z.f2 | a.f3 % '%test_like%' & 5 == a.f5 | (a.f6 == z.f7)
    query = parser.parse([a.f1, z.f2], term, False)
    # assert query == "SELECT f1, f2 FROM oraculs_domain.competitions \n  WHERE \n f1 = f2 or (f3 like '%test_like%' and 5 = f5) or f6 = f7"
    assert "WHERE \n f1 = f2 or (f3 like '%test_like%' and 5 = f5) or f6 = f7" in query

    term = a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7)
    query = parser.parse([a.f1, z.f2], term, False)

    assert "WHERE \n f1 = f2 or (f4 = f3 % 3 and 5 = f5) or f6 = f7" in query
    
    #old tests
    
    term = (x.str0 == y.test_field1 
        | x.int0 == y.test_field2 & 5 == x.float0 
        | (x.complex0 == y.test_field3))
    query = parser.parse([x.str0, y.test_field1], term, True)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n str0 = test_field1 or (int0 = test_field2 and 5 = float0) or complex0 = test_field3'
    assert 'WHERE \n public.default_epure.str0 = oraculs_domain.test_clssasdas.test_field1 or (public.default_epure.int0 = oraculs_domain.test_clssasdas.test_field2 and 5 = public.default_epure.float0) or public.default_epure.complex0 = oraculs_domain.test_clssasdas.test_field3' in query

    query = parser.parse([x, y], x.str0 == y.test_field1 | (x.int0 == y.test_field2 & 5 == x.float0) | x.complex0 == y.test_field3, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n str0 = test_field1 or (int0 = test_field2 and 5 = float0) or complex0 = test_field3'
    assert 'WHERE \n str0 = test_field1 or (int0 = test_field2 and 5 = float0) or complex0 = test_field3' in query

    term = (x.str0 == y.test_field1) | x.int0 == y.test_field2 & 5 == x.float0 | x.complex0 == y.test_field3
    header = [x.str0, x.int0, y.test_field2, y]
    query = parser.parse(header, term, False)
    # assert query == 'SELECT str0, int0, test_field2, oraculs_domain.test_clssasdas.*, node_id FROM public.default_epure \n  WHERE \n str0 = test_field1 or (int0 = test_field2 and 5 = float0) or complex0 = test_field3'
    assert 'WHERE \n str0 = test_field1 or (int0 = test_field2 and 5 = float0) or complex0 = test_field3' in query
    
    #old test end

    term = a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= (a.f4, a.f2)
    # term = a.f1 >= a.f2 | a.f3 % 3
    header = [a.f1, z.f2]
    query = parser.parse(header, term, False)
    assert "WHERE \n f1 = f2 or (f4 = f3 % 3 and 5 = f5) or f6 = f7 or f1 in (f4, f2)" in query

    term = a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= ('f4', 'f2', 4)
    # term = a.f1 >= a.f2 | a.f3 % 3
    header = [a.f1, z.f2]
    query = parser.parse(header, term, False)
    assert "WHERE \n f1 = f2 or (f4 = f3 % 3 and 5 = f5) or f6 = f7 or f1 in ('f4', 'f2', 4)" in query

    term = y.test_field1 @ a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= (a.f4,a.f2)
    # term = a.f1 >= a.f2 | a.f3 % 3
    query = parser.parse(term, True)
    # query = parser.parse(header, term, False)
    assert "WHERE \n oraculs_domain.competitions.f1 = oraculs_domain.oraculs.f2 or (oraculs_domain.competitions.f4 = oraculs_domain.competitions.f3 % 3 and 5 = oraculs_domain.competitions.f5) or oraculs_domain.competitions.f6 = oraculs_domain.oraculs.f7 or oraculs_domain.competitions.f1 in (oraculs_domain.competitions.f4, oraculs_domain.competitions.f2)" in query

    term = (a, z) @ a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= (a.f4,a.f2)
    # term = a.f1 >= a.f2 | a.f3 % 3
    query = parser.parse(term, True)
    # query = parser.parse(header, term, False)
    assert "WHERE \n oraculs_domain.competitions.f1 = oraculs_domain.oraculs.f2 or (oraculs_domain.competitions.f4 = oraculs_domain.competitions.f3 % 3 and 5 = oraculs_domain.competitions.f5) or oraculs_domain.competitions.f6 = oraculs_domain.oraculs.f7 or oraculs_domain.competitions.f1 in (oraculs_domain.competitions.f4, oraculs_domain.competitions.f2)" in query

    term = [a.f1, z.f2] @ a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= ((a.f4,a.f2)@(x.str0 == y.test_field1 | a.f6 == z.f7))
    # term = a.f1 >= a.f2 | a.f3 % 3
    # header = [a.f1, z.f2]
    query = parser.parse(term, True)
    # query = parser.parse(header, term, False)
    assert "WHERE \n oraculs_domain.competitions.f1 = oraculs_domain.oraculs.f2 or (oraculs_domain.competitions.f4 = oraculs_domain.competitions.f3 % 3 and 5 = oraculs_domain.competitions.f5) or oraculs_domain.competitions.f6 = oraculs_domain.oraculs.f7 or oraculs_domain.competitions.f1 in (oraculs_domain.competitions.f4, oraculs_domain.competitions.f2) @ (public.default_epure.str0 = oraculs_domain.test_clssasdas.test_field1 or oraculs_domain.competitions.f6 = oraculs_domain.oraculs.f7)" in query
    
    term = a @ a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= ((a.f4,a.f2)@(x.str0 == y.test_field1))
    # term = a.f1 >= a.f2 | a.f3 % 3    
    query = parser.parse(term, True)
    # query = parser.parse(header, term, False)
    assert "WHERE \n oraculs_domain.competitions.f1 = oraculs_domain.oraculs.f2 or (oraculs_domain.competitions.f4 = oraculs_domain.competitions.f3 % 3 and 5 = oraculs_domain.competitions.f5) or oraculs_domain.competitions.f6 = oraculs_domain.oraculs.f7 or oraculs_domain.competitions.f1 in (oraculs_domain.competitions.f4, oraculs_domain.competitions.f2) @ (public.default_epure.str0 = oraculs_domain.test_clssasdas.test_field1)" in query
    
    term = a.f1 @ a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= ((a.f4,a.f2)@(x.str0 == y.test_field1))
    # term = a.f1 >= a.f2 | a.f3 % 3    
    query = parser.parse(term, True)
    # query = parser.parse(header, term, False)
    assert "WHERE \n oraculs_domain.competitions.f1 = oraculs_domain.oraculs.f2 or (oraculs_domain.competitions.f4 = oraculs_domain.competitions.f3 % 3 and 5 = oraculs_domain.competitions.f5) or oraculs_domain.competitions.f6 = oraculs_domain.oraculs.f7 or oraculs_domain.competitions.f1 in (oraculs_domain.competitions.f4, oraculs_domain.competitions.f2) @ (public.default_epure.str0 = oraculs_domain.test_clssasdas.test_field1)" in query

    term = (a.f1, z.f2, z) @ a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= ((a.f4,a.f2)@(x.str0 == y.test_field1))
    # term = a.f1 >= a.f2 | a.f3 % 3
    query = parser.parse(term, True)
    # query = parser.parse(header, term, False)
    assert "WHERE \n oraculs_domain.competitions.f1 = oraculs_domain.oraculs.f2 or (oraculs_domain.competitions.f4 = oraculs_domain.competitions.f3 % 3 and 5 = oraculs_domain.competitions.f5) or oraculs_domain.competitions.f6 = oraculs_domain.oraculs.f7 or oraculs_domain.competitions.f1 in (oraculs_domain.competitions.f4, oraculs_domain.competitions.f2) @ (public.default_epure.str0 = oraculs_domain.test_clssasdas.test_field1)" in query

    term = (a.f1, z.f2, z) @ a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= ((a.f4,a.f2)@(a.f2 >= ((a.f4,a.f2)@(x.str0 == y.test_field1))))
    # term = a.f1 >= a.f2 | a.f3 % 3
    query = parser.parse(term, True)
    # query = parser.parse(header, term, False)
    assert "WHERE \n oraculs_domain.competitions.f1 = oraculs_domain.oraculs.f2 or (oraculs_domain.competitions.f4 = oraculs_domain.competitions.f3 % 3 and 5 = oraculs_domain.competitions.f5) or oraculs_domain.competitions.f6 = oraculs_domain.oraculs.f7 or oraculs_domain.competitions.f1 in (oraculs_domain.competitions.f4, oraculs_domain.competitions.f2) @ oraculs_domain.competitions.f2 in (oraculs_domain.competitions.f4, oraculs_domain.competitions.f2) @ (public.default_epure.str0 = oraculs_domain.test_clssasdas.test_field1)" in query

    # term = (a.f1, z.f2, z) @ a.f1 > z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= ((a.f4,a.f2)@(a.f2 >= ((a.f4,a.f2)@(x.str0 == y.test_field1))))
    # # term = a.f1 >= a.f2 | a.f3 % 3
    # query = parser.parse(term, True)
    # # query = parser.parse(header, term, False)
    # assert "WHERE \n oraculs_domain.competitions.f1 = oraculs_domain.oraculs.f2 or (oraculs_domain.competitions.f4 = oraculs_domain.competitions.f3 % 3 and 5 = oraculs_domain.competitions.f5) or oraculs_domain.competitions.f6 = oraculs_domain.oraculs.f7 or oraculs_domain.competitions.f1 in (oraculs_domain.competitions.f4, oraculs_domain.competitions.f2) @ oraculs_domain.competitions.f2 in (oraculs_domain.competitions.f4, oraculs_domain.competitions.f2) @ (public.default_epure.str0 = oraculs_domain.test_clssasdas.test_field1)" in query

    # term = [x.str0, x.int0, y.test_field2, y] @ (x.str0 == y.test_field1) | x.int0 == y.test_field2 & 5 == x.float0 | x.complex0 == y.test_field3
    # # header = [x.str0, x.int0, y.test_field2, y]
    # query = term.str(True)

    # term =  [b.f1, b.f2, b.f3, b.f4,
    #             b.f5, b.f6] \
    #         ^ b.f7 == 'v1' \
    #         & b.f8 == 'v2' ^ \
    #         z << (b.f9 == z.f10 
    #                         & b.f11 == z.f12 
    #                         & b.f13 == z.f14) \
    #         ^[a.f15] \
    #         ^ a << z.f16 == a.f17

    # query = parser.parse(term, False)

    # assert query == ""

    # query = parser.parse([z.f1, z.f2], term)

    # assert query == ""

    # term =  [b.f1, b.f2, b.f3, b.f4,
    #             b.f5, b.f6] \
    #         ^ b.f7 == 'v1' \
    #         & b.f8 == 'v2' ^ \
    #         z[z.f2, z.f3, z.f4]^ \
    #         z << (b.f9 == z.f10 
    #                         & b.f11 == z.f12 
    #                         & b.f13 == z.f14) \
    #         ^[a.f15] \
    #         ^ a << z.f16 == a.f17
    

    # query = parser.parse(term, False)

    # assert query == ""

    # query = parser.parse([z.f1, z.f2], term)

    # assert query == ""

    # query = parser.parse([x, y], x.str0 == y.test_field1 | x.int0 == y.test_field2, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n str0 = test_field1 or int0 = test_field2'

    # query = parser.parse([x, y], (x.str0 == y.test_field1 | x.int0 == y.test_field2) & 5 == x.float0 | x.complex0 == y.test_field3, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n (str0 = test_field1 or int0 = test_field2) and 5 = float0 or complex0 = test_field3'

    # query = parser.parse([x, y], (x.str0 == y.test_field1 | x.int0 == y.test_field2) | x.complex0 == y.test_field3 & 5 == x.float0, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n (str0 = test_field1 or int0 = test_field2) or (complex0 = test_field3 and 5 = float0)'

    # query = parser.parse([x, y], x.complex0 == y.test_field3 | (x.str0 == y.test_field1 | x.int0 == y.test_field2) & 5 == x.float0, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n complex0 = test_field3 or ((str0 = test_field1 or int0 = test_field2) and 5 = float0)'

    # query = parser.parse([x, y], (x.str0 == y.test_field1 | (x.int0 == y.test_field2 & 5 == x.float0)) | x.complex0 == y.test_field3, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n (str0 = test_field1 or (int0 = test_field2 and 5 = float0)) or complex0 = test_field3'
    
    term = x >= ((y, x) @ (x.str0 == y.test_field1 & x.int0 == 4)) & y.test_field2
    term_str = term.str(True)
    assert term_str == "public.default_epure >= [oraculs_domain.test_clssasdas, public.default_epure] @ (str0 == test_field1 and int0 == 4) and test_field2"

    term = (x.str0 == y.test_field1) | (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3)
    term_str = term.str(True)
    assert term_str == '(((str0 == test_field1) or ((int0 == test_field2) and (float0 == 5))) or (complex0 == test_field3))'
    query = parser.parse([x, y], term, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n  WHERE \n (str0 = test_field1 or (int0 = test_field2 and float0 = 5)) or complex0 = test_field3'
    assert 'WHERE \n (str0 = test_field1 or (int0 = test_field2 and float0 = 5)) or complex0 = test_field3' in query
    
    term = (x.int0 == y.test_field2) ^ y << (x.str0 == y.test_field1) & (5 == x.float0) | (x.complex0 == y.test_field3)
    term_str = term.str(True)
    assert term_str == '(((int0 == test_field2) ^ oraculs_domain.test_clssasdas << (str0 == test_field1) and (float0 == 5)) or (complex0 == test_field3))'
    query = parser.parse([x, y], term, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1\n WHERE \n (int0 = test_field2) and float0 = 5 or complex0 = test_field3'
    assert 'FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 \n WHERE \n (int0 = test_field2) and float0 = 5 or complex0 = test_field3' in query 

    term = y << x.str0 == y.test_field1 ^ (x.int0 == y.test_field2) & (5 == x.float0) | (x.complex0 == y.test_field3)
    term_str = term.str(True)
    assert term_str == '(oraculs_domain.test_clssasdas << (str0 == test_field1) ^ ((int0 == test_field2) and (float0 == 5)) or (complex0 == test_field3))'
    query = parser.parse([x, y], term, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1\n WHERE \n (int0 = test_field2 and float0 = 5) or complex0 = test_field3'
    assert 'FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 \n WHERE \n (int0 = test_field2 and float0 = 5) or complex0 = test_field3' in query

    term = (x.int0 == y.test_field2) ^ y << (x.str0 == y.test_field1 & (x.float0 == 5 | x.int0 == 4)) | (x.complex0 == y.test_field3)
    term_str = term.str(True)
    assert term_str == '((int0 == test_field2) ^ oraculs_domain.test_clssasdas << (str0 == test_field1 and (float0 == 5 or int0 == 4)) or (complex0 == test_field3))'
    query =  parser.parse([x, y], term, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 and (float0 = 5 or int0 = 4)\n WHERE \n (int0 = test_field2) or complex0 = test_field3'
    assert 'FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 and (float0 = 5 or int0 = 4) \n WHERE \n (int0 = test_field2) or complex0 = test_field3' in query
    
#     # wrong serialize
    term = (x.int0 == y.test_field2) & y << (x.str0 == y.test_field1 & (5 == x.float0)) ^ (x.complex0 == y.test_field3)
    term_str = term.str(True)
    assert term_str == '((int0 == test_field2) and oraculs_domain.test_clssasdas << (str0 == test_field1 and (float0 == 5)) ^ (complex0 == test_field3))'
    query =  parser.parse([x, y], term, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 and float0 = 5\n WHERE \n int0 = test_field2 and (complex0 = test_field3)'
    assert 'FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 and float0 = 5 \n WHERE \n int0 = test_field2 and (complex0 = test_field3)' in query
            
    term = (x.int0 == y.test_field2) &  (x.complex0 == y.test_field3) ^ y << (x.str0 == y.test_field1 & (5 == x.float0))
    term_str = term.str(True)
    assert term_str == '((int0 == test_field2) and (complex0 == test_field3)) ^ oraculs_domain.test_clssasdas << (str0 == test_field1 and (float0 == 5))'
    query =  parser.parse([x, y], term, False)
    # assert query == 'SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 and float0 = 5\n WHERE \n (int0 = test_field2 and complex0 = test_field3)'
    assert 'FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 and float0 = 5 \n WHERE \n (int0 = test_field2 and complex0 = test_field3)' in query                

    term = (y << (x.str0 == y.test_field1 | x.int0 == y.test_field2\
    & x.float0 ==  5 | x.complex0 == y.test_field3)) ^\
        z >> y.test_field1 == z.test_field\
        ^ x.complex0 == 'vse'\
        | y << (x.int3 == y.test_field3)\
        ^ (x.list0 > 100500 | x.tuple0 < False)\
        & x.float3 < y.test_field3\
        | x.complex3 == 4\
        ^ z >> True
    term_str = term.str(True)
    assert term_str == "oraculs_domain.test_clssasdas << (str0 == test_field1 or int0 == test_field2 and float0 == 5 or complex0 == test_field3) ^ oraculs_domain.oraculs >> (test_field1 == test_field) ^ complex0 == 'vse' or oraculs_domain.test_clssasdas << (int3 == test_field3) ^ (list0 > 100500 or tuple0 < False) and float3 < test_field3 or complex3 == 4 ^ oraculs_domain.oraculs >> True"
    query = parser.parse([x.complex0, y.test_field3], term, False)
    # assert(query) == "SELECT complex0, test_field3 FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 or (int0 = test_field2 and float0 = 5) or complex0 = test_field3\nRIGHT JOIN oraculs_domain.oraculs on test_field1 = test_field\nLEFT JOIN oraculs_domain.test_clssasdas on int3 = test_field3\nRIGHT JOIN oraculs_domain.oraculs on True\n WHERE \n complex0 = 'vse' or ((list0 > 100500 or tuple0 < False) and float3 < test_field3) or complex3 = 4"
    assert "FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 or (int0 = test_field2 and float0 = 5) or complex0 = test_field3 \nRIGHT JOIN oraculs_domain.oraculs on test_field1 = test_field \nLEFT JOIN oraculs_domain.test_clssasdas on int3 = test_field3 \nRIGHT JOIN oraculs_domain.oraculs on True \n WHERE \n complex0 = 'vse' or ((list0 > 100500 or tuple0 < False) and float3 < test_field3) or complex3 = 4" in query

    term = (y << (x.str0 == y.test_field1 | x.int0 == y.test_field2\
    & x.float0 ==  5 | x.complex0 == y.test_field3)) ^\
        z >> y.test_field1 == z.test_field\
        ^ x.complex0 == 'vse'\
        | y << (x.int3 == y.test_field3)\
        ^ ((x.list0 > 100500 | x.tuple0 < False)\
        & x.float3 < y.test_field3\
        | x.complex3 == 4)\
        ^ z >> True
    term_str = term.str(True)
    assert term_str == "oraculs_domain.test_clssasdas << (str0 == test_field1 or int0 == test_field2 and float0 == 5 or complex0 == test_field3) ^ oraculs_domain.oraculs >> (test_field1 == test_field) ^ complex0 == 'vse' or oraculs_domain.test_clssasdas << (int3 == test_field3) ^ ((list0 > 100500 or tuple0 < False) and float3 < test_field3 or complex3 == 4) ^ oraculs_domain.oraculs >> True"
    query = parser.parse([x.complex0, y.test_field3], term, False)

    # assert(query) == "SELECT complex0, test_field3 FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 or (int0 = test_field2 and float0 = 5) or complex0 = test_field3\nRIGHT JOIN oraculs_domain.oraculs on test_field1 = test_field\nLEFT JOIN oraculs_domain.test_clssasdas on int3 = test_field3\nRIGHT JOIN oraculs_domain.oraculs on True\n WHERE \n complex0 = 'vse' or ((list0 > 100500 or tuple0 < False) and float3 < test_field3 or complex3 = 4)"
                    #  "SELECT complex0, test_field3 FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 or (int0 = test_field2 and float0 = 5) or complex0 = test_field3\nRIGHT JOIN oraculs_domain.oraculs on test_field1 = test_field\nLEFT JOIN oraculs_domain.test_clssasdas on int3 = test_field3\nRIGHT JOIN oraculs_domain.oraculs on True\n WHERE \n complex0 = 'vse' or ((list0 > 100500 or tuple0 < False) and float3 < test_field3 or complex3 = 4)"
    assert "FROM public.default_epure \n LEFT JOIN oraculs_domain.test_clssasdas on str0 = test_field1 or (int0 = test_field2 and float0 = 5) or complex0 = test_field3 \nRIGHT JOIN oraculs_domain.oraculs on test_field1 = test_field \nLEFT JOIN oraculs_domain.test_clssasdas on int3 = test_field3 \nRIGHT JOIN oraculs_domain.oraculs on True \n WHERE \n complex0 = 'vse' or ((list0 > 100500 or tuple0 < False) and float3 < test_field3 or complex3 = 4)" in query

    # term = x.int3 % '%test_like%'
    # query = parser.parse(term, False)
    # assert query == "(f1 == f2 or f3 % '%test_like%' and 5 == f5 or (f6 == f7))"

def test_columns_select():
    db = DbProxy(real_db)    
    real_x = real_db['default_epure']
    parser = TermParser(real_x)

    '''SELECT cols.table_schema, cols.table_name, 
                        cols.column_name, cols.is_nullable, cols.data_type, cols.column_default,

                        cols_constr.table_schema AS foreign_schema,
                        cols_constr.table_name AS foreign_table,
                        cols_constr.column_name AS foreign_column,

                        constr.constraint_type

                        FROM information_schema.columns cols
                        left join information_schema.constraint_column_usage cols_constr
                            on cols.table_schema = cols_constr.table_schema and cols.table_name = cols_constr.table_name
                            and cols.column_name = cols_constr.column_name
                        left join information_schema.table_constraints constr
                            on cols_constr.constraint_name = constr.constraint_name WHERE
                        cols.table_schema = \'public\' AND
                        cols.table_name = \'default_epure\' '''

    cols = db['information_schema.columns']
    cols_constr = db['information_schema.constraint_column_usage']
    constr = db['information_schema.table_constraints']

    header = (cols.table_schema, cols.table_name, cols.column_name, cols.is_nullable, 
                cols.data_type, cols.column_default,
            cols_constr.table_schema, cols_constr.table_name, cols_constr.column_name, 
            constr.constraint_type)

    term = cols_constr << (cols.table_schema == cols_constr.table_schema 
                            & cols.table_name == cols_constr.table_name 
                            & cols.column_name == cols_constr.column_name) \
            ^ constr << cols_constr.constraint_name == constr.constraint_name \
                \
            ^ cols.table_schema == 'public' \
            & cols.table_name == 'default_epure'

    query = parser.parse(header, term)

    # assert query == "SELECT information_schema.columns.table_schema, information_schema.columns.table_name, information_schema.columns.column_name, information_schema.columns.is_nullable, information_schema.columns.data_type, information_schema.columns.column_default, information_schema.constraint_column_usage.table_schema, information_schema.constraint_column_usage.table_name, information_schema.constraint_column_usage.column_name, information_schema.table_constraints.constraint_type FROM information_schema.columns \n LEFT JOIN information_schema.constraint_column_usage on information_schema.columns.table_schema = information_schema.constraint_column_usage.table_schema and information_schema.columns.table_name = information_schema.constraint_column_usage.table_name and (information_schema.columns.column_name = information_schema.constraint_column_usage.column_name)\nLEFT JOIN information_schema.table_constraints on information_schema.constraint_column_usage.constraint_name = information_schema.table_constraints.constraint_name\n WHERE \n information_schema.columns.table_schema = 'public' and information_schema.columns.table_name = 'default_epure'"
#                     # "SELECT information_schema.columns.table_schema, information_schema.columns.table_name, information_schema.columns.column_name, information_schema.columns.is_nullable, information_schema.columns.data_type, information_schema.columns.column_default, information_schema.constraint_column_usage.table_schema, information_schema.constraint_column_usage.table_name, information_schema.constraint_column_usage.column_name, information_schema.table_constraints.constraint_type FROM information_schema.columns \n LEFT JOIN information_schema.constraint_column_usage on information_schema.columns.table_schema = information_schema.constraint_column_usage.table_schema and information_schema.columns.table_name = information_schema.constraint_column_usage.table_name and (information_schema.columns.column_name = information_schema.constraint_column_usage.column_name)\nLEFT JOIN information_schema.table_constraints on information_schema.constraint_column_usage.constraint_name = information_schema.table_constraints.constraint_name\n WHERE \n information_schema.columns.table_schema = 'public' and information_schema.columns.table_name = 'default_epure'"
    assert "FROM information_schema.columns \n LEFT JOIN information_schema.constraint_column_usage on information_schema.columns.table_schema = information_schema.constraint_column_usage.table_schema and information_schema.columns.table_name = information_schema.constraint_column_usage.table_name and (information_schema.columns.column_name = information_schema.constraint_column_usage.column_name) \nLEFT JOIN information_schema.table_constraints on information_schema.constraint_column_usage.constraint_name = information_schema.table_constraints.constraint_name \n WHERE \n information_schema.columns.table_schema = 'public' and information_schema.columns.table_name = 'default_epure'" in query

    # # mixed
    term =  cols.table_schema == 'public' \
            & cols.table_name == 'default_epure'\
                \
            ^ cols_constr << (cols.table_schema == cols_constr.table_schema 
                            & cols.table_name == cols_constr.table_name 
                            & cols.column_name == cols_constr.column_name) \
            ^ constr << cols_constr.constraint_name == constr.constraint_name


    query = parser.parse(header, term)

    # assert query == "SELECT information_schema.columns.table_schema, information_schema.columns.table_name, information_schema.columns.column_name, information_schema.columns.is_nullable, information_schema.columns.data_type, information_schema.columns.column_default, information_schema.constraint_column_usage.table_schema, information_schema.constraint_column_usage.table_name, information_schema.constraint_column_usage.column_name, information_schema.table_constraints.constraint_type FROM information_schema.columns \n LEFT JOIN information_schema.constraint_column_usage on information_schema.columns.table_schema = information_schema.constraint_column_usage.table_schema and information_schema.columns.table_name = information_schema.constraint_column_usage.table_name and (information_schema.columns.column_name = information_schema.constraint_column_usage.column_name)\nLEFT JOIN information_schema.table_constraints on information_schema.constraint_column_usage.constraint_name = information_schema.table_constraints.constraint_name\n WHERE \n information_schema.columns.table_schema = 'public' and information_schema.columns.table_name = 'default_epure'"
                   ## "SELECT information_schema.columns.table_schema, information_schema.columns.table_name, information_schema.columns.column_name, information_schema.columns.is_nullable, information_schema.columns.data_type, information_schema.columns.column_default, information_schema.constraint_column_usage.table_schema, information_schema.constraint_column_usage.table_name, information_schema.constraint_column_usage.column_name, information_schema.table_constraints.constraint_type FROM information_schema.columns \n LEFT JOIN information_schema.constraint_column_usage on information_schema.columns.table_schema = information_schema.constraint_column_usage.table_schema and information_schema.columns.table_name = information_schema.constraint_column_usage.table_name and (information_schema.columns.column_name = information_schema.constraint_column_usage.column_name)\nLEFT JOIN information_schema.table_constraints on information_schema.constraint_column_usage.constraint_name = information_schema.table_constraints.constraint_name\n WHERE \n information_schema.columns.table_schema = 'public' and information_schema.columns.table_name = 'default_epure'"

    assert "FROM information_schema.columns \n LEFT JOIN information_schema.constraint_column_usage on information_schema.columns.table_schema = information_schema.constraint_column_usage.table_schema and information_schema.columns.table_name = information_schema.constraint_column_usage.table_name and (information_schema.columns.column_name = information_schema.constraint_column_usage.column_name) \nLEFT JOIN information_schema.table_constraints on information_schema.constraint_column_usage.constraint_name = information_schema.table_constraints.constraint_name \n WHERE \n information_schema.columns.table_schema = 'public' and information_schema.columns.table_name = 'default_epure'" in query

#     # splited
    term1 =  cols.table_schema == 'public' \
            & cols.table_name == 'default_epure'
                
    term2 = cols_constr << (cols.table_schema == cols_constr.table_schema 
                            & cols.table_name == cols_constr.table_name 
                            & cols.column_name == cols_constr.column_name) \
            ^ constr << cols_constr.constraint_name == constr.constraint_name

    term = term1 ^ term2

    query = parser.parse(header, term)

#     assert query == "SELECT information_schema.columns.table_schema, information_schema.columns.table_name, information_schema.columns.column_name, information_schema.columns.is_nullable, information_schema.columns.data_type, information_schema.columns.column_default, information_schema.constraint_column_usage.table_schema, information_schema.constraint_column_usage.table_name, information_schema.constraint_column_usage.column_name, information_schema.table_constraints.constraint_type FROM information_schema.columns \n LEFT JOIN information_schema.constraint_column_usage on information_schema.columns.table_schema = information_schema.constraint_column_usage.table_schema and information_schema.columns.table_name = information_schema.constraint_column_usage.table_name and (information_schema.columns.column_name = information_schema.constraint_column_usage.column_name)\nLEFT JOIN information_schema.table_constraints on information_schema.constraint_column_usage.constraint_name = information_schema.table_constraints.constraint_name\n WHERE \n (information_schema.columns.table_schema = 'public' and information_schema.columns.table_name = 'default_epure')"
    assert "FROM information_schema.columns \n LEFT JOIN information_schema.constraint_column_usage on information_schema.columns.table_schema = information_schema.constraint_column_usage.table_schema and information_schema.columns.table_name = information_schema.constraint_column_usage.table_name and (information_schema.columns.column_name = information_schema.constraint_column_usage.column_name) \nLEFT JOIN information_schema.table_constraints on information_schema.constraint_column_usage.constraint_name = information_schema.table_constraints.constraint_name \n WHERE \n (information_schema.columns.table_schema = 'public' and information_schema.columns.table_name = 'default_epure')" in query

    # header in term
    # term =  [cols.table_schema, cols.table_name, cols.column_name, cols.is_nullable,
    #             cols.data_type, cols.column_default] \
    #         ^ cols.table_schema == 'public' \
    #         & cols.table_name == 'default_epure' ^ \
    #         cols_constr << (cols.table_schema == cols_constr.table_schema 
    #                         & cols.table_name == cols_constr.table_name 
    #                         & cols.column_name == cols_constr.column_name) \
    #         ^[constr.constraint_type] \
    #         ^ constr << cols_constr.constraint_name == constr.constraint_name
# ^[cols_constr.table_schema, cols_constr.table_name, cols_constr.column_name] \

    # query = parser.parse(term, False)

    # assert query == ""

def test_join_with_delimeter():
    db = DbProxy(real_db)
    real_x = real_db['default_epure']
    parser = TermParser(real_x)
    x = db['default_epure']
    y = db['epure_class1']
    debugger = MatplotTermDebugger()

    lst = (1, 2, 3)

    query = (x,y) @ y << (x.epure_class1 == y.node_id)

    str_query = query.str(True, True)

    query2 = (x,y) @ (y << (x.epure_class1 == y.node_id)) ^ x.str0 >= lst
    # query2.debugger = debugger
    # query2.debugger.each_step = True
    str_query2 = query2.str(True, True)
    
    query = (x,y) @ y << (x.epure_class1 == y.node_id) ^ x.str0 >= lst

    query = parser.parse(query)
    
    assert 'FROM public.default_epure \n LEFT JOIN public.epure_class1 on public.default_epure.epure_class1 = public.epure_class1.node_id \n WHERE \n public.default_epure.str0 in (1, 2, 3)' in query