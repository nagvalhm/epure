from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...parser.inspect_parser.model import Model
    # from ...resource.db.table import Table

class JoinMethods:
    
    def left_join(self, joined_model:Model, on_clause:str, alias:str=""):
        return self._join(joined_model, on_clause, "LEFT", alias)

    def right_join(self, joined_model:Model, on_clause:str, alias:str=""):
        return self._join(joined_model, on_clause, "RIGHT", alias)

    def join(self, joined_model:Model, on_clause:str, alias:str=""):
        return self._join(joined_model, on_clause, "", alias)

    def full_join(self, joined_model:Model, on_clause:str, alias:str=""):
        return self._join(joined_model, on_clause, "OUTER", alias)

class Join:
    model:Model
    on_clause:str
    join_type:str
    alias:str

    def __init__(self, model:Model, on_clause:str, join_type:str="LEFT", alias:str="") -> None:
        self.model = model
        self.on_clause = on_clause
        self.join_type = join_type
        self.alias = alias
        
class JoinResource(JoinMethods):
    model:Model
    joins:list[Join]

    def __init__(self, model:Model) -> None:
        self.joins = []
        self.model = model

    def _join(self, joined_model:Model, on_clause:str, join_type:str="", alias:str="") -> None:
        join = Join(joined_model, on_clause, join_type, alias)
        res = JoinResource(self.model)
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
            header = [self.model]
            header = header + [join.model for join in self.joins]

        return self.model.__table__.read(header, self.joins, where_clause, **kwargs)