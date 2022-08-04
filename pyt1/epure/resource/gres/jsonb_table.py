from .gres_table import GresTable
from  .gres_header import GresHeader
from typing import Any, Union, Dict
from types import NoneType
from ...helpers.type_helper import check_type
from ..db.table_header import TableHeader
from ..db.table_column import TableColumn
from ..resource import Resource

class JsonbHeader(GresHeader):
    def __contains__(self, other: Any) -> bool:
        if isinstance(other, str):
            return True
        raise NotImplementedError

    def __getitem__(self, key:str):
        res = TableColumn(key, str)
        self.columns[key] = res
        return self.columns[key]


class JsonbTable(GresTable):
    header: JsonbHeader

    def __init__(self, name: str,
            header:Union[TableHeader, Dict[str, Any]]=None, resource:Resource=None, namespace:str = '') -> None:        
        check_type('header', header, [TableHeader, dict, NoneType])        

        header = JsonbHeader()

        super().__init__(name=name, header=header, namespace=namespace, resource=resource)