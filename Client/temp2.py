import pandas as pd
import requests
from lightweight_charts import Chart
from datetime import datetime, timedelta

def fetch_stock_data(ticker, api_key):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?apiKey={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json().get('results', [])
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['t'], unit='ms')
        df = df.rename(columns={
            'o': 'open', 
            'h': 'high', 
            'l': 'low', 
            'c': 'close', 
            'v': 'volume'
        })
        
        return df[['date', 'open', 'high', 'low', 'close', 'volume']]
    else:
        raise Exception("Failed to fetch stock data")

def calculate_sma(df, period: int = 50):
    return pd.DataFrame({
        'time': df['date'],
        f'SMA {period}': df['close'].rolling(window=period).mean()
    }).dropna()

def main(ticker, api_key):
    # Fetch stock data
    df = fetch_stock_data(ticker, api_key)
    
    # Create chart
    chart = Chart()
    chart.legend(visible=True)
    chart.set(df)

    # Create SMA line
    line = chart.create_line('SMA 50')
    sma_data = calculate_sma(df, period=50)
    line.set(sma_data)

    chart.show(block=True)

if __name__ == '__main__':
    # Replace with your Polygon.io API key and desired ticker
    API_KEY = ''
    TICKER = 'AAPL'
    
    main(TICKER, API_KEY)