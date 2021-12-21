# type: ignore
from ..epure.node import *
from ..epure import *
import pytest

car_storage = FileNode(name='car.txt').save()
electrocar_storage = FileNode(name='electrocar.txt').save()
wheel_storage = FileNode(name='wheel.txt').save()
door_storage = FileNode(name='door.txt').save()
handle_storage = FileNode(name='handle.txt').save()



@epure(car_storage, ENode)
class Car:
    wheel1 = None
    door1 = None

@epure(electrocar_storage, ENode)
class ElectroCar(Car):
    wheel2 = None
    door2 = None

class Tesla(ElectroCar):
    wheel3 = None
    wheel4 = None
    door3 = None
    door4 = None

@epure(wheel_storage, ENode)
class Wheel():
    robber_color = 'black'

@epure(door_storage, ENode)
class Door():
    glass = 0
    material = 'metal'
    handle = None

@epure(handle_storage, Node)
class Handle:
    color = 4

def test_save():    

    #wheels
    wheel1 = Wheel()
    wheel1.robber_color = 'blue'
    wheel2 = Wheel()
    wheel2.robber_color = 'green'
    wheel3 = Wheel()
    wheel3.robber_color = 'yellow'
    wheel4 = Wheel()
    
    #handles
    handle1 = Handle()
    handle2 = Handle()
    handle3 = Handle()

    #doors
    door1 = Door()
    door1.handle = handle1
    door2 = Door()
    door2.handle = handle2
    door3 = Door()
    door3.handle = handle3
    door4 = Door()

    #car
    car = Car()
    car.wheel1 = wheel1
    car.wheel2 = wheel2
    car.wheel3 = wheel3
    car.wheel4 = wheel4

    
    car.door1 = door1
    car.door2 = door2
    car.door3 = door3
    car.door4 = door4
    car.save()

    #tesla
    tesla = Tesla()
    tesla.wheel1 = wheel1
    tesla.wheel2 = wheel2
    tesla.wheel3 = wheel3
    tesla.wheel4 = wheel4

    
    tesla.door1 = door1
    tesla.door2 = door2
    tesla.door3 = door3
    tesla.door4 = door4
    tesla.save()

    # assert_contains(car, tesla)


def assert_contains(car, tesla):
    assert car_storage.contains(car)
    assert electrocar_storage.contains(tesla)

    assert wheel_storage.contains(car.wheel1)
    assert wheel_storage.contains(car.wheel2)
    assert wheel_storage.contains(car.wheel3)
    assert wheel_storage.contains(car.wheel4)

    assert door_storage.contains(car.door1)
    assert door_storage.contains(car.door2)
    assert door_storage.contains(car.door3)
    assert door_storage.contains(car.door4)

    assert handle_storage.contains(car.handle1)
    assert handle_storage.contains(car.handle2)
    assert handle_storage.contains(car.handle3)
    assert handle_storage.contains(car.handle4)


def test_del_storages():
    FileNode.root.delete(car_storage)
    assert not FileNode.root.contains(car_storage)

    FileNode.root.delete(electrocar_storage)
    assert not FileNode.root.contains(electrocar_storage)
    
    FileNode.root.delete(wheel_storage)
    assert not FileNode.root.contains(wheel_storage)

    FileNode.root.delete(door_storage)
    assert not FileNode.root.contains(door_storage)

    FileNode.root.delete(handle_storage)
    assert not FileNode.root.contains(handle_storage)