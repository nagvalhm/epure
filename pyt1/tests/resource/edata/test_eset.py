from ....epure import Eset
import pytest
from ....epure.epure import epure, Epure
from typing import List
from ...epure_classes import EpureClass1
from ....epure.resource.edata.edata import EData
from jsonpickle import loads

#delete me
from ....epure.resource.edata.ecollection_metacls import ECollectionMetacls

def test_eset_epures():

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
    class EpureClsWEset1:
        eset1:Eset[EpureCls4]
        str2:str
        int3:int
        epure_field1:EpureClass1
    
    epurecls1 = EpureClsWEset1()
    # epurecls1.eset1 = Eset[EpureCls4]((inst2,inst3,inst4,inst1))
    epurecls1.eset1 = Eset[EpureCls4]((inst2,inst3,inst4,inst1))
    try:
        epurecls1.eset1.add(inst1)
    except(ValueError):
        pass
    id_1 = epurecls1.save().data_id
    ids1 = epurecls1.eset1.ids
    res1 = epurecls1.table.read(data_id=id_1)[0]
    # res_str4 = res1.eset1[0].value.str4
    res1.eset1.load()
    ids2 = res1.eset1.ids

    assert set(ids1) == set(ids2)
    # res1.eset1.ids

    @epure()
    class EpureClsWEset2:
        eset2:Eset[EpureCls4]
        str3:str
        int4:int
        epure_field2:EpureClass1

    epurecls2 = EpureClsWEset2()
    epurecls2.eset2 = Eset[EpureCls4]((inst1,inst3,inst2,inst4))
    id_2 = epurecls2.save().data_id
    res2 = epurecls2.table.read(data_id=id_2)[0]

    # res2.eset2.sort(key=lambda item: item.str4)

    # res1.eset1.sort(key=lambda item: item.str4)

    # res2.eset2.read()
    pass

    # assert res2.eset2 == res2.eset1

@epure()
class EpureClsEset:
    eset:Eset[str] 
    str0:str
    int2:int
    epure_field:EpureClass1

# @pytest.fixture
def eset_epure_cls1():

    return EpureClsEset()


def test_eset_str():
    inst = eset_epure_cls1()
    inst.eset = Eset[str](['abc','defg',"the","brown","fox","jumps","over","lazy","dog"])
    inst.str0 = "The quick brown fox jumps over the lazy dog"
    inst.int2 = 42
    inst.epure_field = EpureClass1()
    id = inst.save().data_id
    res = inst.table.read(data_id=id)
    epure = res[0].epure_field
    eset = res[0].eset
    # assert eset == inst.eset

def test_eset_str_append():
    inst = eset_epure_cls1()
    inst.eset = Eset[str](["the","long","way"])
    inst.str0 = "The quick brown fox jumps over the lazy dog"
    inst.epure_field = EpureClass1()
    id1 = inst.save().data_id
    res_before_update = inst.table.read(data_id=id1)[0]
    res_before_update.eset.add('home')
    id2 = res_before_update.save().data_id
    res_after_update = inst.table.read(data_id=id2)[0]
    # res_after_update.eset.read()
    # assert id1 == id2
    res_after_update.eset.load()
    assert "home" in res_after_update.eset
    # assert eset == inst.eset

def test_eset_str_remove_by_index():
    inst = eset_epure_cls1()
    inst.eset = Eset[str](["object","class","item"])
    inst.str0 = "The quick brown fox jumps over the lazy dog"
    inst.epure_field = EpureClass1()
    id1 = inst.save().data_id
    res_before_update = inst.table.read(data_id=id1)[0]
    inst.eset.discard("object")
    id2 = inst.save().data_id
    res_after_update1 = inst.table.read(data_id=id2)[0]
    # res_after_update1.eset.read()
    assert id1 == id2
    assert inst.eset == res_after_update1.eset
    res_after_update1.eset.discard(0)
    id3 = res_after_update1.save().data_id
    res_after_update2 = inst.table.read(data_id=id3)[0]
    assert inst.eset == res_after_update2.eset
    # assert eset == inst.eset

