from .resource import Resource

class NodePromise:
    resource:Resource
    node_id:object
    def __init__(self, resource, node_id) -> None:
        self.resource = resource
        self.node_id = node_id

    def __get__(self, obj, objtype=None):
        return self.resource.read(node_id=self.node_id)


class FieldPromise(NodePromise):
    field_name:str
    def __init__(self, resource, node_id, field_name) -> None:
        self.field_name = field_name
        return super().__init__(resource, node_id)

    def __get__(self, obj, objtype=None):
        res = self.resource.read([self.field_name], node_id=self.node_id)
        return getattr(res, self.field_name)