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
        pass



    def __new__(cls, storage:Any=None, name:str=None, name_has_root:bool=False) -> Any:
        name = name or cls.class_name()

        
        storage_path = '' if not cls.root or name_has_root else cls.root.path
        if storage and storage.path:
            storage_path = storage.path

        name_tail = str(Path(name).parent)
        if name_tail != '.':
            storage_path = str(Path(storage_path).joinpath(name_tail))

        name_head = Path(name).name

        node_path = str(Path(storage_path).joinpath(name_head))

        if node_path in cls.registry:
            return cls.registry[node_path]
        
        self = super(FileNode, cls).__new__(cls)
        # self = super(FileNode, cls).__new__(cls)
        self._name = name_head
        self._path = node_path
        self.registry[self._path] = self

        return self



    @property
    def path(self) -> str:
        if self._path:
            return str(self._path)
        return super().path



    @path.setter
    def path(self, path:Any) -> None:
        if self.root.contains(self):
            raise AttributeError(f'name of existing file cannot be set to {path}')
        
        self._path = path
        self._name = Path(path).name
        return
            


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

        self._storage = storage
        return self._storage
    

    
    @storage.setter
    def storage(self,storage:Any) -> None:
        raise AttributeError(f'to set {storage} as storage for {self} use save()')

