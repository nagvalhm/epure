# type: ignore
from os import path, putenv
import pytest
from ..epure.node import *
import sys
from ..epure.node.dirnode import dirnode 

def test_node_node_init():
    storage = None
    res = Node(storage)
    assert type(res) == Node


def test_node_dirnode_new():
    ins1 = dirnode
    ins2 = dirnode
    assert ins1 is ins2


def node_dirnode_put(path):
    storage=None
    dir_node = dirnode
    
    assert not dir_node.contains(path=path)
    path = dir_node.put(path=path)
    assert dir_node.contains(path=path)

    return path


def node_dirnode_delete(path):
    dir_node = dirnode
    while path != '.':
        assert dir_node.contains(path=path)
        parent = dir_node.delete(path=path)
        assert parent        
        assert ((not dir_node.contains(path=path)) 
            and dir_node.contains(path=parent))
        path = parent
       
    
def test_node_dirnode_delete():
    file_path = node_dirnode_put("dir1/dir2/file.txt")
    dir_path = node_dirnode_put("dir3/dir4/coc/")

    node_dirnode_delete(file_path)
    node_dirnode_delete(dir_path)

    file_path = node_dirnode_put("dir1/dir2/file.txt")
    node_dirnode_delete("dir1")
    file_path = node_dirnode_put("dir1/dir2/file.txt")
    node_dirnode_delete("dir1/")


@pytest.fixture
def file_node():
    node = FileNode(name = "file.txt", dir_name = "dir1/dir2/", save=False)
    return node


def test_node_dirnode_filenode(file_node):

    dir_node = dirnode
    assert not dir_node.contains(file_node)
    dir_node.put(file_node)
    assert dir_node.contains(file_node)
    dir_node.delete(file_node)
    assert not dir_node.contains(file_node)
    node_dirnode_delete(file_node.dir_name)
    

def test_node_dirnode_filenode_and_path(file_node):

    another_parent = "dir3/dir4/coc/"
    dir_node = dirnode
    assert not dir_node.contains(file_node, path = another_parent)
    dir_node.put(file_node, path = another_parent)
    assert not dir_node.contains(file_node)
    assert dir_node.contains(file_node, path = another_parent)
    dir_node.delete(file_node, path = another_parent)
    assert not dir_node.contains(file_node, path = another_parent)
    node_dirnode_delete(another_parent)    


def test_node_dirnode_save():
    dir_node = dirnode
    dir_node.save()