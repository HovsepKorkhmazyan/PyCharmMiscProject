# 1
num = int(input())
a = 0
b = 1
for i in range(num):
    print(a)
    fib = a + b
    a = b
    b = fib
# 2
sen = input().lower()
vowels = "aeiou"
con_count = 0
for i in range(len(sen)):
    if sen[i].isalpha() and sen[i] not in vowels:
        con_count += 1
print(con_count)

# 3
sen = input()
uppercase = ""
for i in range(len(sen)):
    if sen[i].isupper():
        uppercase += sen[i]
print(uppercase)

# 4
for i in range(100, 1000):
    str_num = str(i)
    if str_num[0] == str_num[2]:
        print(i)
# 5
sen = input()
mod_str = ""
for i in range(len(sen)):
    if sen[i].isupper():
        mod_str = sen[i].lower()
    elif sen[i].islower():
        mod_str = sen[i].upper()
    else:
        mod_str = sen[i]
print(mod_str)
