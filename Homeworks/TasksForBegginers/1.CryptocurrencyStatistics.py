import argparse
import time
try:
        import requests
except ImportError as e:
    print(f"Import error: {e}")
    exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Cryptocurrency Statistics")
    parser.add_argument("--name", type=str, help="Filter by cryptocurrency name")
    parser.add_argument("--value", type=float, help="Filter by current price greater than this value")
    return parser.parse_args()

def fetch_cryptocurrency_data():
    API_KEY = "CG-VqqDFffzX5K8pr8dedoBJFca"
    BASE_URL = "https://api.coingecko.com/api/v3"
    HEADERS = {
        "accept": "application/json",
        "x-cg-pro-api-key": API_KEY
    }

    try:
        url = f"{BASE_URL}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1,
            "sparkline": "false"
        }
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def display_statistics(cryptos, name_filter=None, value_filter=None):
    for crypto in cryptos:
        if name_filter and name_filter.lower() not in crypto['name'].lower():
            continue
        if value_filter and crypto['current_price'] <= value_filter:
            continue

        print(f"Name: {crypto['name']}")
        print(f"Symbol: {crypto['symbol']}")
        print(f"Current Price: ${crypto['current_price']:.2f}")
        print(f"Market Cap: ${crypto['market_cap']:.2f}")
        print(f"Total Volume: ${crypto['total_volume']:.2f}")
        print(f"Price Change (24h): {crypto['price_change_percentage_24h']:.2f}%")
        print("-" * 40)

def main():
    args = parse_arguments()
    name_filter = args.name
    value_filter = args.value

    while True:
        print("\nFetching cryptocurrency data...")
        cryptos = fetch_cryptocurrency_data()
        display_statistics(cryptos, name_filter, value_filter)
        time.sleep(5)

if __name__ == "__main__":
    main()
