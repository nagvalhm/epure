from types import NoneType
from typing import Any, Type, Dict, get_args
from uuid import UUID

# class EcollectionMetacls(type):
#     py_type:type = NoneType
#     __origin__:type = NoneType
#     ecollections:Dict[str,type] = {}

#     def __getitem__(self:Type, param:Any):
#         from ...epure import Epure, epure
#         name = f"{param.__name__}__list"
#         if name in self.elists:
#             return self.elists[name]
        
#         cls_dict = dict(self.__dict__)
#         cls_dict.pop('__dict__', None)
#         res = self.__class__(self.__name__, self.__bases__, cls_dict)
#         # res.__origin__ = self
#         res.py_type = param
#         # res.list_epure = Epure.EDb.get_epure_by_table_name(name)
#         # if res.list_epure is None:
#         obj = type(name, (object,), {})
#         obj.__annotations__ = {"elist_node_id":UUID, "value_order":int, "value":param}
#         # res.list_epure = epure(saver=EsetTableNode)(obj)
#         res.list_epure = epure()(obj)
#         self.elists[name] = res

#         # if issubclass(res.py_type, Constraint):
#         #     # ( hasattr(res.py_type, '__origin__') and  issubclass(res.py_type.__origin__, Constraint)):
#         #     raise EpureError('Constraint parameter cant be Constraint')
#         return res

class ECollectionMetacls(type):
    py_type:type = NoneType
    __origin__:type = NoneType
    # ecollections:Dict[str,type] = {}

    def __getitem__(self:Type, param:Any):
        from ...epure import epure
        from .edata import EsetTableData
        from .elist import Elist, Eset

        if issubclass(self, Elist):
            name = f"elist__{param.__name__}"
            origin = Elist
        else:
            name = f"eset__{param.__name__}"
            origin = Eset

        # if name in self.ecollections:
        #     return self.ecollections[name]
        
        cls_dict = dict(self.__dict__)
        cls_dict.pop('__dict__', None)
        res = self.__class__(self.__name__, self.__bases__, cls_dict)
        res.__origin__ = origin

        res.py_type = param

        obj = type(name, (object,), {})
        
        if issubclass(self, Elist):
            obj.__annotations__ = {"eset_id":UUID, "value_order":int, "value":param}
            res.collection_epure = epure(resource=f'ecollections.{name}')(obj)
        else:
            obj.__annotations__ = {"eset_id":UUID, "value":param}
            res.collection_epure = epure(resource=f'ecollections.{name}', saver=EsetTableData)(obj)
        
        # self.ecollections[name] = res

        # if issubclass(res.py_type, Constraint):
        #     # ( hasattr(res.py_type, '__origin__') and  issubclass(res.py_type.__origin__, Constraint)):
        #     raise EpureError('Constraint parameter cant be Constraint')
        return res
