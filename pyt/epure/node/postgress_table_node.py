from __future__ import annotations
from typing import Any, Dict
from .tablenode import TableNode
from .node import Node

class PostgressTableNode(TableNode):

    def put(self, node:Node=None) -> Any:
        pass