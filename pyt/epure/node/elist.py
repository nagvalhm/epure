from .enode import *
from .node import *
from typing import Any
import copy

class EList(ENode, list[Any]):

    def save(self, storage:Any=None) -> Any:
        
        for index in range(0, len(self)):
            item = self[index]
            if hasattr(item, 'save') and callable(item.save):
                self._save_node(item)
                
        
        return super().save(storage)

    def _save_node(self, item:Node) -> Any:        
        return item.save()