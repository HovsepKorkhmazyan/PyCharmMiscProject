#1
def filter(*args):
    tmp = [el for el in args if type(el) == int]
    return tmp
#2
def are_evens(*args):
    for el in args:
        if el % 2 != 0:
            return False
    return True
#4
def sort_by_arguments(*args):
    temp_d = {
        }
    for el in args:
        key = type(el).__name__
        if key in temp_d:
            temp_d[key].append(el)
        else:
            temp_d[key] = [el]
    return temp_d
