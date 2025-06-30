# 1
def main():
    with open("a.txt", "r") as infile, \
            open("numbers", "w") as num_file, \
            open("words", "w") as word_file:
        for line in infile:
            stripped_line = line.strip()
            try:

                float(stripped_line)

                num_file.write(stripped_line + "\n")
            except ValueError:

                word_file.write(stripped_line + "\n")


if __name__ == "__main__":
    main()


# 2

def sum_element(e):
    try:
        return sum(e)
    except TypeError:
        return e


def max_sum_nested_list(nested_list):
    sums = [sum_element(sublist) for sublist in nested_list]
    max_index = sums.index(max(sums))
    return nested_list[max_index]


numbers = [1, 2, 5, [1, 2, 3], [4, 5], [6, 7, 8, 9], [10]]
result = max_sum_nested_list(numbers)
print(result)
