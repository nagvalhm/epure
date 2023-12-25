from __future__ import annotations
from types import NoneType, CodeType
from typing import cast, Callable, List, Any, get_type_hints, Dict, TYPE_CHECKING
from .resource.resource import Resource
from .helpers.type_helper import check_type
from .errors import EpureError, DefaultConstraintError
from .resource.db.constraint import Foreign, Default, Constraint
from .resource.edata.ecollection_metacls import ECollectionMetacls

from uuid import UUID
from .parser.inspect_parser.db_model import DbModel
import textwrap
import inspect
from .parser.inspect_parser.inspect_parser import InspectParser
import types
import ast
from importlib import import_module
import os
from typing import Any, Callable, TypeVar

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])

# from types import FunctionType
from .resource.edata.edata import TableData
from .resource.savable import Savable
if TYPE_CHECKING:
    from .resource.db.table_storage import TableStorage
    from .resource.db.table import Table
from .resource.db.db_entity import DbEntity
import functools
from .parser.term import Term
from .resource.edata.proto import Proto
from inspect import signature



class Epure(type, Savable):
    
    EDb:TableStorage
    epures:List[Epure] = []
    # annotations:Dict[str,Any]
    resource:Savable
    prepared_resource:object
    init_params:object
    
    # def __new__(mcls, name: str, cls_bases: Tuple[type, ...], namespace: dict[str, Any]) -> Epure:
    #     return super().__new__(mcls, name, cls_bases, namespace)    
    
    def __call__(self, *args, **kwargs):
        if not self.is_saved:
            self.save_epure()
            self.is_saved = True    # __getattr__ is called here, you cannot enter __getattr__ with debuger, so put breakpoint on start of getattr func

        res = super(Epure, self).__call__(*args, **kwargs)
        return res


    def __getattr__(self, attr_name: str) -> Any:
        if not self.is_saved:
            self.is_saved = True    # __getattr__ is called here, you cannot enter __getattr__ with debuger, so put breakpoint on start of getattr func
            self.save_epure()
            return getattr(self, attr_name)
        raise AttributeError(f"'{type(self)}' object has no attribute '{attr_name}'")
        # if self.is_saved:
        #     raise AttributeError(f"'{type(self)}' object has no attribute '{attr_name}'")
        # self.is_saved = True
        # self.save_epure()        
        # return getattr(self, attr_name)

    #decorator
    # @classmethod
    # def read(cls, method):
    #     querying_proxy = None
    #     resource_proxy = None
    #     if getattr(cls, 'resource', None):
    #         querying_proxy = getattr(cls.resource, 'querying_proxy', None)
    #         resource_proxy = getattr(cls.resource, 'resource_proxy', None)

    #     @functools.wraps(method)
    #     def wrap(self, *args, **kwargs):
    #         res = None
    #         if querying_proxy and resource_proxy:
    #             res = method(self, querying_proxy, resource_proxy, *args, **kwargs)
    #         if querying_proxy:
    #             res = method(self, querying_proxy, *args, **kwargs)
    #         if resource_proxy:
    #             res = method(self, resource_proxy, *args, **kwargs)
    #         else:
    #             res = method(self, *args, **kwargs)
    #         if isinstance(res, Term):
    #             return self.resource.read(res)
    #         return res
    #     return wrap
        # def reader(self:Table, *args, **kwargs):
        #     pseudo_self = PresudoTable(self)
        #     pseudo_db = PseudoDb(self.db)
        #     script = selector(pseudo_self, pseudo_db, *args, **kwargs)
        #     return self.execute(selector)
        # setattr(self, selector.__name__, reader)

    def prepare_save(self, resource:object):
        self.__class__.epures.append(self)
        self.prepared_resource = resource


    def save_epure(self):
        self.set_resource()
        self.init_params = self.get_init_params()

    def get_init_params(self):
        res = []
        sig = signature(self.__init__)
        for key, val in sig.parameters.items():
            if val.kind == val.VAR_POSITIONAL:
                    continue
            if val.kind == val.VAR_KEYWORD:
                res.append(True)
            else:
                res.append(key)
        return res[1:]
        # sig = signature(epure_cls.__init__)
        # params = sig.parameters
        # params_vals = params.values()
        # has_kwargs = any([True for p in params_vals if p.kind == p.VAR_KEYWORD])
        # if has_kwargs:
        #     res = epure_cls(**kwargs)
        # else:
        #     arguments = {}
        #     for key, val in params:
        #         if val.kind == val.VAR_POSITIONAL:
        #             continue
        #         if key in kwargs:
        #             arguments[key] = kwargs[key]
        #             continue
        #         if val.default == val.empty:
        #             raise DeserializeError
        #     res = epure_cls(**arguments)


    def set_resource(self):
        resource = self.prepared_resource
        check_type('resource', resource, [str, Savable, NoneType])

        if type(resource) == Savable:
            resource = cast(Savable, resource)
            if not hasattr(resource, 'resource'):
                raise EpureError('For using savable as resource for epure, savable must have own resource')
            grandpa = resource.resource
            grandpa.update(self)
        else:
            table_name = self._get_table_name(self, resource)
            resource = self._create_or_update(table_name)

        self.resource = resource

        

    def _create_or_update(self, table_name:str) -> Table:
        from .resource.db.table import Table
        table:Table = self._get_table_by_cls(table_name)
        res:DbEntity
        if table_name in self.EDb:
            deleted_columns = self.EDb[table_name].header.deleted_columns
            table.header.deleted_columns = deleted_columns
            res = self.EDb.update(table)
        else:
            res = self.EDb.create(table)
        res = cast(Table, res)
        return res

    def _get_table_name(self, cls, resource: object) -> str:
        
        if not isinstance(resource, str):
            resource = cast(Savable, resource)
            return resource.full_name

        if resource:
            return resource
        
        return self.EDb._get_full_table_name(cls.__name__).full_name

        

    def _get_table_by_cls(self, table_name: str = '') -> Table:
        from .resource.db.table import Table
        table:Table
        
        full_name = self.EDb._get_full_table_name(table_name)        
        columns = {}

        for field_name, py_type in self.annotations.items():
            py_type = cast(type, py_type)

            if Table.is_excluded(self, field_name, py_type):
                continue
            py_type = self.get_py_type(field_name, py_type)
            
            columns[field_name] = py_type

        if len(columns) == 1 and list(columns.keys())[0] == 'data_id':
            TableCls = self.EDb.nosql_table_type
        else:
            TableCls = self.EDb.default_table_type
        table = TableCls(full_name.name, columns, self.EDb, full_name.namespace, parser=self.EDb.parser)
        return table

    def get_py_type(self, field_name:str, py_type:type) -> type:
        # from .resource.edata.elist import ElistMetacls
        # from .resource.edata.elist import ECollectionMetacls


        if py_type in self.epures:
            # py_type = cast(Epure, py_type)
            return self.get_py_type(field_name, py_type.annotations['data_id'])
        
        # if isinstance(py_type, ElistMetacls):
        if isinstance(py_type, ECollectionMetacls):
            return self.get_py_type(field_name, UUID)
        # if isinstance(py_type, Constraint)
            
        if isinstance(py_type, Constraint) and issubclass(py_type.__origin__, Default):
            return self.get_default_type(field_name, py_type)

        return py_type

    def get_default_type(self, field_name:str, py_type:Default) -> Any:
        default = getattr(self, field_name, None)
        if not (default or py_type.default):
            raise DefaultConstraintError(self.full_name, field_name)
        if not py_type.default:
            py_type.default = default

        if not isinstance(py_type.default, py_type.py_type):
            raise DefaultConstraintError(message=f'''field {field_name} of class {self.full_name} 
                    has wrong defaul value {py_type.default} not corresponding to {py_type.py_type} type''')

        return py_type


    def get_foreign_type(self, foreign:Epure) -> Any:
        foreign_id_type = foreign.annotations['data_id']

        foreign_table = self._get_table_name(foreign, foreign.prepared_resource)

        foreign_column = 'data_id'
        column_type = Foreign[foreign_id_type, foreign_table, foreign_column]
        return column_type


        

