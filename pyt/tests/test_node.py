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