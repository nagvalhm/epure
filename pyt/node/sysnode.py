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
        if not os.path.exists(path):
            path = Path(os.path.join(SysNode.heap, path))
            path_dir = os.path.dirname(path)
            if not os.path.exists(path_dir):
                Path(path_dir).mkdir(parents=True, exist_ok=True)
            open(path,"w")
        return path

    def __del__(path):
        if os.path.exists(path):
            if not os.path.isdir(path):
                os.remove(path)
                # path = Path(str(path))           #WindowsPath -> str path : \\dir\\file
                path = str(path.as_posix())
                path = path.split('/')              
                del path[-1]
                path = '/'.join(path)
            while [path] != [SysNode.heap]:     #comparing to root dir
                shutil.rmtree(path)
                path = path.split('/')
                del path[-1]
                path = '/'.join(path)
        else:
            return False
