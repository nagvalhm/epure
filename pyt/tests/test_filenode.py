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


# @pytest.fixture
# def filenode_put():
#     res = FileNode('dir/', 'jsonfile_test')
#     res.path
#     res.put()
#     super(res).put
#     assert

# def test_filenode_put(filenode_put):