def epure(resource:object='', saver:type=TableData, epure_metaclass:type=Epure) -> Callable:
    check_type('resource', resource, [str, Savable, NoneType])

    def epure_creator(cls:type) -> Epure:
        epure_cls = _create_epure(cls, saver, epure_metaclass)
        epure_cls.is_saved = False      # might not change true to false in the debuger, because this is overrided setter.
        epure_cls.prepare_save(resource)

        del cls
        return epure_cls

    return epure_creator


def _create_epure(cls, saver, _Epure):
    cls_dict = dict(cls.__dict__)
    cls_dict.pop('__dict__', None)
    if issubclass(cls, Savable):
        return _Epure(cls.__name__, cls.__bases__, cls_dict)

    bases = list(cls.__bases__)
    if object in bases:
        bases.remove(object)
    bases.append(saver)
    return _Epure(cls.__name__, tuple(bases), cls_dict)


def proto(resource:object='', saver:type=Proto, epure_metaclass:type=Epure) -> Callable:
    return epure(resource, saver, epure_metaclass)

def _get_func_br_lines(func_str) -> List[int]:
    
    code_src_splited = func_str.splitlines(True)

    src_lines_dict = dict(enumerate(code_src_splited))

    br_lines_list = [k for k, v in src_lines_dict.items() if v=='\n' or ("#" in v and v.strip().startswith('#'))]

    return br_lines_list

