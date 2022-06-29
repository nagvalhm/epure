from ..savable import Savable
from pathlib import Path

class FileStorage(Savable):

    path: str

    def __init__(self, path:str):
        self.path = path
    
    def exists(self, path: str) -> bool:
        return Path(path).exists()