from .gres_table import GresTable
from  .gres_header import GresHeader
from typing import Any, Union, Dict, List
from types import NoneType
from ...helpers.type_helper import check_type
from ..db.table_header import TableHeader
from ..db.table_column import TableColumn
from ..db.table_storage import TableStorage
from ..resource import Resource
from ...parser.inspect_parser.inspect_parser import InspectParser

class JsonbHeader(GresHeader):
    def __contains__(self, other: Any) -> bool:
        if isinstance(other, str) or isinstance(other, TableColumn):
            return True
        raise NotImplementedError

    def __getitem__(self, key:str):
        res = TableColumn(key, str)
        self.columns[key] = res
        return self.columns[key]


class JsonbTable(GresTable):
    header: JsonbHeader

    def __init__(self, name: str,
            header:Union[TableHeader, Dict[str, Any]]=None, resource:Resource=None, namespace:str = '', parser=InspectParser) -> None:        
        check_type('header', header, [TableHeader, dict, NoneType])        
        # header['jsonb___data'] = Any
        header = JsonbHeader(table=self)

        super().__init__(name=name, header=header, namespace=namespace, resource=resource)
    
    def serialize_header(self, db: TableStorage=None, **kwargs) -> List[Dict[str, str]]:
        res: List[Dict[str, str]] = [{'column_name': 'data_id', 'column_type': 'uuid'}, {'column_name': 'jsonb___data', 'column_type': 'jsonb'}]
        
        return res

        