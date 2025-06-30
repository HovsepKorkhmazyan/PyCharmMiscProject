import requests
import argparse
import json

API_KEY = "d3aa68d0c76b4527874110709252906"
BASE_URL = "http://api.weatherapi.com/v1/current.json"


def get_weather_data(city_name):
    try:
        response = requests.get(
            BASE_URL,
            params={
                "key": API_KEY,
                "q": city_name,
                "aqi": "no"
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def display_all_data(weather_data):
    print("\nFull Weather Report:")
    print("-------------------")
    print(f"Location: {weather_data['location']['name']}, {weather_data['location']['country']}")
    print(f"Local Time: {weather_data['location']['localtime']}")
    print(f"Weather Condition: {weather_data['current']['condition']['text']}")
    print(f"Temperature (°C): {weather_data['current']['temp_c']}")
    print(f"Temperature (°F): {weather_data['current']['temp_f']}")
    print(f"Feels Like (°C): {weather_data['current']['feelslike_c']}")
    print(f"Feels Like (°F): {weather_data['current']['feelslike_f']}")
    print(f"Humidity: {weather_data['current']['humidity']}%")
    print(f"Wind Speed (kph): {weather_data['current']['wind_kph']}")
    print(f"Wind Direction: {weather_data['current']['wind_dir']}")
    print(f"Pressure (mb): {weather_data['current']['pressure_mb']}")
    print(f"Precipitation (mm): {weather_data['current']['precip_mm']}")
    print(f"Cloud Cover: {weather_data['current']['cloud']}%")
    print(f"UV Index: {weather_data['current']['uv']}")
    print(f"Visibility (km): {weather_data['current']['vis_km']}")


def display_specific_data(weather_data, option):
    option = option.lower()
    current = weather_data['current']

    if option == 'temperature':
        print(f"\nTemperature Info:")
        print(f"Current (°C): {current['temp_c']}")
        print(f"Current (°F): {current['temp_f']}")
        print(f"Feels Like (°C): {current['feelslike_c']}")
        print(f"Feels Like (°F): {current['feelslike_f']}")
    elif option == 'humidity':
        print(f"\nHumidity: {current['humidity']}%")
    elif option == 'wind':
        print(f"\nWind Info:")
        print(f"Speed (kph): {current['wind_kph']}")
        print(f"Direction: {current['wind_dir']}")
        print(f"Gust (kph): {current.get('gust_kph', 'N/A')}")
    elif option == 'pressure':
        print(f"\nPressure: {current['pressure_mb']} mb")
    elif option == 'precipitation':
        print(f"\nPrecipitation: {current['precip_mm']} mm")
    elif option == 'visibility':
        print(f"\nVisibility: {current['vis_km']} km")
    elif option == 'uv':
        print(f"\nUV Index: {current['uv']}")
    elif option == 'cloud':
        print(f"\nCloud Cover: {current['cloud']}%")
    else:
        print(f"\nInvalid option: {option}")
        display_options()


def display_options():
    print("\nAvailable weather options:")
    print("- temperature")
    print("- humidity")
    print("- wind")
    print("- pressure")
    print("- precipitation")
    print("- visibility")
    print("- uv")
    print("- cloud")
    print("\nUse 'options' to see this list again")


def main():
    parser = argparse.ArgumentParser(description="Get weather forecast for a city")
    parser.add_argument("city", help="City name to get weather for")
    parser.add_argument("--option", help="Specific weather metric to display")
    args = parser.parse_args()

    weather_data = get_weather_data(args.city)

    if not weather_data:
        return

    if args.option:
        if args.option.lower() == "options":
            display_options()
        else:
            display_specific_data(weather_data, args.option)
    else:
        display_all_data(weather_data)


if __name__ == "__main__":
    main()
