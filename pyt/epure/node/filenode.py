from __future__ import annotations
import os
from typing import Any
from pyt.epure.node.node import Node


class FileNode(Node):
    _dir_name:str
    
    def __init__(self, storage:Any=None, name:str=None, dir_name:str=None, save:bool=True) -> None:

        if dir_name and not dir_name.endswith("/"):
            dir_name = dir_name + '/'

        self._dir_name = dir_name
        super().__init__(storage, name)

        if save:
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
        raise AttributeError(f'dir_name of existing file cannot be set to {dir_name}')



    @property
    def name(self) -> str:
        return super().name



    @name.setter
    def name(self, name:str) -> None:
        raise AttributeError(f'name of existing file cannot be set to {name}')


    def put(self, node:Node=None, **kwargs:Any) -> None:
        node_json = node.to_json()
        print(node_json)
        with open(os.path.join('config_test/',self.name), "a") as file:
            file.write(node_json)

