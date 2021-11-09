# type: ignore
import pytest
from ..epure.proto import *

class Cap(Proto):
    not_special_cap:str = None


class Shaker(Cap):
    not_special_shaker:str

@pytest.fixture
def proto():
    return Shaker()

def test_proto_setattr_not_special_attr(proto, capsys):
    proto.a = 1    
    captured = capsys.readouterr()
    res = captured.out
    print(res)
    assert f'a is not special\n' == res
    assert proto.a == 1

def test_proto_getattribute_not_special_attr(proto, capsys):
    a = proto.not_special_cap
    captured = capsys.readouterr()
    assert f'not_special_cap is not special\n' == captured.out

def test_proto_setattr_error(proto, capsys):
    with pytest.raises(AttributeError):
        proto.___not_exist___ = 123

    
def test_proto_getattribute_error(proto, capsys):
    with pytest.raises(AttributeError):
        a = proto.___not_exist___