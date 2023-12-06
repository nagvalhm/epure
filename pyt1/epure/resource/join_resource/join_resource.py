from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...parser.ast_parser.table_proxy import TableProxy
    # from ...resource.db.table import Table

class Join:
    table_proxy:TableProxy
    on_clause:str
    join_type:str
    alias:str

    def __init__(self, table_proxy:TableProxy, on_clause:str, join_type:str="LEFT", alias:str="") -> None:
        self.table_proxy = table_proxy
        self.on_clause = on_clause
        self.join_type = join_type
        self.alias = alias
        
class JoinResource:
    table_proxy:TableProxy
    joins:list[Join]

    def __init__(self, table_proxy:TableProxy) -> None:
        self.joins = []
        self.table_proxy = table_proxy

    def join(self, joined_table_proxy:TableProxy, on_clause:str, join_type:str="LEFT", alias:str="") -> None:
        join = Join(joined_table_proxy, on_clause, join_type, alias)
        self.joins.append(join)

    def read(self, *args, **kwargs):

        # header = []
        where_clause = ""

        if len(args) >= 2:
            header = args[0]
            where_clause = args[1]

        elif len(args) == 1:
            where_clause = args[0]

        if len(args) <= 1:
            header = [self.table_proxy]
            header = header + [join.table_proxy for join in self.joins]

        return self.table_proxy.__table__.read(header, self.joins, where_clause, **kwargs)