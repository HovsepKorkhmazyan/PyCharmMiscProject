num1 = int(input("Enter the coefficient a: "))  # This is 'a'
num2 = int(input("Enter the coefficient b: "))  # This is 'b'
num3 = int(input("Enter the coefficient c: "))  # This is 'c'

discriminant = num2 ** 2 - 4 * num1 * num3

print(f"The discriminant (D) is: {discriminant}")

if discriminant > 0:
    print("The equation has two distinct real roots.")
elif discriminant == 0:
    print("The equation has exactly one real root (a repeated root).")
else:
    print("The equation has two complex roots.")
