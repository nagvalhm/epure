import types
from typing import Any

class Term:

    #bool_ops
    def _and(self, left, right): #and
        return f"{left} AND {right}"
    
    def _or(self, left, right): #or
        return f"{left} OR {right}"

    # def __and__(self, other) -> str:
    #     return f"{self} AND {other}"    
    
    # def __or__(self, other: Any) -> str:
    #     return f"{self} OR {other}"
    
    # def __ror__(self, other: Any) -> str:
    #     return f"{other} OR {self}"

    #compare_ops
    def _in(self, other): #in
        return f"{self} IN {other}"

    def _eq(self, other): # ==
        return f"{self} = {other}"

    # def __eq__(self, other: object) -> str:
    #     return f"({self} = {other})"
    
    #non-existent in python
    def _like(self, other):
        return f"{self} LIKE {other}"
    
    def __str__(self):
        return self.serialize(True)