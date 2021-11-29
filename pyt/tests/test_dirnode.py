# type: ignore
from ..epure import *
import pytest

def test_node_filenode_setter():

    with pytest.raises(AttributeError):
        res = DirNode(name="dir1/dir2/dir3")
        res.storage = 'storage'
    
def node_filenode_getter():

    res = FileNode()
    res.storage
    
# def test_node_filenode_getter(node_filenode_getter):
    

    