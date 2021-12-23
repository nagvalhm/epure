from __future__ import annotations
from typing import Any, Dict
from .node import Node
from pathlib import Path
import os
import random
import re
import copy

class FileNode(Node):
    _dir_name:str
    heap = None
    root:Node = None
    registry:Dict[str, Node] = {}
    _storage:Node = None



    def __init__(self, name:str=None, storage:Node=None, name_has_root:bool=False) -> None:
        name = name or self.class_name()
        name_head = Path(name).name      

        node_path = self._get_node_path(name, storage, name_has_root, name_head)
        
        self._name = name_head
        self._path = node_path

        if not node_path in self.registry:
            self.registry[node_path] = self

    @classmethod
    def _get_node_path(cls, name:str, storage:Node, name_has_root:bool, name_head:str) -> str:
        storage_path = '' if not cls.root or name_has_root else cls.root.path
        if storage and storage.path:
            storage_path = storage.path

        name_tail = str(Path(name).parent)
        if name_tail != '.':
            storage_path = str(Path(storage_path).joinpath(name_tail))        

        node_path = str(Path(storage_path).joinpath(name_head))

        return node_path


    # def __new__(cls, name:str=None, storage:Node=None, name_has_root:bool=False) -> Any:
    #     name = name or cls.class_name()

        
    #     storage_path = '' if not cls.root or name_has_root else cls.root.path
    #     if storage and storage.path:
    #         storage_path = storage.path

    #     name_tail = str(Path(name).parent)
    #     if name_tail != '.':
    #         storage_path = str(Path(storage_path).joinpath(name_tail))

    #     name_head = Path(name).name

    #     node_path = str(Path(storage_path).joinpath(name_head))

    #     # if node_path in cls.registry:
    #     #     return cls.registry[node_path]
        
    #     self = super(FileNode, cls).__new__(cls)
        
    #     self._name = name_head
    #     self._path = node_path
    #     self.registry[self._path] = self

    #     return self



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
        if not self.root.contains(self):
            self.save()
        
        id = node.get_id()
        node_json = node.to_json()
        node_json = f'___{id}___: {node_json}'
        print(node_json)
        with open(self._path, "a+") as file:
            file_is_empty = os.path.getsize(self._path) == 0
            if(not file_is_empty):
                file.write("\n" + node_json)
            else:
                file.write(node_json)
        # res = self.get_link(node, id)
        return id



    def search(self, keys:Any) -> Any:
        res = []
        with open(self.path, 'r', encoding='UTF-8') as file:
            
            json_pattern = re.compile(r'(\{.*?\}$)')
            for line in file:
                if all(key in line for key in keys):

                    # json_pattern: Any = r'(\{.*?\}$)'
                    # line = re.findall(json_pattern, line)[0]                    
                    line = json_pattern.search(line).group()

                    res.append(line)
            return list(map(lambda item: Node.from_json(item), res))



    def contains(self, node: Node, deep: bool = True) -> bool:
        return bool(self.search([node.to_json()]))

       




    @property
    def storage(self) -> Node:
        if self._storage:
            return self._storage
        
        from .dirnode import DirNode
        storage_path = str(Path(self.path).parent)
        storage = self.registry[storage_path] if storage_path in self.registry\
            else DirNode(str(storage_path), name_has_root=True)

        self._storage = storage
        return self._storage
    

    
    @storage.setter
    def storage(self,storage:Node) -> None:
        raise AttributeError(f'to set {storage} as storage for {self} use save()')

