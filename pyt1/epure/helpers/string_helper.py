



def is_float(val: str) -> bool:
    if val is None:
            return False
    first_char = val[0]
    if not (first_char == '-' or first_char.isdecimal()):
        return False

    other_chars = val[1:]
    return other_chars.replace('.', '', 1).isdecimal()

def is_int(val: str, val_is_float:bool=None) -> bool:
    if val_is_float is None:
        val_is_float = is_float(val)
   
    return (val_is_float and val.count('.') == 0)

def is_bool(val:str) -> bool:
    return val.lower() in ('true', 'false')