# 1 Encapsulation Implementation:

class Number:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if type(value) != int or float or value < 0:
            __value = 0
        else:
            self.__value = value

    def __add__(self, other):
        return Number(self.__value + other.value)

    def __sub__(self, other):
        return Number(self.__value - other.value)

    def __mul__(self, other):
        return Number(self.__value * other.value)

    def __truediv__(self, other):
        return Number(self.__value / other.value)

    def __str__(self):
        return str(self.__value)


n1 = Number(10)
n2 = Number(5)

print(n1.value)

print("Addition:", n1 + n2)
print("Subtraction:", n1 - n2)
print("Multiplication:", n1 * n2)
print("Division:", n1 / n2)


class Human:
    def __init__(self, name, surname, age):
        self.__name = name
        self.__surname = surname
        self.__age = age

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str):
            self.__name = ""
        else:
            self.__name = new_name

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, new_surname):
        if not isinstance(new_surname, str):
            self.__surname = ""
        else:
            self.__surname = new_surname

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, new_age):
        if not isinstance(new_age, int) or new_age < 0:
            self.__age = 0
        else:
            self.__age = new_age

    def speak(self):
        print(f"Hello, my name is {self.__name} {self.__surname}.")

    def get_older(self):
        self.__age += 1


person = Human("John", "Doe", 30)
print(person.name)
print(person.surname)
print(person.age)

person.name = "Jane"
person.surname = "Smith"
person.speak() 



