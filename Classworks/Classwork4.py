from itertools import count

while True:
    string_input = input("Enter words (or type 'stop' to end): ").split()

    if string_input == ["stop"]:
        break

    temp = {}

    for el in string_input:
        if el in temp:
            temp[el] += 1
        else:
            temp[el] = 1

    print("Word counts:", temp)

    max_count = 0
    max_word = ""

    for k, v in temp.items():
        if v > max_count:  # Use v instead of count
            max_count = v
            max_word = k

    if max_word:  # Check if there is a max_word
        print(f"The word with the highest count is '{max_word}' with {max_count} occurrences.")

#2
md1 = {"a":10,"b":20,"c":30}
md2 = {"b":10,"c":20,"d":30}
md3 = {}

for k, v in md1.items():
    if k in md2:
        md2[k] += v
    else:
        md2[k]= v
print(md2)
