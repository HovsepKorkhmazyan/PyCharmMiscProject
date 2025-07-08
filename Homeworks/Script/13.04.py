# 1
string_input = input("Enter a string: ")
letters_alphabetically = []

for letter in string_input:
    if letter.isalpha():
        letters_alphabetically.append(letter)
letters_alphabetically.sort()
print(letters_alphabetically)

# 2
digits_sorted = []
for digit in string_input:
    if digit.isdigit():
        digits_sorted.append(digit)
digits_sorted.sort()
print(digits_sorted)

# 3
string_input = input("Enter a string: ").split()
words_reversed = []
for word in letters_alphabetically:
    if word.isalpha():
        words_reversed.append(word[::-1])
print(words_reversed)

# 4
number = int(input("Enter a number: "))
if number < 2:
    print(f"{number} is not a PRIME number.")
else:
    is_prime = True
    for i in range(2, number):
        if number % i == 0:
            is_prime = False
            break
    if is_prime:
        print(f"YES the{number} is a PRIME number.")
    else:
        print(f"NO the {number} is not a PRIME number.")
