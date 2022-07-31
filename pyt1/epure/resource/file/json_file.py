from .file_storage import FileStorage
from ..savable import Savable
import jsonpickle

class JsonFile(FileStorage):
    
    def serialize_for_update(self, savable: Savable, **kwargs) -> object:
        return str(jsonpickle.encode(savable))