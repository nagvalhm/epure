# import tests
from .epure import *
# print(epure.Epure)
# from sys import modules
# print(modules['epure'])


class Cap:    
    ___cap_field___ = '___cap_field_val'
    __cap_field__ = '__cap_field_val'
    field = 'asdf'

    def out():
        return "cap out"

    # def find():
    #     pass
    # def search():
    #     pass
    # def save():
    #     pass

@epure()
class Shaker(Cap):
    ___shaker_field___ = '___shaker_field_val'
    __shaker_field__ = '__shaker_field_val'


# Shaker = Epure(Shaker, Node, store='')


print(issubclass(Shaker, Node))

print(Shaker.on_setattr)
shak = Shaker()


print(type(Epure))