class Student:
    def __init__(self, student_id, name, grades=None):
        self.student_id = student_id
        self.name = name
        if grades is None:
            self.grades = []
        else:
            self.grades = [int(g) for g in grades]

    def add_grade(self, grade):
        if isinstance(grade, int):
            self.grades.append(grade)
        else:
            print("Error: Grade must be an integer.")

    def calculate_average(self):
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def __str__(self):
        return (f"ID: {self.student_id}, Name: {self.name}, "
                f"Average Grade: {self.calculate_average():.2f}")