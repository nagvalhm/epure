# type: ignore
from ....epure.storage.file.ini_file import IniFile
import pytest

@pytest.fixture
def config():
    return IniFile('./test_config.ini')

# def test_read_non_section(config):
#     db_host = config.db_host
#     assert db_host == 'localhost'

# def test_read_section(config):
#     db_port = config.general.db_port
#     assert db_port == 5432

# def test_read_nested_section(config):
#     db_user = config.section1.section2.db_user
#     assert db_user == 'user'



# def test_read_not_exist_property(config):
#     # with pytest.raises(AttributeError?keyerror):
#     db_host = config.not_exist_prop
#     assert db_host == None

# def test_read_not_exist_config():
#     # with pytest.raises(AttributeError):
#     config = IniFile('not_exist_config.ini')
#     db_host = config.db_host
#     assert db_host == None