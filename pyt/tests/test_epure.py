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

#epure_constructed
@pytest.fixture
def epure_constructed(capsys):    
    res = Epure(Shaker, Make)
    captured = capsys.readouterr()
    assert_epure_msg(captured.out)
    assert type(res) == Epure
    return res


def assert_epure_msg(captured_out):
    instrs = [f'on_setattr Shaker, ___cap_field___, {Shaker.___cap_field___}',        
        f'on_setattr Shaker, ___shaker_field___, {Shaker.___shaker_field___}',]

    notstrs = [f'on_setattr Shaker, __cap_field__, {Shaker.__cap_field__}',        
        f'on_setattr Shaker, __shaker_field__, {Shaker.__shaker_field__}']

    assert all(msg in captured_out for msg in instrs)
    assert all(msg not in captured_out for msg in notstrs)

def test_setattr_constructed(epure_constructed, capsys):
    assert_setattr_msg(epure_constructed, capsys)

def assert_setattr_msg(test_epure, capsys):
    val = '___added_field___val'    
    test_epure.___added_field___ = val    
    captured = capsys.readouterr()    

    instr = f'on_setattr Shaker, ___added_field___, {val}'
    assert instr in captured.out

#epure_decorated
del Shaker

class Shaker(Cap):
    ___shaker_field___ = '___shaker_field_val'
    __shaker_field__ = '__shaker_field_val'

@pytest.fixture
def epure_decorated(capsys):    
    res = epure('storage')(Shaker)
    captured = capsys.readouterr()
    assert_epure_msg(captured.out)
    assert type(res) == Epure
    return res

def test_setattr_decorated(epure_decorated, capsys):
    assert_setattr_msg(epure_decorated, capsys)