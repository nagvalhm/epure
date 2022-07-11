from .file_storage import FileStorage
from ..savable import Savable
import jsonpickle

class JsonFile(FileStorage):
    
    def serialize(self, resource: Savable, method: str = '', **kwargs) -> object:
        return str(jsonpickle.encode(resource))