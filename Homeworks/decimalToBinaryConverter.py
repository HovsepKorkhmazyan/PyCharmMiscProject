num = int(input("Enter a number: "))
bin_Res = ""

if num == 0:
    bin_Res = "0"
else:
    while num > 0:
        bin_Res = str(num % 2) + bin_Res
        num //= 2

print("Binary representation:", bin_Res)
