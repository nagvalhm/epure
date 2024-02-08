import pytest
from ...epure.epure import escript, epure
from uuid import UUID

@epure()
class TestCustomer:
    name:str
    country:str

    def __init__(self, name:str, country:str) -> None:
        self.name = name
        self.country = country

nico = TestCustomer("Nicolas", "Argentina").save()
nico_id = nico.save()
victor_id = TestCustomer("Victor", "USA").save()
tom_id = TestCustomer("Tom", "Japan").save()
john_id = TestCustomer("John", "Laos").save()
mike_id = TestCustomer("Mike", "Monaco").save()
bob_id = TestCustomer("Bob", "Netherlands").save()

@epure()
class TestShippmentOffice:
    adress:str

    def __init__(self, adress) -> None:
        self.adress = adress

office1_id = TestShippmentOffice("Washington str.").save()
office2_id = TestShippmentOffice("Elm str.").save()
office3_id = TestShippmentOffice("Kole str.").save()

@epure()
class TestOrder:
    test_customer_id:UUID
    order_date:str #datetime type maybe
    office_id:UUID

    def __init__(self, test_customer_id, order_date, office_id) -> None:
        self.test_customer_id = test_customer_id
        self.order_date = order_date
        self.office_id = office_id

    # @escript
    # def abc(self):
    #     return 1+1

TestOrder(nico_id, "2022-03-15", office1_id).save()
TestOrder(victor_id, "2022-03-10", office2_id).save()
TestOrder(nico_id, "2022-03-15", office1_id).save()
TestOrder(tom_id, "2022-03-30", office1_id).save()
TestOrder(john_id, "2022-01-15", office3_id).save()
TestOrder(mike_id, "2022-12-10", office2_id).save()
TestOrder(nico_id, "2022-08-04", office1_id).save()
TestOrder(bob_id, "2022-09-15", office3_id).save()
TestOrder(bob_id, "2022-05-11", office1_id).save()



# TestOrder(bob_id, "2022-05-11", office1_id).abc()

# TestOrder(bob_id, "2022-05-11", office1_id).abc()

def foo(foo):
    return foo

def foo2():
    return "adv"

@escript
def test_two_joins(self):
    model = self.md
    domain = self.dom
    test_order_tp = domain.test_order
    test_office_tp = domain.test_shippment_office
    model = self.md
    domain = self.dom
    test_order_tp = domain.test_order
    test_office_tp = domain.test_shippment_office
    lst = ["bde"]
    
    join_res = model.join(test_order_tp, model.data_id == test_order_tp.test_customer_id)

    join_res = join_res.join(test_office_tp, test_order_tp.office_id == test_office_tp.data_id)

    lst = ["bde"]

    query = model.name in ("abc","def") and model.name in lst
    

    res_header = join_res.read([test_office_tp.adress, model.name, model, test_order_tp, model.country], test_office_tp.adress == "Washington str.") # header

    # res_header = join_res.read([md.country], test_office_tp.adress == "Washington str.") # header country

    res_no_header = join_res.read(test_office_tp.adress == "Washington str.") # no header

    res_empty = join_res.read() # no header no on_clause

    return res_header


TestCustomer.test_join = test_two_joins

res = nico.test_join()    

assert res