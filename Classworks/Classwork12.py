#1
def largest_list(*args):
    largest = []
    max_sum = 0
    for el in args:
        if isinstance(el, list):
            current_sum = sum(el)
            if current_sum > max_sum:
                max_sum = current_sum
                largest.append(el)
    return largest

#2
def find_same_index(*args):
    final = []
    min_len = min(len(el) for el in args)
    for i in range(min_len):
        tmp = []
        for el in args:
            tmp.append(el[i])
        if len(set(tmp)) == 1:
            final.append(tmp[0])
    print(final)

    #3
    ml = [7,2,5,6,1,3,4,8,9,11]

    def interleave_even_odd(*args):
        evens = [x for x in args if x % 2 == 0]
        odds = [x for x in args if x % 2 != 0]
        result = []
        i = 0
        j = 0
        while i < len(evens) and j < len(odds):
            result.append(evens[i])
            result.append(odds[j])
            i += 1
            j += 1
        while i < len(evens):
            result.append(evens[i])
            i += 1
        while j < len(odds):
            result.append(odds[j])
            j += 1
        print(result)


