from ....epure.resource.node.elist import Elist
import pytest
from ....epure.epure import epure, Epure
from typing import List
from ...epure_classes import EpureClass1

def test_elist_epures():

    @epure()
    class EpureCls4:
        str4:str
    
    inst1 = EpureCls4()
    inst1.str4 = "abc"
    inst2 = EpureCls4()
    inst2.str4 = "defg"
    inst3 = EpureCls4()
    inst3.str4 = "hyz"
    inst4 = EpureCls4()
    inst4.str4 = "gdf"

    @epure()
    class EpureClsWElist1:
        elist1:Elist[EpureCls4] 
        str2:str
        int3:int
        epure_field1:EpureClass1
    
    epurecls1 = EpureClsWElist1()
    epurecls1.elist1 = Elist[EpureCls4]([inst2,inst3,inst4,inst1])
    id_1 = epurecls1.save().node_id
    res1 = epurecls1.table.read(node_id=id_1)[0]
    # res_str4 = res1.elist1[0].value.str4
    res_str4 = res1.elist1[0].str4
    assert res_str4 == inst2.str4

    @epure()
    class EpureClsWElist2:
        elist2:Elist[EpureCls4]
        str3:str
        int4:int
        epure_field2:EpureClass1

    epurecls2 = EpureClsWElist2()
    epurecls2.elist2 = Elist[EpureCls4]([inst1,inst3,inst2,inst4])
    id_2 = epurecls2.save().node_id
    res2 = epurecls2.table.read(node_id=id_2)[0]

    res2.elist2.sort(key=lambda item: item.str4)

    res1.elist1.sort(key=lambda item: item.str4)

    assert res2.elist2 == res2.elist1

# @pytest.fixture
def elist_epure_cls1():

    @epure()
    class EpureClsElist:
        elist:Elist[str] 
        str0:str
        int2:int
        epure_field:EpureClass1

    return EpureClsElist()


def test_elist_str():
    inst = elist_epure_cls1()
    inst.elist = Elist[str](['abc','defg',"the","brown","fox","jumps","over","lazy","dog"])
    inst.str0 = "The quick brown fox jumps over the lazy dog"
    inst.int2 = 42
    inst.epure_field = EpureClass1()
    id = inst.save().node_id
    res = inst.table.read(node_id=id)
    epure = res[0].epure_field
    elist = res[0].elist
    # assert elist == inst.elist

