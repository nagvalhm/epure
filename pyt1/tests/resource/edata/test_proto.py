


class A:
    pass
class B(A):
    pass
class C(B):
    pass

def test_proto():
    a = C.__bases__
    print(a)