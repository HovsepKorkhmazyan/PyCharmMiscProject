num1 = int(input("Enter a number: "))
num2 = int(input("Enter a number: "))
num3 = int(input("Enter a number: "))

min_num = ""
mid_num = ""
max_num = ""

if num1 < num2 and num1 < num3:
    min_num = num1
elif num2 < num1 and num2 < num3:
    min_num = num2
else:
    min_num = num3

if num1 > num2 and num1 > num3:
    max_num = num1
elif num2 > num1 and num2 > num3:
    max_num = num2
else:
    max_num = num3

if num1 != min_num and num1 != max_num:
    mid_num = num1
elif num2 != min_num and num2 != max_num:
    mid_num = num2
else:
    mid_num = num3

print(f"{min_num}, {mid_num}, {max_num}")
