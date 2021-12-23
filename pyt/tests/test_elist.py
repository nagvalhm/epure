# type: ignore
from ..epure.node import *
import pytest
from .test_enode import *


link_storage = FileNode('links.txt')
list_storage = FileNode('lists.txt')

def test_elist_nodelist_save():
    list1 = EList(storage=list_storage)
    list2 = NodeList(link_storage, storage=list_storage)

    node1 = Car()
    node2 = Wheel()
    node3 = Door()
    str1 = 'str1'
    num1 = 4
    
    list1.append(node1)
    list1.append(node2)
    list1.append(node3)
    list1.append(str1)
    list1.append(num1)

    list2.append(node1)
    list2.append(node2)
    list2.append(node3)

    with pytest.raises(TypeError):
        list2.append(str1)
        list2.append(num1)

    list1.save()
    list2.save()

    res1 = list1.storage.search([list1.node_id])[0]
    res2 = list2.storage.search([list2.node_id])[0]
    assert res1
    assert res2
    res1, res2, res3 = link_storage.search([node1.node_id])[0], \
                        link_storage.search([node2.node_id])[0], \
                        link_storage.search([node3.node_id])[0]
    assert type(res1) == Car
    assert type(res2) == Wheel
    assert type(res3) == Door
    

def test_del_storages():
    FileNode.root.delete(link_storage)
    assert not FileNode.root.contains(link_storage)

    FileNode.root.delete(list_storage)
    assert not FileNode.root.contains(list_storage)
