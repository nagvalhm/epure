from typing import Generic, TypeVar

from pyt1.epure.resource.savable import Savable

class Table(Savable):
    pass

class TableHeader(Savable):
    pass

class TableColumn(Savable):
    pass

_T = TypeVar('_T')
class NotNull(Generic[_T]):
    pass