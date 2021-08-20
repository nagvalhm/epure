class Box:
    mask = 0b0101
    def add():
        pass
    def get():
        pass
    def store():
        pass
    def take():
        pass

epure_box = {
    Box: None
}

class Epure(type):
    def __init__(sels, store):
        sels.store = store   

    # def __call__(self, ep):
    #     def init_substitute():        
    #         if Box not in ep.__bases__:            
    #             raise BaseException('Only box can be epured')
            
    #         ep.get = self.get_decorator(ep.get)
    #         # epure_box[ep.__name__] = storage
    #         print("I got decorated")

    #         return ep

    #     return init_substitute

    def decorator_get(ep, origin_get):
        def substitute_get(self=None):
            # if type(self) is type:
            if self is None:
                return Epure.get(ep)
            else:
                return origin_get()
        
        return substitute_get

    
    def get(self):
        pass

def epure(storage):
    def decor(ep):        
        if Box not in ep.__bases__:            
            raise BaseException('Only box can be epured')
        
        epure_box[ep.__name__] = storage
        ep.get = Epure.decorator_get(ep, ep.get)
        print("I got decorated")

        return ep
    return decor




@epure("lamp_store")
class Lamp(Box):
    def lamp_name():
        return "good"


lamp = Lamp()
Lamp.get()
lamp.get()



print(lamp.mask)
# lamp = {
#     lamp_name = "good"
# }