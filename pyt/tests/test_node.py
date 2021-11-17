# type: ignore
from ..epure.node import *
import pytest

@pytest.fixture
def node_name():
    storage = None
    res = Node(storage)
    res.name = 'code'
    return res.name

def test_node_name(node_name):
    assert node_name == 'code'

@pytest.fixture
def node_name_none():
    storage = None
    res = Node(storage)
    res.name = None
    return res.name

def test_node_name_none(node_name_none):
    assert node_name_none == 'node'

def test_to_json_and_from_json(capsys):
    res = Node()
    res.inner_node = Node()
    res.tuple = ('ad', 'asd', 13)
    res.inner_node.typle = ({1:'king theoden'},{2:'gendalf the grey'})
    res.inner_node.greet = 'hi'
    new_res = res.to_json()
    captured_json = capsys.readouterr()
    # assert {"py/object": "pyt.epure.node.node.Node"}.items() => captured_json.items()
    new_res = Node.from_json(new_res)
    assert res == new_res
