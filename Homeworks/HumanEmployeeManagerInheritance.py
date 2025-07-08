from abc import ABC, abstractmethod

class Human(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, Age: {self.age}"

    @abstractmethod
    def role(self):
        pass


class Employee(Human):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)
        self.employee_id = employee_id

    def __str__(self):
        return f"{super().__str__()}, Employee ID: {self.employee_id}"

    def role(self):
        return "Employee"


class Manager(Employee):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age, employee_id)
        self.employees = []

    def hire(self, employee):
        if len(self.employees) < 10:
            self.employees.append(employee)
            print(f"{employee.name} has been hired.")
        else:
            print("Cannot hire more than 10 employees.")

    def fire(self, employee):
        if employee in self.employees:
            self.employees.remove(employee)
            print(f"{employee.name} has been fired.")
        else:
            print(f"{employee.name} is not an employee.")

    def list_employees(self):
        if self.employees:
            print("Employees under management:")
            for emp in self.employees:
                print(emp)
        else:
            print("No employees under management.")

    def role(self):
        return "Manager"


if __name__ == "__main__":
    manager = Manager("Alice", 35, "M001")
    employee1 = Employee("Bob", 28, "E001")
    employee2 = Employee("Charlie", 30, "E002")

    manager.hire(employee1)
    manager.hire(employee2)
    manager.list_employees()

    manager.fire(employee1)
    manager.list_employees()
