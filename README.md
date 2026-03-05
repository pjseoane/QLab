1- Install requirements:
pip install -r requirements.txt
pip install -e ../pjs_qlab


2- to build and run from container
docker build -t streamlit_app .
docker run -p 8501:8501 streamlit_app

#to run alone
streamlit run app/main.py

# 📈 Stock Market Dashboard

An interactive stock analysis and comparison dashboard built with Streamlit, yfinance, and Plotly.

## Features
- **Candlestick & line charts** with zoom and hover tooltips
- **Technical indicators**: Moving averages (20/50/200), Bollinger Bands, RSI
- **Multi-ticker comparison** with normalised returns (base = 100)
- **Performance summary**: return, annualised volatility, max drawdown
- **Fundamentals table**: P/E, EPS, market cap, revenue, margins, beta, etc.
- **Correlation heatmap** of daily returns across tickers

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## Usage
1. Enter ticker symbols in the sidebar (comma-separated), e.g. `AAPL, MSFT, TSLA`
2. Set your date range and interval
3. Toggle indicators on/off
4. Explore the four tabs: Price Charts, Comparison, Fundamentals, Correlation

## Notes
- Data is cached for 5 minutes to avoid hammering the Yahoo Finance API
- yfinance uses Yahoo Finance's unofficial API — it's great for personal/learning projects
- Max ~8-10 tickers recommended for best performance
