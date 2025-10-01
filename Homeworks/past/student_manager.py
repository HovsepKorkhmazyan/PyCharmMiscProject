import os
from student import Student

def save_students(students, filename="students.txt"):
    try:
        with open(filename, 'w') as file:
            for student in students:
                grades_str = ",".join(map(str, student.grades))
                file.write(f"{student.student_id},{student.name},{grades_str}\n")
        print("Student data saved successfully.")
    except IOError as e:
        print(f"Error saving file: {e}")

def load_students(filename="students.txt"):
    students = []
    if not os.path.exists(filename):
        return students

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                student_id = parts[0]
                name = parts[1]
                grades = parts[2:] if len(parts) > 2 else []
                students.append(Student(student_id, name, grades))
        print("Student data loaded successfully.")
    except IOError as e:
        print(f"Error loading file: {e}")
    return students

def find_student_by_id(students, student_id):
    for student in students:
        if student.student_id == student_id:
            return student
    return None

def main():
    filename = "students.txt"
    students = load_students(filename)

    while True:
        print("\n--- Student Grade Manager ---")
        print("1. Add New Student")
        print("2. Display All Students")
        print("3. Search for Student by ID")
        print("4. Update Student Grades")
        print("5. Save and Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            student_id = input("Enter student ID: ")
            if find_student_by_id(students, student_id):
                print("Error: A student with this ID already exists.")
                continue
            name = input("Enter student name: ")
            students.append(Student(student_id, name))
            print(f"Student '{name}' added successfully.")

        elif choice == '2':
            if not students:
                print("No students to display.")
            else:
                print("\n--- All Students ---")
                for student in students:
                    print(student)

        elif choice == '3':
            student_id = input("Enter student ID to search for: ")
            student = find_student_by_id(students, student_id)
            if student:
                print("\n--- Student Details ---")
                print(student)
                print(f"Grades: {student.grades}")
            else:
                print("Student not found.")

        elif choice == '4':
            student_id = input("Enter student ID to update grades: ")
            student = find_student_by_id(students, student_id)
            if student:
                print(f"Current grades for {student.name}: {student.grades}")
                new_grade_str = input("Enter a new grade to add: ")
                try:
                    new_grade = int(new_grade_str)
                    student.add_grade(new_grade)
                    print(f"Grade {new_grade} added successfully.")
                except ValueError:
                    print("Invalid input. Please enter an integer.")
            else:
                print("Student not found.")

        elif choice == '5':
            save_students(students, filename)
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()