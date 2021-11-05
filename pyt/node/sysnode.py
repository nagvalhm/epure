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
    
    # def put(self, path=None, node=None)
    def put(self, path):
        
        # if not path:
        #     if not self.path:
        #         self.path = SysNode.heap = 'config'
        #     if not self.name:
        #         self.name = re.sub(r'(?<!^)(?=[A-Z])', '_', type(self).__name__).lower  #to snake_case
        #     path = Path(self.path + "/" + self.name)
        
        is_dir = str(path).endswith("/")

        if self.path_exists(path):
            return path

        full_path = self.full_path(path)
        if is_dir:
            Path(full_path).mkdir(parents=True, exist_ok=True)
        else:
            self._create_file(full_path)

        return path



    def delete(self, path):

        if not self.path_exists(path):
            return False

        full_path = self.full_path(path)        
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)
        
        return str(Path(path).parent)


    def path_exists(self, path:str, is_dir: bool=None) -> bool:
        return os.path.exists(self.full_path(path))
        

    def full_path(self, path:str):
        return os.path.join(self.heap, path)


    # def path_exists(self, path:str, is_dir: bool=None) -> bool:
    #     is_dir = is_dir or str(path).endswith("/")

    #     if os.path.exists(path):
    #         if ((is_dir and os.path.isdir(path)) 
    #         or (not is_dir and os.path.isfile(path))):
    #             return True
    #     return False

    def _create_file(self, path:str):
        parent_dir = str(Path(path).parent)
        if not os.path.exists(parent_dir):
            Path(parent_dir).mkdir(parents=True, exist_ok=True)
        open(path,"w")
