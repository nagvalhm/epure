from uuid import UUID
from ..savable import Savable
from ..resource import Resource
from ...errors import ResourceException
from typing import Any, Dict, Callable
import jsonpickle
from ..db.constraint import Constraint
from ...errors import EpureError
from .ecollection_metacls import ECollectionMetacls
from ..data_promise import DataPromise, ElistPromise, EsetPromise
from ...helpers.type_helper import is_uuid

from typing import get_origin

class EData(Savable):

    data_id:object
    __exclude__:list
    __promises_dict__:Dict[str, Any]

    def __init__(self, data_id:object=None, resource:Resource=None) -> None:
        if data_id != None:
            self.data_id = data_id
        super().__init__(resource)

    # def __getattribute__(self, name: str) -> Any:
    #     from ..node_promise import NodePromise
    #     val = super(EData, self).__getattribute__(name)
    #     if isinstance(val, NodePromise):
    #         setattr(self, name, val.get())
    #     return super().__getattribute__(name)
    
    def __getattr__(self, name:str):
        if '__promises_dict__' in self.__dict__ and name in self.__promises_dict__:
            res = self.__promises_dict__[name].get()
            setattr(self, name, res)
            self.__promises_dict__.pop(name)
            return res
        else:
            raise AttributeError(f"'{type(self)}' object has no attribute '{name}'")
        
    def load(self):
        if '__promises_dict__' in self.__dict__ and self.__promises_dict__:
            for name in list(self.__promises_dict__):
                self.__getattr__(name)
            delattr(self, "__promises_dict__")

    @classmethod
    def from_dict(_cls, _dict:Dict[str, Any])->object:
        raise NotImplementedError

    def save(self, asynch:bool=False):
        if not hasattr(self, 'resource'):
            raise ResourceException('Unable save Savable, resource not found')
        resource = self.resource
        
        
        if hasattr(self, 'data_id') and self.data_id:
            res = resource.update(self, asynch)
            return res
        else:
            res = resource.create(self, asynch)
            return res


