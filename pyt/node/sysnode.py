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
    def put(path):
        # if not path:
        #     if not self.path:
        #         self.path = SysNode.heap = 'config'
        #     if not self.name:
        #         self.name = re.sub(r'(?<!^)(?=[A-Z])', '_', type(self).__name__).lower  #to snake_case
        #     path = Path(self.path + "/" + self.name)
        path = os.path.join(SysNode.heap, path)
        if os.path.exists(path):
            return path
        if not str(path).endswith("/"):
            parent_dir = Path(path).parent
            Path(parent_dir).mkdir(parents=True, exist_ok=True)
            open(path,"w")
        else:
            Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def delete(path):
        if not os.path.exists(path):
            return False
        if os.path.isfile(path):
            endfile = os.path.basename(path)
            os.remove(path)
            path = str(path.as_posix())
            path = path.removesuffix(f'/{endfile}')
            return path
        endfile = os.path.basename(path)
        shutil.rmtree(path)
        
        # path = path.split('/')              
        # del path[-1]
        # path = '/'.join(path)
        # while [path] != [SysNode.heap]:     #comparing to root dir
        #     shutil.rmtree(path)
        #     path = path.split('/')
        #     del path[-1]
        #     path = '/'.join(path)