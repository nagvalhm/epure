from .elist import *
from .enode import *
from .node import *
from typing import Any

class NodeList(EList):

    def __init__(self, link_storage:Node, name:str=None, storage:Node = None) -> None:
        self.link_storage = link_storage
        super().__init__(name, storage)

    def _save_node(self, item:Node) -> Any:
        item.save()        
        self.link_storage.put(item.link())


    def append(self, item: Node) -> None:
        if not isinstance(item, Node):
            raise TypeError('item must be Node')
        return super().append(item)