from __future__ import annotations
import os
from typing import Any

from pyt.epure.node.node import Node


class FileNode(Node):    

    def __init__(self, storage:Any=None, dir_name:str=None, name:str=None) -> None:
        self._name = name
        self._dir_name = dir_name
        super().__init__(self)
        self.save()
    


    def save(self, storage:Any=None) -> Any:
        pass
    


    @property
    def path(self) -> str:
        return os.path.join(self._dir_name, self._name)
    


    @property
    def dir_name(self) -> str:
        if not self._dir_name:
            self._dir_name = '.'
        return self._dir_name
    


    @dir_name.setter
    def dir_name(self, dir_name:str) -> None:
        if not dir_name.endswith("/"):
            self._dir_name = dir_name + '/'
            return
        self._dir_name = dir_name
        