def _insert_br_lines(func_str:str, br_lines_list:List[int]) -> str:

    new_func_list = func_str.splitlines(True)

    for i in br_lines_list:
        new_func_list.insert(i, '\n')

    func_str = "".join(new_func_list)

    return func_str

def _compile_func(func:Callable, new_func_w_br_lines:str, func_name:str) -> CodeType:

    file_name = func_name + ".py"

    code_block = compile(new_func_w_br_lines, file_name, 'exec')

    i = next(i for i, v in enumerate(code_block.co_consts) if isinstance(v, CodeType))

    fn_code = code_block.co_consts[i]
    n_fn_code = func.__code__

    new_code = CodeType(
    fn_code.co_argcount,
    fn_code.co_posonlyargcount,
    fn_code.co_kwonlyargcount,
    fn_code.co_nlocals,
    fn_code.co_stacksize,
    fn_code.co_flags,
    fn_code.co_code,
    fn_code.co_consts,
    fn_code.co_names,
    fn_code.co_varnames,
    n_fn_code.co_filename,
    fn_code.co_name,
    n_fn_code.co_firstlineno,
    fn_code.co_linetable,
    # fn_code.co_lnotab,
    fn_code.co_freevars,
    fn_code.co_cellvars)

    return new_code

def escript(func: Callable) -> Callable[[DecoratedCallable], DecoratedCallable]:

    func_source = inspect.getsource(func)

    dedent_src = textwrap.dedent(func_source)

    br_lines_list = _get_func_br_lines(dedent_src)

    parsed_tree = InspectParser().parse(dedent_src)

    ast.fix_missing_locations(parsed_tree)

    new_func_str = ast.unparse(parsed_tree)

    new_func_w_br_lines = _insert_br_lines(new_func_str, br_lines_list)

    func_name = parsed_tree.body[0].name

    new_func_code = _compile_func(func, new_func_w_br_lines, func_name)

    func.__code__ = new_func_code

    def inner(self, *args, **kwargs) -> Any:
        #temporary holders for tp, db proberties
        # tp_err_prop = getattr(self, "tp")
        # dbp_err_prop = getattr(self, "tp")
        # from .resource.edata.elist import ECollectionMetacls
        # from .resource.edata.elist import Elist, Eset

        if isinstance(type(self), Epure) or isinstance(self, Epure):
            db = self.resource.db
            full_name = self.table.full_name
        elif isinstance(type(self), ECollectionMetacls):
            db = self.collection_epure.resource.db
            full_name = self.collection_epure.resource.full_name
        else:
            db = self.db
            full_name = self.full_name
        
        self.dbm = DbModel(db)
        self.md = getattr(self.dbm, full_name)

        res = func(self, *args, **kwargs)

        delattr(self, "dbm")
        delattr(self, "md")
        
        return res

    return inner