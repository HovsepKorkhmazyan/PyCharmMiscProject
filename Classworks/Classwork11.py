#1
ml = ["John,Smith,45,doctor,3000"]
people = []
for el in ml:
    name, surname, age, profession, salary = el.split(',')
    people.append({
        'name': name,
        'surname': surname,
        'age': int(age),
        'profession': profession,
        'salary': int(salary)
    })

def get_oldest_person(people):
    oldest = people[0]
    for person in people:
        if person['age'] > oldest['age']:
            oldest = person
    return oldest
def get_highest_salary(people):
    highest = people[0]
    for person in people:
        if person['salary'] > highest['salary']:
            highest = person
    return highest

def get_people_alphabetically(people):
    return sorted(people, key=lambda x: (x['surname'], x['name']))

def get_people_by_profession(people, profession="doctor"):
    filtered = [person for person in people if person['profession'].lower() == profession.lower()]
    return filtered

oldest_person = get_oldest_person(people)
highest_salary_person = get_highest_salary(people)
people_sorted = get_people_alphabetically(people)
doctors = get_people_by_profession(people, "doctor")
print("Oldest Person:", oldest_person)
print("Highest Salary Person:", highest_salary_person)
print("People Alphabetically:", people_sorted)
print("Doctors:", doctors)

#2
user_input = input()
def change_str(input_str):
    tmp = input_str.split(',')
    temp = []
    for el in tmp:
        if len(el) % 2 == 0:
            temp.append(el.lower())
        else:
            temp.append(el.upper())
    return " ".join(temp)
result = change_str(user_input)
print(result)

#3 Version 1
def count_words(input_str):
    words = input_str.split()
    count = 0
    for word in words:
        count += 1
    return count
result = count_words(user_input)
print(result)
# Version 2
def count_words_2(input_str):
    return len([el for el in input_str.split() if el.isalpha()])





