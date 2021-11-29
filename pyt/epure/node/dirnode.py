from __future__ import annotations
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from .filenode import FileNode

from typing import Optional
import os
from typing import Any
from .node import Node
from pathlib import Path
import shutil


class DirNode(FileNode):
    _instance = None
    _initialized = None

    # def __init__(self, storage:Any = None, name:str=None) -> None:
    #     return super().__init__(storage, name)



    def put(self, node:Node = None) -> Any:
        
        if self.contains(node):
            return node

        node_path = str(Path(self.path).joinpath(node.name))

        is_dir = isinstance(node, DirNode)
        if is_dir:
            node = DirNode(name=node_path, name_has_root=True)
            Path(node_path).mkdir(parents=True, exist_ok=True)
        else:
            node = FileNode(name=node_path, name_has_root=True)
            self._create_file(node_path)

        return node



    def delete(self, node:Node = None) -> Any:

        if node == self.root:
            raise SystemError

        if not self.contains(node):
            return False
       
        if Path(node.path).is_file():
            os.remove(node.path)
        else:
            shutil.rmtree(node.path)
        
        # str(Path(path).parent)
        
        return node.storage



    def contains(self, node:Node=None, deep:bool=True) -> bool:
        if not (node.path and Path(node.path).exists()):
            return False

        parent_path = Path(self.path).parts
        node_path = Path(node.path).parts

        if not deep:
            return parent_path == node_path[:-1]

        return parent_path <= node_path



    # def _full_path(self, path:str) -> str: 
    #     return os.path.join(self.root, path)

    # @property
    # def path(self) -> str:
    #     storage_path = os.curdir
    #     if self.storage:
    #         storage_path = self.storage.path
        
    #     res = os.path.join(storage_path, self.name)
    #     # res = str(os.path.normpath(res))
    #     return res       
            

    # def _path(self, node:Node=None, path:str=None) -> str:
    #     if node and path:            
    #         return str(os.path.join(path, node.name))

    #     if node and isinstance(node, FileNode):        
    #         path = os.path.join(node.dir_name, node.name)


    #     if not isinstance(path, str):
    #         raise TypeError('path must be str')

    #     return path



    def _create_file(self, path:str) -> None:
        parent_dir = Path(path).parent
        
        if not parent_dir.exists():
            parent_dir.mkdir(parents=True, exist_ok=True)
        open(path,"w")


FileNode.root = DirNode(name='config_test')
# FileNode.storage = DirNode.root