def sum_of_numbers(*args):
    return sum(args)

def number_of_rows(*args):
    return len(args)

def arithmetic_mean(*args):
    return sum(args) / len(args) if args else 0

def math_operations(*args):
    if len(args) < 2:
        return None
    addition = args[0] + args[1]
    subtraction = args[0] - args[1]
    multiplication = args[0] * args[1]
    division = args[0] / args[1] if args[1] != 0 else None
    return addition, subtraction, multiplication, division

def to_uppercase(s):
    return ''.join(chr(ord(char) - 32) if 'a' <= char <= 'z' else char for char in s)

def to_lowercase(s):
    return ''.join(chr(ord(char) + 32) if 'A' <= char <= 'Z' else char for char in s)

def to_title_case(s):
    words = s.split()
    return ' '.join(word.capitalize() for word in words)

def toggle_case(s):
    return ''.join(char.upper() if char.islower() else char.lower() for char in s)

def substring_between(s, n):
    return s[n:-n] if n < len(s) else ""

def longest_word(sentence):
    words = sentence.split()
    return max(words, key=len)

def most_used_letter(sentence):
    from collections import Counter
    letters = [char for char in sentence if char.isalpha()]
    return Counter(letters).most_common(1)[0][0] if letters else None

def most_used_letter_in_longest_word(sentence):
    longest = longest_word(sentence)
    return most_used_letter(longest)

def elements_at_index(s, n):
    if n < len(s):
        return s[n], s[-n-1] if n < len(s) else None
    return None

def is_palindrome(num):
    str_num = str(num)
    return str_num == str_num[::-1]

def closest_palindrome(num):
    lower = num - 1
    upper = num + 1
    while True:
        if is_palindrome(lower):
            return lower
        if is_palindrome(upper):
            return upper
        lower -= 1
        upper += 1

def product_of_first_and_last_digit(num):
    str_num = str(num)
    if len(str_num) < 2:
        return int(str_num) ** 2  # If single digit, return square
    first_digit = int(str_num[0])
    last_digit = int(str_num[-1])
    return first_digit * last_digit

def number_of_rows_in_list(lst):
    return len(lst)

def max_number_in_list(lst):
    return max(lst) if lst else None

def two_digit_even_numbers(lst):
    return [num for num in lst if 10 <= num < 100 and num % 2 == 0]

def arithmetic_mean_of_list(lst):
    return sum(lst) / len(lst) if lst else 0

def lengths_of_rows(lst):
    return [len(row) for row in lst]

def sorted_descending(lst):
    return sorted(lst, reverse=True)

def lines_sorted_by_length(lst):
    return sorted(lst, key=len, reverse=True)

def word_with_most_vowels(lst):
    vowels = 'aeiouAEIOU'
    def count_vowels(word):
        return sum(1 for char in word if char in vowels)
    return max(lst, key=count_vowels)

def sentence_with_most_words(lst):
    return max(lst, key=lambda sentence: len(sentence.split()))

def largest_number_in_sentence(sentence):
    import re
    numbers = re.findall(r'\d+', sentence)
    return max(numbers, key=int) if numbers else None

def oldest_person(people):
    return max(people, key=lambda person: person['age'])

def students_sorted_by_first_name(students):
    return sorted(students, key=lambda student: student['first_name'])

def university_with_longest_name(universities):
    return max(universities, key=lambda uni: len(uni['name']))
