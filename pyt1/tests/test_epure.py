from __future__ import annotations
from ..epure.epure import epure, connect
from typing import List, Dict
from datetime import datetime
import pytest


@epure()
class User:
    pass


class Note:
    count = 7
    note_name:str = 'note'
    parent:Note
    owner:User
    students:List[User]
    access:Dict[User,int]

@epure()
class Result:
    student:User
    course:Course
    datetime:datetime
    score:int

    def save(self):
        res = self.db.execute('select 65')
        return res

@epure()
class Card(Note):
    passed:bool
    color:str

@epure('dbt.akkl.cris')
class Course:
    notes:List[Note]
    results:List[Result]

    def __uniq__(self):
        return [(), ()]

#parent
class ParentClass1:
    pass

class ParentClass2(ParentClass1):
    pass

class ParentClass3(ParentClass1):
    pass

#inner
@epure()
class InnerNested1:
    pass

class InnerNested2:
    inner_class:InnerNested1

class InnerNested3:
    inner_class:InnerNested2

#outer
@epure()
class OuterNested1:
    pass

@epure()
class OuterNested2:
    outer_epure:OuterNested1

@epure()
class OuterNested3:
    outer_epure:OuterNested2

#epures
@epure()
class DefaultEpure:
    pass

@epure('CustomTable')
class NamedEpure:
    pass

@epure()
class CustomSaveEpure:
    pass

@pytest.fixture
def default_epure():
    card = Card()
    id = card.save()
    retrieved_course = card.table.search(id=id)
    assert retrieved_course == card
    assert card.note_name == 'note'
    assert card.table.name == 'card'

@pytest.fixture
def named_epure():
    course = Course()
    course.count = 15
    id = course.save()
    retrieved_course = course.table.search(id=id)
    assert retrieved_course == course
    assert retrieved_course.count == 15
    assert course.table.name == 'dbt.akkl.cris'

@pytest.fixture
def custom_save_epure():
    result = Result()
    id = result.save()
    assert result.db.name == 'GresDb'
    assert id == 65

# def test_hirahical_save_is_correct():
#     pass