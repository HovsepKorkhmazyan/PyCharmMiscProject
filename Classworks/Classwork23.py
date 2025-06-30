import os

def read_cities(file_path):
    with open(file_path, 'r') as file:
        cities = file.read().splitlines()
    return cities


def parse_weather_value(value_str):
    return value_str.split(':')[-1].strip().rstrip('C%')


def read_temperature_data(city, directory):
    file_path = os.path.join(directory, f"{city}.txt")

    with open(file_path, 'r') as file:
        parts = file.read().strip().split(',')
        if len(parts) < 3:
            return None, None, None
        temperature = parse_weather_value(parts[0])
        humidity = parse_weather_value(parts[1])
        cloudiness = parse_weather_value(parts[2])
        return temperature, humidity, cloudiness


def print_weather_info(cities_file, countries_directory):
    cities = read_cities(cities_file)
    for city in cities:
        temperature, humidity, cloudiness = read_temperature_data(city, countries_directory)
        if temperature is not None and humidity is not None and cloudiness is not None:
            print(f"{city}\nTemperature: {temperature}C \nHumidity: {humidity}% \nCloudiness: {cloudiness}%\n")
        else:
            print(f"{city}\nTemperature data not found or malformed.\n")


cities_file_path = 'cities'
countries_directory_path = 'countries'
print_weather_info(cities_file_path, countries_directory_path)