def test_eset_str_set_item_by_index():
    inst = eset_epure_cls1()
    inst.eset = Eset[str](["loan","price","driver"])
    id1 = inst.save().data_id
    res_after_update1 = inst.table.read(data_id=id1)[0]
    res_after_update1.eset.load()
    try:
        res_after_update1.eset[1] = "value"
        assert False 
    except TypeError: # eset doesnt support items assigment
        assert True
    id2 = res_after_update1.save().data_id
    res_after_update2 = inst.table.read(data_id=id2)[0]
    res_after_update2.eset.load()
    assert "loan" in res_after_update2.eset

def test_eset_str_insert_into_eset():
    inst = eset_epure_cls1()
    inst.eset = Eset[str](["dove","love","peace"])
    id1 = inst.save().data_id
    res_after_update1 = inst.table.read(data_id=id1)[0]
    res_after_update1.eset.add("derkuli")
    id2 = res_after_update1.save().data_id
    res_after_update2 = inst.table.read(data_id=id2)[0]
    # res_after_update2.eset.read()
    res_after_update2.eset.load()
    assert "derkuli" in res_after_update2.eset 
    assert "dove" in res_after_update2.eset 

def test_eset_str_set_item_by_index_wrong_type():
    inst = eset_epure_cls1()
    inst.eset = Eset[str](["loan","price","driver"])
    try:
        inst.eset[1] = 42
    except(TypeError):
        return True
    
def test_eset_str_from_dict_and_to_dict_save():
    inst = eset_epure_cls1()
    inst.eset = Eset[str](["long","live","the","king"])
    inst.str0 = "Snug as a bug in a rug"
    inst.epure_field = EpureClass1()
    id = inst.save().data_id
    res = inst.table.read(data_id=id)[0]
    inst_to_dict = inst.to_dict()
    inst_to_dict_read = res.to_dict()
    inst_from_dict = EpureClsEset.from_dict(inst_to_dict)
    inst_from_dict_read = EpureClsEset.from_dict(inst_to_dict_read)
    inst_from_dict.epure_field
    inst_from_dict.eset
    inst_from_dict_read.epure_field
    inst_from_dict_read.eset
    pass

def test_eset_str_from_dict_and_to_dict():
    inst = eset_epure_cls1()
    inst.eset = Eset[str](["aurora","borealis","northen","lights"])
    inst.str0 = "A piece of cake"
    inst.epure_field = EpureClass1()
    inst_to_dict = inst.to_dict()
    inst_from_dict = EpureClsEset.from_dict(inst_to_dict)
    inst_from_dict.epure_field
    inst_from_dict.eset
    pass

def test_eset_str_from_dict():
    eset = (["viktor","van","dem","rossen"])
    str0 = "Bread and butter"
    _dict = {"eset":eset,"str0":str0}
    inst_from_dict = EpureClsEset.from_dict(_dict)
    inst_from_dict.eset
    assert inst_from_dict.str0 == str0

def test_eset_bytes_from_dict_save_read():
    @epure()
    class EpureClsEsetBytes:
        eset:Eset[bytes]
        str0:str
        int2:int
        epure_field:EpureClass1

    inst = EpureClsEsetBytes()
    inst.eset = Eset[bytes]([b"utf9",b"asci",b"butes"])
    inst.str0 = "Icepick"
    inst.epure_field = EpureClass1()
    id = inst.save().data_id
    res = inst.table.read(data_id=id)[0]
    inst_to_dict = res.to_dict()
    inst_from_dict = EpureClsEsetBytes.from_dict(inst_to_dict)
    inst_from_dict.epure_field
    inst_from_dict.eset
    inst.eset.ids
    res.eset.ids
    pass

def test_eset_bytes_from_dict():
    @epure()
    class EpureClsEsetBytes:
        eset:Eset[bytes]
        str0:str
        int2:int
        epure_field:EpureClass1

    eset = ["bate","utaf13","utah5"]
    str0 = "Carrot cake"
    _dict = {"eset":eset, "str0":str0}
    inst_from_dict = EpureClsEsetBytes.from_dict(_dict)
    inst_from_dict.eset
    pass

