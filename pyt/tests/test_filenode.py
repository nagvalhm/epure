# type: ignore
from ..epure.node import *
import pytest
from .test_sysnode import node_sysnode_delete

sysnode = DirNode.root
# @pytest.fixture
# def dirnode():
# def dirnode() -> dirnode:
    # return dirnode

def node_filenode_init(dir=None, name=None):
    res = FileNode(dir,name)
    if not dir:
        assert not sysnode.contains(res)
        return
    res.save()
    assert dir.contains(res)
    node_sysnode_delete(res)
    assert not dir.contains(res)

def test_node_filenode_init():
    #nothing
    node_filenode_init()
    #only dir
    node_filenode_init(sysnode)
    node_filenode_init(DirNode(name='folder1/folder2/folder3'))
    #only name
    node_filenode_init(name='file2')
    #both
    node_filenode_init(DirNode(name='folder1/folder2/folder3'), name='folder4/folder5/file2')    
    node_filenode_init(sysnode, name='file2')


def test_filenode_setter_name_path():
    res = FileNode(sysnode).save()
    
    with pytest.raises(AttributeError):
        res.name = 'file'
    with pytest.raises(AttributeError):
        res.path = 'dir'
    # assert res.dir_name == 'dir/'
    # assert res.path == 'dir/file_node'
    node_sysnode_delete(res)
    assert not sysnode.contains(res)

def test_filenode_put(capsys):
# def test_filenode_put(capsys,dirnode):
    res = FileNode()
    with pytest.raises(FileNotFoundError):
        res.put(res)
    res.save()
    res.innernode = Node()
    res.innernode.greet = 'hello'
    res.tuple = ('abc','gg')
    res.innernode.set = (1,2,3)
    res.put(res)
    captured_json = capsys.readouterr()
    assert '"tuple": {"py/tuple": ["abc", "gg"]}' in captured_json.out
    assert '"innernode": {"py/object": "pyt.epure.node.node.Node"' in captured_json.out
    assert '"set": {"py/tuple": [1, 2, 3]}' in captured_json.out
    assert sysnode.contains(res)
    node_sysnode_delete(res)
    assert not sysnode.contains(res)

# def 