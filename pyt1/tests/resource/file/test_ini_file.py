from ....epure.files import IniFile
import pytest
from ...helper import strict_eq

@pytest.fixture
def config():
    return IniFile('./pyt1/tests/test_config.ini')

def test_read_virtual_section(config):
    db_host = config.db_host
    assert strict_eq(db_host, 'localhost')

def test_read_section(config):
    db_port = config.general.db_port
    assert strict_eq(db_port, 5432)

def test_read_nested_section(config):
    db_user = config.section1.section2.db_user
    an_db_user = config.section1.db_port
    assert strict_eq(db_user, 'user')

    pi_begins = config.section1.section2.section3.pi_begins
    assert strict_eq(pi_begins, 3.14159265359)

    asshole = config.epure.best.app.forever.asshole
    assert strict_eq(asshole, True)


def test_read_not_exist_property(config):
    db_host = config.not_exist_prop
    assert db_host == None

def test_read_not_exist_config():
    with pytest.raises(FileNotFoundError):
        config = IniFile('not_exist_config.ini')
        db_host = config.db_host
        assert db_host == None