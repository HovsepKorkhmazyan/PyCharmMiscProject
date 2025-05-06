# 1
sentence = input("Enter a sentence: ")
categorized = {
    "vowels": [],
    "consonants": [],
    "numbers": [],
    "symbols": []
}
for char in sentence:
    if char.isalpha():
        if char in "aeiouAEIOU":
            categorized["vowels"].append(char)
        else:
            categorized["consonants"].append(char)
    elif char.isdigit():
        categorized["numbers"].append(char)
    else:
        categorized["symbols"].append(char)
print(categorized)

# 2
country_capital = {
    'USA': 'Washington, D.C.',
    'Canada': 'Ottawa',
    'France': 'Paris',
    'Germany': 'Berlin',
    'Italy': 'Rome',
    'Spain': 'Madrid',
    'Japan': 'Tokyo',
    'Australia': 'Canberra',
    'Brazil': 'Brasília',
    'India': 'New Delhi',
    'Russia': 'Moscow',
    'China': 'Beijing',
    'South Africa': 'Pretoria',
    'Mexico': 'Mexico City',
    'Argentina': 'Buenos Aires',
    'United Kingdom': 'London',
    'Egypt': 'Cairo',
    'Saudi Arabia': 'Riyadh',
    'Turkey': 'Ankara',
    'Sweden': 'Stockholm',
}
for country, capital in country_capital.items():
    answer = input(f"What is the capital of {country}? ")
    if answer.strip() == capital:
        print("Correct!")
    else:
        print(f"Wrong! The correct answer is {capital}.")
        break

# 3
phonebook = {}
while True:
    name = input("Enter the name of the person or stop to exit.").strip()
    if name.lower() == "stop":
        break
    if name in phonebook:
        print(f"The phone number for {name} is: {phonebook[name]}")
    else:
        phone_number = input(f"Please enter the phone number: ").strip()
        phonebook[name] = phone_number
        print(f"{name} has been added to the phonebook.")
print(phonebook)
