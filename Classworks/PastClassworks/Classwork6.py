# 1
user_input = input().lower()
md = {}
for i in user_input:
    if i.isalpha():
        if i in md:
            md[i] += 1
        else:
            md[i] = 1
print(md)

# 2
letters = []
for i in user_input:
    if i.isalpha() and i not in letters:
        letters.append(i)

if len(letters) == 26:
    print("Yes")
else:
    print("No")

#3
    letters = {
        "vowels": [],
        "consonants": []
    }
while True:
    if user_input.lower() == "stop":
        break
    else:
        for el in user_input:
            if el.isalpha():
                if el.lower() in "aeiou":
                    letters["vowels"].append(el)
                else:
                    letters["consonants"].append(el)

    letters["vowels"].sort()
    letters["consonants"].sort()
    print(letters)
