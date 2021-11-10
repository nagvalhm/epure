# type: ignore
from os import path, putenv
import pytest
from ..epure.node import *
import sys

def test_node_node_init():
    storage = None
    res = Node(storage)
    assert type(res) == Node


def test_node_sysnode_new():
    ins1 = SysNode()
    ins2 = SysNode()
    assert ins1 is ins2


def node_sysnode_put(path):
    storage=None
    sys_node = SysNode(root = 'config_test')
    
    assert not sys_node.contains(path=path)
    path = sys_node.put(path=path)
    assert sys_node.contains(path=path)

    return path


def node_sysnode_delete(path):
    sys_node = SysNode(root = 'config_test')
    while path != '.':
        assert sys_node.contains(path=path)
        parent = sys_node.delete(path=path)
        assert parent        
        assert ((not sys_node.contains(path=path)) 
            and sys_node.contains(path=parent))
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
    node = FileNode()
    node.dir_name = "dir1/dir2/"
    node.name = "file.txt"
    node.path
    return node


def test_node_sysnode_filenode(file_node):

    sys_node = SysNode(root = 'config_test')
    assert not sys_node.contains(file_node)
    sys_node.put(file_node)
    assert sys_node.contains(file_node)
    sys_node.delete(file_node)
    assert not sys_node.contains(file_node)
    node_sysnode_delete(file_node.dir_name)
    

def test_node_sysnode_filenode_and_path(file_node):

    another_parent = "dir3/dir4/coc/"
    sys_node = SysNode(root = 'config_test')
    assert not sys_node.contains(file_node, path = another_parent)
    sys_node.put(file_node, path = another_parent)
    assert not sys_node.contains(file_node)
    assert sys_node.contains(file_node, path = another_parent)
    sys_node.delete(file_node, path = another_parent)
    assert not sys_node.contains(file_node, path = another_parent)
    node_sysnode_delete(another_parent)


def test_node_sysnode_save():
    sys_node = SysNode(root = 'config_test')
    sys_node.save()