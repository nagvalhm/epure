from uuid import UUID
from ..savable import Savable
from ..resource import Resource

class Node(Savable):

    __exclude__:list

    def save(self, level:int=0, resource:Resource=None):
        pass


class TableNode(Node):
    db:Resource
    res_id: UUID
    resource:Savable

    @property
    def table(self) -> Savable:
        return self.resource

    __exclude__:list = Node.__exclude__ + ['table', 'db']