from typing import Any
from .node import Node
import copy

class ENode(Node):
    
    def save(self, storage:Any=None) -> Any:        
        self_copy = copy.copy(self)

        self_fields = vars(self)
        copy_fields = vars(self_copy)
        for name in self_fields:
            val = self_fields[name]
            if isinstance(val, Node) and val._storage:
                del copy_fields[name]
                copy_fields[f'___{name}___'] = val.save()
        
        res = super(ENode, self_copy).save()
        del self_copy
        return res