# from .test_epure import default_epure
from .epure_classes import DefaultEpure
import pytest
from .epure_classes import db as real_db
from ..epure.parser.leaf import DbProxy
# from ..epure.epure import Epure
# from typing import cast

# def test_read_default_epure_lambda_simple():

#     res = DefaultEpure.resource.read(lambda tp: tp.str3 in ('str3_value', 'str3_value2'))
#     assert isinstance(res, list) and bool(res[0])

def test_read_default_epure_lambda():

    res = DefaultEpure.resource.read(lambda tp, dbp: 
        [tp.float3, tp.range0, tp.epure_class, dbp['epure_class3'].node_id,

        dbp['epure_class3'] << (tp.epure_class == dbp['epure_class3'].node_id
        | tp.generic_list0 == dbp['epure_class3'].generic_list2) ^

        tp.str3 == 'str3_value' 
        & (tp.int3 > 3 | tp.float3 < 0.8)

        ^dbp['epure_class1'] << tp.epure_class1 == dbp['epure_class1'].node_id

        # & tp.int0 < dbp['epure_class1'].int2
        ]
    )
    assert isinstance(res, list) and bool(res[0])

def test_read_default_epure_lambda2():

    # res = DefaultEpure.resource.read(lambda tp, dbp:
    #     (tp.float3, tp.range0, tp.epure_class, dbp['epure_class3'].node_id)@

    #     dbp['epure_class3'] << (tp.epure_class == dbp['epure_class3'].node_id
    #     | tp.generic_list0 == dbp['epure_class3'].generic_list2) ^

    #     tp.str3 == 'str3_value' 
    #     & (tp.int3 > 3 | tp.float3 < 0.8)

    #     ^dbp['epure_class1'] << tp.epure_class1 == dbp['epure_class1'].node_id

    #     # & tp.int0 < dbp['epure_class1'].int2
        
    # )
    # assert isinstance(res, list) and bool(res[0])

    DefaultEpure.resource.read(lambda pr, abc: [pr.int0 >= ('all-categories', 'promotions')])
    # DefaultEpure.resource.read(lambda pr, abc: [pr.int0 % "\%abc%"]) # test like and \ notation of python


def test_read_default_epure_kwargs():
    # DefaultEpure.resource.read([], 'and', complex0=5+7j, float3=750479.0714551052)
    # SELECT * FROM public.default_epure where complex0 ~= point('5.0, 7.0') and float3 = 750479.0714551052
    DefaultEpure.resource.read([], 'and', complex0=5+7j, float3=750479.0714551052) # fix point type read !!


def test_read_default_epure_sql():
    DefaultEpure.resource.read('select * from default_epure where float3 = 308396.1685926297')

# def test_read_default_single_backslash():
#     src = "select * from public.default_epure where public.default_epure.str0 = '\gvorog'"
#     res = "".join(list(src))
#     res = DefaultEpure.resource.read(res)
#     res

def test_read_default_epure_term():
    # tp = DefaultEpure.tp
    tp = DefaultEpure.resource.querying_proxy
    # dbp = DefaultEpure.dp
    dbp = DefaultEpure.resource.resource_proxy
    ec_3 = dbp['epure_class3']
    ec_1 = dbp['epure_class1']

    query1 = (ec_3 << (tp.epure_class == ec_3.node_id
        | tp.generic_list0 == ec_3.generic_list2) ^

        tp.str3 == 'str3_value'
        & (tp.int3 > 3 | tp.float3 < 0.8)

        ^ec_1 << tp.epure_class1 == ec_1.node_id

        & tp.int0 < ec_1.int2)

    query2 = (ec_1.int2 == 1111)

    with pytest.raises(Exception) as e_info:
        DefaultEpure.resource.read(tp.float3, tp.range0, 
            tp.epure_class, ec_1.node_id, ec_1.int2, query1 & query2)
    assert "^\nHINT:  No operator matches the given name and argument types. You might need to add explicit type casts.\n" in e_info.value.args[0]

def test_read_default_epure_readmethod():
    DefaultEpure.read_method(3, 0.8, 1111)




    # default_epure = cast(Epure, default_epure)
    # DefaultEpure.resource.read(lambda x, db: 
    #     db['another_table'] << (x.govno == db['another_table'].huiniya 
    #     | x.govno == db['another_table'].other_huiniya) ^

    #     x.zaebalo == 'vse' 
    #     & (x.skolko > 100500 | x.pohui < False) 
    #     & x.govno < db['its_table'].poeben)

# def test_read_default_epure_sql2():
#     db = DbProxy(real_db)
#     x = db['default_epure']
#     real_x = real_db['default_epure']
#     y = db['oraculs_domain.test_clssasdas']
#     # z = db['no_table']
#     z = db['oraculs_domain.oraculs']
#     a = db['oraculs_domain.competitions']
#     b = db['oraculs_domain.tasks']

#     DefaultEpure.resource.read(a.f1 @ a.f1 == z.f2 | a.f4 == a.f3 % 3 & 5 == a.f5 | (a.f6 == z.f7) | a.f1 >= ((a.f4,a.f2)@(x.str0 == y.test_field1)))

def test_read_default_epure_sql2():
    db = DbProxy(real_db)
    x = db['default_epure']
    real_x = real_db['default_epure']
    y = db['oraculs_domain.test_clssasdas']
    # z = db['no_table']
    z = db['oraculs_domain.oraculs']
    a = db['oraculs_domain.competitions']
    b = db['oraculs_domain.tasks']

    DefaultEpure.resource.read(y ^ x << x.float0 == z.node_id)
    # DefaultEpure.resource.read(y @ x << x.float0 == z.node_id)
    # DefaultEpure.resource.read(x)

def test_read_default_epure_empty():
    db = DbProxy(real_db)
    x = db['default_epure']

    res_read = DefaultEpure.resource.read()

    # read_sql = DefaultEpure.resource.read('select * from public.default_epure')

    # assert res_read == read_sql
    assert isinstance(res_read, list) and bool(res_read[0])

# def test_read_join_with_delimeter():
#     db = DbProxy(real_db)
#     x = db['default_epure']
#     y = db['epure_class1']

#     DefaultEpure.resource.read([x,y] @ y << (x.epure_class1 == y.node_id))

