# type: ignore
import pytest
from ..epure.node.node import Node
from ..epure.node.postgress_node import PostgressNode

class Car:
    whie = 'black'


class test2:
    test2_field1 = 5



class test_cls(Car, Node):
    __exclude__ = ['test_field5']
    test_field1 = str
    test_field2 = 'hi'
    test_field3 = None
    test_field4 = test2()
    test_field5 = str

@pytest.fixture
def table_node():
    node = Node("test_cls")
    node.__dict__ = dict(test_cls.__dict__)
    node._name = "test_cls"
    
    return node

@pytest.fixture
def table(table_node):
    db = PostgressNode("localhost", "5432", "postgres", "postgres", "postgres")
    tbl = db.put(table_node)
    return tbl


def test_insert_select(table):
    in_node = test_cls()
    # id = table.put(in_node)
    # out_node = table.search(id=id)
    # assert in_node.test_field2 == out_node.test_field2