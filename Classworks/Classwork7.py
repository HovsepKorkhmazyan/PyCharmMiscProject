# 1 With List
mstr1 = input()
mstr2 = input()
temp = []
for el in mstr1:
    if el not in mstr2:
        temp.append(el)
for el in mstr2:
    if el not in mstr1:
        temp.append(el)
print(', '.join(temp))

# 1 With Set
ms1 = set(mstr1)
ms2 = set(mstr2)
print(list(ms1.symmetric_difference(ms2)))

# 2
user_input = input().split()
symbol = input()
temp = []
for el in user_input:
    if el in symbol:
        temp.append(el)
print(', '.join(temp))

# 3
data = ["Cat1,100, Question1,Answer1", "Cat1, 200, Question2, Answer2", "Cat2,200, Question3,Answer3"]
temp = {}

for el in data:
    cat, point, quest, ans = el.split(',')
    cat = cat.strip()
    point = int(point.strip())
    quest = quest.strip()
    ans = ans.strip()

    if cat not in temp:
        temp[cat] = {}

    tmp = {"Question": quest, "Answer": ans}

    temp[cat][point] = tmp

print(temp)

# 4
words = ["cat", "dog", "elephant", "google"]
is_alphabetical = True
for i in range(len(words) - 1):
    if ord(words[[i][0]].lower()) > ord(words[i + 1][0].lower()):
        is_alphabetical = False
        break
    else:
        is_alphabetical = True
if is_alphabetical:
    print("Yes")
else:
    print("No")
