from .resource import Resource

class Savable(Resource):
    
    resource: Resource


    def save(self, level:int=0, resource:Resource=None):
        pass

    def serialize(self):
        pass

    def deserialize(self):
        pass