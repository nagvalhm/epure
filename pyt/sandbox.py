# import tests
from .epure import *
# print(epure.Epure)
# from sys import modules
# print(modules['epure'])

@epure(123)
class Car:
    pass

print(type(Car))