from ....epure.resource.node.elist import Elist
import pytest
from ....epure.epure import epure
from typing import List
from ...epure_classes import EpureClass1

# @pytest.fixture
def elist_epure_cls1():

    @epure()
    class EpureClsElist:
        elist:Elist[str] 
        str0:str
        int2:int
        epure_field:EpureClass1

    return EpureClsElist()

def test_elist():
    inst = elist_epure_cls1()
    inst.elist = Elist[str](['abc','defg',"the","brown","fox","jumps","over","lazy","dog"])
    inst.str0 = "The quick brown fox jumps over the lazy dog"
    inst.int2 = 42
    inst.epure_field = EpureClass1()
    id = inst.save().node_id
    res = inst.table.read(node_id=id)
    epure = res[0].epure_field
    elist = res[0].elist
    pass