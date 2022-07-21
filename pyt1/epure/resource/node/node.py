from uuid import UUID
from ..savable import Savable
from ..resource import Resource, UPDATE, CREATE
from ...errors import ResourceException

class Node(Savable):

    node_id:object
    __exclude__:list

    def save(self, cache:bool=False):
        if not hasattr(self, 'resource'):
            raise ResourceException('Unable save Savable, resource not found')
        resource = self.resource
        method = ''
        if hasattr(self, 'node_id') and  self.node_id:
            method = UPDATE
        else:
            method = CREATE
            self.node_id = resource.generate_id()

        if cache:
            return resource.cache(self, method)
        
        if method == UPDATE:
            return resource.update(self)
        return resource.create(self)


class TableNode(Node):
    db:Resource
    node_id: UUID
    resource:Savable

    @property
    def table(self) -> Savable:
        return self.resource

    __exclude__:list = Node.__exclude__ + ['table', 'db']

