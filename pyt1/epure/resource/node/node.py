from uuid import UUID
from ..savable import Savable
from ..resource import Resource
from ...errors import ResourceException
from typing import Any, Dict
import jsonpickle
from ..db.constraint import Constraint
from ...errors import EpureError

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

            if not field_name in instance.annotations:
                continue

            cls_attr_type = instance.annotations[field_name]
            
            val_type_match_cls_attr_type = isinstance(val, cls_attr_type)

            if field_name == "node_id" and not isinstance(val, UUID):
                val = UUID(val)
                val_type_match_cls_attr_type = True

            if issubclass(cls_attr_type, Savable) and not val_type_match_cls_attr_type: # check if attr is epure
                val = UUID(val)
                val_type_match_cls_attr_type = True
            
            if val is None:
                val_type_match_cls_attr_type = True

            if isinstance(val, str) and cls_attr_type in (bytes, bytearray): # bytearray is yet to be tested !
                val = cls_attr_type(val.encode())
                val_type_match_cls_attr_type = True

            if val_type_match_cls_attr_type:
                setattr(instance, field_name, val)
            else:
                raise TypeError(f'Value for field "{field_name}" with value "{val}" of type "{type(val)}" does not match expected attr type of class '\
                                 f'"{_cls}" with value name "{field_name}" and type of attr "{cls_attr_type}"')


        return instance
    
    # def to_json(self) -> str:
    #     from ..db.table import NodePromise
    #     res = {}
    #     for field_name, field_type in self.annotations.items():
    #         if isinstance(field_type, Constraint):
    #             field_type = field_type.py_type
                
    #         if self.is_excluded(field_name, field_type):
    #             continue
    #         if field_name not in self.table.header:
    #             continue
    #         if not hasattr(self, field_name):
    #             continue

    #         field_val = getattr(self, field_name, None)

    #         if isinstance(field_val, NodePromise):
    #             field_val = getattr(field_val, 'node_id', None)
    #             # field_val = getattr(field_val, 'none2', None)

    #         #working for db:
    #         if field_val and isinstance(field_type, Savable)\
    #         and not isinstance(field_val, UUID):
    #             field_val = getattr(self, field_name, None)
    #             field_type = field_val.annotations['node_id']
    #             field_val = field_val.save(True).node_id

    #         if isinstance(field_val, UUID):
    #             field_val = str(field_val)

    #         res[field_name] = field_val

    #     jsonpickle.set_preferred_backend('json')
    #     jsonpickle.set_encoder_options('json', ensure_ascii=False)

    #     res = jsonpickle.encode(res)

    #     return res

    def to_dict(self) -> Dict[str, Any]:
        _dict = self.__dict__

        from ..db.table import NodePromise
        for field_name, field_type in _dict.items():
            if isinstance(field_type, Constraint):
                field_type = field_type.py_type
                
            # if self.is_excluded(field_name, field_type):
            #     continue
            # if field_name not in self.table.header:
            #     continue
            # if not hasattr(self, field_name):
            #     continue

            field_val = getattr(self, field_name, None)
            
            if isinstance(field_val, NodePromise):
                field_val = getattr(field_val, 'node_id', None)

            if field_val and isinstance(field_type, Savable)\
            and not isinstance(field_val, UUID):
                field_val = getattr(self, field_name, None)
                field_type = field_val.annotations['node_id']
                field_val = field_val.save(True).node_id

            if isinstance(field_val, UUID):
                field_val = str(field_val)

            _dict[field_name] = field_val

        return _dict
            

    __exclude__:list = Node.__exclude__ + ['table', 'db']