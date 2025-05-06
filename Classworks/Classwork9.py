#1 Getting the even numbers
def get_even_numbers(my_list):
    even_numbers = []
    for number in my_list:
        if isinstance(number, int) and number % 2 == 0:
            even_numbers.append(number)
    return even_numbers


#2 Getting the indexes of the symbols
def get_indexes(my_str, symbol):
    temp = []
    for i in range(len(my_str)):
        if my_str[i] == symbol:
            temp.append(i)
    return temp

#3
def collect_data():
    temp_d = {
        "strings": [],
        "numbers": [],
    }
    while True:
        user_input = input()
        if user_input.lower() == "stop":
            return temp_d
        if user_input.isalpha():
            temp_d["strings"].append(user_input)
        elif user_input.isdigit():
            temp_d["numbers"].append(int(user_input))

def string_upper(my_ls):
    return [el.upper() for el in my_ls]

def num_double(my_ls):
    return [el * 2 for el in my_ls]

def words_reversed(my_str):
    return [el[::-1] for el in my_str.split()]

#4
def getting_user_input():
    user_input = input().split()
    return user_input

def find_longest_word(my_ls):
    longest_word = my_ls[0]
    for word in my_ls[1:]:
        if len(word) > len(longest_word):
            longest_word = word
    return longest_word

def find_most_used_char(my_ls):
    combined_str = ''.join(my_ls)
    char_count = {}
    for char in combined_str:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    return char_count


def get_most_used_char(my_ls):
    char_count = {}
    combined_str = ''.join(my_ls)

    for char in combined_str:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    most_common_char = None
    max_count = 0
    for char, count in char_count.items():
        if count > max_count:
            max_count = count
            most_common_char = char
    return most_common_char

user_input = getting_user_input()
longest_word = find_longest_word(user_input)
most_used_char = get_most_used_char(user_input)
char_count = find_most_used_char(user_input)
