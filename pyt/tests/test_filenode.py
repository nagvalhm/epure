# type: ignore
from ..epure.node import *
import pytest

def test_node_filenode_init():
    res = FileNode()
    assert type(res) == FileNode

@pytest.fixture
def filenode_dir_name_and_name_none():
    storage = None
    dir_name = None
    name = None
    res = FileNode(storage, dir_name, name)
    res.name
    res.dir_name = 'dir'
    res.dir_name
    return res.path

def test_node_filenode_path_none(filenode_dir_name_and_name_none):
    assert filenode_dir_name_and_name_none == 'dir/file_node'
