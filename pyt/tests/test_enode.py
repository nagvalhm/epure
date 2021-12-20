# type: ignore
from ..epure.node import *
from ..epure import *

car_storage = FileNode(name='car.txt').save()
wheel_storage = FileNode(name='wheel.txt').save()
door_storage = FileNode(name='door.txt').save()

# @epure(ENode, FileNode(name='car_storage.txt'))
class Car:
    pass

class ElectroCar(Car):
    pass

class Tesla(ElectroCar):
    pass

# @epure(ENode, FileNode(name='Wheel.txt'))
class Wheel():
    pass

# @epure(ENode, FileNode(name='Wheel.txt'))
class Door():
    pass

def test_del_storages():
    FileNode.root.delete(car_storage)
    assert not FileNode.root.contains(car_storage)
    FileNode.root.delete(wheel_storage)
    assert not FileNode.root.contains(wheel_storage)
    FileNode.root.delete(door_storage)
    assert not FileNode.root.contains(door_storage)