from __future__ import annotations
from types import NoneType, CodeType
from typing import cast, Callable, List, Any, get_type_hints, Dict, TYPE_CHECKING
from .resource.resource import Resource
from .helpers.type_helper import check_type
from .errors import EpureError, DefaultConstraintError
from .resource.db.constraint import Foreign, Default, Constraint
# from .resource.node.elist_metacls import ElistMetacls
# from .resource.node.elist import ECollectionMetacls
from uuid import UUID
from .parser.inspect_parser.db_proxy import DbProxy
import textwrap
import inspect
from .parser.inspect_parser.inspect_parser import InspectParser
import types
import ast
from importlib import import_module
import os


# from types import FunctionType
from .resource.node.node import TableNode
from .resource.savable import Savable
if TYPE_CHECKING:
    from .resource.db.table_storage import TableStorage
    from .resource.db.table import Table
from .resource.db.db_entity import DbEntity
import functools
from .parser.term import Term
from .resource.node.proto import Proto
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
    @classmethod
    def read(cls, method):
        querying_proxy = None
        resource_proxy = None
        if getattr(cls, 'resource', None):
            querying_proxy = getattr(cls.resource, 'querying_proxy', None)
            resource_proxy = getattr(cls.resource, 'resource_proxy', None)

        @functools.wraps(method)
        def wrap(self, *args, **kwargs):
            res = None
            if querying_proxy and resource_proxy:
                res = method(self, querying_proxy, resource_proxy, *args, **kwargs)
            if querying_proxy:
                res = method(self, querying_proxy, *args, **kwargs)
            if resource_proxy:
                res = method(self, resource_proxy, *args, **kwargs)
            else:
                res = method(self, *args, **kwargs)
            if isinstance(res, Term):
                return self.resource.read(res)
            return res
        return wrap
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

        if len(columns) == 1 and list(columns.keys())[0] == 'node_id':
            TableCls = self.EDb.nosql_table_type
        else:
            TableCls = self.EDb.default_table_type
        table = TableCls(full_name.name, columns, self.EDb, full_name.namespace, parser=self.EDb.parser)
        return table

    def get_py_type(self, field_name:str, py_type:type) -> type:
        # from .resource.node.elist import ElistMetacls
        from .resource.node.elist import ECollectionMetacls


        if py_type in self.epures:
            # py_type = cast(Epure, py_type)
            return self.get_py_type(field_name, py_type.annotations['node_id'])
        
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
        foreign_id_type = foreign.annotations['node_id']

        foreign_table = self._get_table_name(foreign, foreign.prepared_resource)

        foreign_column = 'node_id'
        column_type = Foreign[foreign_id_type, foreign_table, foreign_column]
        return column_type


        

def epure(resource:object='', saver:type=TableNode, epure_metaclass:type=Epure) -> Callable:
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


