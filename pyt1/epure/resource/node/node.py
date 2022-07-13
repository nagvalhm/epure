from uuid import UUID
from ..savable import Savable
from ..resource import Resource, UPDATE, CREATE
from ...errors import ResourceException

class Node(Savable):

    __exclude__:list

    def save(self, cache:bool=False):
        if not hasattr(self, 'resource'):
            raise ResourceException('Unable save Savable, resource not found')

        method = UPDATE if self.is_saved else CREATE
        if cache:
            return self.resource.cache(self, method)
        
        if self.is_saved:
            return self.resource.update(self)
        return self.resource.create(self)


class TableNode(Node):
    db:Resource
    res_id: UUID
    resource:Savable

    @property
    def table(self) -> Savable:
        return self.resource

    __exclude__:list = Node.__exclude__ + ['table', 'db']

