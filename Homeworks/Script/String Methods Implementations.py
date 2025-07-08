def to_uppercase(string_input):
    uppercase_string = ""
    for e in string_input:
        if 'a' <= e <= 'z':
            uppercase_string += chr(ord(e) - 32)
        else:
            uppercase_string += e
    return uppercase_string


def to_lowercase(string_input):
    lowercase_string = ""
    for e in string_input:
        if 'A' <= e <= 'Z':
            lowercase_string += chr(ord(e) + 32)
        else:
            lowercase_string += e
    return lowercase_string


def ends_with(string_input, char_to_check):
    return string_input and string_input[-1] == char_to_check


def starts_with(string_input, char_to_check):
    return string_input and string_input[0] == char_to_check


def contains_space(string_input):
    return any(e == " " for e in string_input)


def find_substring(string_input, value_to_find):
    position = string_input.find(value_to_find)
    return position


def is_all_alpha(string_input):
    return all('A' <= e <= 'Z' or 'a' <= e <= 'z' for e in string_input)


def is_lowercase(string_input):
    return all('a' <= e <= 'z' for e in string_input)


def is_uppercase(string_input):
    return all('A' <= e <= 'Z' for e in string_input)


def count_character(string_input, value_to_count):
    return string_input.count(value_to_count)


def to_title_case(string_input):
    mod_string = ""
    capitalize_next = True
    for e in string_input:
        if e == " ":
            mod_string += e
            capitalize_next = True
        else:
            if capitalize_next:
                if 'a' <= e <= 'z':
                    mod_string += chr(ord(e) - 32)
                else:
                    mod_string += e
                capitalize_next = False
            else:
                mod_string += e
    return mod_string


def zfill_string(string_input, zeros_to_fill):
    if string_input and string_input[0] == '-':
        return '-' + '0' * (zeros_to_fill - len(string_input) + 1) + string_input[1:]
    else:
        return '0' * (zeros_to_fill - len(string_input)) + string_input


def index_of_substring(string_input, substring):
    found_index = string_input.find(substring)
    if found_index != -1:
        return found_index
    else:
        raise ValueError(f"'{substring}' is not in the string")


def is_title_case(string_input):
    is_title_case = True
    at_start_of_word = True
    for e in string_input:
        if e == " ":
            at_start_of_word = True
        else:
            if at_start_of_word:
                if not ("A" <= e <= "Z"):
                    is_title_case = False
                    break
            else:
                if not ("a" <= e <= "z"):
                    is_title_case = False
                    break
            at_start_of_word = False
    return is_title_case


def is_decimal(string_input):
    return all('0' <= e <= '9' for e in string_input)


def replace_character(string_input, value_to_replace, replacement_value, how_many_to_replace):
    new_string = ""
    count = 0
    for e in string_input:
        if e == value_to_replace and count < how_many_to_replace:
            new_string += replacement_value
            count += 1
        else:
            new_string += e
    return new_string


def split_string(string_input, delimiter=" "):
    return string_input.split(delimiter)


def strip_string(string_input):
    return string_input.strip()
