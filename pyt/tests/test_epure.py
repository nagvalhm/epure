# type: ignore

import pytest
from ..epure import *
import subprocess

@pytest.fixture
def cap_cls():
    class Cap:    
        ___cap_field___ = '___cap_field_val'
        __cap_field__ = '__cap_field_val'
        field = 'asdf'
        def search(self):
            pass
    return Cap

@pytest.fixture
def shaker_cls(cap_cls):

    class Shaker(cap_cls):
        ___shaker_field___ = '___shaker_field_val'
        __shaker_field__ = '__shaker_field_val'

        def search(self):
            print('Shaker search method')

    return Shaker

def test_raises_second_inherit_error():
    @epure()
    class Cap:
        pass

    with pytest.raises(TypeError):
        @epure()
        class Shaker(Cap):
            pass



#epure_constructed
@pytest.fixture
def epure_constructed(capsys, shaker_cls, cap_cls):

    # res = Epure(cap_cls, Node)
    res = Epure(cap_cls.__name__, cap_cls.__bases__, cap_cls.__dict__, cls=cap_cls, node_cls=Node)
    assert type(res) == Epure

    res = Epure(shaker_cls.__name__, shaker_cls.__bases__, shaker_cls.__dict__, cls=shaker_cls, node_cls=Node)
    captured = capsys.readouterr()
    assert_epure_msg(captured.out, shaker_cls)
    assert type(res) == Epure
    class EpureInhirit(res):
        pass
    return res


def assert_epure_msg(captured_out, Shaker):
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



@pytest.fixture
def epure_decorated(capsys, shaker_cls):

    node_cls = Node

    Shaker = epure(node_cls, 'storage')(shaker_cls)    
    
    captured = capsys.readouterr()
    assert_epure_msg(captured.out, shaker_cls)
    assert type(Shaker) == Epure
    assert issubclass(Shaker, node_cls)
    entity = Shaker()
    entity.search()
    captured = capsys.readouterr()
    assert 'Shaker search method' in captured.out
    return Shaker

def test_setattr_decorated(epure_decorated, capsys):
    assert_setattr_msg(epure_decorated, capsys)




def examine_shell_cmd(cmd):
    return not subprocess.call(cmd.split())

def test_typing():
    assert examine_shell_cmd("pyt/env39/Scripts/python.exe -m mypy pyt/epure")