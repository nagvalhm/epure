from epure import *

def create_epure_decor():
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

@epure('stror')
class Car():
    ___a_filed___ = 1

    def __setattr__(self, name: str, value: Any) -> None:
        print('hi5')
        return super().__setattr__(name, value)

    def add(cls, make):
        print('add2 is called')


def test_save_no_ins():
    a = Car.save(123)

def test_save_ins():
    car = Car()
    car.save()

test_save_ins()