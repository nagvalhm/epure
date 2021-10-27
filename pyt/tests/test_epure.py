import pytest
from ..epure import *
import sys


class Cap:    
    ___cap_field___ = '___cap_field_val'
    __cap_field__ = '__cap_field_val'
    field = 'asdf'
    def take():
        pass


class Shaker(Cap):
    ___shaker_field___ = '___shaker_field_val'
    __shaker_field__ = '__shaker_field_val'

def test_raise_EpureProtocolException():    
    with pytest.raises(EpureProtocolException):
        res = Epure(Shaker)


@pytest.fixture
def epure_constructed(capsys):    
    res = Epure(Shaker, Make)
    captured = capsys.readouterr()
    assert_epure_msg(captured.out)
    assert type(res) == Epure
    return res

def test_foo(epure_constructed):
    pass

def assert_epure_msg(captured_out):
    instrs = [f'on_setattr Shaker, ___cap_field___, {Shaker.___cap_field___}',        
        f'on_setattr Shaker, ___shaker_field___, {Shaker.___shaker_field___}',]

    notstrs = [f'on_setattr Shaker, __cap_field__, {Shaker.__cap_field__}',        
        f'on_setattr Shaker, __shaker_field__, {Shaker.__shaker_field__}']

    assert all(msg in captured_out for msg in instrs)
    assert all(msg not in captured_out for msg in notstrs)


# class tests_epure(TestCase):

#     def create_epure_decor(self):

#         @epure('stror')
#         class Car():
#             ___a_filed___ = 1

#             def __setattr__(self, name: str, value: Any) -> None:
#                 print('hi5')
#                 return super().__setattr__(name, value)

#             def add(cls, make):
#                 print('add2 is called')

#         assert Car is not None


# @epure('stror')
# class Car():
#     ___a_filed___ = 1

#     def __setattr__(self, name: str, value: Any) -> None:
#         print('hi5')
#         return super().__setattr__(name, value)

#     def add(cls, make):
#         print('add2 is called')


# def test_save_no_ins():
#     a = Car.save(123)

# def test_save_ins():
#     car = Car()
#     car.save()

# test_save_ins()