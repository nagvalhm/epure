# type: ignore
from ..epure.node import *
import pytest
from .test_sysnode import node_sysnode_delete

@pytest.fixture
def sysnode() -> SysNode:
    return SysNode(root = 'config_test')

def node_filenode_init(sysnode, **kwargs):
    res = FileNode(**kwargs)
    assert sysnode.contains(res)
    node_sysnode_delete(res.path)
    assert not sysnode.contains(res)

def test_node_filenode_init(sysnode: SysNode):
    node_filenode_init(sysnode)
    node_filenode_init(sysnode, name='file2', dir_name='folder1')
    node_filenode_init(sysnode, dir_name='folder1')
    node_filenode_init(sysnode, name='file2')


def test_filenode_dir_name_and_name_none(sysnode):
    res = FileNode()

    with pytest.raises(AttributeError):
        res.name = 'name'
    with pytest.raises(AttributeError):
        res.dir_name = 'dir'
    # assert res.dir_name == 'dir/'
    # assert res.path == 'dir/file_node'
    node_sysnode_delete(res.path)
    assert not sysnode.contains(res)



# def test_filenode_put(capsys):
#     res = FileNode(dir_name='dir/', name='jsonfile_test')
#     res.inner_node = Node()
#     res.tuple = ['ad', 'asd', 13]
#     res.inner_node.typle.dict = ({},{})
#     res.inner_node.greed = 'hi'
#     res.to_json()
#     captured = capsys.readouterr()
#     assert ' ' in captured.out


    # {"_dir_name": "dir/", "_name": "jsonfile_test", 
    # "inner_node": "<pyt.epure.node.node.Node object at 0x0000020609A89400>"}
    # '{"_dir_name": "\\"dir/\\"", "_name": "\\"jsonfile_test\\"", "inner_node": "{\\"_name\\": \\"null\\", \\"typle\\": \\"[\\\\\\"fast\\\\\\", \\\\\\"long\\\\\\"]\\", \\"greed\\": \\"\\\\\\"hi\\\\\\"\\"}", "tuple": "[\\"ad\\", \\"asd\\", 13]"}'