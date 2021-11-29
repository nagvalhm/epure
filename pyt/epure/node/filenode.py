from __future__ import annotations
from typing import Any, Dict
from .node import Node
from pathlib import Path

class FileNode(Node):
    _dir_name:str
    heap = None
    root:Node = None
    registry:Dict[str, Node] = {}
    _storage:Node = None

    def __init__(self, storage:Any=None, name:str=None, name_has_root:bool=False) -> None:
        name = name or self.name        

        from .dirnode import DirNode

        storage_path = '' if not self.root or name_has_root else self.root.path
        if storage and storage.path:
            storage_path = storage.path

        name_tail = str(Path(name).parent)
        if name_tail != '.':
            storage_path = str(Path(storage_path).joinpath(name_tail))
        
        # if storage:
        #     self._storage = DirNode(name=str(storage_path))

        name_head = Path(name).name
        self._name = name_head
        # if storage_path:
        self._path = str(Path(storage_path).joinpath(name_head))
        self.registry[self._path] = self
        # if dir_name and not dir_name.endswith("/"):
        #     dir_name = dir_name + '/'

        # self._dir_name = dir_name
        # super().__init__(storage, name)

        # if storage:
        #     self.save()

        


    @property
    def path(self) -> str:
        if self._path:
            return self._path
        return super().path



    @path.setter
    def path(self, path:Any) -> None:
        if self.root.contains(self):
            raise AttributeError(f'name of existing file cannot be set to {path}')
        
        self._path = path
        self._name = Path(path).name
        return
            



    # @property
    # def dir_name(self) -> str:
    #     if not self._dir_name:
    #         return './'
    #     return self._dir_name
    


    # @dir_name.setter
    # def dir_name(self, dir_name:str) -> None:
    #     raise AttributeError(f'dir_name of existing file cannot be set to {dir_name}')



    @property
    def name(self) -> str:
        return super().name



    @name.setter
    def name(self, name:str) -> None:
        if self.root.contains(self):
            raise AttributeError(f'name of existing file cannot be set to {name}')
        # super(FileNode, self).__class__
        super_setter = Node.name
        if not isinstance(super_setter, property):
            raise TypeError('super_setter must be property')
        super_setter.__set__(self, name)
        


    def put(self, node:Node=None) -> Any:
        node_json = node.to_json()
        if not self.root.contains(self):
            raise FileNotFoundError()
        print(node_json)
        with open(self._path, "a") as file:
            file.write(node_json)



    @property
    def storage(self) -> Node:
        if self._storage:
            return self._storage
        
        from .dirnode import DirNode
        storage_path = str(Path(self.path).parent)
        storage = self.registry[storage_path] if storage_path in self.registry\
            else DirNode(name=str(storage_path), name_has_root=True)

        # if str(storage_path) in self.registry:
        #     storage = self.registry[str(storage_path)]
        # else:
        #     # storage_path = Path(*storage_path.parts[1:])
        #     storage = DirNode(name=str(storage_path), name_has_root=True)
        # if not isinstance(storage, Node):
        #     raise TypeError('storage must be Node')
        # if storage_path in self.registry:
        #     storage = self.registry[storage_path]
        # else:
        #     storage = DirNode(storage_path)
        # if self.root and self.root.contains(storage):
        self._storage = storage
        return self._storage
        
    

    
    @storage.setter
    def storage(self,storage:Any) -> None:
        raise AttributeError(f'to set {storage} as storage for {self} use save()')

