from typing import Any
from ..epure.resource.node.node import Node

def epure(storage:Any=None) -> Any:
    def epure_creator(cls:type) -> Node:
        return Node()
    return epure_creator

def connect(default_db='') -> bool:
    pass