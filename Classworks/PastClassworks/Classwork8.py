data = ["John,Smith,093010101",
        "James,Smith,094010101",
        "Ann,Smith,091010101"]
providers = {
    "Viva": ["093", "094", "077"],
    "Armentel": ["091", "099"],
    "Ucom": ["055", "095"]
}

result = []  # To store all the person dictionaries

for el in data:
    name, surname, phone_num = el.strip().split(",")
    temp_d = {}
    temp_d["name"] = name
    temp_d["surname"] = surname
    temp_d["phone_number"] = phone_num
    code = phone_num[:3]

    # Find the provider based on the phone number prefix
    for provider, codes in providers.items():
        if code in codes:
            temp_d["provider"] = provider
            break

    result.append(temp_d)  # Append the dictionary to the result list

print(result)

#2
ml = [1, 2, 3, [1, 2, 3], 4, [4, 5, 6], 5, 6]
total_sum = 0  # Changed variable name to avoid shadowing built-in sum function

for el in ml:
    if isinstance(el, list):  # Using isinstance for type checking
        total_sum += sum(el)  # Sum the elements of the sublist
    else:
        total_sum += el  # Add the integer directly

print(total_sum)