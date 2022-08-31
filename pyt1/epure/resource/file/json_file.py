from .file_storage import FileStorage
from ..savable import Savable
import jsonpickle
import json

class JsonFile(FileStorage):
    
    def serialize_for_update(self, savable: Savable, **kwargs) -> object:
        res = str(jsonpickle.encode(savable))
        return res

    def deserialize(self, json_obj: str, **kwargs) -> Savable:
        res = json.dumps(json_obj)
        res = jsonpickle.decode(res)
        return res