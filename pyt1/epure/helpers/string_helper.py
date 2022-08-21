

def screen_regex_specials(val:str):
    res = ''
    specials = ('.', '+', '*', '?', '^', '$', '(', ')', '[', ']', '{', '}', '|', '\\', '<', '>')
    for char in val:
        if char in specials:
            res += f"\\{char}"
            continue
        res += char
    return res

#return dict: {open bracket: close bracket}
def find_parentheses(val:str) -> dict:
    res = {}
    pstack = []

    for i, c in enumerate(val):
        if c == '(':
            pstack.append(i)
        elif c == ')':
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            res[pstack.pop()] = i

    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))

    return res


def is_float(val: str) -> bool:
    if val is None:
            return False
    first_char = val[0]
    if not (first_char == '-' or first_char.isdecimal()):
        return False

    other_chars = val[1:]
    if other_chars == '':
        return True
    return other_chars.replace('.', '', 1).isdecimal()

def is_int(val: str, val_is_float:bool=None) -> bool:
    if val_is_float is None:
        val_is_float = is_float(val)
   
    return (val_is_float and val.count('.') == 0)

def is_bool(val:str) -> bool:
    return val.lower() in ('true', 'false')