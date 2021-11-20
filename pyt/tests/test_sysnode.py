# type: ignore
from os import path, putenv
import pytest
from ..epure.node import *
import sys
from ..epure.node.dirnode import sysnode

def test_node_node_init():
    storage = None
    res = Node(storage)
    assert type(res) == Node


def node_sysnode_put(path):
    assert not sysnode.contains(path=path)
    path = sysnode.put(path=path)
    assert sysnode.contains(path=path)

    return path


def node_sysnode_delete(path):
    while path != '.':
        assert sysnode.contains(path=path)
        parent = sysnode.delete(path=path)
        assert parent        
        assert ((not sysnode.contains(path=path)) 
            and sysnode.contains(path=parent))
        path = parent
       
    
def test_node_sysnode_delete():
    file_path = node_sysnode_put("dir1/dir2/file.txt")
    dir_path = node_sysnode_put("dir3/dir4/coc/")

    node_sysnode_delete(file_path)
    node_sysnode_delete(dir_path)

    file_path = node_sysnode_put("dir1/dir2/file.txt")
    node_sysnode_delete("dir1")
    file_path = node_sysnode_put("dir1/dir2/file.txt")
    node_sysnode_delete("dir1/")


@pytest.fixture
def file_node():
    node = FileNode(name = "file.txt", dir_name = "dir1/dir2/", save=False)
    return node


def test_node_sysnode_filenode(file_node):

    assert not sysnode.contains(file_node)
    sysnode.put(file_node)
    assert sysnode.contains(file_node)
    sysnode.delete(file_node)
    assert not sysnode.contains(file_node)
    node_sysnode_delete(file_node.dir_name)
    

def test_node_sysnode_filenode_and_path(file_node):

    another_parent = "dir3/dir4/coc/"
    assert not sysnode.contains(file_node, path = another_parent)
    sysnode.put(file_node, path = another_parent)
    assert not sysnode.contains(file_node)
    assert sysnode.contains(file_node, path = another_parent)
    sysnode.delete(file_node, path = another_parent)
    assert not sysnode.contains(file_node, path = another_parent)
    node_sysnode_delete(another_parent)    


def test_node_sysnode_save():
    sysnode.save()