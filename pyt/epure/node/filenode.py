from __future__ import annotations
import os
from typing import Any
import json

from pyt.epure.node.node import Node


class FileNode(Node):    
    _dir_name:str
    
    def __init__(self, storage:Any=None, name:str=None, dir_name:str=None) -> None:        
        self._dir_name = dir_name
        super().__init__(self, name)
        self.save()
    


    @property
    def path(self) -> str:
        return os.path.join(self.dir_name, self.name)
    


    @property
    def dir_name(self) -> str:
        if not self._dir_name:
            return './'
        return self._dir_name
    


    @dir_name.setter
    def dir_name(self, dir_name:str) -> None:
        if not dir_name.endswith("/"):
            self._dir_name = dir_name + '/'
            return
        self._dir_name = dir_name


    def put(self, node:Node=None, **kwargs:Any) -> None:
        node_json = json.dumps(self.__dict__, ensure_ascii=False, default=str)
        with open(self.path, "a+") as file_object:
            file_object.seek(0)
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            file_object.write(node_json) 
