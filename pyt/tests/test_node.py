from os import path, putenv
import pytest
from ..node import *
import sys

def test_node_node_init():
    storage = None
    res = Node(storage)
    assert type(res) == Node

def test_node_sysnode_new():
    ins1 = SysNode()
    ins2 = SysNode()
    assert ins1 is ins2

@pytest.fixture
def file_created():
    path = "pack/text/coc"
    SysNode.put(path)
    return SysNode.put(path)

def test_node_sysnode_put_and_del(file_created):
    assert os.path.exists(file_created)
    SysNode.delete(file_created) 
    assert not os.path.exists(file_created)
    
