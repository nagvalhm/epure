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
    sys_node = SysNode()
    
    assert not sys_node.contains(path=path)
    path = sys_node.put(path=path)
    assert sys_node.contains(path=path)

    return path


def node_sysnode_delete(path):
    sys_node = SysNode()
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
    Node.path = property(lambda self: os.path.join(self.dir_name, self.file_name))
    node = Node()
    node.dir_name = "dir1/dir2/"
    node.file_name = "file.txt"    
    return node

def test_node_sysnode_filenode(file_node):

    sys_node = SysNode()
    assert not sys_node.contains(file_node)
    sys_node.put(file_node)
    assert sys_node.contains(file_node)
    sys_node.delete(file_node)
    assert not sys_node.contains(file_node)
    node_sysnode_delete(file_node.dir_name)
    del Node.path

def test_node_sysnode_filenode_and_path(file_node):

    another_parent = "dir3/dir4/coc/"
    sys_node = SysNode()
    assert not sys_node.contains(file_node, another_parent)
    sys_node.put(file_node, another_parent)
    assert not sys_node.contains(file_node)
    assert sys_node.contains(file_node, another_parent)
    sys_node.delete(file_node, another_parent)
    assert not sys_node.contains(file_node, another_parent)
    node_sysnode_delete(another_parent)
    del Node.path
    

def test_node_sysnode_save():
    sys_node = SysNode()
    sys_node.save()