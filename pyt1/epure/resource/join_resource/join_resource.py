from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..db.table import Table
    # from ...resource.db.table import Table

class Join:
    table:Table
    on_clause:str
    join_type:str
    alias:str

    def __init__(self, table:Table, on_clause:str, join_type:str="LEFT", alias:str="") -> None:
        self.table = table
        self.on_clause = on_clause
        self.join_type = join_type
        self.alias = alias
        
class JoinResource:
    table:Table
    joins:list[Join]

    def __init__(self, table:Table) -> None:
        self.joins = []
        self.table = table

    def join(self, table:Table, on_clause:str, join_type:str="LEFT", alias:str="") -> None:
        join = Join(table, on_clause, join_type, alias)
        res = JoinResource(self.table)
        res.joins = self.joins.copy()
        res.joins.append(join)
        return res

    def read(self, *args, **kwargs):

        # header = []
        where_clause = ""

        if len(args) >= 2:
            header = args[0]
            where_clause = args[1]

        elif len(args) == 1:
            where_clause = args[0]

        if len(args) <= 1:
            header = [self.table]
            header = header + [join.table for join in self.joins]

        return self.table.read(header, self.joins, where_clause, **kwargs)