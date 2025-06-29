import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import mplfinance as mpf


"""df_oneday= pd.read_csv("data.csv")
df_oneday["Datetime"] = pd.to_datetime(df_oneday["Datetime"])
df_oneday.columns = df_oneday.columns.str.lower()
df_oneday.columns = df_oneday.columns.str.replace(" ", "_")"""



df_10year= pd.read_csv("10years.csv")
df_10year["Datetime"] = pd.to_datetime(df_10year["Datetime"])
df_10year.columns = df_10year.columns.str.lower()
df_10year.columns = df_10year.columns.str.replace(" ", "_")




#10 years plot    
plt.figure(figsize=(8, 6))
ax = df_10year.groupby(["symbol"])["market_cap"].last() \
    .sort_values( ascending=False)\
    .head(5) \
    .sort_values() \
    .plot(kind="barh")
ax.set_xlabel("Market Cap (in USD)")
ax.ticklabel_format(style="sci",axis="x")
plt.title("Top 5 cryptocurrencies by market cap in last 10 years",fontsize=12)
plt.show()



#plotting top 4 currencies closing trend in last 10 years
top_4=["BTC",'ETH', 'XRP', 'SOL']
data = df_10year[df_10year["symbol"].isin(top_4)]

# 📈 Plotting
plt.figure(figsize=(9, 6))

for coin in top_4:
    coin_data = data[data["symbol"] == coin]
    plt.plot(coin_data["datetime"], coin_data["close"], label=coin)

plt.title("Top 4 Cryptocurrencies: Log(Closing Price) Trend")
plt.ylabel("Closing Price (USDT)")
plt.yscale("log")
plt.show()

#plotting top 4 currencies closing trend in last 10 years except bitcoin
top_4=["DOGE",'ETH', 'XRP', 'SOL']
data = df_10year[df_10year["symbol"].isin(top_4)]

# 📈 Plotting
plt.figure(figsize=(9, 6))

for coin in top_4:
    coin_data = data[data["symbol"] == coin]
    plt.plot(coin_data["datetime"], coin_data["close"], label=coin)

plt.title("Top 4 Cryptocurrencies:log(Closing Price)  Trend (after BTC)")
plt.ylabel("log(Closing Price (USDT))")
plt.yscale("log")
plt.show()



#rolling average on a window of 7 fro bitcoin
btc = df_10year[df_10year["symbol"] == "BTC"].copy()
btc.sort_values("datetime", inplace=True)
btc["close"] = pd.to_numeric(btc["close"], errors='coerce')
btc["ma7"] = btc["close"].rolling(window=7).mean()

plt.figure(figsize=(10, 5))
plt.plot(btc["datetime"], btc["close"], label="BTC Close", alpha=0.4)
plt.plot(btc["datetime"], btc["ma7"], label="7-Day MA", color="orange")
plt.title("Bitcoin Closing Price with 7-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Price (USDT)")
plt.legend()
plt.grid(True)
plt.show()




#candlestick for 6 month of bitcoin
# 📊 Filter only Bitcoin data
btc = df_10year[df_10year["symbol"] == "BTC"].copy()

# 📅 Convert to datetime and set as index
btc["datetime"] = pd.to_datetime(btc["datetime"])
btc.set_index("datetime", inplace=True)

# 🔢 Make sure prices are numbers
btc["open"] = pd.to_numeric(btc["open"], errors='coerce')
btc["high"] = pd.to_numeric(btc["high"], errors='coerce')
btc["low"] = pd.to_numeric(btc["low"], errors='coerce')
btc["close"] = pd.to_numeric(btc["close"], errors='coerce')

# 🗓️ Choose a smaller date range to keep the chart clean
btc = btc["2023-01-01":"2023-06-30"]

# 📈 Plot the candlestick chart
mpf.plot(
    btc[["open", "high", "low", "close"]],
    type="candle",         # show candlesticks
    style="yahoo",         # nice-looking theme
    title="Bitcoin Candlestick Chart (Jan–Jun 2023)",
    ylabel="Price in USDT",
    volume=False           # set to True if you want volume bars
)


#Volatility Analysis Over Time

plt.figure(figsize=(10, 5))
for coin in ['BTC', 'ETH', 'XRP', 'SOL']:
    coin_data = df_10year[df_10year['symbol'] == coin].copy()
    coin_data.sort_values("datetime", inplace=True)
    coin_data["close"] = pd.to_numeric(coin_data["close"], errors="coerce")
    coin_data["volatility"] = coin_data["close"].rolling(window=30).std()
    plt.plot(coin_data["datetime"], coin_data["volatility"], label=coin)

plt.title("30-Day Rolling Volatility of Top Cryptocurrencies (2014–2024)")
plt.xlabel("Date")
plt.ylabel("Volatility (Standard Deviation of Closing Price)")
plt.legend()
plt.show()





#Annual Return Comparison

df_10year["year"] = df_10year["datetime"].dt.year
df_10year["close"] = pd.to_numeric(df_10year["close"], errors="coerce")

# Group by year and coin, get first and last close price
yearly = df_10year.groupby(["symbol", "year"])["close"].agg(["first", "last"]).reset_index()
yearly["return_%"] = (yearly["last"] - yearly["first"]) / yearly["first"] * 100

# Pivot for better plotting
pivot_return = yearly.pivot(index="year", columns="symbol", values="return_%")

# Plot
pivot_return.plot(kind="bar", figsize=(12, 6))
plt.title("Yearly Percentage Return of Cryptocurrencies")
plt.ylabel("Annual Return (%)")
plt.xlabel("Year")
plt.grid(True)
plt.legend(title="Coin")
plt.tight_layout()
plt.show()
