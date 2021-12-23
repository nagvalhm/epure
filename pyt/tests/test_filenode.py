# type: ignore
from ..epure.node import *
import pytest
from .test_sysnode import node_sysnode_delete

sysnode = FileNode.root


def node_filenode_init(dir=None, name=None):
    res = FileNode(name, dir)
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
    node_filenode_init(DirNode('folder1/folder2/folder3'))
    #only name
    node_filenode_init(name='file2')
    #both
    node_filenode_init(DirNode('folder1/folder2/folder3'), name='folder4/folder5/file2')    
    node_filenode_init(sysnode, name='file2')


def test_filenode_setter_name_path():
    res = FileNode(storage=sysnode).save()
    
    with pytest.raises(AttributeError):
        res.name = 'file'
    with pytest.raises(AttributeError):
        res.path = 'dir'
    # assert res.dir_name == 'dir/'
    # assert res.path == 'dir/file_node'
    node_sysnode_delete(res)
    assert not sysnode.contains(res)


file1 = FileNode()
file2 = FileNode('file_node2')

def test_filenode_put(capsys):
# def test_filenode_put(capsys,dirnode):

    
    
    node1 = Node()
    node1.innernode = Node()
    node1.innernode.greet = 'hello'
    node1.tuple = ('abc','gg')
    node1.innernode.set = (1,2,3)
    file1.put(node1)

    # file1.put('str1')
    # file1.put(6)

    captured_json = capsys.readouterr()

    
    another_node = Node()
    another_node.save()
    another_node.job = 'javadeveloper'
    file2.put(another_node)

    assert '"tuple": {"py/tuple": ["abc", "gg"]}' in captured_json.out
    assert '"innernode": {"py/object": "pyt.epure.node.node.Node"' in captured_json.out
    assert '"set": {"py/tuple": [1, 2, 3]}' in captured_json.out

    assert sysnode.contains(file1)
    # new_res = res.search(['"tuple": {"py/tuple": ["abc", "gg"]}','"tuple": {"py/tuple": ["abc", "gg"]}'])
    # new_res = res.search(['"job": "javadeveloper"'])
    assert file1.contains(node1)
    # assert res == new_res[0]


def test_del_storages():
    node_sysnode_delete(file1)
    node_sysnode_delete(file2)
    assert not sysnode.contains(file1)


# def test_filenode_singleobj():
#     filenode1 = FileNode('dir1/dir2/dir3/node1')
#     filenode2 = FileNode('node1', DirNode('dir1/dir2/dir3'))
#     assert filenode2 is filenode1