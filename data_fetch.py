import requests
import pandas as pd
from datetime import datetime, timedelta
import time

symbols = [
    'BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'XRPUSDT', 'DOGEUSDT',
    'SOLUSDT', 'LTCUSDT', 'TRXUSDT', 'AVAXUSDT', 'MATICUSDT'
]

date = "2024-06-01"
start_dt = datetime.strptime(date, "%Y-%m-%d")
end_dt = start_dt + timedelta(days=1)

all_data = []

for symbol in symbols:
    print(f"📥 Fetching data for {symbol}...")

    url = "https://api.binance.com/api/v3/klines"
    
    start_time_ms = int(start_dt.timestamp() * 1000)
    end_time_ms = int(end_dt.timestamp() * 1000)

    params = {
        "symbol": symbol,
        "interval": "1m",
        "startTime": start_time_ms,
        "endTime": end_time_ms,
        "limit": 1000
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        all_ohlc = data

        if len(data) == 1000:
            last_time = data[-1][0]
            params["startTime"] = last_time + 1
            time.sleep(0.2)
            response2 = requests.get(url, params=params)
            all_ohlc += response2.json()

        df = pd.DataFrame(all_ohlc, columns=[
            "Open Time", "Open", "High", "Low", "Close",
            "Volume", "Close Time", "Quote Asset Volume",
            "Number of Trades", "Taker Buy Base Volume", 
            "Taker Buy Quote Volume", "Ignore"
        ])

        df["Datetime"] = pd.to_datetime(df["Open Time"], unit="ms")
        df["Symbol"] = symbol.replace("USDT", "")
        
        # Select and rename necessary columns
        df = df[["Datetime", "Symbol", "Open", "High", "Low", "Close", "Volume", "Quote Asset Volume"]]
        df.rename(columns={
            "Quote Asset Volume": "Market Cap"
        }, inplace=True)

        all_data.append(df)

    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")

final_df = pd.concat(all_data).reset_index(drop=True)
final_df.to_csv("minute_ohlc_with_volume_marketcap.csv", index=False)

print("✅ Data saved to 'minute_ohlc_with_volume_marketcap.csv'")
print(final_df.head())
