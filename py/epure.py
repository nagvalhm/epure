class Box:
    mask = 0b0101
    def add():
        pass
    @staticmethod
    def get():
        pass
    def store():
        pass
    def take():
        pass

epure_box = {
    Box: None
}

def epure(storage):
    def decor(ep):        
        if Box not in ep.__bases__:            
            raise BaseException('Only box can be epured')
        
        epure_box[ep.__name__] = storage
        print("I got decorated")

        return ep
    return decor




@epure('lamp_st')
class Lamp(Box):
    def lamp_name():
        return "good"


lamp = Lamp()
# lamp.get()

print(lamp.mask)
# lamp = {
#     lamp_name = "good"
# }