class TableData(EData):
    db:Resource
    data_id: UUID
    resource:Savable

    def __init__(self, data_id:object=None, resource:Resource=None, **kwargs) -> None:
        if data_id != None and isinstance(data_id, str):
            data_id = UUID(data_id)

        if not isinstance(data_id, UUID):
            data_id = None

        super().__init__(data_id, resource)

    @property
    def table(self) -> Savable:
        return self.resource
    

    def __setattr__(self, name: str, value: Any) -> None:
        from .elist import Eset

        if not (hasattr(value, "__origin__") and value.__origin__ == Eset):
            return super().__setattr__(name, value)

        collection_epure = value.get_collection_epure(parent_obj=self, field_name=name)
        # value.collection_epure = collection_epure
        value._redefine_collection_epure(collection_epure)

        return super().__setattr__(name, value)
    
    # @property
    # def tp(self): # doesnt raise error when called
    #     raise AttributeError("property tp cannot be accessed outside of method decorated by @escript decorator")
    
    # @property
    # def dbp(self): # doesnt raise error when called
    #     raise AttributeError("property dbp cannot be accessed outside of method decorated by @escript decorator")

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
    def from_dict(_cls, _dict:Dict[str, Any]) -> object:
        from .elist import ECollectionMetacls
        from .elist import Elist, Eset


        # instance = _cls.__call__()
        instance = _cls()
        instance.__promises_dict__ = {}

        for field_name, val in _dict.items():

            if not field_name in instance.annotations:
                continue

            cls_attr_type = instance.annotations[field_name]

            if get_origin(cls_attr_type) != None: # check if class is Generic
                cls_attr_type = get_origin(cls_attr_type)
            
            val_type_match_cls_attr_type = isinstance(val, cls_attr_type)

            if field_name == "data_id" and not isinstance(val, UUID):
                val = UUID(val)
                val_type_match_cls_attr_type = True

            if isinstance(cls_attr_type, ECollectionMetacls) and not val_type_match_cls_attr_type: # check if attr is elist or eset
                # try:
                if is_uuid(val) and cls_attr_type.__origin__ == Elist:
                    eset_id = UUID(val)
                    promise = ElistPromise(cls_attr_type.collection_epure.resource, eset_id, cls_attr_type)
                    instance.__promises_dict__[field_name] = promise
                    continue

                elif is_uuid(val) and cls_attr_type.__origin__ == Eset:
                    eset_id = UUID(val)
                    promise = EsetPromise(cls_attr_type.collection_epure.resource, eset_id, cls_attr_type)
                    instance.__promises_dict__[field_name] = promise
                    continue

                elif type(val[0]) == dict and isinstance(cls_attr_type.py_type, Savable)\
                and cls_attr_type.__origin__ in (Elist, Eset):
                    val = val.copy()
                    for i, item in enumerate(val):
                        new_item = cls_attr_type.py_type()
                        for name, it in val[i].items():
                            setattr(new_item, name, it)
                        val[i] = new_item

                # except(Exception):
                elif cls_attr_type.py_type in (bytes, bytearray)\
                    and not type(val[0]) in (bytes, bytearray):
                        val = val.copy()
                        for i, item in enumerate(val):
                            val[i] = item.encode()

                val = cls_attr_type(val)

                val_type_match_cls_attr_type = True

            elif issubclass(cls_attr_type, Savable) and not val_type_match_cls_attr_type and is_uuid(val): # check if attr is epure 
                # try: 
                #     data_id = UUID(val)
                #     promise = DataPromise(cls_attr_type.resource, data_id)
                #     instance.__promises_dict__[field_name] = promise
                #     continue
                # except(Exception):
                #     val = cls_attr_type(val)
                promise = DataPromise(cls_attr_type.resource, val)
                instance.__promises_dict__[field_name] = promise
                continue

            elif issubclass(cls_attr_type, Savable) and not val_type_match_cls_attr_type and type(val) == dict:
                # data_id = val.get("data_id", None)
                val = cls_attr_type(**val)

            val_type_match_cls_attr_type = True
            
            if val is None:
                val_type_match_cls_attr_type = True

            if isinstance(val, str) and cls_attr_type in (bytes, bytearray): # bytearray is yet to be tested!
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

    def _serialize_field_val_to_dict(self, field_val, field_type=None, field_name:str=None, full:bool=None,_rec_depth:int = None, lambda_func:Callable=None):
        # return super()._serialize_field_val(field_type)
        # lambda_func = args[0][0]

        if isinstance(field_val, Savable) and not isinstance(type(field_val), ECollectionMetacls)\
        and (lambda_func(field_name, field_val, field_type, self, _rec_depth) or full == True):
            field_val = field_val.to_dict(full, lambda_func, _rec_depth+1)

        elif (isinstance(type(field_val), ECollectionMetacls) or type(field_val) in (set, tuple, list)) and len(field_val)\
        and isinstance(next(iter(field_val), False), Savable) and\
        (lambda_func(field_name, field_val, field_type, self, _rec_depth) or full == True):
            field_val = [item.to_dict(full, lambda_func, _rec_depth+1) for item in field_val]

        elif isinstance(type(field_val), ECollectionMetacls) and len(field_val) and not isinstance(next(iter(field_val), False), Savable)\
        and lambda_func(field_name, field_val, field_type, self, _rec_depth):
            field_val = [item for item in field_val]

        elif isinstance(field_val, Savable) and hasattr(field_val, "data_id"):
            field_val = field_val.data_id

        elif isinstance(field_val, Savable) and not hasattr(field_val, "data_id"):
            field_val = None

        if isinstance(field_val, UUID):
            field_val = str(field_val)

        return field_val


    def to_dict(self, full=False, lambda_func:Callable = lambda field_name, field_value, field_type, parent_value, rec_depth: 
                rec_depth < 1 or isinstance(type(parent_value), ECollectionMetacls), _rec_depth=0) -> Dict[str, Any]:

        self.load()

        _dict = self._serialize(self, self._serialize_field_val_to_dict, full, _rec_depth, lambda_func)
 
        return _dict

    def to_json(self, full=False, lambda_func:Callable = lambda field_name, field_value, field_type, parent_value, rec_depth: 
                rec_depth < 1 or isinstance(type(parent_value), ECollectionMetacls), _rec_depth=0, encoder:Callable=jsonpickle.encode) -> Dict[str, Any]:

        _dict = self.to_dict(full=full, lambda_func=lambda_func,_rec_depth=_rec_depth)
        
        return encoder(_dict)

    __exclude__:list = EData.__exclude__ + ['table', 'db']

class EsetTableData(TableData):

    def __hash__(self) -> int:
        val = self.value
        # if hasattr(val, "node_id") and val.node_id:
        #     return hash(val.node_id)
        
        return hash(id(val))