from __future__ import annotations
from types import LambdaType, NoneType
from typing import TYPE_CHECKING, Dict, Union, List, ItemsView, Any, Type, Callable, cast
from ..savable import Savable
import inspect
# from .pseudo_table import PresudoTable, PseudoDb
# from .select_query import SelectQuery
from .constraint import Constraint
from ..resource import Resource
from ..node.node import Node
from ...parser.term import Term
from ...parser.leaf import TableProxy, TableColumn, QueryingProxy, DbProxy
from collections.abc import Sequence
from collections import OrderedDict

if TYPE_CHECKING:
    from .table_storage import TableStorage
from .db_entity import DbEntity
from ...helpers.type_helper import check_type
from ...errors import EpureError, DbError
from .table_header import TableHeader
from ...parser.term_parser import TermParser
from ..field_promise import FieldPromise


class Table(DbEntity):
    header:TableHeader
    parser: TermParser
    querying_proxy: QueryingProxy
    resource_proxy: DbProxy

    if TYPE_CHECKING:
        resource:TableStorage

    @property
    def db(self):
        return self.resource

    def __init__(self, name: str,
            header:Union[TableHeader, Dict[str, Any]]=None, resource:Resource=None, namespace:str = '') -> None:        
        check_type('header', header, [TableHeader, dict, NoneType])
        

        self._set_header(header)
        self.parser = TermParser(self)
        self.querying_proxy = TableProxy(self.db, self)
        self.resource_proxy = DbProxy(self.db)

        super().__init__(name, namespace, resource)


    def _serialize(self, node: Savable) -> Dict[str, str]:
        res = {}
        for field_name, field_type in node.annotations.items():
            if isinstance(field_type, Constraint):
                field_type = field_type.py_type
                
            if node.is_excluded(field_name, field_type):
                continue
            if field_name not in self.header:
                continue

            field_val = getattr(node, field_name, None)
            #working for db:
            if isinstance(field_val, Savable):
                field_type = field_val.annotations['node_id']
                field_val = field_val.save(True).node_id
                
            field_val = self.db.cast_py_db_val(field_type, field_val)

            res[field_name] = field_val
        
        return res



    def create(self, node: Node, asynch:bool=False) -> object:
        node.node_id = self.generate_id()
        script = self.serialize_for_create(node)
        if asynch:
            self.cache(script)
        else:
            self.execute(script)
        return node

    
    def read(self, *args, **kwargs) -> Any: #Union[Resource, Sequence[Resource]]:
        pass
        if not (args or kwargs):
            return self.read_by_fields(**kwargs)
        
        if kwargs:
            return self.read_by_kwargs(**kwargs)

        selector = args[0]
        if isinstance(args[0], str):
            return self.read_by_sql(selector)

        if callable(selector):
            return self.read_by_function(selector)

        if isinstance(args[-1], Term):
            selector = args[-1]
            return self.read_by_term(args[0:-2], selector)

        raise NotImplementedError(f'couldn read by object of type {type(selector)}')

        # if isinstance(selector, str):
        #     return self.execute(selector)
        # if not callable(selector):
        #     raise NotImplementedError(f'couldn read by object of type {type(selector)}')


        # if inspect.ismethod(selector):
        #     def reader(self:Table, *args, **kwargs):
        #         pseudo_self = PresudoTable(self)
        #         pseudo_db = PseudoDb(self.db)
        #         script = selector(pseudo_self, pseudo_db, *args, **kwargs)
        #         return self.execute(selector)
        #     setattr(self, selector.__name__, reader)

        # pseudo_self = PresudoTable(self)
        # pseudo_db = PseudoDb(self.db)
        # script = selector(pseudo_self, pseudo_db)
        # res = self.execute(script)
        # return res

    def read_by_fields(self):
        raise NotImplementedError

    def read_by_kwargs(self):
        raise NotImplementedError

    def read_by_sql(self, selector):
        res = self.execute(selector)
        res = self.deserialize(res)
        return res

    def deserialize(self, rows: dict):
        # from ...epure import Epure
        full_name_epure_dict = self._column_full_name_epure_dict(rows[0])
        res = []
        for node_dict in rows:
            res_row = self._init_epures_row(node_dict, full_name_epure_dict)
            res.append(res_row)
        return res

    def _init_epures_row(self, node_dict, full_name_epure_dict) -> Dict[type, dict]:
        epure_kwargs_dict = OrderedDict()
        for full_name in node_dict:
            tpl = full_name_epure_dict[full_name]
            epure_cls = tpl[0]
            field_name = tpl[1]
            if epure_cls not in epure_kwargs_dict:
                epure_kwargs_dict[epure_cls] = {}
            kwargs = epure_kwargs_dict[epure_cls]
            kwargs[field_name] = node_dict[full_name]
        
        res = []
        for epure_cls, kwargs in epure_kwargs_dict.items():             
            epure_obj = self._init_epure(epure_cls, kwargs)
            res.append(epure_obj)
        return res

    def _init_epure(self, epure_cls, kwargs):
        res = epure_cls(kwargs)
        epure_table = getattr(epure_cls, 'resource', None)
        for field_name, field_val in kwargs:
            db_type = None
            if epure_table != None:
                column = epure_table.header[field_name]
                py_type = column.py_type
                db_type = self.db.get_db_type(py_type)
            val = self.db.cast_db_py_val(field_val, db_type)
            setattr(res, field_name, val)

        for field_name in res.annotations():
            if field_name not in kwargs:
                promise = FieldPromise(self, field_name)
                setattr(res, field_name, promise)
        return res

        # tab_col: Dict[str, list] = OrderedDict()
        # for full_name in node_dict:
        #     split = full_name.rsplit('.', 1)
        #     table_name = split[0]
        #     col_name = split[1]
        #     epure_cls = self.db.get_epure_by_table_name(table_name)
        #     if table_name not in tab_col:
        #         tab_col[table_name] = []
        #     tab_col[table_name].append(col_name)
        
        # for table_name in tab_col: 
        #     epure_cls = self.db.get_epure_by_table_name(table_name)

    def _column_full_name_epure_dict(self, node_dict) -> Dict[str, tuple]:
        res = OrderedDict()
        for full_name in node_dict:
            split = full_name.rsplit('.', 1)
            table_name = split[0]
            field_name = split[1]
            epure_cls = self.db.get_epure_by_table_name(table_name)
            res[full_name] = (epure_cls, field_name)
        return res

    def read_by_function(self, func):
        selector = func(self.querying_proxy, self.resource_proxy)
        if isinstance(selector, Sequence):
            return self.read(*selector)
        return self.read(selector)

    def read_by_term(self, header, selector:Term):
        sql = self.parser.parse(header, selector)
        res = self.read(sql)
        return res


    def update(self, node: Savable, asynch:bool=False) -> object:
        script = self.serialize_for_update(node)
        if asynch:
            self.cache(script)
        else:
            self.execute(script)
        return node


    def cache(self, script: str):        
        self.db.cache_queue.append(script)


    def _set_header(self, header):
        if header == None:
            header = TableHeader(table=self)
        
        if isinstance(header, Dict):
            header = TableHeader(columns=header, table=self)
        
        self.header = header
        self.header.resource = self
       
    def serialize_for_create(self, node: Savable, **kwargs) -> object:
        raise NotImplementedError

    def serialize_for_read(self, node: Savable, **kwargs) -> object:
        raise NotImplementedError

    def serialize_for_update(self, node: Savable, **kwargs) -> object:
        raise NotImplementedError

    def serialize_for_delete(self, node: Savable, **kwargs) -> object:
        raise NotImplementedError

    
    def serialize_header(self, db: TableStorage=None, **kwargs) -> List[Dict[str, str]]:
        res: List[Dict[str, str]] = list()

        if db == None:
            db = self.db

        if db == None:
            raise EpureError('undefined db for header serialization')
        
        header = self.header
        for column_name in header:
            column = header[column_name]
           
            serialized = {
                "column_name": column.name,
                "column_type": column.serialize_type(db) #db.get_db_type(column.column_type)
            }
            res.append(serialized)
        return res