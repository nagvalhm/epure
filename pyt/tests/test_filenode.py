# type: ignore
from ..epure.node import *
import pytest
from .test_dirnode import node_dirnode_delete
from ..epure.node.dirnode import dirnode 

# @pytest.fixture
# def dirnode():
# def dirnode() -> dirnode:
    # return dirnode

def node_filenode_init(dirnode,**kwargs):
    res = FileNode(**kwargs)
    assert dirnode.contains(res)
    node_dirnode_delete(res.path)
    assert not dirnode.contains(res)

def test_node_filenode_init():
    node_filenode_init(dirnode)
    node_filenode_init(dirnode, name='file2', dir_name='folder1')
    node_filenode_init(dirnode, dir_name='folder1')
    node_filenode_init(dirnode, name='file2')


def test_filenode_dir_name_and_name_none():
    res = FileNode()

    with pytest.raises(AttributeError):
        res.name = 'name'
    with pytest.raises(AttributeError):
        res.dir_name = 'dir'
    # assert res.dir_name == 'dir/'
    # assert res.path == 'dir/file_node'
    node_dirnode_delete(res.path)
    assert not dirnode.contains(res)

def test_filenode_put(capsys):
# def test_filenode_put(capsys,dirnode):
    res = FileNode()
    res.innernode = Node()
    res.innernode.greet = 'hello'
    res.tuple = ('abc','gg')
    res.innernode.set = (1,2,3)
    res.put()
    captured_json = capsys.readouterr()
    assert '"tuple": {"py/tuple": ["abc", "gg"]}' in captured_json.out
    assert not '"tuple": {"py/tuple": ["not tuple", "ss"]}' in captured_json.out
    assert '"innernode": {"py/object": "pyt.epure.node.node.Node"' in captured_json.out
    assert '"set": {"py/tuple": [1, 2, 3]}' in captured_json.out
    assert dirnode.contains(res)
    node_dirnode_delete(res.path)
    assert not dirnode.contains(res)
    

