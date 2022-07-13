from .gres_table import GresTable
from  .gres_header import GresHeader
from typing import Any

class JsonbHeader(GresHeader):
    def __contains__(self, other: Any) -> bool:
        if isinstance(other, str):
            return True
        raise NotImplementedError


class JsonbTable(GresTable):
    header: JsonbHeader