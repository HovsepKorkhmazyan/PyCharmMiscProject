#1
data = {
    "a":10,
    "b":20,
    "c":15,
    "d":30,
    "e":25,
}

def top_three_values(input_dict):
    top_three = sorted(input_dict.items(), key=lambda item: item[1], reverse=True)[:3]
    result_dict = dict(top_three)
    return result_dict

highest_three = top_three_values(data)
print("The highest three values are:", highest_three.values())

#2
data = [
    "Armenia, Yerevan, 3, 4090",
    "France, Paris, 4, 4810",
    "Nepal, Kathmandu, 8, 8848",
    "USA, Washington, 6, 6190"
]
def parse_data(data):
    parsed_list = []
    for item in data:
        country, capital, population, highest_peak = item.split(", ")
        parsed_list.append({
            "country": country,
            "capital": capital,
            "population": int(population),
            "highest_peak": int(highest_peak)
        })
    return parsed_list

def get_by_country(data, country_name):
    parsed = parse_data(data)
    for country in parsed:
        if country["country"] == country_name:
            return country
    return None

def get_by_capital(data, capital_name):
    parsed = parse_data(data)
    return [entry for entry in parsed if entry["capital"] == capital_name]

def get_population(data, popul):
    parsed = parse_data(data)
    return [country for country in parsed if country["population"] > popul]

def get_highest_peak(data, peak_threshold=0):
    parsed = parse_data(data)
    return [entry for entry in parsed if entry["highest_peak"] > peak_threshold]

def print_objects(ml):
    for obj in ml:
        print("Country: ", obj['country'])
        print("Capital: ", obj['capital'])
        print("Population (millions): ", obj['population'])
        print("Highest Peak (meters): ", obj['highest_peak'])

print("Get by Country:")
print(get_by_country(data,"Armenia"))
print("\nGet by Capital:")
print(get_by_capital(data,"Yerevan"))
print("\nGet Population:")
print(get_population(data,3))
print("\nGet Highest Peak:")
print(get_highest_peak(data,4090))

#3
def top_three_letters(counts):
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts[:3]

def count_letters(input_string):
    counts = {}
    for char in input_string.lower():
        if char.isalpha():
            counts[char] = counts.get(char, 0) + 1
    return counts

input_string = input()
counts = count_letters(input_string)
top_three = top_three_letters(counts)
print("The three most used letters are:")
for letter, count in top_three:
    print(f"Letter: {letter} -> Count: {count}")

#4
def is_unique(number):
    digits = str(number)
    return len(set(digits)) == len(digits)

def count_unique_three_digit_numbers():
    unique_count = 0
    for number in range(100, 1000):
        if is_unique(number):
            unique_count += 1
    return unique_count

unique_count = count_unique_three_digit_numbers()
print(f"There are {unique_count} unique three-digit numbers.")