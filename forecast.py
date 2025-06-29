import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Activation
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error

# --- Load & Prepare Data ---
df = pd.read_csv("10years.csv")
df.columns = df.columns.str.lower()
df['datetime'] = pd.to_datetime(df['datetime'])

# Filter only Bitcoin
df = df[df['symbol'] == 'BTC'].copy()
df.sort_values("datetime", inplace=True)
df.reset_index(drop=True, inplace=True)

# Use only the 'close' column
data = df[['datetime', 'close']].copy()

# Scale the close values
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data[['close']])

# --- Create LSTM Sequences ---
def create_sequences(data, window_len=5):
    X, y = [], []
    for i in range(len(data) - window_len):
        X.append(data[i:i+window_len])
        y.append(data[i+window_len])
    return np.array(X), np.array(y)

window_len = 5
X, y = create_sequences(scaled_data, window_len)

# --- Train/Test Split (80/20) ---
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# --- Build LSTM Model ---
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(100, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.add(Activation('linear'))
    model.compile(loss='mse', optimizer='adam')
    return model

model = build_lstm_model((X_train.shape[1], X_train.shape[2]))

# --- Train the Model ---
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

# --- Make Predictions ---
predicted = model.predict(X_test)
predicted_prices = scaler.inverse_transform(predicted)
actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

# --- Plot 1: Train/Test Split ---
plt.figure(figsize=(10, 5))
plt.plot(df['datetime'][:split + window_len], df['close'].iloc[:split + window_len], label='Train')
plt.plot(df['datetime'][split + window_len:], df['close'].iloc[split + window_len:], label='Test')
plt.axvline(df['datetime'].iloc[split + window_len], color='red', linestyle='--', label='Train/Test Split')
plt.title("Train vs Test Split (80/20)")
plt.xlabel("Date")
plt.ylabel("Closing Price (USDT)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Plot 2: Predictions vs Actual ---
plt.figure(figsize=(10, 5))
plt.plot(actual_prices, label='Actual Prices', color='green')
plt.plot(predicted_prices, label='Predicted Prices', color='orange')
plt.title("Bitcoin Price Prediction vs Actual")
plt.xlabel("Time Step (20% Test Data)")
plt.ylabel("Closing Price (USDT)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- MAE ---
mae = mean_absolute_error(actual_prices, predicted_prices)
print(f"Mean Absolute Error: {mae:.2f} USDT")
