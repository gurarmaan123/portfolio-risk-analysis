# portfolio-risk-analysis
Risk and performance analysis of SPY vs a 60/40 portfolio using Python
# Portfolio Risk & Performance Analysis

This project analyzes the historical performance and risk characteristics of two portfolios:
- 100% SPY (US Equity Portfolio)
- 60/40 Portfolio (60% SPY, 40% Bonds)

## Metrics Computed
- Arithmetic Annual Return
- Compound Annual Growth Rate (CAGR)
- Annualized Volatility
- Sharpe Ratio
- Maximum Drawdown

## Methodology
- Historical daily price data is downloaded using `yfinance`
- Returns are computed using log and simple returns
- Portfolio returns are constructed using weighted asset returns
- Equity curves and drawdowns are visualized using `matplotlib`

## Key Results
- The 60/40 portfolio achieves a higher risk-adjusted return (Sharpe Ratio)
- Diversification reduces volatility with comparable drawdowns
- Demonstrates volatility drag and compounding effects

## Visualization
![Equity Curves](equity_curves.png)

## Tools & Libraries
- Python
- pandas
- numpy
- matplotlib
- yfinance
