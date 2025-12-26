import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# 1. Setup & Download
tickers = ["SPY", "AGG"]
data = yf.download(tickers, start="2010-01-01", auto_adjust=True)
# CRITICAL: Force column order to match our weights
data = data["Close"][["SPY", "AGG"]]

# 2. Define Portfolios
weights_6040 = np.array([0.6, 0.4])

# --- REBALANCING LOGIC ---
# We start with $1.00 and buy units based on our 60/40 split
portfolio_values = []
current_equity = 1.0
units = (current_equity * weights_6040) / data.iloc[0]

for date, prices in data.iterrows():
    # Calculate what our current units are worth today
    current_value = (units * prices).sum()
    portfolio_values.append(current_value)
    
    # REBALANCE: On the first trading day of every year
    if date.is_year_start or (date.month == 1 and date.day <= 7 and 'rebalanced_this_year' not in locals()):
        # This is a simple way to trigger once per January
        units = (current_value * weights_6040) / prices

# Convert the list back to a Series
p6040_equity = pd.Series(portfolio_values, index=data.index)
p6040_returns = p6040_equity.pct_change().dropna()

# 3. SPY Only (For Comparison)
spy_only_returns = data["SPY"].pct_change().dropna()
spy_equity = (1 + spy_only_returns).cumprod()

# 4. Performance Functions
def max_drawdown(equity):
    cumulative_max = equity.cummax()
    drawdown = (equity - cumulative_max) / cumulative_max
    return drawdown.min()

def cagr(equity):
    total_years = len(equity) / 252
    return (equity.iloc[-1] / equity.iloc[0]) ** (1 / total_years) - 1

def print_stats(name, returns, equity):
    ann_ret = returns.mean() * 252
    comp_ret = cagr(equity)
    vol = returns.std() * np.sqrt(252)
    sharpe = ann_ret / vol
    mdd = max_drawdown(equity)
    print(f"--- {name} ---")
    print(f"Arithmetic Return: {ann_ret*100:.2f}%")
    print(f"CAGR: {comp_ret*100:.2f}%")
    print(f"Annual Volatility: {vol*100:.2f}%")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Max Drawdown: {mdd*100:.2f}%\n")

# 5. Output Results
print_stats("100% SPY", spy_only_returns, spy_equity)
print_stats("60/40 Rebalanced", p6040_returns, p6040_equity)

plt.figure(figsize=(10,6))
plt.plot(spy_equity, label="100% SPY")
plt.plot(p6040_equity, label="60/40 Rebalanced")
plt.legend()
plt.title("Growth of $1: SPY vs Rebalanced 60/40")
plt.show()