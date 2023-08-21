# from ....epure.resource.node.elist import Elist
from ....epure import Elist
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

    # res2.elist2.sort(key=lambda item: item.str4)

    # res1.elist1.sort(key=lambda item: item.str4)

    res2.elist2.read()
    pass

    # assert res2.elist2 == res2.elist1

@epure()
class EpureClsElist:
    elist:Elist[str] 
    str0:str
    int2:int
    epure_field:EpureClass1

# @pytest.fixture
def elist_epure_cls1():

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

def test_elist_str_append():
    inst = elist_epure_cls1()
    inst.elist = Elist[str](["the","long","way"])
    inst.str0 = "The quick brown fox jumps over the lazy dog"
    inst.epure_field = EpureClass1()
    id1 = inst.save().node_id
    res_before_update = inst.table.read(node_id=id1)[0]
    res_before_update.elist.append('home')
    id2 = res_before_update.save().node_id
    res_after_update = inst.table.read(node_id=id2)[0]
    res_after_update.elist.read()
    assert id1 == id2
    assert res_after_update.elist[-1] == "home"
    # assert elist == inst.elist

def test_elist_str_remove_by_index():
    inst = elist_epure_cls1()
    inst.elist = Elist[str](["object","class","item"])
    inst.str0 = "The quick brown fox jumps over the lazy dog"
    inst.epure_field = EpureClass1()
    id1 = inst.save().node_id
    res_before_update = inst.table.read(node_id=id1)[0]
    inst.elist.pop(-1)
    id2 = inst.save().node_id
    res_after_update1 = inst.table.read(node_id=id2)[0]
    res_after_update1.elist.read()
    assert id1 == id2
    assert inst.elist[1] == res_after_update1.elist[-1]
    res_after_update1.elist.pop(0)
    id3 = res_after_update1.save().node_id
    res_after_update2 = inst.table.read(node_id=id3)[0]
    assert inst.elist[1] == res_after_update2.elist[0]
    # assert elist == inst.elist

def test_elist_str_set_item_by_index():
    inst = elist_epure_cls1()
    inst.elist = Elist[str](["loan","price","driver"])
    id1 = inst.save().node_id
    res_after_update1 = inst.table.read(node_id=id1)[0]
    res_after_update1.elist[1] = "value"
    id2 = res_after_update1.save().node_id
    res_after_update2 = inst.table.read(node_id=id2)[0]
    res_after_update2.elist.read()
    assert res_after_update2.elist[1] == "value"

def test_elist_str_insert_into_elist():
    inst = elist_epure_cls1()
    inst.elist = Elist[str](["dove","love","peace"])
    id1 = inst.save().node_id
    res_after_update1 = inst.table.read(node_id=id1)[0]
    res_after_update1.elist.insert(0,"derkuli")
    id2 = res_after_update1.save().node_id
    res_after_update2 = inst.table.read(node_id=id2)[0]
    res_after_update2.elist.read()
    assert res_after_update2.elist[0] == "derkuli"
    assert res_after_update2.elist[1] == "dove"

def test_elist_str_set_item_by_index_wrong_type():
    inst = elist_epure_cls1()
    inst.elist = Elist[str](["loan","price","driver"])
    try:
        inst.elist[1] = 42
    except(TypeError):
        return True
    
def test_elist_str_from_dict_and_to_dict():
    inst = elist_epure_cls1()
    inst.elist = Elist[str](["long","live","the","king"])
    inst.str0 = "Snug as a bug in a rug"
    inst.epure_field = EpureClass1()
    inst.save()
    inst_to_dict = inst.to_dict()
    inst_from_dict = EpureClsElist.from_dict(inst_to_dict)
    inst_from_dict.epure_field
    inst_from_dict.elist
    pass

def test_elist_str_from_dict_and_to_dict():
    inst = elist_epure_cls1()
    inst.elist = Elist[str](["aurora","borealis","northen","lights"])
    inst.str0 = "A piece of cake"
    inst.epure_field = EpureClass1()
    inst_to_dict = inst.to_dict()
    inst_from_dict = EpureClsElist.from_dict(inst_to_dict)
    inst_from_dict.epure_field
    inst_from_dict.elist
    pass

def test_elist_str_from_dict():
    elist = (["viktor","van","dem","rossen"])
    str0 = "Bread and butter"
    _dict = {"elist":elist,"str0":str0}
    inst_from_dict = EpureClsElist.from_dict(_dict)
    inst_from_dict.elist
    assert inst_from_dict.str0 == str0