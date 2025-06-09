#1 Recursive Approach

def flatten_recursive(nested_list):
    flat_list = []
    for element in nested_list:
        if isinstance(element, list):
            flat_list.extend(flatten_recursive(element))
        else:
            flat_list.append(element)
    return flat_list


nested_list = [1, [2, [3, 4], 5], 6]
flat_list = flatten_recursive(nested_list)
print(flat_list)

#2 Linear Approach

def flatten_iterative(nested_list):
    flat_list = []
    stack = list(nested_list)

    while stack:
        element = stack.pop()
        if isinstance(element, list):
            stack.extend(reversed(element))
        else:
            flat_list.append(element)

    return flat_list


nested_list = [1, [2, [3, 4], 5], 6]
flat_list = flatten_iterative(nested_list)
print(flat_list)

