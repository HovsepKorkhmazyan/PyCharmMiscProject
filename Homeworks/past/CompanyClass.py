import json
from EmployeeClass import Employee
from typing import List, Dict


class Company:
    def __init__(self, file_path: str = 'employees.json'):

        self.file_path = file_path
        self.employees: List[Employee] = self._load_from_json()

    def _load_from_json(self) -> List[Employee]:

        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return [Employee.from_dict(emp_data) for emp_data in data]
        except FileNotFoundError:

            return []
        except json.JSONDecodeError:

            return []

    def _save_to_json(self):

        with open(self.file_path, 'w') as f:
            json.dump([emp.to_dict() for emp in self.employees], f, indent=4)

    def add_employee(self, employee: Employee):

        if not isinstance(employee, Employee):
            raise TypeError("Only Employee objects can be added.")

        if any(emp.employee_id == employee.employee_id for emp in self.employees):
            print(f"Error: Employee with ID {employee.employee_id} already exists.")
            return

        self.employees.append(employee)
        self._save_to_json()
        print(f"Added: {employee.name}")

    def remove_employee(self, employee_id: str) -> bool:

        initial_count = len(self.employees)
        employee_to_remove = next((emp for emp in self.employees if emp.employee_id == employee_id), None)

        if employee_to_remove:
            self.employees.remove(employee_to_remove)
            self._save_to_json()
            print(f"Removed employee: {employee_to_remove.name} (ID: {employee_id})")
            return True
        else:
            print(f"Error: No employee found with ID {employee_id}.")
            return False

    def find_employee(self, identifier: str) -> List[Employee]:

        identifier_lower = identifier.lower()
        results = [
            emp for emp in self.employees
            if identifier_lower in emp.name.lower() or identifier == emp.employee_id
        ]
        return results

    def list_all_employees(self):

        if not self.employees:
            print("No employees in the company.")
            return

        print("\n--- All Employees ---")
        for emp in self.employees:
            print(emp)
        print("---------------------\n")

    def calculate_average_salary_per_department(self) -> Dict[str, float]:

        if not self.employees:
            return {}

        department_salaries: Dict[str, List[float]] = {}
        for emp in self.employees:
            if emp.department not in department_salaries:
                department_salaries[emp.department] = []
            department_salaries[emp.department].append(emp.salary)

        average_salaries: Dict[str, float] = {}
        for department, salaries in department_salaries.items():
            average_salaries[department] = sum(salaries) / len(salaries)

        return average_salaries
