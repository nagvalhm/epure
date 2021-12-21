# type: ignore

from ..epure import ECommand
import pytest

@pytest.fixture
def command():
    foo = lambda x: True
    return ECommand(foo)

def test_ecommand_script(command):    
    assert str(command) == "it's script for something"

def test_ecommand_execute(command):    
    assert command() == None
    