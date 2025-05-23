from operator import itemgetter

# 1
students = []

for _ in range(5):
    name = input("Enter student's name: ")
    age = int(input("Enter student's age: "))
    mark = float(input("Enter student's mark: "))
    students.append((name, age, mark))

students.sort(key=itemgetter(0))

print("\nSorted students based on names alphabetically:")
for student in students:
    print(student)

# 2
emails = []
while True:
    email = input("Enter email: ")
    if email.lower() == "stop":
        break
    emails.append(email)

names_surnames = []
for email in emails:
    if "@" in email:
        name_part = email.split('@')[0]
        name, surname = name_part.split('_')
        names_surnames.append(f"{name.capitalize()} {surname.capitalize()}")

print("\nList of names and surnames:")
print(names_surnames)
