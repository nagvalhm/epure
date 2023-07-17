# from .test_epure import default_epure
from .epure_classes import DefaultEpure
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


def test_read_default_epure_kwargs():
    # DefaultEpure.resource.read([], 'and', complex0=5+7j, float3=750479.0714551052)
    DefaultEpure.resource.read([], 'and', complex0=5+7j, float3=750479.0714551052)



def test_read_default_epure_sql():
    DefaultEpure.resource.read('select * from default_epure where float3 = 308396.1685926297')


def test_read_default_epure_term():
    tp = DefaultEpure.tp
    dbp = DefaultEpure.dp
    ec_3 = dbp['epure_class3']
    ec_1 = dbp['epure_class1']

    query1 = (ec_3 << (tp.epure_class == ec_3.node_id
        | tp.generic_list0 == ec_3.generic_list2) ^

        tp.str3 == 'str3_value'
        & (tp.int3 > 3 | tp.float3 < 0.8)

        ^ec_1 << tp.epure_class1 == ec_1.node_id

        & tp.int0 < ec_1.int2)

    query2 = (ec_1.int2 == 1111)

    DefaultEpure.resource.read(tp.float3, tp.range0, 
        tp.epure_class, ec_1.node_id, ec_1.int2, query1 & query2)

def test_read_default_epure_readmethod():
    DefaultEpure.read_method(3, 0.8, 1111)




    # default_epure = cast(Epure, default_epure)
    # DefaultEpure.resource.read(lambda x, db: 
    #     db['another_table'] << (x.govno == db['another_table'].huiniya 
    #     | x.govno == db['another_table'].other_huiniya) ^

    #     x.zaebalo == 'vse' 
    #     & (x.skolko > 100500 | x.pohui < False) 
    #     & x.govno < db['its_table'].poeben)