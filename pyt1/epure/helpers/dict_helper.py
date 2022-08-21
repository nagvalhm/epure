def reverse_dict(dict):
    res = {val: key for key, val in dict.items()}
    return res