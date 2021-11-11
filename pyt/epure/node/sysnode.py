from __future__ import annotations
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from .filenode import FileNode

from typing import Optional
import os
from typing import Any
from .node import Node
from pathlib import Path, WindowsPath
import re
import shutil

class SysNode(Node):
    _instance = None
    root = 'config'

    def __init__(self, storage: Any = None, name:str=None, *, root:str=None) -> None:
        self.storage = storage
        self.root = root
        return super().__init__(storage, name)



    def __new__(cls, storage:Any=None, root:str=None) -> Any:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance



    def put(self, node:Node = None, **kwargs:Any) -> Any:
        path = self._path(node, **kwargs)       
        
        if self.contains(path=path):
            return path

        full_path = self._full_path(path)
        is_dir = str(path).endswith("/")
        if is_dir:
            Path(full_path).mkdir(parents=True, exist_ok=True)
        else:
            self._create_file(full_path)

        return path



    def delete(self, node:Node = None, **kwargs:Any) -> Any:
        path = self._path(node, **kwargs)

        if not self.contains(path=path):
            return False

        full_path = self._full_path(path)        
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)
        
        return str(Path(path).parent)



    def contains(self, node:Node=None, **kwargs:Any) -> bool:
        path = self._path(node, **kwargs)
        return os.path.exists(self._full_path(path))



    def _full_path(self, path:str) -> str: 
        return os.path.join(self.root, path)



    def _path(self, node:Node=None, path:str=None) -> str:
        if node and path:            
            return str(os.path.join(path, node.name))

        if node and isinstance(node, FileNode):        
            path = node.path

        if not isinstance(path, str):
            raise Exception('path must be string')

        return path



    def _create_file(self, full_path:str) -> None:
        parent_dir = str(Path(full_path).parent)
        if not os.path.exists(parent_dir):
            Path(parent_dir).mkdir(parents=True, exist_ok=True)
        open(full_path,"w")

FileNode.storage = SysNode()