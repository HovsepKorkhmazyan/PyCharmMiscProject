#1  Convert all letters in a given sentence to uppercase using recursion:

def to_uppercase_recursive(sentence):
    if not sentence:
        return ""
    else:
        return sentence[0].upper() + to_uppercase_recursive(sentence[1:])

input_sentence = "Hello, World!"
result = to_uppercase_recursive(input_sentence)
print(result)

#2 Calculate the sum of all numbers up to a given number:

def rsum(n):
    if n == 0:
        return 0
    else:
        return n + rsum(n - 1)

number = 5
result = rsum(number)
print(result)

#3 Check if a given string is a palindrome:

def is_palindrome(s):
    if len(s) <= 1:
        return True
    else:
        if s[0] == s[-1]:
            return is_palindrome(s[1:-1])
        else:
            return False

input_string = "racecar"
result = is_palindrome(input_string)
print(result)