def escript(func):
# def inner(self, *args, **kwargs):
    # if isinstance(type(self), Epure):
    #     db = self.resource.db
    #     full_name = self.table.full_name
    # else:
    #     db = self.db
    #     full_name = self.full_name

    # self.dbp = DbProxy(db)
    # self.tp = self.dbp[full_name]
    # self.tp = getattr(self.dbp, full_name)

    func_source = inspect.getsource(func)

    dedent_src = textwrap.dedent(func_source)

    parsed_tree = InspectParser().parse(dedent_src)

    ast.fix_missing_locations(parsed_tree)

    # code_src_splited = inspect.getsourcelines(func)[0]

    # index_def_str = next(index for index, string in enumerate(code_src_splited) if "def " in string)

    code_src_splited = dedent_src.splitlines(True)

    line_index = code_src_splited.index("@escript\n")

    # code_src_splited[line_index] = "#@escript\n"

    # code_src_no_def = code_src_splited[index_def_str+1:]

    src_lines_dict = dict(enumerate(code_src_splited))

    br_lines_list = [k for k, v in src_lines_dict.items() if v=='\n' or ("#" in v and v.strip().startswith('#'))]

    new_func_src = ast.unparse(parsed_tree)

    new_func_list = new_func_src.splitlines(True)

    # new_func_list.insert(line_index, '#@escript\n')

    for i in br_lines_list:
        new_func_list.insert(i, '\n')

    new_func_src = "".join(new_func_list)

    func_name = parsed_tree.body[0].name

    file_name = func_name + ".py"
    
    # with open(file_name, 'w') as f:
    #     f.write(new_func_src)

    # mod = import_module(file_name)

    # res = getattr(mod, func_name)(self,*args,**kwargs)

    # code_block = compile(open(file_name).read(), file_name, 'exec')

    # code_block = compile(open(file_name).read(), file_name, 'exec')
    code_block = compile(new_func_src, file_name, 'exec')

    # code_block = compile(func_parsed, "debug_parser.py", "exec")

    # exec(code_block)

    # area_func = locals()[func_name]

    i = next(i for i, v in enumerate(code_block.co_consts) if isinstance(v, CodeType))


    # fn_code = area_func.__code__
    fn_code = code_block.co_consts[i]
    n_fn_code = func.__code__

    cod = CodeType(
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

    func.__code__ = cod
    # func.__code__ = code_block

    # os.remove(file_name)

    # co = compile(parsed_tree, "debug_parser.py", "exec")

    # # get index of code obj compiled from func
    # i = next(i for i, v in enumerate(co.co_consts) if isinstance(v, CodeType))

    # fn = types.FunctionType(co.co_consts[i], func.__globals__, name=func.__name__,
    #                     argdefs=func.__defaults__)
    #                 #    ,closure=func.__closure__)
    # # fn = types.FunctionType(co, globals())
    # fn = functools.update_wrapper(fn, func)
    # fn.__kwdefaults__ = func.__kwdefaults__

    # res = fn(self,*args,**kwargs)

    # func.__code__ = fn.__code__

    # res = func(self,*args,**kwargs)
    
    # res = self.resource.read(res)
    
    # return fn
    # return self.resource.read(res)

    def inner(self, *args, **kwargs):
        #temporary holders for tp, db proberties
        # tp_err_prop = getattr(self, "tp")
        # dbp_err_prop = getattr(self, "tp")

        if isinstance(type(self), Epure):
            db = self.resource.db
            full_name = self.table.full_name
        else:
            db = self.db
            full_name = self.full_name
        
        self.dbp = DbProxy(db)
        self.tp = getattr(self.dbp, full_name)

        res = func(self, *args, **kwargs)
        # res = area_func(self, *args, **kwargs)

        delattr(self, "dbp")
        delattr(self, "tp")

        # self.tp = tp_err_prop
        # self.dbp = dbp_err_prop
        return res

    return inner

# move to other file

# def select(self, *args, joins=[], include_node_id=False, **kwargs):

#     header = get_select_header(args[0])
#     body = args[1]
    
#     if kwargs:
#         # return get_condition_by_kwargs(header, kwargs)
#         body = get_condition_by_kwargs(header[0].__table__.full_name, **kwargs)

#     # if args:
#     return self.serialize_read(header=header, joins=joins, where_clause=body, full_names=True, include_node_id=include_node_id)
        
# def get_condition_by_kwargs(prefix:str, operator:str="", **kwargs):

#     kwargs_items = list(kwargs.items())
#     first_item = list(kwargs_items[0])
#     # term = getattr(tp, first_item[0]) == first_item[1]

#     if type(first_item[1]) in (str, UUID):
#         first_item[1] = repr(str(first_item[1]))

#     term = f"{prefix}.{first_item[0]} = {first_item[1]}"

#     for (key, val) in kwargs_items[1:]:
#             if type(val) in (str, UUID):
#                 val = repr(str(val))

#             if operator == 'or':
#                 term += f" OR {prefix}.{key} = {val}"
#             else:
#                 term += f" AND {prefix}.{key} = {val}"

#     return term

# def get_select_header(header):
    
#     if not isinstance(header, collections.abc.Sequence):
#         header = tuple(header)
    
#     return header

# move to other file

    
