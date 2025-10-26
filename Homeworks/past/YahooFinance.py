from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import yfinance as yf
import uvicorn
import matplotlib.pyplot as plt
import io
import base64
from typing import List

app = FastAPI(
    title="Stock Analysis API (yfinance)",
    description="An API to fetch stock information, including dividends and performance analysis, using only the yfinance library.",
    version="2.0.0"
)


@app.get("/dividends/{ticker}", summary="Get Dividends by Ticker")
def fetch_dividends(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        dividends = stock.dividends

        if dividends.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No dividend information found for ticker '{ticker.upper()}'."
            )

        dividends_df = dividends.reset_index()

        dividends_df.rename(columns={'index': 'Date'}, inplace=True)
        dividends_df.columns = ['Date', 'dividend']

        dividends_df['date_str'] = dividends_df['Date'].dt.strftime('%Y-%m-%d')

        results = dividends_df[['date_str', 'dividend']].to_dict('records')

        return {"ticker": ticker.upper(), "dividends": results}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred with yfinance: {str(e)}"
        )


@app.get("/stock-analysis/", summary="Get 1-Month Stock Analysis")
async def stock_analysis(
        tickers: List[str] = Query(..., description="A list of 3 stock ticker symbols.", min_length=3, max_length=3)):
    upper_tickers = [t.upper() for t in tickers]

    try:

        data = yf.download(upper_tickers, period="1mo")
        if data.empty:
            raise HTTPException(status_code=404, detail="Could not fetch data. Please check if tickers are valid.")

        close_prices = data['Close']

        summary = {}
        valid_tickers_for_plot = []
        for ticker in upper_tickers:
            if ticker in close_prices and not close_prices[ticker].isnull().all():
                summary[ticker] = {
                    'mean_close_price': round(close_prices[ticker].mean(), 2),
                    'min_close_price': round(close_prices[ticker].min(), 2),
                    'max_close_price': round(close_prices[ticker].max(), 2),
                }
                valid_tickers_for_plot.append(ticker)
            else:
                summary[ticker] = {"error": "No data found for this ticker."}

        if not valid_tickers_for_plot:
            raise HTTPException(status_code=404, detail="No valid data found for any of the provided tickers.")

        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(12, 7))

        for ticker in valid_tickers_for_plot:
            ax.plot(close_prices.index, close_prices[ticker], label=ticker)

        ax.set_title('1-Month Stock Closing Prices', fontsize=16)
        ax.set_ylabel('Closing Price (USD)')
        ax.set_xlabel('Date')
        ax.legend(title="Tickers")
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        plt.close(fig)

        plot_base64 = base64.b64encode(buf.read()).decode('utf-8')

        response_data = {
            "summary_statistics": summary,
            "plot_image_base64": plot_base64
        }

        return JSONResponse(content=response_data)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
