from ..savable import Savable
from ..resource import Resource

class Node(Savable):

    __exclude__:list

    def save(self, level:int=0, resource:Resource=None):
        pass


class TableNode(Node):
    table:Savable
    db:Resource