function getType(obj){
    not_primitive = obj !==null && (typeof obj == "object" || typeof obj == "function");
    if(not_primitive && Reflect.has(obj, 'constructor')){
        return obj.constructor.name;
    }

    return typeof(obj);
    // if (obj === null){
    //     return typeof(obj);
    // }
    
    // if (Reflect.has(obj, 'constructor')){
    //     return obj.constructor.name;
    // }else {
    //     return typeof(obj);
    // }
    // (typeof(obj) === 'object' && Reflect.has(obj, constructor)) ? obj.constructor.name : typeof(obj);
}

function clas_decor(cls){
    temp_obj = new cls;
    keys = Reflect.ownKeys(temp_obj);
    for(key in keys){
        key = keys[key];
        obj = temp_obj[key];

        obj_type = getType(obj);         
        console.log(key, ',', obj, obj_type);
    }
    
    delete temp_obj;
    return cls;
}
    // for atr_name in dir(cls):
    //     obj = getattr(cls, atr_name, None)
    //     if atr_name[:2] == "__" and atr_name[-2:] == "__":
    //         continue
    //     print(atr_name, type(obj))
    

class test2{
    test2_field1 = 5;
}

class Car{
    whie = 'black';
}



// @clas_decor
test_cls = clas_decor(
class test_cls extends Car {
    test_field1 = String;
    test_field2 = 'hi';
    test_field3 = null;
    test_field4 = new test2();
}
);

tmp = new test_cls();
// console.log(tmp.test_field4.test2_field1)
console.log('cons', tmp.constructor.name);