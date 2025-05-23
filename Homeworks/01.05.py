# 1
data = ["John,Smith,18,Singer", "Ann,Smith,30,Doctor"]

structured_data = {}

for index, entry in enumerate(data, start=1):
    name, surname, age, profession = entry.split(',')
    structured_data[index] = {
        "name": name,
        "surname": surname,
        "age": int(age),
        "profession": profession
    }

print(structured_data)

# 2
md = {
    1: {
        "name": "John",
        "age": 18,
        "profession": "Singer"
    },
    2: {
        "name": "Ann",
        "surname": "Smith",
        "profession": "Doctor"
    },
    3: {
        "name": "Ann",
        "surname": "Smith",
        "age": 30,
        "profession": "Doctor"
    }
}

required_keys = {"name", "surname", "age", "profession"}

missing_dicts = []

for id, details in md.items():
    missing_keys = required_keys - details.keys()

    if missing_keys:
        missing_dicts.append({
            "id": id,
            "data": list(missing_keys)
        })

print(missing_dicts)
