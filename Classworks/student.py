class Student:

    def __init__(self, student_id, name, grades=None):

        self.student_id = student_id
        self.name = name

        if grades is None:
            self.grades = []
        else:
            self.grades = [int(g) for g in grades]
