import pytest
from ..node import *
import sys


def test_node_node_init():
    storage = None
    res = Node(storage)
    assert type(res) == Node

def test_node_sysnode_new():
    ins1 = SysNode.__new__
    ins2 = SysNode.__new__
    assert ins1 == ins2