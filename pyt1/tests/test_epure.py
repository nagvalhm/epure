from __future__ import annotations
from ..epure.epure import epure, connect
from typing import List, Dict
from datetime import datetime
import pytest
import types
from .epure_classes import *

def get_epure(cls):
    epure = cls()
    id = epure.save()
    res = epure.table.read(id=id)
    assert res == epure
    return res

def table_exists():
    pass


@pytest.fixture
def default_epure():
    return get_epure(DefaultEpure)

# def test_default_epure_table(default_epure):
#     assert default_epure.table.name == 'default_epure'
#     assert default_epure.db.name == 'GresDb'
#     assert table_exists('default_epure')

# def test_default_epure_fields(default_epure):
#     pass


# def test_default_epure_fields_in_correct_tables():
#     pass

# @pytest.fixture
# def aliased_epure():
#     return get_epure(AliasedEpure)

# def test_aliased_epure_fields(aliased_epure):
#     pass

# def test_aliased_epure_table(aliased_epure):
#     assert aliased_epure.table.name == 'prefix.aliasedtable'
#     assert default_epure.db.name == 'GresDb'
#     assert table_exists('prefix.aliasedtable')

# def test_aliased_epure_fields_in_correct_tables():
#     pass

# @pytest.fixture
# def custom_save_epure():
#     epure = CustomSaveEpure()
#     id = epure.save()
#     assert id == 65
#     res = epure.table.read(id=id)   
#     return res

# def test_custom_save_fields(custom_save_epure):
#     pass

# def test_custom_save_table(custom_save_epure):
#     assert custom_save_epure.table.name == 'prefix.aliasedtable'
#     assert default_epure.db.name == 'GresDb'
#     assert table_exists('prefix.aliasedtable')

# def test_custom_save_fields_in_correct_tables():
#     pass



# #test exceptions
# def test_not_null_column_not_accept_null():
#     pass

# def test_not_typed_fields_not_saved():
#     pass

# def test_excluded_fields_not_saved():
#     pass