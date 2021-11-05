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

def node_sysnode_put(path):
    sys_node = SysNode()
    
    assert not sys_node.path_exists(path)
    path = sys_node.put(path)
    assert sys_node.path_exists(path)

    return path


def node_sysnode_delete(path):
    sys_node = SysNode()
    while path != '.':
        assert sys_node.path_exists(path)
        parent = sys_node.delete(path)
        assert parent        
        assert ((not sys_node.path_exists(path)) 
            and sys_node.path_exists(parent))
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