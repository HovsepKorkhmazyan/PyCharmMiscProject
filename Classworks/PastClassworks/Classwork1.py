#1 /Sum
string_input = [1,5,1,7,10,0]
target = int(input("Enter the target value: "))
flag = False
for i in range(0,len(string_input)):
    for j in range(i+1,len(string_input)):
        if string_input[i] + string_input[j] == target:
            print(i,j)
            break
    if flag:
        break



#2 / Sorting
string_input = [1,5,1,7,10,0,6,1,8,9,12]
even_list = []
odd_list = []
for i in string_input:
  if i % 2 == 0:
      even_list.append(i)

  else:
      odd_list.append(i)
even_list.sort()
odd_list.sort()
even_list.extend(odd_list)
print(even_list)

#3 /Bubble Sort
string_input = [1,5,1,7,10,0,6,1,8,9,12]
for i in range(len(string_input)):
    for j in range(len(string_input)-i -1):
        if string_input[j] > string_input[j+1]:
            string_input[j], string_input[j+1] = string_input[j+1], string_input[j]
print(string_input)


#4 /Finding the longest word
string_input = input().split()
longest_word = ""

for word in string_input:
    if len(word) > len(longest_word):
        longest_word = word
print(f" The longest word is: {longest_word}")

#5Finding the most used letter
string_input = input("Enter a string: ")
most_letter = ""
max_count = 0
for i in string_input:
    if i.isalpha():
        letter_count = string_input.count(i)
        if letter_count > max_count:
            max_count = letter_count
            most_letter = i
if most_letter:
    print(f"The most used letter is '{most_letter}' with {max_count} occurrences.")
else:
    print("No letters found in the input.")


