from epure import *

@epure('stror')
class Car():
    ___a_filed___ = 1

    def __setattr__(self, name: str, value: Any) -> None:
        print('hi5')
        return super().__setattr__(name, value)

    def add(cls, make):
        print('add2 is called')

Car.a_filed = 3
print(Car._storage)

Car.add(123)