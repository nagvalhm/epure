from __future__ import annotations
from typing import Any

from pyt.epure.node.node import Node
# from .sysnode import SysNode


class FileNode(Node):
    # storage = SysNode()
    name = None
    path = None
    def __init__(self, storage:Any=None, name:str=None, path:str=None) -> None:
        # self.name = name
        # self.path = path
        super().__init__(self)
        self.save()
    
    def save(self, storage:Any=None) -> Any:
        pass