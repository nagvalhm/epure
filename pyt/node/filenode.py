
from .sysnode import SysNode


class FileNode:
    heap = SysNode()

    def __init__(self, storage=None, name=None, path=None):
        self.name = name
        self.path = path
        super().__init__(self)
        self.save()