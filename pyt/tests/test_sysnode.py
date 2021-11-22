# type: ignore
from os import path, putenv
import pytest
from ..epure.node import *
import sys

sysnode = DirNode.root

def test_node_node_init():
    storage = None
    res = Node(storage)
    assert type(res) == Node


def node_sysnode_put(node):
    assert not sysnode.contains(node)
    path = sysnode.put(node)
    assert sysnode.contains(node)

    return path


def node_sysnode_delete(node):
    while node.path != '.':
        assert sysnode.contains(node)
        parent = sysnode.delete(node)
        assert parent
        assert ((not sysnode.contains(node))
            and sysnode.contains(parent))
        node = parent
       
    
def test_node_sysnode_delete():

    file = node_sysnode_put(FileNode(name="dir1/dir2/file.txt"))
    dir = node_sysnode_put(DirNode(name="dir3/dir4/coc/"))

    node_sysnode_delete(file)
    node_sysnode_delete(dir)

    node_sysnode_put(FileNode(name="dir1/dir2/file.txt"))
    node_sysnode_delete(DirNode(name="dir1"))
    node_sysnode_put(FileNode(name="dir1/dir2/file.txt"))
    node_sysnode_delete(DirNode(name="dir1/"))


@pytest.fixture
def file_node():
    node = FileNode(DirNode("dir1/dir2/"), "file.txt")
    return node


def test_node_sysnode_filenode(file_node):

    assert not sysnode.contains(file_node)
    sysnode.put(file_node)
    assert sysnode.contains(file_node)
    sysnode.delete(file_node)
    assert not sysnode.contains(file_node)
    node_sysnode_delete(file_node.storage.path)
    

def test_node_sysnode_filenode_and_path(file_node):

    another_parent = DirNode(name="dir3/dir4/coc/")
    assert not another_parent.contains(file_node)
    another_parent.put(file_node)
    assert not sysnode.contains(file_node)
    assert another_parent.contains(file_node)
    another_parent.delete(file_node)
    assert not another_parent.contains(file_node)
    node_sysnode_delete(another_parent)    


def test_node_sysnode_save():
    sysnode.save()