import pytest
from ..node import *
import sys


def test_node_node_init():
    storage=[1,2,3]
    res = Node(storage)
    assert type(res) == Node