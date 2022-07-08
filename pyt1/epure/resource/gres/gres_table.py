from ..db.table import Table
from .gres_header import GresHeader
from .gres_entity import GresEntity
from typing import Dict



class GresTable(Table, GresEntity):
    def _set_header(self, header):
        if header == None:
            header = GresHeader(table=self)
        
        if isinstance(header, Dict):
            header = GresHeader(columns=header, table=self)
        
        self.header = header
        self.header.resource = self

class JsonbTable(GresTable):
    pass