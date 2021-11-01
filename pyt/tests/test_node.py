import pytest
from ..node import *
import sys


def test_node_node_init():
    res = Node()
    assert type(res) == Node