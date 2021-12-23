from typing import Any, Sequence
from .node import Node
import copy

class ENode(Node):
    __exclude__:Sequence[Any] = []

    def save(self, storage:Any=None) -> Any:        
        self_copy = copy.copy(self)

        self_type = type(self)
        class_fields = vars(self_type)
        copy_fields = vars(self_copy)
        for name in class_fields:
            if not self.is_savable(name, copy_fields):
                continue
            val = copy_fields[name]
            if hasattr(val, 'save') and callable(val.save):
                del copy_fields[name]
                copy_fields[f'___{name}___'] = val.save()
        
        res = super(ENode, self_copy).save(storage)
        # if exec:
        #     storage = self.get_storage(storage)
        #     res = storage.exec(res)

        del self_copy
        return res

    def _proceed_attr(self, name: str, val: Any) -> Any:
        pass

    def save_script(self) -> str:
        pass

    def is_savable(self, atr_name: str, node_fields: dict[str, Any]) -> bool:
        return atr_name in node_fields and atr_name not in self.__exclude__
        # if atr_name[:2] == "__" and atr_name[-2:] == "__":
        #     return True
        