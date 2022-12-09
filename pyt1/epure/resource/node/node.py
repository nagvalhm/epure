from uuid import UUID
from ..savable import Savable
from ..resource import Resource
from ...errors import ResourceException

class Node(Savable):

    node_id:object
    __exclude__:list

    def __init__(self, node_id:object=None, name: str = '', namespace: str = '', resource:Resource=None) -> None:
        if node_id != None:
            self.node_id = node_id
        super().__init__(name, namespace, resource)

    def save(self, asynch:bool=False):
        if not hasattr(self, 'resource'):
            raise ResourceException('Unable save Savable, resource not found')
        resource = self.resource
        
        
        if hasattr(self, 'node_id') and  self.node_id:
            res = resource.update(self, asynch)
            return res
        else:
            res = resource.create(self, asynch)
            return res


class TableNode(Node):
    db:Resource
    node_id: UUID
    resource:Savable

    def __init__(self, node_id:object=None, name: str = '', namespace: str = '', resource:Resource=None) -> None:
        if node_id != None and isinstance(node_id, str):
            node_id = UUID(node_id)
        super().__init__(node_id, name, namespace, resource)

    @property
    def table(self) -> Savable:
        return self.resource

    __exclude__:list = Node.__exclude__ + ['table', 'db']

