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

def test_node_sysnode_put():
    path = "config/text.txt"
    SysNode.put(path)
    assert os.path.exists(path) 
    return SysNode.put