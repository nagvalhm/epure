import os
from .node import Node
from pathlib import Path
import re
import shutil

class SysNode(Node):
    _instance = None
    heap = 'config'

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance    

    def put(self, node=None, path=None):
        path = self.path(node, path)
        # if not path:
        #     if not self.path:
        #         self.path = SysNode.heap = 'config'
        #     if not self.name:
        #         self.name = re.sub(r'(?<!^)(?=[A-Z])', '_', type(self).__name__).lower  #to snake_case
        #     path = Path(self.path + "/" + self.name)
        
        
        if self.contains(path=path):
            return path

        full_path = self._full_path(path)
        is_dir = str(path).endswith("/")
        if is_dir:
            Path(full_path).mkdir(parents=True, exist_ok=True)
        else:
            self._create_file(full_path)

        return path



    def delete(self, node=None, path=None):
        path = self.path(node, path)

        if not self.contains(path=path):
            return False

        full_path = self._full_path(path)        
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)
        
        return str(Path(path).parent)


    def contains(self, node=None, path=None) -> bool:
        path = self.path(node, path)
        return os.path.exists(self._full_path(path))


    def _full_path(self, path):        
        return os.path.join(self.heap, path)

    def path(self, node=None, path=None):

        if node and path:            
            return os.path.join(path, node.file_name)

        if node:
            path = node.path

        return path


    def _create_file(self, full_path:str):
        parent_dir = str(Path(full_path).parent)
        if not os.path.exists(parent_dir):
            Path(parent_dir).mkdir(parents=True, exist_ok=True)
        open(full_path,"w")
