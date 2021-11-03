import os
from .node import Node
from pathlib import Path
import re

class SysNode(Node):
    _instance = None

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
            path_dir = os.path.dirname(path)
            if not os.path.exists(path_dir):
                os.mkdir(path_dir)
            with Path(path).open("w") as f:
                f.write('writing')
        return path

