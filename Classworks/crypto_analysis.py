from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import requests
import os
from typing import List, Dict, Any

app = FastAPI()

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
CSV_FILENAME = "top20_cryptos.csv"

def fetch_crypto_data() -> List[Dict[str, Any]]:
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1,
        'sparkline': False
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error fetching data from CoinGecko API: {e}")

def create_and_clean_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(data)
    numeric_cols = ['current_price', 'market_cap', 'price_change_percentage_24h']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=numeric_cols, inplace=True)
    return df

def get_top_by_price(df: pd.DataFrame, count: int = 10) -> pd.DataFrame:
    return df.sort_values(by='current_price', ascending=False).head(count)

def get_biggest_movers(df: pd.DataFrame) -> (pd.Series, pd.Series):
    gainer = df.loc[df['price_change_percentage_24h'].idxmax()]
    loser = df.loc[df['price_change_percentage_24h'].idxmin()]
    return gainer, loser

def get_coins_below_price(df: pd.DataFrame, price_limit: float = 1.0) -> pd.DataFrame:
    return df[df['current_price'] < price_limit]

def save_top_market_cap_to_csv(df: pd.DataFrame, filename: str, count: int = 20) -> str:
    top_coins = df.head(count)
    try:
        top_coins.to_csv(filename, index=False)
        return f"Successfully generated '{filename}'"
    except IOError as e:
        return f"Error: Could not write to '{filename}': {e}"

@app.get("/")
def read_root():
    return {"message": "Welcome to the Crypto Analysis API. Use the /analyze endpoint to get data."}

@app.get("/analyze")
def analyze_crypto_data():
    raw_data = fetch_crypto_data()
    if not raw_data:
        raise HTTPException(status_code=500, detail="No data received from the API.")

    df = create_and_clean_dataframe(raw_data)

    top_10_by_price = get_top_by_price(df)
    biggest_gainer, biggest_loser = get_biggest_movers(df)
    average_market_cap = df['market_cap'].mean()
    micro_coins = get_coins_below_price(df)
    csv_status = save_top_market_cap_to_csv(df, CSV_FILENAME)

    analysis_result = {
        "summary": {
            "average_market_cap": f"${average_market_cap:,.2f}",
            "biggest_gainer": {
                "name": biggest_gainer['name'],
                "symbol": biggest_gainer['symbol'],
                "price_change_percentage_24h": f"{biggest_gainer['price_change_percentage_24h']:.2f}%"
            },
            "biggest_loser": {
                "name": biggest_loser['name'],
                "symbol": biggest_loser['symbol'],
                "price_change_percentage_24h": f"{biggest_loser['price_change_percentage_24h']:.2f}%"
            }
        },
        "csv_file_generation": csv_status,
        "top_10_by_current_price": top_10_by_price[['name', 'symbol', 'current_price']].to_dict('records'),
        "coins_below_one_dollar": micro_coins[['name', 'symbol', 'current_price']].to_dict('records')
    }

    return JSONResponse(content=analysis_result)

@app.get("/download-top-20-csv")
def download_csv():
    if not os.path.exists(CSV_FILENAME):
        raise HTTPException(status_code=404, detail=f"File not found. Please run the /analyze endpoint first to generate it.")
    return FileResponse(path=CSV_FILENAME, media_type='text/csv', filename=CSV_FILENAME)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)