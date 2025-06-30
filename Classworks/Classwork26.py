# 1 Class Implementations:
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return (f"Rectangle(width={self.width}, height={self.height}, "
                f"area={self.area()}, perimeter={self.perimeter()})")

    def __add__(self, other):
        return Rectangle(self.width + other.width, self.height + other.height)


rect = Rectangle(4, 5)
print("Area:", rect.area())
print("Perimeter:", rect.perimeter())
print(rect)

rect2 = Rectangle(10, 15)
print(rect + rect2)


# 2 Class Number:

class Number:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return Number(self.value + other.value)

    def __sub__(self, other):
        return Number(self.value - other.value)

    def __mul__(self, other):
        return Number(self.value * other.value)

    def __truediv__(self, other):
        return Number(self.value / other.value)

    def __str__(self):
        return str(self.value)

n1 = Number(10)
n2 = Number(5)

print("Addition:", n1 + n2)
print("Subtraction:", n1 - n2)
print("Multiplication:", n1 * n2)
print("Division:", n1 / n2)
