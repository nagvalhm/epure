from uuid import UUID
from ..savable import Savable
from ..resource import Resource
from ...errors import ResourceException
from typing import Any, Dict

class Node(Savable):

    node_id:object
    __exclude__:list

    def __init__(self, node_id:object=None, resource:Resource=None) -> None:
        if node_id != None:
            self.node_id = node_id
        super().__init__(resource)

    @classmethod
    def from_dict(_cls, _dict:Dict[str, Any])->object:
        raise NotImplementedError

    def save(self, asynch:bool=False):
        if not hasattr(self, 'resource'):
            raise ResourceException('Unable save Savable, resource not found')
        resource = self.resource
        
        
        if hasattr(self, 'node_id') and self.node_id:
            res = resource.update(self, asynch)
            return res
        else:
            res = resource.create(self, asynch)
            return res


class TableNode(Node):
    db:Resource
    node_id: UUID
    resource:Savable

    def __init__(self, node_id:object=None, resource:Resource=None) -> None:
        if node_id != None and isinstance(node_id, str):
            node_id = UUID(node_id)
        super().__init__(node_id, resource)

    @property
    def table(self) -> Savable:
        return self.resource

    @classmethod
    def from_dict_deep(_cls, _dict:Dict[str, Any])->object:

        # instance = _cls.__call__()
        instance = _cls()
        
        for field_name, val in _dict.items():
            if field_name in instance.annotations:
                _type = instance.annotations[field_name]
                if isinstance(_type, Savable):
                    val = _type(val)
                setattr(instance, field_name, val)


        return instance
    
    @classmethod
    def from_dict(_cls, _dict:Dict[str, Any])->object:

        # instance = _cls.__call__()
        instance = _cls()
        
        for field_name, val in _dict.items():
            if field_name in instance.annotations:
                setattr(instance, field_name, val)


        return instance

    __exclude__:list = Node.__exclude__ + ['table', 'db']