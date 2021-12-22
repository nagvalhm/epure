# type: ignore
from pyt.epure.ecommand.file_command import FileCommand
from ..epure.node import *
from .test_sysnode import node_sysnode_delete
from ..epure.ecommand import *


def test_serach_command():
    storage = FileNode().save()
    node1 = ENode()
    node1.name = 'node1'
    node1.size = 4

    node2 = Node()
    node2.name = 'node2'

    storage.put(node1)
    storage.put(node2)
    

    # def foo(node): node.name == 'node1' and node1.size == 4
    # lambda node: node.name == 'node1' and node1.size == 4

    search_command = FileCommand(lambda node: node._name == 'node1' and node1.size == 4)
    res = search_command(storage)
    assert node1 == res[0]
    node_sysnode_delete(storage)