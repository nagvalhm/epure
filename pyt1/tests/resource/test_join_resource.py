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

TestOrder(nico_id, "2022-03-15", office1_id).save()
TestOrder(victor_id, "2022-03-10", office2_id).save()
TestOrder(nico_id, "2022-03-15", office1_id).save()
TestOrder(tom_id, "2022-03-30", office1_id).save()
TestOrder(john_id, "2022-01-15", office3_id).save()
TestOrder(mike_id, "2022-12-10", office2_id).save()
TestOrder(nico_id, "2022-08-04", office1_id).save()
TestOrder(bob_id, "2022-09-15", office3_id).save()
TestOrder(bob_id, "2022-05-11", office1_id).save()


@escript


def test_two_joins(self):
    tp = self.tp
    dbp = self.dbp
    test_order_tp = dbp.test_order
    test_office_tp = dbp.test_shippment_office

    join_res = tp.join(test_order_tp, tp.node_id == test_order_tp.test_customer_id)

    join_res.join(test_office_tp, test_order_tp.office_id == test_office_tp.node_id)

    lst = ["bde"]

    query = tp.name in ("abc","def") and tp.name in lst
    

    res_header = join_res.read([test_office_tp.adress, tp.name, tp, test_order_tp, tp.country], test_office_tp.adress == "Washington str.")

    res_no_header = join_res.read(test_office_tp.adress == "Washington str.")

    res_empty = join_res.read()

    return query


TestCustomer.test_join = test_two_joins

res = nico.test_join()
assert res