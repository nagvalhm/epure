from .resource import Resource

class DataPromise:
    resource:Resource
    data_id:object
    def __init__(self, resource, data_id) -> None:
        self.resource = resource
        self.data_id = data_id

    def get(self):
        res = self.resource.read(data_id=self.data_id)[0]
        return res

class ElistPromise(DataPromise):
    py_type:type

    def __init__(self, resource, data_id, py_type) -> None:
        self.py_type = py_type
        return super().__init__(resource, data_id)

    def get(self):
        list_values = self.resource.read(eset_id=self.data_id)
        data = self.py_type(list_values)
        # node = self.py_type[self.py_type.collection_epure](list_values)
        return data
    
class EsetPromise(DataPromise):
    py_type:type

    def __init__(self, resource, data_id, py_type) -> None:
        self.py_type = py_type
        return super().__init__(resource, data_id)

    def get(self):
        # list_values = self.resource.read(eset_id=self.data_id)
        data = self.py_type([], self.resource)
        data.data_id = self.data_id
        # node = self.py_type[self.py_type.collection_epure](list_values)
        return data

class FieldPromise(DataPromise):
    field_name:str
    def __init__(self, resource, data_id, field_name) -> None:
        self.field_name = field_name
        return super().__init__(resource, data_id)

    def get(self):
        res = self.resource.read([self.field_name], data_id=self.data_id)
        return getattr(res, self.field_name)