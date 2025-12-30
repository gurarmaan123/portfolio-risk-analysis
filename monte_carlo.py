import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# -----------------------------
# 1. PARAMETERS
# -----------------------------
tickers = ["SPY", "AGG"]
weights = np.array([0.6, 0.4])
start_date = "2010-01-01"
n_simulations = 5000     # Number of "alternate universes"
n_years = 10             # How far into the future
n_days = 252 * n_years   # Total trading days
initial_investment = 10000 

print(f"DOWNLOADING DATA FOR {tickers}...")

# -----------------------------
# 2. DOWNLOAD & PREP DATA
# -----------------------------
# Ensure columns are in the correct order to match weights
data = yf.download(tickers, start=start_date, auto_adjust=True)["Close"]
data = data[["SPY", "AGG"]] 
returns = data.pct_change().dropna()

# Calculate the historical 60/40 daily returns
portfolio_returns = returns @ weights

print("SIMULATING 10 YEARS OF RETURNS...")

# -----------------------------
# 3. MONTE CARLO (BOOTSTRAP METHOD)
# -----------------------------
# Instead of a random bell curve, we pull from actual historical days
simulated_paths = np.zeros((n_days, n_simulations))

for i in range(n_simulations):
    # Randomly pick 'n_days' worth of returns from history with replacement
    random_samples = np.random.choice(portfolio_returns, size=n_days, replace=True)
    # Compound them over time and apply to our initial investment
    simulated_paths[:, i] = initial_investment * (1 + random_samples).cumprod()

print("SIMULATION COMPLETE.")

# -----------------------------
# 4. PLOTTING THE EQUITY CURVES
# -----------------------------
plt.figure(figsize=(12, 6))

# Plot the first 100 paths as gray background lines
plt.plot(simulated_paths[:, :100], color="gray", alpha=0.1)

# Plot the median (middle) path - often more realistic than the mean
median_path = np.median(simulated_paths, axis=1)
plt.plot(median_path, color="blue", linewidth=3, label="Median Path (50th Percentile)")

# Plot the "Bad Case" (5th percentile)
bad_case = np.percentile(simulated_paths, 5, axis=1)
plt.plot(bad_case, color="red", linestyle="--", label="Worst 5% Outcome")

plt.title(f"Monte Carlo: 10-Year Growth of ${initial_investment:,.0f} (60/40 Portfolio)")
plt.xlabel("Trading Days")
plt.ylabel("Portfolio Value ($)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# -----------------------------
# 5. RISK & TERMINAL STATS
# -----------------------------
final_values = simulated_paths[-1]
prob_loss = np.mean(final_values < initial_investment)
median_final = np.median(final_values)
top_5pct = np.percentile(final_values, 95)
worst_5pct = np.percentile(final_values, 5)

print("-" * 30)
print(f"RESULTS AFTER {n_years} YEARS")
print("-" * 30)
print(f"Median Final Value:    ${median_final:,.2f}")
print(f"Worst 5% Case:         ${worst_5pct:,.2f}")
print(f"Best 5% Case:          ${top_5pct:,.2f}")
print(f"Probability of Loss:   {prob_loss * 100:.2f}%")
print("-" * 30)

# 6. TERMINAL VALUE HISTOGRAM
plt.figure(figsize=(10, 5))
plt.hist(final_values, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(initial_investment, color='red', linestyle='--', label='Initial Investment')
plt.title("Distribution of Final Portfolio Values")
plt.xlabel("Final Dollar Amount")
plt.ylabel("Frequency")
plt.legend()
plt.show()