# type: ignore
import pytest
from ..epure.proto import *

class Container(Proto):
    ___special_container___ = None

    # def __init__(self, b) -> None:
    #     super().__init__()

class Сow(Proto):
    pass

class Cap(Container):
    not_special_cap:str = None
    not_inited_field:str
    ___special_cap___ = None

    # def __init__(self, b) -> None:
    #     super().__init__(b)

    # def __new__(cls: ProtoMeta, *args: Any, **kwargs: Any) -> Proto:
    #     return super().__new__(*args, **kwargs)

class BarStuf:
    pass

class Shaker(Cap):
    not_special_shaker:str
    ___special_shaker___ = None



    # def __init__(self, b) -> None:
    #     pass# super().__init__(b)



@pytest.fixture
def proto():
    res = Shaker(11)
    return res

def test_proto_new_multiple_inheritance():
    with pytest.raises(MultipleInheritanceError):
        class MilkShaker(Сow, Shaker):
            pass

# def test_proto_inheritance():

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



#####################################################
def test_proto_setattr(proto, capsys):
    proto.___special_container___ = 1
    proto.___special_cap___ = 1
    proto.___special_shaker___ = 1

    captured = capsys.readouterr()
    res = captured.out
    print(res)
    assert f'Container set val for ___special_container___ = 1' in res
    assert f'Cap set val for ___special_cap___ = 1' in res
    assert f'Shaker set val for ___special_shaker___ = 1' in res
    # assert len(res) < 150
    

def test_proto_setattr_error(proto, capsys):
    with pytest.raises(AttributeError):
        proto.___not_exist___ = 123

    
# def test_proto_getattribute_error(proto, capsys):
#     with pytest.raises(AttributeError):
#         a = proto.___not_exist___