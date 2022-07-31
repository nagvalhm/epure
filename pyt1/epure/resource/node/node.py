from uuid import UUID
from ..savable import Savable
from ..resource import Resource
from ...errors import ResourceException

class Node(Savable):

    node_id:object
    __exclude__:list

    def save(self, asynch:bool=False):
        if not hasattr(self, 'resource'):
            raise ResourceException('Unable save Savable, resource not found')
        resource = self.resource
        

        if hasattr(self, 'node_id') and  self.node_id:
            return resource.update(self, asynch)
        else:            
            self.node_id = resource.generate_id()
            return resource.create(self, asynch)



class TableNode(Node):
    db:Resource
    node_id: UUID
    resource:Savable

    @property
    def table(self) -> Savable:
        return self.resource

    __exclude__:list = Node.__exclude__ + ['table', 'db']

