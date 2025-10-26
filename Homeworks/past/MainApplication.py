from CompanyClass import Company
from EmployeeClass import Employee

def print_menu():

    print("\n===== Employee Management System =====")
    print("1. Add a new employee")
    print("2. Remove an employee")
    print("3. Find an employee")
    print("4. List all employees")
    print("5. Calculate average salary per department")
    print("6. Exit")
    print("======================================")

def main():

    my_company = Company()

    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            try:
                name = input("Enter employee name: ")
                department = input("Enter department: ")
                salary_str = input("Enter salary: ")
                salary = float(salary_str)
                new_employee = Employee(name=name, department=department, salary=salary)
                my_company.add_employee(new_employee)
            except ValueError as e:
                print(f"Error: Invalid input. {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif choice == '2':
            employee_id = input("Enter the ID of the employee to remove: ")
            my_company.remove_employee(employee_id)

        elif choice == '3':
            identifier = input("Enter employee name or ID to find: ")
            results = my_company.find_employee(identifier)
            if results:
                print("\n--- Search Results ---")
                for emp in results:
                    print(emp)
                print("----------------------")
            else:
                print("No employees found matching your search.")

        elif choice == '4':
            my_company.list_all_employees()

        elif choice == '5':
            avg_salaries = my_company.calculate_average_salary_per_department()
            if avg_salaries:
                print("\n--- Average Salary Per Department ---")
                for department, avg_salary in avg_salaries.items():
                    print(f"{department}: ${avg_salary:,.2f}")
                print("-------------------------------------")
            else:
                print("Cannot calculate average salaries. No employees found.")

        elif choice == '6':
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
