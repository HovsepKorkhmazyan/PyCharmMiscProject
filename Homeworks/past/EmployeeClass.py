import uuid


class Employee:

    def __init__(self, name: str, department: str, salary: float, employee_id: str = None):

        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        if not department or not isinstance(department, str):
            raise ValueError("Department must be a non-empty string.")
        if not isinstance(salary, (int, float)) or salary < 0:
            raise ValueError("Salary must be a non-negative number.")

        self.employee_id = employee_id if employee_id is not None else str(uuid.uuid4())
        self.name = name
        self.department = department
        self.salary = salary

    def to_dict(self):

        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'department': self.department,
            'salary': self.salary
        }

    @classmethod
    def from_dict(cls, data: dict):

        return cls(
            employee_id=data['employee_id'],
            name=data['name'],
            department=data['department'],
            salary=data['salary']
        )

    def __repr__(self):

        return (f"Employee(ID: {self.employee_id}, Name: {self.name}, "
                f"Department: {self.department}, Salary: ${self.salary:,.2f})")
