from .resource import Resource

class NodePromise:
    resource:Resource
    node_id:object
    def __init__(self, resource, node_id) -> None:
        self.resource = resource
        self.node_id = node_id

    def get(self):
        res = self.resource.read(node_id=self.node_id)[0]
        return res

class ElistPromise(NodePromise):
    py_type:type

    def __init__(self, resource, node_id, py_type) -> None:
        self.py_type = py_type
        return super().__init__(resource, node_id)

    def get(self):
        list_values = self.resource.read(eset_id=self.node_id)
        node = self.py_type(list_values)
        # setattr(res, field_name, node)
        return node

class FieldPromise(NodePromise):
    field_name:str
    def __init__(self, resource, node_id, field_name) -> None:
        self.field_name = field_name
        return super().__init__(resource, node_id)

    def get(self):
        res = self.resource.read([self.field_name], node_id=self.node_id)
        return getattr(res, self.field_name)