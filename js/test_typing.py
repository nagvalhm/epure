# type: ignore
from typing import Any, Dict, Tuple


# class meta_test(type):

#     def __new__(mcls, name: str, cls_bases: Tuple[type, ...], 
#         namespace: dict[str, Any], **kwds: Any) -> meta_test:

#         print("ok")
#         res = super().__new__(mcls, name, cls_bases, namespace)

#         return res

    # def __setattr__(cls, atr_name: str, value: Any) -> None:
    #     mcls = type(cls)

class Car:
    whie = 'black'


def clas_decor(cls):
    for atr_name in dir(cls):
        obj = getattr(cls, atr_name, None)
        if atr_name[:2] == "__" and atr_name[-2:] == "__":
            continue
        print(atr_name, type(obj))
    return cls

class test2:
    test2_field1 = 5


@clas_decor
class test_cls(Car):
    test_field1 = str
    test_field2 = 'hi'
    test_field3 = None
    test_field4 = test2()

tmp = test_cls()
print(tmp.test_field4.test2_field1)