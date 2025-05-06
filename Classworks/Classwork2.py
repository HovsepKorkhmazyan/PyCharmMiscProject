#1 Fibonacci sequence
import string

n = int(input("Enter a number: "))
fib_num = [0,1]
for i in range(2,n):
    fib_num.append(fib_num[i-1]+ fib_num[i-2])
    print(fib_num)
if n==1:
    print(fib_num[0])
else:
    print(fib_num)


#2 Even Numbers in range
n = int(input("Enter a number: "))
m = int(input("Enter a number: "))

if n > m:
    n, m = m, n
if n % 2 ==1:
    n+=1
for i in range (n,m,2):
    print(i)

#3 Printing consonants
string_input = input("Enter a string: ").lower()
cons = ""

for i in string_input:
    if i.isalpha() and i not in "aeiou":
        con = cons + i
print(cons)

#4 Number Sorting 3 Digit
num = []
while True:
    if string_input == "stop":
        break
    if string_input.isdigit() and len(string_input)==3:
                num.append(int(string_input))
    num.sort()
    print(num)

#5 Number Guessing Game
user_guess = int(input("Enter a number: "))
num_to_guess = 50
attempts = 10
while attempts >=1:
    if user_guess == num:
        print("Congratulations! You guessed it!")
        break
    if abs(num_to_guess - user_guess) >= 10:
        print("Wrong guess too far.")
        attempts -= 1
    else:
        print("You are getting nearer")
        attempts -= 1

    if attempts == 0:
        print("Game Over!")
        print(f"The correct number is {num_to_guess}")
        break

#6 Finding the longest word and most often used letter
string_input = input("Enter a string: ").lower().split()
max_count = 0
most_used_letter = ""
string_input.sort(key=len)
longest_word = string_input[-1]
for i in longest_word:
    if i.isalpha():
        letter_count = string_input.count(i)
        if letter_count > max_count:
            max_count = letter_count
            most_used_letter = i
print(f"The longest word is: {longest_word}. The most often used letter is {most_used_letter} ")