def test_eset_epure_remove_item_by_val():

    @epure()
    class EpureCls5:
        str4:str
    
    inst1 = EpureCls5()
    inst1.str4 = "abc"
    inst2 = EpureCls5()
    inst2.str4 = "defg"
    inst3 = EpureCls5()
    inst3.str4 = "hyz"
    inst4 = EpureCls5()
    inst4.str4 = "gdf"

    @epure()
    class EpureClsWEset1:
        eset1:Eset[EpureCls5]
        str2:str
        int3:int
        epure_field1:EpureClass1
    
    epurecls1 = EpureClsWEset1()
    # epurecls1.eset1 = Eset[EpureCls4]((inst2,inst3,inst4,inst1))
    epurecls1.eset1 = Eset[EpureCls5]((inst2,inst3,inst4,inst1))
    try:
        epurecls1.eset1.add(inst1)
    except(ValueError):
        pass
    id_1 = epurecls1.save().data_id
    epurecls1.eset1.discard(inst2)
    assert inst2 not in epurecls1.eset1
    
    ids1 = epurecls1.eset1.ids
    res1 = epurecls1.table.read(data_id=id_1)[0]
    

def test_eset_docs_example():

    @epure()
    class Example:
        int_attr:complex = 5 + 7j
        str_attr:str = "Hello Sky!"

    @epure()
    class EsetExample:
        eset_str:Eset[str]
        eset_epure:Eset[Example]

    ex1 = Example()
    ex1.complex = 10 + 8j

    ex2 = Example()

    eset_ex = EsetExample()

    eset_ex.eset_epure = Eset[Example]((ex1, ex2))

    eset_ex.eset_str = Eset[str](("Grin", "like", "a", "Cheshire", "cat"))

    eset_ex.save() # (1)!

    eset_ex_read = EsetExample.resource.read(data_id = eset_ex.data_id)[0]

    eset_ex_read.eset_epure # -> {}
    eset_ex_read.eset_epure.load() # (2)!
    eset_ex_read.eset_epure # -> {<pyt1.tests.resource...0D4245C00>, <pyt1.tests.resource...0D4245CC0>}

    eset_ex_read.eset_str # -> {}
    eset_ex_read.eset_str.load()
    "".join(eset_ex_read.eset_str) # -> "Grin cat like a Cheshire"

def test_non_epure_cls_w_eset():

    some_eset = Eset[str](["meow", "woof"])
    some_eset.save()

    class NotEpure:
        eset_str:Eset[str] = Eset[str](["chop", "sueye"])

    ins = NotEpure()

    ins.eset_str.save()


def test_eset_object_type_json():

    class Customer:
        name:str
        adress:str

        def __init__(self, name, adress):
            self.name = name
            self.adress = adress

    customer_1 = Customer("Sion Mccall", "Heathfield Road, 30")
    customer_2 = Customer("Darcy Montes", "Ash Street, 13")
    customer_3 = Customer("Isaiah Hughes", "Grasmere Avenue, 19")
    customer_4 = Customer("Jodie Sandoval", " Meadow Rise, 15")
    customer_50 = Customer("Emily Mahoney", "Park Road, 62")
    customer_51 = Customer("Inaaya Hodge", "Rectory Lane, 42")
    customer_52 = Customer("Blanche Colon", "Ferndale Road, 10")
    customer_54 = Customer("Lucia Davenport", "Warwick Street, 56")
    customer_55 = Customer("Vivian Lin", "Carlton Road, 23")
    customer_56 = Customer("Kane Flores", "Beaufort Road, 87")
        
    @epure()
    class ShipmentCompany:
        customers_set:Eset[object] = Eset[object]([customer_1, customer_2, customer_3])

    data_id = ShipmentCompany().save().data_id

    company_res = ShipmentCompany.resource.read(data_id=data_id)

    company_res[0].load()

    