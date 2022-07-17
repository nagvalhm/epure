from .epure_classes import db as real_db
from ..epure.resource.db.pseudo_table import PseudoDb

def test_query():
    db = PseudoDb(real_db)
    x = db['default_epure']
    y = db['oraculs_domain.test_clssasdas']
    # z = db['no_table']
    z = db['oraculs_domain.oraculs']

    q = ((x.str0 == y.test_field1) | (x.int0 == y.test_field2) \
        & (5 == x.float0) | (x.complex0 == y.test_field3))
    a = 1
    # q = (x, y) ^ y << (x.str0 == y.test_field1 | x.int0 == y.test_field2 \
    # & x.float0 ==  5 | x.complex0 == y.test_field3)\
    #     & x.complex0 == 'vse' \
    #     | y << (x.str0 == y.test_field3)\
    #     & (x.list0 > 100500 | x.tuple0 < False) \
    #     & x.str0 < y.test_field3\
    #     & x.no_field == 4\
    #     & x >> z
# '((str0 = test_field1 OR (int0 = test_field2 AND float0 = 5)) OR complex0 = test_field3)'
# '((str0 = test_field1 OR (int0 = test_field2 AND float0 = 5)) OR complex0 = test_field3)'
    assert str(q) == '''SELECT * FROM public.default_epure
        LEFT JOIN oraculs_domain.test_clssasdas
        ON ((public.default_epure.str0 = oraculs_domain.test_clssasdas.test_field1 OR public.default_epure.str0 = oraculs_domain.test_clssasdas.test_field2) OR
    '''